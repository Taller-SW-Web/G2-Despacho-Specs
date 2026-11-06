# ES-F03-09: Recojo de una devolución en el domicilio

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-12.

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor

**UI:** Aplica; ruta, detalle y formularios de la web responsive del repartidor.

**Servicio propietario:** Operación de Reparto y Flota para la operación en campo; Gestión de Despachos para el estado del recojo.

## 1. Contexto y objetivo

El cliente puede devolver un producto que ya recibió. El repartidor va al domicilio, recoge el producto, deja una foto como evidencia y lo lleva al centro de despacho. Si no puede recogerlo, registra el motivo y una foto. Visión general en [overview §12](../../overview.md#12-devolución-del-producto).

## 2. Alcance

- Incluye: ver los recojos en «Mi Ruta» cuando la jornada es de tipo `RECOJOS`, consultar su detalle, iniciar el traslado, registrar el recojo o el no recojo y el efecto del cierre de jornada.
- Fuera de alcance: aprobar la devolución, reembolso o cambio (Ventas y Postventa); abrir la jornada y elegir su tipo ([ES-F06-09](../ES-F06-09-TipoOperacionJornada/spec.md)); asignar el recojo ([ES-F02-09](../ES-F02-09-RecibirAsignarRecojo/spec.md)); confirmar la recepción en el centro, reprogramar o cerrar ([ES-F04-07](../ES-F04-07-RecibirResolverRecojo/spec.md)); calcular la ocupación (F-06).

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor con perfil local activo y vinculado, resuelto desde el `sub` del JWT.
- Precondiciones: el recojo está asignado al repartidor en su jornada activa de hoy, de tipo `RECOJOS`, y hay conexión.
- Disparador: el repartidor abre un recojo de su ruta.
- Resultado exitoso: recojo en `RECOGIDO` o `FALLIDO`, con evidencia e historial.
- Resultado ante rechazo: se informa el error y el recojo no cambia.

## 4. Flujo principal y alternativas

1. El repartidor abre el recojo en «Mi Ruta» y ve dirección, contacto y productos.
2. Pulsa «En camino»; el recojo pasa a `EN_CAMINO`.
3. En el domicilio, recoge el producto y toma la foto.
4. Pulsa «Confirmar recojo»; el recojo pasa a `RECOGIDO`.
5. La interfaz le recuerda llevar el producto al centro de despacho.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| No puede recoger | Cliente ausente, producto no entregado u otro motivo | Registra motivo y foto; pasa a `FALLIDO` | CA-05 |
| Sin foto o sin motivo | Falta un dato obligatorio | Envío bloqueado | CA-04, CA-06 |
| Sin conexión | La petición no llega al backend | Aviso, datos conservados y reintento explícito | CA-08 |
| Reintento | Misma clave de idempotencia | Resultado original sin duplicados | CA-09 |
| Recojo cambiado | Cancelado, reasignado o de otro repartidor | `409` o `404`; se actualiza la ruta | CA-07 |
| Fin de jornada | Recojo en `ASIGNADO` o `EN_CAMINO` | Pasa a `FALLIDO` con `NO_INTENTADO` | CA-10 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | El recojo es una operación aparte del despacho. El despacho original permanece en `ENTREGADO`. | Overview §12; [estados §7](../../arquitectura/diagrama-estados-despacho.md#7-estados-del-recojo) |
| RN-02 | El tipo de la jornada define el trabajo del repartidor: `ENTREGAS` muestra solo despachos y `RECOJOS` solo recojos. La aplicación y el acceso son los mismos, y una jornada nunca mezcla ambos. | [ES-F06-09](../ES-F06-09-TipoOperacionJornada/spec.md) |
| RN-03 | Teléfono y dirección solo se muestran en `ASIGNADO` y `EN_CAMINO`, igual que en un despacho. | F-03, sección 8 |
| RN-04 | `RECOGIDO` y `FALLIDO` solo se aceptan desde `EN_CAMINO`, y exigen una foto válida. | Overview §12.2 |
| RN-05 | La foto cumple la política de evidencia de F-03: tipo, tamaño y carga verificada. | ES-F03-05 RN-01, RN-03 y RN-04 |
| RN-06 | El motivo es obligatorio en `FALLIDO` y debe ser del catálogo con ámbito `RECOJO` o `AMBOS`. | [Gestión §4](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo) |
| RN-07 | El contador de intentos del recojo aumenta solo con un intento real y no afecta al despacho. | Decisión de esta especificación |
| RN-08 | Un recojo `RECOGIDO` ocupa capacidad hasta que Operación confirma la liberación solicitada por la recepción en el centro. Un `FALLIDO` la libera al registrarse, porque no hay producto a bordo. | Overview §12.2; F-06 §4.5 |
| RN-09 | Al cerrar la jornada, un recojo `ASIGNADO` o `EN_CAMINO` pasa a `FALLIDO` con `NO_INTENTADO`, sin foto ni consumo de intento. Uno `RECOGIDO` no cambia y aparece en el resumen como producto por entregar. | F-03 RF-07 |
| RN-10 | Turno, idempotencia, historial y falta de conexión siguen las reglas de ES-F03-04. | ES-F03-04 RN-04 y RN-06 a RN-08 |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| Ruta del repartidor | Lista los recojos | [Operación §3.1](../../integraciones/api-contract-operacion-reparto.md#31-consultar-ruta-detalle-y-resumen) |
| Comandos de recojo | Detalle, inicio, recojo y no recojo | [Operación §3.7](../../integraciones/api-contract-operacion-reparto.md#37-recojo-de-una-devolución) |
| Evidencia | Autorizar la carga y leer la foto | [Operación §3.2](../../integraciones/api-contract-operacion-reparto.md#32-autorizar-la-carga-de-evidencia) y [§3.5](../../integraciones/api-contract-operacion-reparto.md#35-autorizar-la-lectura-de-evidencia) |
| Transición en Gestión | Cambiar y registrar el estado | [Gestión §6.3](../../integraciones/api-contract-gestion-despachos.md#63-operación-solicita-una-transición-de-recojo) |
| Tipo de jornada, asignación y recepción | Pasos previos y posteriores | [ES-F06-09](../ES-F06-09-TipoOperacionJornada/spec.md), [ES-F02-09](../ES-F02-09-RecibirAsignarRecojo/spec.md) y [ES-F04-07](../ES-F04-07-RecibirResolverRecojo/spec.md) |

Estas operaciones son una propuesta: deben revisarse antes de implementarlas y quedan sujetas al acuerdo con Ventas y Postventa.

## 6. Criterios de aceptación

### CA-01. Recojo visible en la ruta

- **DADO** un repartidor con una jornada activa de tipo `RECOJOS` y un recojo `ASIGNADO`.
- **CUANDO** abre «Mi Ruta».
- **ENTONCES** ve solo recojos, en el orden de la jornada, identificados como «Recojo», con dirección, contacto y estado.

### CA-02. Inicio del traslado

- **DADO** un recojo `ASIGNADO`.
- **CUANDO** el repartidor pulsa «En camino».
- **ENTONCES** el recojo pasa a `EN_CAMINO` con marca temporal del servidor y ejecutor.

### CA-03. Recojo exitoso

- **DADO** un recojo `EN_CAMINO`.
- **CUANDO** el repartidor adjunta la foto y pulsa «Confirmar recojo».
- **ENTONCES** el recojo pasa a `RECOGIDO`, se asocia la evidencia, el despacho original sigue `ENTREGADO`, se registra el evento `RECOJO_RECOGIDO` y la interfaz recuerda llevar el producto al centro.

### CA-04. Recojo sin foto

- **DADO** el formulario de recojo sin foto.
- **CUANDO** el repartidor intenta confirmar.
- **ENTONCES** el botón sigue deshabilitado, se indica que la foto es obligatoria y no se envía la petición.

### CA-05. Recojo no realizado

- **DADO** un recojo `EN_CAMINO` que no pudo realizarse.
- **CUANDO** el repartidor selecciona un motivo, adjunta la foto y confirma.
- **ENTONCES** el recojo pasa a `FALLIDO`, el contador del recojo aumenta en uno, se solicita liberar su capacidad, se registra `RECOJO_FALLIDO` y queda disponible para que el Gestor decida en F-04.

### CA-06. Motivo ausente o no válido

- **DADO** el formulario de no recojo.
- **CUANDO** falta el motivo, o se fuerza uno inactivo, no seleccionable o de ámbito `ENTREGA`.
- **ENTONCES** la interfaz bloquea el envío o el backend responde `400 DESP_ERROR_MOTIVO_INVALIDO`, sin cambiar el estado.

### CA-07. Recojo ajeno o actualizado

- **DADO** un recojo de otro repartidor, o uno cancelado o reasignado mientras seguía en pantalla.
- **CUANDO** el repartidor intenta consultarlo u operarlo.
- **ENTONCES** recibe `404` si es ajeno o `409` si cambió, sin datos parciales ni cambios, y la interfaz actualiza la ruta.

### CA-08. Pérdida de conexión

- **DADO** que el repartidor confirma una operación.
- **CUANDO** la petición no llega al backend.
- **ENTONCES** la interfaz informa que el cambio no se registró, conserva foto y datos, y exige un reintento explícito.

### CA-09. Reintento idempotente

- **DADO** un reintento con la misma clave de idempotencia.
- **CUANDO** llega al backend.
- **ENTONCES** devuelve el resultado original sin duplicar transición, contador, evidencia, historial ni evento.

### CA-10. Cierre de jornada

- **DADO** una jornada con un recojo `EN_CAMINO` y otro `RECOGIDO`.
- **CUANDO** el repartidor cierra la jornada.
- **ENTONCES** el primero pasa a `FALLIDO` con `NO_INTENTADO` sin consumir intento, el segundo no cambia y el resumen lo lista en `productosPorEntregar`.

### CA-11. Historial

- **DADO** una transición de recojo aceptada.
- **CUANDO** se persiste.
- **ENTONCES** el historial del recojo guarda ejecutor, origen, marca temporal del servidor, estados anterior y nuevo, motivo y observaciones, en la misma transacción.

### CA-12. Jornada de entregas

- **DADO** un repartidor con una jornada activa de tipo `ENTREGAS`.
- **CUANDO** abre «Mi Ruta» o intenta abrir un recojo.
- **ENTONCES** ve solo despachos, con las mismas pantallas y textos de siempre, y el recojo responde `404`.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: Operación valida perfil, jornada, propiedad y evidencia; Gestión aplica el estado, el historial y el evento.
- No funcionales: los de F-03, sección 8; la evidencia nunca es pública.
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración y UI | Jornada `RECOJOS` con un recojo `ASIGNADO` |
| CA-02 | Integración y UI | Recojo `ASIGNADO` |
| CA-03 | Integración y UI | Recojo `EN_CAMINO` y foto válida |
| CA-04 | UI | Formulario sin foto |
| CA-05 | Integración y UI | Recojo `EN_CAMINO`, motivo válido y foto |
| CA-06 | Integración y UI | Sin motivo; motivo de ámbito `ENTREGA`; `NO_INTENTADO` forzado |
| CA-07 | Integración y UI | Recojo ajeno, cancelado y reasignado |
| CA-08 | UI | Falta de señal al confirmar |
| CA-09 | Integración | Dos solicitudes con la misma clave |
| CA-10 | Integración | Cierre con recojos `EN_CAMINO` y `RECOGIDO` |
| CA-11 | Integración | Transición aceptada |
| CA-12 | Integración y UI | Jornada `ENTREGAS` con despachos |

- [ ] Todos los criterios cuentan con resultados comprobables en `evidence.md`.
- [ ] Los documentos, el contrato y el comportamiento implementado son consistentes.
- [ ] Los pendientes bloqueantes están resueltos y la revisión del equipo está registrada.

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-12, CA-32 a CA-36.
2. [Contrato de Operación §3.7](../../integraciones/api-contract-operacion-reparto.md#37-recojo-de-una-devolución), [Gestión §3.3](../../integraciones/api-contract-gestion-despachos.md#33-recojos-de-devoluciones) y [contrato externo §7.4](../../integraciones/api-contract.md#74-solicitar-y-cancelar-el-recojo-de-una-devolución).
3. [Estados del recojo](../../arquitectura/diagrama-estados-despacho.md#7-estados-del-recojo) y [modelo de datos §3.6](../../arquitectura/modelo-datos.md#36-recojos-de-devoluciones).
4. Archivos de esta especificación: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
