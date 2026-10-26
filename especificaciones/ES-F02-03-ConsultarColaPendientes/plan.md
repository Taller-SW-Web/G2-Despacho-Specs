# Plan de ES-F02-03: Consultar la cola de despachos pendientes

**Responsable:** Tarqui.

**Estado:** Backend implementado y verificado localmente; frontend funcional pendiente. Ejecución en [evidence.md](./evidence.md).

**UI:** Aplica; página `/programacion`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-06 | Especificación atómica SDD. |
| UI | [ui.md](./ui.md), UI-01, UI-02, CUI-01 a CUI-06 | Especificación de interfaz. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-02, RF-06 | Especificación funcional vigente. |
| Contrato de API | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) | Parámetros y respuestas de la cola de pendientes. |
| Componentes React | [componentes-react.md](../../disenio/componentes-react.md), CR-03, CR-05 a CR-10 | Componentes Mantine compartidos. |

## 2. Estrategia y responsabilidades

El backend implementa una consulta paginada con SQL parametrizado mediante el patrón JDBC existente de F-04. Calcula las 3 métricas de resumen mediante agregación e índices, dentro de una lectura consistente. Las escrituras del agregado utilizan JPA con `@Version`. La pantalla prevista bajo `ShellAdministrativo`, React Query y React Router permanece pendiente.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| Frontend | Vista de cola, filtros, KPIs, tabla paginada y modal launcher. | `PaginaProgramacion.tsx`, `TablaColaPendientes.tsx`, `BarraFiltrosCola.tsx`. |
| API / Web | Controlador REST con parámetros de consulta y autorización JWT. | `ConsultaColaPendientesController`, `ColaPendientesResponseDTO`. |
| Aplicación | Caso de uso con filtros dinámicos, cálculo de KPIs y paginación. | `ConsultarColaPendientesUseCase`. |
| Dominio | Especificación JPA de búsqueda y lógica de tipos de intento. | `DespachoSpecification`, `TipoIntentoFiltro`. |
| Infraestructura | Consultas a PostgreSQL indexadas por `estado` y `fecha_programada`. | `DespachoRepository`. |

## 3. Frontend y componentes React

- **Contenedor:** `PaginaProgramacion` gestiona la pestaña activa (`Tabs`), query parameters de la URL y peticiones a través de `useQuery(['despachos-pendientes', filtros])`.
- **KPIs (CR-10):** tarjetas clicables con contadores devueltos en la respuesta de la API.
- **Tabla (CR-07):** maneja ordenamiento visual, truncado de texto y formato numérico (kg con 1 decimal, m³ con 3 decimales).
- **Acceso a Asignación:** el botón "Asignar" abre el modal de asignación de [ES-F02-04](../ES-F02-04-AsignarDespachoRepartidor/spec.md) inyectando el objeto despacho seleccionado.

## 4. Backend, persistencia e integraciones

- **Endpoint:** `GET /api/v1/despachos/pendientes`.
- **Query params:** `pagina` (default 1), `tamanoPagina` (default 20), `idZona`, `fechaDesde`, `fechaHasta`, `tipoIntento` (`TODOS`, `PRIMER_INTENTO`, `REINTENTOS`).
- **Seguridad:** `@PreAuthorize("hasRole('GESTOR_DESPACHO')")`.
- **Persistencia:**
  - Predicado base: `estado = 'PENDIENTE_ASIGNACION'`.
  - Filtro `tipoIntento = REINTENTOS`: existencia de una transición histórica estructurada de F-04 desde `FALLIDO` a `PENDIENTE_ASIGNACION` con `datos.nuevaFechaProgramada`; no usar texto libre ni el contador de fallos.
  - Ordenamiento: `ORDER BY fecha_programada ASC, creado_en ASC`.
- **Índices recomendados:** `CREATE INDEX idx_despachos_cola ON despachos (estado, fecha_programada) WHERE estado = 'PENDIENTE_ASIGNACION'`.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Especificación JPA, repositorio y caso de uso backend. | Esquema PostgreSQL `despachos`. | CA-01, CA-02. |
| I-02 | Controlador REST con cálculo de KPIs y paginación. | I-01, Spring Security JWT. | CA-01, CA-03, CA-04, CA-06. |
| I-03 | Componentes de UI: tabla, filtros, tarjetas KPI y sincronización URL. | I-02, componentes Mantine CR. | CUI-01 a CUI-06. |

## 6. Estrategia de verificación

- Pruebas unitarias de especificaciones JPA con datos de prueba en H2 / Testcontainers.
- Pruebas de integración con MockMvc evaluando filtros combinados, fechas y seguridad.
- Pruebas de rendimiento con JMeter o Gatling verificando respuesta < 250 ms con 10,000 despachos en base de datos.
- Pruebas de componentes React con Vitest verificando renderizado de columnas y deshabilitación por fecha futura.
