# ES-F05-04: Dar de baja lógica al repartidor

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Borrador migrado a SDD; revisión funcional y aceptación pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; dar de baja desde el catálogo administrativo `/repartidores`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> Migración estructural desde `ES-F05-04-DarDeBajaRepartidor.md`, revisión `f3849d9`. Se conservan las reglas y los criterios originales, incluidos sus IDs. Las discrepancias detectadas se registran en §7 y en el plan; esta migración no aprueba cambios de contrato ni acredita integración desplegada.

## 1. Contexto y objetivo

Permitir que el Gestor de Despacho cambie el estado de registro de un repartidor a `INACTIVO`, excluyéndolo de futuras asignaciones y del acceso a F-03, pero conservando su registro y todo su historial operativo.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Confirmación, comprobación de despachos, cambio a INACTIVO y repetición controlada.
- Resultado del comportamiento: Perfil inactivo y auditado, con historial conservado y exclusión operativa verificable en sus consumidores.

### Fuera de alcance

- Eliminar físicamente el registro del repartidor.
- Reactivar un repartidor dado de baja.
- Reasignar despachos en curso a otro repartidor.
- Revocar o desactivar la cuenta en Seguridad y Usuarios.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El repartidor existe y su estado de registro es `ACTIVO`.
- El repartidor no tiene despachos en estado `ASIGNADO` ni `EN_CAMINO`.

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Dar de baja en `/repartidores`, conforme al flujo conservado.
- Resultado exitoso: Perfil inactivo y auditado, con historial conservado y exclusión operativa verificable en sus consumidores.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. El Gestor selecciona `Dar de baja` en la fila del repartidor.
2. El frontend solicita confirmación indicando que el repartidor será excluido de nuevas asignaciones.
3. El Gestor confirma la operación.
4. El backend valida el rol, el estado de registro actual y la ausencia de despachos en curso.
5. El sistema cambia el estado de registro a `INACTIVO` y registra la auditoría.
6. El frontend actualiza la fila del repartidor con el nuevo estado.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Baja exitosa sin despachos en curso | Dar de baja sin despachos, revisar auditoría e historial y verificar exclusión en F-03/F-06 cuando estén disponibles. |
| CA-02 | Rechazo por despachos en curso | Preparar ASIGNADO y EN_CAMINO y comprobar conflicto sin cambios. |
| CA-03 | Repartidor ya inactivo | Repetir la baja y comprobar que no se duplica la mutación ni su auditoría. |
| CA-04 | Acceso sin permisos | Dar de baja con otro rol y comprobar rechazo. |
| CA-05 | Repartidor inexistente | Dar de baja a un UUID ausente y comprobar recurso inexistente. |

## 5. Reglas, datos e integraciones

- Solo se puede dar de baja a un repartidor cuyo estado de registro sea `ACTIVO`.
- Si el repartidor tiene despachos `ASIGNADO` o `EN_CAMINO`, la operación se rechaza con `409 Conflict` indicando que tiene despachos en curso.
- La baja es lógica: el registro se conserva con todo su historial.
- Un repartidor `INACTIVO` no puede recibir asignaciones diarias en F-06 ni acceder a F-03.
- Si el repartidor ya está `INACTIVO`, el sistema informa que la baja ya fue procesada.
- Un usuario sin rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- La auditoría registra el usuario, el estado anterior, el estado nuevo y la marca temporal en UTC.

### Entradas

- Identificador del repartidor.
- Identidad y roles obtenidos del JWT.

### Salidas

- Repartidor con estado de registro `INACTIVO`.
- Historial operativo conservado.
- Registro de auditoría.

### Integraciones

- F-06 excluye al repartidor `INACTIVO` de nuevas asignaciones diarias.
- F-03 niega el acceso al repartidor `INACTIVO`.
- La ruta y códigos se rigen por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `PATCH /api/v1/repartidores/{idRepartidor}/estado`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

## 6. Criterios de aceptación

### CA-01. Baja exitosa sin despachos en curso

- **DADO** un repartidor `ACTIVO` sin despachos `ASIGNADO` ni `EN_CAMINO`.
- **CUANDO** el Gestor confirma la baja.
- **ENTONCES** el sistema cambia el estado a `INACTIVO`, conserva el historial y registra la auditoría.

### CA-02. Rechazo por despachos en curso

- **DADO** un repartidor con despachos en `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor intenta darlo de baja.
- **ENTONCES** el sistema responde `409 Conflict` indicando que tiene despachos en curso.

### CA-03. Repartidor ya inactivo

- **DADO** un repartidor con estado `INACTIVO`.
- **CUANDO** se intenta dar de baja nuevamente.
- **ENTONCES** el sistema informa que la baja ya fue procesada sin duplicar la operación.

### CA-04. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta dar de baja a un repartidor.
- **ENTONCES** el sistema responde `403 Forbidden`.

### CA-05. Repartidor inexistente

- **DADO** un identificador que no corresponde a ningún repartidor.
- **CUANDO** se intenta dar de baja.
- **ENTONCES** el sistema responde `404 Not Found`.

## 7. UI, backend y requisitos no funcionales

- UI: interacción, estados y criterios CUI en [ui.md](./ui.md); reutilización de los [componentes compartidos](../../disenio/componentes-react.md).
- Backend: Dar de baja lógica al repartidor sin carga en curso y conservar su historial. Propiedad local de `repartidores y asignaciones_diarias`; no acceder a la base de Gestión.
- Requisitos no funcionales: Confirmar consistencia de datos, permisos y auditoría; comprobar cancelación, repetición y concurrencia cuando afecten el resultado.
- Seguridad y datos: no mostrar credenciales, tokens ni errores técnicos en la interfaz; la habilitación visual no reemplaza la autorización del backend.
- Pendiente funcional P-01: La implementación conserva una comprobación adicional de reservas activas y cierra jornadas vacías. Revisar ese alcance conservador con el contrato. La exclusión efectiva en F-03/F-06 requiere verificar sus consumidores; la baja local no acredita esa integración completa.
- Responsable de P-01: Rhamses coordina con Arquitectura; la revisión afecta los criterios indicados y debe resolverse antes de declarar la aceptación completa.
- Las implementaciones existentes se referencian en [evidence.md](./evidence.md). Su existencia no reemplaza la comprobación individual de los criterios conservados.

## 8. Verificación y completitud

| Criterio | Comprobación prevista | Nivel y preparación |
|---|---|---|
| CA-01 | Dar de baja sin despachos, revisar auditoría e historial y verificar exclusión en F-03/F-06 cuando estén disponibles. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-02 | Preparar ASIGNADO y EN_CAMINO y comprobar conflicto sin cambios. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-03 | Repetir la baja y comprobar que no se duplica la mutación ni su auditoría. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-04 | Dar de baja con otro rol y comprobar rechazo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-05 | Dar de baja a un UUID ausente y comprobar recurso inexistente. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |

- [ ] Todos los criterios y CUI cuentan con resultados por caso en [evidence.md](./evidence.md).
- [ ] P-01 está resuelto en los documentos propietarios y revisado por el equipo.
- [ ] Los datos, el contrato y la implementación son consistentes.
- [ ] Las dependencias simuladas y la integración real pendiente se identifican expresamente.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-01, CA-04 y CA-05.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
