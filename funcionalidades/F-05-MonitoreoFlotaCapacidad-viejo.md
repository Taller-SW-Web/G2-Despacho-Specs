# Especificación F-05: Monitoreo de Flota, Operadores y Capacidad Diaria

**Responsable:** Rhamses
**Estado:** En especificación
**Actor principal:** Gestor de Despacho
**Lineamiento del curso:** Soporte a la asignación de despacho a operador/repartidor

## 1. Contexto

El módulo opera inicialmente con repartidores y una flota compuesta por furgonetas. Sin un registro de quién está en turno, qué furgoneta tiene y cuánta carga lleva, F-02 no puede asignar despachos sin riesgo de sobrecarga, y F-03 no puede saber si un repartidor está habilitado para operar.

Esta funcionalidad es la fuente única de disponibilidad y ocupación del módulo. Administra repartidores y furgonetas, empareja a cada repartidor con una furgoneta y una zona para la jornada, y calcula su ocupación a partir de los despachos que tiene en curso. Además, vincula a cada repartidor con su usuario en Seguridad y Usuarios, que es el dueño de las identidades.

## 2. Propósito

Proveer al Gestor de Despacho un panel para administrar repartidores y furgonetas, abrir y cerrar las jornadas operativas y supervisar la ocupación de la flota, y proveer a F-02 y F-03 información confiable de habilitación y capacidad remanente.

## 3. Alcance

Esta funcionalidad incluye:

- Gestión de repartidores: registro, edición, baja lógica y vinculación con su usuario de Seguridad y Usuarios.
- Gestión de furgonetas: placa, estado y límites de carga (kg, m³ y máximo de paquetes en ruta).
- Asignación operativa diaria: emparejamiento repartidor – furgoneta – zona para la jornada.
- Estado operativo del repartidor calculado a partir de su jornada y sus despachos.
- Cálculo de ocupación en kg, m³ y paquetes a partir de los despachos en poder del repartidor: `ASIGNADO`, `EN_CAMINO` y `FALLIDO` aún no recibidos en el centro de despacho.
- Panel de monitoreo con indicadores por repartidor y resumen de la flota.
- Consulta de repartidores disponibles con su capacidad remanente para F-02.
- Cierre de turno, invocado por F-03 al cerrar la jornada o por el Gestor de Despacho.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- La configuración requiere JWT con rol `GESTOR_DESPACHO`.
- El documento de identidad de un repartidor y la placa de una furgoneta son únicos.
- Para la asignación diaria, el repartidor debe estar activo y vinculado, la furgoneta `DISPONIBLE` y la zona activa en F-01.
- Solo existe una asignación diaria activa por repartidor y por furgoneta en cada jornada.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Incorporar `REPARTIDOR`, crear la cuenta pendiente, gestionar su activación y comunicar el identificador y estado. |
| Zonas y Cotizador (F-01) | Proveer las zonas activas para la asignación diaria. |
| Programación y Asignación (F-02) | Consumir la disponibilidad y capacidad remanente antes de asignar. F-02 ejecuta la asignación; F-05 solo calcula e informa la capacidad. |
| Web del Repartidor (F-03) | Consultar la habilitación del repartidor y solicitar el cierre de su turno. |
| Entregas Fallidas (F-04) | Confirmar la recepción en el centro de los paquetes `FALLIDO`, para que dejen de contar en la ocupación del repartidor y la furgoneta. |

### 4.3. Resultados

- Un repartidor registrado queda activo, en `FUERA_DE_TURNO` y con vinculación `PENDIENTE`, `PENDIENTE_ACTIVACION`, `VINCULADO` o `ERROR`.
- La asignación diaria pone al repartidor en `DISPONIBLE` con los límites de la furgoneta y la zona de trabajo.
- La ocupación y el estado operativo se recalculan cada vez que cambia un despacho del repartidor.
- El cierre de turno pone al repartidor en `FUERA_DE_TURNO` y libera la furgoneta.

### 4.4. Estados del repartidor

| Dimensión | Estados | Cómo cambia |
|---|---|---|
| Registro | `ACTIVO`, `INACTIVO` | Acción del Gestor de Despacho (baja lógica). |
| Vinculación | `PENDIENTE`, `PENDIENTE_ACTIVACION`, `VINCULADO`, `ERROR` | Resultado de la integración y activación de la cuenta en Seguridad. |
| Operativo en la jornada | `FUERA_DE_TURNO`, `DISPONIBLE`, `EN_RUTA`, `SATURADO` | Calculado: `FUERA_DE_TURNO` sin asignación diaria activa; `SATURADO` si alcanzó cualquiera de sus tres límites; `EN_RUTA` si tiene al menos un despacho `EN_CAMINO`; `DISPONIBLE` en los demás casos. |

### 4.5. Regla de cálculo de ocupación

F-02 es responsable de asignar los despachos. Antes de confirmar una asignación, consulta la capacidad remanente calculada por F-05. F-05 no decide ni ejecuta la asignación: calcula la ocupación sumando el peso, el volumen y la cantidad de paquetes según estas reglas:

- Un despacho `ASIGNADO` ocupa capacidad.
- Un despacho `EN_CAMINO` ocupa capacidad.
- Un despacho `FALLIDO` sin recepción confirmada en el centro ocupa capacidad.
- Un despacho `FALLIDO` recibido en el centro deja de ocupar capacidad, aunque todavía esté pendiente de reprogramación o cierre por F-04.
- Los despachos `ENTREGADO`, `CANCELADO` y `DEVUELTO_A_ORIGEN` no ocupan capacidad.

Cuando F-04 confirma la recepción de un paquete fallido, Gestión de Despachos solicita a Operación liberar la reserva de capacidad. F-05 refleja la liberación en el siguiente cálculo; la comunicación usa la API interna definida en el contrato.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Gestión de repartidores

El sistema DEBE permitir registrar, editar, dar de baja y consultar repartidores.

#### CA-01. Registro exitoso de un nuevo repartidor

- **DADO** que el Gestor de Despacho ingresa nombres, apellidos, DNI, teléfono, correo, número de brevete y turno habitual.
- **CUANDO** confirma el registro.
- **ENTONCES** el sistema valida que el DNI no exista, crea el repartidor `ACTIVO` en `FUERA_DE_TURNO`, solicita a Seguridad y Usuarios la creación de su usuario y devuelve el identificador del repartidor.

#### CA-02. Rechazo por documento duplicado

- **DADO** un repartidor existente con un DNI.
- **CUANDO** se registra otro con el mismo DNI.
- **ENTONCES** el sistema responde `409 Conflict` sin persistir el duplicado.

#### CA-03. Baja lógica de un repartidor

- **DADO** un repartidor con despachos históricos y sin despachos `ASIGNADO` ni `EN_CAMINO`.
- **CUANDO** el Gestor lo cambia a `INACTIVO`.
- **ENTONCES** el sistema conserva el registro y su historial, lo excluye de nuevas asignaciones y F-03 le niega el acceso. Si tuviera despachos en curso, la operación se rechaza con `409 Conflict`.

#### CA-04. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta registrar o modificar repartidores.
- **ENTONCES** el sistema responde `403 Forbidden`.

### RF-02. Gestión de furgonetas y capacidad

El sistema DEBE administrar únicamente furgonetas con sus límites y su estado.

#### CA-05. Registro de furgoneta

- **DADO** una furgoneta con placa "ABC-123", 500 kg, 4.0 m³ y máximo de 80 paquetes en ruta.
- **CUANDO** el Gestor confirma el registro.
- **ENTONCES** se guarda en `DISPONIBLE` con esos límites.

#### CA-06. Placa duplicada

- **DADO** una furgoneta existente con placa "ABC-123".
- **CUANDO** se registra otro con la misma placa.
- **ENTONCES** el sistema responde `409 Conflict`.

#### CA-07. Furgoneta a mantenimiento

- **DADO** una furgoneta que debe entrar a mantenimiento.
- **CUANDO** el Gestor lo cambia a `EN_MANTENIMIENTO`.
- **ENTONCES** queda excluido de nuevas asignaciones diarias; si estaba en una jornada activa sin despachos en curso, esa jornada se cierra y el repartidor pasa a `FUERA_DE_TURNO`. Si el repartidor tiene despachos `ASIGNADO` o `EN_CAMINO`, la operación se rechaza con `409 Conflict` hasta que F-02 los reasigne o se cierren.

### RF-03. Asignación operativa diaria

El sistema DEBE vincular a cada repartidor con una furgoneta y una zona para la jornada.

#### CA-08. Asignación diaria exitosa

- **DADO** el repartidor "Juan Pérez", activo y vinculado, la furgoneta "ABC-123" disponible y la zona activa "Lima Centro".
- **CUANDO** el Gestor confirma la asignación del día.
- **ENTONCES** el repartidor pasa a `DISPONIBLE` con límites de 500 kg, 4.0 m³ y 80 paquetes, zona "Lima Centro", y aparece en la consulta de disponibilidad.

#### CA-09. Asignación duplicada en la jornada

- **DADO** que "Juan Pérez" ya tiene una asignación activa hoy.
- **CUANDO** se intenta crear otra.
- **ENTONCES** el sistema responde `409 Conflict`.

### RF-04. Panel de monitoreo de flota

El sistema DEBE mostrar la ocupación de cada repartidor y de la flota.

#### CA-10. Repartidor saturado

- **DADO** un repartidor con máximo de 50 paquetes y 50 despachos en `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor consulta el panel.
- **ENTONCES** se muestra con estado `SATURADO`, barra en rojo y la relación "50/50 paquetes (100 %)", junto a su ocupación en kg y m³. Las barras se muestran en verde por debajo de 70 %, en ámbar entre 70 % y 99 % y en rojo al 100 %.

#### CA-11. Resumen global

- **DADO** ocho repartidores con distintos estados.
- **CUANDO** el Gestor abre el panel.
- **ENTONCES** se muestran los totales `DISPONIBLE`, `EN_RUTA`, `SATURADO` y `FUERA_DE_TURNO`, actualizados sin recargar la página.

### RF-05. Consulta de disponibilidad para programación

El sistema DEBE devolver los repartidores habilitados con su capacidad remanente.

#### CA-12. Repartidores disponibles

- **DADO** cinco repartidores en jornada, tres `DISPONIBLE` o `EN_RUTA` y dos `SATURADO`.
- **CUANDO** F-02 consulta la disponibilidad.
- **ENTONCES** recibe los tres habilitados con identificador, nombre, zona, furgoneta, límites, capacidad remanente en kg, m³ y paquetes, porcentaje de ocupación y estado operativo.

#### CA-13. Sin repartidores disponibles

- **DADO** que todos los repartidores están `SATURADO` o `FUERA_DE_TURNO`.
- **CUANDO** F-02 consulta la disponibilidad.
- **ENTONCES** recibe `200 OK` con una lista vacía.

### RF-06. Vinculación con el usuario de Seguridad

El sistema DEBE asociar cada repartidor con su usuario en Seguridad y Usuarios, para que F-03 lo identifique desde el token.

#### CA-14. Vinculación y activación exitosas

- **DADO** el registro de un nuevo repartidor.
- **CUANDO** Seguridad crea la cuenta, devuelve su identificador y posteriormente confirma que puede iniciar sesión con rol `REPARTIDOR`.
- **ENTONCES** el sistema guarda el identificador, pasa primero por `PENDIENTE_ACTIVACION` y finalmente marca al repartidor como `VINCULADO`.

#### CA-15. Vinculación pendiente

- **DADO** que Seguridad no responde, rechaza la creación o la cuenta todavía no fue activada.
- **CUANDO** se registra el repartidor.
- **ENTONCES** el repartidor queda en `PENDIENTE`, `ERROR` o `PENDIENTE_ACTIVACION` según corresponda, no puede recibir una jornada y el panel ofrece reintentar cuando sea aplicable.

### RF-07. Estado operativo y cierre de turno

El sistema DEBE mantener el estado operativo coherente con los despachos y cerrar los turnos de forma segura.

#### CA-16. Paso a `EN_RUTA` y retorno a `DISPONIBLE`

- **DADO** un repartidor `DISPONIBLE`.
- **CUANDO** F-03 registra su primer despacho `EN_CAMINO` y, más tarde, ya no le queda ningún despacho `EN_CAMINO`.
- **ENTONCES** el repartidor pasa a `EN_RUTA` y luego vuelve a `DISPONIBLE`, y su ocupación se recalcula en cada cambio.

#### CA-17. Cierre de turno con despachos en curso

- **DADO** un repartidor con despachos `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor de Despacho intenta cerrar su turno manualmente.
- **ENTONCES** el sistema responde `409 Conflict`; el cierre con pendientes solo lo ejecuta F-03, que primero los resuelve como `NO_INTENTADO`.

#### CA-18. Saturación por peso o volumen

- **DADO** un repartidor con 20 paquetes de un máximo de 80, pero con 500 kg de 500 kg.
- **CUANDO** se calcula su estado operativo.
- **ENTONCES** el repartidor queda `SATURADO` y se excluye de la consulta de disponibilidad.

## 6. Frontend

| Elemento | Responsabilidad |
|---|---|
| Panel de Repartidores | Listado con filtros por estado, turno y vinculación; acciones de alta, edición, baja y reintento de vinculación. |
| Formulario de Repartidor | Datos personales, correo, brevete y turno habitual. |
| Panel de Furgonetas | Catálogo con filtros por estado y placa. |
| Formulario de Furgoneta | Placa, estado y límites de carga. |
| Asignación Diaria | Emparejamiento repartidor – furgoneta – zona con validación previa. |
| Dashboard de Monitoreo | Resumen de flota y tabla por repartidor con barras de ocupación en kg, m³ y paquetes. |
| Retroalimentación | Éxito, duplicados, conflictos y errores de red. |

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Gestión de repartidores | CRUD con unicidad de DNI, baja lógica y autorización. |
| Vinculación con Seguridad | Solicitar la creación del usuario, guardar su identificador y permitir reintentos. |
| Gestión de furgonetas | CRUD con unicidad de placa, estado y límites de carga. |
| Asignación diaria | Crear y cerrar jornadas repartidor – furgoneta – zona. |
| Motor de ocupación | Calcular kg, m³ y paquetes a partir de los despachos en poder del repartidor (`ASIGNADO`, `EN_CAMINO` y `FALLIDO` no recibidos en el centro) y derivar el estado operativo. |
| Consulta de disponibilidad | Devolver los repartidores habilitados con capacidad remanente en menos de 200 ms. |
| Persistencia y auditoría | Registrar cambios con usuario y marca temporal en UTC. |

Las rutas, cuerpos y códigos se centralizan en `integraciones/api-contract.md`.

## 8. Requisitos no funcionales

- **Rendimiento:** la consulta de disponibilidad responde en menos de 200 ms.
- **Seguridad:** toda la configuración y la consulta administrativa requieren `GESTOR_DESPACHO`.
- **Fuente única:** ninguna otra funcionalidad mantiene saldos de capacidad; la ocupación se calcula siempre desde el estado de los despachos.
- **Aislamiento:** no se accede a bases de datos de otros módulos.
- **Integridad referencial:** repartidores y furgonetas con historial solo admiten baja lógica.
- **Trazabilidad:** cambios de estado y asignaciones registran usuario y marca temporal en UTC.
- **Escalabilidad:** el panel pagina a partir de 50 repartidores.

## 9. Fuera de alcance

- **Asignación de despachos:** corresponde a F-02.
- **Autenticación y gestión de credenciales:** corresponden a Seguridad y Usuarios; F-05 solo solicita el alta del usuario y guarda el vínculo.

Motocicletas, automóviles, despacho express y gestión avanzada de flota quedan fuera del alcance aprobado. F-05 administra únicamente furgonetas.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 a CA-04 | Registrar, duplicar, dar de baja con y sin despachos en curso, y acceder sin permisos. | Integración y unitaria | Registro `ACTIVO`, `409` y `403` según corresponda. |
| CA-05 a CA-07 | Registrar furgonetas, duplicar placa y pasar a mantenimiento con y sin despachos en curso. | Integración y unitaria | Registro, `409` y cierre de jornada coherente. |
| CA-08 y CA-09 | Crear asignación diaria y repetirla. | Unitaria e integración | `DISPONIBLE` con límites y zona; `409`. |
| CA-10 y CA-11 | Consultar el panel con distintos niveles de carga. | Integración y frontend | Colores y totales correctos. |
| CA-12 y CA-13 | Consultar disponibilidad con y sin habilitados. | Integración | Lista filtrada con remanentes y lista vacía. |
| CA-14 y CA-15 | Registrar con Seguridad disponible y no disponible. | Integración con doble de prueba | Vinculación exitosa o pendiente sin asignación posible. |
| CA-16 a CA-18 | Simular transiciones de despachos, cierre manual con pendientes y saturación por peso. | Unitaria e integración | Estados operativos derivados correctamente y `409` en el cierre. |

Además, se ejecutarán dos recorridos funcionales completos:

1. Alta de repartidor → vinculación → asignación diaria → aparición en disponibilidad → asignación desde F-02 → ocupación actualizada.
2. Ocupación al 100 % en cualquier límite → `SATURADO` → exclusión de disponibilidad → entrega en F-03 → vuelve a `DISPONIBLE` o `EN_RUTA`.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Los criterios `CA-01` a `CA-18` están implementados y cuentan con pruebas automatizadas exitosas.
- Los dos recorridos funcionales han sido verificados.
- F-02 asigna respetando los tres límites informados por F-05.
- F-03 identifica al repartidor a partir del usuario vinculado.
- La baja lógica preserva el historial.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.
