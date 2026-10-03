# ES-F05-01: Registrar un nuevo repartidor

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho registre un nuevo repartidor en el módulo con sus datos personales, licencia de conducir y turno habitual. Al confirmarse el registro, el sistema solicita automáticamente a Seguridad y Usuarios la creación de la cuenta del repartidor, iniciando el flujo de vinculación.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El DNI del nuevo repartidor no existe en el módulo.
- Los campos obligatorios son: nombres, apellidos, DNI, teléfono, correo electrónico, número de brevete y turno habitual.
- El módulo de Seguridad y Usuarios debe estar disponible para recibir la solicitud de creación de cuenta.

## 3. Flujo principal

1. El Gestor ingresa al panel de repartidores y selecciona `Nuevo repartidor`.
2. El frontend presenta el formulario con los campos obligatorios.
3. El Gestor completa los datos y confirma el registro.
4. El backend valida el rol, la completitud de los campos y la unicidad del DNI.
5. El sistema crea el repartidor con estado de registro `ACTIVO` y vinculación `PENDIENTE`.
6. El sistema solicita a Seguridad y Usuarios la creación del usuario con rol `REPARTIDOR`.
7. Se registra la auditoría del alta con usuario y marca temporal en UTC.
8. El frontend muestra el repartidor creado con su identificador y estado de vinculación.

## 4. Reglas y validaciones

- El DNI debe ser único en el módulo. Si ya existe, se rechaza con `409 Conflict`.
- Todos los campos obligatorios deben estar presentes y con formato válido; de lo contrario, se responde `400 Bad Request` con el detalle de los campos inválidos.
- El repartidor se crea siempre en estado de registro `ACTIVO` y estado de vinculación `PENDIENTE`.
- Si la solicitud a Seguridad y Usuarios falla o no responde, el repartidor se persiste igualmente, pero su vinculación queda en `ERROR` y el panel ofrece reintentar.
- Un usuario sin el rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- El registro no asigna jornada, furgoneta ni zona; eso corresponde a F-06.

## 5. Entradas, salidas e integraciones

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
- La ruta, cuerpos y códigos se rigen por `integraciones/api-contract.md` [cite: 2].

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

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Edición de datos del repartidor después del registro.
- Baja lógica del repartidor.
- Gestión completa de la vinculación y activación de la cuenta.
- Asignación de jornada, furgoneta o zona.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-01 y CA-01 a CA-03.
- [cite: 2] `integraciones/api-contract.md`.
- [cite: 3] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-03 y CA-14 a CA-15.
