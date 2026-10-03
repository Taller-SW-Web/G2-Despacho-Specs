# ES-F05-08: Editar furgoneta y límites de carga

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho modifique los límites de carga de una furgoneta existente. Los nuevos límites se aplican a las jornadas futuras; las jornadas activas conservan los valores con los que fueron creadas.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- La furgoneta existe en el módulo.
- La furgoneta no tiene una jornada activa en el momento de la edición, o si la tiene, los nuevos límites solo se aplicarán a jornadas futuras.
- Los campos editables son: límite de peso (kg), límite de volumen (m³) y máximo de paquetes en ruta.
- La placa no es editable.

## 3. Flujo principal

1. El Gestor selecciona `Editar` en la fila de la furgoneta.
2. El frontend presenta el formulario con los datos actuales precargados.
3. El Gestor modifica los límites y confirma.
4. El backend valida el rol, la existencia de la furgoneta y que los límites sean mayores que cero.
5. El sistema actualiza los límites, registra la auditoría y responde con la furgoneta actualizada.
6. El frontend muestra la confirmación.

## 4. Reglas y validaciones

- Solo los límites de carga son editables; la placa y el estado no se modifican en esta operación.
- Los límites deben ser mayores que cero; de lo contrario, se responde `400 Bad Request`.
- Los nuevos límites aplican a jornadas futuras. Las jornadas activas en F-06 conservan los valores originales con los que fueron creadas.
- Si la furgoneta no existe, se responde `404 Not Found`.
- Un usuario sin rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- La edición registra auditoría con usuario y marca temporal en UTC.

## 5. Entradas, salidas e integraciones

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
- La ruta, cuerpos y códigos se rigen por `integraciones/api-contract.md` [cite: 2].

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

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Cambiar el estado de la furgoneta.
- Modificar la placa.
- Registrar nuevas furgonetas.
- Recalcular la ocupación de una jornada activa con los nuevos límites.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-02 y CA-10.
- [cite: 2] `integraciones/api-contract.md`.
