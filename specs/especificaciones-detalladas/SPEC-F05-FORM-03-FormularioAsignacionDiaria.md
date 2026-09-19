# Especificación SPEC-F05-FORM-03: Formulario de Asignación Diaria de Jornada

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-05: Monitoreo de Flota, Operadores y Capacidad Diaria  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Flota  

---

## 1. Contexto

Al iniciar cada jornada operativa en el centro de despacho, el Gestor de Flota debe emparejar al personal de transporte con los recursos físicos disponibles. Este emparejamiento diario vincula al repartidor con un vehículo específico y con la zona geográfica en la que operará durante el día, determinando la capacidad máxima de carga que tendrá habilitada para recibir asignaciones de pedidos de F-02.

---

## 2. Propósito

Proveer una interfaz de usuario web responsive para crear la asignación operativa del día, emparejando un Repartidor activo, un Vehículo disponible y una Zona geográfica activa de F-01, validando la unicidad de recursos por jornada y habilitando al chofer en estado `DISPONIBLE` para recibir despachos.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Formulario de apertura de jornada con 3 selectores dependientes:
  - Repartidor: lista únicamente conductores en estado `ACTIVO`, vinculados con Seguridad y actualmente en `FUERA_DE_TURNO`.
  - Vehículo: lista únicamente unidades en estado `DISPONIBLE`.
  - Zona de cobertura: lista zonas en estado `ACTIVO` provistas por F-01.
- Tarjeta de resumen de capacidades resultantes (muestra los kg, m³ y paquetes máximos que heredará la jornada a partir del vehículo seleccionado).
- Validación de unicidad de jornada: impide que un chofer o un vehículo cuenten con más de una jornada activa en la misma fecha (rechazo `409 Conflict`).
- Envío mediante `POST /api/v1/jornadas/asignacion-diaria`.
- Puesta en marcha operativa: el chofer pasa inmediatamente a estado `DISPONIBLE`, con saldo remanente al 100% de la capacidad del vehículo, apareciendo en la consulta de F-02.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Repartidor activo y vinculado a su cuenta de Seguridad.
- Vehículo disponible (no asignado a otro chofer hoy y fuera de taller).
- Zona activa en F-01.
- Usuario autenticado con rol `GESTOR_FLOTA` o `ADMIN`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| F-01 (Zonas y Tarifas) | Proveer el catálogo de zonas activas para el selector. |
| `POST /api/v1/jornadas/asignacion-diaria` | Endpoint backend que crea la jornada y habilita al operador. |
| F-02 (Programación) | Consumirá al chofer en su consulta de disponibilidad una vez creada la jornada. |

### 4.3. Resultados
- Jornada registrada en base de datos para la fecha actual.
- Repartidor en estado `DISPONIBLE` listo para recibir despachos.
- Vehículo marcado en estado `EN_USO`.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Emparejamiento y validación de recursos
El formulario DEBE validar que ninguno de los recursos esté comprometido en otra jornada.

#### CA-01. Asignación diaria exitosa
- **DADO** el repartidor "Juan Pérez" en `FUERA_DE_TURNO`, la furgoneta "ABC-123" disponible (600 kg, 4 m³, 80 paquetes) y la zona activa "Lima Moderna".
- **CUANDO** el gestor confirma la asignación diaria.
- **ENTONCES** el sistema crea la jornada, pasa a Juan Pérez a estado `DISPONIBLE` con saldo remanente de 600 kg / 4 m³ / 80 paquetes, marca la furgoneta como `EN_USO` y responde `201 Created`.

#### CA-02. Rechazo por repartidor ya asignado en la fecha
- **DADO** un repartidor que ya cuenta con una jornada abierta el día de hoy.
- **CUANDO** se intenta crear una segunda asignación para el mismo chofer.
- **ENTONCES** el backend rechaza la operación con código `409 Conflict` informando *"El repartidor ya cuenta con una jornada activa para la fecha actual"*.

#### CA-03. Rechazo por vehículo en uso
- **DADO** un vehículo que ya fue emparejado con otro chofer en el turno matutino.
- **CUANDO** se intenta asignar a un segundo conductor en la misma jornada.
- **ENTONCES** el sistema responde `409 Conflict` informando *"El vehículo seleccionado ya se encuentra asignado a otra jornada activa"*.

---

## 6. Frontend

### 6.1. Componentes
- **`DailyAssignmentModal`**: Diálogo modal de configuración de jornada.
- **`DriverSelectWithAvatar`**: Dropdown con buscador de choferes que muestra turno habitual.
- **`VehicleSelectWithSpecs`**: Dropdown de vehículos que muestra placa y capacidades.
- **`ZoneSelectDropdown`**: Dropdown de zonas activas.
- **`ResultingCapacityPreviewCard`**: Panel dinámico que muestra los límites que se asignarán a la jornada: Peso máximo, Volumen máximo y Paquetes máximos.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `POST /api/v1/jornadas/asignacion-diaria`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Content-Type: application/json`
- **Cuerpo:**
```json
{
  "idRepartidor": "REP-0012",
  "idVehiculo": "VEH-0045",
  "idZona": "ZONA-LIMA-MODERNA",
  "fecha": "2026-09-19",
  "turno": "MAÑANA"
}
```
- **Respuesta Exitosa (`201 Created`):**
```json
{
  "idJornada": "JOR-20260919-012",
  "idRepartidor": "REP-0012",
  "idVehiculo": "VEH-0045",
  "placa": "ABC-123",
  "estadoOperativo": "DISPONIBLE",
  "capacidadRemanenteKg": 600.0,
  "capacidadRemanenteM3": 4.5,
  "paquetesMaximos": 80
}
```

---

## 8. Requisitos no funcionales

- **Integridad:** Restricción de base de datos `UNIQUE(id_repartidor, fecha)` y `UNIQUE(id_vehiculo, fecha)` para garantizar que no existan duplicados ni ante condiciones de carrera.
- **Seguridad:** Rol requerido `GESTOR_FLOTA` o `ADMIN`.

---

## 9. Fuera de alcance

- Asignación de despachos individuales (responsabilidad de F-02).
- Planificación de turnos con semanas de anticipación (este formulario es para la operación del día).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Integration UI Test | Cypress | Submit válido crea jornada y chofer aparece en disponibilidad. |
| CA-02 | Unique Constraint Test | `@DataJpaTest` | Intento de doble jornada para chofer arroja `409 Conflict`. |
| CA-03 | Vehicle Guard Test | JUnit 5 | Vehículo en uso bloquea segunda jornada con `409 Conflict`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El formulario permita emparejar chofer, vehículo y zona de forma integrada.
2. Se garantice la unicidad de jornadas diarias por chofer y vehículo.
3. El operador pase a `DISPONIBLE` y figure de inmediato en la API de F-02.
