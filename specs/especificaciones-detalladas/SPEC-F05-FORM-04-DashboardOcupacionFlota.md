# Especificación SPEC-F05-FORM-04: Dashboard de Monitoreo Semafórico de Ocupación de Flota

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-05: Monitoreo de Flota, Operadores y Capacidad Diaria  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Flota / Gestor de Despacho  

---

## 1. Contexto

Durante el transcurso de la jornada, los repartidores reciben asignaciones desde el centro de despacho, inician traslados, entregan paquetes o reportan incidencias. El Gestor de Flota necesita una visión panorámica en tiempo real para supervisar qué choferes están cerca de saturarse, cuáles tienen capacidad ociosa para recibir más carga y cuántas unidades se encuentran actualmente rodando en calle.

---

## 2. Propósito

Proveer un panel de control (Dashboard) analítico y operativo web responsive que presente métricas consolidadas de la flota y una tabla de conductores en jornada activa con barras de progreso semaforizadas para peso (kg), volumen (m³) y paquetes, actualizadas reactivamente sin necesidad de recarga forzada de página.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Tarjetas de métricas globales de la flota:
  - Total de choferes en jornada hoy.
  - Choferes en estado `DISPONIBLE` (con capacidad para recibir carga).
  - Choferes en estado `EN_RUTA` (con al menos un paquete en traslado en calle).
  - Choferes en estado `SATURADO` (al 100% en cualquiera de sus 3 límites).
  - Choferes en estado `FUERA_DE_TURNO` (cerrados).
- Tabla detallada por repartidor en jornada:
  - Chofer, placa y tipo de vehículo, zona asignada.
  - Chip de estado operativo derivado en vivo.
  - Triple indicador semafórico de ocupación:
    1. Barra de Peso: `actualKg / maxKg` y porcentaje.
    2. Barra de Volumen: `actualM3 / maxM3` y porcentaje.
    3. Barra de Paquetes: `actualPaquetes / maxPaquetes` y porcentaje.
  - Reglas de coloración semafórica:
    - Verde: `< 70%` de ocupación.
    - Ámbar: `70% - 99%` de ocupación.
    - Rojo: `100%` (saturación total).
- Filtros por zona de trabajo y estado operativo.
- Refresco reactivo periódico (polling de 30 segundos o revalidación por foco).
- Botón de cierre manual de turno por contingencia (habilitado únicamente si el chofer no tiene despachos activos).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Existencia de jornadas abiertas en la fecha actual.
- Token JWT con rol `GESTOR_FLOTA`, `GESTOR_DESPACHO` o `ADMIN`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/flota/monitoreo` | Endpoint backend que computa y entrega los saldos de ocupación (`SPEC-F05-PROC-01`). |
| React Query / SWR | Manejo de caché y refresco automático en segundo plano. |

### 4.3. Resultados
- Supervisión en tiempo real de la capacidad remanente de toda la flota.
- Detección inmediata de cuellos de botella o desbalances de carga entre zonas.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Despliegue de métricas globales y semáforos
El panel DEBE reflejar fielmente la suma de las cargas de los despachos en curso.

#### CA-01. Repartidor saturado por paquetes o peso
- **DADO** un repartidor con vehículo de 80 paquetes máximos que tiene exactamente 80 despachos asignados o en camino.
- **CUANDO** el gestor observa el panel de monitoreo.
- **ENTONCES** el chofer se muestra con badge rojo `SATURADO`, la barra de paquetes al 100% en color rojo y se contabiliza dentro del contador global de saturados.

#### CA-02. Actualización de estado a "En Ruta"
- **DADO** un chofer en estado `DISPONIBLE` al cual se le registra su primer despacho en estado `EN_CAMINO`.
- **CUANDO** el dashboard refresca sus datos.
- **ENTONCES** el estado operativo del chofer cambia automáticamente a `EN_RUTA` y el contador de unidades en ruta se incrementa en 1.

#### CA-03. Coloración semafórica de barras
- **DADO** un chofer con 60% de peso, 75% de volumen y 100% de paquetes.
- **CUANDO** se renderizan sus indicadores.
- **ENTONCES** la barra de peso se colorea en verde, la de volumen en ámbar y la de paquetes en rojo, derivando el estado general a `SATURADO`.

---

## 6. Frontend

### 6.1. Componentes
- **`FleetMonitoringDashboard`**: Contenedor principal con grid de tarjetas superiores y tabla inferior.
- **`GlobalMetricsCards`**: 4 tarjetas con iconos temáticos y contadores animados.
- **`DriverOccupancyRow`**: Fila de tabla con avatar, datos de vehículo y el componente `TripleProgressBar`.
- **`TripleProgressBar`**: Componente compacto con 3 barras apiladas o en columnas con tooltips informativos de kilos, metros cúbicos y bultos.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `GET /api/v1/flota/monitoreo`
- **Cabeceras:** `Authorization: Bearer <JWT>`
- **Respuesta (`200 OK`):**
```json
{
  "fecha": "2026-09-19",
  "resumenGlobal": {
    "totalConductoresJornada": 8,
    "disponibles": 3,
    "enRuta": 3,
    "saturados": 2,
    "fueraDeTurno": 0
  },
  "conductores": [
    {
      "idRepartidor": "REP-0012",
      "nombre": "Juan Pérez",
      "vehiculo": "FURGONETA (ABC-123)",
      "zona": "Lima Moderna",
      "estadoOperativo": "SATURADO",
      "peso": { "actualKg": 600.0, "maxKg": 600.0, "porcentaje": 100.0 },
      "volumen": { "actualM3": 3.2, "maxM3": 4.5, "porcentaje": 71.1 },
      "paquetes": { "actual": 55, "max": 80, "porcentaje": 68.7 }
    }
  ]
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** Endpoint computado y servido en menos de 200 ms gracias a índices agregados en la tabla de despachos.
- **Visualización Ergonométrica:** Adaptable a pantallas panorámicas de centros de control de monitoreo (1920x1080).

---

## 9. Fuera de alcance

- Localización GPS en mapa en tiempo real de los vehículos (no se captura GPS de acuerdo al alcance del proyecto).
- Despacho directo de paquetes desde esta pantalla (se ejecuta en F-02).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Visual Semaphore Test | Storybook / RTL | Barras al 100% aplican clase CSS `bg-red-500`. |
| CA-02 | Polling Refresh Test | Cypress | Cambio en backend actualiza badge a `EN_RUTA` en siguiente ciclo. |
| CA-03 | Global Count Test | Vitest | Suma de estados coincide con total de choferes en jornada. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El dashboard muestre el balance de ocupación en kg, m³ y paquetes por chofer.
2. Aplique los colores verde, ámbar y rojo según los umbrales (<70%, 70-99%, 100%).
3. Mantenga sincronizadas las tarjetas de métricas globales con el detalle de la grilla.
