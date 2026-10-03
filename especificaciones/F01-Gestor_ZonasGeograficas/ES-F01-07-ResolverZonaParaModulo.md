# ES-F01-07: Resolver la zona de un destino para el módulo

**Funcionalidad padre:** F-01 — Gestor de zonas geográficas y cotizador de envíos  
**Responsable:** Valqui  
**Estado:** Borrador  
**Actor principal:** Programación y asignación (F-02)

## 1. Objetivo

Determinar qué zona de cobertura activa contiene un destino y entregar esa resolución a las funcionalidades que la necesitan. F-02 la utiliza al crear un despacho para asociarle su zona o para rechazar el destino, y F-05 la utiliza para asignar la zona de trabajo de un repartidor en su jornada. Al ser F-01 la fuente única de cobertura del módulo, ninguna otra funcionalidad mantiene reglas propias de cobertura.

## 2. Actor y precondiciones

- El consumidor es una funcionalidad interna del módulo que actúa con identidad de servicio.
- El destino se identifica con `distrito`, `codigoPostal` o ambos.
- Las zonas y su delimitación se encuentran persistidas por esta misma funcionalidad.
- El destino puede o no estar cubierto; ambos resultados son respuestas válidas.

## 3. Flujo principal

1. F-02 recibe una solicitud de despacho o F-05 prepara la asignación de una jornada y obtiene el destino.
2. El consumidor solicita la resolución de zona con los datos del destino.
3. El backend busca la zona en estado `ACTIVO` que contiene el distrito o el código postal.
4. El sistema devuelve el identificador y el nombre de la zona, junto con los datos normalizados del destino.
5. El consumidor asocia la zona a su operación o declara que el destino no tiene cobertura.

## 4. Reglas y validaciones

- Solo las zonas en estado `ACTIVO` resuelven cobertura; una zona `INACTIVO` se trata como si no existiera.
- Un destino no cubierto se responde `200 OK` con `coberturaDisponible: false`, sin zona y con el mensaje de destino fuera de cobertura.
- La resolución no crea, edita ni cambia el estado de ninguna zona ni de ningún despacho.
- La zona devuelta es la vigente en el momento de la resolución; un cambio posterior de estado no modifica los registros ya asociados.
- La resolución no aplica tarifas ni calcula costos: esos datos corresponden al motor de cotización de ES-F01-06.
- El consumidor no puede forzar una zona distinta de la que resulta de la cobertura, ni declarar cobertura cuando el sistema la niega.
- La resolución debe ser estable para el mismo destino mientras la configuración no cambie, de modo que F-02 y F-05 observen la misma zona.
- El límite de solicitudes por consumidor se aplica también a esta operación interna.
- Un destino sin `distrito` ni `codigoPostal` identificables no puede resolverse y se rechaza con `400 Bad Request`.

## 5. Entradas, salidas e integraciones

### Entradas

- Datos del destino: `distrito` y, opcionalmente, `codigoPostal` y `direccion`.
- Identidad de servicio del consumidor interno.

### Salidas

- Identificador y nombre de la zona que cubre el destino, o la declaración de que no existe cobertura.
- Datos normalizados del destino utilizados en la resolución.
- Error normalizado cuando el destino no es identificable.

### Integraciones

- F-02 consume la resolución al crear un despacho y rechaza los destinos sin cobertura.
- F-05 consume el catálogo de zonas activas para asignar la zona de trabajo del repartidor.
- El mecanismo concreto por el que F-05, que pertenece al microservicio de Operación de Reparto y Flota, accede a esta información es un acuerdo pendiente de documentar en `integraciones/api-contract.md` [cite: 2].
- La zona es propiedad de Gestión de Despachos; ningún consumidor accede a su base de datos.

## 6. Criterios de aceptación

### CA-01. Resolución de un destino cubierto

- **DADO** una solicitud de despacho con destino en San Isidro, que pertenece a "Lima Centro".
- **CUANDO** F-02 solicita la resolución de zona.
- **ENTONCES** el sistema devuelve el identificador y el nombre de "Lima Centro" y F-02 los asocia al despacho.

### CA-02. Resolución de un destino sin cobertura

- **DADO** un destino cuyo distrito o código postal no pertenece a ninguna zona activa.
- **CUANDO** el consumidor solicita la resolución.
- **ENTONCES** el sistema responde `200 OK` con `coberturaDisponible: false`, sin zona y con el mensaje de destino fuera de cobertura.

### CA-03. Destino cubierto por una zona desactivada

- **DADO** un destino que solo pertenece a zonas en estado `INACTIVO`.
- **CUANDO** el consumidor solicita la resolución.
- **ENTONCES** el sistema lo declara sin cobertura, porque la desactivación retira la zona de la cobertura efectiva.

### CA-04. Destino no identificable

- **DADO** una solicitud que no informa `distrito` ni `codigoPostal`.
- **CUANDO** el consumidor solicita la resolución.
- **ENTONCES** el sistema responde `400 Bad Request` y no devuelve una zona por defecto.

### CA-05. Zona desactivada con despachos existentes

- **DADO** una zona desactivada con despachos ya registrados.
- **CUANDO** se consulta la resolución de uno de esos destinos.
- **ENTONCES** los despachos existentes conservan la zona con la que fueron creados, aunque la zona ya no resuelva cobertura para destinos nuevos.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Calcular costo, plazo o fecha estimada de entrega.
- Crear, editar, activar o desactivar zonas y sus tarifas.
- Registrar o reasignar despachos, y abrir o cerrar jornadas.
- Definir la ruta interna o la comunicación entre microservicios que entrega esta resolución.

### Referencias

- [cite: 1] `funcionalidades/F-01-Gestor_ZonasGeograficas.md`, RF-04, CA-02, CA-12 y CA-13.
- [cite: 2] `integraciones/api-contract.md`, secciones 3.2, 3.4, 9.1 y 13.
- [cite: 3] `arquitectura/modelo-datos.md`, tablas `zonas`, `zona_distritos` y `asignaciones_diarias`.
- [cite: 4] `overview.md`, secciones 3.1 y 3.2 sobre relaciones entre F-01, F-02 y F-05.
- [cite: 5] `arquitectura/macroproceso-despacho.md`, solicitud de despacho y resolución de zona.