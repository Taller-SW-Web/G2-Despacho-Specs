# Especificación SPEC-F05-PROC-02: Servicio REST de Disponibilidad y Saldo Remanente

**Tipo:** Proceso Interno / API REST de Alto Rendimiento  
**Macro-funcionalidad:** F-05: Monitoreo de Flota, Operadores y Capacidad Diaria  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Programación y Asignación de Despachos (F-02)  

---

## 1. Contexto

Para que el Gestor de Despacho en F-02 pueda asignar paquetes a los choferes sin riesgo de sobrecarga ni asignación a personal fuera de turno, requiere un servicio de consulta ultra-rápido que devuelva en tiempo real qué conductores están habilitados en la fecha y zona del paquete, junto con sus saldos remanentes exactos en kilos, metros cúbicos y paquetes.

---

## 2. Propósito

Implementar el endpoint y servicio REST de alto rendimiento `GET /api/v1/repartidores/disponibles` que expone a F-02 el catálogo de operadores en turno con estado `DISPONIBLE` o `EN_RUTA` que cuenten con capacidad residual de transporte, calculada mediante el motor de ocupación (`SPEC-F05-PROC-01`).

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Exposición del endpoint `GET /api/v1/repartidores/disponibles`.
- Parámetros de consulta opcionales:
  - `idZona`: Filtra choferes asignados a una zona de cobertura específica.
  - `fecha`: Fecha de la jornada (por defecto la fecha actual del servidor).
- Filtrado estricto de operadores:
  - Excluye choferes en estado `FUERA_DE_TURNO` o dados de baja (`INACTIVO`).
  - Excluye choferes en estado `SATURADO` (aquellos que ya alcanzaron el 100% en peso, volumen o paquetes).
- Retorno estructurado con: datos del chofer, tipo y placa del vehículo, zona asignada, capacidades máximas, capacidades remanentes netas (kg, m³, paquetes) y porcentaje de ocupación global.
- Respuesta HTTP `200 OK` con arreglo vacío `[]` cuando no existan choferes disponibles con capacidad.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Token JWT con rol `GESTOR_DESPACHO`, `GESTOR_FLOTA` o `ADMIN`.
- Jornadas operativas registradas en la fecha consultada.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `SPEC-F05-PROC-01` | Motor dinámico que provee la carga y capacidad remanente por chofer. |
| F-02 (Asignación) | Consumidor principal del endpoint en su modal de asignación. |

### 4.3. Resultados
- Respuesta estructurada en menos de 100 ms para alimentar la interfaz de asignación de pedidos sin latencia perceptible.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Filtrado y exclusión de no habilitados
El endpoint DEBE devolver únicamente personal con capacidad remanente disponible.

#### CA-01. Consulta exitosa con choferes habilitados
- **DADO** 5 choferes en jornada: 2 en `DISPONIBLE`, 1 en `EN_RUTA` con saldo disponible, y 2 en `SATURADO`.
- **CUANDO** F-02 invoca `GET /api/v1/repartidores/disponibles?idZona=ZONA-LIMA-CENTRO`.
- **ENTONCES** el servicio responde `200 OK` retornando exactamente los 3 choferes habilitados con sus saldos remanentes, excluyendo a los 2 saturados.

#### CA-02. Consulta sin choferes disponibles
- **DADO** que todos los choferes de la zona están saturados al 100% o no hay jornadas abiertas.
- **CUANDO** se invoca el endpoint.
- **ENTONCES** el servicio responde `200 OK` con un arreglo JSON vacío `[]`.

---

## 6. Frontend

*N/A - Proceso de backend.* Consumido por el modal de asignación en `SPEC-F02-FORM-02`.

---

## 7. Backend

### 7.1. Controlador y DTO de Respuesta (Java 21 / Spring Boot)
```java
@RestController
@RequestMapping("/api/v1/repartidores")
@RequiredArgsConstructor
public class DisponibilidadFlotaController {

    private final DisponibilidadFlotaService disponibilidadService;

    @GetMapping("/disponibles")
    @PreAuthorize("hasAnyRole('GESTOR_DESPACHO', 'GESTOR_FLOTA', 'ADMIN')")
    public ResponseEntity<List<RepartidorDisponibleDto>> obtenerDisponibles(
            @RequestParam(required = false) String idZona,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate fecha) {
        
        LocalDate fechaConsulta = (fecha != null) ? fecha : LocalDate.now();
        List<RepartidorDisponibleDto> disponibles = disponibilidadService.consultarDisponibilidad(idZona, fechaConsulta);
        return ResponseEntity.ok(disponibles);
    }
}
```

### 7.2. Contrato HTTP de Respuesta (`200 OK`)
```json
[
  {
    "idRepartidor": "REP-0012",
    "nombre": "Juan Pérez",
    "tipoVehiculo": "FURGONETA",
    "placaVehiculo": "ABC-123",
    "idZona": "ZONA-LIMA-CENTRO",
    "nombreZona": "Lima Moderna / Centro",
    "capacidadMaxKg": 600.0,
    "capacidadRemanenteKg": 180.5,
    "capacidadMaxM3": 4.5,
    "capacidadRemanenteM3": 1.45,
    "maxPaquetesRuta": 80,
    "paquetesActuales": 35,
    "paquetesRemanentes": 45,
    "porcentajeOcupacion": 63.9,
    "estadoOperativo": "DISPONIBLE"
  }
]
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** SLA estricto de latencia P95 inferior a 100 ms.
- **Seguridad:** Autenticación obligatoria mediante JWT y verificación de permisos RBAC.

---

## 9. Fuera de alcance

- Asignación o deducción directa de capacidad (se procesa en F-02).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Integration Controller Test | MockMvc | Lista JSON estructurada filtrando saturados. |
| CA-02 | Empty State Test | JUnit 5 | Respuesta `200 OK` con `[]` cuando no hay disponibles. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El endpoint `GET /api/v1/repartidores/disponibles` opere con tiempo de respuesta < 100 ms.
2. Excluya automáticamente choferes saturados o fuera de turno.
3. Se integre limpiamente con el modal de asignación de F-02.
