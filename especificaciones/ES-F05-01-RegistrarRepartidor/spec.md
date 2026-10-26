# ES-F05-01: Registrar un nuevo repartidor

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Implementación y automatización verificadas; Seguridad real y revisión humana pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; nuevo repartidor desde el catálogo administrativo `/repartidores`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> La migración SDD se conserva en el historial. Esta revisión alinea los comportamientos con Operación §4.1 y Seguridad §8.4; mantiene los IDs de criterios y registra los cambios funcionales en la evidencia.

## 1. Contexto y objetivo

Permitir al Gestor registrar el perfil maestro con datos personales, contacto, brevete y turno. El alta es local: queda `ACTIVO` y `PENDIENTE` hasta que el Gestor asocia la cuenta existente mediante ES-F05-05 [cite: 1].

## 2. Alcance

- Incluye: Datos personales, contacto, brevete, turno habitual y resultado del registro.
- Resultado del comportamiento: Perfil local identificable, con estados y auditoría conforme a los criterios conservados.

### Fuera de alcance

- Edición de datos del repartidor después del registro.
- Baja lógica del repartidor.
- Creación, activación y modificación de la cuenta global, que pertenecen a Seguridad.
- Asignación de jornada, furgoneta o zona.

## 3. Actor, precondiciones y resultados

- Actor: Gestor autenticado con `GESTOR_DESPACHO`.
- DNI y correo únicos; datos válidos conforme a [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas).
- Disparador: `Nuevo repartidor` desde `/repartidores`.
- Resultado: perfil `ACTIVO`/`PENDIENTE` con usuarioId nulo y auditoría local.
- Seguridad autoriza el token; no se invoca un alta remota de cuentas como efecto de este registro.

## 4. Flujo principal y alternativas

1. Abrir el formulario y completar los siete campos.
2. Validar campos y autorización.
3. Comprobar unicidad y persistir el perfil local con su auditoría.
4. Devolver el recurso creado y su ubicación.
5. Refrescar el catálogo; la vinculación manual queda disponible como operación separada.

## 5. Reglas, datos e integraciones

- DNI y correo deben ser únicos; un conflicto no produce altas ni auditorías adicionales.
- El perfil se crea `ACTIVO/PENDIENTE`, con `usuarioId=null`.
- Nombres, apellidos, DNI y datos de contacto/turno cumplen los límites definidos exclusivamente en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas).
- No se asignan jornada, vehículo ni zona y no se crea una cuenta global.
- Registro y auditoría son atómicos; el actor procede del JWT.
- La cuenta se crea mediante el canal de Seguridad y se asocia en [ES-F05-05](../ES-F05-05-VincularRepartidorConSeguridad/spec.md).

## 6. Criterios de aceptación

### CA-01. Registro exitoso

- **DADO** que el Gestor autorizado ingresa nombres, apellidos, DNI, teléfono, correo, brevete y turno válidos.
- **CUANDO** confirma el registro.
- **ENTONCES** se crea el perfil local `ACTIVO` con vínculo `PENDIENTE` y usuarioId nulo, se audita y se devuelve su identificador; no se crea una cuenta global.

### CA-02. DNI duplicado

- **DADO** un perfil con el mismo DNI.
- **CUANDO** se intenta registrar otro.
- **ENTONCES** se responde 409 sin otro perfil ni auditoría de alta.

### CA-03. Datos incompletos o inválidos

- **DADO** campos obligatorios ausentes, vacíos o inválidos.
- **CUANDO** se intenta registrar.
- **ENTONCES** se responde 400 con los campos conocidos rechazados y no se persiste el alta.

### CA-04. Registro local sin provisión remota

- **DADO** un JWT autorizado y los datos locales válidos, sin invocar la creación de cuentas de Seguridad.
- **CUANDO** se registra al repartidor.
- **ENTONCES** el alta local se confirma como `PENDIENTE`; la asociación posterior se realiza en ES-F05-05.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin `GESTOR_DESPACHO`.
- **CUANDO** intenta registrar.
- **ENTONCES** se responde 403 antes de ejecutar el alta.

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
| CA-01 | Registro exitoso; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-02 | DNI duplicado; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-03 | Datos incompletos o inválidos; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-04 | Registro local sin provisión remota; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |
| CA-05 | Acceso sin permisos; comprobar el resultado y la ausencia de efectos no autorizados | [Matriz de casos](./evidence.md#2-cobertura-de-criterios) |

- [ ] Todos los CA/CUI y requisitos no funcionales del alcance tienen aceptación completa.
- [ ] Las dependencias reales y la revisión humana se verificaron.
- [ ] La verificación local y sus límites están registrados.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-01 y CA-01 a CA-03.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [cite: 3] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-03 y CA-14 a CA-15.
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
