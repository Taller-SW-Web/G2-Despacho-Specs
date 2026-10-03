# ES-F02-07: Cancelar despacho por anulación del pedido

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Módulo de Ventas y Postventa (token de servicio)

## 1. Objetivo

Atender y procesar de forma segura, idempotente y controlada las solicitudes de cancelación que emite el módulo de Ventas y Postventa cuando un cliente anula su pedido comercial. El sistema evalúa el estado del despacho en su ciclo de vida: si aún permanece físicamente en el centro de despacho (`PENDIENTE_ASIGNACION` o `ASIGNADO`), cancela de inmediato la entrega liberando la reserva de capacidad en la furgoneta; si se encuentra en `FALLIDO`, registra la anulación para forzar su devolución a origen en F-04; y si el paquete ya se encuentra en traslado (`EN_CAMINO`) o en un estado final, rechaza la cancelación informando el estado actual.

## 2. Actor y precondiciones

- El sistema llamante se autentica mediante un token de servicio JWT emitido por Seguridad y Usuarios con el scope `despachos:cancelar` y audiencia `aud=api-despacho`.
- El pedido fue anulado formalmente en el módulo de Ventas y Postventa.
- Existe un despacho registrado en el módulo de Despacho asociado al `idPedido` proporcionado.

## 3. Flujo principal

1. Ventas y Postventa invoca `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion` enviando el motivo de anulación del pedido y su token de servicio.
2. El backend de Despacho valida la autenticidad del token y el scope `despachos:cancelar`.
3. El sistema busca el despacho asociado al identificador de pedido y evalúa su estado operativo vigente:
   - **Caso 1: Estado `PENDIENTE_ASIGNACION`:**
     - El despacho cambia a estado `CANCELADO`.
     - Se retira automáticamente de la cola de pendientes.
     - Se registra la auditoría con la marca temporal y el motivo.
     - El sistema responde `200 OK` con el estado final `CANCELADO`.
   - **Caso 2: Estado `ASIGNADO`:**
     - El despacho cambia a estado `CANCELADO`.
     - Se retira de la ruta del repartidor en la jornada actual y se compacta la secuencia restante.
     - Se solicita a F-06 la liberación inmediata de la reserva de capacidad en la furgoneta (peso en kg, volumen en m³ y paquetes físicos).
     - Se registra la auditoría correspondiente.
     - El sistema responde `200 OK` con el estado final `CANCELADO`.
   - **Caso 3: Estado `FALLIDO`:**
     - El despacho conserva el estado vigente `FALLIDO` (el paquete físico continúa en retorno hacia el centro).
     - Se marca el indicador `pedidoAnulado = true` en el despacho.
     - Esta marca garantiza que, cuando el paquete regrese al centro y se confirme su recepción, F-04 únicamente permita la opción de cerrar como `DEVUELTO_A_ORIGEN`, bloqueando cualquier reprogramación.
     - El sistema responde `202 Accepted` indicando que la anulación fue registrada pero el despacho espera cierre físico.
   - **Caso 4: Estado `EN_CAMINO`, `ENTREGADO` o `DEVUELTO_A_ORIGEN`:**
     - El despacho no admite cancelación directa; el backend responde `409 Conflict` informando el estado vigente.
4. Para los casos confirmados (1 y 2), se emite el evento de cambio de estado hacia los canales pertinentes.

## 4. Reglas y validaciones

- **Cancelación física viable:** la cancelación directa solo es aplicable cuando el paquete todavía se encuentra bajo custodia del centro de despacho (`PENDIENTE_ASIGNACION` o `ASIGNADO`).
- **Tratamiento de despacho en tránsito (`EN_CAMINO`):** si el repartidor ya recogió el paquete e inició su recorrido, no es posible cancelar la entrega por API; el sistema responde `409 Conflict`. El repartidor continuará su flujo hasta concretar la entrega o registrar un fallo, y Ventas recibirá el resultado final mediante los eventos regulares.
- **Tratamiento de despacho fallido (`FALLIDO`):** no transiciona a `CANCELADO`; mantiene el estado `FALLIDO` con la marca `pedidoAnulado=true` y responde `202 Accepted`. En F-04 la acción de reprogramación quedará deshabilitada obligando al cierre como `DEVUELTO_A_ORIGEN`.
- **Estados finales inmutables:** despachos en `ENTREGADO`, `DEVUELTO_A_ORIGEN` o `CANCELADO` responden `409 Conflict` indicando que el ciclo del despacho ya concluyó.
- **Liberación de capacidad en F-06:** en un despacho `ASIGNADO`, la anulación libera de inmediato y de forma transaccional la reserva de peso, volumen y paquetes de la furgoneta asignada en F-06.
- **Idempotencia:** solicitudes repetidas de cancelación para un despacho que ya se encuentra en `CANCELADO` responden `200 OK` sin duplicar transiciones ni registros en auditoría.
- **Seguridad:** peticiones sin token o sin el scope `despachos:cancelar` son rechazadas con `401 Unauthorized` o `403 Forbidden`.

## 5. Entradas, salidas e integraciones

### Entradas

- Ruta: `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion`.
- Payload JSON conforme a `integraciones/api-contract.md`:
  ```json
  {
    "motivo": "Cliente canceló la compra en marketplace",
    "fechaAnulacion": "2026-09-24T14:30:00Z"
  }
  ```
- Encabezado `Authorization: Bearer <token_servicio>`.

### Salidas

- Respuesta HTTP `200 OK` (para despachos en `PENDIENTE_ASIGNACION` o `ASIGNADO`):
  - `idDespacho`: identificador del despacho.
  - `idPedido`: referencia del pedido.
  - `estado`: `CANCELADO`.
  - `fechaCancelacion`: marca temporal en UTC.
- Respuesta HTTP `202 Accepted` (para despachos en `FALLIDO`):
  - `idDespacho`: identificador del despacho.
  - `estado`: `FALLIDO`.
  - `pedidoAnulado`: `true`.
  - `mensaje`: "Anulación registrada. El despacho será cerrado como devuelto a origen tras la recepción del paquete."
- Respuesta HTTP `409 Conflict` si el despacho está en `EN_CAMINO`, `ENTREGADO` o `DEVUELTO_A_ORIGEN`.

### Integraciones

- **Ventas y Postventa:** emite la solicitud al detectarse la anulación comercial del pedido.
- **Disponibilidad y Capacidad (F-06):** recibe la solicitud de liberación de capacidad reservada si el despacho estaba asignado.
- **Entregas Fallidas (F-04):** lee la bandera `pedidoAnulado` para restringir la decisión a únicamente `DEVUELTO_A_ORIGEN`.
- **Trazabilidad (ES-F02-08):** registra el motivo y la cancelación en el historial.
- Contrato definido en `integraciones/api-contract.md` (Sección 8).

## 6. Criterios de aceptación

### CA-01. Cancelación exitosa de despacho asignado

- **DADO** un despacho en estado `ASIGNADO` asociado al pedido `PED-2026-00891`.
- **CUANDO** Ventas y Postventa solicita su cancelación con token válido y motivo de anulación.
- **ENTONCES** el despacho cambia a `CANCELADO`, se retira de la ruta del repartidor, F-06 libera la capacidad reservada de la furgoneta, se registra la auditoría y se responde `200 OK`.

### CA-02. Cancelación exitosa de despacho pendiente

- **DADO** un despacho en estado `PENDIENTE_ASIGNACION`.
- **CUANDO** Ventas y Postventa envía la solicitud de cancelación.
- **ENTONCES** el estado cambia a `CANCELADO`, el despacho desaparece de la cola de pendientes y el backend responde `200 OK`.

### CA-03. Cancelación sobre despacho fallido (`202 Accepted`)

- **DADO** un despacho en estado `FALLIDO` cuyo paquete aún no ha sido recibido en el centro.
- **CUANDO** Ventas y Postventa solicita su cancelación.
- **ENTONCES** el sistema registra `pedidoAnulado=true`, conserva el estado `FALLIDO`, responde `202 Accepted` y, al llegar a F-04, la reprogramación queda deshabilitada.

### CA-04. Rechazo por despacho en traslado (`EN_CAMINO`)

- **DADO** un despacho que ya fue marcado en traslado (`EN_CAMINO`) por el repartidor en F-03.
- **CUANDO** Ventas y Postventa intenta solicitar su cancelación.
- **ENTONCES** el sistema responde `409 Conflict` indicando que el paquete está en ruta y no puede cancelarse de forma remota.

### CA-05. Petición repetida de cancelación (idempotencia)

- **DADO** un despacho que ya fue procesado como `CANCELADO`.
- **CUANDO** Ventas y Postventa reenvía la solicitud para ese mismo pedido.
- **ENTONCES** el sistema no duplica auditorías ni transiciones y responde `200 OK` con los datos del despacho cancelado.

### CA-06. Acceso sin permisos requeridos

- **DADO** una solicitud enviada sin token o sin el scope `despachos:cancelar`.
- **CUANDO** el backend procesa la petición.
- **ENTONCES** responde `401 Unauthorized` o `403 Forbidden` y no modifica el despacho.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Gestión de reembolsos de dinero al cliente (responsabilidad de Ventas y Postventa).
- Cancelación manual por parte del repartidor en su teléfono (el repartidor solo registra fallos con evidencia en F-03).
- Reincorporación de mercancía a inventario físico.

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-08).
- Contrato de API: `integraciones/api-contract.md` (Sección 8).
- Máquina de estados: `arquitectura/diagrama-estados-despacho.md`.
