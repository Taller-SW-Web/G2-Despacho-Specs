# [HU-F04-03] Reprogramación de un Despacho Fallido

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-04: Entregas Fallidas y Reprogramaciones |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-04`, `sdd`, `reprogramacion`, `reintentos` |
| **Responsable sugerido** | Gerardo |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho

**QUIERO** reprogramar para una fecha futura un despacho fallido cuyo paquete ya fue recibido y que todavía admite otro intento

**PARA** devolver el despacho a la cola de asignación y ofrecer una nueva oportunidad de entrega sin perder su historial.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md), `RF-03`, `RF-06` y precondición de `RF-07`; `CA-06` a `CA-09`, `CA-14`, `CA-15` y `CA-17` [cite: 1].
- **Especificación atómica:** [ES-F04-04](../../especificaciones/ES-F04-04-ReprogramarDespachoFallido/spec.md).
- **Contrato asociado:** [Gestión §5.2.2](../../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04), definición canónica de la reprogramación, y [Común §7.3](../../integraciones/api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa), evento a Ventas [cite: 2]. La atómica conserva los criterios detallados; esta historia no define otro contrato.
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada.
- **Componentes de Frontend:**
  - Formulario de reprogramación desde el detalle de la incidencia.
  - Selector de fecha futura y confirmación explícita.
  - Bloqueo de la acción por recepción pendiente, máximo de intentos alcanzado o pedido anulado.
  - Mensajes de validación, conflicto por información desactualizada, error y éxito.
- **Reglas de negocio y consistencia:**
  - Solo puede reprogramarse un despacho cuyo estado vigente sea `FALLIDO`.
  - El paquete debe tener recepción confirmada mediante HU-F04-06 y el pedido no debe estar anulado.
  - La nueva fecha civil debe ser posterior al día actual del servidor en `America/Lima`, según Gestión §5.2.2; observación opcional normalizada y reglas de formato en ese mismo contrato.
  - El número de intentos debe ser menor que el máximo configurado, cuyo valor inicial es dos.
  - Una reprogramación válida cambia el estado a `PENDIENTE_ASIGNACION` y conserva el contador de intentos.
  - Reprogramar no incrementa el contador; F-03 origina el incremento cuando registra un fallo con intento real. `NO_INTENTADO` tampoco lo incrementa.
  - Se conserva la zona original aunque haya sido desactivada posteriormente; esta operación no crea un despacho nuevo.
  - El cambio de estado, la nueva fecha, el historial y el evento `DESPACHO_REPROGRAMADO` se registran en la misma transacción local.
  - El despacho sale del listado de fallidos y aparece en la cola de F-02. Si su fecha es futura, permanece visible en solo lectura y F-02 solo permite asignarlo cuando corresponda.
  - Reprogramar no asigna repartidor ni reserva la capacidad del siguiente reparto.
  - Liberación pendiente/de revisión no bloquea reprogramar; F-02 espera la liberación de la reserva anterior para aceptar otra asignación. Se conservan referencias históricas de la salida y se retiran las de asignación vigente.
  - El comando conserva incidencia/versión y resultado durable. Un replay exacto autorizado devuelve el resultado original aun después de otra salida; otro contenido/ejecutor con la misma identidad responde `409`. Cierre y anulación concurrentes compiten por la versión.
  - Una simulación conserva historial y marca de prueba sin emitir eventos externos; la indisponibilidad de Ventas no revierte una decisión local aceptada.
  - El backend debe volver a validar todas las reglas aunque el frontend haya bloqueado previamente una acción inválida.
- **Datos involucrados:** despacho, fecha reprogramada, política de intentos e historial auditable.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-06: Reprogramación válida**
  - **DADO** un despacho `FALLIDO`, recibido en el centro, cuyo pedido no está anulado, con un intento registrado y máximo configurado de dos.
  - **CUANDO** el Gestor selecciona una fecha futura y confirma la reprogramación.
  - **ENTONCES** cambia a `PENDIENTE_ASIGNACION`, guarda la nueva fecha, conserva el contador en uno y la zona original, y registra historial y evento para Ventas sin volver a validar cobertura activa.

- [ ] **CA-07: Fecha inválida**
  - **DADO** que un despacho puede ser reprogramado.
  - **CUANDO** el Gestor selecciona la fecha actual o una fecha pasada.
  - **ENTONCES** el backend responde `400 Bad Request`, explica la validación y mantiene el despacho en `FALLIDO`.

- [ ] **CA-08: Límite de intentos alcanzado**
  - **DADO** que el despacho alcanzó el máximo de intentos configurado.
  - **CUANDO** el Gestor consulta su detalle o intenta reprogramarlo.
  - **ENTONCES** el frontend deshabilita la reprogramación y el backend responde `422 Unprocessable Entity` al intentar ejecutarla; solo queda el cierre como `DEVUELTO_A_ORIGEN`, previa recepción confirmada.

- [ ] **CA-09: Estado incompatible**
  - **DADO** que el despacho ya no se encuentra en estado `FALLIDO`.
  - **CUANDO** se intenta reprogramar usando información desactualizada.
  - **ENTONCES** el backend responde `409 Conflict`, conserva el estado vigente e informa que el despacho fue actualizado.

- [ ] **CA-14: Reprogramación de un despacho no intentado**
  - **DADO** un despacho `FALLIDO` con motivo `NO_INTENTADO`, recibido en el centro, con contador inferior al máximo y pedido no anulado.
  - **CUANDO** el Gestor lo reprograma con una fecha futura.
  - **ENTONCES** vuelve a `PENDIENTE_ASIGNACION` conservando el contador y se identifica como `No intentado` mientras se consulta la incidencia.

- [ ] **CA-15: Despacho fallido con pedido anulado**
  - **DADO** un despacho `FALLIDO` sobre el que F-02 registró la anulación del pedido.
  - **CUANDO** el Gestor abre el detalle o intenta reprogramarlo.
  - **ENTONCES** la reprogramación está deshabilitada, el comando responde `409 Conflict` y solo se permite cerrar como `DEVUELTO_A_ORIGEN` después de confirmar la recepción.

- [ ] **CA-17: Decisión sin recepción confirmada — reprogramación**
  - **DADO** un despacho `FALLIDO` cuyo paquete aún no tiene recepción confirmada.
  - **CUANDO** el Gestor intenta reprogramarlo.
  - **ENTONCES** el backend responde `409 Conflict` e indica que primero debe confirmarse la recepción, sin cambiar el despacho.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de uso valida estado, recepción, fecha futura, máximo configurable y anulación.
- [ ] Cambio a `PENDIENTE_ASIGNACION`, nueva fecha, historial y evento persistidos en la misma transacción local.
- [ ] Verificado que la reprogramación no incrementa el contador de intentos.
- [ ] Formulario responsive implementado con confirmación, validaciones y bloqueo visual por límite alcanzado.
- [ ] Pruebas unitarias cubren las reglas de fecha, estado y política de intentos.
- [ ] Pruebas de integración y frontend cubren `CA-06` a `CA-09`, `CA-14`, `CA-15` y `CA-17`, incluidos concurrencia y reintentos sin efectos duplicados.
- [ ] Verificada la conservación de zona y la visibilidad inmediata en F-02 con asignación bloqueada hasta la fecha programada.
- [ ] Contrato HTTP validado y actualizado en [integraciones/api-contract-gestion-despachos.md](../../integraciones/api-contract-gestion-despachos.md) antes de cerrar la historia.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
