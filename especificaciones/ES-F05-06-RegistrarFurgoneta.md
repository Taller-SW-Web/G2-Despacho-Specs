# ES-F05-06: Registrar una nueva furgoneta

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho registre una furgoneta en el módulo, definiendo su placa identificadora y sus límites de carga (peso en kg, volumen en m³ y máximo de paquetes en ruta). La furgoneta queda disponible para ser asignada a jornadas operativas en F-06.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- La placa de la furgoneta no existe en el módulo.
- Los campos obligatorios son: placa, límite de peso (kg), límite de volumen (m³) y máximo de paquetes en ruta.
- Los límites de carga deben ser mayores que cero.

## 3. Flujo principal

1. El Gestor ingresa al panel de furgonetas y selecciona `Nueva furgoneta`.
2. El frontend presenta el formulario con los campos obligatorios.
3. El Gestor completa los datos y confirma el registro.
4. El backend valida el rol, la completitud, el formato y la unicidad de la placa.
5. El sistema crea la furgoneta con estado `DISPONIBLE` y los límites definidos.
6. Se registra la auditoría del alta con usuario y marca temporal en UTC.
7. El frontend muestra la furgoneta creada en el panel.

## 4. Reglas y validaciones

- La placa debe ser única en el módulo. Si ya existe, se rechaza con `409 Conflict`.
- Los límites de peso, volumen y paquetes deben ser mayores que cero. Si alguno es inválido, se responde `400 Bad Request`.
- La furgoneta se crea siempre con estado `DISPONIBLE`.
- Un usuario sin el rol `GESTOR_DESPACHO` recibe `403 Forbidden`.

## 5. Entradas, salidas e integraciones

### Entradas

- Placa de la furgoneta.
- Límite de peso en kg.
- Límite de volumen en m³.
- Máximo de paquetes en ruta.
- Identidad y roles obtenidos del JWT.

### Salidas

- Furgoneta creada con identificador, placa, límites y estado `DISPONIBLE`.
- Registro de auditoría.

### Integraciones

- F-06 consume las furgonetas `DISPONIBLE` para las asignaciones diarias.
- La ruta, cuerpos y códigos se rigen por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Registro exitoso

- **DADO** una furgoneta con placa "ABC-123", 500 kg, 4.0 m³ y máximo de 80 paquetes.
- **CUANDO** el Gestor confirma el registro.
- **ENTONCES** el sistema la guarda en estado `DISPONIBLE` con esos límites y registra la auditoría.

### CA-02. Placa duplicada

- **DADO** una furgoneta existente con placa "ABC-123".
- **CUANDO** se intenta registrar otra con la misma placa.
- **ENTONCES** el sistema responde `409 Conflict` sin persistir el duplicado.

### CA-03. Límites inválidos

- **DADO** un formulario con peso igual a cero o negativo.
- **CUANDO** el Gestor intenta confirmar el registro.
- **ENTONCES** el sistema responde `400 Bad Request` detallando los campos inválidos.

### CA-04. Datos incompletos

- **DADO** un formulario sin placa o sin alguno de los límites.
- **CUANDO** el Gestor intenta confirmar.
- **ENTONCES** el sistema responde `400 Bad Request`.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta registrar una furgoneta.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Editar los límites de carga después del registro.
- Cambiar el estado de la furgoneta.
- Asignar la furgoneta a una jornada operativa.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-02 y CA-08 a CA-09.
- [cite: 2] `integraciones/api-contract.md`.
