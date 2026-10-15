# [HU-F04-04] Cierre de un Despacho como Devuelto a Origen

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-04: Entregas Fallidas y Reprogramaciones |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 8 |
| **Componentes** | Backend, Frontend, Base de Datos, Integración |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-04`, `sdd`, `devolucion-origen`, `integracion` |
| **Responsable sugerido** | Gerardo |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho

**QUIERO** cerrar como devuelto a origen un despacho fallido cuyo paquete ya fue recibido en el centro y no tendrá otro intento

**PARA** cerrar su tratamiento logístico, conservar la decisión y comunicar el resultado a Ventas y Postventa.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md), `RF-04`, restricciones de `RF-06` y `RF-07`; `CA-10`, `CA-11`, `CA-12`, `CA-15` y `CA-17` [cite: 1].
- **Especificación atómica:** [ES-F04-05](../../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen.md).
- **Contrato asociado:** [API, Externo §7.3, Gestión §5, Común §9](../../integraciones/api-contract-gestion-despachos.md), operación de cierre, evento e idempotencia [cite: 2]. Referencia: [Convenciones e integración externa](../../integraciones/api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa).
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada.
- **Dependencia externa:** RT-03 entrega el evento a Ventas y Postventa de forma asíncrona mediante webhook HTTPS y bandeja de salida. El cierre local no espera la disponibilidad de Ventas; el contrato correspondiente define autenticación y reintentos.
- **Componentes de Frontend:**
  - Confirmación explícita del cierre desde el detalle, con motivo obligatorio y recepción previamente confirmada.
  - Advertencia clara sobre el efecto de la decisión.
  - Retroalimentación diferenciada para operación exitosa, decisión ya procesada y problema de comunicación externa.
- **Reglas de negocio, idempotencia e integración:**
  - Solo puede cerrarse un despacho cuyo estado vigente sea `FALLIDO` y cuyo paquete tenga recepción confirmada.
  - El motivo es obligatorio y no puede contener solo espacios.
  - El Gestor puede cerrar por decisión operativa aunque queden intentos. Si se alcanzó el máximo o el pedido fue anulado, el cierre es la única decisión permitida, después de la recepción.
  - Una decisión aceptada cambia el estado a `DEVUELTO_A_ORIGEN` y registra el historial y `DESPACHO_DEVUELTO_A_ORIGEN` en la misma transacción local.
  - Repetir la misma operación no debe duplicar el cambio de estado, la auditoría de negocio ni la comunicación externa.
  - Una falla al comunicar el resultado no debe revertir el estado local ya aceptado.
  - Todo intento de comunicación debe registrarse como exitoso, pendiente o fallido, con información suficiente para su tratamiento posterior.
  - El paquete permanece en el centro a disposición de Ventas y Postventa. La historia no ejecuta reembolsos, cambios, reingreso a inventario ni reintegros de stock.
  - La recepción física se registra antes mediante HU-F04-06; cerrar no sustituye esa confirmación.
- **Datos involucrados:** despacho, decisión de devolución, auditoría e intentos de comunicación externa.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-10: Cierre exitoso**
  - **DADO** un despacho `FALLIDO` con recepción confirmada en el centro.
  - **CUANDO** el Gestor confirma su cierre indicando un motivo.
  - **ENTONCES** cambia a `DEVUELTO_A_ORIGEN` y se registran el historial y un único evento `DESPACHO_DEVUELTO_A_ORIGEN` para su entrega asíncrona a Ventas y Postventa.

- [ ] **CA-11: Operación repetida**
  - **DADO** que el despacho ya fue cerrado como `DEVUELTO_A_ORIGEN` por la misma operación.
  - **CUANDO** se repite la misma operación.
  - **ENTONCES** el sistema no duplica el cambio de estado, la auditoría de negocio ni la comunicación externa, e informa que la decisión ya fue procesada.

- [ ] **CA-12: Falla de la integración externa**
  - **DADO** que el despacho fue cerrado como `DEVUELTO_A_ORIGEN`.
  - **CUANDO** no es posible comunicar el resultado a Ventas y Postventa.
  - **ENTONCES** el sistema conserva el estado local, registra la comunicación como pendiente o fallida y deja evidencia suficiente para su reintento o tratamiento posterior.

- [ ] **CA-17: Decisión sin recepción confirmada — cierre**
  - **DADO** un despacho `FALLIDO` cuyo paquete aún no tiene recepción confirmada.
  - **CUANDO** el Gestor intenta cerrarlo.
  - **ENTONCES** el backend responde `409 Conflict` e indica que primero debe confirmarse la recepción, sin cambiar el despacho ni generar el evento de cierre.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de uso de cierre implementado con validación de estado `FALLIDO`, recepción y motivo obligatorio.
- [ ] Cambio a `DEVUELTO_A_ORIGEN`, historial y evento persistidos en la misma transacción local.
- [ ] Protección idempotente implementada para impedir efectos y comunicaciones duplicadas.
- [ ] Intentos de comunicación externa persistidos con estado exitoso, pendiente o fallido.
- [ ] Interfaz responsive implementada con confirmación y mensajes diferenciados para los resultados previstos.
- [ ] Pruebas cubren cierre voluntario, máximo alcanzado, pedido anulado, recepción pendiente, motivo ausente, repetición e indisponibilidad de Ventas y Postventa.
- [ ] Contrato de integración con Ventas y Postventa acordado y documentado en [integraciones/api-contract.md](../../integraciones/api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa).
- [ ] Verificado que una falla externa conserva el estado local y no se pierde silenciosamente.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
