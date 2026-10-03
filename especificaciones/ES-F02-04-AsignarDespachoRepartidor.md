# ES-F02-04: Asignar despacho a un repartidor

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho (aplicación web)

## 1. Objetivo

Asignar un despacho pendiente, cuya fecha programada sea igual o anterior a la fecha actual, a un repartidor habilitado en la jornada de hoy. La asignación valida de forma transaccional y en tiempo real que no se sobrepase la capacidad remanente de la furgoneta en sus tres dimensiones obligatorias (peso en kg, volumen en m³ y paquetes físicos) provistas por F-06. La operación transiciona el despacho al estado `ASIGNADO`, lo ubica automáticamente al final de la secuencia de ruta del repartidor, registra observaciones de entrega y reserva la capacidad en la flota.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO` mediante token JWT.
- El despacho existe y se encuentra en estado `PENDIENTE_ASIGNACION`.
- La fecha programada del despacho es igual o anterior al día actual del servidor.
- El repartidor seleccionado cuenta con una jornada operativa abierta hoy en F-06 y su estado operativo es `DISPONIBLE` o `EN_RUTA`.
- El servicio de Disponibilidad y Capacidad Diaria (F-06) provee la capacidad remanente y límites de la furgoneta asignada.

## 3. Flujo principal

1. El Gestor pulsa "Asignar" en la fila de un despacho habilitado en la cola de pendientes.
2. El frontend abre el modal de asignación mostrando el resumen físico del despacho (código, pedido, zona, dirección, peso en kg, volumen en m³, cantidad de paquetes y fecha) y solicita a F-06 los repartidores en jornada.
3. El modal despliega los repartidores agrupados en dos listas: primero los repartidores asignados a la zona del despacho y posteriormente los de otras zonas.
4. El Gestor selecciona un repartidor; el modal calcula y dibuja la proyección rayada en las tres barras de ocupación (kg, m³ y paquetes).
5. Se verifica que ninguna de las tres barras supere el 100 % de ocupación resultante.
6. El Gestor ingresa opcionalmente observaciones o instrucciones de entrega y pulsa "Confirmar asignación".
7. El backend procesa la asignación de manera transaccional:
   - Valida mediante bloqueo optimista que el despacho continúe en `PENDIENTE_ASIGNACION`.
   - Consulta a F-06 la capacidad libre y confirma que cubre el peso, volumen y cantidad de paquetes.
   - Cambia el estado del despacho a `ASIGNADO`.
   - Registra el `idRepartidor`, `idJornada`, marca temporal y la observación en la entidad despacho.
   - Asigna la posición correlativa final (N+1) en la secuencia de ruta de esa jornada.
   - Solicita a F-06 la reserva de capacidad de los tres recursos físicos en la furgoneta.
   - Registra el historial de trazabilidad y auditoría.
8. El backend responde `200 OK` con los datos del despacho asignado, repartidor y número de parada en ruta.
9. El frontend notifica "Despacho [código] asignado a [repartidor]" y retira el despacho de la tabla de pendientes.

## 4. Reglas y validaciones

- **Evaluación tridimensional obligatoria de capacidad:**
  - `pesoActual + pesoDespacho <= limitePesoKg`
  - `volumenActual + volumenDespacho <= limiteVolumenM3`
  - `paquetesActuales + paquetesDespacho <= limitePaquetes`
  - Si cualquiera de los tres límites se sobrepasa, la operación se bloquea visualmente en el cliente y, ante un intento forzado, el backend responde `422 Unprocessable Entity` indicando el recurso excedido ("Capacidad de carga del repartidor excedida: [peso / volumen / paquetes]").
- **Restricción de estado operativo del repartidor:** solo pueden recibir asignaciones repartidores con estado operativo `DISPONIBLE` o `EN_RUTA`. Un repartidor en `SATURADO`, `FUERA_DE_TURNO` o registro `INACTIVO` genera un rechazo `409 Conflict`.
- **Restricción temporal del despacho:** solo se asignan despachos en `PENDIENTE_ASIGNACION` cuya `fechaProgramada <= fechaActual`. Si un despacho tiene fecha futura, el backend rechaza la asignación con `409 Conflict`.
- **Ubicación en ruta:** todo nuevo despacho asignado se añade automáticamente en la última posición disponible de la secuencia de la jornada (parada N+1).
- **Concurrencia optimista:** si otro usuario gestor asignó el mismo despacho o si el repartidor dejó de estar habilitado antes de confirmar, el sistema responde `409 Conflict` ("El despacho ya fue procesado"), no realiza cambios y solicita actualizar la cola.
- **Observaciones:** campo opcional de texto libre de hasta 250 caracteres preservado para consulta del repartidor en F-03.
- **Persistencia transaccional:** la actualización del despacho, la posición en la jornada y la reserva de capacidad en F-06 ocurren en una misma transacción lógica.

## 5. Entradas, salidas e integraciones

### Entradas

- Ruta: `POST /api/v1/despachos/{idDespacho}/asignacion`.
- Payload JSON conforme a `integraciones/api-contract.md`:
  - `idRepartidor` (string, ej. `REP-0012`).
  - `idJornada` (string, ej. `JOR-20260923-0012`).
  - `observacion` (opcional, string).
- Encabezado `Authorization: Bearer <jwt_usuario>`.

### Salidas

- Respuesta HTTP `200 OK`:
  - `idDespacho`: identificador del despacho.
  - `estado`: `ASIGNADO`.
  - `idRepartidor`: repartidor asignado.
  - `idJornada`: identificador de la jornada.
  - `posicionSecuencia`: número de parada en ruta.
  - `fechaAsignacion`: marca temporal en UTC.
- Notificación de confirmación en la UI y retiro del despacho de la cola.
- Errores normalizados: `400 Bad Request`, `403 Forbidden`, `409 Conflict` o `422 Unprocessable Entity`.

### Integraciones

- **Disponibilidad y Capacidad Diaria (F-06):** provee los repartidores en jornada y procesa la reserva de capacidad en kg, m³ y paquetes.
- **Web del Repartidor (F-03):** expone el despacho en "Mi Ruta" una vez que adquiere el estado `ASIGNADO`.
- **Trazabilidad (ES-F02-08):** registra la auditoría con los datos del gestor y la ocupación resultante.
- El contrato del endpoint sigue estrictamente `integraciones/api-contract.md` (Sección 9.2).

## 6. Criterios de aceptación

### CA-01. Asignación exitosa dentro de la capacidad disponible

- **DADO** un despacho en `PENDIENTE_ASIGNACION` programado para hoy y un repartidor en estado `DISPONIBLE` con capacidad remanente suficiente en peso, volumen y paquetes en F-06.
- **CUANDO** el Gestor confirma la asignación en el modal.
- **ENTONCES** el despacho cambia a estado `ASIGNADO`, se le asigna la última posición en la ruta del repartidor, F-06 registra la reserva de capacidad en sus tres variables y el backend responde `200 OK`.

### CA-02. Rechazo por capacidad excedida (peso, volumen o paquetes)

- **DADO** un repartidor cuya capacidad remanente en paquetes es 2, y un despacho que contiene 3 paquetes físicos.
- **CUANDO** el Gestor intenta confirmar la asignación a dicho repartidor.
- **ENTONCES** el modal muestra la alerta de sobrecarga, el backend responde `422 Unprocessable Entity` ("Capacidad de carga del repartidor excedida: paquetes") y el despacho continúa en `PENDIENTE_ASIGNACION`.

### CA-03. Rechazo por repartidor no habilitado o saturado

- **DADO** un repartidor que pasó a estado operativo `SATURADO` o cerró su jornada a `FUERA_DE_TURNO` concurrentemente.
- **CUANDO** se intenta confirmar la asignación del despacho.
- **ENTONCES** el backend responde `409 Conflict` informando que el repartidor no está habilitado y conserva el despacho en la cola de pendientes.

### CA-04. Despacho asignado concurrentemente

- **DADO** un despacho que ya fue asignado por otro Gestor desde otra sesión.
- **CUANDO** el usuario intenta confirmar la asignación sobre la pantalla desactualizada.
- **ENTONCES** el backend responde `409 Conflict` indicando que el despacho ya fue procesado, cierra el modal y recarga la cola.

### CA-05. Intento de asignar despacho con fecha futura

- **DADO** un despacho en `PENDIENTE_ASIGNACION` programado para una fecha posterior a hoy.
- **CUANDO** se envía una solicitud de asignación.
- **ENTONCES** el sistema responde `409 Conflict` y mantiene el despacho en cola con asignación bloqueada hasta que llegue su fecha.

### CA-06. Acceso sin permisos

- **DADO** un usuario autenticado sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta ejecutar la asignación.
- **ENTONCES** el backend responde `403 Forbidden` y no procesa la asignación.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Asignación manual de turnos, jornadas o furgonetas (responsabilidad de F-05 y F-06).
- Reordenar la ruta del repartidor tras la asignación (corresponde a ES-F02-05).
- Inicio de traslado o confirmación de entrega física (corresponde a F-03).

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-03).
- Contrato de API: `integraciones/api-contract.md` (Sección 9.2).
- Disponibilidad y capacidad de flota: `funcionalidades/F-06-DisponibilidadCapacidadDiaria.md`.
- Diseño de interfaz: `disenio/funcionalidades/f-02.md` (Pantalla 2).
