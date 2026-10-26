# ES-F02-03: Consultar la cola de despachos pendientes

**Funcionalidad padre:** [F-02 — Programación y asignación de despachos](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-02 y RF-06.

**Responsable:** Tarqui.

**Estado:** Backend implementado y verificado localmente; pantalla e integración frontend pendientes. Ver [evidence.md](./evidence.md).

**Actor principal:** Gestor de Despacho (aplicación web administrativa).

**Servicio propietario:** Gestión de Despachos.

**UI:** Aplica; pestaña "Cola de pendientes" del Panel de Programación (`/programacion`), documentada en [ui.md](./ui.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md) y [UI](./ui.md). Preparación del 16/10/2026; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

El Gestor de Despacho necesita un panel unificado donde consultar, filtrar y priorizar los despachos que se encuentran físicamente en el centro de despacho esperando salir (estado `PENDIENTE_ASIGNACION`). La consulta proporciona una vista rápida de las variables de carga (peso en kg, volumen en m³ y paquetes físicos), el tiempo transcurrido en espera y la fecha programada de entrega.

El objetivo es permitir al Gestor consultar de forma paginada y filtrable los despachos pendientes, distinguiendo aquellos listos para asignación inmediata en la jornada de hoy de aquellos reprogramados a futuro por F-04 (cuya asignación está bloqueada) o despachos simulados de prueba, ofreciendo indicadores KPI interactivos y un estado vacío amigable [cite: 1].

## 2. Alcance

- Incluye: listado paginado de despachos en estado estricto `PENDIENTE_ASIGNACION`; ordenamiento por fecha programada ascendente; filtros por rango de fecha, zona de cobertura y tipo de intento (`TODOS`, `PRIMER_INTENTO`, `REINTENTOS`); indicadores KPI interactivos (Pendientes para hoy, Programados a futuro, Reintentos); visualización de peso, volumen, paquetes, tiempo en espera y etiquetas de estado ("Simulado", "Programado para [fecha]"); habilitación/deshabilitación del botón "Asignar"; estado vacío y control de acceso por rol `GESTOR_DESPACHO`.
- Fuera de alcance: ejecución de la asignación del despacho a un repartidor (ES-F02-04); consulta de rutas o despachos asignados/en tránsito (ES-F02-05); reprogramación de entregas fallidas (F-04).

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- El Gestor está autenticado con JWT y posee el rol `GESTOR_DESPACHO`. Usuarios sin este rol son rechazados con HTTP `403 Forbidden`.
- Existen registros de despachos persistidos en el sistema.
- El servidor aplica la zona horaria civil `America/Lima` para la determinación de la fecha "hoy".

### 3.2. Dependencias

- **Contrato de API:** [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).
- **Zonas y Cotizador (F-01):** provee el catálogo de zonas activas para el filtro de zona.
- **Entregas Fallidas (F-04):** devuelve a la cola despachos reprogramados que ingresan inmediatamente a `PENDIENTE_ASIGNACION`.
- **Generación de Simulaciones (ES-F02-02):** incorpora despachos de prueba en cola.

### 3.3. Resultados

- Respuesta HTTP `200 OK` con metadata de paginación (`paginaActual`, `totalPaginas`, `totalElementos`, `tamanoPagina`) y arreglo de despachos pendientes con todas las variables de carga y seguimiento.
- Visualización en la tabla de React con acciones de filtrado, paginación y botón "Asignar" condicionado a la fecha programada.

## 4. Flujo principal y alternativas

1. El Gestor ingresa a la ruta `/programacion` en la aplicación web.
2. El frontend solicita `GET /api/v1/despachos/pendientes` con los parámetros por omisión (`pagina=1`, `tamanoPagina=20`).
3. El backend valida el JWT y el rol `GESTOR_DESPACHO`.
4. El backend consulta la base de datos aplicando la restricción obligatoria `estado = 'PENDIENTE_ASIGNACION'` y orden `fecha_programada ASC, creado_en ASC`.
5. Calcula los 3 contadores KPI sobre todo el universo de pendientes:
   - `pendientesHoy`: `fechaProgramada <= hoy`.
   - `programadosFuturo`: `fechaProgramada > hoy`.
   - `reintentos`: despachos con al menos una reprogramación aceptada en su historial.
6. Retorna la página con los datos y los indicadores.
7. El frontend renderiza las tarjetas KPI, la barra de filtros y la tabla paginada.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Filtro por zona y reintentos | El Gestor selecciona zona y chip "Reintentos" | Devuelve únicamente despachos de esa zona con reprogramaciones previas | CA-02 |
| Fecha programada a futuro | `fechaProgramada > hoy` | Fila muestra badge informativo y botón "Asignar" deshabilitado | CA-03 |
| Cola vacía | No hay despachos pendientes de asignación | Muestra estado vacío "No hay despachos pendientes de asignación" y botón de prueba | CA-04 |
| Despacho simulado | `esSimulacion == true` | Fila muestra badge neutral punteado "Simulado" | CA-05 |
| Acceso no autorizado | Usuario sin rol `GESTOR_DESPACHO` | Backend responde `403 Forbidden` y el frontend muestra pantalla de acceso denegado | CA-06 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Solo se listan despachos cuyo estado vigente sea estrictamente `PENDIENTE_ASIGNACION`. | F-02 RF-02 |
| RN-02 | Orden predeterminado: `fechaProgramada` ascendente; desempate por `creadoEn` ascendente. | F-02 CA-03 |
| RN-03 | Despachos reprogramados para una fecha futura se listan en cola en modo solo lectura; su asignación se bloquea hasta que llegue dicha fecha. | F-02 RF-06, CA-13 |
| RN-04 | El filtro `tipoIntento` admite `TODOS`, `PRIMER_INTENTO` y `REINTENTOS`. `REINTENTOS` filtra por presencia de reprogramaciones previas, no por `numeroIntentos > 1`. | api-contract-gestion-despachos.md §3.2 |
| RN-05 | Rendimiento: tiempo de respuesta inferior a 250 ms para páginas de hasta 100 registros. | F-02 RNF Rendimiento |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `GET /api/v1/despachos/pendientes` | Endpoint canónico de consulta paginada. | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) |
| Catálogo de Zonas (F-01) | Opciones del filtro desplegable de zona. | [F-01-Gestor_ZonasGeograficas.md](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) |
| Componentes React compartidos | Shell, tablas, filtros, tarjetas KPI y badges. | [componentes-react.md](../../disenio/componentes-react.md) |

## 6. Criterios de aceptación

### CA-01. Consulta exitosa de la cola de pendientes

- **DADO** que existen despachos registrados en estado `PENDIENTE_ASIGNACION`.
- **CUANDO** el Gestor abre la pantalla de programación con credenciales válidas o invoca `GET /api/v1/despachos/pendientes`.
- **ENTONCES** el sistema devuelve exclusivamente los despachos en dicho estado con todas sus columnas obligatorias (código de rastreo, pedido, zona, dirección, peso en kg, volumen en m³, cantidad física de paquetes, fecha programada, número de intento y tiempo en espera), ordenados por fecha programada ascendente y con metadata de paginación.

### CA-02. Filtro combinado por zona y tipo de intento

- **DADO** una lista de despachos pendientes con diversas zonas y reprogramaciones aceptadas (incluyendo contador 1 tras un fallo y contador 0 tras `NO_INTENTADO`).
- **CUANDO** el Gestor filtra por la zona "Lima Norte" y selecciona "Reintentos".
- **ENTONCES** el backend devuelve únicamente los despachos de esa zona con al menos una reprogramación aceptada en su historial, conservando su estado y contadores inalterados. El selector "Primer intento" excluye esos mismos despachos y "Todos" no aplica restricción de intento.

### CA-03. Restricción operativa en despachos programados a futuro

- **DADO** un despacho reprogramado por F-04 con fecha de entrega programada posterior al día actual.
- **CUANDO** el Gestor visualiza la fila en la tabla de pendientes.
- **ENTONCES** el despacho muestra la etiqueta "Programado para [fecha]" y el botón de acción "Asignar" se encuentra deshabilitado con el mensaje explicativo "Disponible desde [fecha]".

### CA-04. Cola de pendientes vacía

- **DADO** que no existen despachos en espera de asignación (o ningún registro coincide con los filtros aplicados).
- **CUANDO** el Gestor consulta la vista en el panel.
- **ENTONCES** la interfaz muestra el estado visual vacío "No hay despachos pendientes de asignación" junto al botón "Generar pedido de prueba", sin exponer registros de otros estados operativos.

### CA-05. Distintivo de despachos simulados

- **DADO** que existen despachos originados por simulación (`esSimulacion = true`).
- **CUANDO** son listados en la cola de pendientes.
- **ENTONCES** se presentan con el badge neutral punteado "Simulado" y pueden ser filtrados y asignados normalmente.

### CA-06. Acceso sin permisos requeridos

- **DADO** un usuario autenticado sin el rol `GESTOR_DESPACHO` o una petición sin token.
- **CUANDO** intenta consultar el listado de pendientes en `GET /api/v1/despachos/pendientes`.
- **ENTONCES** el sistema responde `403 Forbidden` si el token aceptado carece del rol, o `401 Unauthorized` si no hay token aceptado, según Común §3.5; no expone datos operativos ni contadores de la cola.

## 7. Referencias

1. [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md): requisitos RF-02 y RF-06; criterios CA-03, CA-04, CA-05 y CA-13.
2. [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación): parámetros y respuestas de la cola de pendientes.
3. [ui.md](./ui.md): diseño detallado y componentes de la pantalla.
