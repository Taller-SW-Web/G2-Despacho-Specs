# ES-F02-08: Registrar la trazabilidad de las operaciones

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho / Sistema

## 1. Objetivo

Garantizar que toda operación de recepción, simulación, asignación, reordenamiento de ruta, reasignación y cancelación ejecutada sobre los despachos de F-02 deje un registro auditable, inmutable y ordenado cronológicamente que permita reconstruir con precisión qué ocurrió, qué usuario o servicio externo ejecutó la acción, cuándo se procesó en UTC y cuáles fueron los estados y recursos asociados. La trazabilidad se persiste automáticamente como parte de la transacción de negocio y da cumplimiento al requisito transversal de auditoría (RT-02).

## 2. Actor y precondiciones

- La operación de negocio de F-02 (ES-F02-01 a ES-F02-07) superó con éxito todas sus validaciones y será aceptada.
- La identidad del actor ejecutor se obtiene directamente de los claims autenticados del token JWT (usuario humano o token de servicio).
- La marca temporal de registro procede del reloj del servidor central en UTC.
- La persistencia de auditoría forma parte de la misma transacción en base de datos que el cambio operativo.

## 3. Flujo principal

1. Un caso de uso de F-02 (recepción, simulación, asignación, reordenamiento, reasignación o cancelación) valida la solicitud.
2. Antes de confirmar la transacción de persistencia, el sistema prepara la entidad de auditoría conteniendo:
   - Identificador del despacho (`idDespacho`) e identificador del pedido (`idPedido`).
   - Tipo de operación (ej. `RECEPCION_SOLICITUD`, `SIMULACION_CREADA`, `ASIGNACION_REPARTIDOR`, `REORDENAMIENTO_RUTA`, `REASIGNACION_REPARTIDOR`, `CANCELACION_PEDIDO`).
   - Identidad del ejecutor (nombre de usuario o identificador de servicio extraído del token).
   - Marca temporal precisa del servidor en formato UTC.
   - Estado anterior y estado nuevo del despacho.
   - Parámetros contextuales: repartidor asignado, jornada, posición en secuencia, ocupación de carga resultante en F-06, motivo de reasignación u observaciones de entrega.
3. El sistema guarda la modificación de negocio y el registro de auditoría de forma atómica en PostgreSQL.
4. En caso de requerir publicación de eventos hacia Ventas y Postventa (RT-03), el evento se almacena en la tabla outbox dentro de la misma transacción.
5. El registro queda permanentemente disponible para su consulta a través del historial de estados del despacho.

## 4. Reglas y validaciones

- **Unicidad e inmutabilidad:** toda operación aceptada genera exactamente un registro de trazabilidad; dicho registro es estrictamente inmutable y no puede ser alterado ni eliminado por ninguna interfaz o endpoint.
- **Identidad fidedigna:** el usuario o sistema ejecutor se extrae obligatoriamente del claim `sub` o `client_id` del token JWT; no se aceptan identificadores de autoría provistos en campos libres del payload.
- **Operaciones rechazadas:** si una operación resulta en un error de validación o conflicto (`400`, `403`, `409`, `422`), la transacción se cancela y no se persiste ningún registro de auditoría de negocio aceptado.
- **Idempotencia:** las peticiones repetidas que devuelvan respuestas idempotentes no generan registros duplicados de trazabilidad.
- **Detalle de asignación:** en una asignación se registra el repartidor, la jornada, la posición otorgada en la ruta y las instrucciones u observaciones.
- **Detalle de reasignación:** en una reasignación se registra tanto el repartidor anterior como el nuevo, la jornada y el motivo obligatorio ingresado.
- **Detalle de cancelación:** se registra el motivo de anulación informado por Ventas y Postventa y el estado previo en el que se encontraba el paquete.
- **Marcas temporales:** todas las marcas se almacenan estrictamente en zona horaria UTC (`Instant`).

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador del despacho (`idDespacho`).
- Tipo de operación ejecutada.
- Identidad del ejecutor autenticado.
- Estado inicial y estado resultante.
- Datos complementarios: `idRepartidor`, `idJornada`, `posicionSecuencia`, `motivo`, `observacion`, `ocupacionResultante`.
- Marca temporal del sistema.

### Salidas

- Registro de auditoría persistido en la tabla de historial de estados.
- Evento correspondiente en la tabla outbox (cuando aplique según RT-03).
- Historial consultable a través del endpoint `GET /api/v1/despachos/{idDespacho}`.

### Integraciones

- Las especificaciones atómicas ES-F02-01, ES-F02-02, ES-F02-04, ES-F02-05, ES-F02-06 y ES-F02-07 generan los eventos de trazabilidad.
- El componente transversal de máquina de estados e historial (RT-01 y RT-02) administra el modelo de datos de trazabilidad.
- `integraciones/api-contract.md` (Sección 9.2) define el endpoint de consulta del detalle e historial.

## 6. Criterios de aceptación

### CA-01. Registro automático tras asignación a repartidor

- **DADO** que una asignación a un repartidor es aceptada por el backend.
- **CUANDO** finaliza la transacción.
- **ENTONCES** el sistema persiste un registro de auditoría con el `idDespacho`, usuario gestor, repartidor, jornada, secuencia, observaciones, estados `PENDIENTE_ASIGNACION` -> `ASIGNADO` y marca temporal en UTC.

### CA-02. Registro automático tras reasignación con motivo

- **DADO** una reasignación válida entre repartidores.
- **CUANDO** se confirma la operación.
- **ENTONCES** se genera el registro de auditoría incluyendo el repartidor anterior, el nuevo repartidor, el motivo obligatorio y la posición final en la nueva ruta, manteniendo el estado `ASIGNADO`.

### CA-03. Registro automático tras cancelación de pedido

- **DADO** una cancelación de pedido procesada con éxito sobre un despacho asignado.
- **CUANDO** se confirma la transacción.
- **ENTONCES** se registra la transición de `ASIGNADO` a `CANCELADO`, la liberación de carga en la furgoneta y el motivo de anulación provisto por Ventas y Postventa.

### CA-04. Inmutabilidad de los registros

- **DADO** un registro de trazabilidad persistido en el sistema.
- **CUANDO** se ejecutan operaciones de consulta o actualización en los módulos de despacho.
- **ENTONCES** el registro permanece inalterable en sus campos originales sin admitir modificaciones ni borrados.

### CA-05. Petición idempotente no duplica auditoría

- **DADO** una solicitud repetida de recepción o cancelación que responde de forma idempotente con `200 OK`.
- **CUANDO** se procesa la llamada.
- **ENTONCES** el sistema devuelve el despacho sin generar una segunda entrada idéntica en el historial de trazabilidad.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Registro de auditoría de operaciones de otros módulos (Ventas, Seguridad).
- Interfaz gráfica independiente para auditoría (el historial se consulta dentro de cada despacho).

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-04, CA-10).
- Requisito transversal de trazabilidad: `overview.md` (Sección 6, RT-02).
- Contrato de API: `integraciones/api-contract.md` (Sección 9.2).
