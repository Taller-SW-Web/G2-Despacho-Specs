# ES-F05-08: Editar furgoneta y límites de carga

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Implementación local en verificación; aceptación integrada y revisión humana pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; editar límites desde el catálogo administrativo `/furgonetas`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> La migración SDD se conserva en el historial. Esta revisión alinea los comportamientos con Operación §4.1 y Seguridad §8.4; mantiene los IDs de criterios y registra los cambios funcionales en la evidencia.

## 1. Contexto y objetivo

Permitir que el Gestor de Despacho modifique los límites de carga de una furgoneta existente. Los nuevos límites se aplican a las jornadas futuras; las jornadas activas conservan los valores con los que fueron creadas.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Edición de las tres capacidades, validación y comprobación de jornadas previas.
- Resultado del comportamiento: Nuevas capacidades maestras auditadas; placa, estado y capacidades de jornadas previas conservados.

### Fuera de alcance

- Cambiar el estado de la furgoneta.
- Modificar la placa.
- Registrar nuevas furgonetas.
- Recalcular la ocupación de una jornada activa con los nuevos límites.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- La furgoneta existe en el módulo.
- La furgoneta no tiene una jornada activa en el momento de la edición, o si la tiene, los nuevos límites solo se aplicarán a jornadas futuras.
- Los campos editables son: límite de peso (kg), límite de volumen (m³) y máximo de paquetes en ruta.
- La placa no es editable.

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Editar límites en `/furgonetas`, conforme al flujo conservado.
- Resultado exitoso: Nuevas capacidades maestras auditadas; placa, estado y capacidades de jornadas previas conservados.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. El Gestor selecciona `Editar` en la fila de la furgoneta.
2. El frontend presenta el formulario con los datos actuales precargados.
3. El Gestor modifica los límites y confirma.
4. El backend valida el rol, la existencia de la furgoneta y que los límites sean mayores que cero.
5. El sistema actualiza los límites, registra la auditoría y responde con la furgoneta actualizada.
6. El frontend muestra la confirmación.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Edición exitosa de límites | Editar capacidades y comprobar valores, auditoría, placa y estado. |
| CA-02 | Límites aplican solo a jornadas futuras | Crear jornada con capacidades originales, editar el maestro y comprobar que solo las jornadas futuras toman los nuevos límites. |
| CA-03 | Límites inválidos | Enviar límites inválidos y comprobar que el maestro no cambia. |
| CA-04 | Furgoneta inexistente | Editar un UUID ausente y comprobar recurso inexistente. |
| CA-05 | Acceso sin permisos | Editar con otro rol y comprobar rechazo. |

## 5. Reglas, datos e integraciones

- Solo los límites de carga son editables; la placa y el estado no se modifican en esta operación.
- Los límites deben ser mayores que cero; de lo contrario, se responde `400 Bad Request`.
- Los nuevos límites aplican a jornadas futuras. Las jornadas activas en F-06 conservan los valores originales con los que fueron creadas.
- Si la furgoneta no existe, se responde `404 Not Found`.
- Un usuario sin rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- La edición registra auditoría con usuario y marca temporal en UTC.

### Entradas

- Identificador de la furgoneta.
- Nuevo límite de peso en kg.
- Nuevo límite de volumen en m³.
- Nuevo máximo de paquetes en ruta.
- Identidad y roles obtenidos del JWT.

### Salidas

- Furgoneta actualizada con los nuevos límites.
- Registro de auditoría.

### Integraciones

- F-06 utiliza los límites vigentes al momento de crear la asignación diaria.
- La ruta, cuerpos y códigos se rigen por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `PUT /api/v1/furgonetas/{idFurgoneta}`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

## 6. Criterios de aceptación

### CA-01. Edición exitosa de límites

- **DADO** una furgoneta con límites de 500 kg, 4.0 m³ y 80 paquetes.
- **CUANDO** el Gestor cambia los límites a 600 kg, 5.0 m³ y 100 paquetes y confirma.
- **ENTONCES** el sistema actualiza los límites y registra la auditoría.

### CA-02. Límites aplican solo a jornadas futuras

- **DADO** una furgoneta con jornada activa en F-06 con límites de 500 kg.
- **CUANDO** el Gestor cambia el límite de peso a 600 kg.
- **ENTONCES** la jornada activa conserva los 500 kg; las nuevas jornadas usarán 600 kg.

### CA-03. Límites inválidos

- **DADO** una furgoneta existente.
- **CUANDO** el Gestor envía un límite de peso igual a cero.
- **ENTONCES** el sistema responde `400 Bad Request` y no modifica la furgoneta.

### CA-04. Furgoneta inexistente

- **DADO** un identificador que no corresponde a ninguna furgoneta.
- **CUANDO** se intenta editar.
- **ENTONCES** el sistema responde `404 Not Found`.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta editar una furgoneta.
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
| CA-01 | Edición exitosa de límites; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-02 | Límites aplican solo a jornadas futuras; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-03 | Límites inválidos; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-04 | Furgoneta inexistente; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-05 | Acceso sin permisos; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |

- [ ] Todos los CA/CUI y requisitos no funcionales del alcance tienen aceptación completa.
- [ ] Las dependencias reales y la revisión humana se verificaron.
- [ ] La verificación local y sus límites están registrados.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-02 y CA-10.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
