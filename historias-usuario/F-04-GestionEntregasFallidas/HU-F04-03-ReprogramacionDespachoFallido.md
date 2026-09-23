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
**QUIERO** reprogramar para una fecha futura una entrega fallida que todavía admite otro intento  
**PARA** devolver el despacho a la cola de asignación y ofrecer una nueva oportunidad de entrega sin perder su historial.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md) (Requisito `RF-03`, Criterios `CA-06`, `CA-07`, `CA-08`, `CA-09`).
- **Endpoints asociados:** pendientes de validación en el contrato único [integraciones/api-contract.md](../../integraciones/api-contract.md). Esta historia no establece rutas ni cuerpos de solicitud.
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada.
- **Componentes de Frontend:**
  - Formulario de reprogramación desde el detalle de la incidencia.
  - Selector de fecha futura y confirmación explícita.
  - Bloqueo de la acción cuando se conozca que el límite de intentos fue alcanzado.
  - Mensajes de validación, conflicto por información desactualizada, error y éxito.
- **Reglas de negocio y consistencia:**
  - Solo puede reprogramarse un despacho cuyo estado vigente sea `FALLIDO`.
  - La nueva fecha debe ser posterior a la fecha actual.
  - El número de intentos debe ser menor que el máximo configurado, cuyo valor inicial es dos.
  - Una reprogramación válida cambia el estado a `PENDIENTE_ASIGNACION` y conserva el contador de intentos.
  - El contador se incrementa únicamente cuando el repartidor ejecuta un nuevo intento, no durante la reprogramación.
  - El cambio de estado, la nueva fecha y la auditoría deben persistirse consistentemente.
  - El backend debe volver a validar todas las reglas aunque el frontend haya bloqueado previamente una acción inválida.
- **Datos involucrados:** despacho, fecha reprogramada, política de intentos e historial auditable.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-06: Reprogramación válida**
  - **DADO** que un despacho fallido tiene un intento registrado y el máximo configurado es dos.
  - **CUANDO** el Gestor selecciona una fecha futura y confirma la reprogramación.
  - **ENTONCES** el sistema cambia el estado a `PENDIENTE_ASIGNACION`, guarda la nueva fecha, conserva el contador en uno y registra la auditoría.

- [ ] **CA-07: Fecha inválida**
  - **DADO** que un despacho puede ser reprogramado.
  - **CUANDO** el Gestor selecciona la fecha actual o una fecha pasada.
  - **ENTONCES** el sistema rechaza la operación, explica la validación y mantiene el despacho en `FALLIDO`.

- [ ] **CA-08: Límite de intentos alcanzado**
  - **DADO** que el despacho alcanzó el máximo de intentos configurado.
  - **CUANDO** el Gestor consulta su detalle o intenta reprogramarlo.
  - **ENTONCES** el frontend deshabilita la reprogramación, el backend rechaza cualquier intento equivalente y solo se ofrece la derivación a almacén.

- [ ] **CA-09: Estado incompatible**
  - **DADO** que el despacho ya no se encuentra en estado `FALLIDO`.
  - **CUANDO** se intenta reprogramar usando información desactualizada.
  - **ENTONCES** el sistema rechaza la operación, conserva el estado vigente e informa que el despacho fue actualizado.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de uso de reprogramación implementado con validación de estado, fecha futura y máximo configurable de intentos.
- [ ] Cambio a `PENDIENTE_ASIGNACION`, nueva fecha y auditoría persistidos dentro de una operación consistente.
- [ ] Verificado que la reprogramación no incrementa el contador de intentos.
- [ ] Formulario responsive implementado con confirmación, validaciones y bloqueo visual por límite alcanzado.
- [ ] Pruebas unitarias cubren las reglas de fecha, estado y política de intentos.
- [ ] Pruebas de integración y frontend cubren `CA-06` a `CA-09`, incluida la actualización concurrente o desactualizada.
- [ ] El despacho reprogramado vuelve a estar disponible para la cola de asignación de F-02.
- [ ] Contrato HTTP validado y actualizado en [integraciones/api-contract.md](../../integraciones/api-contract.md) antes de cerrar la historia.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
