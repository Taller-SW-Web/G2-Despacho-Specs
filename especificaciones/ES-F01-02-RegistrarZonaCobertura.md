# ES-F01-02: Registrar y editar una zona de cobertura

**Funcionalidad padre:** F-01 — Gestor de zonas geográficas y cotizador de envíos  
**Responsable:** Valqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho registre una nueva zona de cobertura y edite las existentes, delimitando su cobertura mediante distritos y códigos postales. La delimitación correcta de las zonas es la base de la fuente única de cobertura del módulo: de ella dependen las cotizaciones de los canales y la resolución de zona que consumen F-02 y F-05.

## 2. Actor y precondiciones

- El actor está autenticado con un JWT que incluye el rol `GESTOR_DESPACHO`.
- El catálogo de distritos y códigos postales de referencia está disponible para la selección.
- La operación se ejecuta contra las tablas propias de zonas de Gestión de Despachos.

## 3. Flujo principal

1. El Gestor abre el formulario de zona desde el catálogo.
2. Ingresa el nombre y selecciona al menos un distrito y, opcionalmente, códigos postales.
3. El frontend deshabilita la acción de guardar mientras falte el nombre o la delimitación.
4. El backend valida el rol, la unicidad del nombre y la ausencia de solapamiento con zonas activas.
5. El sistema persiste la zona con identificador único, estado elegido y marcas de auditoría, y devuelve el recurso creado.

## 4. Reglas y validaciones

- El nombre de la zona es obligatorio, no admite duplicados y se conserva entre 1 y 80 caracteres.
- Una zona debe conservar al menos un distrito o un código postal; una zona sin delimitación no se persiste.
- Un distrito o código postal no puede pertenecer a más de una zona en estado `ACTIVO`; el conflicto se detecta contra el estado de cada zona y no solo contra su identificador.
- Un conflicto de nombre, distrito o código postal produce `409 Conflict` con el detalle de la zona y del elemento en conflicto, y no persiste nada.
- Los datos inválidos del formulario producen `400 Bad Request` con el detalle de los campos afectados, y el frontend los marca junto al campo correspondiente.
- Editar una zona conserva su identificador y su historial de cambios; la edición nunca cambia su estado.
- Un editar no puede dejar la zona sin cobertura, y tampoco puede introducir un solapamiento con otra zona activa.
- La persistencia registra el usuario autenticado y la marca temporal del servidor en UTC.
- Un usuario sin el rol `GESTOR_DESPACHO` obtiene `403 Forbidden` y no expone información de configuración.
- La interfaz impide las acciones conocidas como inválidas, pero las reglas se vuelven a validar en el backend.

## 5. Entradas, salidas e integraciones

### Entradas

- Nombre de la zona.
- Distrito o distritos comprendidos.
- Códigos postales opcionales.
- Estado inicial elegido (`ACTIVO` o `INACTIVO`).
- Identidad y roles obtenidos del JWT.

### Salidas

- Zona persistida con identificador único, cobertura y estado.
- Confirmación de la operación y actualización del catálogo.
- Error normalizado ante datos inválidos, duplicidad o falta de permisos.

### Integraciones

- La operación no consulta a otros módulos: la delimitación pertenece a esta funcionalidad.
- Seguridad y Usuarios emite el JWT que habilita el acceso administrativo.
- La ruta, los cuerpos, las respuestas y los códigos de error se rigen exclusivamente por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Creación de una zona válida

- **DADO** que un usuario con rol `GESTOR_DESPACHO` ingresa el nombre de la zona, sus distritos y el estado Activo.
- **CUANDO** confirma la creación.
- **ENTONCES** el sistema registra la zona con identificador único y estado `ACTIVO`, la devuelve como recurso creado y la incluye en el catálogo.

### CA-02. Creación con nombre o cobertura duplicada

- **DADO** que el nombre, un distrito o un código postal ya están registrados en una zona activa.
- **CUANDO** se confirma la creación.
- **ENTONCES** el sistema responde `409 Conflict`, detalla la zona y el elemento en conflicto y no persiste la zona.

### CA-03. Creación sin delimitación

- **DADO** que el formulario no incluye ningún distrito ni código postal.
- **CUANDO** se intenta guardar.
- **ENTONCES** el sistema rechaza la operación y ni el frontend ni el backend permiten persistir una zona sin cobertura.

### CA-04. Edición de una zona existente

- **DADO** una zona existente con cobertura que no colisiona con otra zona activa.
- **CUANDO** el Gestor modifica su nombre o sus distritos y confirma.
- **ENTONCES** el sistema conserva su identificador, persiste los cambios con usuario y marca temporal, y la zona resuelve cobertura con su nueva delimitación.

### CA-05. Edición con conflicto de cobertura

- **DADO** que la edición asigna un distrito que pertenece a otra zona activa.
- **CUANDO** el Gestor confirma.
- **ENTONCES** el sistema responde `409 Conflict`, no persiste cambios parciales y la zona conserva su delimitación anterior.

### CA-06. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta registrar o editar una zona.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone información de configuración.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Cambiar el estado de una zona y sus efectos sobre despachos existentes.
- Configurar la tarifa de la zona.
- Dibujar polígonos, detectar solapamientos geográficos o almacenar geometrías.
- Resolver la cobertura de un destino para F-02, F-05 o los canales.

### Referencias

- [cite: 1] `funcionalidades/F-01-Gestor_ZonasGeograficas.md`, RF-01, CA-01, CA-03, CA-04 y CA-16.
- [cite: 2] `integraciones/api-contract.md`, secciones 3.3, 3.5 y 9.1.
- [cite: 3] `disenio/funcionalidades/f-01.md`, Pantalla 2: Formulario de Zona.
- [cite: 4] `disenio/SystemDesign/f-01-alta-fidelidad.md`, formulario de zona y estados de validación.
- [cite: 5] `arquitectura/modelo-datos.md`, tablas `zonas` y `zona_distritos`.
- [cite: 6] `overview.md`, sección 1.2 sobre fuentes únicas de cobertura.