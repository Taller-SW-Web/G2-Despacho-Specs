# ES-F01-01: Consultar el catálogo de zonas de cobertura

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Gestor de Despacho

**UI:** Aplica; Panel de Gestión de Zonas (Pantalla 1) de la aplicación administrativa.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación existente en la revisión `12d5041`; migrada al flujo SDD el 15/10/2026, conservando las reglas y los criterios CA-01 a CA-04.

## 1. Contexto y objetivo

El catálogo es el punto de entrada del panel de gestión de zonas. Permite al Gestor de Despacho consultar las zonas de cobertura con filtros por nombre, distrito y estado, y reconocer para cada una su delimitación, su tarifa vigente o la ausencia de esta, su estado y su última modificación. Con esa vista el Gestor orienta las decisiones de editar, tarifar o activar y desactivar. Esta especificación concreta el requisito RF-01 de la funcionalidad padre y no repite su alcance general [cite: 1].

## 2. Alcance

- Incluye: consulta paginada del catálogo de zonas con filtros opcionales por nombre, distrito y estado; exposición de la cobertura, la tarifa vigente o su ausencia, el estado y la última modificación de cada zona; estado vacío diferenciado y autorización por rol.
- Fuera de alcance: registrar, editar, activar o desactivar zonas (ES-F01-02 y ES-F01-03); configurar o consultar la estructura de una tarifa (ES-F01-04); evaluar la cobertura de un destino concreto (ES-F01-05 y ES-F01-06); exponer auditoría de cambios o el historial de tarifas sustituidas (ES-F01-08).

## 3. Actor, precondiciones y resultados

- Actor y autorización: el Gestor de Despacho autenticado con un JWT humano de rol `GESTOR_DESPACHO`, conforme a la sección 3.3 del contrato [cite: 2].
- Precondiciones: las zonas y sus tarifas vigentes están persistidas por esta misma funcionalidad; las operaciones se ejecutan contra las tablas propias de zonas de Gestión de Despachos.
- Disparador: el Gestor abre la pantalla «Zonas y Tarifas» desde la barra lateral.
- Resultado exitoso: una página de zonas con nombre, distritos, códigos postales, tarifa vigente o la indicación «Sin tarifa», estado y última modificación, junto con los metadatos de paginación.
- Resultado ante rechazo: `403 Forbidden` sin información de configuración; los parámetros inválidos se informan con el formato de error central sin incorporar datos ajenos a la consulta.

## 4. Flujo principal y alternativas

1. El Gestor ingresa a la pantalla «Zonas y Tarifas» desde la barra lateral.
2. El frontend solicita la primera página del catálogo con los filtros seleccionados.
3. El backend valida el rol y recupera las zonas que coinciden con los filtros.
4. El sistema incorpora a cada resultado sus distritos, códigos postales, la tarifa vigente o su ausencia y la última modificación.
5. El frontend presenta la tabla paginada y habilita las acciones de edición, tarifas y cambio de estado.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Catálogo sin resultados | No hay zonas o los filtros no devuelven coincidencias | Estado vacío diferenciado con acción para limpiar filtros o registrar una zona; sin datos de otras consultas | CA-02 |
| Zona activa sin tarifa vigente | Una zona `ACTIVO` no tiene tarifa vigente | La fila se identifica con una advertencia de zona sin tarifa configurada | CA-03 |
| Acceso sin permisos | Usuario sin rol `GESTOR_DESPACHO` o solicitud sin token | `403 Forbidden` o `401 Unauthorized`; sin información de configuración | CA-04 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | El listado muestra como mínimo nombre, distritos, códigos postales, tarifa vigente o «Sin tarifa», estado y última modificación. | F-01 CA-15 y §4.3 |
| RN-02 | Los filtros por nombre, distrito y estado pueden combinarse y se aplican antes de paginar. | F-01 CA-15 |
| RN-03 | Solo se consultan zonas; esta especificación no crea, edita ni cambia el estado de ninguna. | Alcance de esta especificación |
| RN-04 | Una zona `INACTIVO` se muestra atenuada y conserva sus acciones de edición y activación. | Diseño F-01, Pantalla 1 |
| RN-05 | Una zona activa sin tarifa vigente se identifica con una advertencia visible, porque no podrá producir costo de envío. | F-01 CA-23 y diseño F-01 |
| RN-06 | Si no hay zonas o no hay coincidencias, se muestra un estado vacío diferenciado sin incorporar datos de otras consultas. | F-01 CA-15 |
| RN-07 | La paginación informa el total de registros y la página actual. | F-01 CA-15 |
| RN-08 | Un usuario sin el rol requerido obtiene `403 Forbidden` y no recibe información de configuración. | F-01 CA-04 |
| RN-09 | El catálogo no expone los canales que cotizaron con la zona ni los límites aplicados a cada consumidor. | F-01 §3 y §9 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `GET /api/v1/zonas` | Listar zonas, con filtros y paginación | [Gestión §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas) |
| Seguridad y Usuarios | Emite el JWT que habilita el acceso administrativo | Contrato externo §§3.3 y 8 |
| Tablas `zonas`, `zonas_distritos`, `zonas_codigos_postales` y `tarifas_zona` | Fuente del catálogo; códigos postales desde la relación canónica | [Modelo de datos](../../arquitectura/modelo-datos.md), §3.1 |

Los parámetros exactos de filtros, paginación y el DTO de respuesta se consultan en el contrato de Gestión y en los pendientes del plan; no se definen aquí [cite: 2].

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

## 7. UI, backend y requisitos no funcionales

- UI: aplica. La interacción, los estados, la accesibilidad y los criterios de UI se detallan en [ui.md](./ui.md).
- Backend: consulta autorizada de solo lectura sobre las tablas propias de zonas y tarifas; no crea, edita ni cambia estados, y no publica eventos.
- Requisitos no funcionales: el catálogo no expone datos de otros módulos ni los límites de los canales; las operaciones administrativas requieren JWT de rol `GESTOR_DESPACHO`; las fechas se presentan en la zona operativa `America/Lima` según el modelo de datos.
- Pendientes: los parámetros de filtros y paginación y el DTO del listado se registran en [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes); su resolución precede a la integración real.

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración y UI | Zonas en distintos estados, con y sin tarifa; más de una página; filtros combinados. |
| CA-02 | Integración y UI | Sin zonas y con filtros sin coincidencias; existen zonas de otros estados. |
| CA-03 | Integración y UI | Zona `ACTIVO` sin tarifa vigente junto a otras con tarifa. |
| CA-04 | Seguridad e integración | Usuario con otro rol y solicitud sin token; vista con datos cargados antes del rechazo. |

- [ ] Los criterios CA-01 a CA-04 y los criterios de UI cuentan con resultados comprobables en [evidence.md](./evidence.md).
- [ ] El contrato y los DTO del listado están definidos y verificados.
- [ ] La revisión del alcance y los commits de implementación están enlazados.

La descomposición está en [tasks.md](./tasks.md) y los resultados se registrarán en [evidence.md](./evidence.md); todas las comprobaciones de comportamiento están pendientes.

## 9. Referencias

1. [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-01, CA-04 y CA-15.
2. [cite: 2] [Contrato de Gestión, sección 3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas); [convenciones compartidas](../../integraciones/api-contract.md#3-convenciones-comunes), secciones 3.3 y 3.5.
3. [cite: 3] [Diseño de F-01](../../disenio/funcionalidades/f-01.md), Pantalla 1; [alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md).
4. [cite: 4] [Modelo de datos](../../arquitectura/modelo-datos.md), tablas `zonas`, `zonas_distritos`, `zonas_codigos_postales` y `tarifas_zona`.
5. Archivos de esta especificación: [ui.md](./ui.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
