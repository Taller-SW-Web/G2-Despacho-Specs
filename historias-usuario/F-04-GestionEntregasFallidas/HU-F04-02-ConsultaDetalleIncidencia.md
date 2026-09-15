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
**PARA** disponer de la información necesaria para decidir si corresponde reprogramarla o derivarla a almacén.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../specs/funcionalidades/F-04-GestionEntregasFallidas.md) (Requisito `RF-02`, Criterios `CA-04`, `CA-05`).
- **Endpoints asociados:** pendientes de validación en el contrato único [specs/api-contract.md](../../specs/api-contract.md). Esta historia no establece rutas ni estructuras de respuesta.
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada.
- **Componentes de Frontend:**
  - Vista responsive de detalle de la incidencia.
  - Presentación del motivo, fecha, repartidor, intento actual, historial de estados y evidencia disponible.
  - Estado de recurso inexistente sin presentación de información parcial.
- **Reglas de negocio:**
  - El despacho consultado debe existir.
  - La información mostrada debe corresponder al estado y al historial persistidos por el módulo.
  - La evidencia debe presentarse solo cuando se encuentre disponible y mediante el mecanismo de acceso autorizado definido con F-03.
  - Una consulta inexistente no debe revelar datos parciales ni información de otro despacho.
- **Datos involucrados:** despacho, historial de estados, reporte de fallo, intentos y referencia de evidencia.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-04: Consulta de detalle exitosa**
  - **DADO** que existe un despacho en estado `FALLIDO`.
  - **CUANDO** el Gestor abre su detalle.
  - **ENTONCES** visualiza el motivo, fecha, repartidor, intento actual, historial de estados y evidencia disponible.

- [ ] **CA-05: Despacho inexistente**
  - **DADO** que el código consultado no corresponde a un despacho existente.
  - **CUANDO** el Gestor solicita el detalle.
  - **ENTONCES** el sistema informa que el recurso no existe y no presenta datos parciales.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de consulta de detalle implementado en backend con recuperación del historial y la incidencia relacionada.
- [ ] Autorización del Gestor de Despacho validada antes de exponer información operativa o evidencia.
- [ ] Vista responsive implementada con estados de carga, éxito, error y recurso inexistente.
- [ ] Pruebas unitarias y de integración cubren un despacho existente y uno inexistente.
- [ ] Pruebas de frontend verifican la presentación de toda la información requerida y la ausencia de datos parciales ante error.
- [ ] Integración con el mecanismo autorizado de consulta de evidencia de F-03 verificada cuando exista evidencia.
- [ ] Contrato HTTP validado y actualizado en [specs/api-contract.md](../../specs/api-contract.md) antes de cerrar la historia.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
