# [HU-F04-05] Trazabilidad de Decisiones sobre Entregas Fallidas

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

**COMO** Gestor de Despacho y Auditor de Operaciones  
**QUIERO** que toda reprogramación o derivación a almacén quede registrada con su responsable, fecha y transición  
**PARA** reconstruir las decisiones tomadas sobre una entrega fallida y garantizar su trazabilidad operativa.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../specs/funcionalidades/F-04-GestionEntregasFallidas.md) (Requisito `RF-05`, Criterio `CA-13`).
- **Mecanismo de captura:**
  - Se ejecuta automáticamente cuando una reprogramación o derivación a almacén es aceptada.
  - La identidad del usuario debe obtenerse de la sesión autenticada y no de un identificador libre enviado por el cliente.
- **Reglas de negocio y persistencia:**
  - Cada registro debe contener, como mínimo, usuario, fecha, estado anterior, estado nuevo y observaciones aplicables.
  - La auditoría debe conservar la relación con el despacho y la decisión que la originó.
  - El cambio de estado y su auditoría deben persistirse consistentemente.
  - Una operación rechazada no debe registrarse como una decisión de negocio aceptada.
  - La repetición idempotente de una derivación ya procesada no debe generar una segunda auditoría de negocio.
- **Datos involucrados:** despacho, historial de estados y registro de auditoría.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-13: Registro de auditoría**
  - **DADO** que el Gestor reprograma o deriva un despacho a almacén.
  - **CUANDO** la operación es aceptada.
  - **ENTONCES** se registra el usuario, la fecha, el estado anterior, el estado nuevo y la información relevante de la decisión.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Registro de auditoría implementado para las decisiones aceptadas de reprogramación y derivación.
- [ ] Identidad del usuario obtenida del contexto autenticado.
- [ ] Persistencia consistente verificada entre el cambio de estado y su auditoría.
- [ ] Pruebas unitarias verifican los campos obligatorios y la ausencia de auditoría de negocio en operaciones rechazadas o repetidas.
- [ ] Pruebas de integración confirman la trazabilidad después de ambos recorridos de F-04.
- [ ] Los registros pueden consultarse posteriormente para fines operativos o de auditoría.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
