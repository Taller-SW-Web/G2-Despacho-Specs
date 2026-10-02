# ES-F04-01: Consultar entregas fallidas

**Funcionalidad padre:** F-04 — Entregas fallidas y reprogramaciones  
**Responsable:** Gerardo  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho consulte únicamente los despachos cuyo estado vigente es `FALLIDO`, identifique si sus paquetes ya regresaron al centro y reconozca los retornos atrasados. El listado proporciona el punto de entrada para confirmar una recepción o revisar el detalle antes de decidir una reprogramación o un cierre.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- Los fallos fueron registrados previamente por F-03 con su motivo, fecha, repartidor, número de intento y referencia de evidencia cuando corresponda.
- El sistema dispone del estado de recepción del paquete y de la información necesaria para determinar si la jornada del repartidor ya terminó.
- La consulta utiliza paginación y puede incluir filtros por motivo, fecha de incidencia y estado de recepción.

## 3. Flujo principal

1. El Gestor ingresa a la pantalla de Entregas Fallidas.
2. El frontend solicita la primera página con los filtros seleccionados.
3. El backend valida el rol y recupera únicamente los despachos en `FALLIDO`.
4. El sistema incorpora a cada resultado sus indicadores de recepción, evidencia, pedido anulado, condición `NO_INTENTADO` y retorno atrasado cuando correspondan.
5. El frontend presenta el listado paginado y permite abrir el detalle o iniciar la confirmación de recepción de un paquete pendiente de retorno.

## 4. Reglas y validaciones

- La consulta no debe incluir despachos cuyo estado vigente sea distinto de `FALLIDO`.
- Cada fila debe mostrar como mínimo código operativo interno, fecha de la incidencia, motivo, número de intento sobre el máximo configurado, repartidor, recepción, disponibilidad de evidencia e indicador de pedido anulado.
- El estado de recepción se representa como `Pendiente de retorno` o `Recibido en centro`.
- Un fallo con motivo `NO_INTENTADO` debe identificarse como `No intentado` y distinguirse de un fallo que consumió un intento real.
- Un paquete se muestra como `Retorno atrasado` cuando el repartidor cerró su jornada y la recepción en el centro continúa pendiente.
- Los filtros por motivo, fecha y recepción pueden combinarse y siempre se aplican sobre despachos `FALLIDO`.
- Si no existen coincidencias, se muestra un estado vacío y no se incorporan registros de otros estados.
- Un usuario sin el rol requerido no recibe información operativa y obtiene `403 Forbidden`.
- El listado no expone el comentario interno del repartidor, la fotografía ni datos personales innecesarios; esos datos pertenecen al detalle autorizado.

## 5. Entradas, salidas e integraciones

### Entradas

- Página y tamaño de página.
- Filtro opcional por motivo del fallo.
- Rango opcional de fechas de la incidencia.
- Filtro opcional por recepción: todos, pendiente de retorno o recibido en centro.
- Identidad y roles obtenidos del JWT.

### Salidas

- Página de despachos fallidos con los campos e indicadores definidos en esta especificación.
- Metadatos de paginación.
- Estado vacío cuando no existen resultados.
- Error normalizado cuando la solicitud no está autorizada o sus filtros son inválidos.

### Integraciones

- F-03 proporciona el fallo, el motivo, el intento, el repartidor y la referencia de evidencia.
- F-02 registra la anulación del pedido que debe mostrarse como indicador.
- La información de jornada necesaria para identificar un retorno atrasado procede de F-05 mediante el mecanismo acordado por el módulo.
- La ruta, los parámetros y la forma de error se rigen exclusivamente por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Listado con incidencias

- **DADO** que existen despachos cuyo estado vigente es `FALLIDO`.
- **CUANDO** el Gestor abre la pantalla de Entregas Fallidas.
- **ENTONCES** el sistema muestra exclusivamente esos despachos con sus datos operativos, indicadores y paginación.

### CA-02. Aplicación de filtros

- **DADO** un conjunto de despachos fallidos con distintos motivos, fechas y estados de recepción.
- **CUANDO** el Gestor combina uno o más filtros.
- **ENTONCES** el sistema devuelve solo las coincidencias y conserva la restricción del estado `FALLIDO`.

### CA-03. Listado sin incidencias

- **DADO** que no existen despachos fallidos que coincidan con la consulta.
- **CUANDO** el Gestor abre o filtra el listado.
- **ENTONCES** el frontend muestra un estado vacío sin datos pertenecientes a otros estados.

### CA-04. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar el listado.
- **ENTONCES** el backend responde `403 Forbidden` y no expone información de los despachos.

### CA-05. Retorno atrasado

- **DADO** un despacho `FALLIDO` cuyo repartidor ya cerró su jornada y cuyo paquete no tiene recepción confirmada.
- **CUANDO** el Gestor consulta el listado.
- **ENTONCES** el resultado se identifica como `Retorno atrasado` junto al repartidor responsable.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Consultar el detalle completo, el historial o la fotografía de la incidencia.
- Confirmar la recepción física del paquete.
- Reprogramar o cerrar el despacho.
- Registrar el fallo en campo o cerrar la jornada del repartidor.

### Referencias

- [cite: 1] `funcionalidades/F-04-GestionEntregasFallidas.md`, RF-01, RF-06, RF-07 y CA-01 a CA-03, CA-14 y CA-18.
- [cite: 2] `integraciones/api-contract.md`, sección 11, API de F-04.
- [cite: 3] `disenio/funcionalidades/f-04.md`, Pantalla 1: Listado de Entregas Fallidas.
- [cite: 4] `overview.md`, integración de F-03, F-04 y F-05.
