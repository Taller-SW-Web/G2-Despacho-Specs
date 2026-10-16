# Tareas de ES-F02-06: Reasignar despacho a otro repartidor

**Responsable de coordinación:** Tarqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoint de reasignación documentado en Gestión §3.2. | Contrato | api-contract-gestion-despachos.md | CA-01, CA-02 | Completada |
| T-02 | Orquestación de transferencia de capacidad con cliente de Operación (F-06). | Backend / Integración | Contrato Operación §5.1 | CA-01, CA-03 | Pendiente |
| T-03 | Caso de uso `ReasignarDespachoUseCase` con validación de estado ASIGNADO y recálculo de secuencia. | Backend / Dominio | T-02 | CA-01, CA-04, CA-05 | Pendiente |
| T-04 | Controlador REST `ReasignacionController` con `@PreAuthorize` y Bean Validation. | Backend / API | T-03 | CA-02, CA-06, CA-07 | Pendiente |
| T-05 | Pruebas de integración de backend con WireMock y Testcontainers. | Calidad / Backend | T-04 | CA-01 a CA-07 | Pendiente |
| T-06 | Modal React `ModalReasignacionDespacho` con exclusión de chofer actual y campo obligatorio de motivo. | Frontend / UI | CR-02, CR-11, CR-12, CR-20 | CUI-01 a CUI-04 | Pendiente |
| T-07 | Conexión con React Query y recarga reactiva de rutas en la interfaz. | Integración UI | T-04, T-06 | CUI-05 | Pendiente |

## 2. Detalle de tareas

### T-01. Confirmar contrato
- Alcance: verificar payload `{ idNuevoRepartidor, idNuevaJornada, motivo }` en [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).
- Comprobación: contrato revisado.

### T-02. Transferencia de capacidad
- Alcance: llamadas coordinadas a Operación: reservar en chofer destino y liberar en chofer origen.
- Comprobación: tests con WireMock simulando escenarios de sobrecarga en el nuevo chofer (422).

### T-03. Caso de uso
- Alcance: `ReasignarDespachoUseCase` comprobando `@Version`, estado `ASIGNADO` y posicionamiento al final de la ruta del nuevo conductor.
- Comprobación: pruebas unitarias con JUnit 5.

### T-04. Controlador REST
- Alcance: `POST /api/v1/despachos/{idDespacho}/reasignacion` con validaciones de motivo y rol `GESTOR_DESPACHO`.
- Comprobación: pruebas con MockMvc verificando errores 400 y 403.

### T-05. Pruebas de integración
- Alcance: suite completa verificando éxito, chofer inhabilitado y concurrencia ante inicio de traslado en F-03.
- Comprobación: 100% de tests aprobados.

### T-06. Componente Modal React
- Alcance: modal Mantine con exclusión del conductor actual, validación visual de motivo no vacío y barras de ocupación proyectadas.
- Comprobación: tests de UI con Testing Library.

### T-07. Integración frontend
- Alcance: apertura desde el botón "Reasignar" de la parada, mutación y feedback con toast Mantine.
- Comprobación: verificación manual o E2E con Playwright.
