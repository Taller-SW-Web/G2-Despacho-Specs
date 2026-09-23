# [HU-F05-02] Registro y Gestión de Vehículos de Flota

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-05: Monitoreo de Flota, Operadores y Capacidad Diaria |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Frontend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-05`, `sdd`, `vehiculos`, `flota`, `capacidad` |
| **Responsable sugerido** | Rhamses |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Flota
**QUIERO** registrar los vehículos de la flota con su tipo, placa, estado mecánico y límites de capacidad de carga, y actualizar su estado de servicio
**PARA** disponer de un catálogo actualizado de unidades disponibles para asignar a repartidores y garantizar que los despachos no excedan la capacidad real de cada vehículo.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-05-MonitoreoFlotaCapacidad.md](../../funcionalidades/F-05-MonitoreoFlotaCapacidad.md) (Requisito `RF-02`, Criterios `CA-05`, `CA-06`, `CA-07`).
- **Endpoints asociados:**
  - `POST /api/v1/vehiculos` — Registro de nuevo vehículo con límites de carga (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md) §7.3).
  - `GET /api/v1/vehiculos` — Catálogo de flota vehicular con filtros por tipo, estado y placa.
  - `PUT /api/v1/vehiculos/{idVehiculo}` — Edición de datos y cambio de estado mecánico.
- **Roles requeridos:** `GESTOR_FLOTA` o `ADMIN_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Panel de Vehículos: catálogo paginado con filtros por tipo, estado mecánico y placa, y acciones de alta, edición y cambio de estado.
  - Formulario de Vehículo: campos para tipo (`MOTO`, `AUTO`, `FURGONETA`), placa, estado mecánico y límites de carga (peso en kg, volumen en m³, máximo de paquetes por jornada).
- **Reglas de negocio:**
  - La placa del vehículo debe ser única en el sistema; un intento de duplicar la placa se responde con `409 Conflict`.
  - Un vehículo recién registrado queda en estado `DISPONIBLE`.
  - Un vehículo en estado `EN_MANTENIMIENTO` se excluye del catálogo de asignaciones operativas disponibles y, si tenía un repartidor vinculado en el turno activo, ese repartidor queda marcado sin vehículo asignado.
  - La desactivación aplica baja lógica para preservar el historial de asignaciones.
- **Entidades de datos involucradas:** `vehiculos`, `turnos_operador` (ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-05: Registro de vehículo con parámetros de capacidad**
  - **DADO** que el Gestor registra una furgoneta con placa "ABC-123", capacidad de 500 kg, 4.0 m³ y tope de 80 paquetes diarios.
  - **CUANDO** confirma el registro en `POST /api/v1/vehiculos`.
  - **ENTONCES** el sistema guarda la unidad con estado `DISPONIBLE`, sus límites de carga configurados y retorna el recurso creado con código `201 Created`.

- [ ] **CA-06: Rechazo de vehículo con placa duplicada**
  - **DADO** que ya existe un vehículo registrado con la placa "ABC-123".
  - **CUANDO** se intenta registrar otro con la misma placa.
  - **ENTONCES** el sistema rechaza la operación con código `409 Conflict` e indica que la placa ya está registrada, sin persistir el duplicado.

- [ ] **CA-07: Desactivación de vehículo por mantenimiento**
  - **DADO** que un vehículo debe entrar a mantenimiento.
  - **CUANDO** el Gestor cambia su estado a `EN_MANTENIMIENTO` mediante `PUT /api/v1/vehiculos/{idVehiculo}`.
  - **ENTONCES** el sistema excluye la unidad del catálogo de asignaciones disponibles y, si tenía un repartidor asociado en el turno activo, lo marca como sin vehículo asignado.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Código implementado en Java 21 / Spring Boot siguiendo las convenciones de [AGENTS.md](../../AGENTS.md).
- [ ] Entidad JPA y repositorio para `vehiculos` en Spring Data con restricción de unicidad sobre placa.
- [ ] DTOs de entrada validados con `@NotNull`, `@NotBlank`, `@Positive` para los límites de capacidad (`jakarta.validation`).
- [ ] Pruebas unitarias (`JUnit 5 + Mockito`) cubriendo los 3 escenarios (`CA-05`, `CA-06`, `CA-07`).
- [ ] Prueba de integración verificando que al poner un vehículo `EN_MANTENIMIENTO` se desvincula del repartidor activo.
- [ ] Panel de Vehículos implementado en React + Tailwind con tabla responsive y filtros por tipo, estado y placa.
- [ ] Formulario de Vehículo con validación de capacidad en tiempo real (valores positivos).
- [ ] Respuestas HTTP alineadas al contrato en [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
