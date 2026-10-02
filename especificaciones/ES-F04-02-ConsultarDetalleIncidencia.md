# ES-F04-02: Consultar el detalle de una incidencia

**Funcionalidad padre:** F-04 — Entregas fallidas y reprogramaciones  
**Responsable:** Gerardo  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho examine la incidencia, la recepción y el historial de un despacho fallido antes de decidir cómo resolverlo. La consulta reúne la información operativa y habilita el acceso autorizado a la evidencia sin convertir esta especificación en responsable de almacenar o registrar dicha evidencia.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El despacho consultado existe y cuenta con una incidencia registrada por F-03.
- La información del fallo, sus intentos, la recepción y el historial están asociados al mismo despacho.
- La evidencia, cuando existe, dispone de una referencia que permite solicitar acceso temporal mediante el mecanismo definido para F-03.

## 3. Flujo principal

1. El Gestor selecciona `Ver detalle` desde el listado de entregas fallidas.
2. El frontend solicita la incidencia mediante el identificador del despacho.
3. El backend valida el rol, la existencia del despacho y su incidencia asociada.
4. El sistema obtiene los datos del fallo, los intentos, la recepción y el historial.
5. Cuando existe evidencia, el sistema ofrece el acceso autorizado previsto por el contrato, sin exponer su ubicación interna.
6. El frontend muestra la información y las acciones disponibles de acuerdo con la recepción, el máximo de intentos y la posible anulación del pedido.

## 4. Reglas y validaciones

- El detalle debe corresponder íntegramente al despacho solicitado; no se combinan datos de incidencias diferentes.
- Se muestran como mínimo motivo, comentario del repartidor, fecha de la incidencia, repartidor, intento actual, máximo configurado, datos de recepción e historial de estados.
- Si existe una fotografía, su visualización utiliza una autorización temporal; no se expone una ruta de almacenamiento permanente.
- La ausencia de evidencia se representa de forma explícita y no impide consultar los demás datos.
- El panel de decisiones refleja las restricciones conocidas: recepción pendiente, máximo de intentos alcanzado o pedido anulado.
- Un identificador inexistente responde `404 Not Found` y no devuelve datos parciales.
- Un usuario sin el rol requerido obtiene `403 Forbidden`.
- La consulta no modifica el despacho, la recepción, los intentos ni el historial.

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador del despacho.
- Identidad y roles obtenidos del JWT.

### Salidas

- Datos de la incidencia y del repartidor responsable.
- Intento actual y máximo de intentos configurado.
- Estado y datos de la recepción en el centro.
- Historial ordenado del despacho.
- Estado de anulación del pedido.
- Referencia o autorización temporal de lectura de la evidencia cuando corresponda.
- Disponibilidad de las acciones de recepción, reprogramación y cierre.

### Integraciones

- F-03 origina la incidencia y proporciona el mecanismo autorizado de acceso a la evidencia.
- F-02 proporciona el indicador de anulación registrado sobre un despacho fallido.
- La consulta de incidencia y la autorización de evidencia respetan las rutas definidas en `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Consulta exitosa

- **DADO** un despacho `FALLIDO` con una incidencia registrada.
- **CUANDO** el Gestor abre su detalle.
- **ENTONCES** visualiza el motivo, comentario, fecha, repartidor, intentos, recepción, historial e indicador de evidencia correspondientes al despacho.

### CA-02. Evidencia disponible

- **DADO** que la incidencia posee una fotografía asociada.
- **CUANDO** el Gestor autorizado solicita verla desde el detalle.
- **ENTONCES** el sistema permite su lectura mediante el mecanismo temporal definido por F-03 sin revelar la ubicación interna del archivo.

### CA-03. Evidencia ausente

- **DADO** que la incidencia no posee evidencia disponible.
- **CUANDO** el Gestor consulta el detalle.
- **ENTONCES** el frontend informa su ausencia y mantiene accesibles los demás datos de la incidencia.

### CA-04. Despacho inexistente

- **DADO** un identificador que no corresponde a un despacho existente.
- **CUANDO** el Gestor solicita el detalle.
- **ENTONCES** el backend responde `404 Not Found` sin devolver información parcial.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar una incidencia.
- **ENTONCES** el backend responde `403 Forbidden` y no expone información ni evidencia.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Registrar o modificar la incidencia informada por el repartidor.
- Almacenar la fotografía o definir su tiempo de conservación.
- Confirmar la recepción, reprogramar o cerrar el despacho desde el backend de esta consulta.
- Modificar manualmente el historial o el contador de intentos.

### Referencias

- [cite: 1] `funcionalidades/F-04-GestionEntregasFallidas.md`, RF-02 y CA-04 a CA-05.
- [cite: 2] `integraciones/api-contract.md`, secciones 10 y 11.
- [cite: 3] `disenio/funcionalidades/f-04.md`, Pantalla 2: Detalle de la Incidencia.
- [cite: 4] `overview.md`, RT-02 sobre historial auditable.
