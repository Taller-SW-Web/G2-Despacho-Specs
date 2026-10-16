# [HU-F02-06] Reasignación de Despacho a otro Repartidor antes del Traslado

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend, Integración |
| **Etiquetas (Labels)** | `despacho`, `f-02`, `sdd`, `reasignacion`, `capacidad`, `concurrencia` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** reasignar un despacho que aún no ha iniciado su traslado hacia otro repartidor disponible registrando obligatoriamente el motivo del cambio  
**PARA** responder ante incidencias en el centro de despacho (como averías de furgoneta o redistribución de carga), transfiriendo la reserva de capacidad sin sobrecargar al nuevo conductor.

---

## 2. Descripción y Contexto Técnico

- **Especificación SDD origen:** [ES-F02-06: Reasignar despacho a otro repartidor](../../especificaciones/ES-F02-06-ReasignarDespachoRepartidor/spec.md).
- **Especificación funcional padre:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-07`; Criterios `CA-15`, `CA-16`).
- **Endpoints asociados:** `POST /api/v1/despachos/{idDespacho}/reasignacion` (detallado en [integraciones/api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación)).
- **Roles requeridos:** `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Modal de reasignación con selector de conductor (excluye al chofer actual).
  - Proyección tridimensional de barras de capacidad del nuevo chofer.
  - Campo de texto obligatorio para el motivo de la reasignación (`Textarea`).
- **Reglas de negocio y transaccionalidad:**
  - El despacho DEBE estar en estado `ASIGNADO`. Si está en `EN_CAMINO`, `ENTREGADO` o `FALLIDO`, se responde `409 Conflict`.
  - El nuevo chofer debe contar con capacidad suficiente en kg, m³ y paquetes en F-06. Si excede cualquiera, se responde `422 Unprocessable Entity`.
  - El motivo de reasignación es estrictamente obligatorio; de omitirse, se responde `400 Bad Request`.
  - La operación transfiere las reservas en F-06, retira el paquete de la ruta previa, lo sitúa al final de la ruta del nuevo conductor (`MAX + 1`) y audita la acción con ambos choferes y el motivo.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-15: Reasignación exitosa**
  - **DADO** un despacho en estado `ASIGNADO` y otro repartidor habilitado con capacidad suficiente en F-06.
  - **CUANDO** el Gestor confirma la reasignación en `POST /api/v1/despachos/{idDespacho}/reasignacion` indicando obligatoriamente un motivo.
  - **ENTONCES** el sistema cambia el repartidor del despacho, lo ubica al final de la secuencia del nuevo repartidor, lo retira de la ruta del anterior, actualiza las reservas de capacidad en F-06 y registra la auditoría con ambos repartidores y el motivo.

- [ ] **CA-16: Reasignación de un despacho en traslado o cerrado**
  - **DADO** un despacho en cualquier estado distinto de `ASIGNADO` (`EN_CAMINO`, `ENTREGADO`, `FALLIDO`, `CANCELADO`).
  - **CUANDO** se intenta reasignarlo a otro operador.
  - **ENTONCES** el sistema responde `409 Conflict` y conserva el repartidor original sin alterar rutas ni balances.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Endpoint `POST /api/v1/despachos/{idDespacho}/reasignacion` implementado en Spring Boot.
- [ ] Orquestación de transferencia de capacidad con cliente de Operación (F-06).
- [ ] Pruebas unitarias y de integración con `JUnit 5 + MockMvc` cubriendo `CA-15` y `CA-16`.
- [ ] Modal en React con validación visual del motivo y barras de ocupación proyectadas.
- [ ] Documentación y trazabilidad sincronizadas con [ES-F02-06](../../especificaciones/ES-F02-06-ReasignarDespachoRepartidor/spec.md).
