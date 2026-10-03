# ES-F02-05: Consultar y reordenar la secuencia de ruta

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho (aplicación web)

## 1. Objetivo

Permitir que el Gestor de Despacho consulte el seguimiento operativo integral de la ruta asignada a un repartidor en su jornada y ajuste manualmente la secuencia u orden de entrega de aquellos despachos que se encuentran en estado `ASIGNADO` antes de que el operador inicie su recorrido. La especificación asegura que la secuencia se mantenga matemáticamente continua sin saltos ni duplicados y actualiza de inmediato el orden que visualiza la aplicación del repartidor (F-03).

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO` mediante token JWT.
- Existe una jornada operativa activa para el repartidor en F-06.
- Existen despachos asignados a dicha jornada.
- La identidad del ejecutor procede de la sesión autenticada.

## 3. Flujo principal

1. El Gestor accede a la pestaña "Rutas por repartidor" y selecciona a un repartidor en turno de la lista lateral (o mediante el selector en tableta).
2. El frontend consulta `GET /api/v1/jornadas/{idJornada}/ruta` enviando el identificador de la jornada.
3. El backend valida los permisos y retorna la información de cabecera (repartidor, furgoneta, zona, barras de ocupación en kg, m³ y paquetes) y el listado de despachos en ruta con sus estados vigentes (`ASIGNADO`, `EN_CAMINO`, `ENTREGADO`, `FALLIDO`) y marca temporal del último cambio.
4. El Gestor reordena la secuencia de las paradas en estado `ASIGNADO` utilizando el asa de arrastre (`drag and drop`) o pulsando los botones de fila "Subir" o "Bajar".
5. El frontend detecta la modificación, renumera visualmente las paradas y despliega la barra fija inferior de cambios pendientes con las opciones "Descartar" y "Guardar orden".
6. El Gestor pulsa "Guardar orden"; el frontend envía una petición `PUT /api/v1/jornadas/{idJornada}/secuencia` conteniendo el arreglo ordenado de identificadores y sus nuevas posiciones.
7. El backend valida de forma atómica:
   - Que todos los despachos incluidos sigan en estado `ASIGNADO`.
   - Que pertenezcan a la jornada indicada.
   - Que las posiciones conformen una secuencia continua válida (1 a N) sin repeticiones ni huecos.
8. El sistema actualiza las posiciones de los despachos en la base de datos y registra la auditoría de la operación.
9. El backend responde `200 OK` con la secuencia confirmada.
10. El frontend oculta la barra de cambios pendientes y notifica "Orden de ruta actualizado correctamente". La web del repartidor (F-03) refleja de inmediato la nueva secuencia en su próxima consulta.

## 4. Reglas y validaciones

- **Exclusividad de reordenamiento:** únicamente los despachos en estado `ASIGNADO` admiten reordenamiento y exhiben controles de arrastre o botones Subir/Bajar.
- **Inmutabilidad de despachos en curso o cerrados:** los despachos en `EN_CAMINO`, `ENTREGADO` y `FALLIDO` son estrictamente inmutables en su posición; se presentan atenuados (60 % de opacidad), sin asa de arrastre ni controles de desplazamiento, fijados en su orden cronológico u operativo.
- **Continuidad estricta de la secuencia:** la lista reordenada debe representar una secuencia continua de enteros positivos `[1, 2, ..., N]` sin omisiones, posiciones repetidas ni valores nulos.
- **Detección de conflictos de concurrencia (`409 Conflict`):** si mientras el Gestor ajusta el orden en pantalla, el repartidor marca "En camino" sobre uno de los paquetes en F-03, o si Ventas cancela un pedido, el backend rechaza la actualización con `409 Conflict` ("Un despacho cambió de estado mientras ordenabas"), no altera la base de datos y recarga automáticamente la ruta con la información vigente.
- **Descarte de cambios pendientes:** si el usuario pulsa "Descartar" en la barra inferior o intenta cambiar de repartidor/pestaña confirmando el diálogo de abandono, el frontend cancela las modificaciones y restaura el orden previamente guardado en el servidor.
- **Trazabilidad y seguimiento en ruta:** cada fila expone la hora o tiempo transcurrido desde el último cambio de estado para dar soporte al requisito transversal de seguimiento en ruta (RT-04).
- **Despachos cancelados:** un despacho cancelado por Ventas y Postventa es purgado de la ruta y las posiciones restantes se compactan correlativamente.

## 5. Entradas, salidas e integraciones

### Entradas

- Consulta de ruta: `GET /api/v1/jornadas/{idJornada}/ruta`.
- Actualización de secuencia: `PUT /api/v1/jornadas/{idJornada}/secuencia`.
- Payload JSON de reordenamiento según `integraciones/api-contract.md`:
  ```json
  {
    "despachos": [
      { "idDespacho": "DSP-100234", "posicion": 1 },
      { "idDespacho": "DSP-100240", "posicion": 2 }
    ]
  }
  ```
- Encabezado `Authorization: Bearer <jwt_usuario>`.

### Salidas

- Respuesta HTTP `200 OK` con la lista de despachos y sus posiciones consolidadas.
- Notificación toast en frontend y ocultamiento de la barra de cambios pendientes.
- Error `409 Conflict` si algún despacho cambió de estado durante la edición.
- Error `400 Bad Request` si la secuencia es discontinua o contiene identificadores duplicados.

### Integraciones

- **Web del Repartidor (F-03):** consume la secuencia persistida a través del endpoint `GET /api/v1/repartidor/mi-ruta`.
- **Trazabilidad (ES-F02-08):** audita el cambio de secuencia con el identificador del gestor y la jornada.
- **Reasignación (ES-F02-06):** el botón de fila "Reasignar" disponible en paradas `ASIGNADO` abre el flujo de reasignación.
- Los contratos y esquemas se rigen por `integraciones/api-contract.md` (Sección 9.2).

## 6. Criterios de aceptación

### CA-01. Consulta exitosa de la ruta del repartidor

- **DADO** un repartidor con jornada activa y despachos asignados en distintos estados (`ASIGNADO`, `EN_CAMINO`, `ENTREGADO`).
- **CUANDO** el Gestor abre el detalle de su ruta.
- **ENTONCES** el sistema muestra todas las paradas en su orden de secuencia actual, destacando los despachos operables `ASIGNADO` y presentando atenuados y fijos los despachos en traslado o cerrados con su hora de última actualización.

### CA-02. Reordenamiento exitoso de despachos asignados

- **DADO** un repartidor con 3 despachos en estado `ASIGNADO` en las posiciones 1, 2 y 3.
- **CUANDO** el Gestor intercambia la posición 1 con la 3 y pulsa "Guardar orden".
- **ENTONCES** el sistema valida que todos sigan en `ASIGNADO`, persiste la nueva secuencia continua 1, 2 y 3 en base de datos y responde `200 OK`.

### CA-03. Conflicto concurrente por cambio de estado en ruta (`409`)

- **DADO** que el Gestor tiene cambios sin guardar en la secuencia de ruta de un repartidor.
- **CUANDO** el repartidor pulsa "En camino" sobre uno de esos despachos desde F-03 y el Gestor intenta pulsar "Guardar orden".
- **ENTONCES** el backend responde `409 Conflict`, no aplica el reordenamiento, muestra la alerta explicativa en pantalla y recarga la ruta con el despacho actualizado a `EN_CAMINO`.

### CA-04. Intento de reordenar despachos en traslado o cerrados

- **DADO** un despacho en estado `EN_CAMINO`, `ENTREGADO` o `FALLIDO`.
- **CUANDO** se renderiza la fila en la ruta.
- **ENTONCES** la interfaz no ofrece asa de arrastre ni botones Subir/Bajar, y si se envía en el payload del endpoint de secuencia, el backend responde `400 Bad Request` o `409 Conflict`.

### CA-05. Descarte de cambios no guardados

- **DADO** que el Gestor modificó el orden de las paradas en pantalla pero decide no aplicarlo.
- **CUANDO** pulsa el botón "Descartar" en la barra de cambios pendientes.
- **ENTONCES** la interfaz revierte las paradas al orden exacto guardado en el servidor y oculta la barra de cambios pendientes.

### CA-06. Acceso sin permisos requeridos

- **DADO** un usuario autenticado sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar la ruta o actualizar la secuencia.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone datos operativos.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Optimización algorítmica automática de rutas mediante mapas o GPS (el orden es definido por el criterio del Gestor).
- Navegación asistida paso a paso para el repartidor (corresponde a apps externas vía F-03).
- Registro de evidencias fotográficas o cambios de estado a `EN_CAMINO` / `ENTREGADO` (corresponde a F-03).

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-06).
- Contrato de API: `integraciones/api-contract.md` (Sección 9.2).
- Seguimiento en ruta y estados: `arquitectura/diagrama-estados-despacho.md`.
- Diseño de interfaz: `disenio/funcionalidades/f-02.md` (Pantalla 3) y `disenio/SYSTEM-DESIGN.md` (Sección 13.11).
