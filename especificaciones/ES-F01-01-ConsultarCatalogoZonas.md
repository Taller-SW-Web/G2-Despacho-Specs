# ES-F01-01: Consultar el catálogo de zonas de cobertura

**Funcionalidad padre:** F-01 — Gestor de zonas geográficas y cotizador de envíos  
**Responsable:** Valqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho consulte el catálogo de zonas de cobertura con filtros por nombre, distrito y estado, y visualice para cada zona su cobertura, su tarifa vigente y su última modificación. El catálogo es el punto de entrada del panel de gestión y permite orientar la decisión sobre qué zonas activar, editar o tarifar.

## 2. Actor y precondiciones

- El actor está autenticado con un JWT que incluye el rol `GESTOR_DESPACHO`.
- Las zonas y sus tarifas vigentes se encuentran persistidas por esta misma funcionalidad.
- La consulta es paginada y admite filtros opcionales por nombre, distrito y estado (`ACTIVO` o `INACTIVO`).

## 3. Flujo principal

1. El Gestor ingresa a la pantalla "Zonas y Tarifas" desde la barra lateral.
2. El frontend solicita la primera página del catálogo con los filtros seleccionados.
3. El backend valida el rol y recupera las zonas que coinciden con los filtros.
4. El sistema incorpora a cada resultado sus distritos, códigos postales, la tarifa vigente o la ausencia de esta y la última modificación.
5. El frontend presenta la tabla paginada y habilita las acciones de edición, tarifas y cambio de estado.

## 4. Reglas y validaciones

- El listado debe mostrar como mínimo nombre de la zona, distritos comprendidos, códigos postales, tarifa vigente o la indicación "Sin tarifa", estado y última modificación.
- Los filtros por nombre, distrito y estado pueden combinarse y siempre se aplican antes de paginar.
- Solo se consultan zonas; esta especificación no crea, edita ni cambia el estado de ninguna.
- Una zona `INACTIVO` se muestra atenuada y conserva sus acciones de edición y activación.
- Una zona activa sin tarifa vigente se identifica con una advertencia visible, porque no podrá producir costo de envío.
- Si no existen zonas, o si los filtros no devuelven coincidencias, el frontend muestra un estado vacío diferenciado y no incorpora datos de otras consultas.
- La paginación informa el total de registros y la página actual.
- Un usuario sin el rol requerido obtiene `403 Forbidden` y no recibe información de configuración.
- El catálogo no expone información de los canales que cotizaron con la zona ni los límites aplicados a cada consumidor.

## 5. Entradas, salidas e integraciones

### Entradas

- Número de página y tamaño de página.
- Filtro opcional por nombre de zona.
- Filtro opcional por distrito.
- Filtro opcional por estado.
- Identidad y roles obtenidos del JWT.

### Salidas

- Página de zonas con cobertura, tarifa vigente o ausencia de esta, estado y última modificación.
- Metadatos de paginación.
- Estado vacío cuando no existen resultados.
- Error normalizado cuando la solicitud no está autorizada o sus parámetros son inválidos.

### Integraciones

- Los datos proceden exclusivamente de las tablas propias de zonas y tarifas de Gestión de Despachos; esta especificación no consulta a otros módulos.
- Seguridad y Usuarios emite el JWT que habilita el acceso administrativo.
- La ruta, los parámetros de consulta y la forma de error se rigen exclusivamente por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Catálogo con filtros

- **DADO** que existen zonas registradas en distintos estados y con tarifas distintas.
- **CUANDO** el Gestor abre la pantalla y aplica uno o más filtros.
- **ENTONCES** el sistema devuelve únicamente las zonas que coinciden, con su cobertura, su tarifa vigente o la indicación de ausencia, su estado y su última modificación, junto con los metadatos de paginación.

### CA-02. Catálogo sin resultados

- **DADO** que no existen zonas registradas, o que los filtros aplicados no devuelven coincidencias.
- **CUANDO** el Gestor abre o filtra el catálogo.
- **ENTONCES** el frontend muestra un estado vacío con la acción para limpiar filtros o registrar una nueva zona, sin incorporar datos ajenos a la consulta.

### CA-03. Zona sin tarifa vigente

- **DADO** que una zona se encuentra en `ACTIVO` y no tiene tarifa vigente.
- **CUANDO** el Gestor consulta el catálogo.
- **ENTONCES** la fila se identifica con una advertencia de zona sin tarifa configurada.

### CA-04. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`, o una solicitud sin token.
- **CUANDO** intenta consultar el catálogo.
- **ENTONCES** el backend responde `403 Forbidden` o `401 Unauthorized` según corresponda y no expone información de configuración.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Registrar, editar, activar o desactivar zonas.
- Configurar o consultar la estructura de una tarifa.
- Evaluar la cobertura de un destino concreto.
- Exponer auditoría de cambios o el historial de tarifas sustituidas.

### Referencias

- [cite: 1] `funcionalidades/F-01-Gestor_ZonasGeograficas.md`, RF-01, CA-04 y CA-15.
- [cite: 2] `integraciones/api-contract.md`, secciones 3.3 y 9.1.
- [cite: 3] `disenio/funcionalidades/f-01.md`, Pantalla 1: Panel de Gestión de Zonas.
- [cite: 4] `disenio/SystemDesign/f-01-alta-fidelidad.md`, tabla de zonas y estados.
- [cite: 5] `arquitectura/modelo-datos.md`, tablas `zonas`, `zona_distritos` y `tarifas_zona`.
- [cite: 6] `overview.md`, sección 4 sobre el rol `GESTOR_DESPACHO`.