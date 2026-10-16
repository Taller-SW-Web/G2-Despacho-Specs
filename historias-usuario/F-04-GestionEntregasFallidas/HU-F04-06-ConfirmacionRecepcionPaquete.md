# [HU-F04-06] Confirmación de Recepción de un Paquete en el Centro

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-04: Entregas Fallidas y Reprogramaciones |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | Por estimar |
| **Componentes** | Backend, Frontend, Base de Datos, Integración |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-04`, `sdd`, `recepcion-centro`, `retorno` |
| **Responsable sugerido** | Gerardo |

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho

**QUIERO** confirmar que un paquete no entregado regresó físicamente al centro y registrar su condición

**PARA** controlar su retorno, liberar la capacidad que ocupaba y habilitar una decisión de reprogramación o cierre.

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md), `RF-07`, `CA-16`, `CA-17` y relación con `CA-18` [cite: 1].
- **Especificación atómica:** [ES-F04-03](../../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete.md).
- **Contrato asociado:** [API, Gestión §5, Operación §5.2, Común §9](../../integraciones/api-contract-gestion-despachos.md), recepción, liberación de reserva e idempotencia [cite: 2]. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#52-gestión-libera-una-reserva-en-operación), [Convenciones e integración externa](../../integraciones/api-contract.md#9-reglas-de-idempotencia-y-concurrencia).
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada.
- **Precondiciones:** despacho vigente en `FALLIDO`, recepción pendiente y paquete físicamente en el centro.
- **Componentes de Frontend:** modal accesible desde listado o detalle con resumen, selección obligatoria del sello sin valor por defecto, observación y confirmación.
- **Reglas de negocio:**
  - Se indica obligatoriamente si el sello está intacto. La observación conserva el carácter opcional establecido actualmente en ES-F04-03; la discrepancia con el diseño se resolverá al acordar esa regla.
  - Usuario y fecha se obtienen del JWT y del servidor.
  - La recepción registra su historial y mantiene el despacho en `FALLIDO`, ahora como `Recibido en centro`.
  - Se solicita la liberación idempotente de la reserva en Operación por el motivo definido en el contrato; F-06 refleja la capacidad liberada.
  - Una recepción repetida no duplica recepción, historial ni liberación.
  - Reprogramar o cerrar sin recepción confirmada responde `409 Conflict`.
  - La recepción habilita las decisiones que correspondan por intentos y anulación; no las ejecuta automáticamente.
  - Un sello alterado no impide registrar el retorno ni decide automáticamente un reembolso, cambio o tratamiento comercial.
- **Dependencias:** F-03 origina el fallo; F-06 refleja la liberación de capacidad; HU-F04-05 registra la trazabilidad; HU-F04-03 y HU-F04-04 consumen la recepción confirmada.
- **Límites:** no se modifica el cierre de turno de F-06. La identificación de cada salida y la recuperación de una caída de Operación siguen pendientes de definición en el contrato; esta historia no establece mecanismos alternativos.

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-16: Confirmación de recepción**
  - **DADO** un despacho `FALLIDO` marcado como `Pendiente de retorno` cuyo paquete llegó al centro.
  - **CUANDO** el Gestor confirma su recepción indicando si el sello está intacto.
  - **ENTONCES** se marca como `Recibido en centro`, conserva `FALLIDO`, registra la auditoría y el paquete deja de contar en la ocupación del repartidor y la furgoneta en F-06.

- [ ] **CA-17: Decisión sin recepción confirmada**
  - **DADO** un despacho `FALLIDO` cuyo paquete aún no se recibió en el centro.
  - **CUANDO** el Gestor intenta reprogramarlo o cerrarlo.
  - **ENTONCES** el backend responde `409 Conflict`, indica que primero debe confirmarse la recepción y conserva el estado vigente.

La presentación del retorno atrasado de `CA-18` se verifica en HU-F04-01. Los escenarios complementarios de sello alterado, repetición, estado incompatible, datos incompletos y permisos se detallan en ES-F04-03.

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Confirmación con validación de estado, rol, recepción pendiente y sello informado.
- [ ] Fecha, usuario, sello, observación aplicable e historial persistidos sin cambiar `FALLIDO`.
- [ ] Liberación de capacidad integrada con Operación conforme al contrato correspondiente, sin efectos duplicados.
- [ ] Modal y actualización del listado/detalle verificados, con errores y operación ya registrada.
- [ ] Verificados `CA-16`, `CA-17` y los escenarios complementarios de ES-F04-03.
- [ ] Ninguna decisión se habilita antes de la recepción; después se respetan intentos y anulación.
- [ ] Pendientes contractuales resueltos antes de verificar la integración real; evidencia de implementación registrada sin confundirla con esta actualización documental.
- [ ] Documentación y trazabilidad actualizadas.
