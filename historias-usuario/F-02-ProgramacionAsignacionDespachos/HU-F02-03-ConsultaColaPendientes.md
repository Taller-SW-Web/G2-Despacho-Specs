# [HU-F02-03] Consulta y Visualización de la Cola de Despachos Pendientes

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-02`, `sdd`, `cola-pendientes`, `dashboard` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** consultar la cola de pedidos pendientes de entrega mediante una tabla paginada y filtrable en el dashboard administrativo  
**PARA** evaluar el volumen de envíos por asignar, priorizar los pedidos críticos y balancear la carga operativa diaria.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-02`, Criterios `CA-04`, `CA-05`, `CA-06`).
- **Endpoints asociados:**
  - `GET /api/v1/despachos/pendientes` (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md)).
  - Parámetros de consulta: `pagina` (int, default 1), `limite` (int, default 10 o 20), `zona` (string opcional), `ordenarPor` (enum: `FECHA_LIMITE`, `FECHA_CREACION`, `PESO`).
- **Roles requeridos:** `GESTOR_DESPACHO` (autenticación JWT). Usuarios sin este rol deben recibir `403 Forbidden`.
- **Reglas de negocio y visuales:**
  - Solo se listan registros cuyo estado actual sea exactamente `PENDIENTE_ASIGNACION`.
  - La respuesta debe incluir paginación estándar: `paginaActual`, `totalPaginas`, `totalElementos` y la lista de despachos.
  - Cada fila debe mostrar: código de rastreo, ID de pedido, dirección de destino, peso (kg), volumen (m³), fecha límite estimada y tiempo transcurrido en espera.
  - Si no existen pedidos pendientes (o el filtro no arroja resultados), se debe mostrar un estado visual vacío amigable: *"No hay despachos pendientes de asignación"*.
  - Tiempo de respuesta del endpoint: menor a 250 ms para lotes de hasta 100 registros.
- **Entidades de datos involucradas:** `despachos`.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-04: Listado con despachos pendientes**
  - **DADO** que existen despachos registrados en estado `PENDIENTE_ASIGNACION`.
  - **CUANDO** el Gestor accede a la vista de Programación y Asignación en el frontend o invoca `GET /api/v1/despachos/pendientes`.
  - **ENTONCES** el sistema despliega la lista paginada mostrando código de rastreo, pedido, dirección, peso, volumen, fecha límite y tiempo en espera con código de respuesta `200 OK`.

- [ ] **CA-05: Listado sin despachos pendientes**
  - **DADO** que no existen pedidos pendientes de asignación en el sistema o para el filtro seleccionado.
  - **CUANDO** el Gestor consulta la vista en el dashboard.
  - **ENTONCES** el sistema muestra un estado visual vacío indicando "No hay despachos pendientes de asignación" con código `200 OK` y lista vacía.

- [ ] **CA-06: Acceso sin permisos requeridos**
  - **DADO** que un usuario sin el rol `GESTOR_DESPACHO` intenta acceder al listado de pendientes.
  - **CUANDO** realiza la petición HTTP al endpoint `GET /api/v1/despachos/pendientes`.
  - **ENTONCES** el sistema rechaza la solicitud con código `403 Forbidden`, cuerpo de error estandarizado y no expone información operativa alguna.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Repositorio Spring Data JPA con consulta paginada (`Pageable`) indexada por estado `PENDIENTE_ASIGNACION`.
- [ ] Pruebas unitarias en backend (`JUnit 5 + Mockito`) verificando paginación, filtros y ordenamiento.
- [ ] Pruebas de seguridad (`Spring Security Test`) verificando acceso con rol `GESTOR_DESPACHO` y rechazo `403` para otros roles o usuarios anónimos.
- [ ] Componente React de Dashboard con tabla responsive, controles de paginación y skeleton loaders durante la carga.
- [ ] Estado visual amigable cuando la lista está vacía implementado con Tailwind CSS.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
