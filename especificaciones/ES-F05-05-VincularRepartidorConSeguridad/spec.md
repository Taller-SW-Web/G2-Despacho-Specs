# ES-F05-05: Vincular repartidor con Seguridad y Usuarios

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Implementación y automatización verificadas; Seguridad real y revisión humana pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; formulario de asociación manual desde el catálogo de repartidores.

**Servicio propietario:** Operación de Reparto y Flota.

> La migración SDD se conserva en el historial. Esta revisión alinea los comportamientos con Operación §4.1 y Seguridad §8.4; mantiene los IDs de criterios y registra los cambios funcionales en la evidencia.

## 1. Contexto y objetivo

Asociar un perfil local al `usuario_id` de una cuenta creada previamente por el canal administrativo de Seguridad. La asociación se realiza por el Gestor con un UUID; Despacho no crea la cuenta ni gestiona su activación o contraseña. El acceso posterior resuelve el perfil mediante el `sub` del JWT [cite: 1, 2].

## 2. Alcance

- Incluye asociación manual, unicidad, auditoría, repetición idempotente y rechazos del vínculo.
- Fuera de alcance: crear/activar/bloquear cuentas globales, solicitar contraseñas, sustituir una cuenta ya vinculada o implementar reintentos de provisión remota.

## 3. Actor, precondiciones y resultados

- Actor autenticado con `GESTOR_DESPACHO`.
- Perfil existente y `ACTIVO`.
- Identificador UUID comunicado por el canal administrativo de Seguridad.
- Disparador: `Vincular cuenta` desde `/repartidores`.
- Resultado: vínculo `VINCULADO` y auditoría; ante rechazo se conserva el estado anterior.
- La existencia/activación global de la cuenta es una precondición externa; esta operación local no demuestra una comprobación remota.

## 4. Flujo principal y alternativas

1. Seleccionar un repartidor activo y pendiente.
2. Introducir el UUID comunicado por Seguridad.
3. Validar autorización, formato, existencia y estado del perfil.
4. Comprobar unicidad de la cuenta y confirmar vínculo y auditoría juntos.
5. Responder sin cuerpo y actualizar el catálogo.
6. Si el mismo vínculo ya existe, confirmar sin otra auditoría; rechazar un cambio de cuenta.

## 5. Reglas, datos e integraciones

- Se recibe únicamente `usuarioId` UUID; no se aceptan credenciales ni campos ajenos.
- Un perfil activo/pendiente cambia a `VINCULADO`; se conserva su estado de registro.
- Un usuarioId pertenece como máximo a un perfil, incluso con solicitudes concurrentes.
- Repetir el vínculo del mismo perfil activo es idempotente.
- Perfil inactivo, cuenta ya asociada o intento de sustituir un vínculo: conflicto sin cambios.
- Perfil inexistente: recurso no encontrado; formato inválido: error de campos.
- Auditoría y vínculo se confirman o revierten en una transacción.
- Estados locales: `PENDIENTE` y `VINCULADO`; no hay rol global `REPARTIDOR` ni estados de provisión remota.
- Fuente única de formato y códigos: [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).

## 6. Criterios de aceptación

### CA-01. Vinculación manual exitosa

- **DADO** un perfil `ACTIVO` y `PENDIENTE` y el UUID de una cuenta creada previamente en Seguridad.
- **CUANDO** el Gestor autorizado asocia ese identificador.
- **ENTONCES** el perfil queda `VINCULADO`, conserva su estado de registro, guarda el UUID único y registra una auditoría.

### CA-02. Identificador de usuario inválido

- **DADO** un usuarioId ausente o con formato no UUID.
- **CUANDO** se intenta asociar la cuenta.
- **ENTONCES** se responde 400 y el perfil y su auditoría permanecen sin cambios.

### CA-03. Cuenta asociada a otro repartidor

- **DADO** una cuenta ya vinculada a otro perfil.
- **CUANDO** se intenta asociarla a un perfil distinto.
- **ENTONCES** se responde 409 y se conservan los vínculos existentes.

### CA-04. Perfil inactivo

- **DADO** un repartidor `INACTIVO`.
- **CUANDO** se intenta vincular una cuenta.
- **ENTONCES** se responde 409 sin crear ni modificar el vínculo.

### CA-05. Repetición idempotente

- **DADO** un perfil `ACTIVO` ya `VINCULADO` a un usuarioId.
- **CUANDO** se repite la asociación del mismo identificador.
- **ENTONCES** se responde 204 y no se duplica el vínculo ni la auditoría.

### CA-06. Cambio de cuenta no permitido

- **DADO** un perfil `VINCULADO` a una cuenta.
- **CUANDO** se intenta sustituirla por un usuarioId diferente.
- **ENTONCES** se responde 409 y se conserva la cuenta original.

### CA-07. Acceso sin permisos

- **DADO** un usuario sin `GESTOR_DESPACHO` o un token de servicio.
- **CUANDO** intenta asociar una cuenta.
- **ENTONCES** se responde 403 antes de leer o modificar el vínculo.

## 7. UI, backend y requisitos no funcionales

- UI: [interacción y criterios CUI](./ui.md), con controles compartidos y estados de consulta distintos.
- Backend: Operación valida identidad y rol, aplica las reglas del catálogo y conserva sus datos; no consulta las tablas de Gestión.
- Acuerdos locales: los DTO, límites, estados, errores e idempotencia están definidos en Operación §4.1 y contrastados con ambos repositorios.
- Requisitos no funcionales: Conservar autorización, datos y auditoría; comprobar repetición y concurrencia cuando afecten el resultado.
- Pendientes externos: aceptación con Seguridad real; revisión visual humana y efectos de los consumidores F-03/F-06 que excedan las comprobaciones locales.
- [Evidencia](./evidence.md) distingue las comprobaciones locales, los dobles y los criterios todavía pendientes.

## 8. Verificación y completitud

| Criterio | Comprobación | Evidencia |
|---|---|---|
| CA-01 | Vinculación manual exitosa; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-02 | Identificador de usuario inválido; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-03 | Cuenta asociada a otro repartidor; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-04 | Perfil inactivo; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-05 | Repetición idempotente; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-06 | Cambio de cuenta no permitido; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-07 | Acceso sin permisos; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |

- [ ] Todos los CA/CUI y requisitos no funcionales del alcance tienen aceptación completa.
- [ ] Las dependencias reales y la revisión humana se verificaron.
- [ ] La verificación local y sus límites están registrados.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-03 y CA-14 a CA-16.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [cite: 3] [overview.md](../../overview.md), integración con Seguridad y Usuarios.
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
