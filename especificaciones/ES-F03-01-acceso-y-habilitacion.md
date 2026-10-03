# ES-F03-01: Acceso y habilitación operativa del repartidor

**Funcionalidad padre:** F-03 — Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** Max Rojas  
**Estado:** Borrador  
**Actor principal:** Repartidor

## 1. Objetivo

Permitir el ingreso a la vista de campo únicamente a usuarios con rol `REPARTIDOR` vinculados a un repartidor activo en F-05, y determinar si ese repartidor puede ejecutar cambios de estado (en turno) o solo consultar información (fuera de turno).

Con esto se garantiza que ningún despacho sea operado por alguien no autorizado y que solo el personal en turno registre transiciones.

## 2. Actor y precondiciones

- Actor: repartidor desde su celular.
- Rol requerido: `REPARTIDOR` en el JWT emitido por Seguridad y Usuarios.
- El identificador de usuario del token está vinculado a un repartidor registrado y activo en F-05.
- Para habilitar transiciones: asignación diaria activa y estado operativo `DISPONIBLE`, `EN_RUTA` o `SATURADO`.
- Existe conexión activa.

## 3. Flujo principal

1. El repartidor abre la vista web y se autentica.
2. El sistema valida el JWT (vigencia y rol `REPARTIDOR`).
3. El sistema resuelve, mediante F-05, el repartidor vinculado al identificador de usuario del token.
4. El sistema consulta en F-05 el estado operativo y la asignación diaria del repartidor.
5. Si el repartidor está en turno, el sistema habilita las acciones de cambio de estado; si está `FUERA_DE_TURNO`, habilita solo la consulta de ruta y resumen.
6. El sistema muestra la vista "Mi Ruta".

## 4. Reglas y validaciones

- El repartidor se resuelve siempre desde el token; el backend no confía en identificadores enviados por el cliente.
- Solicitud sin token o con token vencido: `401 Unauthorized`, sin exponer información de despachos.
- Token con rol distinto de `REPARTIDOR`, o usuario no vinculado a un repartidor activo: `403 Forbidden`.
- Repartidor `FUERA_DE_TURNO`: puede consultar su ruta y su resumen del día; toda transición se rechaza con `409 Conflict` indicando que su turno no está activo.
- La pantalla de acceso comunica el motivo del bloqueo (turno inactivo, rol incorrecto o usuario no vinculado).
- La interfaz oculta o deshabilita acciones no permitidas, pero la validación definitiva siempre ocurre en el backend.

## 5. Entradas, salidas e integraciones

### Entradas

- JWT con identificador de usuario y rol.

### Salidas

- Contexto del repartidor: identificador resuelto, estado operativo y habilitación para transiciones.
- Vista "Mi Ruta" en modo operativo o de solo lectura, o la respuesta de error correspondiente.

### Integraciones

- Seguridad y Usuarios: emisión y validación del JWT (acuerdo pendiente, Anexo C n.º 1 de F-03).
- F-05 Monitoreo de Flota: vínculo usuario–repartidor, estado operativo y asignación diaria.
- Ver `integraciones/api-contract.md` para rutas y códigos de respuesta.

## 6. Criterios de aceptación

### CA-01. Acceso exitoso (F-03 CA-01)

- **DADO** un repartidor vinculado, con asignación diaria activa y estado operativo `DISPONIBLE`.
- **CUANDO** se autentica desde su celular.
- **ENTONCES** el sistema muestra la vista "Mi Ruta" y habilita las acciones de cambio de estado.

### CA-02. Credencial ausente o expirada (F-03 CA-02)

- **DADO** una solicitud sin token o con token vencido.
- **CUANDO** se invoca cualquier recurso de la funcionalidad.
- **ENTONCES** el backend responde `401 Unauthorized` y no expone información de despachos.

### CA-03. Rol distinto o usuario no vinculado (F-03 CA-03)

- **DADO** un token válido cuyo rol no es `REPARTIDOR`, o cuyo usuario no está vinculado a un repartidor activo en F-05.
- **CUANDO** se invocan los recursos de operación de campo.
- **ENTONCES** el backend responde `403 Forbidden`.

### CA-04. Repartidor fuera de turno (F-03 CA-04)

- **DADO** un repartidor activo cuyo estado operativo en F-05 es `FUERA_DE_TURNO`.
- **CUANDO** accede a la aplicación.
- **ENTONCES** el sistema permite consultar su ruta y su resumen del día, pero rechaza toda transición con `409 Conflict` e informa que su turno no está activo.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Emisión de credenciales, gestión de contraseñas y del token (Seguridad y Usuarios).
- Registro de repartidores, asignación diaria y cambios de estado operativo (F-05).

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-01 y sección 8 (Seguridad).
- `integraciones/api-contract.md`.
- Wireframe de la pantalla de acceso de F-03.
