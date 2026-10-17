# ES-F05-02: Consultar repartidores

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Borrador migrado a SDD; revisión funcional y aceptación pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; consultar repartidores desde el catálogo administrativo `/repartidores`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> Migración estructural desde `ES-F05-02-ConsultarRepartidores.md`, revisión `f3849d9`. Se conservan las reglas y los criterios originales, incluidos sus IDs. Las discrepancias detectadas se registran en §7 y en el plan; esta migración no aprueba cambios de contrato ni acredita integración desplegada.

## 1. Contexto y objetivo

Permitir que el Gestor de Despacho consulte el catálogo de repartidores del módulo mediante un listado paginado con filtros por estado de registro, estado de vinculación y turno habitual. El panel sirve como punto de entrada para las operaciones de edición, baja y reintento de vinculación.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Listado, filtros por registro/vinculación/turno, paginación y estados vacíos.
- Resultado del comportamiento: Página coherente con los filtros confirmados, sin mutaciones del catálogo.

### Fuera de alcance

- Registrar, editar o dar de baja repartidores.
- Consultar la disponibilidad operativa o la ocupación del repartidor en una jornada.
- Gestionar furgonetas.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- Los repartidores fueron registrados previamente mediante ES-F05-01.
- La consulta utiliza paginación y puede incluir filtros opcionales.

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Consultar repartidores en `/repartidores`, conforme al flujo conservado.
- Resultado exitoso: Página coherente con los filtros confirmados, sin mutaciones del catálogo.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. El Gestor ingresa al panel de repartidores.
2. El frontend solicita la primera página con los filtros seleccionados.
3. El backend valida el rol y recupera los repartidores que coinciden con los filtros.
4. El sistema devuelve la página con datos del repartidor, estados de registro y vinculación, y turno habitual.
5. El frontend presenta el listado con acciones disponibles por fila: editar, dar de baja y reintentar vinculación cuando aplique.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Listado con repartidores | Sembrar perfiles y comparar las filas y metadatos de paginación. |
| CA-02 | Aplicación de filtros | Combinar filtros y comprobar exclusivamente las coincidencias. |
| CA-03 | Listado vacío | Consultar sin coincidencias y verificar un vacío real, no un error presentado como vacío. |
| CA-04 | Acceso sin permisos | Consultar con otro rol y comprobar rechazo. |

## 5. Reglas, datos e integraciones

- Cada fila muestra como mínimo: identificador, nombres, apellidos, DNI, teléfono, turno habitual, estado de registro (`ACTIVO` / `INACTIVO`) y estado de vinculación (`PENDIENTE`, `PENDIENTE_ACTIVACION`, `VINCULADO`, `ERROR`).
- Los filtros por estado de registro, estado de vinculación y turno habitual pueden combinarse.
- Si no existen repartidores que coincidan, se muestra un estado vacío.
- Un usuario sin el rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- El listado pagina a partir de 50 registros y responde en menos de 200 ms.

### Entradas

- Página y tamaño de página.
- Filtro opcional por estado de registro.
- Filtro opcional por estado de vinculación.
- Filtro opcional por turno habitual.
- Identidad y roles obtenidos del JWT.

### Salidas

- Página de repartidores con los campos definidos.
- Metadatos de paginación.
- Estado vacío cuando no existen resultados.
- Error normalizado si la solicitud no está autorizada.

### Integraciones

- La ruta, parámetros y forma de error se rigen por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `GET /api/v1/repartidores; GET /api/v1/repartidores/{idRepartidor}`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

## 6. Criterios de aceptación

### CA-01. Listado con repartidores

- **DADO** que existen repartidores registrados.
- **CUANDO** el Gestor abre el panel de repartidores.
- **ENTONCES** el sistema muestra un listado paginado con los datos y estados de cada repartidor.

### CA-02. Aplicación de filtros

- **DADO** repartidores con distintos estados y turnos.
- **CUANDO** el Gestor combina uno o más filtros.
- **ENTONCES** el sistema devuelve solo las coincidencias.

### CA-03. Listado vacío

- **DADO** que no existen repartidores que coincidan con los filtros.
- **CUANDO** el Gestor consulta el panel.
- **ENTONCES** el frontend muestra un estado vacío.

### CA-04. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar los repartidores.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. UI, backend y requisitos no funcionales

- UI: interacción, estados y criterios CUI en [ui.md](./ui.md); reutilización de los [componentes compartidos](../../disenio/componentes-react.md).
- Backend: Consultar el catálogo paginado y combinar filtros de repartidores. Propiedad local de `repartidores`; no acceder a la base de Gestión.
- Requisitos no funcionales: Conservar el requisito original de menos de 200 ms; medirlo con volumen de datos, percentil, red y entorno registrados. No se acredita esa cifra mediante una prueba de presentación.
- Seguridad y datos: no mostrar credenciales, tokens ni errores técnicos en la interfaz; la habilitación visual no reemplaza la autorización del backend.
- Pendiente funcional P-01: La fuente conserva PENDIENTE_ACTIVACION y ERROR, mientras el contrato y el modelo vigentes usan el vínculo local pendiente/vinculado. Confirmar los estados del filtro antes de cerrar CA-01/02. La exigencia de menos de 200 ms necesita una medición con entorno y carga identificados.
- Responsable de P-01: Rhamses coordina con Arquitectura y Seguridad; la revisión afecta los criterios indicados y debe resolverse antes de declarar la aceptación completa.
- Las implementaciones existentes se referencian en [evidence.md](./evidence.md). Su existencia no reemplaza la comprobación individual de los criterios conservados.

## 8. Verificación y completitud

| Criterio | Comprobación prevista | Nivel y preparación |
|---|---|---|
| CA-01 | Sembrar perfiles y comparar las filas y metadatos de paginación. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-02 | Combinar filtros y comprobar exclusivamente las coincidencias. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-03 | Consultar sin coincidencias y verificar un vacío real, no un error presentado como vacío. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-04 | Consultar con otro rol y comprobar rechazo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |

- [ ] Todos los criterios y CUI cuentan con resultados por caso en [evidence.md](./evidence.md).
- [ ] P-01 está resuelto en los documentos propietarios y revisado por el equipo.
- [ ] Los datos, el contrato y la implementación son consistentes.
- [ ] Las dependencias simuladas y la integración real pendiente se identifican expresamente.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-01 y CA-07.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
