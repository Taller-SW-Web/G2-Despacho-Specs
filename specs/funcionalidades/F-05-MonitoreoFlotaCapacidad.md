# Especificación: F-05 - Panel de Monitoreo de Flota, Operadores y Capacidad Diaria

## 1. Contexto
La operación de última milla depende críticamente de la gestión de los recursos físicos (vehículos) y humanos (conductores/repartidores). Sin un control centralizado de los turnos de trabajo, las capacidades de carga y el estado operativo diario, la asignación de pedidos corre el riesgo de sobrecargar a ciertos repartidores, asignar envíos a personal ausente o designar paquetes pesados a vehículos sin capacidad suficiente (ej. una moto).

Este subsistema administra las tablas maestras de la flota y los repartidores de Despacho. Opera como el núcleo de disponibilidad logística, proveyendo información esencial al **Panel de Programación y Asignación de Despachos** (F-02, a cargo de Tarqui) y sirviendo como base para el inicio de sesión de la **Web Responsive del Repartidor** (F-03, a cargo de Max).

## 2. Propósito
Proveer al Gestor de Flota (y al administrador del módulo de despacho) de un panel de control interactivo para:
- Gestionar el ciclo de vida del personal de reparto y los vehículos.
- Configurar límites operativos diarios y de turno (máximo de paquetes, peso y volumen).
- Asignar qué vehículo usará qué repartidor en el día actual.
- Supervisar en tiempo real la disponibilidad, ocupación y saturación de la flota mediante métricas, indicadores gráficos y alertas automáticas.

## 3. Alcance
Esta especificación comprende:
- **CRUD administrativo de Repartidores:** Registro, edición, cambios de estado (Activo, Inactivo, En Descanso) y asignación de turnos (Mañana, Tarde, Noche).
- **CRUD administrativo de Vehículos:** Registro de unidades (moto, furgoneta, auto), placa, estado mecánico y establecimiento de su capacidad máxima (peso en kg, volumen en m³ y cantidad tope de paquetes).
- **Asignación Operativa Diaria:** Interfaz para emparejar a un repartidor con un vehículo para su jornada actual.
- **Panel Gráfico (Dashboard) en tiempo real:**
  - Total de repartidores por estado (`ACTIVO`, `EN_RUTA`, `DISPONIBLE`, `SATURADO`, `INACTIVO`).
  - Barra de progreso por repartidor mostrando la capacidad ocupada (ej. `30/40 paquetes (75%)`).
- **Exposición de API (Backend):** Endpoint clave `GET /api/v1/repartidores/disponibles` para consumo directo por parte del servicio de programación (F-02).

## 4. Requisitos Funcionales

### Requisito 1: Gestión Integral de Repartidores
El sistema DEBE permitir mantener un registro actualizado del personal, controlando quién puede recibir asignaciones.

#### Escenario 1.1: Alta de un nuevo operador
- **DADO** que el Gestor de Flota requiere registrar a un nuevo operador.
- **CUANDO** ingresa los datos personales (Nombres, Apellidos, DNI/CE, Teléfono, Brevete) y define su turno habitual.
- **ENTONCES** el sistema valida que el documento de identidad no exista previamente, guarda el registro con estado `INACTIVO` (hasta que inicie turno) y autogenera sus credenciales de acceso para la web responsive.

#### Escenario 1.2: Cambio de estado a No Disponible (Baja médica o término de turno)
- **DADO** un repartidor que finalizó su jornada o reportó una emergencia.
- **CUANDO** el Gestor cambia su estado operativo a `FUERA_DE_TURNO` o `INACTIVO`.
- **ENTONCES** el sistema actualiza su disponibilidad en tiempo real, bloquea nuevas asignaciones automáticas y lo remueve de la lista de operadores disponibles que consume el F-02.

### Requisito 2: Gestión de Flota y Parámetros de Capacidad
El sistema DEBE mantener el catálogo de vehículos, que determina la capacidad real de carga de cada operador asignado a ellos.

#### Escenario 2.1: Registro de un vehículo de carga mayor
- **DADO** que se da de alta una nueva "Furgoneta".
- **CUANDO** el Gestor ingresa su placa "ABC-123", y define capacidades máximas: 500 kg, 4.0 m³ y tope de 150 paquetes diarios.
- **ENTONCES** el sistema guarda la unidad con estado `DISPONIBLE`. 

#### Escenario 2.2: Emparejamiento Diario (Repartidor - Vehículo)
- **DADO** que empieza el turno de la mañana.
- **CUANDO** el Gestor vincula la furgoneta "ABC-123" al repartidor "Juan Pérez" para el día de hoy.
- **ENTONCES** el sistema hereda los límites de carga de la furgoneta a "Juan Pérez", permitiéndole recibir hasta 150 paquetes o 500 kg en su ruta.

### Requisito 3: Panel Gráfico de Monitoreo y Alertas de Saturación
El sistema DEBE calcular dinámicamente la saturación sumando el volumen, peso o cantidad de despachos actualmente asignados en estado `EN_CAMINO` o `ASIGNADO`.

#### Escenario 3.1: Alerta visual de repartidor saturado
- **DADO** un repartidor con tope de 50 paquetes y se le han asignado 48 despachos.
- **CUANDO** el Gestor visualiza el Dashboard de Flota.
- **ENTONCES** la fila de ese operador muestra una barra de progreso en color rojo (96% de saturación) y muestra la etiqueta `SATURADO`.

### Requisito 4: API de Disponibilidad para Programación (F-02)
El sistema DEBE exponer un servicio para que el módulo de Programación filtre y elija repartidores idóneos sin sobrepasar sus límites.

#### Escenario 4.1: Solicitud de repartidores disponibles
- **DADO** que el sistema de asignación (F-02) necesita asignar 5 paquetes pequeños.
- **CUANDO** invoca el endpoint `GET /api/v1/repartidores/disponibles`.
- **ENTONCES** el API responde con un JSON que incluye únicamente a los operadores en estado `DISPONIBLE` o `EN_RUTA` cuya capacidad restante permita asumir más carga.
- **Y** la respuesta excluye a operadores `SATURADOS` o `FUERA_DE_TURNO`.

*Estructura esperada de respuesta (Ejemplo referencial):*
```json
{
  "repartidores": [
    {
      "idRepartidor": 101,
      "nombre": "Carlos Mendoza",
      "vehiculo": "Moto (Placa XYZ-789)",
      "capacidadMaxima": 40,
      "paquetesAsignados": 25,
      "porcentajeOcupacion": 62.5,
      "estado": "EN_RUTA"
    }
  ]
}
```

## 5. Requisitos no funcionales
- **Alta Disponibilidad y Concurrencia:** El endpoint `GET /api/v1/repartidores/disponibles` será consumido frecuentemente. Debe tener un tiempo de respuesta menor a 200 ms.
- **Seguridad (Autenticación):** Todas las acciones del CRUD y consulta del dashboard están protegidas mediante un Token JWT, requiriendo el rol `GESTOR_FLOTA` o `ADMIN_DESPACHO`.
- **Integridad Referencial de Auditoría (Soft Delete):** No se pueden eliminar físicamente de la base de datos repartidores ni vehículos que tengan historial de entregas. Se utilizará borrado lógico (`estado = ELIMINADO`).

## 6. Fuera de Alcance
- **Mantenimiento mecánico y costos:** Registrar gastos de gasolina, refacciones o revisiones técnicas vehiculares es competencia de un ERP externo.
- **Rastreo GPS en tiempo real del vehículo:** El seguimiento punto a punto con telemetría no se incluye en esta fase. Solo se rastrean los "cambios de estado" de los paquetes.
- **Asignación directa de pedidos:** Esta funcionalidad *prepara y provee* la lista de la flota, pero la acción de hacer "Match" entre un paquete y el repartidor es responsabilidad exclusiva del Panel de Programación (F-02).

## 7. Criterio de Completitud
Se considerará aprobada esta funcionalidad cuando:
1. El Gestor pueda realizar el CRUD completo de operadores y vehículos sin errores.
2. El Dashboard calcule y pinte correctamente los porcentajes de saturación y cambie de colores (verde, amarillo, rojo) según la carga del día.
3. El Integrante 2 (Tarqui) pueda consumir el endpoint `/disponibles` e integre la lista en su flujo de trabajo exitosamente.
4. Existan pruebas unitarias comprobando el cálculo de la saturación y pruebas de integración para el endpoint de disponibilidad.
