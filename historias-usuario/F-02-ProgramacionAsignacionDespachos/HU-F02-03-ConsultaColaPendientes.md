# [HU-F02-03] Consulta y Visualización de la Cola de Despachos Pendientes

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `f-02`, `sdd`, `cola-pendientes`, `dashboard`, `kpi` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** consultar la cola de despachos pendientes mediante una tabla paginada y filtrable con tarjetas de resumen KPI en el panel administrativo  
**PARA** evaluar la carga operativa diaria, priorizar los pedidos críticos y distinguir los despachos listos para asignar hoy de aquellos programados para fechas futuras.

---

## 2. Descripción y Contexto Técnico

- **Especificación SDD origen:** [ES-F02-03: Consultar la cola de despachos pendientes](../../especificaciones/ES-F02-03-ConsultarColaPendientes/spec.md).
- **Especificación funcional padre:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisitos `RF-02` y `RF-06`; Criterios `CA-03`, `CA-04`, `CA-05`, `CA-13`).
- **Endpoints asociados:** `GET /api/v1/despachos/pendientes` (detallado en [integraciones/api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación)).
- **Parámetros de consulta:** `pagina` (int), `tamanoPagina` (int), `idZona` (string), `fechaDesde` / `fechaHasta` (date), `tipoIntento` (enum: `TODOS`, `PRIMER_INTENTO`, `REINTENTOS`).
- **Roles requeridos:** `GESTOR_DESPACHO` (autenticación JWT). Usuarios sin este rol reciben `403 Forbidden`.
- **Componentes de Frontend:**
  - Pestañas Mantine: "Cola de pendientes" y "Rutas por repartidor".
  - Fila de 3 tarjetas KPI interactivas: "Pendientes para hoy", "Programados a futuro" y "Reintentos".
  - Barra de filtros: selector de fecha, selector de zona y chips de intento.
  - Tabla de datos con columnas completas (peso en kg, volumen en m³, cantidad física de paquetes).
  - Estado vacío amigable ("No hay despachos pendientes de asignación") y botón de generar pedido de prueba.
  - Restricción visual en fecha futura: badge "Programado para [fecha]" y botón "Asignar" deshabilitado.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-03: Listado con despachos pendientes**
  - **DADO** que existen despachos registrados en estado `PENDIENTE_ASIGNACION`.
  - **CUANDO** el Gestor abre la vista de Programación y Asignación o invoca `GET /api/v1/despachos/pendientes`.
  - **ENTONCES** el sistema muestra código interno/rastreo, pedido, zona, dirección, peso, volumen, cantidad de paquetes, fecha programada, número de intento y tiempo en espera, ordenados por fecha programada ascendente con paginación estándar.

- [ ] **CA-04: Listado sin despachos pendientes**
  - **DADO** que no existen despachos pendientes en el sistema o para los filtros aplicados.
  - **CUANDO** el Gestor consulta la vista en el panel.
  - **ENTONCES** el sistema muestra el estado vacío "No hay despachos pendientes de asignación" con acceso directo a generar pedidos de prueba.

- [ ] **CA-05: Acceso sin permisos requeridos**
  - **DADO** un usuario sin rol `GESTOR_DESPACHO` o una petición anónima.
  - **CUANDO** intenta acceder a la cola de pendientes.
  - **ENTONCES** el sistema responde `403 Forbidden` y no expone información operativa.

- [ ] **CA-13: Despacho programado para una fecha futura**
  - **DADO** un despacho reprogramado por F-04 con fecha programada posterior al día actual.
  - **CUANDO** el Gestor consulta la cola en el frontend o intenta asignarlo.
  - **ENTONCES** la fila muestra el identificador "Programado para [fecha]", el botón "Asignar" se encuentra deshabilitado y el backend rechaza su asignación con `409 Conflict` hasta que llegue esa fecha.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Endpoint `GET /api/v1/despachos/pendientes` implementado con Spring Data JPA Specifications.
- [ ] Tiempo de respuesta inferior a 250 ms validado para lotes de hasta 100 registros.
- [ ] Pruebas unitarias y de integración con `JUnit 5 + MockMvc` cubriendo `CA-03`, `CA-04`, `CA-05` y `CA-13`.
- [ ] Componente React implementado con Mantine (tarjetas KPI, filtros, tabla responsive y estado vacío).
- [ ] Sincronización de filtros y paginación en la URL del navegador.
- [ ] Documentación y trazabilidad sincronizadas con [ES-F02-03](../../especificaciones/ES-F02-03-ConsultarColaPendientes/spec.md).
