# ES-F04-01: Consultar entregas fallidas

**Funcionalidad padre:** [F-04 — Entregas fallidas y reprogramaciones](../../funcionalidades/F-04-GestionEntregasFallidas.md)

**Responsable:** Gerardo

**Estado:** Reglas de consulta acordadas el 15/10/2026; implementación backend parcial en T-06/T-07; endpoint y verificación funcional pendientes.

**Actor principal:** Gestor de Despacho

**UI:** Aplica; listado de entregas fallidas en la aplicación administrativa.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación existente en `8586a78`, migrada al flujo SDD en `333e4e5`. Esta revisión conserva CA-01 a CA-05 y añade CA-06 a CA-11 para concretar los seis acuerdos de revisión del listado.

## 1. Objetivo

Permitir que el Gestor consulte una bandeja de trabajo con todos los despachos cuyo estado vigente es `FALLIDO`, sin limitar inicialmente las fechas, e identifique cuáles están pendientes de retorno, cuáles ya fueron recibidos y cuáles tienen retorno atrasado. Se muestra una fila por despacho con su incidencia más reciente. El listado permite abrir el detalle o iniciar una confirmación de recepción; las decisiones se ejecutan en sus especificaciones propias.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- Los fallos fueron registrados previamente por F-03 con su motivo, fecha, repartidor, número de intento y referencia de evidencia cuando corresponda.
- Gestión dispone de una referencia inequívoca a la última incidencia de cada despacho fallido y de su recepción. El nombre del repartidor y el cierre de la jornada se consultan en Operación; su indisponibilidad se trata explícitamente, sin inventar datos.
- La consulta utiliza paginación y puede incluir filtros por motivo, fecha de incidencia y estado de recepción.

## 3. Flujo principal

1. El Gestor ingresa a la pantalla de Entregas Fallidas.
2. Al entrar sin una consulta guardada en la URL, solicita la primera página sin filtro de fechas ni motivo y con todas las situaciones de recepción. Al volver del detalle, restaura los filtros y página de la URL y vuelve a consultar.
3. El backend valida identidad, rol y filtros; selecciona una incidencia vigente por despacho `FALLIDO` y aplica motivo y fechas.
4. Obtiene el cierre de las jornadas de las incidencias pendientes y calcula los indicadores sobre toda esa base. Después aplica recepción/atraso y pagina en el orden acordado.
5. El frontend muestra filas, totales, indicadores y posibles avisos de información operativa no disponible. Permite abrir el detalle o iniciar la confirmación de recepción pendiente.

## 4. Reglas y validaciones

- La consulta no debe incluir despachos cuyo estado vigente sea distinto de `FALLIDO`.
- Cada fila muestra código operativo interno, fecha de incidencia, motivo, `Intentos consumidos` sobre el máximo configurado, repartidor, recepción, indicador de evidencia e indicador de pedido anulado.
- El estado de recepción se representa como `Pendiente de retorno` o `Recibido en centro`.
- `NO_INTENTADO` se identifica como `No intentado en esta salida`. No aumenta ni pone a cero el contador acumulado. Puede mostrarse con `0 de 2` o `1 de 2` en la columna `Intentos consumidos`; no se presenta como `Intento 0`.
- Un paquete se muestra como `Retorno atrasado` cuando la jornada asociada a esa incidencia tiene cierre manual o automático confirmado y la recepción sigue pendiente. No se usa la jornada actual del repartidor ni se infiere el cierre por el reloj.
- Los filtros por motivo, fecha y recepción pueden combinarse y siempre se aplican sobre despachos `FALLIDO`.
- Si no existen coincidencias, se muestra un estado vacío y no se incorporan registros de otros estados.
- Un usuario sin el rol requerido no recibe información operativa y obtiene `403 Forbidden`.
- El listado no expone el comentario interno del repartidor, la fotografía ni datos personales innecesarios; esos datos pertenecen al detalle autorizado.

### 4.1. Bandeja vigente y orden

- La consulta inicial incluye fallidos de días anteriores aún sin resolver. Las fechas solo restringen la búsqueda cuando se seleccionan explícitamente y corresponden a la incidencia vigente, con días inclusivos en `America/Lima`.
- Si un despacho falló, fue recibido, se reprogramó y vuelve a fallar, reaparece una sola vez con los datos de la nueva incidencia. Su recepción anterior no acredita el retorno del nuevo reparto. El historial completo pertenece a ES-F04-02.
- Al reprogramarse o cerrarse deja de aparecer en la siguiente consulta, porque ya no está `FALLIDO`.
- Primero se muestran los `Recibidos en centro`, luego los `Pendientes de retorno`. Dentro de cada grupo, la incidencia más antigua primero; el desempate estable y la paginación se definen en el contrato, Gestión §5.1. Se conserva este orden al filtrar. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01).
- El filtro de motivos incluye `NO_INTENTADO` y motivos históricos inactivos desde el catálogo único. Esto no habilita su registro manual en F-03.

### 4.2. Indicadores y filtros de grupo

| Tarjeta | Qué cuenta | Acción al pulsarla |
|---|---|---|
| Pendientes de retorno | Paquetes sin recepción confirmada. | Mostrar ese grupo de filas. |
| Recibidos en centro | Paquetes recibidos cuyos despachos siguen `FALLIDO`. | Mostrar ese grupo de filas. |
| Retornos atrasados | Subconjunto de pendientes con jornada cerrada confirmada. | Mostrar solo ese subconjunto. |

Las tres tarjetas respetan motivo y fechas, pero no el filtro de grupo ni la página seleccionada. Por ejemplo, 7 pendientes, 5 recibidos y 2 atrasados representan 12 despachos, porque los 2 atrasados ya están entre los 7 pendientes. Pulsar una tarjeta reinicia la página y conserva las cifras de las otras; volver a pulsar la seleccionada restablece todos los grupos. El selector de recepción y las tarjetas reflejan el mismo filtro; al elegir recepción desde el selector se desactiva la selección de solo atrasados. `Limpiar filtros` elimina motivo, fechas y grupo y vuelve a la primera página, conservando el tamaño de página elegido.

### 4.3. Información operativa desconocida

- Si falta confirmar la jornada de una fila pendiente, se muestra `No se pudo confirmar el cierre de jornada`. No se marca como atrasada ni se presenta como retorno a tiempo.
- Si alguna jornada pendiente de la base no puede confirmarse, la tarjeta de atrasados muestra `No disponible` y queda deshabilitada; se informa cuántos retornos no pudieron evaluarse y se ofrece reintentar. Las filas y las dos tarjetas de recepción siguen disponibles.
- Una consulta explícita de solo atrasados necesita información completa para ese cálculo; si no la hay, devuelve el error de dependencia definido en el contrato, nunca una lista parcial o un vacío engañoso. Se conserva el filtro para reintentar y se permite volver a todos los grupos.
- Un nombre no recuperado se muestra como `Nombre del repartidor no disponible`, conservando su identificador. No bloquea el resto de la consulta.
- Un paquete recibido no está atrasado aunque no pueda consultarse su jornada. Los valores desconocidos no se sustituyen por cero, `false` ni nombres ficticios.

## 5. Entradas, salidas e integraciones

### Entradas

- Página y tamaño de página.
- Filtro opcional por motivo del fallo.
- Rango opcional de fechas de la incidencia.
- Filtro opcional por recepción: todos, pendiente de retorno o recibido en centro.
- Selección opcional de solo retornos atrasados.
- Identidad y roles obtenidos del JWT.

### Salidas

- Página de despachos fallidos con los campos e indicadores definidos en esta especificación.
- Metadatos de paginación.
- Indicadores agregados y marca de consulta; condición de jornada desconocida cuando corresponda.
- Estado vacío cuando no existen resultados.
- Error normalizado cuando la solicitud no está autorizada o sus filtros son inválidos.

### Integraciones

- F-03 proporciona el fallo, el motivo, el intento, la referencia del repartidor y la referencia de evidencia.
- F-05 proporciona los datos básicos del perfil local del repartidor que se muestran en la consulta.
- F-02 registra la anulación del pedido que debe mostrarse como indicador.
- Operación, como propietario de los perfiles de F-05 y jornadas de F-06, provee la lectura por lotes de la sección 5.4 de su contrato [cite: 2]. Se consultan las jornadas necesarias para el conjunto base antes de paginar; los nombres pueden resolverse solo para la página.
- Gestión no consulta tablas de Operación ni modifica el cierre de turno o las reglas de capacidad de F-06.
- Ruta, parámetros, respuesta, nulabilidad, orden y errores se rigen exclusivamente por `integraciones/api-contract-gestion-despachos.md`, Gestión §4, Gestión §5.1, Operación §5.4 [cite: 2]. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo), [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias).

## 6. Criterios de aceptación

### CA-01. Listado con incidencias

- **DADO** que existen despachos cuyo estado vigente es `FALLIDO`.
- **CUANDO** el Gestor abre la pantalla de Entregas Fallidas.
- **ENTONCES** muestra esos despachos, incluidos los de días anteriores sin resolver, con sus datos operativos, indicadores y paginación, sin aplicar un filtro implícito de fechas.

### CA-02. Aplicación de filtros

- **DADO** un conjunto de despachos fallidos con distintos motivos, fechas y estados de recepción.
- **CUANDO** el Gestor combina uno o más filtros.
- **ENTONCES** devuelve solo las coincidencias, conserva `FALLIDO`, interpreta el rango como días inclusivos de la incidencia vigente en `America/Lima` y reinicia la página al modificar filtros.

### CA-03. Listado sin incidencias

- **DADO** que no existen despachos fallidos que coincidan con la consulta.
- **CUANDO** el Gestor abre o filtra el listado.
- **ENTONCES** el frontend muestra un estado vacío sin datos pertenecientes a otros estados.

### CA-04. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar el listado.
- **ENTONCES** el backend responde `403 Forbidden` y no expone información de los despachos.

### CA-05. Retorno atrasado

- **DADO** un despacho `FALLIDO` cuya jornada asociada a la incidencia tiene cierre manual o automático confirmado y cuyo paquete no tiene recepción confirmada.
- **CUANDO** el Gestor consulta el listado.
- **ENTONCES** el resultado se identifica como `Retorno atrasado` junto al repartidor responsable.

### CA-06. Una incidencia vigente por despacho

- **DADO** un despacho con un fallo anterior recibido y un nuevo fallo después de reprogramarlo.
- **CUANDO** el Gestor consulta el listado.
- **ENTONCES** aparece una sola fila con motivo, fecha, repartidor, jornada, recepción e indicador de evidencia de la nueva incidencia, sin heredar la recepción anterior ni mezclar registros.

### CA-07. Orden estable de atención

- **DADO** varios despachos recibidos y pendientes, con incidencias de distintas fechas o fechas iguales.
- **CUANDO** se consulta y pagina el listado.
- **ENTONCES** se muestran primero los recibidos y luego los pendientes, con la incidencia más antigua primero en cada grupo y el desempate del contrato; sin cambios concurrentes, no se repiten ni omiten filas entre páginas.

### CA-08. Indicadores coherentes con la búsqueda

- **DADO** una base filtrada por motivo y fechas con 7 pendientes, 5 recibidos y 2 atrasados incluidos entre los pendientes.
- **CUANDO** el Gestor cambia página o selecciona una tarjeta.
- **ENTONCES** las tarjetas conservan 7, 5 y 2, la tabla muestra solo el grupo seleccionado y su total propio; los indicadores se recalculan al cambiar motivo o fechas y nunca desde una página parcial.

### CA-09. Salida no intentada y contador acumulado

- **DADO** un despacho con un fallo que consumió intento y una salida posterior con `NO_INTENTADO`.
- **CUANDO** aparece en el listado.
- **ENTONCES** muestra `Intentos consumidos: 1 de 2` para un máximo de dos y `No intentado en esta salida`, manteniendo el contador sin aumento ni reinicio. Sin fallos previos se muestra `0 de 2` bajo el mismo título.

### CA-10. Jornada o nombre no disponible

- **DADO** una consulta normal en la que no puede confirmarse alguna jornada pendiente o recuperarse un nombre.
- **CUANDO** el Gestor consulta el listado.
- **ENTONCES** conserva las filas y cifras locales, muestra los avisos de §4.3, no fabrica atraso ni nombre y permite reintentar. Si pidió solo atrasados y no puede calcularse el conjunto completo, recibe el error de dependencia del contrato en lugar de resultados parciales.

### CA-11. Filtros inválidos

- **DADO** un rango invertido, motivo inexistente, paginación inválida o combinación incompatible de recepción y atrasados.
- **CUANDO** se solicita el listado.
- **ENTONCES** el backend responde `400` con el error normalizado y campos del contrato, sin cambiar datos ni presentar el error como ausencia de incidencias.

## 7. Fuera de alcance

- Consultar el detalle completo, el historial o la fotografía de la incidencia.
- Confirmar la recepción física del paquete.
- Reprogramar o cerrar el despacho.
- Registrar el fallo en campo o cerrar la jornada del repartidor.

## 8. UI, backend y verificación

- La interacción, los estados, la accesibilidad y los criterios de UI se detallan en [ui.md](./ui.md).
- El backend realiza una consulta autorizada de solo lectura. Este comportamiento no confirma recepciones, cambia estados, libera capacidad ni publica eventos.
- El listado expone solo sus indicadores operativos; no devuelve fotografías, URLs firmadas ni comentarios internos del detalle.
- Las decisiones documentales y las fuentes se concretan en Gestión §§4 y 5.1 y Operación §5.4, enlazadas en [cite: 2]. Su implementación, pruebas de contrato y dependencias se registran en [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes); documentarlas no acredita disponibilidad real.

| Criterio | Comprobación prevista | Datos necesarios |
|---|---|---|
| CA-01 | Consulta de integración y renderizado de la página | Despachos fallidos y de otros estados; recepción, intentos e indicadores variados. |
| CA-02 | Combinación de filtros y paginación | Motivos, fechas y recepción distintos; más resultados que una página. |
| CA-03 | Listado vacío y búsqueda sin coincidencias | Sin fallidos o filtros sin resultados; existen despachos de otros estados. |
| CA-04 | Autorización del endpoint y retirada de datos en UI | Usuario autenticado con otro rol; vista con datos cargados antes del rechazo. |
| CA-05 | Cálculo y presentación de retorno atrasado | Jornada cerrada/activa y recepción pendiente/confirmada. |
| CA-06 | Consulta sin duplicados ni recepción heredada | Dos incidencias del mismo despacho con distinto motivo, jornada, recepción y evidencia. |
| CA-07 | Orden y paginación estable | Fechas iguales/distintas y más resultados que una página. |
| CA-08 | Agregados antes de paginar y filtros de grupo | Base 7/5/2, varias páginas, cambio de motivo/fecha y tarjetas. |
| CA-09 | Contador independiente de la incidencia | `NO_INTENTADO` con cero o un fallo previo. |
| CA-10 | Degradación y error al filtrar atrasados | Lote fallido, jornada desconocida, nombre ausente y recibido con jornada desconocida. |
| CA-11 | Rechazo de filtros inválidos | Casos y límites de Gestión §5.1 del contrato. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01). |

La descomposición está en [tasks.md](./tasks.md). Los resultados se registrarán en [evidence.md](./evidence.md); todas las comprobaciones de comportamiento están pendientes.

- [ ] Los criterios CA-01 a CA-11 y los criterios de UI tienen evidencia real.
- [ ] El contrato y las fuentes de datos necesarios están definidos y verificados.
- [ ] La revisión del alcance y los commits de implementación están enlazados.

## 9. Referencias

- [cite: 1] [Funcionalidad F-04](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-01, RF-06, RF-07 y CA-01 a CA-03, CA-14 y CA-18.
- [cite: 2] [Contrato de API](../../integraciones/api-contract-gestion-despachos.md), Gestión §4, Gestión §5.1, Operación §5.4 para catálogo, listado y lectura operativa; Común §3.3, Común §3.5 para autorización y errores. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias), [Convenciones e integración externa](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- [cite: 3] [Diseño de F-04](../../disenio/funcionalidades/f-04.md), Pantalla 1; [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md), sección 23 para su presentación vigente.
- [cite: 4] [Visión general](../../overview.md), integración de F-03, F-04, F-05 y F-06.
