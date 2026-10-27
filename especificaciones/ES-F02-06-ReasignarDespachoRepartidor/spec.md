# ES-F02-06: Reasignar despacho a otro repartidor

**Funcionalidad padre:** [F-02 — Programación y asignación de despachos](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-07, CA-15 y CA-16.

**Responsable:** Tarqui.

**Estado:** Coordinación durable y UI implementadas y verificadas localmente; aceptación humana y Seguridad real pendientes. Consultar evidence.md.

**Actor principal:** Gestor de Despacho (aplicación web administrativa).

**Servicio propietario:** Gestión de Despachos.

**UI:** Aplica; modal interactivo de reasignación invocado desde la vista de Rutas por Repartidor, documentado en [ui.md](./ui.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md) y [UI](./ui.md). La solicitud versionada, idempotencia, cerco y recuperación se definen en [Gestión §3.2.2](../../integraciones/api-contract-gestion-despachos.md#322-reasignación-recuperable--es-f02-06); no se confunde atomicidad local de F-06 con una transacción distribuida.

## 1. Contexto y objetivo

Durante la jornada pueden surgir incidencias operativas en el centro de despacho, tales como averías mecánicas en una furgoneta, retrasos o sobrecarga inesperada, que requieran transferir un paquete ya asignado hacia otro repartidor habilitado antes de que inicie su traslado.

El objetivo es permitir al Gestor de Despacho transferir de forma transaccional un despacho en estado `ASIGNADO` hacia otro repartidor en turno activo. La funcionalidad valida que el nuevo repartidor cuente con capacidad remanente suficiente en peso, volumen y paquetes (F-06), exige el registro obligatorio de un motivo de reasignación, reubica el despacho al final de la ruta del nuevo repartidor, lo retira de la ruta original y actualiza atómicamente las reservas de capacidad en ambas furgonetas [cite: 1].

## 2. Alcance

- Incluye: selección de nuevo repartidor habilitado para la jornada; validación tridimensional de capacidad libre en el destinatario; exigencia obligatoria de motivo de reasignación; actualización de capacidad en F-06 (liberación en la furgoneta original y reserva en la nueva furgoneta); reubicación del despacho al final de la secuencia de ruta del nuevo repartidor; remoción de la ruta del repartidor previo; registro de auditoría con ambos choferes y el motivo (RT-02).
- Fuera de alcance: reasignar despachos en estado `EN_CAMINO`, `ENTREGADO` o `FALLIDO` (bloqueados permanentemente); modificación de datos comerciales o del destino del paquete; división de paquetes entre repartidores.

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- El Gestor está autenticado con JWT y posee el rol `GESTOR_DESPACHO`.
- El despacho existe y se encuentra estrictamente en estado `ASIGNADO` (permanece en el centro de despacho).
- El nuevo repartidor está habilitado para la jornada (`DISPONIBLE` o `EN_RUTA`) y es distinto del repartidor actualmente asignado.
- La capacidad remanente del nuevo repartidor en F-06 cubre simultáneamente el peso, volumen y cantidad física de paquetes del despacho.
- La solicitud incluye un motivo no vacío (`motivo`) que justifique el cambio operativo.

### 3.2. Dependencias

- **Disponibilidad y Capacidad Diaria (F-06):** gestiona la liberación en el repartidor saliente y la reserva en el nuevo repartidor conforme a [api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación).
- **Web del Repartidor (F-03):** retira el despacho de la lista del conductor anterior y lo añade en la ruta del nuevo conductor.
- **Trazabilidad (ES-F02-08 / RT-02):** registra la auditoría con repartidor origen, repartidor destino y motivo.
- **Contrato de API:** [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).

### 3.3. Resultados

- Despacho actualizado: conserva estado `ASIGNADO`, nuevo `idRepartidor`, nuevo `idJornada` y nueva `posicionSecuencia` al final de la ruta destino.
- Capacidad ajustada en F-06: cupo liberado en el repartidor original y reservado en el nuevo.
- Respuesta HTTP `200 OK` con los datos del despacho reasignado.
- Registro de auditoría persistido inmutablemente.

## 4. Flujo principal y alternativas

1. Desde la vista "Rutas por repartidor", el Gestor pulsa el botón "Reasignar" en un despacho en estado `ASIGNADO`.
2. Se abre el modal de reasignación mostrando los datos del despacho, el repartidor actual y la lista de otros repartidores disponibles.
3. El Gestor selecciona al nuevo repartidor y visualiza la proyección de las tres barras de ocupación.
4. Ingresa obligatoriamente el motivo de la reasignación (ej. "Avería mecánica en furgoneta original").
5. Pulsa "Confirmar reasignación".
6. El backend:
   - Valida que el despacho continúe en `ASIGNADO` mediante bloqueo optimista (`@Version`).
   - Verifica que el motivo no esté en blanco.
   - Solicita a F-06 la transferencia o reserva en el nuevo repartidor y liberación en el anterior.
   - Retira el despacho de la ruta original y calcula la nueva secuencia (`MAX + 1` en la ruta destino).
   - Actualiza el despacho en base de datos e incrementa su versión.
   - Persiste la auditoría con ambos repartidores, el usuario gestor y el motivo.
7. Responde `200 OK`.
8. La interfaz cierra el modal, muestra toast de confirmación y actualiza reactivamente las rutas.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Motivo ausente | El campo `motivo` está en blanco o nulo | Responde `400 Bad Request` ("El motivo de reasignación es obligatorio") | CA-02 |
| Capacidad insuficiente | El nuevo repartidor no tiene cupo en peso, volumen o paquetes | Responde `422 Unprocessable Entity` ("Capacidad de carga del nuevo repartidor excedida") | CA-03 |
| Despacho en traslado o cerrado | El despacho pasó a `EN_CAMINO`, `ENTREGADO` o `FALLIDO` | Responde `409 Conflict` y conserva el repartidor original | CA-04 |
| Repartidor saturado o no disponible | El nuevo chofer está `SATURADO`, `FUERA_DE_TURNO` o inactivo | Responde `409 Conflict` informando la inhabilitación | CA-05 |
| Mismo repartidor | Se selecciona el mismo repartidor que ya tiene asignado el paquete | Responde `400 Bad Request` ("El nuevo repartidor debe ser diferente al actual") | CA-02 |
| Conflicto concurrente | El chofer inició el traslado mientras se confirmaba el modal | Responde `409 Conflict`, recarga la ruta y cierra el modal | CA-06 |
| Sin rol Gestor | Petición sin rol `GESTOR_DESPACHO` | Responde `403 Forbidden` | CA-07 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Solo los despachos en estado `ASIGNADO` pueden ser reasignados. | F-02 RF-07, CA-16 |
| RN-02 | El motivo de reasignación es estrictamente obligatorio para fines de auditoría. | F-02 RF-07, CA-15 |
| RN-03 | El despacho reasignado se ubica siempre en la última posición (`MAX + 1`) de la ruta del nuevo repartidor. | F-02 CA-15 |
| RN-04 | La transferencia de reservas es localmente atómica en F-06 conforme a §5.3.1. Gestión necesita intención durable y bloqueo del traslado para consolidar/recuperar el cambio; no existe atomicidad distribuida implícita. | api-contract-operacion-reparto.md §5.3.1 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `POST /api/v1/despachos/{idDespacho}/reasignacion` | Endpoint canónico de reasignación. | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) |
| Integración de Capacidad (F-06) | Liberación en chofer origen y reserva en chofer destino. | [api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación) |
| Auditoría (RT-02) | Registro de la reasignación con ambos repartidores. | [ES-F02-08](../ES-F02-08-RegistrarTrazabilidadOperaciones/spec.md) |

## 6. Criterios de aceptación

### CA-01. Reasignación exitosa de despacho ASIGNADO con motivo obligatorio

- **DADO** un despacho en estado `ASIGNADO` y otro repartidor habilitado con capacidad remanente suficiente en kg, m³ y paquetes en F-06.
- **CUANDO** el Gestor confirma la reasignación en `POST /api/v1/despachos/{idDespacho}/reasignacion` enviando un motivo válido.
- **ENTONCES** el despacho actualiza su asignación al nuevo chofer, se ubica al final de su ruta, se retira de la ruta del chofer anterior, F-06 actualiza las reservas en ambas furgonetas, se audita la operación con ambos repartidores y el motivo, y el backend responde `200 OK`.

### CA-02. Rechazo por omisión de motivo o mismo repartidor

- **DADO** una solicitud de reasignación con el campo `motivo` vacío o que especifica como nuevo repartidor al mismo que ya tenía asignado el despacho.
- **CUANDO** es evaluada en el backend.
- **ENTONCES** el sistema responde `400 Bad Request` indicando el error de validación y mantiene la asignación original sin cambios.

### CA-03. Rechazo por capacidad insuficiente en nuevo repartidor

- **DADO** un despacho que supera el peso, volumen o paquetes disponibles del nuevo repartidor propuesto.
- **CUANDO** se intenta confirmar la reasignación.
- **ENTONCES** el backend responde `422 Unprocessable Entity` ("Capacidad de carga del repartidor excedida"), no modifica los balances de flota y conserva el despacho en su ruta actual.

### CA-04. Rechazo de reasignación de despacho en camino o cerrado

- **DADO** un despacho en estado `EN_CAMINO`, `ENTREGADO`, `FALLIDO` o `CANCELADO`.
- **CUANDO** se envía una petición de reasignación.
- **ENTONCES** el backend responde `409 Conflict`, no realiza modificaciones y mantiene el repartidor original.

### CA-05. Rechazo por nuevo repartidor saturado o no disponible

- **DADO** un repartidor destino que se encuentra en `FUERA_DE_TURNO`, `SATURADO` o inactivo.
- **CUANDO** se intenta transferirle un despacho.
- **ENTONCES** el sistema rechaza la solicitud con código `409 Conflict` informando el estado del operador.

### CA-06. Conflicto de concurrencia al reasignar

- **DADO** que el repartidor original marcó "En camino" en su aplicación móvil mientras el Gestor preparaba la reasignación.
- **CUANDO** se procesa la confirmación en Gestión.
- **ENTONCES** el bloqueo optimista detecta el cambio de estado, responde `409 Conflict` e instruye recargar la ruta.

### CA-07. Acceso sin permisos requeridos

- **DADO** un usuario autenticado sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta reasignar un despacho.
- **ENTONCES** el sistema responde `403 Forbidden` y no altera ninguna ruta ni reserva.

## 7. Referencias

1. [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md): requisito RF-07 y criterios CA-15 y CA-16.
2. [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación): endpoint de reasignación.
3. [ui.md](./ui.md): especificación visual y de interacción modal.
