# Especificación SPEC-F05-FORM-02: Panel y Formulario de Catálogo de Vehículos

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-05: Monitoreo de Flota, Operadores y Capacidad Diaria  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Flota / Administrador  

---

## 1. Contexto

La flota de distribución es heterogénea y comprende desde motocicletas ágiles para paquetería menor hasta furgonetas de alta capacidad cúbica para electrodomésticos o pedidos voluminosos. Para que el algoritmo de asignación de despachos (F-02) no sobrecargue los vehículos, se requiere un inventario centralizado donde se parametricen las capacidades técnicas exactas y el estado operativo de cada unidad de transporte.

---

## 2. Propósito

Proveer una interfaz de usuario web responsive para catalogar, dar de alta, editar y gestionar el estado operativo de los vehículos de la empresa, configurando sus límites máximos de carga en peso (kg), volumen cúbico (m³) y cantidad tope de paquetes simultáneos en ruta.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Tabla paginada de vehículos con filtros por tipo (`MOTO`, `AUTO`, `FURGONETA`), estado operativo (`DISPONIBLE`, `EN_USO`, `EN_MANTENIMIENTO`, `DE_BAJA`) y buscador por placa.
- Formulario modal de alta y edición de vehículo con los campos:
  - Tipo de vehículo (selector con defaults sugeridos).
  - Placa de rodaje (alfanumérico único con formato estándar peruano, ej. `ABC-123`).
  - Capacidad máxima de peso (kg, mayor a cero).
  - Capacidad máxima de volumen (m³, mayor a cero).
  - Límite máximo de paquetes en ruta (número entero positivo).
  - Marca, modelo y año de fabricación (opcionales para referencia técnica).
- Acción de cambio de estado a `EN_MANTENIMIENTO`:
  - Si el vehículo está en una jornada con despachos en curso (`ASIGNADO` o `EN_CAMINO`), se rechaza la operación con HTTP `409 Conflict`.
  - Si no tiene despachos en curso, se autoriza el mantenimiento y se libera al repartidor asignado.
- Baja lógica del vehículo (`DE_BAJA`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Usuario autenticado con rol `GESTOR_FLOTA` o `ADMIN`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/vehiculos` | Obtener el catálogo de vehículos con filtros. |
| `POST /api/v1/vehiculos` | Crear vehículo validando unicidad de placa. |
| `PATCH /api/v1/vehiculos/{id}/estado` | Cambiar estado a mantenimiento o baja. |

### 4.3. Resultados
- Vehículo registrado con sus límites de ingeniería en base de datos.
- Disponibilidad actualizada para las asignaciones diarias de jornada.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Registro y límites de capacidad
El formulario DEBE registrar los límites de carga y validar la unicidad de la placa.

#### CA-01. Registro exitoso de furgoneta
- **DADO** que el gestor selecciona tipo `FURGONETA`, ingresa placa "ABC-123", 600.0 kg, 4.5 m³ y 80 paquetes máximos.
- **CUANDO** confirma el formulario.
- **ENTONCES** el backend valida unicidad, persiste la unidad en estado `DISPONIBLE`, responde `201 Created` y la tabla se actualiza.

#### CA-02. Rechazo por placa duplicada
- **DADO** un vehículo previamente registrado con la placa "ABC-123".
- **CUANDO** se intenta dar de alta otro vehículo con la misma placa.
- **ENTONCES** el sistema responde `409 Conflict` con el mensaje *"La placa ingresada ya se encuentra registrada en el sistema"*.

### RF-02. Gestión de mantenimiento y bloqueo preventivo
El sistema DEBE impedir enviar a mantenimiento vehículos con entregas en curso.

#### CA-03. Envío a mantenimiento bloqueado por despachos activos
- **DADO** un vehículo asignado a una jornada con 2 paquetes en `EN_CAMINO`.
- **CUANDO** el gestor intenta pasarlo a `EN_MANTENIMIENTO`.
- **ENTONCES** el sistema responde `409 Conflict` informando *"El vehículo tiene despachos activos en ruta. Reasigne los paquetes antes de ingresarlo a mantenimiento"*.

#### CA-04. Envío a mantenimiento exitoso sin paquetes activos
- **DADO** un vehículo en jornada pero sin despachos asignados pendientes.
- **CUANDO** se confirma el cambio a `EN_MANTENIMIENTO`.
- **ENTONCES** el estado cambia a `EN_MANTENIMIENTO`, la jornada se cierra liberando al conductor, y el vehículo queda excluido de futuras asignaciones.

---

## 6. Frontend

### 6.1. Componentes
- **`VehiclesCatalogPage`**: Vista general con estadísticas de flota (total unidades, operativas, en taller).
- **`VehicleFormModal`**: Diálogo modal con selector de tipo que autocompleta valores sugeridos de carga.
- **`PlateInput`**: Input con máscara de texto y conversión automática a mayúsculas.
- **`MaintenanceDialog`**: Diálogo de confirmación para entrada a taller mecánico.

---

## 7. Backend (Contrato consumido)

- **Ruta creación:** `POST /api/v1/vehiculos`
- **Cuerpo:**
```json
{
  "placa": "ABC-123",
  "tipo": "FURGONETA",
  "capacidadMaxKg": 600.0,
  "capacidadMaxM3": 4.5,
  "maxPaquetesRuta": 80,
  "marca": "Hyundai",
  "modelo": "H1",
  "ano": 2022
}
```
- **Ruta estado:** `PATCH /api/v1/vehiculos/{idVehiculo}/estado` (`{ "estado": "EN_MANTENIMIENTO", "motivo": "Revisión técnica de frenos" }`)

---

## 8. Requisitos no funcionales

- **Integridad:** La placa vehicular es clave natural única indexada (`UNIQUE INDEX(placa)`).
- **Seguridad:** Acceso restringido a `GESTOR_FLOTA` y `ADMIN`.

---

## 9. Fuera de alcance

- Control de telemetría OBD-II o consumo de combustible en tiempo real.
- Registro de gastos de facturas de talleres mecánicos.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI Form Test | RTL / Vitest | Formulario válido envía JSON estructurado y recibe `201`. |
| CA-02 | Database Unique Test | `@DataJpaTest` | Intento de duplicar placa arroja `DataIntegrityViolationException`. |
| CA-03 | Active Shipments Guard | JUnit 5 | Chofer con despachos activos bloquea paso a mantenimiento con `409`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El catálogo permita parametrizar los límites de kg, m³ y paquetes por vehículo.
2. Se garantice la unicidad estricta de placas de rodaje.
3. Se prevenga el paso a mantenimiento de vehículos con entregas en ruta.
