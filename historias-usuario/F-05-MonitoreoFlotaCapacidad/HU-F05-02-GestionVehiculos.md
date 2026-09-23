# [HU-F05-02] Registro y Gestión de Furgonetas

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-05: Monitoreo de Flota, Operadores y Capacidad Diaria |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Frontend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-05`, `sdd`, `furgonetas`, `flota`, `capacidad` |
| **Responsable sugerido** | Rhamses |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho
**QUIERO** registrar las furgonetas con su placa, estado mecánico y límites de capacidad de carga, y actualizar su estado de servicio
**PARA** disponer de un catálogo actualizado de furgonetas y garantizar que los despachos no excedan la capacidad real de cada una.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-05-MonitoreoFlotaCapacidad.md](../../funcionalidades/F-05-MonitoreoFlotaCapacidad.md) (Requisito `RF-02`, Criterios `CA-05`, `CA-06`, `CA-07`).
- **Endpoints asociados:**
  - `POST /api/v1/furgonetas` — Registro de una furgoneta con límites de carga.
  - `GET /api/v1/furgonetas` — Catálogo con filtros por estado y placa.
  - `PUT /api/v1/furgonetas/{idFurgoneta}` — Edición de datos y límites.
- **Rol requerido:** `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Panel de Vehículos: catálogo paginado con filtros por tipo, estado mecánico y placa, y acciones de alta, edición y cambio de estado.
  - Formulario de Vehículo: campos para tipo (`MOTO`, `AUTO`, `FURGONETA`), placa, estado mecánico y límites de carga (peso en kg, volumen en m³, máximo de paquetes por jornada).
- **Reglas de negocio:**
  - La placa de la furgoneta debe ser única; un intento de duplicarla se responde con `409 Conflict`.
  - Una furgoneta recién registrada queda en estado `DISPONIBLE`.
  - Una furgoneta en `EN_MANTENIMIENTO` se excluye de nuevas jornadas.
  - La desactivación aplica baja lógica para preservar el historial de asignaciones.
- **Entidades de datos involucradas:** `furgonetas`, `asignaciones_diarias` (ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-05: Registro de furgoneta con parámetros de capacidad**
  - **DADO** que el Gestor registra una furgoneta con placa "ABC-123", capacidad de 500 kg, 4.0 m³ y tope de 80 paquetes diarios.
  - **CUANDO** confirma el registro en `POST /api/v1/furgonetas`.
  - **ENTONCES** el sistema guarda la unidad con estado `DISPONIBLE`, sus límites de carga configurados y retorna el recurso creado con código `201 Created`.

- [ ] **CA-06: Rechazo de furgoneta con placa duplicada**
  - **DADO** que ya existe una furgoneta registrada con la placa "ABC-123".
  - **CUANDO** se intenta registrar otro con la misma placa.
  - **ENTONCES** el sistema rechaza la operación con código `409 Conflict` e indica que la placa ya está registrada, sin persistir el duplicado.

- [ ] **CA-07: Desactivación de furgoneta por mantenimiento**
  - **DADO** que una furgoneta debe entrar a mantenimiento.
  - **CUANDO** el Gestor cambia su estado a `EN_MANTENIMIENTO` mediante `PUT /api/v1/furgonetas/{idFurgoneta}`.
  - **ENTONCES** el sistema la excluye de nuevas jornadas y aplica las reglas de cierre seguro de la jornada vigente.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Código implementado en Java 21 / Spring Boot siguiendo las convenciones de [AGENTS.md](../../AGENTS.md).
- [ ] Entidad JPA y repositorio para `furgonetas` en Spring Data con restricción de unicidad sobre placa.
- [ ] DTOs de entrada validados con `@NotNull`, `@NotBlank`, `@Positive` para los límites de capacidad (`jakarta.validation`).
- [ ] Pruebas unitarias (`JUnit 5 + Mockito`) cubriendo los 3 escenarios (`CA-05`, `CA-06`, `CA-07`).
- [ ] Prueba de integración verificando que una furgoneta `EN_MANTENIMIENTO` queda excluida de nuevas jornadas.
- [ ] Panel de Vehículos implementado en React + Tailwind con tabla responsive y filtros por tipo, estado y placa.
- [ ] Formulario de Vehículo con validación de capacidad en tiempo real (valores positivos).
- [ ] Respuestas HTTP alineadas al contrato en [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
