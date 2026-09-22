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

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisito `RF-01`, Criterio `CA-02`).
- **Endpoints asociados:**
  - `GET /api/v1/zonas` (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md)).
  - Parámetros de consulta: `pagina` (int, default 1), `limite` (int, default 10 o 20), `nombre` (string opcional), `distrito` (string opcional), `estado` (enum `ACTIVO` / `INACTIVO` opcional).
- **Roles requeridos:** `ADMIN` o `GESTOR_DESPACHO` (autenticación JWT). Usuarios sin estos roles deben recibir `403 Forbidden`.
- **Componentes de Frontend:**
  - Panel de Gestión de Zonas: listado paginado con filtros por nombre, distrito y estado, y acciones para activar o desactivar coberturas.
- **Reglas de negocio y visuales:**
  - La respuesta debe incluir paginación estándar: `paginaActual`, `totalPaginas`, `totalElementos` y la lista de zonas.
  - Cada fila debe mostrar: identificador, nombre de la zona, distritos comprendidos, código postal representativo y estado actual.
  - Si no existen zonas o el filtro no arroja resultados, se debe mostrar un estado visual vacío amigable: *"No hay zonas de cobertura registradas"*.
  - Al activar o desactivar una cobertura se debe confirmar la acción y reflejar el cambio de estado en la lista.
- **Entidades de datos involucradas:** `zonas` (ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-02: Consulta de cobertura para dirección fuera de rango**
  - **DADO** que se consulta la cobertura para un distrito no registrado en ninguna zona activa (ej. provincia no cubierta).
  - **CUANDO** el cotizador evalúa la dirección.
  - **ENTONCES** el sistema retorna código `200 OK` con bandera `coberturaDisponible: false` y el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura".

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Repositorio Spring Data JPA con consulta paginada (`Pageable`) y filtros por nombre, distrito y estado.
- [ ] Pruebas unitarias en backend (`JUnit 5 + Mockito`) verificando paginación, filtros y ordenamiento.
- [ ] Pruebas de seguridad (`Spring Security Test`) verificando acceso con rol `ADMIN` o `GESTOR_DESPACHO` y rechazo `403` para otros roles o usuarios anónimos.
- [ ] Componente React de Panel de Gestión de Zonas con tabla responsive, filtros, controles de paginación y skeleton loaders durante la carga.
- [ ] Estado visual amigable cuando la lista está vacía implementado con Tailwind CSS.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.