# [HU-F02-05] Consulta y Reordenamiento de la Secuencia de Ruta

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `f-02`, `sdd`, `secuencia-ruta`, `drag-and-drop`, `repartidor` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** consultar la lista de despachos asignados a un repartidor en su jornada y reordenar manualmente su secuencia de entrega mediante arrastre o controles de teclado  
**PARA** optimizar el recorrido logístico antes de que el repartidor inicie su traslado y asegurar que la ruta visualizada en la aplicación móvil sea matemáticamente continua.

---

## 2. Descripción y Contexto Técnico

- **Especificación SDD origen:** [ES-F02-05: Consultar y reordenar la secuencia de ruta](../../especificaciones/ES-F02-05-ConsultarReordenarSecuenciaRuta/spec.md).
- **Especificación funcional padre:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-06`; Criterio `CA-14`).
- **Endpoints asociados:**
  - `GET /api/v1/jornadas/{idJornada}/ruta` (consulta de paradas).
  - `PUT /api/v1/jornadas/{idJornada}/secuencia` (actualización atómica de orden), detallados en [integraciones/api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).
- **Roles requeridos:** `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Pestaña "Rutas por repartidor" con selector de conductor en jornada.
  - Lista interactiva drag & drop (`@hello-pangea/dnd`) con botones subir/bajar accesibles.
  - Bloqueo de paradas en traslado o cerradas (`EN_CAMINO`, `ENTREGADO`, `FALLIDO`).
  - Barra inferior flotante de cambios pendientes (`BarraAccionesFija` CR-13) con botones "Guardar orden" y "Descartar".
- **Reglas de negocio:**
  - Solo los despachos en estado `ASIGNADO` admiten modificación de posición.
  - Se permutan las posiciones vigentes sin duplicados ni huecos nuevos: `1..N` para rutas nuevas; conservar los huecos históricos por retiro y las posiciones fijas, conforme a Gestión §3.2.1.
  - Actualización atómica en base de datos bajo bloqueo optimista.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-14: Reordenamiento de la secuencia de ruta**
  - **DADO** un repartidor con varios despachos en estado `ASIGNADO` en la jornada actual.
  - **CUANDO** el Gestor cambia el orden de esos despachos mediante arrastre o botones subir/bajar y confirma en `PUT /api/v1/jornadas/{idJornada}/secuencia`.
  - **ENTONCES** permuta las posiciones vigentes sin duplicados ni nuevos huecos, conserva los huecos históricos y las posiciones de no `ASIGNADO`, registra auditoría y publica proyecciones versionadas. F-03 muestra el orden tras procesarlas y consultar de nuevo, conforme a Gestión §3.2.1.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Endpoints `GET /api/v1/jornadas/{idJornada}/ruta` y `PUT /api/v1/jornadas/{idJornada}/secuencia` implementados en Spring Boot.
- [ ] Validador de permutación continua `1..N` e inmutabilidad de paradas iniciadas implementado.
- [ ] Pruebas unitarias y de integración con `JUnit 5 + MockMvc` verificando validación de secuencia, estados bloqueados y concurrencia.
- [ ] Componente drag & drop en React con soporte de teclado y barra flotante de confirmación.
- [ ] Documentación y trazabilidad sincronizadas con [ES-F02-05](../../especificaciones/ES-F02-05-ConsultarReordenarSecuenciaRuta/spec.md).
