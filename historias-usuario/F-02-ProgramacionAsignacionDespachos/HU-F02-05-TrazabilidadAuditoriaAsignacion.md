# [HU-F02-05] Trazabilidad y Auditoría de la Asignación de Despachos

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-02`, `sdd`, `auditoria`, `trazabilidad` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho y Auditor de Operaciones  
**QUIERO** que cada asignación y transición de estado quede registrada con marca temporal UTC, usuario gestor, operador asignado y balance de capacidad resultante  
**PARA** mantener un historial auditable completo, prevenir inconsistencias transaccionales y garantizar la transparencia operativa del transporte.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-02-ProgramacionAsignacionDespachos.md](../../specs/funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-04`, Criterio `CA-11`).
- **Mecanismo de captura:**
  - Se ejecuta automáticamente durante el flujo de asignación (`POST /api/v1/despachos/{idDespacho}/asignar`).
  - La identidad del usuario gestor se extrae directamente del token JWT (`SecurityContextHolder`).
- **Reglas de negocio y persistencia:**
  - El registro de auditoría DEBE persistirse dentro de la misma transacción de base de datos (`@Transactional`) de la asignación; si la auditoría falla, la asignación debe revertirse (rollback).
  - La marca temporal debe guardarse en tiempo universal coordinado (UTC).
  - Cada entrada debe contener: `idAuditoria` (UUID), `idDespacho`, `idRepartidor`, `idUsuarioGestor`, `fechaHoraAsignacion` (UTC), `estadoAnterior` (`PENDIENTE_ASIGNACION`), `estadoNuevo` (`ASIGNADO`), `pesoAsignadoKg`, `volumenAsignadoM3`, `capacidadRemanentePesoKg`, `capacidadRemanenteVolumenM3` y `observaciones`.
  - Los registros de auditoría son inmutables (solo inserción, sin operaciones de actualización ni eliminación).
- **Entidades de datos involucradas:** `auditoria_asignaciones`, `historial_estados_despacho`.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-11: Registro de auditoría y actualización de carga operativa**
  - **DADO** que una asignación de despacho es aceptada exitosamente en el sistema.
  - **CUANDO** finaliza la transacción en el backend.
  - **ENTONCES** se persiste un registro de auditoría inmutable con identificador del despacho, repartidor asignado, identificador del usuario gestor autenticado, marca temporal exacta en UTC, observaciones y el nuevo balance de capacidad vehicular resultante.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Entidad JPA y repositorio para persistencia de auditoría implementados en Spring Data.
- [ ] Servicio de auditoría desacoplado e invocado dentro de la transacción de asignación.
- [ ] Prueba unitaria con `JUnit 5 + Mockito` verificando la captura del usuario desde el contexto de seguridad.
- [ ] Prueba de integración con `DataJpaTest` o `SpringBootTest` confirmando inserción correcta en la tabla de auditoría tras una asignación exitosa.
- [ ] Verificación de atomicidad: si ocurre una excepción en la persistencia de auditoría, se comprueba el rollback de la asignación.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
