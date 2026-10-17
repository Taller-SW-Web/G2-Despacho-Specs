# ES-F05-07: Consultar furgonetas

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Implementación local en verificación; aceptación integrada y revisión humana pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; consultar furgonetas desde el catálogo administrativo `/furgonetas`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> La migración SDD se conserva en el historial. Esta revisión alinea los comportamientos con Operación §4.1 y Seguridad §8.4; mantiene los IDs de criterios y registra los cambios funcionales en la evidencia.

## 1. Contexto y objetivo

Permitir que el Gestor de Despacho consulte el catálogo de furgonetas del módulo mediante un listado paginado con filtros por estado y placa. El panel sirve como punto de entrada para las operaciones de edición y cambio de estado de cada furgoneta.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Filtros combinables de estado y coincidencia de placa, paginación y ausencia de resultados.
- Resultado del comportamiento: Página con capacidades, estados y totales coherentes, sin cambios de datos.

### Fuera de alcance

- Registrar, editar o cambiar el estado de furgonetas.
- Consultar la ocupación actual de una furgoneta en jornada.
- Gestionar repartidores.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- Las furgonetas fueron registradas previamente mediante ES-F05-06.
- La consulta utiliza paginación y puede incluir filtros opcionales.

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Consultar furgonetas en `/furgonetas`, conforme al flujo conservado.
- Resultado exitoso: Página con capacidades, estados y totales coherentes, sin cambios de datos.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. El Gestor ingresa al panel de furgonetas.
2. El frontend solicita la primera página con los filtros seleccionados.
3. El backend valida el rol y recupera las furgonetas que coinciden con los filtros.
4. El sistema devuelve la página con datos de la furgoneta incluyendo placa, estado y límites de carga.
5. El frontend presenta el listado con acciones disponibles por fila: editar y cambiar estado.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Listado con furgonetas | Sembrar furgonetas y revisar filas, capacidades y totales. |
| CA-02 | Filtro por estado | Filtrar por DISPONIBLE y comprobar todas las filas devueltas. |
| CA-03 | Búsqueda por placa | Buscar ABC y comprobar coincidencias de placa. |
| CA-04 | Listado vacío | Consultar sin coincidencias y verificar el estado vacío. |
| CA-05 | Acceso sin permisos | Consultar con otro rol y comprobar rechazo. |

## 5. Reglas, datos e integraciones

- Cada fila muestra como mínimo: identificador, placa, estado (`DISPONIBLE`, `EN_MANTENIMIENTO`, `FUERA_DE_SERVICIO`), límite de peso (kg), límite de volumen (m³) y máximo de paquetes.
- Los filtros por estado y búsqueda por placa pueden combinarse.
- Si no existen furgonetas que coincidan, se muestra un estado vacío.
- Un usuario sin el rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- El listado pagina a partir de 50 registros y responde en menos de 200 ms.

### Entradas

- Página y tamaño de página.
- Filtro opcional por estado de la furgoneta.
- Búsqueda opcional por placa.
- Identidad y roles obtenidos del JWT.

### Salidas

- Página de furgonetas con los campos definidos.
- Metadatos de paginación.
- Estado vacío cuando no existen resultados.
- Error normalizado si la solicitud no está autorizada.

### Integraciones

- La ruta, parámetros y forma de error se rigen por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `GET /api/v1/furgonetas`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

## 6. Criterios de aceptación

### CA-01. Listado con furgonetas

- **DADO** que existen furgonetas registradas.
- **CUANDO** el Gestor abre el panel de furgonetas.
- **ENTONCES** el sistema muestra un listado paginado con placa, estado y límites de carga.

### CA-02. Filtro por estado

- **DADO** furgonetas con distintos estados.
- **CUANDO** el Gestor filtra por `DISPONIBLE`.
- **ENTONCES** el sistema devuelve solo las furgonetas en ese estado.

### CA-03. Búsqueda por placa

- **DADO** furgonetas registradas.
- **CUANDO** el Gestor busca por placa "ABC".
- **ENTONCES** el sistema devuelve las furgonetas cuya placa contiene ese texto.

### CA-04. Listado vacío

- **DADO** que no existen furgonetas que coincidan con los filtros.
- **CUANDO** el Gestor consulta el panel.
- **ENTONCES** el frontend muestra un estado vacío.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar las furgonetas.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. UI, backend y requisitos no funcionales

- UI: [interacción y criterios CUI](./ui.md), con controles compartidos y estados de consulta distintos.
- Backend: Operación valida identidad y rol, aplica las reglas del catálogo y conserva sus datos; no consulta las tablas de Gestión.
- Acuerdos locales: los DTO, límites, estados, errores e idempotencia están definidos en Operación §4.1 y contrastados con ambos repositorios.
- Requisitos no funcionales: El requisito de menos de 200 ms debe medirse por separado con entorno y volumen registrados; una prueba con mocks o el resultado funcional de una suite no lo acredita.
- Pendientes externos: aceptación con Seguridad real; revisión visual humana y efectos de los consumidores F-03/F-06 que excedan las comprobaciones locales.
- [Evidencia](./evidence.md) distingue las comprobaciones locales, los dobles y los criterios todavía pendientes.

## 8. Verificación y completitud

| Criterio | Comprobación | Evidencia |
|---|---|---|
| CA-01 | Listado con furgonetas; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-02 | Filtro por estado; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-03 | Búsqueda por placa; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-04 | Listado vacío; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-05 | Acceso sin permisos; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |

- [ ] Todos los CA/CUI y requisitos no funcionales del alcance tienen aceptación completa.
- [ ] Las dependencias reales y la revisión humana se verificaron.
- [ ] La verificación local y sus límites están registrados.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-02 y CA-13.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
