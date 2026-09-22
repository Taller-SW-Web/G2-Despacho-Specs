# Especificación F-04: Entregas Fallidas y Reprogramaciones

**Responsable:** Gerardo
**Estado:** En especificación
**Actor principal:** Gestor de Despacho
**Lineamiento del curso:** Gestión de entregas fallidas/reprogramaciones

## 1. Contexto

Todos los despachos salen del centro de despacho de la tienda con el paquete sellado. Cuando una entrega no se concreta, ya sea por una incidencia (cliente ausente, dirección no localizada, rechazo, etc.) o porque la jornada terminó sin intentarla, la web del repartidor (F-03) deja el despacho en `FALLIDO` y el repartidor regresa el paquete al centro de despacho.

En el centro, el Gestor de Despacho confirma que el paquete volvió y decide qué hacer: programar un nuevo intento o cerrar el despacho como `DEVUELTO_A_ORIGEN`, con lo cual el paquete queda en el centro a disposición de Ventas y Postventa, dueño del pedido, para continuar su tratamiento (reembolso, cambio o nuevo envío).

## 2. Propósito

Permitir que el Gestor de Despacho controle el retorno de los paquetes no entregados al centro de despacho y decida, bajo una política de intentos, si reprogramar el despacho o cerrarlo como devuelto a origen, dejando cada decisión auditada y comunicada a Ventas y Postventa.

## 3. Alcance

Esta funcionalidad incluye:

- Panel de despachos en `FALLIDO`, distinguiendo los paquetes pendientes de retorno de los ya recibidos en el centro.
- Confirmación de la recepción del paquete en el centro de despacho.
- Detalle del despacho con historial de estados e intentos, y visualización autorizada de la evidencia mediante el mecanismo que se defina en F-03.
- Política de intentos configurable, con valor inicial de dos.
- Reprogramación con nueva fecha y retorno a la cola de F-02.
- Tratamiento diferenciado de los despachos `NO_INTENTADO`, que no consumen intentos.
- Cierre del despacho como `DEVUELTO_A_ORIGEN`.
- Restricción al cierre como devuelto cuando el pedido fue anulado.
- Auditoría de cada recepción y decisión.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario está autenticado con rol `GESTOR_DESPACHO`.
- El despacho existe y está en `FALLIDO`.
- El registro del fallo contiene motivo, fecha, repartidor y número de intento.
- Para reprogramar o cerrar el despacho, su paquete debe haberse recibido en el centro de despacho.
- La política de intentos está configurada; el valor inicial es dos.
- La nueva fecha de entrega es posterior a la fecha actual.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Proporcionar la identidad y el rol `GESTOR_DESPACHO`. |
| Web del Repartidor (F-03) | Registrar el fallo, su motivo, la evidencia y el contador; proveer el catálogo de motivos y el acceso autorizado a la evidencia. |
| Programación y Asignación (F-02) | Recibir los despachos reprogramados en la cola y registrar la anulación de pedidos sobre despachos fallidos. |
| Monitoreo de Flota (F-05) | Dejar de contar el paquete en la ocupación del repartidor cuando se confirma su recepción. |
| Requisitos transversales (overview, sección 6) | Validar las transiciones, registrar el historial y publicar los eventos hacia Ventas y Postventa. |
| Ventas y Postventa | Recibir el resultado de la reprogramación o del cierre como devuelto a origen. |

### 4.3. Resultados

- Una recepción confirmada registra fecha, usuario y observaciones del estado del paquete, sin cambiar el estado del despacho.
- Una reprogramación válida cambia el estado a `PENDIENTE_ASIGNACION`, registra la nueva fecha programada y conserva el contador de intentos.
- Un cierre cambia el estado a `DEVUELTO_A_ORIGEN` y genera el evento correspondiente hacia Ventas y Postventa.
- Toda operación registra usuario, fecha, estado anterior, estado nuevo y observaciones.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Consultar entregas fallidas

El sistema DEBE permitir al Gestor consultar los despachos en `FALLIDO`.

#### CA-01. Listado con incidencias

- **DADO** que existen despachos en `FALLIDO`.
- **CUANDO** el Gestor abre la pantalla de Entregas Fallidas.
- **ENTONCES** el sistema muestra código de rastreo, fecha del incidente, motivo, número de intento sobre el máximo, repartidor, indicador de recepción ("Pendiente de retorno" o "Recibido en centro"), indicador de evidencia e indicador de pedido anulado, con paginación y filtros por motivo, fecha y recepción.

#### CA-02. Listado sin incidencias

- **DADO** que no existen despachos en `FALLIDO`.
- **CUANDO** el Gestor abre la pantalla.
- **ENTONCES** se muestra un estado vacío sin información de otros estados.

#### CA-03. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** consulta las incidencias.
- **ENTONCES** el backend responde `403 Forbidden`.

### RF-02. Consultar el detalle de una incidencia

El sistema DEBE mostrar la información necesaria para decidir.

#### CA-04. Detalle exitoso

- **DADO** un despacho en `FALLIDO`.
- **CUANDO** el Gestor abre su detalle.
- **ENTONCES** ve motivo, comentario del repartidor, fecha, repartidor, intento actual, datos de recepción, historial de estados y la fotografía mediante el mecanismo de acceso autorizado definido por F-03.

#### CA-05. Despacho inexistente

- **DADO** un código que no corresponde a un despacho.
- **CUANDO** se solicita el detalle.
- **ENTONCES** el backend responde `404 Not Found` sin datos parciales.

### RF-03. Reprogramar un despacho

El sistema DEBE permitir fijar una nueva fecha mientras no se haya alcanzado el máximo de intentos.

#### CA-06. Reprogramación válida

- **DADO** un despacho fallido, recibido en el centro, con un intento y máximo configurado de dos.
- **CUANDO** el Gestor selecciona una fecha futura y confirma.
- **ENTONCES** el estado cambia a `PENDIENTE_ASIGNACION` ("En centro de despacho"), se guarda la nueva fecha programada, el contador se mantiene en uno y se registra la auditoría.

#### CA-07. Fecha inválida

- **DADO** un despacho reprogramable.
- **CUANDO** el Gestor selecciona la fecha actual o una pasada.
- **ENTONCES** el sistema responde `400 Bad Request`, explica la validación y el despacho sigue en `FALLIDO`.

#### CA-08. Límite de intentos alcanzado

- **DADO** un despacho cuyo contador es igual al máximo configurado.
- **CUANDO** el Gestor abre el detalle o intenta reprogramar.
- **ENTONCES** el frontend deshabilita la reprogramación, el backend responde `422 Unprocessable Entity` ante cualquier intento y solo se ofrece el cierre como `DEVUELTO_A_ORIGEN`.

#### CA-09. Estado desactualizado

- **DADO** un despacho que ya no está en `FALLIDO`.
- **CUANDO** se intenta reprogramar con información desactualizada.
- **ENTONCES** el backend responde `409 Conflict` y conserva el estado vigente.

### RF-04. Cerrar el despacho como devuelto a origen

El sistema DEBE permitir cerrar un despacho fallido cuyo paquete permanecerá en el centro de despacho y comunicar el resultado a Ventas y Postventa.

#### CA-10. Cierre exitoso

- **DADO** un despacho en `FALLIDO` recibido en el centro.
- **CUANDO** el Gestor confirma el cierre indicando un motivo.
- **ENTONCES** el estado cambia a `DEVUELTO_A_ORIGEN` ("De vuelta en el centro de despacho"), se registra la auditoría y se publica el evento `DESPACHO_DEVUELTO_A_ORIGEN` hacia Ventas y Postventa.

#### CA-11. Operación repetida

- **DADO** un despacho ya cerrado como `DEVUELTO_A_ORIGEN`.
- **CUANDO** se repite la operación.
- **ENTONCES** no se duplican el cambio de estado, la auditoría ni el evento, y se informa que la decisión ya fue procesada.

#### CA-12. Falla de la comunicación externa

- **DADO** un despacho cerrado como `DEVUELTO_A_ORIGEN`.
- **CUANDO** Ventas y Postventa no está disponible.
- **ENTONCES** el estado local se conserva y el evento queda registrado como pendiente de reintento (overview, RT-03).

### RF-05. Mantener trazabilidad

El sistema DEBE conservar el historial de recepciones y decisiones.

#### CA-13. Registro de auditoría

- **DADO** una recepción, reprogramación o cierre aceptado.
- **CUANDO** se persiste.
- **ENTONCES** se registran usuario, fecha, estado anterior, estado nuevo y datos de la operación (observación de recepción, nueva fecha o motivo de cierre).

### RF-06. Casos especiales de resolución

El sistema DEBE tratar de forma diferenciada los despachos no intentados y los pedidos anulados.

#### CA-14. Reprogramación de un despacho no intentado

- **DADO** un despacho en `FALLIDO` con motivo `NO_INTENTADO`, recibido en el centro.
- **CUANDO** el Gestor lo reprograma con una fecha futura.
- **ENTONCES** el despacho vuelve a `PENDIENTE_ASIGNACION` sin cambiar el contador de intentos, y el listado lo identifica como "No intentado" para distinguirlo de los fallos con intento real.

#### CA-15. Despacho fallido con pedido anulado

- **DADO** un despacho en `FALLIDO` sobre el cual F-02 registró la anulación del pedido.
- **CUANDO** el Gestor abre su detalle o intenta reprogramarlo.
- **ENTONCES** la reprogramación está deshabilitada, el backend la rechaza con `409 Conflict` y solo se permite el cierre como `DEVUELTO_A_ORIGEN`.

### RF-07. Recepción del paquete en el centro de despacho

El sistema DEBE registrar el retorno físico del paquete antes de cualquier decisión.

#### CA-16. Confirmación de recepción

- **DADO** un despacho en `FALLIDO` marcado como "Pendiente de retorno".
- **CUANDO** el Gestor confirma que el paquete llegó al centro de despacho, indicando si el sello está intacto.
- **ENTONCES** el despacho se marca como "Recibido en centro" sin cambiar de estado, se registra la auditoría y el paquete deja de contar en la ocupación del repartidor en F-05.

#### CA-17. Decisión sin recepción confirmada

- **DADO** un despacho en `FALLIDO` cuyo paquete aún no se recibió en el centro.
- **CUANDO** el Gestor intenta reprogramarlo o cerrarlo.
- **ENTONCES** el backend responde `409 Conflict` indicando que primero debe confirmarse la recepción.

#### CA-18. Paquete no retornado al cierre de la jornada

- **DADO** un despacho en `FALLIDO` cuyo repartidor ya cerró su jornada.
- **CUANDO** el paquete sigue sin recepción confirmada.
- **ENTONCES** el listado lo resalta como "Retorno atrasado" junto al nombre del repartidor responsable.

## 6. Frontend

| Elemento | Responsabilidad |
|---|---|
| Pantalla de Entregas Fallidas | Filtros, listado paginado, indicadores de recepción, "No intentado", "Pedido anulado" y "Retorno atrasado", y estados de carga, vacío y error. |
| Confirmación de recepción | Registro del retorno del paquete con estado del sello y observaciones. |
| Detalle de la incidencia | Motivo, comentario, intento actual, recepción, historial y fotografía. |
| Formulario de reprogramación | Fecha futura con validación; disponible solo con recepción confirmada. |
| Confirmación de cierre | Motivo obligatorio y advertencia de que el despacho no tendrá más intentos. |
| Retroalimentación | Éxito, validaciones, conflictos y errores de comunicación. |

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Consulta de incidencias | Recuperar despachos `FALLIDO` con filtros y paginación. |
| Registro de recepción | Marcar el paquete como recibido en el centro y registrar la auditoría. |
| Consulta de detalle | Obtener historial, motivo, intentos, recepción y solicitar a F-03 el acceso autorizado a la evidencia. |
| Caso de uso de reprogramación | Validar estado, recepción, fecha, límite de intentos y anulación antes de solicitar la transición. |
| Caso de uso de cierre | Validar recepción y solicitar la transición a `DEVUELTO_A_ORIGEN`. |
| Política de intentos | Leer y aplicar el máximo configurable. |
| Persistencia y auditoría | Guardar recepciones y decisiones de manera consistente. |

Esta sección no prescribe clases ni paquetes. Las rutas, cuerpos y códigos se definen en `specs/api-contract.md`.

## 8. Requisitos no funcionales

- **Seguridad:** todas las operaciones requieren rol `GESTOR_DESPACHO`.
- **Aislamiento:** no se accede a bases de datos de otros módulos.
- **Consistencia:** el cambio de estado, la auditoría y el registro del evento pendiente se persisten en la misma transacción.
- **Idempotencia:** la recepción y el cierre repetidos no producen efectos duplicados.
- **Trazabilidad:** las recepciones, las decisiones y el estado de su comunicación son consultables.
- **Usabilidad y escalabilidad:** pantalla responsive y listados paginados.

## 9. Fuera de alcance

- **Reembolsos, cambios, devoluciones comerciales y reclamos:** pertenecen a Ventas y Postventa.
- **Almacenamiento, reingreso a inventario y reintegro de stock:** pertenecen a la operación del centro, Ventas y Postventa y Productos y Ofertas; Despacho solo registra que el paquete volvió.
- **Registro del fallo en campo:** corresponde a F-03.
- **Asignación del nuevo intento a un repartidor:** corresponde a F-02.
- **Transporte y reintentos de los eventos:** corresponden al requisito transversal RT-03 del overview.

La posible logística inversa posterior a una entrega está centralizada en [Pendientes](../pendiente.md), sección F-04. No forma parte de esta funcionalidad mientras no exista un acuerdo con Ventas y Postventa.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 y CA-02 | Consultar con y sin incidencias. | Integración y frontend | Listado con indicadores y estado vacío. |
| CA-03 | Consultar sin permisos. | Integración de seguridad | `403`. |
| CA-04 y CA-05 | Consultar un detalle existente e inexistente. | Integración y frontend | Datos con evidencia visible y `404`. |
| CA-06 a CA-09 | Probar fechas, límite y estado desactualizado. | Unitaria, integración y frontend | Reprogramación válida; `400`, `422` y `409`. |
| CA-10 a CA-12 | Cerrar, repetir y simular indisponibilidad de Ventas y Postventa. | Unitaria e integración | Un único cambio y un único evento; evento pendiente si falla. |
| CA-13 | Revisar la auditoría tras cada operación. | Integración con persistencia | Registro completo. |
| CA-14 y CA-15 | Reprogramar un `NO_INTENTADO` y un despacho con pedido anulado. | Unitaria e integración | Contador sin cambio; `409` con pedido anulado. |
| CA-16 a CA-18 | Confirmar recepción, decidir sin recepción y cerrar la jornada sin retorno. | Unitaria e integración | Ocupación liberada en F-05, `409` y alerta de retorno atrasado. |

Además, se ejecutarán tres recorridos funcionales completos:

1. `FALLIDO` → recepción en centro → reprogramación → `PENDIENTE_ASIGNACION` → visible en la cola de F-02 en la fecha programada.
2. `FALLIDO` → recepción en centro → cierre → `DEVUELTO_A_ORIGEN` → evento registrado hacia Ventas y Postventa.
3. Segundo fallo con intento real → recepción → límite alcanzado → solo cierre disponible.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Los criterios `CA-01` a `CA-18` están implementados y cuentan con pruebas exitosas.
- Los tres recorridos funcionales han sido verificados.
- Ninguna decisión se toma sin recepción confirmada del paquete.
- La política de intentos se aplica y los `NO_INTENTADO` no consumen intentos.
- Ningún cierre deja de comunicarse silenciosamente a Ventas y Postventa.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede relacionarse con cada criterio de aceptación.
