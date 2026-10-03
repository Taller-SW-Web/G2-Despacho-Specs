# ES-F05-03: Editar datos del repartidor

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho modifique los datos de contacto, la licencia de conducir o el turno habitual de un repartidor existente, sin alterar su estado de registro ni su vinculación con Seguridad y Usuarios.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El repartidor existe en el módulo.
- Los campos editables son: teléfono, correo electrónico, número de brevete y turno habitual.
- El DNI no es editable porque es el identificador natural del repartidor.

## 3. Flujo principal

1. El Gestor selecciona `Editar` en la fila del repartidor desde el panel.
2. El frontend presenta el formulario con los datos actuales precargados.
3. El Gestor modifica los campos deseados y confirma.
4. El backend valida el rol, la existencia del repartidor y el formato de los campos.
5. El sistema actualiza los datos, registra la auditoría con el estado anterior y el nuevo, y responde con el repartidor actualizado.
6. El frontend muestra la confirmación del cambio.

## 4. Reglas y validaciones

- Solo los campos teléfono, correo, brevete y turno habitual son editables.
- El DNI, el estado de registro y el estado de vinculación no se modifican en esta operación.
- Los campos deben tener formato válido; de lo contrario, se responde `400 Bad Request`.
- Si el repartidor no existe, se responde `404 Not Found`.
- Un usuario sin rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- La edición registra auditoría con usuario y marca temporal en UTC.

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador del repartidor.
- Campos a modificar: teléfono, correo, brevete, turno habitual.
- Identidad y roles obtenidos del JWT.

### Salidas

- Repartidor actualizado con los nuevos datos.
- Registro de auditoría.

### Integraciones

- La ruta, cuerpos y códigos se rigen por `integraciones/api-contract.md` [cite: 2].

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

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Modificar el DNI, el estado de registro o el estado de vinculación.
- Dar de baja al repartidor.
- Registrar nuevos repartidores.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-01 y CA-03.
- [cite: 2] `integraciones/api-contract.md`.
