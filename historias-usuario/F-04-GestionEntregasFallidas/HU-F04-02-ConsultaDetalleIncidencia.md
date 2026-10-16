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
- **Especificación atómica:** [ES-F04-02](../../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/spec.md).
- **Contrato asociado:** [Detalle, Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02) y [lectura de evidencia, Operación §3.4](../../integraciones/api-contract-operacion-reparto.md#34-autorizar-la-lectura-de-evidencia), con respuesta, nulabilidad, acciones y errores definidos documentalmente; implementación pendiente [cite: 2].
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada.
- **Componentes de Frontend:**
  - Vista responsive de detalle de la incidencia.
  - Presentación del motivo, comentario del repartidor, fecha, repartidor, contador sobre el máximo, recepción, historial y evidencia disponible.
  - Recepción con fecha, usuario, estado del sello y observación registrada.
  - Panel con `Confirmar recepción`, `Reprogramar` y `Cerrar como devuelto a origen`, según las restricciones vigentes.
  - Estado de recurso inexistente sin presentación de información parcial.
- **Reglas de negocio:**
  - El despacho debe existir y tener incidencia histórica; se muestra la última mediante `ultima_incidencia_id`, sin heredar recepción ni fotografía de una anterior.
  - Fuera de `FALLIDO` se conserva el detalle histórico y se ocultan las acciones de resolución. El detalle incluye el historial de operaciones sin transición y, por separado, las comunicaciones locales con Ventas.
  - Se muestran intentos consumidos sobre el máximo vigente; `NO_INTENTADO` no aumenta ni reinicia el acumulado. Contador igual o superior al máximo impide reprogramar.
  - La información mostrada debe corresponder al estado y al historial persistidos por el módulo.
  - La evidencia debe presentarse solo cuando se encuentre disponible y mediante el mecanismo de acceso autorizado definido con F-03.
  - Un `NO_INTENTADO` puede no tener fotografía; esa ausencia no impide consultar la incidencia y se explica en pantalla.
  - Sin recepción confirmada se bloquean reprogramación y cierre, incluso cuando el pedido esté anulado o se haya alcanzado el máximo.
  - Con recepción confirmada, el máximo alcanzado o el pedido anulado solo permiten el cierre. Estas restricciones también se validan en los comandos del backend.
  - La consulta no modifica el despacho ni ejecuta las acciones del panel.
  - La vista activa se actualiza como máximo cada 30 segundos y tras operaciones/conflictos; una actualización fallida bloquea acciones hasta recuperar datos actuales. Los datos de Operación desconocidos y los errores de fotografía se diferencian de la ausencia de información.
  - Una consulta inexistente no debe revelar datos parciales ni información de otro despacho.
- **Datos involucrados:** despacho, historial de estados, reporte de fallo, intentos y referencia de evidencia.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-04: Consulta de detalle exitosa**
  - **DADO** que existe un despacho en estado `FALLIDO`.
  - **CUANDO** el Gestor abre su detalle.
  - **ENTONCES** visualiza la última incidencia con motivo, comentario, fechas, repartidor, contador sobre el máximo vigente, recepción, historial completo, comunicaciones y fotografía autorizada cuando existe, con acciones según recepción, límite y anulación; una consulta posterior a la resolución conserva el estado actual sin acciones incompatibles.

- [ ] **CA-05: Despacho inexistente**
  - **DADO** que el código consultado no corresponde a un despacho existente.
  - **CUANDO** el Gestor solicita el detalle.
  - **ENTONCES** el backend responde `404 Not Found` y no presenta datos parciales.

---

Los escenarios verificables adicionales se mantienen en ES-F04-02, CA-01 a CA-11, sin duplicarlos aquí: varias incidencias, consulta histórica, restricciones combinadas, dependencias caídas, autorización, renovación de evidencia, actualización y ausencia de efectos de negocio.

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de consulta de detalle implementado en backend con recuperación del historial y la incidencia relacionada.
- [ ] Autorización del Gestor de Despacho validada antes de exponer información operativa o evidencia.
- [ ] Vista responsive implementada con estados de carga, éxito, error y recurso inexistente.
- [ ] Pruebas de contrato, integración y UI cubren CA-01 a CA-11 de ES-F04-02; distinguen fixtures y servicios reales, sin acreditar resultados pendientes.
- [ ] Pruebas de frontend verifican la presentación de toda la información requerida y la ausencia de datos parciales ante error.
- [ ] Integración con el mecanismo autorizado de consulta de evidencia de F-03 verificada cuando exista evidencia.
- [ ] Verificadas las variantes sin fotografía por `NO_INTENTADO`, enlace expirado y panel de decisiones con restricciones combinadas.
- [ ] Contrato HTTP validado y actualizado en [integraciones/api-contract-gestion-despachos.md](../../integraciones/api-contract-gestion-despachos.md) antes de cerrar la historia.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
