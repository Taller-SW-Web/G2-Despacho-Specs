# Tareas de ES-F02-03: Consultar la cola de despachos pendientes

**Responsable de coordinación:** Tarqui.

**Estado:** Backend implementado y verificado localmente; pantalla e integración frontend pendientes. Ver [evidence.md](./evidence.md).

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Parámetros y DTOs de respuesta de cola documentados en Gestión §3.2. | Contrato | api-contract-gestion-despachos.md | CA-01 | Completada |
| T-02 | Consulta SQL parametrizada de filtros dinámicos (zona, fechas, tipoIntento). | Backend / Datos | Esquema `despachos` | CA-01, CA-02 | Verificada localmente |
| T-03 | Caso de uso con cálculo de contadores KPI e integración de paginación. | Backend / Dominio | T-02 | Parte backend de CA-01 a CA-05 | Verificada localmente |
| T-04 | Controlador REST protegido mediante Spring Security y rol `GESTOR_DESPACHO`. | Backend / API | T-03 | CA-06 | Verificada localmente |
| T-05 | Pruebas de integración de backend con MockMvc y PostgreSQL real. | Calidad / Backend | T-04 | Parte backend de CA-01 a CA-06 | Aprobada con PostgreSQL externo; ver evidencia |
| T-06 | Componentes React: BarraFiltros, TarjetaKpi y TablaDatos en Mantine. | Frontend / UI | CR-06, CR-07, CR-10 | CUI-01, CUI-02 | Pendiente |
| T-07 | Lógica de presentación de fechas futuras, badges y estado vacío. | Frontend / UI | T-06 | CUI-03, CUI-04 | Pendiente |
| T-08 | Conexión con la API real mediante React Query y sincronización de URL. | Integración UI | T-04, T-07 | CUI-05, CUI-06 | Pendiente |

## 2. Detalle de tareas

### T-01. Contrato y DTOs
- Alcance: `ColaPendientesResponseDTO`, `DespachoResumenDTO` y `MetricasKpiDTO`.
- Comprobación: esquemas validados con Swagger / OpenAPI.

### T-02. Filtros SQL dinámicos
- Alcance: consultas parametrizadas en `ProgramacionPersistencia`, siguiendo el patrón JDBC existente de F-04; estado pendiente, fechas inclusivas y transición histórica estructurada para reintentos.
- Comprobación: PostgreSQL real con diversas combinaciones de filtros.

### T-03. Caso de uso y KPIs
- Alcance: `ConsultarColaPendientesUseCase` calculando `pendientesHoy`, `programadosFuturo` y `reintentos` de forma optimizada.
- Comprobación: tests unitarios con JUnit 5.

### T-04. Endpoint REST
- Alcance: `GET /api/v1/despachos/pendientes` con mapeo de parámetros y manejo de excepciones.
- Comprobación: respuesta HTTP 200 con paginación y 403 sin rol.

### T-05. Pruebas de integración
- Alcance: suite de integración con PostgreSQL real, mediante Testcontainers o base externa exclusiva de pruebas, evaluando orden, filtros y estados vacíos.
- Comprobación: 100% de tests aprobados.

### T-06. Componentes visuales
- Alcance: composición en React con componentes compartidos CR, tarjetas KPI y tabla adaptable a escritorio y tableta.
- Comprobación: pruebas con Storybook / Vitest.

### T-07. Reglas de interfaz
- Alcance: badge "Simulado", badge "Programado para [fecha]" y botón "Asignar" deshabilitado condicionalmente.
- Comprobación: renderizado verificado con pruebas de componentes.

### T-08. Integración con React Query
- Alcance: custom hook `useColaPendientes` con query params bidireccionales en la URL.
- Comprobación: navegación de filtros y recarga de página probadas.
