# ES-F05-09: Cambiar estado de furgoneta

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho cambie el estado de una furgoneta entre `DISPONIBLE`, `EN_MANTENIMIENTO` y `FUERA_DE_SERVICIO`, controlando que no se retire una furgoneta que tiene despachos en curso en una jornada activa.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- La furgoneta existe en el módulo.
- Las transiciones válidas son:
  - `DISPONIBLE` → `EN_MANTENIMIENTO`
  - `DISPONIBLE` → `FUERA_DE_SERVICIO`
  - `EN_MANTENIMIENTO` → `DISPONIBLE`
  - `EN_MANTENIMIENTO` → `FUERA_DE_SERVICIO`
  - `FUERA_DE_SERVICIO` → `DISPONIBLE` (rehabilitación)

## 3. Flujo principal

1. El Gestor selecciona la acción de cambio de estado en la fila de la furgoneta.
2. El frontend muestra el estado actual y las transiciones válidas.
3. El Gestor selecciona el nuevo estado y confirma.
4. El backend valida el rol, la existencia, la transición válida y la ausencia de conflictos con jornadas activas.
5. El sistema actualiza el estado, gestiona la jornada activa si corresponde y registra la auditoría.
6. El frontend actualiza la fila con el nuevo estado.

## 4. Reglas y validaciones

- Si la furgoneta tiene una jornada activa con despachos `ASIGNADO` o `EN_CAMINO`, el cambio a `EN_MANTENIMIENTO` o `FUERA_DE_SERVICIO` se rechaza con `409 Conflict`.
- Si la furgoneta tiene jornada activa sin despachos en curso, la jornada se cierra y el repartidor pasa a `FUERA_DE_TURNO` en F-06.
- Una furgoneta en `EN_MANTENIMIENTO` o `FUERA_DE_SERVICIO` queda excluida de nuevas asignaciones diarias en F-06.
- `FUERA_DE_SERVICIO` representa un retiro definitivo, pero se conserva el historial.
- Un usuario sin rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- La auditoría registra usuario, estado anterior, estado nuevo y marca temporal en UTC.

## 5. Entradas, salidas e integraciones

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
- La ruta y códigos se rigen por `integraciones/api-contract.md` [cite: 2].

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

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Editar los límites de carga de la furgoneta.
- Registrar nuevas furgonetas.
- Reasignar despachos en curso a otra furgoneta.
- Gestionar la logística de mantenimiento del vehículo.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-02, CA-11 y CA-12.
- [cite: 2] `integraciones/api-contract.md`.
