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
- Detalle del despacho con historial de operaciones e intentos y evidencia mediante el acceso temporal de Operación, §3.4; conserva consulta histórica después de resolverlo.
- Política de intentos configurable, con valor inicial de dos.
- Reprogramación con nueva fecha y retorno a la cola de F-02.
- Tratamiento diferenciado de los despachos `NO_INTENTADO`, que no consumen intentos.
- Cierre del despacho como `DEVUELTO_A_ORIGEN`.
- Restricción al cierre como devuelto cuando el pedido fue anulado.
- Auditoría de cada recepción y decisión.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario está autenticado con rol `GESTOR_DESPACHO`.
- Para recibir, reprogramar o cerrar, el despacho existe y está en `FALLIDO`; el detalle de una incidencia histórica sigue consultable en otros estados, sin acciones de resolución.
- El registro del fallo contiene motivo, fecha, repartidor y condición de consumo de intento; el despacho conserva el contador acumulado.
- Para reprogramar o cerrar el despacho, su paquete debe haberse recibido en el centro de despacho.
- La política de intentos está configurada; el valor inicial es dos.
- La nueva fecha de entrega es posterior a la fecha actual.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Proporcionar la identidad y el rol `GESTOR_DESPACHO`. |
| Web del Repartidor (F-03) | Originar el registro del fallo, su motivo, evidencia y referencias de repartidor/jornada; Gestión conserva la incidencia canónica y el contador. F-03 provee el acceso autorizado a la evidencia y consume el catálogo único de Gestión. |
| Programación y Asignación (F-02) | Recibir los despachos reprogramados en la cola y registrar la anulación de pedidos sobre despachos fallidos. |
| Gestión de Repartidores y Vehículos (F-05) | Proveer los datos básicos del perfil local del repartidor asociado al intento para las consultas operativas. |
| Disponibilidad y Capacidad Diaria (F-06) | Dejar de contar el paquete en la ocupación del repartidor y la furgoneta cuando se confirma su recepción. |
| Requisitos transversales (overview, sección 6) | Validar las transiciones, registrar el historial y publicar los eventos hacia Ventas y Postventa. |
| Ventas y Postventa | Recibir el resultado de la reprogramación o del cierre como devuelto a origen. |

### 4.3. Resultados

- Una recepción confirmada registra fecha, usuario, sello y observación opcional, sin cambiar `FALLIDO`, e inserta una solicitud durable de liberación. La capacidad se considera liberada solo cuando Operación la confirma; una caída no revierte el retorno físico.
- Una reprogramación válida cambia el estado a `PENDIENTE_ASIGNACION`, registra la nueva fecha programada y conserva el contador de intentos.
- Un cierre cambia el estado a `DEVUELTO_A_ORIGEN` y genera el evento correspondiente hacia Ventas y Postventa.
- Toda operación registra usuario, fecha, estado anterior, estado nuevo y observaciones.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Consultar entregas fallidas

El sistema DEBE permitir al Gestor consultar los despachos en `FALLIDO`.

#### CA-01. Listado con incidencias

- **DADO** que existen despachos en `FALLIDO`.
- **CUANDO** el Gestor abre la pantalla de Entregas Fallidas.
- **ENTONCES** muestra una fila por despacho con código operativo interno, fecha y motivo de su incidencia vigente, `Intentos consumidos` sobre el máximo, repartidor, recepción, indicador de evidencia y pedido anulado, con paginación y filtros por motivo, fecha y recepción.

La consulta inicial no restringe fechas y mantiene visibles los fallidos de días anteriores sin resolver. Se muestran primero los recibidos y luego los pendientes, con la incidencia más antigua primero en cada grupo. El listado utiliza siempre motivo, repartidor, jornada, recepción y evidencia de la misma incidencia vigente; un nuevo fallo después de reprogramar no hereda la recepción anterior.

Los indicadores `Pendientes de retorno`, `Recibidos en centro` y `Retornos atrasados` respetan motivo y fechas, pero no la página ni el grupo seleccionado. Los atrasados son un subconjunto de pendientes. Los detalles verificables de selección, orden, indicadores y degradación se desarrollan en [ES-F04-01](../especificaciones/ES-F04-01-ConsultarEntregasFallidas/spec.md), sin duplicar el contrato de API.

#### CA-02. Listado sin incidencias

- **DADO** que no existen despachos en `FALLIDO`.
- **CUANDO** el Gestor abre la pantalla.
- **ENTONCES** se muestra un estado vacío sin información de otros estados.

#### CA-03. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** consulta las incidencias.
- **ENTONCES** el backend responde `403 Forbidden`.

### RF-02. Consultar el detalle de una incidencia

El sistema DEBE mostrar la información necesaria para decidir y conservar su consulta después de la resolución. [ES-F04-02](../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/spec.md) concreta la última incidencia, recepción por salida, historial completo, evidencia, degradación y acciones combinadas; el formato se define en [Gestión §5.3](../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02).

#### CA-04. Detalle exitoso

- **DADO** un despacho en `FALLIDO`.
- **CUANDO** el Gestor abre su detalle.
- **ENTONCES** ve la última incidencia sin mezclar salidas: motivo, comentario, fecha, repartidor, intentos consumidos sobre el máximo vigente, recepción, historial de operaciones y estado local de comunicación con Ventas. La fotografía utiliza el acceso autorizado de Operación; las acciones respetan primero recepción y después límite/anulación. Fuera de `FALLIDO` se muestra el estado actual y se conserva solo la consulta.

#### CA-05. Despacho inexistente

- **DADO** un código que no corresponde a un despacho.
- **CUANDO** se solicita el detalle.
- **ENTONCES** el backend responde `404 Not Found` sin datos parciales.

### RF-03. Reprogramar un despacho

El sistema DEBE permitir fijar una nueva fecha mientras no se haya alcanzado el máximo de intentos. [ES-F04-04](../especificaciones/ES-F04-04-ReprogramarDespachoFallido/spec.md) concreta recepción por incidencia, fecha civil futura en `America/Lima`, observación opcional, conflictos, idempotencia y retorno inmediato a F-02; [Gestión §5.2.2](../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04) es la definición canónica de la operación.

#### CA-06. Reprogramación válida

- **DADO** un despacho fallido, recibido en el centro, con un intento y máximo configurado de dos.
- **CUANDO** el Gestor selecciona una fecha futura y confirma.
- **ENTONCES** responde `200`, cambia a `PENDIENTE_ASIGNACION` ("En centro de despacho"), guarda la nueva fecha, conserva el contador en uno y persiste versión, entrada a cola, auditoría y resultado durable; registra el evento si no es simulado. F-02 lo muestra inmediatamente, con asignación bloqueada hasta la fecha programada y mientras siga activa la reserva anterior. Conserva la zona original aunque esté inactiva, sin recotizar ni crear otra asignación; una liberación pendiente no impide reprogramar.

#### CA-07. Fecha inválida

- **DADO** un despacho reprogramable.
- **CUANDO** el Gestor selecciona la fecha actual o una pasada.
- **ENTONCES** el sistema responde `400 Bad Request`, explica la validación y el despacho sigue en `FALLIDO`.

#### CA-08. Límite de intentos alcanzado

- **DADO** un despacho cuyo contador es igual o superior al máximo configurado.
- **CUANDO** el Gestor abre el detalle o intenta reprogramar.
- **ENTONCES** el frontend deshabilita la reprogramación, el backend responde `422 Unprocessable Entity` ante el intento que cumple las demás precondiciones y, una vez recibida la devolución física, solo se ofrece el cierre como `DEVUELTO_A_ORIGEN`. Con recepción pendiente, primero se exige confirmarla.

#### CA-09. Estado desactualizado

- **DADO** un despacho que ya no está en `FALLIDO`.
- **CUANDO** se intenta reprogramar con información desactualizada.
- **ENTONCES** el backend responde `409 Conflict` y conserva el estado vigente.

### RF-04. Cerrar el despacho como devuelto a origen

El sistema DEBE permitir cerrar un despacho fallido cuyo paquete permanecerá en el centro de despacho y comunicar el resultado a Ventas y Postventa. [ES-F04-05](../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen/spec.md) concreta el cierre individual con motivo en texto libre, recepción por incidencia, concurrencia y recuperación; [Gestión §5.2.3](../integraciones/api-contract-gestion-despachos.md#523-cerrar-como-devuelto-a-origen--es-f04-05) define la operación. El caso habitual es límite alcanzado o pedido anulado; se conserva la decisión operativa explícita aunque queden intentos, sin cierre automático.

#### CA-10. Cierre exitoso

- **DADO** un despacho en `FALLIDO` recibido en el centro.
- **CUANDO** el Gestor confirma el cierre indicando un motivo.
- **ENTONCES** responde `200`, cambia a `DEVUELTO_A_ORIGEN` ("De vuelta en el centro de despacho") y guarda versión, motivo, auditoría y resultado original; registra el evento `DESPACHO_DEVUELTO_A_ORIGEN` para envío asíncrono si es real. El simulado conserva historial sin evento externo. La liberación pendiente de la recepción continúa sin bloquear ni revertir el cierre.

#### CA-11. Operación repetida

- **DADO** un despacho ya cerrado como `DEVUELTO_A_ORIGEN`.
- **CUANDO** se repite la operación.
- **ENTONCES** no se duplican el cambio de estado, la auditoría ni el evento, y se informa que la decisión ya fue procesada.

#### CA-12. Falla de la comunicación externa

- **DADO** un despacho cerrado como `DEVUELTO_A_ORIGEN`.
- **CUANDO** Ventas y Postventa no está disponible.
- **ENTONCES** el estado local se conserva y el evento queda registrado como pendiente de reintento (overview, RT-03).

### RF-05. Mantener trazabilidad

El sistema DEBE conservar el historial de recepciones y decisiones. [ES-F04-06](../especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones/spec.md) concreta las garantías de esos mismos registros de ES-F04-03/04/05 en el historial único de RT-02: captura en la transacción de origen, datos por incidencia, inmutabilidad y ausencia de duplicados; no agrega otra auditoría, tabla o pantalla.

#### CA-13. Registro de auditoría

- **DADO** una recepción, reprogramación o cierre aceptado.
- **CUANDO** se persiste.
- **ENTONCES** se guarda exactamente una entrada del historial común en la misma transacción de origen, con ejecutor del JWT, instante UTC, origen manual, incidencia, estados y datos propios de recepción, nueva fecha o motivo de cierre. Rechazos, repeticiones y reintentos técnicos no agregan otra decisión aceptada; el detalle presenta solo los campos previstos por su contrato.

### RF-06. Casos especiales de resolución

El sistema DEBE tratar de forma diferenciada los despachos no intentados y los pedidos anulados.

#### CA-14. Reprogramación de un despacho no intentado

- **DADO** un despacho en `FALLIDO` con motivo `NO_INTENTADO`, recibido en el centro, pedido no anulado y contador inferior al máximo vigente.
- **CUANDO** el Gestor lo reprograma con una fecha futura.
- **ENTONCES** el despacho vuelve a `PENDIENTE_ASIGNACION` sin cambiar el contador y deja el listado de fallidos. Antes de decidir, el listado identifica la incidencia como `No intentado en esta salida`; el historial conserva ese motivo aunque existan intentos fallidos previos.

#### CA-15. Despacho fallido con pedido anulado

- **DADO** un despacho en `FALLIDO` sobre el cual F-02 registró la anulación del pedido.
- **CUANDO** el Gestor abre su detalle o intenta reprogramarlo.
- **ENTONCES** la reprogramación está deshabilitada, el backend la rechaza con `409 Conflict` y, después de confirmar la recepción, solo se permite el cierre como `DEVUELTO_A_ORIGEN`.

### RF-07. Recepción del paquete en el centro de despacho

El sistema DEBE registrar el retorno físico de cada paquete antes de cualquier decisión. Normalmente ocurre al volver del recorrido; el cierre de jornada no confirma recepciones ni obliga a recibir automáticamente todos los pendientes. [ES-F04-03](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/spec.md) concreta la recepción individual, idempotencia y recuperación de la liberación, sin requerir jornada cerrada para un fallo ya registrado.

#### CA-16. Confirmación de recepción

- **DADO** un despacho en `FALLIDO` marcado como "Pendiente de retorno".
- **CUANDO** el Gestor confirma que el paquete llegó al centro de despacho, indicando si el sello está intacto.
- **ENTONCES** responde `202`, marca "Recibido en centro" sin cambiar `FALLIDO` y guarda recepción, auditoría, versión y solicitud durable en una transacción local. F-06 deja de contar la reserva cuando Operación confirma su liberación; mientras tanto el detalle informa sincronización pendiente sin revertir la recepción.

#### CA-17. Decisión sin recepción confirmada

- **DADO** un despacho en `FALLIDO` cuyo paquete aún no se recibió en el centro.
- **CUANDO** el Gestor intenta reprogramarlo o cerrarlo.
- **ENTONCES** el backend responde `409 Conflict` indicando que primero debe confirmarse la recepción.

#### CA-18. Paquete no retornado al cierre de la jornada

- **DADO** un despacho en `FALLIDO` cuya jornada asociada a la incidencia tiene cierre manual o automático confirmado.
- **CUANDO** el paquete sigue sin recepción confirmada.
- **ENTONCES** el listado lo resalta como "Retorno atrasado" junto al nombre del repartidor responsable.

Si no puede confirmarse la jornada, el listado informa `No se pudo confirmar el cierre de jornada`, sin inventar un atraso ni descartarlo. La tarjeta de atrasados muestra `No disponible` si no puede calcularse su cifra exacta; las filas y los indicadores de recepción siguen disponibles según ES-F04-01 y el contrato. La consulta no altera las reglas de cierre de turno ni de capacidad de F-06.

## 6. Frontend

| Elemento | Responsabilidad |
|---|---|
| Pantalla de Entregas Fallidas | Filtros, listado paginado, indicadores de recepción, "No intentado", "Pedido anulado" y "Retorno atrasado", y estados de carga, vacío y error. |
| Confirmación de recepción | Registro del retorno del paquete con estado del sello y observaciones. |
| Detalle de la incidencia | Última incidencia, intentos consumidos, recepción por salida, historial completo, comunicación con Ventas y fotografía autorizada; consulta histórica tras resolver. |
| Formulario de reprogramación | Fecha futura con validación; disponible solo con recepción confirmada. |
| Confirmación de cierre | Motivo obligatorio y advertencia de que el despacho no tendrá más intentos. |
| Retroalimentación | Éxito, validaciones, conflictos y errores de comunicación. |

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Consulta de incidencias | Recuperar despachos `FALLIDO` con filtros y paginación. |
| Registro de recepción | Guardar retorno, auditoría, versión y solicitud durable; recuperar la liberación por la reserva original y exponer su estado pendiente/confirmado. |
| Consulta de detalle | Componer los datos canónicos, historial y acciones; devolver la referencia de evidencia para que el contenedor de UI solicite su lectura a Operación. |
| Caso de uso de reprogramación | Validar estado, recepción, fecha, límite de intentos y anulación antes de solicitar la transición. |
| Caso de uso de cierre | Validar recepción y solicitar la transición a `DEVUELTO_A_ORIGEN`. |
| Política de intentos | Leer y aplicar el máximo configurable. |
| Persistencia y auditoría | Guardar recepciones y decisiones de manera consistente. |

Esta sección no prescribe clases ni paquetes. Las rutas, cuerpos y códigos se definen en `integraciones/api-contract-gestion-despachos.md`.

## 8. Requisitos no funcionales

- **Seguridad:** todas las operaciones requieren rol `GESTOR_DESPACHO`.
- **Aislamiento:** no se accede a bases de datos de otros módulos.
- **Consistencia:** cambios de estado, auditoría y eventos asociados se persisten en la misma transacción local. La recepción persiste junto con su historial y solicitud de liberación; Operación se actualiza después con entrega recuperable e idempotente.
- **Idempotencia:** la recepción, reprogramación y cierre repetidos no producen efectos duplicados; un resultado aceptado se reconoce antes de aplicar las precondiciones actuales.
- **Trazabilidad:** las recepciones, las decisiones y el estado de su comunicación son consultables.
- **Usabilidad y escalabilidad:** pantalla responsive y listados paginados.

## 9. Fuera de alcance

- **Reembolsos, cambios, devoluciones comerciales y reclamos:** pertenecen a Ventas y Postventa.
- **Almacenamiento, reingreso a inventario y reintegro de stock:** pertenecen a la operación del centro, Ventas y Postventa y Productos y Ofertas; Despacho solo registra que el paquete volvió.
- **Registro del fallo en campo:** corresponde a F-03.
- **Asignación del nuevo intento a un repartidor:** corresponde a F-02.
- **Transporte y reintentos de los eventos:** corresponden al requisito transversal RT-03 del overview.

La posible logística inversa posterior a una entrega está centralizada en [Pendientes](./pendiente.md), sección F-04. No forma parte de esta funcionalidad mientras no exista un acuerdo con Ventas y Postventa.

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
| CA-16 a CA-18 | Confirmar recepción, decidir sin recepción y cerrar la jornada sin retorno. | Unitaria e integración | Ocupación liberada en F-06, `409` y alerta de retorno atrasado. |

Además, se ejecutarán tres recorridos funcionales completos:

1. `FALLIDO` → recepción en centro → reprogramación → `PENDIENTE_ASIGNACION` → visible inmediatamente en la cola de F-02, con asignación habilitada desde la fecha programada.
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
