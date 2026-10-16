# Plan de ES-F02-07: Cancelar despacho por anulación del pedido

**Responsable:** Tarqui.

**Estado:** Plan técnico documental preparado el 16/10/2026; implementación y verificación pendientes.

**UI:** No aplica; endpoint externo REST consumido por `modulo-ventas`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-07 | Especificación atómica SDD. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-08, CA-17, CA-18, CA-19 | Especificación funcional vigente. |
| Contrato de API | [api-contract.md §7.2](../../integraciones/api-contract.md#72-cancelar-por-anulación-del-pedido) | Endpoint canónico de cancelación externa. |
| Integración de Capacidad | [api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación) | Liberación de capacidad en Operación. |
| Arquitectura y datos | [Modelo de datos](../../arquitectura/modelo-datos.md), §1 y §3.1 | Columna `pedido_anulado` y estados terminales. |

## 2. Estrategia y responsabilidades

El controlador REST de cancelación autentica el token de servicio de Ventas exigiendo `despachos:cancelar`. Se implementa una máquina de estados controlada para evaluar si procede la cancelación directa, el registro de la marca de anulación o el rechazo por estar en ruta. La comunicación con Operación para liberar capacidad (en caso `ASIGNADO`) se realiza de forma síncrona dentro del flujo del caso de uso.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| API / Web | Endpoint `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion`, validación de token y headers. | `CancelacionDespachoController`, `CancelarDespachoRequestDTO`. |
| Aplicación | Caso de uso con evaluación de ciclo de vida e idempotencia. | `CancelarDespachoUseCase`, `IdempotenciaService`. |
| Dominio | Máquina de estados de cancelación y marca `pedidoAnulado = true`. | `Despacho`, `EstadoDespacho`. |
| Infraestructura | Cliente HTTP interno hacia Operación §5.1 y persistencia JPA. | `OperacionCapacidadClient`, `DespachoRepository`, `AuditoriaRepository`. |

## 3. Frontend y componentes React

No aplica interfaz directa de usuario. El impacto visual en el frontend administrativo se refleja de manera reactiva:
- Si el despacho estaba en la cola de pendientes (`PENDIENTE_ASIGNACION`), desaparece de la tabla y se actualiza el contador KPI.
- Si el despacho estaba en la ruta de un repartidor (`ASIGNADO`), se retira de la lista de paradas de la jornada y se recalculan las barras de capacidad del vehículo.
- Si el despacho estaba en `FALLIDO`, en la pantalla de Entregas Fallidas (F-04) se visualiza la etiqueta o badge "Pedido anulado" y se deshabilitan las opciones de reprogramación, permitiendo únicamente el cierre como devuelto a origen.

## 4. Backend, persistencia e integraciones

- **Endpoint:** `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion`.
- **Headers obligatorios:** `Authorization: Bearer <token_servicio>`, `Idempotency-Key: <UUID>`.
- **Mapeo de respuestas:**
  - `PENDIENTE_ASIGNACION`: `UPDATE despachos SET estado = 'CANCELADO', version = version + 1 WHERE ...` -> HTTP `200 OK`.
  - `ASIGNADO`: Invocar `OperacionCapacidadClient.liberarCapacidad(claveReserva)` -> `UPDATE despachos SET estado = 'CANCELADO', version = version + 1 WHERE ...` -> HTTP `200 OK`.
  - `FALLIDO`: `UPDATE despachos SET pedido_anulado = true, version = version + 1 WHERE ...` -> HTTP `202 Accepted`.
  - `EN_CAMINO`: Lanzar excepción de conflicto -> HTTP `409 Conflict` ("Despacho en traslado").
  - `ENTREGADO`, `DEVUELTO_A_ORIGEN`, `CANCELADO`: Lanzar excepción de conflicto -> HTTP `409 Conflict` (salvo que sea la misma clave de idempotencia, en cuyo caso responde el resultado previo con 200/202).
- **Auditoría:** registro de `CANCELACION_POR_ANULACION` en `historial_estados_despacho`.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Controlador REST y filtro de seguridad con scope `despachos:cancelar`. | Spring Security. | CA-07. |
| I-02 | Caso de uso con reglas de ciclo de vida (`PENDIENTE_ASIGNACION`, `FALLIDO`, `EN_CAMINO`). | Repositorio JPA. | CA-01, CA-03, CA-04, CA-05. |
| I-03 | Integración con Operación para liberación de capacidad en caso `ASIGNADO`. | Contrato Operación §5.1. | CA-02. |
| I-04 | Control de idempotencia y persistencia transaccional de auditoría. | `IdempotenciaService`. | CA-06. |

## 6. Estrategia de verificación

- Pruebas unitarias de `CancelarDespachoUseCase` probando exhaustivamente los 5 estados del despacho.
- Pruebas de integración con MockMvc y Testcontainers simulando la llamada externa desde Ventas.
- Pruebas de resiliencia con WireMock simulando respuestas de Operación al liberar capacidad.
- Pruebas de concurrencia: comprobar que una cancelación sobre `FALLIDO` incrementa la versión e impide una reprogramación concurrente sobre la misma versión.
