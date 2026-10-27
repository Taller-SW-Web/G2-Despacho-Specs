# ES-F02-07: Cancelar despacho por anulación del pedido

**Funcionalidad padre:** [F-02 — Programación y asignación de despachos](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-08, CA-17, CA-18 y CA-19.

**Responsable:** Tarqui.

**Estado:** Implementada y verificada localmente con G2 real y Seguridad temporal; aceptación humana y proveedores externos reales pendientes.

**Actor principal:** Módulo de Ventas y Postventa (token de servicio).

**Servicio propietario:** Gestión de Despachos.

**UI:** No aplica una interfaz web ni formulario directo. Es una integración externa invocada por Ventas y Postventa vía API REST; su impacto visual se manifiesta en el retiro del despacho de la cola de pendientes o de la ruta del repartidor, justificado también en [plan.md](./plan.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md). La coordinación durable, validación e idempotencia se precisan en [Común §7.2.1](../../integraciones/api-contract.md#721-coordinación-durable-y-recuperación-de-cancelaciones--es-f02-07). No se promete atomicidad distribuida: el cerco mantiene el despacho no trasladable hasta consolidar su cancelación.

## 1. Contexto y objetivo

Cuando un cliente anula su compra en los canales comerciales de la tienda, el módulo de Ventas y Postventa es responsable de notificar a Despacho para detener la entrega física del pedido.

El objetivo es atender de forma segura, recuperable e idempotente las solicitudes de cancelación que emite Ventas y Postventa. El sistema evalúa el estado del despacho en su ciclo de vida operativo: si permanece en el centro (`PENDIENTE_ASIGNACION` o `ASIGNADO`), cancela la entrega liberando la reserva si corresponde, con confirmación local atómica y coordinación durable del efecto remoto; si está en `FALLIDO`, registra la anulación (`pedidoAnulado = true`) para obligar a que F-04 solo permita cerrarlo como `DEVUELTO_A_ORIGEN`; y si ya está en traslado (`EN_CAMINO`) o terminal, rechaza informando el estado actual [cite: 1].

## 2. Alcance

- Incluye: autenticación con token de servicio y scope `despachos:cancelar`; exigencia de `Idempotency-Key` (UUID v4); evaluación del ciclo de vida del despacho; transición a `CANCELADO` para despachos en centro; retiro de la cola o de la ruta; liberación de capacidad en F-06 si estaba asignado; registro de marca `pedidoAnulado = true` en despachos `FALLIDO` respondiendo `202 Accepted`; respuestas de rechazo `409 Conflict` cuando el paquete ya salió a reparto; registro de auditoría (RT-02).
- Fuera de alcance: gestión de cobros, devoluciones monetarias o reembolsos al cliente final (Ventas y Postventa); anulación arbitraria por el Gestor sin orden de Ventas; retorno físico del paquete en ruta.

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- El sistema emisor se autentica mediante token JWT emitido por Seguridad con `sub=modulo-ventas`, `aud=api-despacho` y scope `despachos:cancelar`.
- La petición incluye un encabezado obligatorio `Idempotency-Key` con formato UUID v4 de hasta 128 caracteres.
- El despacho existe y está asociado al `idPedido` indicado en la ruta.
- El cuerpo incluye `motivo` (ej. `"PEDIDO_ANULADO"`) y opcionalmente `observacion`.

### 3.2. Dependencias

- **Ventas y Postventa:** emite la solicitud de cancelación conforme a [api-contract.md §7.2](../../integraciones/api-contract.md#72-cancelar-por-anulación-del-pedido).
- **Operación de Reparto y Flota (F-06):** recibe la solicitud de liberación de capacidad cuando el despacho cancelado estaba en estado `ASIGNADO`.
- **Entregas Fallidas (F-04):** lee la marca `pedidoAnulado` para restringir las opciones de resolución a únicamente `DEVUELTO_A_ORIGEN`.
- **Trazabilidad (ES-F02-08 / RT-02):** registra la auditoría con el usuario de servicio y motivo.

### 3.3. Resultados

- Despacho en `PENDIENTE_ASIGNACION`: cambia a `CANCELADO`, desaparece de la cola y responde `200 OK`.
- Despacho en `ASIGNADO`: cambia a `CANCELADO`, se retira de la ruta, libera capacidad en F-06 y responde `200 OK`.
- Despacho en `FALLIDO`: registra marca `pedidoAnulado = true`, conserva estado `FALLIDO` y responde `202 Accepted`.
- Despacho en `EN_CAMINO`: responde `409 Conflict` indicando que el pedido ya está en ruta de reparto.
- Despacho en `ENTREGADO`, `DEVUELTO_A_ORIGEN` o previamente `CANCELADO`: responde `409 Conflict` (o `200 OK` si se repite la misma clave de idempotencia).

## 4. Flujo principal y alternativas

1. Ventas y Postventa invoca `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion` enviando el token de servicio y la clave de idempotencia.
2. Gestión de Despachos valida el token JWT, el scope `despachos:cancelar` y el formato del payload.
3. Busca el despacho por `idPedido`. Si no existe, responde `404 Not Found`.
4. Verifica si la clave de idempotencia ya fue procesada: si ya existe respuesta previa registrada, devuelve el resultado original (HTTP 200/202).
5. Evalúa el estado actual del despacho:
   - **Caso A (`PENDIENTE_ASIGNACION`):** transiciona a `CANCELADO`, registra auditoría y devuelve `200 OK`.
   - **Caso B (`ASIGNADO`):** registra intención/cerco, solicita liberación en F-06 fuera de transacción y confirma localmente `CANCELADO`, auditoría, outbox y resultado; retira de la ruta y devuelve `200 OK`. Si no se conoce el resultado, conserva el cerco y recupera la misma operación.
   - **Caso C (`FALLIDO`):** setea `pedidoAnulado = true`, incrementa versión para control de concurrencia con F-04, registra auditoría y devuelve `202 Accepted`.
   - **Caso D (`EN_CAMINO`, `ENTREGADO`, `DEVUELTO_A_ORIGEN`):** rechaza con `409 Conflict` detallando el estado actual sin modificar el despacho.
6. En `ASIGNADO`, preparar intención y cerco durables antes de liberar por Operación §5.2; confirmar resultado, historial y outbox localmente después. Ante resultado desconocido, recuperar la misma reserva sin recrearla. En los otros casos aceptados, decisión y resultado son una sola transacción local. El flujo no mantiene transacciones durante HTTP.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Despacho en traslado | Estado actual `EN_CAMINO` | Responde `409 Conflict` ("Despacho en traslado, no es posible cancelar") | CA-04 |
| Despacho fallido | Estado actual `FALLIDO` | Registra `pedidoAnulado=true` y responde `202 Accepted` | CA-03 |
| Despacho ya finalizado | Estado `ENTREGADO`, `DEVUELTO_A_ORIGEN` o `CANCELADO` | Responde `409 Conflict` indicando estado terminal | CA-05 |
| Reintento idempotente | Misma clave de idempotencia ya aceptada | Responde el código y cuerpo original sin duplicar transiciones ni eventos | CA-06 |
| Sin scope | Token sin `despachos:cancelar` | Responde `403 Forbidden` | CA-07 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Un despacho solo puede pasar a `CANCELADO` directamente si está en `PENDIENTE_ASIGNACION` o `ASIGNADO`. | F-02 RF-08, CA-17 |
| RN-02 | Si el despacho estaba `ASIGNADO`, la cancelación debe liberar obligatoriamente la capacidad reservada en F-06. | F-02 CA-17 |
| RN-03 | Un despacho en `EN_CAMINO` no puede ser cancelado; debe completar su flujo de entrega o fallo en campo. | F-02 CA-18 |
| RN-04 | En `FALLIDO`, la cancelación registra `pedidoAnulado = true` y responde `202 Accepted`; no cambia el estado a `CANCELADO` de inmediato. | F-02 CA-19, api-contract §7.2 |
| RN-05 | La llamada exige encabezado `Idempotency-Key` (UUID v4 de hasta 128 caracteres). | api-contract §7.2 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion` | Endpoint canónico de cancelación por anulación. | [api-contract.md §7.2](../../integraciones/api-contract.md#72-cancelar-por-anulación-del-pedido) |
| Liberación de capacidad (F-06) | Liberar cupo de furgoneta cuando estaba asignado. | [api-contract-operacion-reparto.md §5.2](../../integraciones/api-contract-operacion-reparto.md#52-gestión-libera-una-reserva-en-operación) |
| Auditoría (RT-02) | Registro de la cancelación con usuario de servicio. | [ES-F02-08](../ES-F02-08-RegistrarTrazabilidadOperaciones/spec.md) |

## 6. Criterios de aceptación

### CA-01. Cancelación exitosa de despacho en PENDIENTE_ASIGNACION

- **DADO** un despacho en estado `PENDIENTE_ASIGNACION`.
- **CUANDO** Ventas y Postventa solicita su cancelación mediante `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion` con token válido e `Idempotency-Key`.
- **ENTONCES** el sistema transiciona el despacho al estado `CANCELADO`, lo retira de la cola de pendientes, registra la auditoría y responde `200 OK` con los datos del despacho cancelado.

### CA-02. Cancelación exitosa de despacho en ASIGNADO y liberación de capacidad

- **DADO** un despacho en estado `ASIGNADO` asignado a una jornada en curso.
- **CUANDO** Ventas y Postventa solicita su cancelación indicando el pedido anulado.
- **ENTONCES** el sistema cambia el estado a `CANCELADO`, lo retira de la ruta del repartidor, libera la reserva de capacidad en la furgoneta en F-06, registra la auditoría y responde `200 OK`.

### CA-03. Cancelación sobre despacho en estado FALLIDO

- **DADO** un despacho cuyo estado actual es `FALLIDO`.
- **CUANDO** Ventas y Postventa solicita su cancelación por anulación del pedido.
- **ENTONCES** el sistema registra internamente `pedidoAnulado = true` e incrementa la versión del despacho sin cambiar su estado, registra la auditoría y responde `202 Accepted` informando que el paquete será devuelto a origen una vez recibido en el centro.

### CA-04. Rechazo de cancelación sobre despacho en traslado (EN_CAMINO)

- **DADO** un despacho que ya se encuentra en estado `EN_CAMINO`.
- **CUANDO** Ventas y Postventa solicita su cancelación.
- **ENTONCES** el sistema responde `409 Conflict`, no modifica el despacho y mantiene la asignación y ruta intactas.

### CA-05. Rechazo de cancelación sobre despacho cerrado o finalizado

- **DADO** un despacho en estado `ENTREGADO`, `DEVUELTO_A_ORIGEN` o previamente `CANCELADO`.
- **CUANDO** se envía una solicitud de cancelación con una nueva clave de idempotencia.
- **ENTONCES** el sistema responde `409 Conflict` indicando que el despacho ya concluyó su ciclo de vida y no puede ser alterado.

### CA-06. Idempotencia en solicitudes repetidas de cancelación

- **DADO** que una solicitud de cancelación con clave de idempotencia UUID v4 ya fue procesada y aceptada.
- **CUANDO** se reenvía la petición con la misma clave de idempotencia y el mismo cuerpo.
- **ENTONCES** el sistema no duplica la transición, no altera la capacidad ni registra doble auditoría, y responde con el mismo código (`200 OK` o `202 Accepted`) y cuerpo previo.

### CA-07. Acceso sin autenticación o con scope insuficiente

- **DADO** una petición de cancelación sin token o sin el scope `despachos:cancelar`.
- **CUANDO** es interceptada por el filtro de seguridad.
- **ENTONCES** el sistema responde `401 Unauthorized` o `403 Forbidden` y no procesa ninguna cancelación.

## 7. Referencias

1. [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md): requisito RF-08 y criterios CA-17, CA-18 y CA-19.
2. [api-contract.md §7.2](../../integraciones/api-contract.md#72-cancelar-por-anulación-del-pedido): especificación del endpoint externo de cancelación.
