# [HU-F04-02] Consulta del Detalle de una Incidencia

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-04: Entregas Fallidas y Reprogramaciones |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-04`, `sdd`, `incidencia`, `detalle` |
| **Responsable sugerido** | Gerardo |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho

**QUIERO** consultar el detalle y el historial de intentos de una entrega fallida

**PARA** verificar el retorno del paquete y disponer de la información necesaria para reprogramar el despacho o cerrarlo como devuelto a origen.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md), `RF-02`, `CA-04` y `CA-05`; restricciones de `RF-03`, `RF-06` y `RF-07` [cite: 1].
- **Especificación atómica:** [ES-F04-02](../../especificaciones/ES-F04-02-ConsultarDetalleIncidencia.md).
- **Contrato asociado:** [API, Operación §3, Gestión §5](../../integraciones/api-contract-gestion-despachos.md). La consulta de incidencia y el acceso temporal a evidencia ya tienen rutas; las respuestas completas se concretarán en el contrato correspondiente [cite: 2]. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#3-api-de-f-03-operación-del-repartidor).
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada.
- **Componentes de Frontend:**
  - Vista responsive de detalle de la incidencia.
  - Presentación del motivo, comentario del repartidor, fecha, repartidor, contador sobre el máximo, recepción, historial y evidencia disponible.
  - Recepción con fecha, usuario, estado del sello y observación registrada.
  - Panel con `Confirmar recepción`, `Reprogramar` y `Cerrar como devuelto a origen`, según las restricciones vigentes.
  - Estado de recurso inexistente sin presentación de información parcial.
- **Reglas de negocio:**
  - El despacho consultado debe existir.
  - La información mostrada debe corresponder al estado y al historial persistidos por el módulo.
  - La evidencia debe presentarse solo cuando se encuentre disponible y mediante el mecanismo de acceso autorizado definido con F-03.
  - Un `NO_INTENTADO` puede no tener fotografía; esa ausencia no impide consultar la incidencia y se explica en pantalla.
  - Sin recepción confirmada se bloquean reprogramación y cierre, incluso cuando el pedido esté anulado o se haya alcanzado el máximo.
  - Con recepción confirmada, el máximo alcanzado o el pedido anulado solo permiten el cierre. Estas restricciones también se validan en los comandos del backend.
  - La consulta no modifica el despacho ni ejecuta las acciones del panel.
  - Una consulta inexistente no debe revelar datos parciales ni información de otro despacho.
- **Datos involucrados:** despacho, historial de estados, reporte de fallo, intentos y referencia de evidencia.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-04: Consulta de detalle exitosa**
  - **DADO** que existe un despacho en estado `FALLIDO`.
  - **CUANDO** el Gestor abre su detalle.
  - **ENTONCES** visualiza motivo, comentario, fecha, repartidor, contador sobre el máximo, recepción, historial de estados y fotografía mediante acceso temporal autorizado cuando existe, con las acciones disponibles según recepción, límite y anulación.

- [ ] **CA-05: Despacho inexistente**
  - **DADO** que el código consultado no corresponde a un despacho existente.
  - **CUANDO** el Gestor solicita el detalle.
  - **ENTONCES** el backend responde `404 Not Found` y no presenta datos parciales.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de consulta de detalle implementado en backend con recuperación del historial y la incidencia relacionada.
- [ ] Autorización del Gestor de Despacho validada antes de exponer información operativa o evidencia.
- [ ] Vista responsive implementada con estados de carga, éxito, error y recurso inexistente.
- [ ] Pruebas unitarias y de integración cubren un despacho existente y uno inexistente.
- [ ] Pruebas de frontend verifican la presentación de toda la información requerida y la ausencia de datos parciales ante error.
- [ ] Integración con el mecanismo autorizado de consulta de evidencia de F-03 verificada cuando exista evidencia.
- [ ] Verificadas las variantes sin fotografía por `NO_INTENTADO`, enlace expirado y panel de decisiones con restricciones combinadas.
- [ ] Contrato HTTP validado y actualizado en [integraciones/api-contract-gestion-despachos.md](../../integraciones/api-contract-gestion-despachos.md) antes de cerrar la historia.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
