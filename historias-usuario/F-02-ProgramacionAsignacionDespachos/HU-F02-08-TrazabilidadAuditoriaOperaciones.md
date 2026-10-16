# [HU-F02-08] Trazabilidad y Auditoría de las Operaciones de Despacho

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `f-02`, `sdd`, `auditoria`, `trazabilidad`, `inmutabilidad` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho y Auditor de Operaciones  
**QUIERO** que cada operación de recepción, simulación, asignación, reordenamiento, reasignación y cancelación quede registrada con marca temporal UTC, usuario o servicio ejecutor y balances asociados  
**PARA** mantener un historial inmutable y transparente que permita reconstruir cronológicamente el ciclo de vida del despacho y asegurar la integridad transaccional.

---

## 2. Descripción y Contexto Técnico

- **Especificación SDD origen:** [ES-F02-08: Registrar la trazabilidad de las operaciones](../../especificaciones/ES-F02-08-RegistrarTrazabilidadOperaciones/spec.md).
- **Especificación funcional padre:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-04`; Criterio `CA-10`; Requisito transversal `RT-02`).
- **Mecanismo de captura:**
  - Invocado atómicamente dentro de la misma transacción de base de datos (`@Transactional`) de cada operación de negocio en `servicio-gestion-despachos`.
  - La identidad del usuario se extrae directamente del token JWT (`SecurityContextHolder`) o del token de servicio entrante.
- **Reglas de persistencia:**
  - Inmutabilidad estricta: la tabla `historial_estados_despacho` es de solo inserción (`INSERT-only`), sin operaciones de actualización ni borrado.
  - Marca temporal generada en UTC (`Instant.now()`).
  - Atomicidad garantizada: si la inserción en auditoría falla, la mutación completa se revierte (`rollback`).
  - Cada registro incluye: despacho, estado anterior, estado nuevo, usuario ejecutor, fecha/hora UTC, jornada, repartidor, secuencia, observaciones y metadatos JSONB con balances.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-10: Registro de auditoría de la asignación y operaciones**
  - **DADO** que una operación de recepción, simulación, asignación, reordenamiento, reasignación o cancelación es aceptada en el sistema.
  - **CUANDO** finaliza la transacción en el backend.
  - **ENTONCES** se persiste un registro de auditoría inmutable con identificador del despacho, usuario o servicio ejecutor autenticado, marca temporal exacta en UTC, estado anterior y nuevo, observaciones y, en caso de asignación o reasignación, el repartidor, jornada, secuencia y ocupación resultante.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Entidad JPA `HistorialEstadoDespacho` y repositorio Spring Data de solo inserción implementados.
- [ ] Componente `AuditoriaService` desacoplado e integrado en todos los casos de uso de F-02.
- [ ] Pruebas unitarias con `JUnit 5 + Mockito` verificando la captura del usuario autenticado y timestamp UTC.
- [ ] Pruebas de integración con `DataJpaTest` verificando inserción correcta y orden cronológico.
- [ ] Prueba de atomicidad confirmando rollback total ante fallos de persistencia en auditoría.
- [ ] Documentación y trazabilidad sincronizadas con [ES-F02-08](../../especificaciones/ES-F02-08-RegistrarTrazabilidadOperaciones/spec.md).
