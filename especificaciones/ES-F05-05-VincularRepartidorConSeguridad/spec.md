# ES-F05-05: Vincular repartidor con Seguridad y Usuarios

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Borrador migrado a SDD; revisión funcional y aceptación pendientes.

**Actor principal:** Sistema / Gestor de Despacho.

**UI:** Aplica; vincular cuenta / reintentar según acuerdo pendiente desde el catálogo administrativo `/repartidores`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> Migración estructural desde `ES-F05-05-VincularRepartidorConSeguridad.md`, revisión `f3849d9`. Se conservan las reglas y los criterios originales, incluidos sus IDs. Las discrepancias detectadas se registran en §7 y en el plan; esta migración no aprueba cambios de contrato ni acredita integración desplegada.

## 1. Contexto y objetivo

Gestionar el ciclo de vinculación entre un repartidor del módulo y su cuenta de usuario en Seguridad y Usuarios. El proceso abarca la solicitud de creación de cuenta, la recepción del identificador de usuario, el seguimiento de la activación y el reintento ante fallos. Un repartidor `VINCULADO` puede ser identificado por F-03 a través de su token JWT.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Vínculo, activación y reintentos descritos por los criterios originales; revisión explícita frente al contrato vigente.
- Resultado del comportamiento: Asociación y estado comprobables según el flujo contractual revisado, sin manejar credenciales en Despacho.

### Fuera de alcance

- Gestionar credenciales, contraseñas o tokens del repartidor.
- Activar o desactivar cuentas directamente en Seguridad y Usuarios.
- Revocar la vinculación al dar de baja al repartidor.

## 3. Actor, precondiciones y resultados

- La solicitud inicial de creación se dispara automáticamente al registrar un repartidor (ES-F05-01).
- El reintento manual lo ejecuta el Gestor de Despacho autenticado con rol `GESTOR_DESPACHO`.
- El repartidor existe y su estado de vinculación es `PENDIENTE` o `ERROR`.
- El módulo de Seguridad y Usuarios está integrado mediante API.

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Vincular cuenta / reintentar según acuerdo pendiente en `/repartidores`, conforme al flujo conservado.
- Resultado exitoso: Asociación y estado comprobables según el flujo contractual revisado, sin manejar credenciales en Despacho.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. Al registrar un repartidor, el sistema envía a Seguridad y Usuarios una solicitud de creación de cuenta con rol `REPARTIDOR`.
2. Si Seguridad responde exitosamente, el sistema guarda el identificador de usuario y cambia la vinculación a `PENDIENTE_ACTIVACION`.
3. Cuando Seguridad confirma que la cuenta fue activada y el repartidor puede iniciar sesión, el sistema cambia la vinculación a `VINCULADO`.
4. Si Seguridad no responde o rechaza la creación, la vinculación queda en `ERROR`.
5. El Gestor puede seleccionar `Reintentar vinculación` en el panel para repartidores en `ERROR`.
6. Cada cambio de estado de vinculación se registra con auditoría.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Vinculación y activación exitosas | Conciliar el flujo antes de comprobar creación, activación y transición esperadas por el criterio original. |
| CA-02 | Seguridad no responde | Definir la simulación de indisponibilidad y el estado contractual esperado. |
| CA-03 | Seguridad rechaza la creación | Definir el rechazo de Seguridad y verificar el resultado después de conciliarlo. |
| CA-04 | Cuenta pendiente de activación | Confirmar si el estado de activación pertenece al vínculo local o exclusivamente a Seguridad. |
| CA-05 | Reintento exitoso | Conciliar el reintento y comprobar el identificador y estado finales. |
| CA-06 | Reintento fallido | Comprobar fallo del reintento sin pérdida del vínculo ni duplicación una vez acordado el flujo. |
| CA-07 | Reintento con vinculación no aplicable | Verificar repetición sobre un vínculo existente y ausencia de duplicados. |

## 5. Reglas, datos e integraciones

- Los estados de vinculación siguen la progresión: `PENDIENTE` → `PENDIENTE_ACTIVACION` → `VINCULADO`, o `PENDIENTE` / `PENDIENTE_ACTIVACION` → `ERROR`.
- El reintento solo está disponible para repartidores en estado `ERROR`.
- Un repartidor con vinculación distinta de `VINCULADO` no puede recibir asignaciones diarias en F-06.
- La vinculación no modifica el estado de registro (`ACTIVO` / `INACTIVO`) del repartidor.
- El identificador de usuario devuelto por Seguridad se almacena para que F-03 pueda identificar al repartidor desde el token.
- Si la activación tarda, el repartidor permanece en `PENDIENTE_ACTIVACION` hasta que Seguridad confirme.

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
- La comunicación se rige por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `PUT /api/v1/repartidores/{idRepartidor}/vinculacion`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

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

## 7. UI, backend y requisitos no funcionales

- UI: interacción, estados y criterios CUI en [ui.md](./ui.md); reutilización de los [componentes compartidos](../../disenio/componentes-react.md).
- Backend: Documentar el vínculo entre perfil local y cuenta de Seguridad, pendiente de conciliar el flujo heredado. Propiedad local de `repartidores`; no acceder a la base de Gestión.
- Requisitos no funcionales: Confirmar consistencia de datos, permisos y auditoría; comprobar cancelación, repetición y concurrencia cuando afecten el resultado.
- Seguridad y datos: no mostrar credenciales, tokens ni errores técnicos en la interfaz; la habilitación visual no reemplaza la autorización del backend.
- Pendiente funcional P-01: Los siete criterios heredados describen creación automática, activación y reintento; Seguridad §8.4 y Operación §4.1 acuerdan asociar el usuario creado previamente por ADMIN_SISTEMA. No se reemplazan esos criterios durante una migración de estructura: requieren revisión de Rhamses con Seguridad y Arquitectura antes de aceptar el comportamiento.
- Responsable de P-01: Rhamses coordina con Arquitectura y Seguridad; la revisión afecta los criterios indicados y debe resolverse antes de declarar la aceptación completa.
- Las implementaciones existentes se referencian en [evidence.md](./evidence.md). Su existencia no reemplaza la comprobación individual de los criterios conservados.

## 8. Verificación y completitud

| Criterio | Comprobación prevista | Nivel y preparación |
|---|---|---|
| CA-01 | Conciliar el flujo antes de comprobar creación, activación y transición esperadas por el criterio original. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-02 | Definir la simulación de indisponibilidad y el estado contractual esperado. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-03 | Definir el rechazo de Seguridad y verificar el resultado después de conciliarlo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-04 | Confirmar si el estado de activación pertenece al vínculo local o exclusivamente a Seguridad. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-05 | Conciliar el reintento y comprobar el identificador y estado finales. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-06 | Comprobar fallo del reintento sin pérdida del vínculo ni duplicación una vez acordado el flujo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-07 | Verificar repetición sobre un vínculo existente y ausencia de duplicados. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |

- [ ] Todos los criterios y CUI cuentan con resultados por caso en [evidence.md](./evidence.md).
- [ ] P-01 está resuelto en los documentos propietarios y revisado por el equipo.
- [ ] Los datos, el contrato y la implementación son consistentes.
- [ ] Las dependencias simuladas y la integración real pendiente se identifican expresamente.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-03 y CA-14 a CA-16.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [cite: 3] [overview.md](../../overview.md), integración con Seguridad y Usuarios.
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
