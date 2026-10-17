# ES-F05-03: Editar datos del repartidor

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Borrador migrado a SDD; revisión funcional y aceptación pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; editar desde el catálogo administrativo `/repartidores`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> Migración estructural desde `ES-F05-03-EditarRepartidor.md`, revisión `f3849d9`. Se conservan las reglas y los criterios originales, incluidos sus IDs. Las discrepancias detectadas se registran en §7 y en el plan; esta migración no aprueba cambios de contrato ni acredita integración desplegada.

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

- UI: interacción, estados y criterios CUI en [ui.md](./ui.md); reutilización de los [componentes compartidos](../../disenio/componentes-react.md).
- Backend: Actualizar contacto, brevete y turno preservando identidad y estados del repartidor. Propiedad local de `repartidores`; no acceder a la base de Gestión.
- Requisitos no funcionales: Confirmar consistencia de datos, permisos y auditoría; comprobar cancelación, repetición y concurrencia cuando afecten el resultado.
- Seguridad y datos: no mostrar credenciales, tokens ni errores técnicos en la interfaz; la habilitación visual no reemplaza la autorización del backend.
- Pendiente funcional P-01: Precisar en el contrato de Operación los DTO y errores de campo pendientes de ratificación (DC-04 del diseño compartido); la adaptación de transporte existente no es por sí sola aprobación contractual.
- Responsable de P-01: Rhamses coordina con Arquitectura; la revisión afecta los criterios indicados y debe resolverse antes de declarar la aceptación completa.
- Las implementaciones existentes se referencian en [evidence.md](./evidence.md). Su existencia no reemplaza la comprobación individual de los criterios conservados.

## 8. Verificación y completitud

| Criterio | Comprobación prevista | Nivel y preparación |
|---|---|---|
| CA-01 | Cambiar el teléfono del escenario y comprobar los estados y la auditoría. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-02 | Enviar correo inválido y comprobar que todos los datos previos se conservan. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-03 | Editar un UUID ausente y comprobar recurso inexistente. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-04 | Editar con otro rol y comprobar rechazo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |

- [ ] Todos los criterios y CUI cuentan con resultados por caso en [evidence.md](./evidence.md).
- [ ] P-01 está resuelto en los documentos propietarios y revisado por el equipo.
- [ ] Los datos, el contrato y la implementación son consistentes.
- [ ] Las dependencias simuladas y la integración real pendiente se identifican expresamente.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-01 y CA-03.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
