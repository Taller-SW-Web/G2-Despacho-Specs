# Tareas de ES-F02-04: Asignar despacho a un repartidor

**Responsable de coordinación:** Tarqui.

**Estado:** Ejecución parcial; modal con barras verificado localmente, integración backend/nube y aceptación pendientes.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoint de asignación documentado en Gestión §3.2 y Operación §5.1. | Contrato | api-contract-gestion-despachos.md | CA-01 | Completada |
| T-02 | Cliente HTTP interno hacia Operación para validación y reserva tridimensional. | Integración interna | Contrato Operación §5.1 | CA-01, CA-02, CA-03 | Pendiente |
| T-03 | Lógica de secuencia de ruta incremental y asignación transaccional con `@Version`. | Backend / Dominio | Esquema `despachos` | CA-01, CA-04, CA-05 | Pendiente |
| T-04 | Mecanismo de compensación de reserva ante fallos transaccionales locales. | Backend / Resiliencia | T-02, T-03 | CA-01 | Pendiente |
| T-05 | Controlador REST `AsignacionController` con autorización `@PreAuthorize`. | Backend / API | T-03 | CA-07 | Pendiente |
| T-06 | Pruebas de integración de backend con WireMock y Testcontainers. | Calidad / Backend | T-05 | CA-01 a CA-07 | Pendiente |
| T-07 | Componente React `ModalAsignacion` con barras Mantine (CR-11, CR-20). | Frontend / UI | CR-11, CR-12, CR-20 | CUI-01 a CUI-05 | Implementada localmente; verificación con API simulada en EV-04; aceptación real pendiente |
| T-08 | Conexión con React Query, invalidación de cola y feedback toast. | Integración UI | T-05, T-07 | CUI-06 | Pendiente |

## 2. Detalle de tareas

### T-01. Contratos de integración
- Alcance: confirmar payload de asignación `{ idRepartidor, idJornada, observacion? }` y endpoint interno de reserva en Operación.
- Comprobación: contratos verificados.

### T-02. Cliente REST de Operación
- Alcance: `CapacidadProgramacionHttp` para reserva y liberación según las operaciones canónicas de Operación §§5.1/5.2, manejando 200, 409 y 422. No utilizar el DELETE previsto históricamente.
- Comprobación: pruebas con WireMock.

### T-03. Caso de uso AsignarDespachoUseCase
- Alcance: validación de estado `PENDIENTE_ASIGNACION`, fecha de hoy, bloqueo optimista, cálculo de `posicionSecuencia = MAX + 1` y cambio a `ASIGNADO`.
- Comprobación: tests unitarios con JUnit 5.

### T-04. Servicio de compensación
- Alcance: `AsignarDespacho` conserva la intención y compensación durables; consulta si hubo confirmación antes de liberar y aplaza los fallos recuperables. HTTP fuera de transacciones locales.
- Comprobación: `ProgramacionHttpTests` incluye fallos posteriores a reserva y recuperación; requiere PostgreSQL desechable. Su ejecución completa en esta sesión quedó bloqueada por Docker; no se declara aprobada.

### T-05. Controlador REST
- Alcance: `POST /api/v1/despachos/{idDespacho}/asignacion` exigiendo rol `GESTOR_DESPACHO`.
- Comprobación: validación con MockMvc.

### T-06. Suite de integración
- Alcance: pruebas E2E de backend cubriendo asignación exitosa, sobrecarga en kg, m³ y paquetes, chofer inhabilitado y concurrencia.
- Comprobación: 100% aprobado.

### T-07. Modal React
- Alcance: interfaz modal con tarjeta de despacho, lista de repartidores agrupados por zona, proyección tridimensional con rayado sobre barras de progreso y validaciones visuales.
- Comprobación: pruebas de UI con Vitest y Testing Library.

### T-08. Integración completa en frontend
- Alcance: apertura desde el botón "Asignar" de la tabla, mutación con TanStack Query y cierre reactivo con toast.
- Comprobación: flujo de asignación manual o con Playwright.
