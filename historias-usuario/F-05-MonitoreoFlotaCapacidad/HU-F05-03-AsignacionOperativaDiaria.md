# [HU-F05-03] Asignación Operativa Diaria Repartidor–Vehículo

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-05: Monitoreo de Flota, Operadores y Capacidad Diaria |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-05`, `sdd`, `asignacion-diaria`, `turno`, `capacidad` |
| **Responsable sugerido** | Rhamses |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Flota
**QUIERO** vincular a cada repartidor un vehículo para la jornada en curso, activándolo con los límites de carga de esa unidad
**PARA** que el Panel de Programación (F-02) disponga de operadores habilitados con capacidad real confirmada al momento de asignar despachos.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-05-MonitoreoFlotaCapacidad.md](../../funcionalidades/F-05-MonitoreoFlotaCapacidad.md) (Requisito `RF-03`, Criterios `CA-08`, `CA-09`).
- **Endpoints asociados:**
  - `POST /api/v1/repartidores/{idRepartidor}/asignacion-diaria` — Vincular repartidor con vehículo para la jornada activa (a consolidar en [integraciones/api-contract.md](../../integraciones/api-contract.md)).
- **Roles requeridos:** `GESTOR_FLOTA` o `ADMIN_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Interfaz de Asignación Diaria: selector de repartidor y vehículo disponibles con validación de disponibilidad antes de confirmar.
  - Indicador visual del estado del repartidor tras confirmar la asignación (`DISPONIBLE`).
- **Reglas de negocio:**
  - Solo puede existir una asignación operativa activa por repartidor por jornada. Un segundo intento en el mismo día para el mismo operador se responde con `409 Conflict`.
  - Al confirmar la asignación, el repartidor transiciona a estado `DISPONIBLE` y hereda los límites de carga del vehículo asignado (peso en kg, volumen en m³ y tope de paquetes diarios).
  - Solo pueden participar repartidores en estado `INACTIVO` (sin turno activo) y vehículos en estado `DISPONIBLE`.
  - La asignación diaria activa al operador y lo incluye inmediatamente en las respuestas de `GET /api/v1/repartidores/disponibles`.
- **Entidades de datos involucradas:** `repartidores`, `vehiculos`, `turnos_operador` (ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-08: Asignación diaria exitosa**
  - **DADO** que el Gestor selecciona al repartidor "Juan Pérez" (estado `INACTIVO`) y la furgoneta "ABC-123" (estado `DISPONIBLE`) para la jornada del día.
  - **CUANDO** confirma la asignación operativa.
  - **ENTONCES** el sistema activa al repartidor con estado `DISPONIBLE`, le asigna los límites de la furgoneta (500 kg, 4.0 m³, 80 paquetes) y lo incluye en las respuestas del endpoint de disponibilidad.

- [ ] **CA-09: Rechazo por asignación duplicada en la misma jornada**
  - **DADO** que el repartidor "Juan Pérez" ya tiene una asignación operativa activa en la jornada actual.
  - **CUANDO** se intenta crear otra asignación para el mismo operador en el mismo día.
  - **ENTONCES** el sistema rechaza la operación con código `409 Conflict` e indica que el repartidor ya fue asignado en esta jornada.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Código implementado en Java 21 / Spring Boot siguiendo las convenciones de [AGENTS.md](../../AGENTS.md).
- [ ] Servicio de asignación diaria implementado con `@Transactional`, validación de unicidad por repartidor y jornada, y herencia de límites del vehículo.
- [ ] Entidad JPA y repositorio para `turnos_operador` con restricción de unicidad `(idRepartidor, fechaJornada)`.
- [ ] Pruebas unitarias (`JUnit 5 + Mockito`) cubriendo los 2 escenarios (`CA-08`, `CA-09`).
- [ ] Prueba de integración verificando que el repartidor asignado aparece en `GET /api/v1/repartidores/disponibles` con los límites correctos.
- [ ] Interfaz de Asignación Diaria implementada en React + Tailwind con validación de disponibilidad antes de confirmar.
- [ ] Endpoint de asignación diaria consolidado en [integraciones/api-contract.md](../../integraciones/api-contract.md) antes de cerrar la historia.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
