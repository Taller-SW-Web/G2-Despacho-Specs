# ES-F05-09: Cambiar estado de furgoneta

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Borrador migrado a SDD; revisión funcional y aceptación pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; cambiar estado desde el catálogo administrativo `/furgonetas`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> Migración estructural desde `ES-F05-09-CambiarEstadoFurgoneta.md`, revisión `f3849d9`. Se conservan las reglas y los criterios originales, incluidos sus IDs. Las discrepancias detectadas se registran en §7 y en el plan; esta migración no aprueba cambios de contrato ni acredita integración desplegada.

## 1. Contexto y objetivo

Permitir que el Gestor de Despacho cambie el estado de una furgoneta entre `DISPONIBLE`, `EN_MANTENIMIENTO` y `FUERA_DE_SERVICIO`, controlando que no se retire una furgoneta que tiene despachos en curso en una jornada activa.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Transiciones permitidas, retiro, rehabilitación, conflictos de carga y cierre de jornada vacía.
- Resultado del comportamiento: Estado y auditoría confirmados con cierre de jornada cuando corresponde, manteniendo historial y carga.

### Fuera de alcance

- Editar los límites de carga de la furgoneta.
- Registrar nuevas furgonetas.
- Reasignar despachos en curso a otra furgoneta.
- Gestionar la logística de mantenimiento del vehículo.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- La furgoneta existe en el módulo.
- Las transiciones válidas son:
  - `DISPONIBLE` → `EN_MANTENIMIENTO`
  - `DISPONIBLE` → `FUERA_DE_SERVICIO`
  - `EN_MANTENIMIENTO` → `DISPONIBLE`
  - `EN_MANTENIMIENTO` → `FUERA_DE_SERVICIO`
  - `FUERA_DE_SERVICIO` → `DISPONIBLE` (rehabilitación)

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Cambiar estado en `/furgonetas`, conforme al flujo conservado.
- Resultado exitoso: Estado y auditoría confirmados con cierre de jornada cuando corresponde, manteniendo historial y carga.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. El Gestor selecciona la acción de cambio de estado en la fila de la furgoneta.
2. El frontend muestra el estado actual y las transiciones válidas.
3. El Gestor selecciona el nuevo estado y confirma.
4. El backend valida el rol, la existencia, la transición válida y la ausencia de conflictos con jornadas activas.
5. El sistema actualiza el estado, gestiona la jornada activa si corresponde y registra la auditoría.
6. El frontend actualiza la fila con el nuevo estado.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Cambio a mantenimiento sin jornada activa | Pasar a mantenimiento sin jornada y revisar disponibilidad y auditoría. |
| CA-02 | Cambio a mantenimiento con jornada activa sin despachos en curso | Retirar con jornada vacía y comprobar cierre, auditoría y estado operativo derivado en F-06. |
| CA-03 | Rechazo por despachos en curso | Crear despachos ASIGNADO y EN_CAMINO y comprobar rechazo del retiro sin cambios. |
| CA-04 | Retorno a disponible desde mantenimiento | Volver de mantenimiento a DISPONIBLE y verificar el catálogo. |
| CA-05 | Cambio a fuera de servicio | Retirar a FUERA_DE_SERVICIO y conservar el historial; revisar rehabilitación admitida. |
| CA-06 | Furgoneta inexistente | Cambiar estado de un UUID ausente y comprobar recurso inexistente. |
| CA-07 | Acceso sin permisos | Cambiar estado con otro rol y comprobar rechazo. |

## 5. Reglas, datos e integraciones

- Si la furgoneta tiene una jornada activa con despachos `ASIGNADO` o `EN_CAMINO`, el cambio a `EN_MANTENIMIENTO` o `FUERA_DE_SERVICIO` se rechaza con `409 Conflict`.
- Si la furgoneta tiene jornada activa sin despachos en curso, la jornada se cierra y el repartidor pasa a `FUERA_DE_TURNO` en F-06.
- Una furgoneta en `EN_MANTENIMIENTO` o `FUERA_DE_SERVICIO` queda excluida de nuevas asignaciones diarias en F-06.
- `FUERA_DE_SERVICIO` representa un retiro definitivo, pero se conserva el historial.
- Un usuario sin rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- La auditoría registra usuario, estado anterior, estado nuevo y marca temporal en UTC.

### Entradas

- Identificador de la furgoneta.
- Nuevo estado.
- Identidad y roles obtenidos del JWT.

### Salidas

- Furgoneta con estado actualizado.
- Jornada activa cerrada si correspondía.
- Registro de auditoría.

### Integraciones

- F-06 cierra la jornada activa y pone al repartidor en `FUERA_DE_TURNO` cuando se retira la furgoneta.
- F-06 excluye furgonetas `EN_MANTENIMIENTO` y `FUERA_DE_SERVICIO` de nuevas asignaciones.
- La ruta y códigos se rigen por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `PATCH /api/v1/furgonetas/{idFurgoneta}/estado`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

## 6. Criterios de aceptación

### CA-01. Cambio a mantenimiento sin jornada activa

- **DADO** una furgoneta `DISPONIBLE` sin jornada activa.
- **CUANDO** el Gestor la cambia a `EN_MANTENIMIENTO`.
- **ENTONCES** el sistema actualiza el estado y la excluye de nuevas asignaciones.

### CA-02. Cambio a mantenimiento con jornada activa sin despachos en curso

- **DADO** una furgoneta `DISPONIBLE` con jornada activa pero sin despachos `ASIGNADO` ni `EN_CAMINO`.
- **CUANDO** el Gestor la cambia a `EN_MANTENIMIENTO`.
- **ENTONCES** el sistema cierra la jornada, el repartidor pasa a `FUERA_DE_TURNO` y la furgoneta queda en `EN_MANTENIMIENTO`.

### CA-03. Rechazo por despachos en curso

- **DADO** una furgoneta con jornada activa y despachos `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor intenta cambiarla a `EN_MANTENIMIENTO` o `FUERA_DE_SERVICIO`.
- **ENTONCES** el sistema responde `409 Conflict` indicando que la furgoneta tiene despachos en curso.

### CA-04. Retorno a disponible desde mantenimiento

- **DADO** una furgoneta en `EN_MANTENIMIENTO`.
- **CUANDO** el Gestor la cambia a `DISPONIBLE`.
- **ENTONCES** el sistema actualiza el estado y la furgoneta vuelve a estar disponible para asignaciones diarias.

### CA-05. Cambio a fuera de servicio

- **DADO** una furgoneta `DISPONIBLE` o `EN_MANTENIMIENTO` sin jornada activa con despachos en curso.
- **CUANDO** el Gestor la cambia a `FUERA_DE_SERVICIO`.
- **ENTONCES** el sistema actualiza el estado, la excluye definitivamente y conserva el historial.

### CA-06. Furgoneta inexistente

- **DADO** un identificador que no corresponde a ninguna furgoneta.
- **CUANDO** se intenta cambiar su estado.
- **ENTONCES** el sistema responde `404 Not Found`.

### CA-07. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta cambiar el estado de una furgoneta.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. UI, backend y requisitos no funcionales

- UI: interacción, estados y criterios CUI en [ui.md](./ui.md); reutilización de los [componentes compartidos](../../disenio/componentes-react.md).
- Backend: Cambiar el estado del vehículo y cerrar jornadas vacías sin retirar carga en curso. Propiedad local de `furgonetas y asignaciones_diarias`; no acceder a la base de Gestión.
- Requisitos no funcionales: Confirmar consistencia de datos, permisos y auditoría; comprobar cancelación, repetición y concurrencia cuando afecten el resultado.
- Seguridad y datos: no mostrar credenciales, tokens ni errores técnicos en la interfaz; la habilitación visual no reemplaza la autorización del backend.
- Pendiente funcional P-01: La fuente admite rehabilitación pero también llama definitivo al retiro; revisar esa redacción funcional sin eliminar criterios. Confirmar la traducción FUERA_DE_SERVICIO/INACTIVA y verificar en F-06 el estado FUERA_DE_TURNO derivado del cierre de jornada.
- Responsable de P-01: Rhamses coordina con Arquitectura; la revisión afecta los criterios indicados y debe resolverse antes de declarar la aceptación completa.
- Las implementaciones existentes se referencian en [evidence.md](./evidence.md). Su existencia no reemplaza la comprobación individual de los criterios conservados.

## 8. Verificación y completitud

| Criterio | Comprobación prevista | Nivel y preparación |
|---|---|---|
| CA-01 | Pasar a mantenimiento sin jornada y revisar disponibilidad y auditoría. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-02 | Retirar con jornada vacía y comprobar cierre, auditoría y estado operativo derivado en F-06. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-03 | Crear despachos ASIGNADO y EN_CAMINO y comprobar rechazo del retiro sin cambios. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-04 | Volver de mantenimiento a DISPONIBLE y verificar el catálogo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-05 | Retirar a FUERA_DE_SERVICIO y conservar el historial; revisar rehabilitación admitida. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-06 | Cambiar estado de un UUID ausente y comprobar recurso inexistente. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-07 | Cambiar estado con otro rol y comprobar rechazo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |

- [ ] Todos los criterios y CUI cuentan con resultados por caso en [evidence.md](./evidence.md).
- [ ] P-01 está resuelto en los documentos propietarios y revisado por el equipo.
- [ ] Los datos, el contrato y la implementación son consistentes.
- [ ] Las dependencias simuladas y la integración real pendiente se identifican expresamente.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-02, CA-11 y CA-12.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
