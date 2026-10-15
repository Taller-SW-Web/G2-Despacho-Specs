# [HU-F04-05] Trazabilidad de Recepciones y Decisiones sobre Entregas Fallidas

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-04: Entregas Fallidas y Reprogramaciones |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-04`, `sdd`, `auditoria`, `trazabilidad` |
| **Responsable sugerido** | Gerardo |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho

**QUIERO** que toda recepción, reprogramación o cierre quede registrado con su responsable, fecha, estados y datos de la operación

**PARA** reconstruir las decisiones tomadas sobre una entrega fallida y garantizar su trazabilidad operativa.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md), `RF-05` y `CA-13`, en relación con `RF-07` [cite: 1].
- **Especificación atómica:** [ES-F04-06](../../especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones.md); historial transversal RT-02 del [overview](../../overview.md) [cite: 2].
- **Mecanismo de captura:**
  - Se ejecuta automáticamente cuando una recepción, reprogramación o cierre es aceptado; no requiere una pantalla ni un comando independiente del Gestor.
  - La identidad del usuario debe obtenerse de la sesión autenticada y no de un identificador libre enviado por el cliente.
- **Reglas de negocio y persistencia:**
  - Cada registro debe contener, como mínimo, usuario, fecha, estado anterior, estado nuevo y observaciones aplicables.
  - La auditoría debe conservar la relación con el despacho y la decisión que la originó.
  - La operación de negocio y su historial se persisten consistentemente. Reprogramación y cierre incluyen también su evento pendiente en la misma transacción local.
  - En la recepción se registra `FALLIDO` como estado anterior y nuevo, junto con el sello y la observación aplicable; no se inventa una transición de estado.
  - En la reprogramación se registra `PENDIENTE_ASIGNACION` y la nueva fecha; en el cierre, `DEVUELTO_A_ORIGEN` y el motivo.
  - Usuario y fecha proceden del JWT y del servidor; los registros no se editan ni eliminan mediante F-04.
  - Una operación rechazada no debe registrarse como una decisión de negocio aceptada.
  - Una repetición idempotente de cualquiera de las tres operaciones no debe generar una segunda auditoría de negocio.
- **Datos involucrados:** despacho, historial de estados y registro de auditoría.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-13: Registro de auditoría**
  - **DADO** que el Gestor confirma una recepción, reprograma o cierra un despacho.
  - **CUANDO** la operación es aceptada.
  - **ENTONCES** se registra usuario, fecha del servidor, estado anterior, estado nuevo y datos aplicables: sello y observación, nueva fecha o motivo del cierre.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Registro de auditoría implementado para las recepciones, reprogramaciones y cierres aceptados.
- [ ] Identidad del usuario obtenida del contexto autenticado.
- [ ] Persistencia consistente verificada entre cada operación aceptada y su historial, incluida la recepción que conserva el estado.
- [ ] Pruebas unitarias verifican los campos obligatorios y la ausencia de auditoría de negocio en operaciones rechazadas o repetidas.
- [ ] Pruebas de integración confirman la trazabilidad después de recepción, reprogramación y cierre, sin duplicados por reintento.
- [ ] Los registros pueden consultarse posteriormente para fines operativos o de auditoría.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
