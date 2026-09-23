# [HU-F05-01] Registro y Gestión de Repartidores

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-05: Monitoreo de Flota, Operadores y Capacidad Diaria |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-05`, `sdd`, `repartidores`, `gestion` |
| **Responsable sugerido** | Rhamses |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Flota
**QUIERO** registrar nuevos repartidores, editar sus datos, consultar el listado de operadores y cambiar su estado operativo
**PARA** mantener actualizado el padrón de personal disponible para ejecutar despachos y controlar quién puede recibir asignaciones.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-05-MonitoreoFlotaCapacidad.md](../../funcionalidades/F-05-MonitoreoFlotaCapacidad.md) (Requisito `RF-01`, Criterios `CA-01`, `CA-02`, `CA-03`, `CA-04`).
- **Endpoints asociados:**
  - `POST /api/v1/repartidores` — Alta de nuevo repartidor (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md) §7.3).
  - `GET /api/v1/repartidores` — Listado paginado con filtros por estado y turno.
  - `PUT /api/v1/repartidores/{idRepartidor}` — Modificación de datos personales y estado operativo.
- **Roles requeridos:** `GESTOR_FLOTA` o `ADMIN_DESPACHO` (autenticación JWT). Usuarios sin estos roles deben recibir `403 Forbidden`.
- **Componentes de Frontend:**
  - Panel de Repartidores: listado paginado con filtros por estado y turno, y acciones para registrar, editar o cambiar el estado de un operador.
  - Formulario de Repartidor: campos para nombres, apellidos, DNI, teléfono, número de brevete y turno habitual.
- **Reglas de negocio:**
  - El DNI del repartidor debe ser único en el sistema; un intento de duplicar el documento se responde con `409 Conflict`.
  - Un repartidor recién registrado queda automáticamente en estado `INACTIVO` hasta que se le asigne un turno y un vehículo.
  - La desactivación de un repartidor con historial de despachos se aplica como baja lógica (sin eliminación física) para preservar la trazabilidad.
  - Un repartidor en estado `INACTIVO` no aparece en las respuestas del endpoint de disponibilidad (`GET /api/v1/repartidores/disponibles`).
- **Entidades de datos involucradas:** `repartidores` (ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-01: Registro exitoso de un nuevo repartidor**
  - **DADO** que el Gestor de Flota ingresa los datos de un nuevo operador: nombres, apellidos, DNI, teléfono, número de brevete y turno habitual.
  - **CUANDO** confirma el registro en `POST /api/v1/repartidores`.
  - **ENTONCES** el sistema valida que el DNI no exista previamente, crea el repartidor con estado `INACTIVO` y devuelve su identificador único con código `201 Created`.

- [ ] **CA-02: Rechazo por documento de identidad duplicado**
  - **DADO** que ya existe un repartidor registrado con un DNI determinado.
  - **CUANDO** se intenta registrar otro operador con el mismo número de documento.
  - **ENTONCES** el sistema rechaza la operación con código `409 Conflict` e indica que el documento ya está registrado, sin persistir el duplicado.

- [ ] **CA-03: Desactivación de un repartidor con despachos históricos**
  - **DADO** que un repartidor tiene despachos finalizados asociados en el historial.
  - **CUANDO** el Gestor cambia su estado a `INACTIVO` mediante `PUT /api/v1/repartidores/{idRepartidor}`.
  - **ENTONCES** el sistema aplica baja lógica (no elimina el registro), lo excluye de nuevas asignaciones y preserva su historial de entregas intacto.

- [ ] **CA-04: Acceso sin permisos requeridos**
  - **DADO** que un usuario sin el rol `GESTOR_FLOTA` ni `ADMIN_DESPACHO` intenta registrar o modificar repartidores.
  - **CUANDO** realiza la petición al backend.
  - **ENTONCES** el sistema rechaza la solicitud con código `403 Forbidden` y no expone información del personal.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Código implementado en Java 21 / Spring Boot siguiendo las convenciones de [AGENTS.md](../../AGENTS.md).
- [ ] Entidad JPA y repositorio para `repartidores` implementados en Spring Data con restricción de unicidad sobre DNI.
- [ ] DTOs de entrada validados con anotaciones `@NotNull`, `@NotBlank`, `@Size` (`jakarta.validation`).
- [ ] Baja lógica implementada sin eliminación física del registro.
- [ ] Pruebas unitarias (`JUnit 5 + Mockito`) cubriendo los 4 escenarios (`CA-01`, `CA-02`, `CA-03`, `CA-04`).
- [ ] Pruebas de seguridad (`Spring Security Test`) verificando `403 Forbidden` para roles incorrectos o usuarios anónimos.
- [ ] Panel de Repartidores implementado en React + Tailwind con tabla responsive, filtros, skeleton loaders y estado visual vacío.
- [ ] Formulario de Repartidor con validación visual en tiempo real.
- [ ] Respuestas HTTP alineadas al contrato en [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
