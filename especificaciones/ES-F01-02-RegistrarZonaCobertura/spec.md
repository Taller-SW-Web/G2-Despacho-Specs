# ES-F01-02: Registrar y editar una zona de cobertura

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Gestor de Despacho

**UI:** Aplica; formulario de zona (Pantalla 2) de la aplicación administrativa.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación existente en la revisión `12d5041`; migrada al flujo SDD el 15/10/2026, conservando las reglas y los criterios CA-01 a CA-06.

## 1. Contexto y objetivo

El registro y la edición de zonas permiten delimitar la cobertura del centro de despacho mediante distritos y códigos postales. La delimitación correcta es la base de la fuente única de cobertura del módulo: de ella dependen la resolución de zona que consumen F-02 y F-05 y las cotizaciones de los canales. Esta especificación concreta RF-01 de la funcionalidad padre y no repite su alcance general [cite: 1].

## 2. Alcance

- Incluye: crear una zona con nombre, delimitación por distritos y códigos postales y estado inicial; editar el nombre o la delimitación de una zona existente; validar unicidad de nombre y ausencia de solapamiento entre zonas activas.
- Fuera de alcance: cambiar el estado de una zona (ES-F01-03); configurar su tarifa (ES-F01-04); resolver la cobertura de un destino para módulos o canales (ES-F01-05, ES-F01-06 y ES-F01-07); dibujar polígonos, detectar solapamientos geográficos o almacenar geometrías.

## 3. Actor, precondiciones y resultados

- Actor y autorización: el Gestor de Despacho autenticado con un JWT humano de rol `GESTOR_DESPACHO`, conforme a la sección 3.3 del contrato [cite: 2].
- Precondiciones: el catálogo de distritos y códigos postales de referencia está disponible para la selección; las operaciones se ejecutan contra las tablas propias de zonas de Gestión de Despachos.
- Disparador: el Gestor abre el formulario de zona desde el catálogo («Nueva zona» o «Editar»).
- Resultado exitoso: la zona queda persistida con identificador único, cobertura, estado y marcas de auditoría, y el catálogo se actualiza.
- Resultado ante rechazo: `409 Conflict` con el elemento en conflicto, `400 Bad Request` con el detalle de los campos inválidos o `403 Forbidden`; en ningún caso se persiste un cambio parcial.

## 4. Flujo principal y alternativas

1. El Gestor abre el formulario de zona desde el catálogo.
2. Ingresa el nombre y selecciona al menos un distrito y, opcionalmente, códigos postales.
3. El frontend deshabilita la acción de guardar mientras falte el nombre o la delimitación.
4. El backend valida el rol, la unicidad del nombre y la ausencia de solapamiento con zonas activas.
5. El sistema persiste la zona con identificador único, estado elegido y marcas de auditoría, y devuelve el recurso creado o actualizado.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Nombre o cobertura duplicada | El nombre, un distrito o un código postal ya pertenecen a una zona activa | `409 Conflict` con la zona y el elemento en conflicto; no persiste | CA-02, CA-05 |
| Sin delimitación | No se selecciona ningún distrito ni código postal | El frontend y el backend impiden guardar | CA-03 |
| Edición válida | La zona existe y la nueva cobertura no colisiona con otra zona activa | Conserva identificador y persiste los cambios | CA-04 |
| Acceso sin permisos | Usuario sin rol `GESTOR_DESPACHO` | `403 Forbidden` sin información de configuración | CA-06 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | El nombre es obligatorio, no admite duplicados y se conserva entre 1 y 80 caracteres. | F-01 CA-01 |
| RN-02 | Una zona debe conservar al menos un distrito o un código postal; una zona sin delimitación no se persiste. | F-01 CA-03, CA-16 |
| RN-03 | Un distrito o código postal no puede pertenecer a más de una zona `ACTIVO`; el conflicto se detecta contra el estado de cada zona, no solo contra su identificador. | F-01 CA-01 |
| RN-04 | Un conflicto de nombre, distrito o código postal produce `409 Conflict` con el detalle de la zona y del elemento en conflicto, y no persiste nada. | F-01 CA-04 |
| RN-05 | Los datos inválidos del formulario producen `400 Bad Request` con el detalle de los campos afectados, que el frontend marca junto al campo correspondiente. | F-01 CA-04 |
| RN-06 | Editar una zona conserva su identificador y su historial de cambios; la edición nunca cambia su estado. | F-01 CA-16 |
| RN-07 | Un editar no puede dejar la zona sin cobertura ni introducir un solapamiento con otra zona activa. | F-01 CA-03, CA-16 |
| RN-08 | La persistencia registra el usuario autenticado y la marca temporal del servidor en UTC. | F-01 CA-16 |
| RN-09 | Un usuario sin el rol `GESTOR_DESPACHO` obtiene `403 Forbidden` y no se expone información de configuración. | F-01 CA-04 |
| RN-10 | La interfaz impide las acciones conocidas como inválidas, pero las reglas se vuelven a validar en el backend. | F-01 CA-04 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `POST /api/v1/zonas` | Crear una zona | [Contrato §9.1](../../integraciones/api-contract.md#91-zonas-y-tarifas) |
| `GET /api/v1/zonas/{idZona}` | Recuperar una zona para edición | [Contrato §9.1](../../integraciones/api-contract.md#91-zonas-y-tarifas) |
| `PUT /api/v1/zonas/{idZona}` | Editar nombre o delimitación | [Contrato §9.1](../../integraciones/api-contract.md#91-zonas-y-tarifas) |
| Seguridad y Usuarios | Emite el JWT que habilita el acceso administrativo | Contrato §§3.3 y 8 |
| Catálogo de distritos y códigos postales | Fuente de selección de la delimitación | [Modelo de datos](../../arquitectura/modelo-datos.md), tabla `distrito` |

Los cuerpos, respuestas y códigos de error se consultan en el contrato central; no se definen aquí [cite: 2].

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

## 7. UI, backend y requisitos no funcionales

- UI: aplica. La interacción, los estados, la accesibilidad y los criterios de UI se detallan en [ui.md](./ui.md).
- Backend: alta y edición autorizadas sobre las tablas propias de zonas; valida unicidad y solapamiento antes de persistir; no publica eventos.
- Requisitos no funcionales: las operaciones administrativas requieren JWT de rol `GESTOR_DESPACHO`; la identidad del ejecutor y la marca temporal proceden del servidor, nunca de un campo libre del cliente; las marcas se persisten en UTC y se presentan en `America/Lima`.
- Pendientes: la conciliación entre `zona_distritos` y `zonas_distritos`, y el detalle del cuerpo de creación y edición se registran en [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes); su resolución precede a la integración real.

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración y UI | Alta con delimitación y estado Activo; verificación del recurso creado. |
| CA-02 | Integración y UI | Nombre, distrito o código postal ya pertenecientes a una zona activa. |
| CA-03 | UI e integración | Formulario sin distritos ni códigos postales; intento directo contra la API. |
| CA-04 | Integración y UI | Zona editable cuya nueva delimitación no colisiona. |
| CA-05 | Integración y UI | Edición que asigna un distrito de otra zona activa. |
| CA-06 | Seguridad e integración | Usuario con otro rol y solicitud sin token. |

- [ ] Los criterios CA-01 a CA-06 y los criterios de UI cuentan con resultados comprobables en [evidence.md](./evidence.md).
- [ ] El contrato de los cuerpos de creación y edición está definido y verificado.
- [ ] La revisión del alcance y los commits de implementación están enlazados.

La descomposición está en [tasks.md](./tasks.md) y los resultados se registrarán en [evidence.md](./evidence.md); todas las comprobaciones de comportamiento están pendientes.

## 9. Referencias

1. [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-01, CA-01, CA-03, CA-04 y CA-16.
2. [cite: 2] [Contrato de API](../../integraciones/api-contract.md), secciones 3.3, 3.5 y 9.1.
3. [cite: 3] [Diseño de F-01](../../disenio/funcionalidades/f-01.md), Pantalla 2; [alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md), formulario de zona.
4. [cite: 4] [Modelo de datos](../../arquitectura/modelo-datos.md), tablas `zonas`, `zona_distritos` y `distrito`.
5. Archivos de esta especificación: [ui.md](./ui.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
