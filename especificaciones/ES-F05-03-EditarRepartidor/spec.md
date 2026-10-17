# ES-F05-03: Editar datos del repartidor

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Implementación local en verificación; aceptación integrada y revisión humana pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; editar desde el catálogo administrativo `/repartidores`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> La migración SDD se conserva en el historial. Esta revisión alinea los comportamientos con Operación §4.1 y Seguridad §8.4; mantiene los IDs de criterios y registra los cambios funcionales en la evidencia.

## 1. Contexto y objetivo

Permitir que el Gestor de Despacho modifique los datos de contacto, la licencia de conducir o el turno habitual de un repartidor existente, sin alterar su estado de registro ni su vinculación con Seguridad y Usuarios.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Precarga, validación y modificación de los cuatro campos editables.
- Resultado del comportamiento: Datos permitidos actualizados, identidad y estados conservados, con auditoría.

### Fuera de alcance

- Modificar el DNI, el estado de registro o el estado de vinculación.
- Dar de baja al repartidor.
- Registrar nuevos repartidores.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El repartidor existe en el módulo.
- Los campos editables son: teléfono, correo electrónico, número de brevete y turno habitual.
- El DNI no es editable porque es el identificador natural del repartidor.

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Editar en `/repartidores`, conforme al flujo conservado.
- Resultado exitoso: Datos permitidos actualizados, identidad y estados conservados, con auditoría.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. El Gestor selecciona `Editar` en la fila del repartidor desde el panel.
2. El frontend presenta el formulario con los datos actuales precargados.
3. El Gestor modifica los campos deseados y confirma.
4. El backend valida el rol, la existencia del repartidor y el formato de los campos.
5. El sistema actualiza los datos, registra la auditoría con el estado anterior y el nuevo, y responde con el repartidor actualizado.
6. El frontend muestra la confirmación del cambio.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Edición exitosa | Cambiar el teléfono del escenario y comprobar los estados y la auditoría. |
| CA-02 | Datos inválidos | Enviar correo inválido y comprobar que todos los datos previos se conservan. |
| CA-03 | Repartidor inexistente | Editar un UUID ausente y comprobar recurso inexistente. |
| CA-04 | Acceso sin permisos | Editar con otro rol y comprobar rechazo. |

## 5. Reglas, datos e integraciones

- Solo los campos teléfono, correo, brevete y turno habitual son editables.
- El DNI, el estado de registro y el estado de vinculación no se modifican en esta operación.
- Los campos deben tener formato válido; de lo contrario, se responde `400 Bad Request`.
- Si el repartidor no existe, se responde `404 Not Found`.
- Un usuario sin rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- La edición registra auditoría con usuario y marca temporal en UTC.

### Entradas

- Identificador del repartidor.
- Campos a modificar: teléfono, correo, brevete, turno habitual.
- Identidad y roles obtenidos del JWT.

### Salidas

- Repartidor actualizado con los nuevos datos.
- Registro de auditoría.

### Integraciones

- La ruta, cuerpos y códigos se rigen por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `PUT /api/v1/repartidores/{idRepartidor}`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

## 6. Criterios de aceptación

### CA-01. Edición exitosa

- **DADO** un repartidor registrado con teléfono "999-111-222".
- **CUANDO** el Gestor cambia el teléfono a "999-333-444" y confirma.
- **ENTONCES** el sistema actualiza el teléfono, conserva el estado de registro y vinculación, y registra la auditoría.

### CA-02. Datos inválidos

- **DADO** un repartidor registrado.
- **CUANDO** el Gestor envía un correo con formato inválido.
- **ENTONCES** el sistema responde `400 Bad Request` y no modifica el repartidor.

### CA-03. Repartidor inexistente

- **DADO** un identificador que no corresponde a ningún repartidor.
- **CUANDO** se intenta editar.
- **ENTONCES** el sistema responde `404 Not Found`.

### CA-04. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta editar un repartidor.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. UI, backend y requisitos no funcionales

- UI: [interacción y criterios CUI](./ui.md), con controles compartidos y estados de consulta distintos.
- Backend: Operación valida identidad y rol, aplica las reglas del catálogo y conserva sus datos; no consulta las tablas de Gestión.
- Acuerdos locales: los DTO, límites, estados, errores e idempotencia están definidos en Operación §4.1 y contrastados con ambos repositorios.
- Requisitos no funcionales: Conservar autorización, datos y auditoría; comprobar repetición y concurrencia cuando afecten el resultado.
- Pendientes externos: aceptación con Seguridad real; revisión visual humana y efectos de los consumidores F-03/F-06 que excedan las comprobaciones locales.
- [Evidencia](./evidence.md) distingue las comprobaciones locales, los dobles y los criterios todavía pendientes.

## 8. Verificación y completitud

| Criterio | Comprobación | Evidencia |
|---|---|---|
| CA-01 | Edición exitosa; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-02 | Datos inválidos; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-03 | Repartidor inexistente; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-04 | Acceso sin permisos; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |

- [ ] Todos los CA/CUI y requisitos no funcionales del alcance tienen aceptación completa.
- [ ] Las dependencias reales y la revisión humana se verificaron.
- [ ] La verificación local y sus límites están registrados.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-01 y CA-03.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
