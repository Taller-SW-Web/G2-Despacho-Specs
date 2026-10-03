# Especificación F-06: Disponibilidad y Capacidad Diaria de la Flota

**Responsable:** Rhamses
**Estado:** En especificación
**Actor principal:** Gestor de Despacho
**Lineamiento del curso:** Soporte a la asignación de despacho a operador/repartidor

## 1. Contexto

Una vez que los repartidores y las furgonetas están registrados en F-05, el módulo necesita emparejarlos con una zona para cada jornada de trabajo, y calcular en tiempo real cuánta carga lleva cada repartidor para que F-02 pueda asignar despachos sin riesgo de sobrecarga y F-03 pueda saber si un repartidor está habilitado.

Esta funcionalidad es la fuente única de disponibilidad, ocupación y saturación del módulo. Conecta repartidor, furgoneta y zona para la jornada, calcula la ocupación a partir de los despachos en curso y expone la capacidad remanente para que F-02 tome decisiones de asignación informadas.

## 2. Propósito

Proveer al Gestor de Despacho un panel para abrir y cerrar jornadas operativas y supervisar la ocupación de la flota, y proveer a F-02 y F-03 información confiable de habilitación, disponibilidad y capacidad remanente de cada repartidor.

## 3. Alcance

Esta funcionalidad incluye:

- Asignación operativa diaria: emparejamiento repartidor – furgoneta – zona para la jornada.
- Estado operativo del repartidor calculado a partir de su jornada y sus despachos: `FUERA_DE_TURNO`, `DISPONIBLE`, `EN_RUTA`, `SATURADO`.
- Cálculo de ocupación en kg, m³ y paquetes a partir de los despachos en poder del repartidor: `ASIGNADO`, `EN_CAMINO` y `FALLIDO` aún no recibidos en el centro de despacho.
- Panel de monitoreo con indicadores por repartidor y resumen de la flota.
- Consulta de repartidores disponibles con su capacidad remanente para F-02.
- Cierre de turno, invocado por F-03 al cerrar la jornada o por el Gestor de Despacho.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario está autenticado con JWT y rol `GESTOR_DESPACHO`.
- Para la asignación diaria, el repartidor debe estar `ACTIVO` y `VINCULADO` en F-05.
- La furgoneta debe estar en estado `DISPONIBLE` en F-05.
- La zona debe estar activa en F-01.
- Solo existe una asignación diaria activa por repartidor y por furgoneta en cada jornada.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Gestión de Repartidores y Vehículos (F-05) | Proveer los repartidores activos y vinculados, y las furgonetas disponibles con sus límites de carga. |
| Zonas y Cotizador (F-01) | Proveer las zonas activas para la asignación diaria. |
| Programación y Asignación (F-02) | Consumir la disponibilidad y capacidad remanente antes de asignar. F-02 ejecuta la asignación; F-06 solo calcula e informa la capacidad. |
| Web del Repartidor (F-03) | Consultar la habilitación del repartidor y solicitar el cierre de su turno. |
| Entregas Fallidas (F-04) | Confirmar la recepción en el centro de los paquetes `FALLIDO`, para que dejen de contar en la ocupación del repartidor y la furgoneta. |

### 4.3. Resultados

- La asignación diaria pone al repartidor en `DISPONIBLE` con los límites de la furgoneta asignada y la zona de trabajo.
- La ocupación y el estado operativo se recalculan cada vez que cambia un despacho del repartidor.
- El cierre de turno pone al repartidor en `FUERA_DE_TURNO` y libera la furgoneta para futuras asignaciones.

### 4.4. Estado operativo del repartidor en la jornada

| Estado | Condición |
|---|---|
| `FUERA_DE_TURNO` | No tiene asignación diaria activa. |
| `DISPONIBLE` | Tiene asignación diaria activa y no ha alcanzado ningún límite ni tiene despachos `EN_CAMINO`. |
| `EN_RUTA` | Tiene al menos un despacho `EN_CAMINO`. |
| `SATURADO` | Ha alcanzado cualquiera de sus tres límites (kg, m³ o paquetes). |

### 4.5. Regla de cálculo de ocupación

F-06 calcula la ocupación sumando el peso, el volumen y la cantidad de paquetes según estas reglas:

- Un despacho `ASIGNADO` ocupa capacidad.
- Un despacho `EN_CAMINO` ocupa capacidad.
- Un despacho `FALLIDO` sin recepción confirmada en el centro ocupa capacidad.
- Un despacho `FALLIDO` recibido en el centro deja de ocupar capacidad, aunque esté pendiente de reprogramación o cierre por F-04.
- Los despachos `ENTREGADO`, `CANCELADO` y `DEVUELTO_A_ORIGEN` no ocupan capacidad.

Cuando F-04 confirma la recepción de un paquete fallido, Gestión de Despachos solicita a Operación liberar la reserva de capacidad. F-06 refleja la liberación en el siguiente cálculo; la comunicación usa la API interna definida en el contrato.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Asignación operativa diaria

El sistema DEBE vincular a cada repartidor con una furgoneta y una zona para la jornada.

#### CA-01. Asignación diaria exitosa

- **DADO** el repartidor "Juan Pérez", `ACTIVO` y `VINCULADO` en F-05, la furgoneta "ABC-123" `DISPONIBLE` en F-05 y la zona activa "Lima Centro" en F-01.
- **CUANDO** el Gestor confirma la asignación del día.
- **ENTONCES** el repartidor pasa a estado operativo `DISPONIBLE` con los límites de 500 kg, 4.0 m³ y 80 paquetes de la furgoneta, zona "Lima Centro", y aparece en la consulta de disponibilidad.

#### CA-02. Asignación duplicada en la jornada

- **DADO** que "Juan Pérez" ya tiene una asignación activa hoy.
- **CUANDO** se intenta crear otra.
- **ENTONCES** el sistema responde `409 Conflict`.

#### CA-03. Repartidor no apto para asignación

- **DADO** un repartidor `INACTIVO` o con vinculación distinta de `VINCULADO`.
- **CUANDO** el Gestor intenta asignarle una jornada.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` indicando la razón.

#### CA-04. Furgoneta no disponible

- **DADO** una furgoneta en `EN_MANTENIMIENTO` o `FUERA_DE_SERVICIO`, o ya asignada a otro repartidor en la jornada.
- **CUANDO** el Gestor intenta asignarla.
- **ENTONCES** el sistema responde `409 Conflict`.

#### CA-05. Zona inactiva

- **DADO** una zona que no está activa en F-01.
- **CUANDO** el Gestor intenta usarla en una asignación diaria.
- **ENTONCES** el sistema responde `422 Unprocessable Entity`.

#### CA-06. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta crear una asignación diaria.
- **ENTONCES** el sistema responde `403 Forbidden`.

### RF-02. Panel de monitoreo de flota

El sistema DEBE mostrar la ocupación de cada repartidor y el resumen de la flota.

#### CA-07. Repartidor saturado

- **DADO** un repartidor con máximo de 50 paquetes y 50 despachos en `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor consulta el panel.
- **ENTONCES** se muestra con estado `SATURADO`, barra en rojo y la relación "50/50 paquetes (100 %)", junto a su ocupación en kg y m³. Las barras se muestran en verde por debajo de 70 %, en ámbar entre 70 % y 99 % y en rojo al 100 %.

#### CA-08. Resumen global

- **DADO** ocho repartidores con distintos estados operativos.
- **CUANDO** el Gestor abre el panel.
- **ENTONCES** se muestran los totales `DISPONIBLE`, `EN_RUTA`, `SATURADO` y `FUERA_DE_TURNO`, actualizados sin recargar la página.

### RF-03. Consulta de disponibilidad para programación

El sistema DEBE devolver los repartidores habilitados con su capacidad remanente.

#### CA-09. Repartidores disponibles

- **DADO** cinco repartidores en jornada, tres `DISPONIBLE` o `EN_RUTA` y dos `SATURADO`.
- **CUANDO** F-02 consulta la disponibilidad.
- **ENTONCES** recibe los tres habilitados con identificador, nombre, zona, furgoneta, límites, capacidad remanente en kg, m³ y paquetes, porcentaje de ocupación y estado operativo.

#### CA-10. Sin repartidores disponibles

- **DADO** que todos los repartidores están `SATURADO` o `FUERA_DE_TURNO`.
- **CUANDO** F-02 consulta la disponibilidad.
- **ENTONCES** recibe `200 OK` con una lista vacía.

### RF-04. Estado operativo y cierre de turno

El sistema DEBE mantener el estado operativo coherente con los despachos y cerrar los turnos de forma segura.

#### CA-11. Paso a `EN_RUTA` y retorno a `DISPONIBLE`

- **DADO** un repartidor `DISPONIBLE`.
- **CUANDO** F-03 registra su primer despacho `EN_CAMINO` y, más tarde, ya no le queda ningún despacho `EN_CAMINO`.
- **ENTONCES** el repartidor pasa a `EN_RUTA` y luego vuelve a `DISPONIBLE`, y su ocupación se recalcula en cada cambio.

#### CA-12. Cierre de turno sin despachos en curso

- **DADO** un repartidor sin despachos `ASIGNADO` ni `EN_CAMINO`.
- **CUANDO** el Gestor o F-03 cierra su turno.
- **ENTONCES** el repartidor pasa a `FUERA_DE_TURNO` y la furgoneta queda liberada.

#### CA-13. Cierre de turno con despachos en curso

- **DADO** un repartidor con despachos `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor de Despacho intenta cerrar su turno manualmente.
- **ENTONCES** el sistema responde `409 Conflict`; el cierre con pendientes solo lo ejecuta F-03, que primero los resuelve como `NO_INTENTADO`.

#### CA-14. Saturación por peso o volumen

- **DADO** un repartidor con 20 paquetes de un máximo de 80, pero con 500 kg de 500 kg.
- **CUANDO** se calcula su estado operativo.
- **ENTONCES** el repartidor queda `SATURADO` y se excluye de la consulta de disponibilidad.

#### CA-15. Liberación de capacidad por recepción de paquete fallido

- **DADO** un repartidor `SATURADO` con un despacho `FALLIDO` que ocupaba 100 kg.
- **CUANDO** F-04 confirma la recepción del paquete en el centro de despacho.
- **ENTONCES** la ocupación del repartidor se reduce en 100 kg, y su estado operativo se recalcula (puede pasar de `SATURADO` a `DISPONIBLE` o `EN_RUTA`).

## 6. Frontend

| Elemento | Responsabilidad |
|---|---|
| Asignación Diaria | Emparejamiento repartidor – furgoneta – zona con validación previa de requisitos. Muestra solo repartidores activos y vinculados, furgonetas disponibles y zonas activas. |
| Dashboard de Monitoreo | Resumen de flota con totales por estado operativo y tabla por repartidor con barras de ocupación en kg, m³ y paquetes. Actualización sin recarga. |
| Detalle del Repartidor en Jornada | Despachos asignados, ocupación actual, límites y zona de trabajo. |
| Retroalimentación | Éxito, conflictos de asignación, furgoneta no disponible, zona inactiva y errores de red. |

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Asignación diaria | Crear y cerrar jornadas repartidor – furgoneta – zona, validando precondiciones con F-05 y F-01. |
| Motor de ocupación | Calcular kg, m³ y paquetes a partir de los despachos en poder del repartidor (`ASIGNADO`, `EN_CAMINO` y `FALLIDO` no recibidos en el centro) y derivar el estado operativo. |
| Consulta de disponibilidad | Devolver los repartidores habilitados con capacidad remanente en menos de 200 ms. |
| Panel de monitoreo | Proveer resumen de flota y ocupación por repartidor con datos actualizados. |
| Persistencia y auditoría | Registrar asignaciones, cierres y cambios de estado con usuario y marca temporal en UTC. |

Las rutas, cuerpos y códigos se centralizan en `integraciones/api-contract.md`.

## 8. Requisitos no funcionales

- **Rendimiento:** la consulta de disponibilidad responde en menos de 200 ms.
- **Seguridad:** la configuración y consulta administrativa requieren `GESTOR_DESPACHO`.
- **Fuente única:** ninguna otra funcionalidad mantiene saldos de capacidad; la ocupación se calcula siempre desde el estado de los despachos.
- **Aislamiento:** no se accede a bases de datos de otros módulos.
- **Trazabilidad:** asignaciones diarias y cierres registran usuario y marca temporal en UTC.
- **Escalabilidad:** el panel pagina a partir de 50 repartidores.

## 9. Fuera de alcance

- **CRUD de repartidores y furgonetas:** corresponde a F-05.
- **Vinculación con Seguridad y Usuarios:** corresponde a F-05.
- **Asignación de despachos a repartidores:** corresponde a F-02.
- **Autenticación y gestión de credenciales:** corresponden a Seguridad y Usuarios.
- Motocicletas, automóviles, despacho express y gestión avanzada de flota quedan fuera del alcance aprobado.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 a CA-06 | Crear asignación diaria exitosa, duplicada, con repartidor no apto, furgoneta no disponible, zona inactiva y sin permisos. | Integración y unitaria | `DISPONIBLE` con límites y zona; `409`, `422` y `403` según corresponda. |
| CA-07 y CA-08 | Consultar el panel con distintos niveles de carga y estados. | Integración y frontend | Colores, barras y totales correctos. |
| CA-09 y CA-10 | Consultar disponibilidad con y sin habilitados. | Integración | Lista filtrada con remanentes y lista vacía. |
| CA-11 a CA-14 | Simular transiciones de despachos, cierre manual con y sin pendientes, y saturación por peso. | Unitaria e integración | Estados operativos derivados correctamente y `409` en el cierre. |
| CA-15 | Confirmar recepción de paquete fallido y verificar liberación de ocupación. | Integración | Ocupación reducida y estado operativo recalculado. |

Además, se ejecutarán dos recorridos funcionales completos:

1. Asignación diaria → repartidor `DISPONIBLE` → aparición en consulta de disponibilidad → asignación de despacho desde F-02 → ocupación actualizada → saturación → exclusión de disponibilidad.
2. Repartidor `SATURADO` → entrega exitosa en F-03 → recalculación → vuelve a `DISPONIBLE` o `EN_RUTA` → cierre de turno → `FUERA_DE_TURNO` y furgoneta liberada.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Los criterios `CA-01` a `CA-15` están implementados y cuentan con pruebas automatizadas exitosas.
- Los dos recorridos funcionales han sido verificados.
- F-02 asigna respetando los tres límites informados por F-06.
- La consulta de disponibilidad responde en menos de 200 ms.
- El cierre de turno libera la furgoneta correctamente.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.
