# Tareas de ES-F02-07: Cancelar despacho por anulación del pedido

**Responsable de coordinación:** Tarqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoint de cancelación documentado en api-contract.md §7.2. | Contrato | api-contract.md | CA-01 | Completada |
| T-02 | Filtro de seguridad JWT exigiendo scope `despachos:cancelar` y verificación de `Idempotency-Key`. | Seguridad / Backend | Configuración JWT | CA-07 | Pendiente |
| T-03 | Lógica de negocio y máquina de estados de cancelación según ciclo de vida. | Backend / Dominio | Esquema `despachos` | CA-01, CA-03, CA-04, CA-05 | Pendiente |
| T-04 | Integración con cliente de Operación para liberación de capacidad en despacho `ASIGNADO`. | Backend / Integración | Contrato Operación §5.1 | CA-02 | Pendiente |
| T-05 | Mecanismo de persistencia de idempotencia para repeticiones de cancelación. | Backend / Datos | Esquema base | CA-06 | Pendiente |
| T-06 | Pruebas de integración E2E con MockMvc, WireMock y Testcontainers. | Calidad / Backend | T-01 a T-05 | CA-01 a CA-07 | Pendiente |

## 2. Detalle de tareas

### T-01. Validar contrato de API
- Alcance: confirmar método `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion`, payload y tabla de estados en [api-contract.md §7.2](../../integraciones/api-contract.md#72-cancelar-por-anulación-del-pedido).
- Comprobación: contrato revisado.

### T-02. Seguridad e idempotencia
- Alcance: `@PreAuthorize("hasAuthority('SCOPE_despachos:cancelar')")`, cabecera `Idempotency-Key` obligatoria.
- Comprobación: tests con MockMvc verificando 401 y 403.

### T-03. Máquina de estados de cancelación
- Alcance: `CancelarDespachoUseCase` implementando las ramas de negocio:
  - `PENDIENTE_ASIGNACION` -> `CANCELADO` (200).
  - `FALLIDO` -> marca `pedidoAnulado = true` (202).
  - `EN_CAMINO`, `ENTREGADO`, `DEVUELTO_A_ORIGEN` -> Conflicto (409).
- Comprobación: pruebas unitarias exhaustivas con JUnit 5.

### T-04. Liberación de capacidad en Operación
- Alcance: en caso `ASIGNADO`, llamar a `OperacionCapacidadClient.liberarCapacidad()` antes de consolidar el estado `CANCELADO`.
- Comprobación: prueba con WireMock simulando liberación exitosa.

### T-05. Persistencia idempotente y auditoría
- Alcance: comprobación y guardado en tabla de respuestas de idempotencia y registro en `historial_estados_despacho`.
- Comprobación: doble petición con la misma clave devuelve el resultado exacto previo.

### T-06. Suite de pruebas de integración
- Alcance: pruebas completas evaluando todos los estados del despacho y respuestas HTTP.
- Comprobación: 100% de tests aprobados.
