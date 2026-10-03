# Especificación F-05: Gestión de Repartidores y Vehículos

**Responsable:** Rhamses
**Estado:** En especificación
**Actor principal:** Gestor de Despacho
**Lineamiento del curso:** Administración de recursos operativos del módulo

## 1. Contexto

Antes de que un repartidor pueda operar en una jornada, debe existir como recurso registrado del módulo con sus datos personales, su licencia y su vinculación con el usuario de Seguridad y Usuarios que le permite autenticarse. Del mismo modo, cada furgoneta debe estar catalogada con su placa, su estado y sus límites de carga.

Esta funcionalidad es el catálogo maestro de repartidores y furgonetas. Sin estos registros, F-06 no puede crear asignaciones diarias, F-02 no puede asignar despachos y F-03 no puede identificar al repartidor desde su token.

## 2. Propósito

Proveer al Gestor de Despacho las operaciones de alta, edición, consulta y baja lógica de repartidores y furgonetas, incluyendo la vinculación de cada repartidor con su cuenta en Seguridad y Usuarios, y el registro de las capacidades de carga de cada furgoneta.

## 3. Alcance

Esta funcionalidad incluye:

- Registro de repartidores con datos personales, brevete y turno habitual.
- Edición de datos del repartidor.
- Baja lógica de repartidores con preservación del historial.
- Vinculación del repartidor con su usuario en Seguridad y Usuarios: solicitud de creación, seguimiento de activación y reintento ante fallos.
- Estados de registro (`ACTIVO`, `INACTIVO`) y estados de vinculación (`PENDIENTE`, `PENDIENTE_ACTIVACION`, `VINCULADO`, `ERROR`).
- Registro de furgonetas con placa, estado y límites de carga (kg, m³ y máximo de paquetes en ruta).
- Edición de datos y límites de la furgoneta.
- Cambio de estado de la furgoneta (`DISPONIBLE`, `EN_MANTENIMIENTO`, `FUERA_DE_SERVICIO`).
- Consulta paginada y filtrable de repartidores y furgonetas.
- Validación de unicidad de DNI para repartidores y de placa para furgonetas.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario está autenticado con JWT y rol `GESTOR_DESPACHO`.
- El DNI de cada repartidor es único en el módulo.
- La placa de cada furgoneta es única en el módulo.
- Un repartidor solo puede darse de baja si no tiene despachos en `ASIGNADO` ni `EN_CAMINO`.
- Una furgoneta solo puede pasar a `EN_MANTENIMIENTO` o `FUERA_DE_SERVICIO` si no está asignada a una jornada activa con despachos en curso.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Incorporar el rol `REPARTIDOR`, crear la cuenta del repartidor, gestionar su activación y comunicar el identificador y estado. |
| Disponibilidad y Capacidad Diaria (F-06) | Consumir los repartidores activos y vinculados y las furgonetas disponibles para crear asignaciones diarias. |
| Web del Repartidor (F-03) | Identificar al repartidor desde el token vinculado por esta funcionalidad. |

### 4.3. Resultados

- Un repartidor registrado queda en estado de registro `ACTIVO` y con vinculación `PENDIENTE` hasta que Seguridad confirme la creación y activación de su cuenta.
- La vinculación progresa por `PENDIENTE` → `PENDIENTE_ACTIVACION` → `VINCULADO`, o queda en `ERROR` si la integración falla.
- Una baja lógica cambia el estado a `INACTIVO`, conserva el historial y excluye al repartidor de nuevas asignaciones.
- Una furgoneta registrada queda en `DISPONIBLE` con sus límites de carga definidos.

### 4.4. Estados del repartidor

| Dimensión | Estados | Cómo cambia |
|---|---|---|
| Registro | `ACTIVO`, `INACTIVO` | Acción del Gestor de Despacho (baja lógica / reactivación). |
| Vinculación | `PENDIENTE`, `PENDIENTE_ACTIVACION`, `VINCULADO`, `ERROR` | Resultado de la integración con Seguridad y Usuarios. |

### 4.5. Estados de la furgoneta

| Estado | Significado |
|---|---|
| `DISPONIBLE` | Lista para ser asignada a una jornada. |
| `EN_MANTENIMIENTO` | Temporalmente fuera de operación, excluida de nuevas asignaciones. |
| `FUERA_DE_SERVICIO` | Retirada definitivamente, conserva historial. |

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Gestión de repartidores

El sistema DEBE permitir registrar, editar, dar de baja y consultar repartidores.

#### CA-01. Registro exitoso de un nuevo repartidor

- **DADO** que el Gestor de Despacho ingresa nombres, apellidos, DNI, teléfono, correo, número de brevete y turno habitual.
- **CUANDO** confirma el registro.
- **ENTONCES** el sistema valida que el DNI no exista, crea el repartidor `ACTIVO` con vinculación `PENDIENTE`, solicita a Seguridad y Usuarios la creación de su usuario y devuelve el identificador del repartidor.

#### CA-02. Rechazo por documento duplicado

- **DADO** un repartidor existente con un DNI.
- **CUANDO** se registra otro con el mismo DNI.
- **ENTONCES** el sistema responde `409 Conflict` sin persistir el duplicado.

#### CA-03. Edición de datos del repartidor

- **DADO** un repartidor registrado.
- **CUANDO** el Gestor modifica su teléfono, correo, brevete o turno habitual.
- **ENTONCES** el sistema actualiza los datos, registra la auditoría y conserva el estado de registro y vinculación.

#### CA-04. Baja lógica de un repartidor

- **DADO** un repartidor con despachos históricos y sin despachos `ASIGNADO` ni `EN_CAMINO`.
- **CUANDO** el Gestor lo cambia a `INACTIVO`.
- **ENTONCES** el sistema conserva el registro y su historial, lo excluye de nuevas asignaciones y F-03 le niega el acceso.

#### CA-05. Rechazo de baja con despachos en curso

- **DADO** un repartidor con despachos en `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor intenta darlo de baja.
- **ENTONCES** el sistema responde `409 Conflict` indicando que tiene despachos en curso.

#### CA-06. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta registrar o modificar repartidores.
- **ENTONCES** el sistema responde `403 Forbidden`.

#### CA-07. Consulta paginada de repartidores

- **DADO** que existen repartidores registrados.
- **CUANDO** el Gestor abre el panel de repartidores.
- **ENTONCES** el sistema muestra un listado paginado con filtros por estado de registro, estado de vinculación y turno habitual.

### RF-02. Gestión de furgonetas y capacidad

El sistema DEBE administrar furgonetas con sus límites de carga y su estado.

#### CA-08. Registro de furgoneta

- **DADO** una furgoneta con placa "ABC-123", 500 kg, 4.0 m³ y máximo de 80 paquetes en ruta.
- **CUANDO** el Gestor confirma el registro.
- **ENTONCES** se guarda en `DISPONIBLE` con esos límites.

#### CA-09. Placa duplicada

- **DADO** una furgoneta existente con placa "ABC-123".
- **CUANDO** se registra otra con la misma placa.
- **ENTONCES** el sistema responde `409 Conflict`.

#### CA-10. Edición de límites de carga

- **DADO** una furgoneta registrada sin jornada activa.
- **CUANDO** el Gestor modifica sus límites de carga.
- **ENTONCES** el sistema actualiza los valores y registra la auditoría. Los límites aplican a las jornadas futuras; las jornadas activas conservan los valores originales.

#### CA-11. Cambio a mantenimiento

- **DADO** una furgoneta sin jornada activa con despachos en curso.
- **CUANDO** el Gestor la cambia a `EN_MANTENIMIENTO`.
- **ENTONCES** queda excluida de nuevas asignaciones diarias. Si tenía jornada activa sin despachos en curso, esa jornada se cierra.

#### CA-12. Rechazo de mantenimiento con despachos en curso

- **DADO** una furgoneta asignada a una jornada con despachos `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor intenta cambiarla a `EN_MANTENIMIENTO`.
- **ENTONCES** el sistema responde `409 Conflict` indicando que la furgoneta tiene despachos en curso.

#### CA-13. Consulta paginada de furgonetas

- **DADO** que existen furgonetas registradas.
- **CUANDO** el Gestor abre el panel de furgonetas.
- **ENTONCES** el sistema muestra un listado paginado con filtros por estado y placa.

### RF-03. Vinculación con el usuario de Seguridad

El sistema DEBE asociar cada repartidor con su usuario en Seguridad y Usuarios para que F-03 lo identifique desde el token.

#### CA-14. Vinculación y activación exitosas

- **DADO** el registro de un nuevo repartidor.
- **CUANDO** Seguridad crea la cuenta, devuelve su identificador y posteriormente confirma que puede iniciar sesión con rol `REPARTIDOR`.
- **ENTONCES** el sistema guarda el identificador, pasa primero por `PENDIENTE_ACTIVACION` y finalmente marca al repartidor como `VINCULADO`.

#### CA-15. Vinculación pendiente o fallida

- **DADO** que Seguridad no responde, rechaza la creación o la cuenta aún no fue activada.
- **CUANDO** se registra el repartidor.
- **ENTONCES** el repartidor queda en `PENDIENTE`, `ERROR` o `PENDIENTE_ACTIVACION` según corresponda, no puede recibir una jornada y el panel ofrece reintentar cuando sea aplicable.

#### CA-16. Reintento de vinculación

- **DADO** un repartidor en estado de vinculación `ERROR`.
- **CUANDO** el Gestor selecciona la opción de reintentar.
- **ENTONCES** el sistema vuelve a solicitar la creación del usuario a Seguridad y actualiza el estado de vinculación según la respuesta.

## 6. Frontend

| Elemento | Responsabilidad |
|---|---|
| Panel de Repartidores | Listado paginado con filtros por estado de registro, vinculación y turno; acciones de alta, edición, baja y reintento de vinculación. |
| Formulario de Repartidor | Campos: nombres, apellidos, DNI, teléfono, correo, brevete y turno habitual. Validación en cliente y retroalimentación. |
| Panel de Furgonetas | Catálogo paginado con filtros por estado y placa; acciones de alta, edición y cambio de estado. |
| Formulario de Furgoneta | Campos: placa, límites de carga (kg, m³, paquetes) y estado. Validación en cliente. |
| Retroalimentación | Éxito, duplicados, conflictos y errores de red. |

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Gestión de repartidores | CRUD con unicidad de DNI, baja lógica, autorización y auditoría. |
| Vinculación con Seguridad | Solicitar la creación del usuario, guardar su identificador, gestionar reintentos y actualizar estados de vinculación. |
| Gestión de furgonetas | CRUD con unicidad de placa, estado, límites de carga y auditoría. |
| Persistencia y auditoría | Registrar cambios con usuario y marca temporal en UTC. |

Las rutas, cuerpos y códigos se centralizan en `integraciones/api-contract.md`.

## 8. Requisitos no funcionales

- **Seguridad:** todas las operaciones requieren JWT con rol `GESTOR_DESPACHO`.
- **Aislamiento:** no se accede a bases de datos de otros módulos.
- **Integridad referencial:** repartidores y furgonetas con historial solo admiten baja lógica.
- **Trazabilidad:** cambios de estado, ediciones y registros auditan usuario y marca temporal en UTC.
- **Escalabilidad:** los paneles paginan a partir de 50 registros.
- **Rendimiento:** las consultas paginadas responden en menos de 200 ms.

## 9. Fuera de alcance

- **Asignación diaria repartidor – furgoneta – zona:** corresponde a F-06.
- **Cálculo de ocupación, disponibilidad y saturación:** corresponde a F-06.
- **Panel de monitoreo de flota en tiempo real:** corresponde a F-06.
- **Asignación de despachos:** corresponde a F-02.
- **Autenticación y gestión de credenciales:** corresponden a Seguridad y Usuarios; F-05 solo solicita el alta del usuario y guarda el vínculo.
- Motocicletas, automóviles, despacho express y gestión avanzada de flota quedan fuera del alcance aprobado. F-05 administra únicamente furgonetas.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 a CA-06 | Registrar, duplicar, editar, dar de baja con y sin despachos en curso, y acceder sin permisos. | Integración y unitaria | Registro `ACTIVO`, `409`, `403` y baja coherente. |
| CA-07 | Consultar repartidores con filtros y paginación. | Integración y frontend | Listado paginado con filtros funcionales. |
| CA-08 a CA-13 | Registrar furgonetas, duplicar placa, editar límites y cambiar estado con y sin despachos en curso. | Integración y unitaria | Registro, `409`, edición y cierre de jornada coherente. |
| CA-14 a CA-16 | Registrar con Seguridad disponible, no disponible y reintentar. | Integración con doble de prueba | Vinculación exitosa, pendiente o error con reintento funcional. |

Además, se ejecutarán dos recorridos funcionales completos:

1. Alta de repartidor → vinculación exitosa con Seguridad → repartidor `ACTIVO` y `VINCULADO` → disponible para F-06.
2. Alta de furgoneta → edición de límites → cambio a `EN_MANTENIMIENTO` → exclusión de F-06 → retorno a `DISPONIBLE`.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Los criterios `CA-01` a `CA-16` están implementados y cuentan con pruebas automatizadas exitosas.
- Los dos recorridos funcionales han sido verificados.
- F-03 identifica al repartidor a partir del usuario vinculado por F-05.
- La baja lógica preserva el historial.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.
