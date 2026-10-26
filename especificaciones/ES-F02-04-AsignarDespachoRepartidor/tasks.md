# Tareas de ES-F02-04: Asignar despacho a un repartidor

**Responsable de coordinación:** Tarqui.

**Estado:** Backend de Gestión implementado y verificado con Operación HTTP simulada; proveedor real y frontend funcional pendientes. Ver [evidence.md](./evidence.md).

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoint de asignación documentado en Gestión §3.2 y Operación §5.1. | Contrato | api-contract-gestion-despachos.md | CA-01 | Completada |
| T-02 | Cliente HTTP interno hacia Operación para validación y reserva tridimensional. | Integración interna | Contrato Operación §5.1 | CA-01, CA-02, CA-03 | Verificada con doble HTTP |
| T-03 | Lógica de secuencia de ruta incremental y asignación transaccional con `@Version`. | Backend / Dominio | Esquema `despachos` | CA-01, CA-04, CA-05 | Verificada localmente |
| T-04 | Mecanismo durable de compensación de reserva ante fallos transaccionales locales. | Backend / Resiliencia | T-02, T-03 | CA-01 | Verificada localmente |
| T-05 | `ControladorProgramacion` protegido mediante Spring Security y rol `GESTOR_DESPACHO`. | Backend / API | T-03 | CA-07 | Verificada localmente |
| T-06 | Pruebas de backend con PostgreSQL real, JWT firmados y dobles HTTP. | Calidad / Backend | T-05 | Parte de Gestión de CA-01 a CA-07 | Aprobada con PostgreSQL externo; ver evidencia |
| T-07 | Componente React `ModalAsignacionDespacho` con barras Mantine (CR-11, CR-20). | Frontend / UI | CR-11, CR-12, CR-20 | CUI-01 a CUI-05 | Pendiente |
| T-08 | Conexión con React Query, invalidación de cola y feedback toast. | Integración UI | T-05, T-07 | CUI-06 | Pendiente |

## 2. Detalle de tareas

### T-01. Contratos de integración
- Alcance: confirmar payload de asignación `{ idRepartidor, idJornada, observacion? }` y endpoint interno de reserva en Operación.
- Comprobación: contratos verificados.

### T-02. Cliente REST de Operación
- Alcance: `CapacidadProgramacionHttp` con reserva y liberación POST según Operación §§5.1–5.2, manejando 200, 409 y 422.
- Comprobación: pruebas con servidor HTTP del JDK, identificado como doble del proveedor.

### T-03. Caso de uso AsignarDespachoUseCase
- Alcance: validación de estado `PENDIENTE_ASIGNACION`, fecha de hoy, bloqueo optimista, cálculo de `posicionSecuencia = MAX + 1` y cambio a `ASIGNADO`.
- Comprobación: tests unitarios con JUnit 5.

### T-04. Servicio de compensación
- Alcance: registrar intención y clave antes del HTTP; capturar fallos posteriores a la reserva, invocar liberación y conservar una compensación durable recuperable si falla.
- Comprobación: test de compensación simulando fallo en `saveAndFlush`.

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
