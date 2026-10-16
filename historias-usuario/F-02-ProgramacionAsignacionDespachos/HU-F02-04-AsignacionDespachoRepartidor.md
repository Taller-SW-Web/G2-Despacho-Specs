# [HU-F02-04] Asignación de Despacho a Repartidor con Validación Tridimensional

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend, Integración |
| **Etiquetas (Labels)** | `despacho`, `f-02`, `sdd`, `asignacion`, `capacidad`, `concurrencia` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** asignar un despacho pendiente a un repartidor en turno activo validando su capacidad remanente en kg, m³ y paquetes mediante un modal interactivo  
**PARA** garantizar que el pedido sea transportado sin sobrecargar la furgoneta, asignándole su posición en la ruta y reservando la capacidad operativa en la flota.

---

## 2. Descripción y Contexto Técnico

- **Especificación SDD origen:** [ES-F02-04: Asignar despacho a un repartidor](../../especificaciones/ES-F02-04-AsignarDespachoRepartidor/spec.md).
- **Especificación funcional padre:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-03`; Criterios `CA-06`, `CA-07`, `CA-08`, `CA-09`).
- **Endpoints asociados:**
  - `POST /api/v1/despachos/{idDespacho}/asignacion` (detallado en [integraciones/api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación)).
  - Reserva interna en Operación: `POST /internal/v1/operacion/capacidad/reserva` ([api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación)).
- **Roles requeridos:** `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Modal de asignación centrado con resumen del despacho (peso, volumen, paquetes).
  - Tarjetas de repartidores agrupadas (primero los de la zona del despacho).
  - Tres barras de ocupación simultáneas con proyección sombreada de carga.
  - Bloqueo visual del botón de confirmación ante sobrecarga o fecha futura.
- **Reglas de negocio y transaccionalidad:**
  - Evaluación tridimensional obligatoria: el despacho debe cumplir `peso <= capacidadPesoRemanente`, `volumen <= capacidadVolumenRemanente` y `paquetes <= capacidadPaquetesRemanente`. Si excede cualquiera, responde `422 Unprocessable Entity`.
  - El repartidor debe estar en estado `DISPONIBLE` o `EN_RUTA`. Si está `FUERA_DE_TURNO`, `INACTIVO` o `SATURADO`, responde `409 Conflict`.
  - Control de concurrencia optimista (`@Version`): si el despacho ya fue asignado o modificado, responde `409 Conflict`.
  - Al confirmarse, se asigna la siguiente posición en la ruta (`MAX + 1`) y cambia a `ASIGNADO`.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-06: Asignación exitosa dentro de la capacidad disponible**
  - **DADO** un despacho en `PENDIENTE_ASIGNACION` programado para hoy y un repartidor en estado `DISPONIBLE` o `EN_RUTA` cuya capacidad remanente en F-06 cubre su peso, volumen y cantidad de paquetes.
  - **CUANDO** el Gestor confirma la asignación en `POST /api/v1/despachos/{idDespacho}/asignacion`, ingresando opcionalmente instrucciones de entrega.
  - **ENTONCES** el sistema cambia el estado a `ASIGNADO`, registra el repartidor, la jornada actual y las observaciones, asigna la siguiente posición de la secuencia de ruta, reserva la capacidad en F-06, registra la auditoría y responde `200 OK`.

- [ ] **CA-07: Rechazo por capacidad excedida**
  - **DADO** un despacho cuyo peso, volumen o cantidad de paquetes supera la capacidad remanente del repartidor.
  - **CUANDO** el Gestor intenta confirmar la asignación.
  - **ENTONCES** el sistema responde `422 Unprocessable Entity`, indica el límite excedido ("Capacidad de carga del repartidor excedida: [peso / volumen / paquetes]") y mantiene el despacho en `PENDIENTE_ASIGNACION`.

- [ ] **CA-08: Rechazo por repartidor no habilitado**
  - **DADO** un repartidor en estado operativo `FUERA_DE_TURNO` o `SATURADO`, o con registro `INACTIVO`.
  - **CUANDO** se intenta asignarle un despacho.
  - **ENTONCES** el sistema responde `409 Conflict` y mantiene el despacho en la cola.

- [ ] **CA-09: Despacho en estado incompatible o ya asignado**
  - **DADO** un despacho que ya fue asignado o que no está en `PENDIENTE_ASIGNACION`.
  - **CUANDO** se ejecuta una asignación concurrente o desactualizada.
  - **ENTONCES** el sistema responde `409 Conflict` e informa que el despacho ya fue procesado.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Caso de uso de asignación implementado con `@Transactional` e integración con cliente de Operación (F-06).
- [ ] Control de concurrencia optimista con `@Version` validado ante peticiones simultáneas.
- [ ] Pruebas unitarias completas con `JUnit 5 + Mockito` cubriendo los 4 escenarios (`CA-06`, `CA-07`, `CA-08`, `CA-09`).
- [ ] Modal interactivo en React + Mantine con proyección tridimensional de barras y bloqueo de confirmación.
- [ ] Respuestas HTTP alineadas al contrato en [integraciones/api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).
- [ ] Documentación y trazabilidad sincronizadas con [ES-F02-04](../../especificaciones/ES-F02-04-AsignarDespachoRepartidor/spec.md).
