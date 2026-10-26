# ES-F02-04: Asignar despacho a un repartidor

**Funcionalidad padre:** [F-02 — Programación y asignación de despachos](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-03 y RF-06.

**Responsable:** Tarqui.

**Estado:** Backend de Gestión implementado y verificado con Operación HTTP simulada; proveedor real e interfaz funcional pendientes. Ver [evidence.md](./evidence.md).

**Actor principal:** Gestor de Despacho (aplicación web administrativa).

**Servicio propietario:** Gestión de Despachos.

**UI:** Aplica; modal interactivo de asignación en el panel administrativo, documentado en [ui.md](./ui.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md) y [UI](./ui.md). Preparación del 16/10/2026; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

Cuando un despacho está en el centro en estado `PENDIENTE_ASIGNACION` y su fecha programada es igual o anterior al día de hoy, el Gestor de Despacho debe asignarlo a un repartidor en turno activo. La asignación define la jornada y ubica el despacho al final de la secuencia de ruta del operador.

El objetivo es ejecutar la asignación validando de forma transaccional y en tiempo real que no se sobrepase la capacidad remanente de la furgoneta en sus tres dimensiones obligatorias simultáneas (peso en kg, volumen en m³ y cantidad física de paquetes), provistas por F-06. La operación transiciona el despacho al estado `ASIGNADO`, reserva la capacidad operativa en Operación de Reparto y Flota, y deja el despacho listo para el consumo de la web del repartidor (F-03) [cite: 1].

## 2. Alcance

- Incluye: selección de repartidor disponible en jornada activa; validación tridimensional de capacidad (kg, m³, paquetes) consultando F-06; registro de observaciones opcionales de entrega; transición de estado a `ASIGNADO`; asignación de la siguiente posición en la secuencia de ruta; reserva de capacidad en F-06 mediante clave técnica idempotente; control de concurrencia optimista (`@Version`); auditoría con usuario gestor y ocupación resultante (RT-02).
- Fuera de alcance: reordenar la secuencia de ruta tras la asignación (ES-F02-05); reasignar a otro repartidor (ES-F02-06); ejecución del traslado en campo (F-03); definición inicial de turnos o furgonetas (F-05/F-06).

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- El Gestor está autenticado con JWT y rol `GESTOR_DESPACHO`.
- El despacho existe y se encuentra estrictamente en estado `PENDIENTE_ASIGNACION`.
- La fecha programada del despacho es menor o igual a la fecha civil de hoy en `America/Lima`.
- Si el despacho proviene de una reprogramación previa (F-04), cualquier reserva de capacidad de su salida anterior debe encontrarse liberada en F-06.
- El repartidor seleccionado está en estado operativo `DISPONIBLE` o `EN_RUTA` y cuenta con jornada abierta para hoy.
- La capacidad remanente del repartidor en F-06 cubre simultáneamente: `pesoDespacho <= capacidadPesoRemanente`, `volumenDespacho <= capacidadVolumenRemanente` y `cantidadPaquetes <= capacidadPaquetesRemanente`.

### 3.2. Dependencias

- **Disponibilidad y Capacidad Diaria (F-06):** provee los repartidores en jornada y procesa la reserva de capacidad conforme a [api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación).
- **Web del Repartidor (F-03):** visualiza los despachos en estado `ASIGNADO` con su jornada y secuencia.
- **Trazabilidad (ES-F02-08 / RT-02):** registra la auditoría con la ocupación resultante.
- **Contrato de API:** [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).

### 3.3. Resultados

- Despacho actualizado a estado `ASIGNADO`, con `idRepartidor`, `idJornada`, `posicionSecuencia` y `observaciones` persistidos.
- Reserva de capacidad confirmada en F-06 con clave técnica única.
- Retiro inmediato del despacho de la cola de pendientes y respuesta HTTP `200 OK`.
- Registro de auditoría persistido atómicamente.

## 4. Flujo principal y alternativas

1. El Gestor pulsa "Asignar" en una fila de la cola de pendientes habilitada para hoy.
2. La interfaz abre el modal de asignación mostrando los datos del despacho y cargando los repartidores en jornada agrupados (primero los de la zona del despacho).
3. El Gestor selecciona un repartidor cuyas barras de capacidad en kg, m³ y paquetes admitan la carga proyectada.
4. Ingresa opcionalmente instrucciones o una observación de entrega y pulsa "Confirmar asignación".
5. El backend inicia la transacción:
   - Verifica que el despacho siga en `PENDIENTE_ASIGNACION` y que su versión coincida (bloqueo optimista).
   - Valida que `fechaProgramada <= hoy`.
   - Consulta a F-06 y ejecuta la reserva de capacidad en las tres dimensiones.
   - Determina la siguiente posición de la secuencia (`MAX(posicion) + 1` en la ruta del repartidor).
   - Transiciona el estado a `ASIGNADO` e incrementa la versión.
   - Persiste el registro de auditoría con la ocupación resultante.
6. El backend responde `200 OK` con los datos de asignación.
7. La interfaz cierra el modal, muestra toast de éxito y retira el despacho de la cola.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Capacidad excedida | Peso, volumen o paquetes superan el remanente en F-06 | Responde `422 Unprocessable Entity` ("Capacidad de carga excedida: [variable]") y mantiene en cola | CA-02 |
| Repartidor no habilitado | Repartidor en estado `FUERA_DE_TURNO`, `SATURADO` o inactivo | Responde `409 Conflict` informando que el repartidor no está habilitado | CA-03 |
| Conflicto concurrente | El despacho ya fue asignado o cancelado concurrentemente | Responde `409 Conflict` indicando que el despacho ya fue procesado | CA-04 |
| Fecha programada a futuro | Se intenta forzar asignación en `fechaProgramada > hoy` | Responde `409 Conflict` ("Despacho programado para fecha futura") | CA-05 |
| Reserva previa no liberada | Reprogramado con reserva de salida anterior activa | Responde `409 Conflict` hasta confirmar liberación en F-06 | CA-06 |
| Sin autorización | Token aceptado sin rol `GESTOR_DESPACHO` o petición sin token aceptado | Responde `403 Forbidden` o `401 Unauthorized`, respectivamente, según Común §3.5 | CA-07 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Evaluación tridimensional estricta: peso, volumen y paquetes deben cumplirse a la vez; sobrepasar cualquiera bloquea la asignación. | F-02 RF-03, CA-07 |
| RN-02 | Todo despacho asignado adquiere automáticamente la última posición en la secuencia de ruta de la jornada. | F-02 RF-06 |
| RN-03 | La asignación exige concurrencia optimista (`@Version`); si otro proceso mutó el despacho, la transacción se aborta con 409. | F-02 RNF Concurrencia |
| RN-04 | La reserva en F-06 utiliza una clave técnica idempotente; una asignación nueva genera una clave fresca y no reutiliza reservas pasadas. | api-contract-operacion-reparto.md §5.1 |
| RN-05 | No se permite asignar despachos con `fechaProgramada > hoy`. | F-02 RF-06, CA-13 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `POST /api/v1/despachos/{idDespacho}/asignacion` | Endpoint canónico de asignación. | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) |
| `POST /internal/v1/capacidad/reservas` | Reserva tridimensional en Operación. | [api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación) |
| Auditoría (RT-02) | Registro de la asignación en auditoría. | [ES-F02-08](../ES-F02-08-RegistrarTrazabilidadOperaciones/spec.md) |

## 6. Criterios de aceptación

### CA-01. Asignación exitosa dentro de la capacidad disponible

- **DADO** un despacho en `PENDIENTE_ASIGNACION` programado para hoy y un repartidor en estado `DISPONIBLE` o `EN_RUTA` cuya capacidad remanente en F-06 cubre su peso, volumen y paquetes.
- **CUANDO** el Gestor confirma la asignación en `POST /api/v1/despachos/{idDespacho}/asignacion`.
- **ENTONCES** el despacho cambia a estado `ASIGNADO`, se le asigna la última posición en la secuencia de ruta del repartidor, F-06 registra la reserva de capacidad en sus tres variables, se persiste la auditoría y el backend responde `200 OK`.

### CA-02. Rechazo por capacidad excedida (peso, volumen o paquetes)

- **DADO** un repartidor cuya capacidad remanente en paquetes es 2, y un despacho que contiene 3 paquetes físicos (o con peso/volumen excedido).
- **CUANDO** el Gestor intenta confirmar la asignación a dicho repartidor.
- **ENTONCES** el backend responde `422 Unprocessable Entity` ("Capacidad de carga del repartidor excedida: [paquetes/peso/volumen]"), no altera la capacidad de la furgoneta y mantiene el despacho en `PENDIENTE_ASIGNACION`.

### CA-03. Rechazo por repartidor no habilitado o fuera de turno

- **DADO** un repartidor que se encuentra en estado `FUERA_DE_TURNO`, `INACTIVO` o `SATURADO`.
- **CUANDO** se envía una solicitud para asignarle un despacho.
- **ENTONCES** el sistema rechaza la operación con código `409 Conflict`, detalla el motivo de la inhabilitación y mantiene el despacho en cola.

### CA-04. Despacho en estado incompatible o asignado concurrentemente

- **DADO** un despacho que ya fue asignado previamente por otro gestor o que no se encuentra en `PENDIENTE_ASIGNACION`.
- **CUANDO** se ejecuta una asignación concurrente o desactualizada.
- **ENTONCES** el backend detecta el conflicto mediante bloqueo optimista, responde `409 Conflict` e informa que el despacho ya fue procesado.

### CA-05. Intento de asignar despacho con fecha futura

- **DADO** un despacho en `PENDIENTE_ASIGNACION` cuya fecha programada es posterior al día de hoy.
- **CUANDO** se procesa una petición de asignación.
- **ENTONCES** el backend responde `409 Conflict` ("Despacho programado para fecha futura") y bloquea la operación hasta que llegue su fecha.

### CA-06. Rechazo por reserva anterior de salida previa no liberada

- **DADO** un despacho reprogramado por F-04 cuya reserva de capacidad en la salida anterior aún figura activa en Operación.
- **CUANDO** se intenta asignar una nueva salida.
- **ENTONCES** el sistema responde `409 Conflict` indicando que la reserva previa está en proceso de liberación y mantiene el despacho en cola.

### CA-07. Acceso sin permisos requeridos

- **DADO** un usuario autenticado sin el rol `GESTOR_DESPACHO` o una petición anónima.
- **CUANDO** intenta invocar el endpoint de asignación.
- **ENTONCES** el backend responde `403 Forbidden` si el token aceptado carece del rol, o `401 Unauthorized` si no hay token aceptado, según Común §3.5; no efectúa ninguna reserva ni cambio de estado.

## 7. Referencias

1. [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md): requisito RF-03 y criterios CA-06 a CA-09.
2. [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación): endpoint de asignación.
3. [api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación): integración de reserva tridimensional con F-06.
