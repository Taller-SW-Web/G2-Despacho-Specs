# Especificación SPEC-TRANS-PROC-01: Motor Central de Máquina de Estados del Despacho

**Tipo:** Proceso Interno de Backend / Componente Transversal  
**Macro-funcionalidad:** Capacidades Transversales del Módulo (overview.md)  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Todos los Servicios del Módulo (F-02, F-03, F-04)  

---

## 1. Contexto

El ciclo de vida de un despacho atraviesa múltiples estados a lo largo de su operación: desde su registro inicial en el centro, su asignación a un vehículo, el traslado en calle por el repartidor, hasta su entrega exitosa, reprogramación o devolución final a origen. Para evitar transiciones ilegales, estados huérfanos o corrupción de datos causada por peticiones concurrentes, debe existir una única máquina de estados centralizada que gobierne todo el ciclo.

---

## 2. Propósito

Implementar el componente de dominio transversal que valida, ejecuta y persiste todas las transiciones de estado del ciclo de vida del despacho, asegurando el cumplimiento estricto de la matriz oficial de transiciones, aplicando control de concurrencia optimista y bloqueando con HTTP `409 Conflict` cualquier intento de alteración no permitida.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Matriz de transiciones permitidas del ciclo de vida (definida en overview.md, sección 5):

| Estado Origen | Estado Destino | Módulo / Actor Ejecutor | Regla Adicional |
|---|---|---|---|
| *Ninguno (Creación)* | `PENDIENTE_ASIGNACION` | F-02 (Recepción / Simulación) | Inicia con 0 intentos |
| `PENDIENTE_ASIGNACION` | `ASIGNADO` | F-02 (Gestor de Despacho) | Requiere chofer con capacidad |
| `PENDIENTE_ASIGNACION` | `CANCELADO` | F-02 (Anulación comercial) | No requiere chofer |
| `ASIGNADO` | `CANCELADO` | F-02 (Anulación comercial) | Libera cupo en vehículo |
| `ASIGNADO` | `EN_CAMINO` | F-03 (Repartidor) | Inicia traslado en calle |
| `EN_CAMINO` | `ENTREGADO` | F-03 (Repartidor) | Requiere foto obligatoria |
| `EN_CAMINO` | `FALLIDO` | F-03 (Repartidor) | Requiere motivo y foto; suma +1 intento |
| `ASIGNADO` o `EN_CAMINO` | `FALLIDO` | F-03 (Cierre o corte nocturno) | Motivo `NO_INTENTADO`; no suma intento |
| `FALLIDO` | `PENDIENTE_ASIGNACION` | F-04 (Gestor de Despacho) | Exige `recibidoEnCentro = true` e intentos < 2 |
| `FALLIDO` | `DEVUELTO_A_ORIGEN` | F-04 (Gestor de Despacho) | Exige `recibidoEnCentro = true` |

- Rechazo taxativo de cualquier otra combinación con HTTP `409 Conflict`.
- Control de concurrencia optimista con anotación JPA `@Version` en la entidad `Despacho`.
- Invocación síncrona obligatoria al servicio de historial común (`SPEC-TRANS-PROC-02`) dentro de la misma transacción.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Despacho existente en base de datos.
- Contexto transaccional activo (`@Transactional`).

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `SPEC-TRANS-PROC-02` | Servicio de historial y auditoría que registra la transición. |
| `SPEC-TRANS-PROC-03` | Publicador outbox para notificar eventos externos. |

### 4.3. Resultados
- Estado actualizado con integridad matemática en la tabla `despachos`.
- Historial común alimentado de forma consistente.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Validación de matriz de transiciones
El motor DEBE rechazar cualquier cambio que viole la secuencia del ciclo de vida.

#### CA-01. Transición legal ejecutada
- **DADO** un despacho en estado `ASIGNADO`.
- **CUANDO** F-03 solicita pasar a `EN_CAMINO`.
- **ENTONCES** el motor valida la matriz, aplica el cambio a `EN_CAMINO` y dispara el registro en el historial.

#### CA-02. Transición ilegal rechazada
- **DADO** un despacho en estado `ENTREGADO`.
- **CUANDO** cualquier servicio o usuario intenta moverlo a `EN_CAMINO` o `PENDIENTE_ASIGNACION`.
- **ENTONCES** el motor rechaza la operación arrojando `TransicionEstadoInvalidaException` que responde HTTP `409 Conflict`, conservando el estado original.

### RF-02. Control de concurrencia optimista
El motor DEBE prevenir que dos transacciones simultáneas colisionen.

#### CA-03. Conflicto de versiones concurrentes
- **DADO** dos peticiones que leen el despacho en versión 1 (ej. cancelación de F-02 y entrega de F-03).
- **CUANDO** la primera comitea y la segunda intenta escribir.
- **ENTONCES** Hibernate lanza `OptimisticLockException`, la segunda operación revierte y retorna `409 Conflict`.

---

## 6. Frontend

*N/A - Componente de backend central.*

---

## 7. Backend

### 7.1. Validador de Máquina de Estados (Java 21 / Spring Boot)
```java
@Component
public class MaquinaEstadosDespacho {

    private static final Map<EstadoDespacho, Set<EstadoDespacho>> TRANSICIONES_VALIDAS = Map.of(
        EstadoDespacho.PENDIENTE_ASIGNACION, Set.of(EstadoDespacho.ASIGNADO, EstadoDespacho.CANCELADO),
        EstadoDespacho.ASIGNADO, Set.of(EstadoDespacho.EN_CAMINO, EstadoDespacho.CANCELADO, EstadoDespacho.FALLIDO),
        EstadoDespacho.EN_CAMINO, Set.of(EstadoDespacho.ENTREGADO, EstadoDespacho.FALLIDO),
        EstadoDespacho.FALLIDO, Set.of(EstadoDespacho.PENDIENTE_ASIGNACION, EstadoDespacho.DEVUELTO_A_ORIGEN),
        EstadoDespacho.ENTREGADO, Set.of(),
        EstadoDespacho.CANCELADO, Set.of(),
        EstadoDespacho.DEVUELTO_A_ORIGEN, Set.of()
    );

    public void validarTransicion(EstadoDespacho estadoOrigen, EstadoDespacho estadoDestino) {
        Set<EstadoDespacho> destinosPermitidos = TRANSICIONES_VALIDAS.getOrDefault(estadoOrigen, Set.of());
        if (!destinosPermitidos.contains(estadoDestino)) {
            throw new TransicionInvalidaException(
                String.format("Transición ilegal de estado: no se permite pasar de %s a %s", estadoOrigen, estadoDestino)
            );
        }
    }
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** Validación en memoria ejecutada en microsegundos (< 1 ms).
- **Atomicidad:** Transición y persistencia de auditoría envueltas en `@Transactional(isolation = Isolation.READ_COMMITTED)`.

---

## 9. Fuera de alcance

- Máquinas de estado de los pedidos comerciales de Ventas (Despacho solo gestiona el ciclo de vida del transporte físico).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Matrix Unit Test | JUnit 5 | Todas las transiciones válidas son aprobadas. |
| CA-02 | Matrix Rejection Test | JUnit 5 | Intentos de transición ilegal arrojan `TransicionInvalidaException`. |
| CA-03 | Multi-thread Concurrency | Testcontainers | Dos transacciones en paralelo resuelven con 1 éxito y 1 `409 Conflict`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Ninguna transición fuera de la matriz oficial sea aceptada por el backend.
2. El control de versiones optimista prevenga dobles escrituras concurrentes.
3. El componente sea el único autorizador de cambios de estado en el módulo.
