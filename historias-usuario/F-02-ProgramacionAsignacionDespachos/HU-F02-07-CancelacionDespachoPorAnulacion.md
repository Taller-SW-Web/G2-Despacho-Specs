# [HU-F02-07] Cancelación de Despacho por Anulación del Pedido

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Integración, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `f-02`, `sdd`, `cancelacion`, `ventas`, `idempotencia` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Sistema Comercial (Ventas y Postventa)  
**QUIERO** notificar la anulación de un pedido comercial mediante un endpoint REST formal con clave de idempotencia  
**PARA** que el módulo de despacho cancele la entrega antes de su salida liberando la capacidad de la furgoneta o marque el paquete como anulado si está fallido, evitando entregas erróneas.

---

## 2. Descripción y Contexto Técnico

- **Especificación SDD origen:** [ES-F02-07: Cancelar despacho por anulación del pedido](../../especificaciones/ES-F02-07-CancelarDespachoPorAnulacion/spec.md).
- **Especificación funcional padre:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-08`; Criterios `CA-17`, `CA-18`, `CA-19`).
- **Endpoints asociados:** `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion` (detallado en [integraciones/api-contract.md §7.2](../../integraciones/api-contract.md#72-cancelar-por-anulación-del-pedido)).
- **Autenticación:** token de servicio JWT emitido por Seguridad con `sub=modulo-ventas`, `aud=api-despacho` y scope `despachos:cancelar`.
- **Encabezados obligatorios:** `Authorization: Bearer <token>`, `Idempotency-Key: <UUID v4>`.
- **Reglas de negocio por estado:**
  - `PENDIENTE_ASIGNACION`: transiciona directamente a `CANCELADO`, lo retira de la cola y responde `200 OK`.
  - `ASIGNADO`: transiciona a `CANCELADO`, lo retira de la ruta, libera la capacidad en F-06 y responde `200 OK`.
  - `FALLIDO`: registra internamente `pedidoAnulado = true`, incrementa la versión para concurrencia, responde `202 Accepted` y restringe a F-04 para que solo permita cerrarlo como `DEVUELTO_A_ORIGEN`.
  - `EN_CAMINO`: responde `409 Conflict` indicando que el paquete está en traslado.
  - `ENTREGADO`, `DEVUELTO_A_ORIGEN` o previamente `CANCELADO`: responde `409 Conflict` (salvo repetición idempotente con la misma clave, que responde el resultado previo).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-17: Cancelación antes del traslado**
  - **DADO** un despacho en estado `PENDIENTE_ASIGNACION` o `ASIGNADO`.
  - **CUANDO** Ventas y Postventa solicita su cancelación indicando el pedido anulado en `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion`.
  - **ENTONCES** el sistema cambia el estado a `CANCELADO`, lo retira de la cola o de la ruta del repartidor, libera la reserva de capacidad en F-06 si estaba asignado, registra la auditoría y responde `200 OK` con el estado resultante.

- [ ] **CA-18: Cancelación de un despacho en traslado o cerrado**
  - **DADO** un despacho en estado `EN_CAMINO`, `ENTREGADO`, `DEVUELTO_A_ORIGEN` o previamente `CANCELADO`.
  - **CUANDO** Ventas y Postventa solicita su cancelación.
  - **ENTONCES** el sistema responde `409 Conflict` indicando el estado actual y no modifica el despacho.

- [ ] **CA-19: Cancelación de un despacho fallido**
  - **DADO** un despacho cuyo estado actual es `FALLIDO`.
  - **CUANDO** Ventas y Postventa solicita su cancelación por anulación del pedido.
  - **ENTONCES** el sistema registra la anulación del pedido sobre el despacho (`pedidoAnulado = true`) sin cambiar su estado, responde `202 Accepted` y, cuando el paquete regrese al centro de despacho, F-04 solo permite cerrarlo como `DEVUELTO_A_ORIGEN`.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Endpoint `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion` implementado con seguridad JWT y control de idempotencia.
- [ ] Evaluación rigurosa del ciclo de vida del despacho con respuestas diferenciadas (200, 202, 409).
- [ ] Integración con cliente de Operación para liberación de capacidad en caso `ASIGNADO`.
- [ ] Pruebas unitarias y de integración con `JUnit 5 + MockMvc` cubriendo los 3 criterios (`CA-17`, `CA-18`, `CA-19`).
- [ ] Documentación y trazabilidad sincronizadas con [ES-F02-07](../../especificaciones/ES-F02-07-CancelarDespachoPorAnulacion/spec.md).
