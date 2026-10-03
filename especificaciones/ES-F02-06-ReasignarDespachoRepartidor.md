# ES-F02-06: Reasignar despacho a otro repartidor

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho (aplicación web)

## 1. Objetivo

Permitir que el Gestor de Despacho transfiera un despacho que aún permanece físicamente en el centro de despacho en estado `ASIGNADO` hacia otro repartidor habilitado para la jornada. La funcionalidad valida de forma transaccional que el repartidor destino posea capacidad remanente suficiente en peso, volumen y paquetes (F-06), exige el registro obligatorio de un motivo de reasignación, reubica el despacho en la última parada del nuevo repartidor y actualiza automáticamente las reservas de carga de ambas furgonetas.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO` mediante token JWT.
- El despacho existe y se encuentra estrictamente en estado `ASIGNADO`.
- El repartidor destino cuenta con jornada operativa abierta hoy en F-06 y su estado operativo es `DISPONIBLE` o `EN_RUTA`.
- El repartidor destino es distinto al repartidor que actualmente tiene asignado el despacho.
- F-06 reporta capacidad remanente suficiente en kg, m³ y paquetes para el repartidor destino.

## 3. Flujo principal

1. En la pestaña "Rutas por repartidor", el Gestor localiza un despacho en estado `ASIGNADO` y pulsa la acción de fila "Reasignar".
2. El sistema despliega el modal amplio de reasignación (880 px) presentando el resumen físico del despacho (código, pedido, zona, dirección, peso, volumen, paquetes) y la etiqueta destacada "Repartidor actual: [nombre] ([furgoneta])".
3. El modal muestra el catálogo de repartidores destino disponibles (excluyendo automáticamente al operador actual) con sus barras tridimensionales de ocupación.
4. El Gestor selecciona al nuevo repartidor y el modal dibuja la proyección rayada resultante en sus barras de carga.
5. El Gestor completa el campo obligatorio "Motivo de la reasignación" (ej. "Avería mecánica del vehículo ABC-123") y pulsa "Confirmar reasignación".
6. El backend procesa la petición `POST /api/v1/despachos/{idDespacho}/reasignacion` de manera transaccional:
   - Valida mediante bloqueo optimista que el despacho continúe en estado `ASIGNADO`.
   - Consulta a F-06 la capacidad disponible del repartidor destino y valida que cubra el peso, volumen y cantidad de paquetes.
   - Valida la presencia del motivo de reasignación.
   - Actualiza el despacho asignándole el nuevo `idRepartidor` y la nueva `idJornada`.
   - Retira el despacho de la ruta original y compacta correlativamente la secuencia de las paradas restantes del repartidor emisor.
   - Posiciona el despacho al final de la secuencia de ruta del nuevo repartidor (posición N+1).
   - Solicita a F-06 la transferencia de la reserva de capacidad (liberación en la furgoneta origen y asignación en la furgoneta destino).
   - Registra el historial de auditoría con la referencia de ambos repartidores, el usuario gestor y el motivo.
7. El backend responde `200 OK` con la confirmación de la reasignación.
8. El frontend cierra el modal, muestra la notificación toast "Despacho [código] reasignado a [nuevo repartidor]" y refresca en pantalla las rutas y barras de ocupación de ambos operadores.

## 4. Reglas y validaciones

- **Exclusividad estricta de estado:** la reasignación solo se permite mientras el despacho permanezca en `ASIGNADO` y físicamente en el centro de despacho. Si el despacho se encuentra en `EN_CAMINO`, `ENTREGADO`, `FALLIDO` o `CANCELADO`, la operación se rechaza con `409 Conflict` ("El despacho ya inició su traslado y no puede reasignarse").
- **Motivo obligatorio:** el campo `motivo` es estrictamente requerido, con una longitud de entre 5 y 250 caracteres. Peticiones sin motivo son rechazadas con `400 Bad Request`.
- **Exclusión del operador actual:** el catálogo destino excluye al repartidor actualmente asignado para evitar reasignaciones redundantes.
- **Validación tridimensional en destino:** el despacho solo puede confirmarse si el repartidor destino cuenta con capacidad suficiente en peso (kg), volumen (m³) y cantidad de paquetes (unidades físicas). Si alguno de los tres límites se sobrepasa, el backend responde `422 Unprocessable Entity` ("Capacidad de carga del repartidor excedida: [recurso]").
- **Estado del repartidor destino:** el nuevo repartidor debe encontrarse en estado operativo `DISPONIBLE` o `EN_RUTA`. Un operador en `SATURADO` o `FUERA_DE_TURNO` provoca un rechazo `409 Conflict`.
- **Posición en la nueva ruta:** el despacho transferido se añade como la última parada de la secuencia del nuevo repartidor.
- **Concurrencia optimista:** si mientras el Gestor reasigna en el panel, el repartidor original confirma la salida marcando "En camino" desde F-03, la operación se cancela de forma atómica y el sistema responde `409 Conflict`.

## 5. Entradas, salidas e integraciones

### Entradas

- Ruta: `POST /api/v1/despachos/{idDespacho}/reasignacion`.
- Payload JSON conforme a `integraciones/api-contract.md`:
  ```json
  {
    "idNuevoRepartidor": "REP-0018",
    "idNuevaJornada": "JOR-20260923-0018",
    "motivo": "Falla mecánica de la furgoneta"
  }
  ```
- Encabezado `Authorization: Bearer <jwt_usuario>`.

### Salidas

- Respuesta HTTP `200 OK`:
  - `idDespacho`: identificador del despacho.
  - `estado`: `ASIGNADO`.
  - `idRepartidorAnterior`: operador de origen.
  - `idNuevoRepartidor`: nuevo operador asignado.
  - `nuevaPosicion`: parada asignada en la nueva ruta.
  - `fechaReasignacion`: marca temporal en UTC.
- Notificación de éxito en el frontend y actualización de rutas en pantalla.
- Errores normalizados: `400 Bad Request`, `403 Forbidden`, `409 Conflict` o `422 Unprocessable Entity`.

### Integraciones

- **Disponibilidad y Capacidad Diaria (F-06):** gestiona la transferencia transaccional de reservas de capacidad entre ambas furgonetas.
- **Web del Repartidor (F-03):** actualiza las rutas de ambos repartidores; en el repartidor emisor el despacho desaparece y en el receptor aparece al final.
- **Trazabilidad (ES-F02-08):** registra la auditoría con el motivo y los dos repartidores involucrados.
- Contrato especificado en `integraciones/api-contract.md` (Sección 9.2).

## 6. Criterios de aceptación

### CA-01. Reasignación exitosa dentro de capacidad con motivo

- **DADO** un despacho en estado `ASIGNADO` y un repartidor destino con capacidad libre suficiente en F-06.
- **CUANDO** el Gestor ingresa el motivo obligatorio y confirma la reasignación.
- **ENTONCES** el sistema cambia el repartidor del despacho, lo ubica al final de la ruta del nuevo operador, lo retira de la ruta anterior, transfiere la reserva de carga en F-06 y responde `200 OK`.

### CA-02. Rechazo por despacho en traslado (`EN_CAMINO`)

- **DADO** un despacho cuyo repartidor ya confirmó la salida iniciando traslado (`EN_CAMINO`).
- **CUANDO** se intenta enviar una solicitud de reasignación.
- **ENTONCES** el backend responde `409 Conflict`, conserva el repartidor original y muestra en pantalla que el despacho ya inició su traslado.

### CA-03. Rechazo por capacidad excedida en repartidor destino

- **DADO** un repartidor destino cuya capacidad remanente de volumen no cubre los metros cúbicos del despacho a reasignar.
- **CUANDO** el Gestor intenta confirmar la reasignación.
- **ENTONCES** el modal muestra la alerta de capacidad excedida, el backend responde `422 Unprocessable Entity` y el despacho permanece con su repartidor actual.

### CA-04. Rechazo por falta de motivo

- **DADO** una solicitud de reasignación donde el campo `motivo` está ausente o tiene menos de 5 caracteres.
- **CUANDO** se intenta enviar la petición.
- **ENTONCES** el sistema responde `400 Bad Request` y no ejecuta la reasignación.

### CA-05. Repartidor destino no habilitado

- **DADO** que el repartidor destino seleccionado cerró su turno o pasó a `SATURADO` de forma concurrente.
- **CUANDO** el Gestor envía la confirmación.
- **ENTONCES** el backend responde `409 Conflict` y no modifica el despacho.

### CA-06. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta ejecutar una reasignación.
- **ENTONCES** el backend responde `403 Forbidden` y no procesa el cambio.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Reasignación de despachos en poder del cliente o en tránsito (`EN_CAMINO`).
- Modificación de la zona de cobertura del despacho.
- Tratamiento de devoluciones a centro (corresponde a F-04).

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-07).
- Contrato de API: `integraciones/api-contract.md` (Sección 9.2).
- Disponibilidad y capacidad de flota: `funcionalidades/F-06-DisponibilidadCapacidadDiaria.md`.
- Diseño de interfaz: `disenio/funcionalidades/f-02.md` (Pantalla 4).
