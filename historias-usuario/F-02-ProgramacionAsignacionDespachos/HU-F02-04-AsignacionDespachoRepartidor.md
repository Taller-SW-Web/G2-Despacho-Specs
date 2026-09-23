# [HU-F02-04] Asignación de Despacho a Repartidor con Validación de Capacidad

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-02`, `sdd`, `asignacion`, `capacidad` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** asignar un despacho en cola a un repartidor disponible y en turno activo validando su capacidad de carga remanente  
**PARA** garantizar que el pedido sea transportado sin exceder los límites físicos de la furgoneta ni provocar dobles asignaciones.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-03`, Criterios `CA-07`, `CA-08`, `CA-09`, `CA-10`).
- **Endpoints asociados:**
  - `POST /api/v1/despachos/{idDespacho}/asignar` (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md)).
  - Consulta de integración con Flota: `GET /api/v1/repartidores/disponibles` (provisto por F-05).
- **Roles requeridos:** `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Modal de asignación accesible desde cada fila de la cola de despachos pendientes.
  - Indicadores visuales de balance de capacidad (barras de porcentaje de peso y volumen remanente).
  - Bloqueo visual del botón de confirmación si el paquete sobrepasa la capacidad del operador seleccionado.
- **Reglas de negocio y transaccionalidad:**
  - El despacho DEBE estar en estado `PENDIENTE_ASIGNACION`. Si se encuentra en otro estado (`ASIGNADO`, `EN_CAMINO`, `ENTREGADO`), se responde `409 Conflict`.
  - El repartidor DEBE existir, tener turno activo en la fecha y estar en estado `DISPONIBLE` o `EN_RUTA`. Si está `FUERA_DE_TURNO`, `INACTIVO` o `SATURADO`, se responde `409 Conflict`.
  - Se debe verificar que `pesoDespacho <= capacidadPesoRemanente` y `volumenDespacho <= capacidadVolumenRemanente`. Si se excede cualquiera, se responde `422 Unprocessable Entity` con mensaje "Capacidad de carga del repartidor excedida".
  - Al confirmarse, Operación reserva capacidad en la furgoneta y Gestión cambia el despacho a `ASIGNADO`; una compensación libera la reserva si el segundo paso falla.
  - Control de concurrencia: uso de bloqueo optimista (`@Version`) o bloqueo pesimista en base de datos para impedir que dos gestores asignen simultáneamente el mismo despacho.
- **Entidades de datos involucradas:** `despachos`, `historial_estados_despacho`, `repartidores` (lectura/balance).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-07: Asignación exitosa dentro de la capacidad disponible**
  - **DADO** un despacho en estado `PENDIENTE_ASIGNACION` y un repartidor en estado `DISPONIBLE` cuya capacidad remanente cubre el peso y volumen del paquete.
  - **CUANDO** el Gestor selecciona al repartidor y confirma la asignación en `POST /api/v1/despachos/{idDespacho}/asignar`.
  - **ENTONCES** el sistema cambia el estado del despacho a `ASIGNADO`, descuenta la capacidad remanente del operador, registra la fecha de asignación y responde con código `200 OK`.

- [ ] **CA-08: Rechazo por capacidad de peso o volumen excedida**
  - **DADO** un despacho cuyo peso o volumen supera la capacidad remanente del repartidor seleccionado.
  - **CUANDO** el Gestor intenta confirmar la asignación.
  - **ENTONCES** el sistema bloquea la operación, responde con código `422 Unprocessable Entity`, mensaje descriptivo "Capacidad de carga del repartidor excedida" y mantiene el despacho en `PENDIENTE_ASIGNACION`.

- [ ] **CA-09: Rechazo por repartidor no disponible o fuera de turno**
  - **DADO** un repartidor que se encuentra en estado `FUERA_DE_TURNO`, `INACTIVO` o `SATURADO`.
  - **CUANDO** se intenta asignar un despacho a dicho operador.
  - **ENTONCES** el sistema rechaza la solicitud con código `409 Conflict`, detalle del motivo y mantiene el despacho en cola sin alterar balances.

- [ ] **CA-10: Despacho en estado incompatible o ya asignado**
  - **DADO** un despacho que ya fue asignado previamente por otro gestor o cuyo estado no es `PENDIENTE_ASIGNACION`.
  - **CUANDO** se intenta ejecutar una asignación concurrente o desactualizada.
  - **ENTONCES** el sistema detecta el conflicto transaccional, rechaza la operación con `409 Conflict` y notifica que el despacho ya fue procesado.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de uso de asignación implementado con `@Transactional` e integridad de datos garantizada.
- [ ] Control de concurrencia optimista implementado y validado ante peticiones simultáneas.
- [ ] Pruebas unitarias completas con `JUnit 5 + Mockito` cubriendo los 4 escenarios (`CA-07`, `CA-08`, `CA-09`, `CA-10`).
- [ ] Modal interactivo en React + Tailwind con selección de chofer, cálculo visual de capacidad en tiempo real y manejo de errores.
- [ ] Respuestas HTTP alineadas al contrato en [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
