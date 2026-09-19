# Especificación SPEC-TRANS-PROC-02: Servicio Centralizado de Historial y Auditoría

**Tipo:** Proceso Interno de Backend / Componente Transversal  
**Macro-funcionalidad:** Capacidades Transversales del Módulo (overview.md)  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Todos los Componentes del Módulo / Auditores  

---

## 1. Contexto

La trazabilidad es un requisito transversal crítico (RT-02) en la distribución de mercancías. Para responder a reclamos de clientes, auditorías de inventario o disputas operativas, el sistema debe conservar una bitácora cronológica inalterable de cada evento que afecte a un despacho, indicando con precisión matemática qué cambió, qué componente lo originó, quién lo ejecutó y cuándo ocurrió en horario universal coordinado.

---

## 2. Propósito

Implementar el servicio centralizado de persistencia y consulta del historial de transiciones y auditoría de los despachos, garantizando la inmutabilidad de los registros, capturando marcas temporales en UTC y exponiendo la línea de tiempo operativa para los portales de seguimiento y paneles de gestión.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Definición de la entidad JPA inmutable `HistorialEstadoDespacho` y su tabla en PostgreSQL.
- Servicio transaccional `HistorialDespachoService` invocado obligatoriamente por la máquina de estados común (`SPEC-TRANS-PROC-01`) en cada transición.
- Campos capturados por cada evento:
  - `idHistorial` (UUID clave primaria).
  - `idDespacho` (UUID foráneo).
  - `estadoAnterior` (enum de estado previo o `null` si es creación).
  - `estadoNuevo` (enum de estado resultante).
  - `funcionalidadOrigen` (F-01, F-02, F-03, F-04, F-05 o SISTEMA).
  - `ejecutor` (identificador del usuario gestor, chofer o actor del sistema).
  - `origenOperacion` (`MANUAL` o `AUTOMATICO`).
  - `marcaTemporal` (Instant UTC del servidor).
  - `motivo` (código de motivo tipificado si aplica).
  - `observaciones` (texto descriptivo opcional).
- Exposición del endpoint de consulta `GET /api/v1/despachos/{idDespacho}/historial` ordenado cronológicamente.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Existencia del despacho y ejecución dentro de la misma transacción de cambio de estado.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| PostgreSQL (Supabase) | Almacenamiento persistente con índices sobre `(id_despacho, marca_temporal)`. |
| `SPEC-TRANS-PROC-01` | Máquina de estados que dispara el registro de historial. |

### 4.3. Resultados
- Registro inmutable insertado en la base de datos.
- Disponibilidad inmediata de la línea de tiempo para consultas de auditoría o tracking.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Registro atómico y campos obligatorios
El servicio DEBE registrar todos los campos requeridos en la misma transacción que el cambio de estado.

#### CA-01. Registro de transición manual en historial
- **DADO** una transición de `ASIGNADO` a `EN_CAMINO` ejecutada por el chofer "juan.perez".
- **CUANDO** se comitea la transacción.
- **ENTONCES** se inserta un registro en `historial_estados_despacho` con `estadoAnterior = ASIGNADO`, `estadoNuevo = EN_CAMINO`, `funcionalidadOrigen = F-03`, `ejecutor = juan.perez`, `origenOperacion = MANUAL` y `marcaTemporal` UTC.

#### CA-02. Registro de corte automático
- **DADO** un despacho cerrado por el batch nocturno.
- **CUANDO** se registra el historial.
- **ENTONCES** se guarda con `funcionalidadOrigen = F-03`, `ejecutor = SISTEMA_CORTE_AUTOMATICO`, `origenOperacion = AUTOMATICO` y `motivo = NO_INTENTADO`.

### RF-02. Consulta de línea de tiempo
El servicio DEBE devolver los eventos ordenados cronológicamente.

#### CA-03. Consulta cronológica de historial
- **DADO** un despacho que pasó por creación, asignación, traslado y entrega.
- **CUANDO** se invoca `GET /api/v1/despachos/{idDespacho}/historial`.
- **ENTONCES** se retorna un arreglo con los 4 hitos en estricto orden cronológico ascendente por fecha/hora.

---

## 6. Frontend

*N/A - Proceso de backend.* Consumido por la línea de tiempo de auditoría en los paneles del gestor y en el portal de seguimiento de clientes.

---

## 7. Backend

### 7.1. Entidad JPA inmutable (Java 21 / Spring Boot)
```java
@Entity
@Table(name = "historial_estados_despacho", indexes = {
    @Index(name = "idx_historial_despacho_fecha", columnList = "id_despacho, marca_temporal")
})
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class HistorialEstadoDespacho {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id_historial", updatable = false, nullable = false)
    private UUID idHistorial;

    @Column(name = "id_despacho", updatable = false, nullable = false)
    private UUID idDespacho;

    @Enumerated(EnumType.STRING)
    @Column(name = "estado_anterior", updatable = false)
    private EstadoDespacho estadoAnterior;

    @Enumerated(EnumType.STRING)
    @Column(name = "estado_nuevo", updatable = false, nullable = false)
    private EstadoDespacho estadoNuevo;

    @Column(name = "funcionalidad_origen", updatable = false, nullable = false)
    private String funcionalidadOrigen;

    @Column(name = "ejecutor", updatable = false, nullable = false)
    private String ejecutor;

    @Enumerated(EnumType.STRING)
    @Column(name = "origen_operacion", updatable = false, nullable = false)
    private TipoOrigenOperacion origenOperacion;

    @Column(name = "marca_temporal", updatable = false, nullable = false)
    private Instant marcaTemporal;

    @Column(name = "motivo", updatable = false)
    private String motivo;

    @Column(name = "observaciones", updatable = false)
    private String observaciones;
}
```

---

## 8. Requisitos no funcionales

- **Inmutabilidad Absoluta:** Tabla configurada sin permisos de `UPDATE` ni `DELETE` (Append-Only Log).
- **Rendimiento de Consulta:** Retorno del historial completo de un despacho en menos de 20 ms.
- **Normalización Temporal:** Marcas de tiempo exclusivamente en formato ISO-8601 UTC (`yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`).

---

## 9. Fuera de alcance

- Registro de auditoría de tablas maestras (zonas o vehículos); este servicio se enfoca exclusivamente en la trazabilidad del ciclo de vida de los despachos.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Data Insertion Test | `@DataJpaTest` | Registro insertado con todos los campos obligatorios. |
| CA-02 | Automatic Origin Test | JUnit 5 | Se persiste correctamente `origenOperacion = AUTOMATICO`. |
| CA-03 | Timeline Order Test | MockMvc | Lista JSON retornada ordenada ascendentemente por `marcaTemporal`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Toda transición de estado del módulo genere de forma obligatoria su registro de historial.
2. La entidad sea estrictamente de solo inserción (inmutable).
3. El endpoint de consulta provea la línea de tiempo ordenada a los consumidores.
