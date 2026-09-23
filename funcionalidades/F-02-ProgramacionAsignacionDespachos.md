# Especificación F-02: Programación y Asignación de Despachos

**Responsable:** Tarqui
**Estado:** En especificación
**Actor principal:** Gestor de Despacho
**Lineamientos del curso:** Generación de solicitud de despacho a partir de un pedido; Asignación de despacho a operador/repartidor

## 1. Contexto

Todos los pedidos de la tienda se preparan en un único centro de despacho. Cuando un pedido ya fue pagado y su paquete está sellado en ese centro, el módulo de Ventas y Postventa, dueño de la entidad pedido, solicita a Despacho su entrega a domicilio. A partir de esa solicitud nace el despacho, entidad cuyo dueño es este módulo, en estado `PENDIENTE_ASIGNACION` ("En centro de despacho").

El Gestor de Despacho necesita un panel donde ver la cola de despachos pendientes y asignarlos a los repartidores en turno, sin sobrepasar la capacidad de sus furgonetas. La asignación define además la jornada y el orden en que el repartidor atenderá cada despacho, información que consume la web del repartidor (F-03).

## 2. Propósito

Registrar las solicitudes de despacho recibidas desde Ventas y Postventa, mantener la cola de pendientes, asignar cada despacho a un repartidor habilitado para la jornada en curso respetando su capacidad, definir la secuencia de ruta y atender la cancelación de despachos cuando el pedido es anulado.

## 3. Alcance

Esta funcionalidad incluye:

- Recepción de solicitudes de despacho desde Ventas y Postventa, con resolución de zona mediante F-01 y control de duplicados por pedido.
- Cola paginada y filtrable de despachos en `PENDIENTE_ASIGNACION`, incluidos los reprogramados por F-04.
- Asignación de un despacho a un repartidor para la jornada en curso, validando disponibilidad y capacidad con la información de F-05.
- Secuencia de ruta: posición automática al asignar y reordenamiento por el Gestor.
- Reasignación de un despacho `ASIGNADO` a otro repartidor.
- Cancelación de despachos por anulación del pedido en Ventas y Postventa.
- Auditoría de recepciones, asignaciones, reasignaciones y cancelaciones.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- Las operaciones del panel requieren un token JWT con rol `GESTOR_DESPACHO`.
- La recepción y la cancelación desde Ventas y Postventa requieren un token de servicio de `modulo-ventas` con `despachos:crear` o `despachos:cancelar`, respectivamente.
- Una solicitud de despacho corresponde a un pedido pagado ya preparado y sellado, e incluye: identificador de pedido, destinatario, destino, peso, volumen, cantidad de paquetes físicos y fecha comprometida. Las coordenadas son opcionales y `cantidadPaquetes` normalmente vale `1`.
- Al crear un despacho nuevo, el destino debe estar cubierto por una zona activa de F-01. Los despachos existentes conservan la zona registrada y pueden continuar su ciclo o ser reprogramados aunque posteriormente esa zona sea desactivada.
- Solo se asignan despachos en `PENDIENTE_ASIGNACION` cuya fecha de entrega programada sea igual o anterior a la fecha actual.
- El repartidor debe tener una asignación diaria activa en F-05 y un estado operativo `DISPONIBLE` o `EN_RUTA`.
- El peso, el volumen y la cantidad de paquetes del despacho no deben superar la capacidad remanente del repartidor.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Emitir el JWT del Gestor y el token de servicio de Ventas y Postventa. |
| Ventas y Postventa | Enviar solicitudes de despacho y solicitudes de cancelación por anulación del pedido. |
| Zonas y Cotizador (F-01) | Resolver la zona del destino y rechazar destinos sin cobertura. |
| Monitoreo de Flota (F-05) | Calcular y proveer los repartidores disponibles con su capacidad remanente en kg, m³ y paquetes. F-02 conserva la responsabilidad de ejecutar la asignación del despacho. |
| Web del Repartidor (F-03) | Recibir los despachos `ASIGNADO` con su jornada y secuencia. |
| Entregas Fallidas (F-04) | Devolver a la cola los despachos reprogramados, con su nueva fecha programada. |
| Requisitos transversales (overview, sección 6) | Validar cada transición en la máquina de estados común, registrar el historial y publicar el evento hacia Ventas y Postventa. |

### 4.3. Resultados

- Una solicitud válida crea un despacho en `PENDIENTE_ASIGNACION` con código operativo interno único, zona, fecha programada igual a la fecha comprometida y contador de intentos en cero.
- Una solicitud repetida para el mismo pedido no crea un segundo despacho.
- Una asignación válida cambia el estado a `ASIGNADO`, registra repartidor, jornada y secuencia, y se refleja en la ocupación calculada por F-05.
- Una cancelación válida cambia el estado a `CANCELADO` y libera la capacidad del repartidor si el despacho estaba asignado.
- Toda operación queda auditada con fecha, usuario o sistema origen, despacho y observaciones.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Recepción y creación de solicitudes de despacho

El sistema DEBE registrar las solicitudes de despacho recibidas desde Ventas y Postventa.

#### CA-01. Recepción exitosa desde Ventas y Postventa

- **DADO** que Ventas y Postventa envía una solicitud con identificador de pedido, destinatario, dirección, distrito, peso, volumen, cantidad de paquetes y fecha comprometida válidos, y el destino está cubierto por una zona activa.
- **CUANDO** la solicitud se procesa con un token de servicio válido.
- **ENTONCES** el sistema crea el despacho en `PENDIENTE_ASIGNACION`, genera un código operativo interno y responde `201 Created` con ambos identificadores; los canales consultan el seguimiento por `idPedido`.

#### CA-02. Rechazo de solicitud con datos incompletos o inconsistentes

- **DADO** una solicitud sin dirección o con peso o volumen menor o igual a cero.
- **CUANDO** es evaluada.
- **ENTONCES** el sistema responde `400 Bad Request`, detalla los campos inválidos y no persiste registros parciales.

### RF-02. Consultar la cola de despachos pendientes

El sistema DEBE permitir al Gestor consultar y filtrar de forma paginada los despachos que esperan asignación.

#### CA-03. Listado con despachos pendientes

- **DADO** que existen despachos en `PENDIENTE_ASIGNACION`.
- **CUANDO** el Gestor abre la vista de Programación y Asignación.
- **ENTONCES** el sistema muestra código interno, pedido, zona, dirección, peso, volumen, cantidad de paquetes, fecha programada, número de intento y tiempo en espera, ordenados por fecha programada.

#### CA-04. Listado sin despachos pendientes

- **DADO** que no existen despachos pendientes.
- **CUANDO** el Gestor consulta la vista.
- **ENTONCES** el sistema muestra el estado vacío "No hay despachos pendientes de asignación".

#### CA-05. Acceso sin permisos requeridos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta acceder a la cola o a la asignación.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone información operativa.

### RF-03. Asignar despacho a un repartidor

El sistema DEBE asignar un despacho pendiente a un repartidor habilitado para la jornada en curso, sin exceder su capacidad.

#### CA-06. Asignación exitosa dentro de la capacidad disponible

- **DADO** un despacho en `PENDIENTE_ASIGNACION` programado para hoy y un repartidor `DISPONIBLE` cuya capacidad remanente cubre su peso, volumen y cantidad de paquetes.
- **CUANDO** el Gestor confirma la asignación.
- **ENTONCES** el sistema cambia el estado a `ASIGNADO`, registra el repartidor y la jornada actual, asigna la siguiente posición de la secuencia de ruta y la ocupación del repartidor en F-05 refleja el nuevo despacho.

#### CA-07. Rechazo por capacidad excedida

- **DADO** un despacho cuyo peso, volumen o cantidad de paquetes supera la capacidad remanente del repartidor.
- **CUANDO** el Gestor intenta confirmar la asignación.
- **ENTONCES** el sistema responde `422 Unprocessable Entity`, indica el límite excedido ("Capacidad de carga del repartidor excedida") y mantiene el despacho en `PENDIENTE_ASIGNACION`.

#### CA-08. Rechazo por repartidor no habilitado

- **DADO** un repartidor en estado operativo `FUERA_DE_TURNO` o `SATURADO`, o con registro `INACTIVO`.
- **CUANDO** se intenta asignarle un despacho.
- **ENTONCES** el sistema responde `409 Conflict` y mantiene el despacho en la cola.

#### CA-09. Despacho en estado incompatible o ya asignado

- **DADO** un despacho que ya fue asignado o que no está en `PENDIENTE_ASIGNACION`.
- **CUANDO** se ejecuta una asignación concurrente o desactualizada.
- **ENTONCES** el sistema responde `409 Conflict` e informa que el despacho ya fue procesado.

### RF-04. Mantener trazabilidad y auditoría

El sistema DEBE registrar un historial auditable de cada operación sobre el despacho.

#### CA-10. Registro de auditoría de la asignación

- **DADO** que una asignación es aceptada.
- **CUANDO** finaliza la transacción.
- **ENTONCES** se registran despacho, repartidor, usuario gestor, jornada, secuencia, marca temporal en UTC y la ocupación resultante del repartidor.

### RF-05. Integridad de la recepción

El sistema DEBE impedir despachos duplicados y despachos sin cobertura.

#### CA-11. Solicitud repetida para el mismo pedido

- **DADO** que ya existe un despacho para el pedido `PED-2026-00891`.
- **CUANDO** Ventas y Postventa vuelve a enviar una solicitud con ese identificador de pedido.
- **ENTONCES** el sistema no crea un nuevo despacho y responde `200 OK` con el despacho existente, su código interno y su estado actual.

#### CA-12. Destino sin cobertura

- **DADO** una solicitud cuyo destino no pertenece a ninguna zona activa de F-01.
- **CUANDO** es evaluada.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con el código `DESP_ERROR_SIN_COBERTURA` y no persiste el despacho.

### RF-06. Programación de la jornada y secuencia de ruta

El sistema DEBE definir para cada despacho asignado la jornada y su posición en la ruta del repartidor.

#### CA-13. Despacho programado para una fecha futura

- **DADO** un despacho reprogramado por F-04 para una fecha posterior a hoy.
- **CUANDO** el Gestor consulta la cola o intenta asignarlo.
- **ENTONCES** la cola lo muestra identificado como "Programado para [fecha]" y el backend rechaza su asignación con `409 Conflict` hasta que llegue esa fecha.

#### CA-14. Reordenamiento de la secuencia de ruta

- **DADO** un repartidor con varios despachos en `ASIGNADO` en la jornada actual.
- **CUANDO** el Gestor cambia el orden de esos despachos y confirma.
- **ENTONCES** el sistema actualiza la secuencia sin posiciones repetidas ni vacías, y F-03 muestra la ruta con el nuevo orden en la siguiente consulta. Solo cambian de posición los despachos en `ASIGNADO`.

### RF-07. Reasignación de despachos

El sistema DEBE permitir mover a otro repartidor un despacho que aún no inició su traslado.

#### CA-15. Reasignación exitosa

- **DADO** un despacho en `ASIGNADO` y otro repartidor habilitado con capacidad suficiente.
- **CUANDO** el Gestor confirma la reasignación indicando un motivo.
- **ENTONCES** el sistema cambia el repartidor del despacho, lo ubica al final de la secuencia del nuevo repartidor, lo retira de la ruta del anterior y registra la auditoría con ambos repartidores.

#### CA-16. Reasignación de un despacho en traslado

- **DADO** un despacho en cualquier estado distinto de `ASIGNADO`.
- **CUANDO** se intenta reasignarlo.
- **ENTONCES** el sistema responde `409 Conflict` y conserva el repartidor original.

### RF-08. Cancelación por anulación del pedido

El sistema DEBE atender las solicitudes de cancelación que Ventas y Postventa envía cuando anula un pedido.

#### CA-17. Cancelación antes del traslado

- **DADO** un despacho en `PENDIENTE_ASIGNACION` o `ASIGNADO`.
- **CUANDO** Ventas y Postventa solicita su cancelación indicando el pedido anulado.
- **ENTONCES** el sistema cambia el estado a `CANCELADO`, lo retira de la cola o de la ruta del repartidor, registra la auditoría y responde con el estado resultante. Un despacho `ASIGNADO` todavía permanece físicamente en el centro de despacho; si el repartidor ya lo recogió y salió, debe encontrarse en `EN_CAMINO` y se aplica el rechazo definido en CA-18.

#### CA-18. Cancelación de un despacho en traslado o cerrado

- **DADO** un despacho en `EN_CAMINO`, `ENTREGADO`, `DEVUELTO_A_ORIGEN` o `CANCELADO`.
- **CUANDO** Ventas y Postventa solicita su cancelación.
- **ENTONCES** el sistema responde `409 Conflict` indicando el estado actual y no modifica el despacho. Ventas y Postventa recibirá el resultado final mediante los eventos de estado.

#### CA-19. Cancelación de un despacho fallido

- **DADO** un despacho en `FALLIDO`.
- **CUANDO** Ventas y Postventa solicita su cancelación.
- **ENTONCES** el sistema registra la anulación del pedido sobre el despacho sin cambiar su estado, responde `202 Accepted` y, cuando el paquete regrese al centro de despacho, F-04 solo permite cerrarlo como `DEVUELTO_A_ORIGEN`.

## 6. Frontend

| Elemento | Responsabilidad |
|---|---|
| Panel de Programación | Cola de `PENDIENTE_ASIGNACION` con filtros por fecha, zona e intento, y paginación. |
| Modal de Asignación | Catálogo de repartidores disponibles, priorizando los de la zona del despacho, con furgoneta y barras de ocupación en kg, m³ y paquetes. |
| Ruta por repartidor | Despachos de cada repartidor en la jornada con su estado actual y hora del último cambio (seguimiento en ruta, overview RT-04), con reordenamiento y reasignación. |
| Indicadores de capacidad | Alerta previa cuando un despacho excede la capacidad del repartidor seleccionado. |
| Retroalimentación | Éxito, sobrecarga, conflictos de concurrencia, despachos programados a futuro y errores de red. |

La interfaz debe deshabilitar acciones inválidas, pero todas las reglas se validan en el backend.

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Receptor de solicitudes | Validar la solicitud, controlar duplicados por pedido, resolver la zona con F-01 y crear el despacho. |
| Consulta de cola | Recuperar despachos pendientes con filtros, orden por fecha programada y paginación. |
| Caso de uso de asignación | Validar estado, fecha programada, habilitación y capacidad remanente de forma transaccional. |
| Gestión de secuencia | Asignar la siguiente posición y aplicar reordenamientos sin huecos ni duplicados. |
| Caso de uso de reasignación | Mover un despacho `ASIGNADO` entre repartidores validando capacidad. |
| Caso de uso de cancelación | Aplicar las reglas de cancelación según el estado del despacho. |
| Integración con F-05 | Consultar disponibilidad y capacidad remanente antes de confirmar. |
| Persistencia y auditoría | Guardar despachos y auditoría en PostgreSQL; las transiciones se registran mediante la máquina de estados común. |

Las rutas, cuerpos, respuestas y códigos se centralizan en `integraciones/api-contract.md`.

## 8. Requisitos no funcionales

- **Seguridad:** el panel requiere JWT con rol `GESTOR_DESPACHO`; la recepción y la cancelación requieren los scopes de servicio `despachos:crear` y `despachos:cancelar`.
- **Aislamiento:** el módulo no accede a bases de datos de otros módulos.
- **Concurrencia:** la asignación, la reasignación y la cancelación usan bloqueo optimista para impedir operaciones simultáneas sobre el mismo despacho.
- **Idempotencia:** la recepción es idempotente por identificador de pedido.
- **Rendimiento:** la cola responde en menos de 250 ms para páginas de hasta 100 registros; la recepción responde en menos de 500 ms.
- **Trazabilidad:** cada operación registra marca temporal en UTC y usuario o sistema origen.
- **Usabilidad:** el panel es adaptable a escritorio y tablet.

## 9. Fuera de alcance

- **Optimización automática de rutas:** el orden lo define el Gestor; la navegación usa herramientas externas.
- **Ejecución de la entrega:** corresponde a F-03.
- **Resolución de entregas fallidas:** corresponde a F-04.
- **Administración de repartidores, furgonetas y jornadas:** corresponde a F-05.
- **Anulación del pedido:** la decide Ventas y Postventa; F-02 solo aplica su efecto sobre el despacho.
- **Preparación y sellado del paquete:** ocurren en el centro de despacho antes de la solicitud; el módulo recibe el paquete listo para enviar.
- **Cobros y facturación:** corresponden a Ventas y Postventa.

Las posibles ampliaciones de esta funcionalidad están centralizadas en [Pendientes](./pendiente.md), sección F-02. No forman parte de los criterios de completitud actuales.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 y CA-02 | Enviar solicitudes válidas e inválidas. | Integración y unitaria | `201` con zona asignada y `400` para datos inválidos. |
| CA-03 y CA-04 | Consultar la cola con y sin pendientes. | Integración y frontend | Tabla paginada ordenada y estado vacío. |
| CA-05 | Invocar la cola y la asignación sin credenciales o con rol incorrecto. | Integración de seguridad | `403 Forbidden`. |
| CA-06 a CA-09 | Asignar con capacidad suficiente, excedida por cada límite, repartidor no habilitado y conflicto concurrente. | Unitaria e integración | `ASIGNADO` con secuencia; `422` y `409` según corresponda. |
| CA-10 | Consultar la auditoría tras una asignación. | Integración con persistencia | Registro completo con jornada, secuencia y ocupación resultante. |
| CA-11 y CA-12 | Repetir una solicitud y enviar un destino sin cobertura. | Integración | Un único despacho por pedido y `422` sin persistencia. |
| CA-13 y CA-14 | Asignar un despacho programado a futuro y reordenar una ruta. | Unitaria e integración | `409` para fecha futura; secuencia continua y reflejada en F-03. |
| CA-15 y CA-16 | Reasignar un despacho `ASIGNADO` y otro `EN_CAMINO`. | Integración | Cambio de repartidor en el primer caso y `409` en el segundo. |
| CA-17 a CA-19 | Cancelar despachos en cada estado. | Unitaria e integración | `CANCELADO`, `409` o anulación registrada según el estado. |

Además, se ejecutarán tres recorridos funcionales completos:

1. Recepción → resolución de zona → cola en `PENDIENTE_ASIGNACION`.
2. Despacho en cola → asignación → `ASIGNADO` con secuencia → visible en la ruta de F-03.
3. Despacho `ASIGNADO` → anulación del pedido → `CANCELADO` y retirado de la ruta de F-03.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Los criterios `CA-01` a `CA-19` están implementados y cuentan con pruebas automatizadas exitosas.
- Los tres recorridos funcionales han sido verificados de extremo a extremo.
- No existe más de un despacho por pedido.
- Ninguna asignación supera la capacidad en kg, m³ o paquetes informada por F-05.
- Cada despacho asignado tiene jornada y secuencia consumibles por F-03.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.
