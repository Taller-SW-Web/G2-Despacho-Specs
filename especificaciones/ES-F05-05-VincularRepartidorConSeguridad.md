# ES-F05-05: Vincular repartidor con Seguridad y Usuarios

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Sistema / Gestor de Despacho

## 1. Objetivo

Gestionar el ciclo de vinculación entre un repartidor del módulo y su cuenta de usuario en Seguridad y Usuarios. El proceso abarca la solicitud de creación de cuenta, la recepción del identificador de usuario, el seguimiento de la activación y el reintento ante fallos. Un repartidor `VINCULADO` puede ser identificado por F-03 a través de su token JWT.

## 2. Actor y precondiciones

- La solicitud inicial de creación se dispara automáticamente al registrar un repartidor (ES-F05-01).
- El reintento manual lo ejecuta el Gestor de Despacho autenticado con rol `GESTOR_DESPACHO`.
- El repartidor existe y su estado de vinculación es `PENDIENTE` o `ERROR`.
- El módulo de Seguridad y Usuarios está integrado mediante API.

## 3. Flujo principal

1. Al registrar un repartidor, el sistema envía a Seguridad y Usuarios una solicitud de creación de cuenta con rol `REPARTIDOR`.
2. Si Seguridad responde exitosamente, el sistema guarda el identificador de usuario y cambia la vinculación a `PENDIENTE_ACTIVACION`.
3. Cuando Seguridad confirma que la cuenta fue activada y el repartidor puede iniciar sesión, el sistema cambia la vinculación a `VINCULADO`.
4. Si Seguridad no responde o rechaza la creación, la vinculación queda en `ERROR`.
5. El Gestor puede seleccionar `Reintentar vinculación` en el panel para repartidores en `ERROR`.
6. Cada cambio de estado de vinculación se registra con auditoría.

## 4. Reglas y validaciones

- Los estados de vinculación siguen la progresión: `PENDIENTE` → `PENDIENTE_ACTIVACION` → `VINCULADO`, o `PENDIENTE` / `PENDIENTE_ACTIVACION` → `ERROR`.
- El reintento solo está disponible para repartidores en estado `ERROR`.
- Un repartidor con vinculación distinta de `VINCULADO` no puede recibir asignaciones diarias en F-06.
- La vinculación no modifica el estado de registro (`ACTIVO` / `INACTIVO`) del repartidor.
- El identificador de usuario devuelto por Seguridad se almacena para que F-03 pueda identificar al repartidor desde el token.
- Si la activación tarda, el repartidor permanece en `PENDIENTE_ACTIVACION` hasta que Seguridad confirme.

## 5. Entradas, salidas e integraciones

### Entradas

- Datos del repartidor para la solicitud de creación (nombres, apellidos, correo, DNI).
- Identificador del repartidor para el reintento.
- Identidad y roles obtenidos del JWT (para reintento manual).

### Salidas

- Estado de vinculación actualizado: `PENDIENTE_ACTIVACION`, `VINCULADO` o `ERROR`.
- Identificador de usuario de Seguridad almacenado.
- Registro de auditoría por cada cambio de estado.

### Integraciones

- Seguridad y Usuarios: creación de cuenta, confirmación de activación y devolución del identificador de usuario.
- F-03 identifica al repartidor mediante el identificador de usuario vinculado.
- F-06 requiere vinculación `VINCULADO` para las asignaciones diarias.
- La comunicación se rige por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Vinculación y activación exitosas

- **DADO** el registro de un nuevo repartidor.
- **CUANDO** Seguridad crea la cuenta, devuelve su identificador y posteriormente confirma la activación.
- **ENTONCES** el sistema guarda el identificador, progresa por `PENDIENTE_ACTIVACION` y finalmente marca al repartidor como `VINCULADO`.

### CA-02. Seguridad no responde

- **DADO** que Seguridad y Usuarios no responde a la solicitud de creación.
- **CUANDO** se registra el repartidor.
- **ENTONCES** el repartidor queda con vinculación `ERROR` y el panel ofrece reintentar.

### CA-03. Seguridad rechaza la creación

- **DADO** que Seguridad y Usuarios rechaza la solicitud.
- **CUANDO** se registra el repartidor.
- **ENTONCES** el repartidor queda con vinculación `ERROR` y el panel ofrece reintentar.

### CA-04. Cuenta pendiente de activación

- **DADO** que Seguridad creó la cuenta pero aún no fue activada.
- **CUANDO** se consulta el repartidor.
- **ENTONCES** su vinculación aparece como `PENDIENTE_ACTIVACION` y no puede recibir asignaciones diarias.

### CA-05. Reintento exitoso

- **DADO** un repartidor con vinculación `ERROR`.
- **CUANDO** el Gestor selecciona reintentar y Seguridad responde exitosamente.
- **ENTONCES** el sistema guarda el identificador de usuario y la vinculación progresa a `PENDIENTE_ACTIVACION`.

### CA-06. Reintento fallido

- **DADO** un repartidor con vinculación `ERROR`.
- **CUANDO** el Gestor selecciona reintentar y Seguridad no responde.
- **ENTONCES** la vinculación permanece en `ERROR` y se permite reintentar nuevamente.

### CA-07. Reintento con vinculación no aplicable

- **DADO** un repartidor con vinculación `VINCULADO`.
- **CUANDO** se intenta reintentar la vinculación.
- **ENTONCES** el sistema informa que el repartidor ya está vinculado.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Gestionar credenciales, contraseñas o tokens del repartidor.
- Activar o desactivar cuentas directamente en Seguridad y Usuarios.
- Revocar la vinculación al dar de baja al repartidor.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-03 y CA-14 a CA-16.
- [cite: 2] `integraciones/api-contract.md`.
- [cite: 3] `overview.md`, integración con Seguridad y Usuarios.
