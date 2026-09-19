# Especificación SPEC-F05-PROC-01: Motor Dinámico de Ocupación y Estado Operativo

**Tipo:** Proceso Interno de Backend / Motor de Dominio  
**Macro-funcionalidad:** F-05: Monitoreo de Flota, Operadores y Capacidad Diaria  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Servicios Internos del Sistema  

---

## 1. Contexto

Para que la asignación de paquetes y el monitoreo de flota funcionen sin inconsistencias, debe existir una única fuente de verdad matemática sobre la carga activa que transporta cada operador. El sistema no debe almacenar saldos estáticos en tablas que puedan desfasarse; en su lugar, la ocupación y el estado operativo del chofer deben computarse dinámicamente a partir del estado real de los despachos que se encuentran bajo su custodia física.

---

## 2. Propósito

Implementar el motor de cálculo de backend encargado de evaluar la carga física activa en peso (kg), volumen (m³) y cantidad de bultos en poder del repartidor, deduciendo en tiempo real su capacidad remanente y derivando de forma determinista su estado operativo (`DISPONIBLE`, `EN_RUTA`, `SATURADO`, `FUERA_DE_TURNO`).

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Regla de inclusión de despachos en custodia:
  - Cuentan como carga activa los despachos asignados al chofer en estados: `ASIGNADO`, `EN_CAMINO` y `FALLIDO` que aún no hayan sido recibidos físicamente en el centro (`recibidoEnCentro == false`).
  - NO cuentan como carga los despachos en estados terminales: `ENTREGADO`, `CANCELADO`, `DEVUELTO_A_ORIGEN`, ni los `FALLIDO` cuya recepción física ya fue confirmada en el centro (`recibidoEnCentro == true`).
- Fórmulas de agregación:
  - `pesoCargaActual = SUM(d.pesoKg)`
  - `volumenCargaActual = SUM(d.volumenM3)`
  - `paquetesCargaActual = COUNT(d.idDespacho)`
- Deducción de saldos remanentes contra el vehículo emparejado en la jornada:
  - `remanenteKg = max(0, capacidadMaxKg - pesoCargaActual)`
  - `remanenteM3 = max(0, capacidadMaxM3 - volumenCargaActual)`
  - `remanentePaquetes = max(0, maxPaquetesRuta - paquetesCargaActual)`
- Algoritmo de derivación del estado operativo del repartidor:
  1. Si no cuenta con asignación de jornada activa en la fecha: `FUERA_DE_TURNO`.
  2. Si `remanenteKg <= 0` O `remanenteM3 <= 0` O `remanentePaquetes <= 0`: `SATURADO`.
  3. Si tiene al menos un despacho en estado `EN_CAMINO`: `EN_RUTA`.
  4. En cualquier otro caso con jornada activa: `DISPONIBLE`.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Repartidor con jornada abierta en la fecha actual.
- Conexión a la base de datos PostgreSQL.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `DespachoRepository` | Ejecutar la consulta de agregación sobre los despachos en custodia. |
| `JornadaRepository` | Obtener los límites del vehículo emparejado en la jornada. |

### 4.3. Resultados
- Capacidades remanentes y estado operativo actualizados y listos para ser expuestos a F-02 y al dashboard de F-05.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Cómputo de carga y liberación de espacio
El motor DEBE sumarizar únicamente los paquetes que el repartidor transporta físicamente.

#### CA-01. Liberación inmediata de espacio tras entrega
- **DADO** un repartidor con 50 kg de carga y un despacho de 10 kg en `EN_CAMINO`.
- **CUANDO** el despacho transiciona a `ENTREGADO`.
- **ENTONCES** el motor recalcula la ocupación del chofer en exactamente 40 kg y su saldo remanente aumenta en 10 kg.

#### CA-02. Paquete fallido continúa ocupando espacio hasta recepción
- **DADO** un despacho de 15 kg que pasa a `FALLIDO` con `recibidoEnCentro = false`.
- **CUANDO** se calcula la ocupación del repartidor.
- **ENTONCES** los 15 kg siguen sumando a la carga del chofer.
- **CUANDO** el gestor confirma la recepción en el centro (`recibidoEnCentro = true` en F-04).
- **ENTONCES** los 15 kg se liberan inmediatamente del balance del operador.

### RF-02. Derivación del estado operativo
El estado del repartidor DEBE responder automáticamente a los umbrales de saturación y traslado.

#### CA-03. Paso a SATURADO por cualquiera de las 3 restricciones
- **DADO** un repartidor con furgoneta de 500 kg, 4 m³ y 60 paquetes máximos.
- **CUANDO** acumula 60 paquetes pero su peso total es de solo 200 kg.
- **ENTONCES** el motor deriva su estado a `SATURADO` y lo excluye de la consulta de disponibilidad para nuevas asignaciones.

#### CA-04. Transición a EN_RUTA y vuelta a DISPONIBLE
- **DADO** un chofer en estado `DISPONIBLE`.
- **CUANDO** se inicia el traslado de su primer paquete (`EN_CAMINO`).
- **ENTONCES** su estado pasa a `EN_RUTA`.
- **CUANDO** dicho paquete se entrega y no tiene otros en camino.
- **ENTONCES** su estado retorna a `DISPONIBLE`.

---

## 6. Frontend

*N/A - Proceso puramente de backend.* Consumido por `SPEC-F05-FORM-04` y `SPEC-F05-PROC-02`.

---

## 7. Backend

### 7.1. Consulta de Agregación Nativa en PostgreSQL
```java
@Repository
public interface DespachoCargaRepository extends JpaRepository<Despacho, UUID> {

    @Query("""
        SELECT new com.modulodespacho.flota.dto.CargaActivaDto(
            COALESCE(SUM(d.pesoKg), 0.0),
            COALESCE(SUM(d.volumenM3), 0.0),
            COUNT(d.idDespacho),
            COUNT(CASE WHEN d.estado = 'EN_CAMINO' THEN 1 END)
        )
        FROM Despacho d
        WHERE d.idRepartidor = :idRepartidor
          AND d.estado IN ('ASIGNADO', 'EN_CAMINO', 'FALLIDO')
          AND (d.estado != 'FALLIDO' OR d.recibidoEnCentro = false)
    """)
    CargaActivaDto calcularCargaActivaRepartidor(@Param("idRepartidor") String idRepartidor);
}
```

### 7.2. Lógica de Derivación de Estado Operativo
```java
public EstadoOperativoRepartidor derivarEstado(LimitesVehiculoDto limites, CargaActivaDto carga, boolean tieneJornadaActiva) {
    if (!tieneJornadaActiva) {
        return EstadoOperativoRepartidor.FUERA_DE_TURNO;
    }

    boolean saturado = carga.pesoTotal() >= limites.maxKg() ||
                       carga.volumenTotal() >= limites.maxM3() ||
                       carga.totalPaquetes() >= limites.maxPaquetes();

    if (saturado) {
        return EstadoOperativoRepartidor.SATURADO;
    }

    if (carga.paquetesEnCamino() > 0) {
        return EstadoOperativoRepartidor.EN_RUTA;
    }

    return EstadoOperativoRepartidor.DISPONIBLE;
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** Consulta de agregación indexada por `(id_repartidor, estado, recibido_en_centro)` ejecutada en menos de 15 ms.
- **Fuente Única:** Ningún otro módulo calcula saldos propios; todos consumen la derivación de este motor.

---

## 9. Fuera de alcance

- Asignación de nuevas cargas (competencia de F-02).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Unit Aggregation Test | JUnit 5 | Paquete `ENTREGADO` no suma en `CargaActivaDto`. |
| CA-02 | Center Reception Test | `@DataJpaTest` | Paquete fallido deja de sumar cuando `recibidoEnCentro = true`. |
| CA-03 | Saturation Logic Test | JUnit 5 | Chofer al 100% en paquetes deriva a `SATURADO`. |
| CA-04 | State Transit Test | JUnit 5 | Chofer con `paquetesEnCamino > 0` deriva a `EN_RUTA`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. La ocupación refleje estrictamente los bultos en posesión física del chofer.
2. Los estados operativos se deriven dinámicamente sin tablas de saldo desfasadas.
3. Se superen las pruebas de agregación y límites de carga.
