# ES-F01-03: Activar y desactivar una zona de cobertura

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Gestor de Despacho

**UI:** Aplica; confirmación de desactivación de zona (Pantalla 4) de la aplicación administrativa.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación existente en la revisión `12d5041`; migrada al flujo SDD el 15/10/2026, conservando las reglas y los criterios CA-01 a CA-06.

## 1. Contexto y objetivo

El cambio de estado retira o devuelve una zona de la cobertura efectiva del módulo. La activación reinserta la zona en la cobertura y vuelve a atender cotizaciones y resoluciones para su delimitación; la desactivación la retira de nuevas cotizaciones y solicitudes sin alterar los despachos ya asociados a ella. Esta especificación concreta RF-01 de la funcionalidad padre y no repite su alcance general [cite: 1].

## 2. Alcance

- Incluye: activar una zona `INACTIVO` sin conflicto de cobertura; desactivar una zona `ACTIVO`; verificación de idempotencia por estado y de control de versión ante operaciones concurrentes.
- Fuera de alcance: registrar o editar la cobertura (ES-F01-02); configurar la tarifa (ES-F01-04); reasignar, reprogramar o cancelar despachos asociados a una zona desactivada; notificar a F-02, F-05 o a los canales el cambio de estado.

## 3. Actor, precondiciones y resultados

- Actor y autorización: el Gestor de Despacho autenticado con un JWT humano de rol `GESTOR_DESPACHO`, conforme a la sección 3.3 del contrato [cite: 2].
- Precondiciones: la zona existe con su delimitación persistida por esta misma funcionalidad; los despachos asociados conservan su identificador de zona aunque la zona se desactive.
- Disparador: el Gestor elige la acción de activar o desactivar desde el catálogo, y confirma en el modal de advertencia.
- Resultado exitoso: la zona queda en el estado solicitado, con el usuario y la marca temporal registrados; el catálogo se actualiza.
- Resultado ante rechazo: `409 Conflict` por solapamiento o por versión concurrente (la zona conserva su estado), `403 Forbidden` por rol, o el estado vigente si ya estaba en el estado solicitado sin generar cambio.

## 4. Flujo principal y alternativas

1. El Gestor selecciona la acción de activar o desactivar desde el catálogo.
2. El frontend muestra la confirmación con el efecto esperado sobre cotizaciones y solicitudes.
3. El backend valida el rol y el estado actual de la zona.
4. En una activación, el sistema verifica que la cobertura no colisione con otra zona activa.
5. El sistema cambia el estado de la zona, registra el usuario y la marca temporal, y confirma la operación.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Activación con conflicto de solapamiento | La zona comparte distrito o código postal con otra zona `ACTIVO` | `409 Conflict` con la zona activa en conflicto; permanece `INACTIVO` | CA-02 |
| Desactivación con despachos registrados | La zona activa tiene despachos no entregados | Deja de aceptar cotizaciones y solicitudes nuevas; los despachos existentes conservan su zona y su ciclo | CA-03 |
| Repetición de la misma operación | La zona ya está en el estado solicitado | Responde el estado vigente sin cambio ni auditoría adicional | CA-04 |
| Cambios concurrentes | Dos solicitudes simultáneas sobre la misma zona | Solo una se aplica; la otra recibe `409 Conflict` con el estado vigente | CA-05 |
| Acceso sin permisos | Usuario sin rol `GESTOR_DESPACHO` | `403 Forbidden` sin información de configuración | CA-06 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Los únicos estados de una zona son `ACTIVO` e `INACTIVO`. | F-01 CA-17 |
| RN-02 | Solo se cotiza y solo se resuelve zona para destinos incluidos en zonas `ACTIVO`. | F-01 CA-13, CA-17 |
| RN-03 | Una zona desactivada deja de aceptar nuevas cotizaciones y nuevas solicitudes de despacho. | F-01 CA-13 |
| RN-04 | Los despachos ya registrados en la zona desactivada conservan su zona y continúan su ciclo sin cambios, incluidas sus reprogramaciones. | F-01 CA-13 |
| RN-05 | Una zona no puede activarse si comparte distrito o código postal con una zona `ACTIVO`; el conflicto produce `409 Conflict` y la zona permanece `INACTIVO`. | F-01 CA-17 |
| RN-06 | Si la zona ya está en el estado solicitado, el sistema responde el estado vigente sin cambio ni auditoría adicional. | F-01 CA-17 |
| RN-07 | La operación es idempotente por zona y estado: repetirla no produce duplicados. | F-01 CA-17 |
| RN-08 | El cambio de estado se valida con control de versión para que dos operaciones simultáneas no se pisen. | F-01 CA-17 |
| RN-09 | El frontend nunca ejecuta la desactivación directamente desde la tabla: siempre requiere la confirmación advertida. | Diseño F-01, Pantalla 4 |
| RN-10 | Un usuario sin el rol `GESTOR_DESPACHO` obtiene `403 Forbidden` y no se expone información de configuración. | F-01 CA-04 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `PATCH /api/v1/zonas/{idZona}/estado` | Cambiar el estado de la zona | [Contrato §9.1](../../integraciones/api-contract.md#91-zonas-y-tarifas) |
| Seguridad y Usuarios | Emite el JWT que habilita el acceso administrativo | Contrato §§3.3 y 8 |
| Transiciones de estado de zonas | Se rige por el flujo definido en el contrato | Contrato [§14](../../integraciones/api-contract.md#14-flujos-de-estado-y-trazabilidad) |
| Tablas `zonas` y relación con `despachos` | Estado de la zona y despachos asociados | [Modelo de datos](../../arquitectura/modelo-datos.md), §3.1 |

La operación no publica eventos: F-02 y los canales observan el efecto a través de la resolución de zona y la cotización [cite: 2].

## 6. Criterios de aceptación

### CA-01. Activación sin conflicto

- **DADO** una zona en `INACTIVO` cuyos distritos y códigos postales no pertenecen a otra zona activa.
- **CUANDO** el Gestor la activa.
- **ENTONCES** el sistema la cambia a `ACTIVO` y vuelve a atender cotizaciones y resoluciones de zona para su cobertura.

### CA-02. Activación con conflicto de solapamiento

- **DADO** una zona en `INACTIVO` que comparte un distrito o código postal con una zona `ACTIVO`.
- **CUANDO** el Gestor intenta activarla.
- **ENTONCES** el sistema responde `409 Conflict`, identifica la zona activa en conflicto y conserva el estado `INACTIVO`.

### CA-03. Desactivación de una zona con despachos registrados

- **DADO** una zona activa con despachos registrados que aún no han sido entregados.
- **CUANDO** el Gestor la desactiva.
- **ENTONCES** la zona deja de aceptar cotizaciones y solicitudes nuevas, y los despachos existentes conservan su zona y continúan su ciclo, incluidas sus reprogramaciones.

### CA-04. Repetición de la misma operación

- **DADO** que la zona ya se encuentra en el estado solicitado.
- **CUANDO** el Gestor repite la acción.
- **ENTONCES** el sistema responde con el estado vigente sin generar un cambio adicional ni una auditoría duplicada.

### CA-05. Cambios concurrentes

- **DADO** dos solicitudes simultáneas de cambio de estado sobre la misma zona.
- **CUANDO** ambas se procesan.
- **ENTONCES** solo una se aplica y la otra recibe `409 Conflict` con el estado vigente.

### CA-06. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta cambiar el estado de una zona.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone información de configuración.

## 7. UI, backend y requisitos no funcionales

- UI: aplica. La confirmación de desactivación y los estados de la interacción se detallan en [ui.md](./ui.md).
- Backend: cambio de estado autorizado, idempotente y con control de versión; no publica eventos ni altera despachos existentes.
- Requisitos no funcionales: las operaciones administrativas requieren JWT de rol `GESTOR_DESPACHO`; la identidad y la marca temporal proceden del servidor en UTC y se presentan en `America/Lima`.
- Pendientes: el mecanismo de control de versión, dado que `zonas` no define una columna de versión en el modelo, y el formato del `409` se registran en [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración | Zona `INACTIVO` sin solapamiento; verificación de cobertura posterior. |
| CA-02 | Integración | Zona `INACTIVO` que comparte cobertura con otra zona `ACTIVO`. |
| CA-03 | Integración e impacto | Zona activa con despachos no entregados; comprobación de sus reprogramaciones. |
| CA-04 | Integración e idempotencia | Repetición de la misma operación; conteo de auditorías. |
| CA-05 | Integración y concurrencia | Dos solicitudes simultáneas sobre la misma zona. |
| CA-06 | Seguridad e integración | Usuario con otro rol y solicitud sin token. |

- [ ] Los criterios CA-01 a CA-06 y los criterios de UI cuentan con resultados comprobables en [evidence.md](./evidence.md).
- [ ] El mecanismo de control de versión y el contrato del `409` están definidos y verificados.
- [ ] La revisión del alcance y los commits de implementación están enlazados.

La descomposición está en [tasks.md](./tasks.md) y los resultados se registrarán en [evidence.md](./evidence.md); todas las comprobaciones de comportamiento están pendientes.

## 9. Referencias

1. [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-01, CA-04, CA-13 y CA-17.
2. [cite: 2] [Contrato de API](../../integraciones/api-contract.md), secciones 3.3, 9.1 y 14.
3. [cite: 3] [Diseño de F-01](../../disenio/funcionalidades/f-01.md), Pantalla 4; [alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md), modal de desactivación.
4. [cite: 4] [Modelo de datos](../../arquitectura/modelo-datos.md), columna `estado` de `zonas` y relaciones con `despachos`.
5. Archivos de esta especificación: [ui.md](./ui.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
