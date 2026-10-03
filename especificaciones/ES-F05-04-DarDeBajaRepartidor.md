# ES-F05-04: Dar de baja lógica al repartidor

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho cambie el estado de registro de un repartidor a `INACTIVO`, excluyéndolo de futuras asignaciones y del acceso a F-03, pero conservando su registro y todo su historial operativo.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El repartidor existe y su estado de registro es `ACTIVO`.
- El repartidor no tiene despachos en estado `ASIGNADO` ni `EN_CAMINO`.

## 3. Flujo principal

1. El Gestor selecciona `Dar de baja` en la fila del repartidor.
2. El frontend solicita confirmación indicando que el repartidor será excluido de nuevas asignaciones.
3. El Gestor confirma la operación.
4. El backend valida el rol, el estado de registro actual y la ausencia de despachos en curso.
5. El sistema cambia el estado de registro a `INACTIVO` y registra la auditoría.
6. El frontend actualiza la fila del repartidor con el nuevo estado.

## 4. Reglas y validaciones

- Solo se puede dar de baja a un repartidor cuyo estado de registro sea `ACTIVO`.
- Si el repartidor tiene despachos `ASIGNADO` o `EN_CAMINO`, la operación se rechaza con `409 Conflict` indicando que tiene despachos en curso.
- La baja es lógica: el registro se conserva con todo su historial.
- Un repartidor `INACTIVO` no puede recibir asignaciones diarias en F-06 ni acceder a F-03.
- Si el repartidor ya está `INACTIVO`, el sistema informa que la baja ya fue procesada.
- Un usuario sin rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- La auditoría registra el usuario, el estado anterior, el estado nuevo y la marca temporal en UTC.

## 5. Entradas, salidas e integraciones

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
- La ruta y códigos se rigen por `integraciones/api-contract.md` [cite: 2].

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

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Eliminar físicamente el registro del repartidor.
- Reactivar un repartidor dado de baja.
- Reasignar despachos en curso a otro repartidor.
- Revocar o desactivar la cuenta en Seguridad y Usuarios.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-01, CA-04 y CA-05.
- [cite: 2] `integraciones/api-contract.md`.
