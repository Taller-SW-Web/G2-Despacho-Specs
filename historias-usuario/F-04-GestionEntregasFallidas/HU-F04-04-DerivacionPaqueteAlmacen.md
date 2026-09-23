# [HU-F04-04] Derivación de un Paquete a Almacén

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-04: Entregas Fallidas y Reprogramaciones |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 8 |
| **Componentes** | Backend, Frontend, Base de Datos, Integración |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-04`, `sdd`, `devolucion`, `almacen`, `integracion` |
| **Responsable sugerido** | Gerardo |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** derivar a almacén un despacho fallido que no debe volver a intentarse  
**PARA** cerrar su tratamiento logístico, conservar la decisión y comunicar el resultado a Ventas y Postventa.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md) (Requisito `RF-04`, Criterios `CA-10`, `CA-11`, `CA-12`).
- **Endpoints asociados:** pendientes de validación en el contrato único [integraciones/api-contract.md](../../integraciones/api-contract.md). Esta historia no determina la ruta ni el transporte de integración.
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada.
- **Dependencia externa:** Ventas y Postventa debe recibir el resultado de la devolución. El mecanismo síncrono o asíncrono, el contrato de datos y la autenticación entre módulos deben acordarse antes de cerrar la historia.
- **Componentes de Frontend:**
  - Confirmación explícita de derivación a almacén desde el detalle de la incidencia.
  - Advertencia clara sobre el efecto de la decisión.
  - Retroalimentación diferenciada para operación exitosa, decisión ya procesada y problema de comunicación externa.
- **Reglas de negocio, idempotencia e integración:**
  - Solo puede derivarse un despacho cuyo estado vigente sea `FALLIDO`.
  - Una decisión aceptada cambia el estado a `DERIVADO_A_ALMACEN` y registra la auditoría.
  - Repetir la misma operación no debe duplicar el cambio de estado, la auditoría de negocio ni la comunicación externa.
  - Una falla al comunicar el resultado no debe revertir el estado local ya aceptado.
  - Todo intento de comunicación debe registrarse como exitoso, pendiente o fallido, con información suficiente para su tratamiento posterior.
  - La historia no incluye reembolsos, extornos, notas de crédito ni la definición del proceso físico de recepción en almacén.
- **Datos involucrados:** despacho, decisión de devolución, auditoría e intentos de comunicación externa.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-10: Derivación exitosa**
  - **DADO** que un despacho se encuentra en estado `FALLIDO`.
  - **CUANDO** el Gestor confirma su derivación a almacén.
  - **ENTONCES** el sistema cambia el estado a `DERIVADO_A_ALMACEN`, registra la auditoría e inicia la comunicación del resultado a Ventas y Postventa.

- [ ] **CA-11: Operación repetida**
  - **DADO** que el despacho ya fue derivado a almacén.
  - **CUANDO** se repite la misma operación.
  - **ENTONCES** el sistema no duplica el cambio de estado, la auditoría de negocio ni la comunicación externa, e informa que la decisión ya fue procesada.

- [ ] **CA-12: Falla de la integración externa**
  - **DADO** que el despacho fue derivado a almacén.
  - **CUANDO** no es posible comunicar el resultado a Ventas y Postventa.
  - **ENTONCES** el sistema conserva el estado local, registra la comunicación como pendiente o fallida y deja evidencia suficiente para su reintento o tratamiento posterior.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de uso de derivación implementado con validación del estado `FALLIDO`.
- [ ] Cambio a `DERIVADO_A_ALMACEN` y auditoría persistidos consistentemente.
- [ ] Protección idempotente implementada para impedir efectos y comunicaciones duplicadas.
- [ ] Intentos de comunicación externa persistidos con estado exitoso, pendiente o fallido.
- [ ] Interfaz responsive implementada con confirmación y mensajes diferenciados para los resultados previstos.
- [ ] Pruebas unitarias y de integración cubren la derivación exitosa, la repetición y la indisponibilidad de Ventas y Postventa.
- [ ] Contrato de integración con Ventas y Postventa acordado y documentado únicamente en [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Verificado que una falla externa conserva el estado local y no se pierde silenciosamente.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
