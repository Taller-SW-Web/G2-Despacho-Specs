# ES-F05-01: Registrar un nuevo repartidor

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Borrador migrado a SDD; revisión funcional y aceptación pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; nuevo repartidor desde el catálogo administrativo `/repartidores`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> Migración estructural desde `ES-F05-01-RegistrarRepartidor.md`, revisión `f3849d9`. Se conservan las reglas y los criterios originales, incluidos sus IDs. Las discrepancias detectadas se registran en §7 y en el plan; esta migración no aprueba cambios de contrato ni acredita integración desplegada.

## 1. Contexto y objetivo

Permitir que el Gestor de Despacho registre un nuevo repartidor en el módulo con sus datos personales, licencia de conducir y turno habitual. Al confirmarse el registro, el sistema solicita automáticamente a Seguridad y Usuarios la creación de la cuenta del repartidor, iniciando el flujo de vinculación.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Datos personales, contacto, brevete, turno habitual y resultado del registro.
- Resultado del comportamiento: Perfil local identificable, con estados y auditoría conforme a los criterios conservados.

### Fuera de alcance

- Edición de datos del repartidor después del registro.
- Baja lógica del repartidor.
- Gestión completa de la vinculación y activación de la cuenta.
- Asignación de jornada, furgoneta o zona.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El DNI del nuevo repartidor no existe en el módulo.
- Los campos obligatorios son: nombres, apellidos, DNI, teléfono, correo electrónico, número de brevete y turno habitual.
- El módulo de Seguridad y Usuarios debe estar disponible para recibir la solicitud de creación de cuenta.

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Nuevo repartidor en `/repartidores`, conforme al flujo conservado.
- Resultado exitoso: Perfil local identificable, con estados y auditoría conforme a los criterios conservados.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. El Gestor ingresa al panel de repartidores y selecciona `Nuevo repartidor`.
2. El frontend presenta el formulario con los campos obligatorios.
3. El Gestor completa los datos y confirma el registro.
4. El backend valida el rol, la completitud de los campos y la unicidad del DNI.
5. El sistema crea el repartidor con estado de registro `ACTIVO` y vinculación `PENDIENTE`.
6. El sistema solicita a Seguridad y Usuarios la creación del usuario con rol `REPARTIDOR`.
7. Se registra la auditoría del alta con usuario y marca temporal en UTC.
8. El frontend muestra el repartidor creado con su identificador y estado de vinculación.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Registro exitoso | Crear con todos los campos válidos y revisar estados, identificador y auditoría; contrastar el efecto externo pendiente. |
| CA-02 | DNI duplicado | Repetir el DNI y comprobar conflicto sin alta adicional. |
| CA-03 | Datos incompletos o inválidos | Enviar campos ausentes o inválidos y comprobar errores sin persistencia. |
| CA-04 | Fallo en la comunicación con Seguridad | Simular fallo de Seguridad solo después de conciliar el flujo con el contrato externo. |
| CA-05 | Acceso sin permisos | Intentar registrar con otro rol y comprobar rechazo sin escritura. |

## 5. Reglas, datos e integraciones

- El DNI debe ser único en el módulo. Si ya existe, se rechaza con `409 Conflict`.
- Todos los campos obligatorios deben estar presentes y con formato válido; de lo contrario, se responde `400 Bad Request` con el detalle de los campos inválidos.
- El repartidor se crea siempre en estado de registro `ACTIVO` y estado de vinculación `PENDIENTE`.
- Si la solicitud a Seguridad y Usuarios falla o no responde, el repartidor se persiste igualmente, pero su vinculación queda en `ERROR` y el panel ofrece reintentar.
- Un usuario sin el rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- El registro no asigna jornada, furgoneta ni zona; eso corresponde a F-06.

### Entradas

- Nombres del repartidor.
- Apellidos del repartidor.
- DNI (documento de identidad).
- Teléfono.
- Correo electrónico.
- Número de brevete.
- Turno habitual.
- Identidad y roles obtenidos del JWT.

### Salidas

- Repartidor creado con identificador único, estado de registro `ACTIVO` y vinculación `PENDIENTE`.
- Registro de auditoría con usuario, operación y marca temporal en UTC.
- Solicitud enviada a Seguridad y Usuarios para la creación de la cuenta.

### Integraciones

- Seguridad y Usuarios recibe la solicitud de creación de cuenta con rol `REPARTIDOR`.
- La vinculación posterior se gestiona en ES-F05-05.
- La ruta, cuerpos y códigos se rigen por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `POST /api/v1/repartidores`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

## 6. Criterios de aceptación

### CA-01. Registro exitoso

- **DADO** que el Gestor ingresa nombres, apellidos, DNI, teléfono, correo, brevete y turno habitual válidos.
- **CUANDO** confirma el registro.
- **ENTONCES** el sistema crea el repartidor `ACTIVO` con vinculación `PENDIENTE`, solicita a Seguridad la creación del usuario y devuelve el identificador del repartidor.

### CA-02. DNI duplicado

- **DADO** un repartidor existente con un DNI determinado.
- **CUANDO** se intenta registrar otro repartidor con el mismo DNI.
- **ENTONCES** el sistema responde `409 Conflict` sin persistir el duplicado.

### CA-03. Datos incompletos o inválidos

- **DADO** un formulario con campos obligatorios vacíos o con formato inválido.
- **CUANDO** el Gestor intenta confirmar el registro.
- **ENTONCES** el sistema responde `400 Bad Request` detallando los campos inválidos.

### CA-04. Fallo en la comunicación con Seguridad

- **DADO** que Seguridad y Usuarios no responde o rechaza la solicitud.
- **CUANDO** se completa el registro del repartidor.
- **ENTONCES** el repartidor se persiste como `ACTIVO` con vinculación `ERROR` y el panel ofrece reintentar la vinculación.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta registrar un repartidor.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. UI, backend y requisitos no funcionales

- UI: interacción, estados y criterios CUI en [ui.md](./ui.md); reutilización de los [componentes compartidos](../../disenio/componentes-react.md).
- Backend: Registrar el perfil maestro del repartidor y registrar el alta con auditoría. Propiedad local de `repartidores`; no acceder a la base de Gestión.
- Requisitos no funcionales: Confirmar consistencia de datos, permisos y auditoría; comprobar cancelación, repetición y concurrencia cuando afecten el resultado.
- Seguridad y datos: no mostrar credenciales, tokens ni errores técnicos en la interfaz; la habilitación visual no reemplaza la autorización del backend.
- Pendiente funcional P-01: La especificación original exige creación automática, rol global REPARTIDOR y estado ERROR; Operación §4.1 y Seguridad §8.4 describen asociación manual y niegan ese rol global. CA-01 y CA-04 requieren conciliación funcional antes de aceptarse.
- Responsable de P-01: Rhamses coordina con Arquitectura y Seguridad; la revisión afecta los criterios indicados y debe resolverse antes de declarar la aceptación completa.
- Las implementaciones existentes se referencian en [evidence.md](./evidence.md). Su existencia no reemplaza la comprobación individual de los criterios conservados.

## 8. Verificación y completitud

| Criterio | Comprobación prevista | Nivel y preparación |
|---|---|---|
| CA-01 | Crear con todos los campos válidos y revisar estados, identificador y auditoría; contrastar el efecto externo pendiente. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-02 | Repetir el DNI y comprobar conflicto sin alta adicional. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-03 | Enviar campos ausentes o inválidos y comprobar errores sin persistencia. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-04 | Simular fallo de Seguridad solo después de conciliar el flujo con el contrato externo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-05 | Intentar registrar con otro rol y comprobar rechazo sin escritura. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |

- [ ] Todos los criterios y CUI cuentan con resultados por caso en [evidence.md](./evidence.md).
- [ ] P-01 está resuelto en los documentos propietarios y revisado por el equipo.
- [ ] Los datos, el contrato y la implementación son consistentes.
- [ ] Las dependencias simuladas y la integración real pendiente se identifican expresamente.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-01 y CA-01 a CA-03.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [cite: 3] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-03 y CA-14 a CA-15.
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
