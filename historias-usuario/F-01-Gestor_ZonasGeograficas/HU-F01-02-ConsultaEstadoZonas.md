# [HU-F01-02] Consulta y Control de Estado de las Zonas de Cobertura

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-01: Gestor de Zonas Geográficas y Cotizador de Envíos |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-01`, `sdd`, `zonas`, `panel`, `gestion` |
| **Responsable sugerido** | Valqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** consultar el listado paginado de zonas de cobertura con filtros por nombre, distrito y estado, y activar o desactivar coberturas según la operación  
**PARA** mantener actualizadas las áreas de atención logística y orientar la asignación de los despachos.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisito `RF-01`, Criterios `CA-15`, `CA-17`, `CA-13`).
- **Endpoints asociados:**
  - `GET /api/v1/zonas` (listar con filtros y paginación) y `GET /api/v1/zonas/{idZona}` (consultar detalle), definidos en el [contrato de Gestión, sección 3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas).
  - `PATCH /api/v1/zonas/{idZona}/estado` (activar o desactivar), definido en la sección 3.1 del mismo contrato.
  - Parámetros de consulta del listado: `pagina` (int, default 1), `limite` (int, default 10 o 20), `nombre` (string opcional), `distrito` (string opcional), `estado` (enum `ACTIVO` / `INACTIVO` opcional).
- **Rol requerido:** `GESTOR_DESPACHO` (autenticación JWT). Usuarios sin este rol deben recibir `403 Forbidden`.
- **Componentes de Frontend:**
  - Panel de Gestión de Zonas: listado paginado con filtros por nombre, distrito y estado, y acciones para activar o desactivar coberturas.
- **Reglas de negocio y visuales:**
  - La respuesta debe incluir paginación estándar: `paginaActual`, `totalPaginas`, `totalElementos` y la lista de zonas.
  - Cada fila debe mostrar: nombre de la zona, distritos comprendidos, códigos postales, tarifa vigente o la indicación "Sin tarifa", estado actual y última modificación.
  - Si no existen zonas o el filtro no arroja resultados, se debe mostrar un estado visual vacío amigable: *"No hay zonas de cobertura registradas"*.
  - Al activar o desactivar una cobertura se debe confirmar la acción y reflejar el cambio de estado en la lista.
  - Una activación que comparte un distrito o código postal con otra zona `ACTIVO` se rechaza con `409 Conflict` y la zona permanece `INACTIVO`.
  - Una desactivación deja la zona sin aceptar cotizaciones ni solicitudes nuevas, pero los despachos existentes conservan su zona.
- **Entidades de datos involucradas:** `zonas` (ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-15: Consulta del catálogo de zonas**
  - **DADO** que existen zonas registradas en distintos estados y con tarifas distintas.
  - **CUANDO** el Gestor abre el panel de zonas y aplica filtros por nombre, distrito y estado.
  - **ENTONCES** el sistema devuelve una página con las zonas que coinciden, mostrando nombre, distritos, códigos postales, tarifa vigente o la indicación de que no existe, estado y última modificación.

- [ ] **CA-17: Activación de una zona y conflicto de solapamiento**
  - **DADO** que una zona está en `INACTIVO` y sus distritos y códigos postales no pertenecen a ninguna otra zona activa.
  - **CUANDO** el Gestor la activa.
  - **ENTONCES** el sistema la cambia a `ACTIVO` y vuelve a atender cotizaciones y resoluciones de zona para su cobertura.
  - **DADO** que la zona por activar comparte un distrito o código postal con una zona `ACTIVO`.
  - **CUANDO** el Gestor intenta activarla.
  - **ENTONCES** el sistema responde `409 Conflict`, identifica la zona activa en conflicto y conserva el estado `INACTIVO`.

- [ ] **CA-13: Desactivación de una zona con despachos registrados**
  - **DADO** una zona con despachos registrados que aún no han sido entregados.
  - **CUANDO** el Gestor la desactiva.
  - **ENTONCES** la zona deja de aceptar nuevas cotizaciones y nuevas solicitudes, pero los despachos existentes conservan su zona y continúan su ciclo sin cambios, incluidas sus reprogramaciones.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Repositorio Spring Data JPA con consulta paginada (`Pageable`) y filtros por nombre, distrito y estado.
- [ ] Pruebas unitarias en backend (`JUnit 5 + Mockito`) verificando paginación, filtros y ordenamiento.
- [ ] Prueba de integración del `PATCH /api/v1/zonas/{idZona}/estado` verificando el cambio de estado y el `409 Conflict` ante solapamiento con otra zona activa.
- [ ] Pruebas de seguridad (`Spring Security Test`) verificando acceso con `GESTOR_DESPACHO` y rechazo `403` para otros roles o usuarios anónimos.
- [ ] Componente React de Panel de Gestión de Zonas con tabla responsive, filtros, controles de paginación y skeleton loaders durante la carga.
- [ ] Estado visual amigable cuando la lista está vacía implementado con Tailwind CSS.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
