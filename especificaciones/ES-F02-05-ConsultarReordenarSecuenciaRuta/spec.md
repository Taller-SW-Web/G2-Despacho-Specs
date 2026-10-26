# ES-F02-05: Consultar y reordenar la secuencia de ruta

**Funcionalidad padre:** [F-02 — Programación y asignación de despachos](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-06 y CA-14.

**Responsable:** Tarqui.

**Estado:** Implementada y verificada localmente en `feature/f02-rutas-transferencia-segura`; aceptación humana pendiente. Resultados en evidence.md.

**Actor principal:** Gestor de Despacho (aplicación web administrativa).

**Servicio propietario:** Gestión de Despachos.

**UI:** Aplica; pestaña "Rutas por repartidor" del panel administrativo con reordenamiento manual drag & drop y botones subir/bajar, documentada en [ui.md](./ui.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md) y [UI](./ui.md). Preparación del 16/10/2026; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

Una vez que los despachos han sido asignados a un repartidor para la jornada en curso, el Gestor de Despacho necesita supervisar el recorrido integral y optimizar manualmente el orden de las paradas según criterios logísticos, geográficos o de prioridad de entrega.

El objetivo es consultar la ruta y permutar las posiciones vigentes de despachos `ASIGNADO`, preservando posiciones históricas de paradas iniciadas/cerradas. Una ruta nueva es continua `1..N`; los huecos históricos por retiro no se compactan. El orden se entrega a F-03 mediante proyecciones versionadas durables, con consistencia eventual [cite: 1].

## 2. Alcance

- Incluye: consulta ordenada de ruta con estados; reordenamiento de `ASIGNADO` mediante arrastre o subir/bajar; permutación de posiciones vigentes, conservando huecos históricos y posiciones fijas; fotografía versionada, resultado recuperable, persistencia, barra Guardar/Descartar, auditoría y proyecciones durables (RT-02).
- Fuera de alcance: optimización automática de rutas mediante algoritmos TSP / ruteo vehicular externo (el orden lo decide el Gestor); alteración del orden de despachos en estado `EN_CAMINO`, `ENTREGADO` o `FALLIDO` (bloqueados permanentemente); ejecución del traslado por el repartidor (F-03).

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- El Gestor está autenticado con JWT y posee el rol `GESTOR_DESPACHO`.
- La jornada del repartidor existe y se encuentra activa para el día actual.
- Existen despachos asignados a dicha jornada.
- Solo los despachos en estado `ASIGNADO` son elegibles para cambiar de posición.

### 3.2. Dependencias

- **Contrato de API:** [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) (`GET /api/v1/jornadas/{idJornada}/ruta` y `PUT /api/v1/jornadas/{idJornada}/secuencia`).
- **Web del Repartidor (F-03):** consume el nuevo orden de paradas en su pantalla "Mi Ruta".
- **Trazabilidad (ES-F02-08 / RT-02):** registra la auditoría con la secuencia anterior y nueva.

### 3.3. Resultados

- Secuencia actualizada permutando los espacios vigentes (`1..N` en rutas nuevas), sin compactar huecos históricos.
- Respuesta HTTP `200 OK` con la lista de despachos reordenados.
- En la interfaz web, la ruta refleja el orden confirmado y la barra de cambios pendientes desaparece.
- F-03 muestra las paradas en el nuevo orden tras procesar las proyecciones versionadas y consultar de nuevo.

## 4. Flujo principal y alternativas

1. El Gestor ingresa a la pestaña "Rutas por repartidor" y selecciona un repartidor o jornada activa.
2. El sistema invoca `GET /api/v1/jornadas/{idJornada}/ruta` y despliega la secuencia de entregas.
3. El Gestor arrastra una tarjeta de despacho `ASIGNADO` o utiliza los botones de flecha (subir/bajar) para cambiar su posición relativa.
4. La interfaz activa la barra inferior fija de cambios pendientes indicando el número de paradas modificadas, con botones "Guardar orden" y "Descartar".
5. El Gestor pulsa "Guardar orden".
6. El frontend envía `PUT /api/v1/jornadas/{idJornada}/secuencia` con el arreglo de `{ idDespacho, posicion }`.
7. El backend valida:
   - Que todos los despachos pertenezcan a la jornada indicada.
   - Que todos los despachos cuyo orden cambia estén estrictamente en estado `ASIGNADO` y la jornada esté confirmada activa.
   - Que las posiciones sean una permutación exacta de los espacios vigentes, sin duplicados ni huecos nuevos.
   - Control de fotografía original mediante `If-Match` y versiones de despacho; resultado durable con `Idempotency-Key`.
8. Persiste atómicamente la nueva secuencia y el registro de auditoría.
9. Responde `200 OK`.
10. La interfaz muestra notificación de confirmación y oculta la barra de cambios pendientes.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Despacho en camino o cerrado | Se intenta reordenar un despacho en `EN_CAMINO`, `ENTREGADO` o `FALLIDO` | Responde `409 Conflict` y no modifica la secuencia | CA-03 |
| Secuencia discontinua | El payload contiene posiciones duplicadas o con saltos (ej. 1, 3) | Responde `400 Bad Request` indicando "Secuencia de ruta inválida" | CA-04 |
| Conflicto de estado concurrente | Un despacho pasó a `EN_CAMINO` en F-03 mientras el Gestor reordenaba | Responde `409 Conflict`, recarga la ruta y notifica el conflicto | CA-05 |
| Descarte de cambios en UI | El Gestor pulsa "Descartar" en la barra de cambios | La interfaz revierte la vista al orden persistido original sin invocar a la API | CUI-03 |
| Sin permisos | Token sin rol `GESTOR_DESPACHO` | Responde `403 Forbidden` | CA-06 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Solo los despachos en estado `ASIGNADO` admiten reordenamiento; los estados posteriores quedan fijados. | F-02 RF-06, CA-14 |
| RN-02 | Permutar exactamente las posiciones vigentes; `1..N` en rutas nuevas. No crear huecos ni compactar los históricos por retiro. | Gestión §3.2.1 |
| RN-03 | Los despachos ya completados o en traslado conservan su número de posición histórica. | api-contract-gestion-despachos.md §3.2 |
| RN-04 | Todo reordenamiento exitoso queda auditado con la secuencia anterior y la nueva. | F-02 RF-04, RT-02 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `GET /api/v1/jornadas/{idJornada}/ruta` | Consulta completa de paradas de la jornada. | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) |
| `PUT /api/v1/jornadas/{idJornada}/secuencia` | Actualización atómica de la secuencia. | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) |
| Web del Repartidor (F-03) | Consumo del orden de entrega en ruta. | [F-03-AppMovilRepartidor.md](../../funcionalidades/F-03-AppMovilRepartidor.md) |

## 6. Criterios de aceptación

### CA-01. Consulta del seguimiento operativo y ruta de la jornada

- **DADO** un repartidor con despachos asignados en la jornada en curso.
- **CUANDO** el Gestor consulta `GET /api/v1/jornadas/{idJornada}/ruta`.
- **ENTONCES** el sistema devuelve la lista completa de despachos ordenada por `posicionSecuencia` ascendente, con sus respectivos estados (`ASIGNADO`, `EN_CAMINO`, `ENTREGADO`, `FALLIDO`), direcciones y datos del destinatario.

### CA-02. Reordenamiento exitoso de despachos en estado ASIGNADO

- **DADO** una jornada con varios despachos en estado `ASIGNADO`.
- **CUANDO** el Gestor envía una nueva secuencia válida en `PUT /api/v1/jornadas/{idJornada}/secuencia`.
- **ENTONCES** permuta atómicamente las posiciones vigentes sin nuevos huecos ni duplicados, conserva las posiciones fijas y los huecos históricos, audita y responde `200 OK` con la ruta y nueva versión.

### CA-03. Rechazo de alteración de posición para despachos en traslado o cerrados

- **DADO** un despacho que se encuentra en `EN_CAMINO`, `ENTREGADO` o `FALLIDO`.
- **CUANDO** se envía una solicitud que intenta modificar su número de posición en la secuencia.
- **ENTONCES** el sistema responde `409 Conflict`, no realiza cambios parciales y conserva inalteradas las posiciones previas.

### CA-04. Rechazo por secuencia discontinua o duplicada

- **DADO** un payload con posiciones repetidas, identidades omitidas/ajenas o posiciones que no corresponden al conjunto vigente (por ejemplo, 1 y 3 para una ruta original 1 y 2).
- **CUANDO** es validado por el backend.
- **ENTONCES** el sistema responde `400 Bad Request` ("Secuencia de ruta inválida") y no aplica cambios en base de datos.

### CA-05. Conflicto por cambio de estado concurrente en F-03

- **DADO** que un despacho estaba en `ASIGNADO` y el repartidor confirma "En camino" en F-03 antes de que el Gestor guarde la nueva secuencia.
- **CUANDO** se ejecuta la actualización en Gestión.
- **ENTONCES** el backend detecta el conflicto de concurrencia, rechaza la operación con `409 Conflict` e instruye recargar la ruta actualizada.

### CA-06. Acceso sin permisos requeridos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar o modificar la secuencia de una ruta.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone datos operativos.

## 7. Referencias

1. [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md): requisito RF-06 y criterio CA-14.
2. [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación): endpoints de ruta y secuencia.
3. [ui.md](./ui.md): especificación visual y de interacción drag & drop.
