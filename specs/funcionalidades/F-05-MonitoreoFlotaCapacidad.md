# Especificación: F-06 - Panel de Monitoreo de Flota, Operadores y Capacidad Diaria

## 1. Contexto
La operación de última milla depende críticamente de la gestión de los recursos físicos (vehículos) y humanos (conductores/repartidores). Sin un control centralizado de los turnos de trabajo, las capacidades de carga y el estado operativo diario, la asignación de pedidos corre el riesgo de sobrecargar a ciertos repartidores o asignar envíos a personal ausente o vehículos en mantenimiento.

Este subsistema administra las tablas maestras de la flota y los repartidores de Despacho, operando como el proveedor oficial de información de disponibilidad para el Panel de Programación (F-02, Integrante 2) y para la validación de sesiones activas de la App Móvil del Repartidor (F-03, Integrante 3).

## 2. Propósito
Proveer al Gestor de Flota de un panel administrativo para gestionar el ciclo de vida del personal de reparto y los vehículos asociados, configurar límites operativos diarios (máximo de paquetes, peso y volumen por turno) y supervisar en tiempo real el porcentaje de ocupación y saturación de la flota mediante métricas e indicadores gráficos.

## 3. Alcance
Incluye:
- CRUD administrativo completo de Repartidores (registro, edición de datos personales, activación/desactivación y asignación de turnos).
- CRUD administrativo completo de Vehículos (registro de tipo: moto/furgoneta/auto, placa, capacidad máxima de peso en kg y volumen en m³, estado de mantenimiento).
- Asociación operativa entre repartidor, vehículo y turno de trabajo del día.
- Panel gráfico de monitoreo de flota en tiempo real:
  - Total de repartidores activos, en ruta, disponibles y fuera de servicio.
  - Indicador de capacidad usada diaria (porcentaje de ocupación respecto al límite configurado).
- Exposición de la API backend de alta disponibilidad: `GET /api/v1/repartidores/disponibles` para consumo directo del Integrante 2 al programar despachos.

## 4. Requisitos

### Requisito 1: Gestión de Repartidores y Asignación de Turnos
El sistema DEBE permitir registrar, modificar y desactivar operadores de reparto, así como definir su horario y turno diario de operación.

#### Escenario: Registro exitoso de un nuevo repartidor
- DADO que un Gestor de Flota con rol administrativo ingresa los datos de un nuevo repartidor (nombre, DNI, teléfono, brevete/licencia de conducir y turno asignado).
- CUANDO confirma el registro en el panel de flota.
- ENTONCES el sistema valida que el documento de identidad no esté duplicado, guarda el registro con estado inicial `DISPONIBLE` y retorna el identificador único generado.

#### Escenario: Desactivación temporal de operador por ausencia o descanso
- DADO un repartidor que solicita permiso médico o no labora en el turno actual.
- CUANDO el Gestor cambia su estado operativo a `FUERA_DE_TURNO` o inactivo.
- ENTONCES el sistema actualiza de inmediato su disponibilidad y lo excluye automáticamente del catálogo de asignaciones disponibles.

### Requisito 2: Gestión de Flota Vehicular y Parámetros de Capacidad
El sistema DEBE permitir registrar vehículos de reparto definiendo su tipo, placa de rodaje y topes máximos de capacidad física (peso y volumen).

#### Escenario: Configuración de límites de carga vehicular
- DADO que se da de alta un vehículo de tipo "Furgoneta" con capacidad máxima de 500 kg y 4.0 m³.
- CUANDO se asocia dicho vehículo al repartidor en su turno de trabajo.
- ENTONCES el sistema registra estos valores como los límites de carga diarios para el operador asociado.

### Requisito 3: Panel Gráfico de Monitoreo y Saturación de la Flota
El sistema DEBE presentar un tablero visual con el porcentaje de capacidad utilizada por repartidor y las alertas de saturación de carga diaria.

#### Escenario: Alerta visual de repartidor saturado
- DADO un repartidor que ha alcanzado el 90% o más de su capacidad máxima asignada para el día.
- CUANDO el Gestor de Flota visualiza el panel de monitoreo.
- ENTONCES el sistema destaca al operador con una barra de progreso en color rojo y una etiqueta de estado "Saturado", advirtiendo al equipo de programación.

### Requisito 4: API de Consulta de Disponibilidad para Programación de Despachos
El sistema DEBE proveer un endpoint eficiente `GET /api/v1/repartidores/disponibles` para que el Panel de Asignación (F-02) consulte qué operadores pueden recibir nuevos despachos sin incurrir en sobrecarga.

#### Escenario: Respuesta con catálogo de operadores disponibles y balance de carga
- DADO que existen 5 repartidores en turno, de los cuales 3 están en estado `DISPONIBLE` con capacidad remanente.
- CUANDO el frontend o backend del Integrante 2 invoca `GET /api/v1/repartidores/disponibles`.
- ENTONCES el servicio retorna la lista de los 3 operadores habilitados, detallando su capacidad ocupada, remanente en kg/m³ y número de paquetes en curso.

## 5. Requisitos no funcionales
- **Seguridad:** Operaciones del panel restringidas a roles `GESTOR_FLOTA` y `GESTOR_DESPACHO` mediante token JWT.
- **Eficiencia y Concurrencia:** El endpoint de repartidores disponibles debe responder en menos de 150 ms para evitar retardos al momento de programar pedidos en la cola del Integrante 2.
- **Integridad Referencial:** No se permite eliminar físicamente repartidores o vehículos que mantengan despachos históricos o activos asociados; únicamente se permite su desactivación lógica.

## 6. Fuera de alcance
- **Mantenimiento mecánico y taller:** El registro de reparaciones mecánicas complejas o compras de repuestos se gestiona en el ERP general de la compañía.
- **Monitoreo de telemetría OBD-II / Sensores IoT:** El cálculo de consumo de combustible o velocidad del vehículo físico no está comprendido en esta etapa.
- **Asignación directa de despachos:** La acción de vincular un pedido a un repartidor corresponde al Panel de Programación y Asignación (F-02, Integrante 2).

## Criterio de completitud
La capacidad se considera correctamente implementada cuando:
- El CRUD de repartidores y vehículos funciona con todas las validaciones de negocio.
- El panel gráfico refleja en tiempo real el estado y porcentaje de ocupación de la flota.
- El endpoint `GET /api/v1/repartidores/disponibles` suministra los datos correctos al Integrante 2.
- No se incorporan alcances no especificados.
