# Especificación SPEC-F02-PROC-02: Asignación Transaccional y Control de Capacidad

**Tipo:** Proceso Interno / Caso de Uso Backend  
**Macro-funcionalidad:** F-02: Programación y Asignación de Despachos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho  

---

## 1. Contexto

La asignación de un despacho a un repartidor es una operación crítica en la logística de distribución. Debe ejecutarse con estrictas garantías ACID para evitar que dos gestores asignen simultáneamente el mismo paquete a diferentes choferes, y para asegurar que ningún vehículo sea despachado con exceso de peso o volumen sobre sus especificaciones técnicas aprobadas.

---

## 2. Propósito

Implementar el caso de uso transaccional de backend que valida la disponibilidad del operador, verifica que la carga no exceda la capacidad remanente del vehículo (en kilogramos, metros cúbicos y paquetes en ruta), aplica control de concurrencia optimista, transiciona el estado del despacho a `ASIGNADO` y descuenta atómicamente la capacidad del operador.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Exposición del endpoint `POST /api/v1/despachos/{idDespacho}/asignar`.
- Validación de precondiciones de estado del despacho (debe ser estrictamente `PENDIENTE_ASIGNACION`).
- Consulta de habilitación y balance del operador con el servicio de Flota F-05 (`SPEC-F05-PROC-02`).
- Verificación matemática de triple restricción de carga:
  1. `pesoDespacho <= capacidadRemanenteKg`
  2. `volumenDespacho <= capacidadRemanenteM3`
  3. `paquetesActuales + 1 <= maxPaquetesRuta`
- Manejo de control de concurrencia optimista mediante columna de versión (`@Version`) en la entidad `Despacho`.
- Transición de estado a `ASIGNADO` vinculando el `idRepartidor` y la fecha de asignación.
- Descuento y actualización de saldo operativo en F-05.
- Disparo síncrono del registro de auditoría (`SPEC-F02-PROC-03`) dentro de la misma transacción.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Token JWT con rol `GESTOR_DESPACHO` o `ADMIN`.
- El despacho debe existir y estar en estado `PENDIENTE_ASIGNACION`.
- El repartidor debe contar con asignación de jornada activa hoy y estar en estado operativo `DISPONIBLE` o `EN_RUTA`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| F-05 (`FlotaCapacidadService`) | Validar estado operativo del chofer y obtener capacidades remanentes. |
| `SPEC-TRANS-PROC-01` | Máquina de estados centralizada para validar la transición a `ASIGNADO`. |
| `SPEC-F02-PROC-03` | Servicio de auditoría que persiste el registro inmutable de la operación. |

### 4.3. Resultados
- Despacho actualizado a estado `ASIGNADO` con persistencia definitiva.
- Capacidad del vehículo del repartidor actualizada.
- Registro de auditoría guardado con marca temporal UTC y usuario gestor.
- Retorno de código `200 OK`.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Validación de capacidad y reglas de carga
El proceso DEBE bloquear cualquier asignación que supere los límites del vehículo.

#### CA-01. Asignación exitosa dentro de límites
- **DADO** un despacho de 15.0 kg y 0.08 m³ en estado `PENDIENTE_ASIGNACION` y un repartidor con remanente de 100.0 kg y 0.5 m³.
- **CUANDO** se ejecuta la asignación.
- **ENTONCES** el estado cambia a `ASIGNADO`, la capacidad remanente del chofer disminuye en 15.0 kg y 0.08 m³, se persiste la fecha de asignación y responde `200 OK`.

#### CA-02. Rechazo por sobrecarga de peso o volumen
- **DADO** un despacho cuyo peso (ej. 30 kg) supera la capacidad remanente del repartidor (ej. 20 kg).
- **CUANDO** se intenta confirmar la transacción.
- **ENTONCES** el sistema aborta la operación con código `422 Unprocessable Entity`, mensaje descriptivo *"Capacidad de carga del repartidor excedida"*, efectúa rollback y mantiene el despacho en `PENDIENTE_ASIGNACION`.

#### CA-03. Rechazo por operador fuera de turno o saturado
- **DADO** un repartidor cuyo estado en la jornada es `FUERA_DE_TURNO` o `SATURADO`.
- **CUANDO** se invoca el endpoint de asignación con dicho chofer.
- **ENTONCES** el backend responde `409 Conflict` con el mensaje *"El repartidor no se encuentra disponible para recibir asignaciones en la jornada actual"*.

### RF-02. Control de concurrencia e integridad transaccional
El proceso DEBE garantizar aislamiento y atomicidad en ambientes multi-usuario.

#### CA-04. Detección de asignación concurrente (Optimistic Locking)
- **DADO** dos gestores que intentan asignar simultáneamente el mismo despacho.
- **CUANDO** la primera transacción confirma y la segunda intenta comitear con una versión desactualizada.
- **ENTONCES** el backend intercepta `OptimisticLockingFailureException`, rechaza la segunda petición con `409 Conflict` e informa *"El despacho ya fue asignado o modificado por otro usuario"*.

---

## 6. Frontend

*N/A - Proceso exclusivamente de backend.* La interacción visual que consume este caso de uso reside en el modal `SPEC-F02-FORM-02`.

---

## 7. Backend

### 7.1. Componentes y lógica del servicio (Java 21 / Spring Boot)
```java
@Service
public class AsignacionDespachoService {

    private final DespachoRepository despachoRepository;
    private final FlotaCapacidadClient flotaClient;
    private final AuditoriaAsignacionService auditoriaService;

    @Transactional(isolation = Isolation.READ_COMMITTED)
    public DespachoResponse asignarDespacho(UUID idDespacho, AsignacionRequest request, String usuarioGestor) {
        // 1. Cargar despacho con lock optimista
        Despacho despacho = despachoRepository.findById(idDespacho)
            .orElseThrow(() -> new RecursoNoEncontradoException("Despacho no encontrado"));

        // 2. Validar estado inicial
        if (despacho.getEstado() != EstadoDespacho.PENDIENTE_ASIGNACION) {
            throw new ConflictoEstadoException("El despacho no se encuentra en estado PENDIENTE_ASIGNACION");
        }

        // 3. Validar chofer y capacidad en F-05
        CapacidadRepartidorDto chofer = flotaClient.obtenerCapacidadRepartidor(request.idRepartidor());
        if (!chofer.estaDisponible()) {
            throw new ConflictoOperativoException("El repartidor no está disponible");
        }
        if (despacho.getPesoKg() > chofer.capacidadRemanenteKg() || 
            despacho.getVolumenM3() > chofer.capacidadRemanenteM3()) {
            throw new CapacidadExcedidaException("Capacidad de carga del repartidor excedida");
        }

        // 4. Transicionar estado
        despacho.setEstado(EstadoDespacho.ASIGNADO);
        despacho.setIdRepartidor(request.idRepartidor());
        despacho.setFechaAsignacion(Instant.now());
        despacho.setObservacionesAsignacion(request.observaciones());
        despachoRepository.save(despacho);

        // 5. Descontar cupo en F-05
        flotaClient.descontarCapacidad(chofer.idRepartidor(), despacho.getPesoKg(), despacho.getVolumenM3());

        // 6. Registrar auditoría atómica
        auditoriaService.registrarAuditoria(despacho, chofer, usuarioGestor);

        return DespachoMapper.toResponse(despacho);
    }
}
```

---

## 8. Requisitos no funcionales

- **Atomicidad y Aislamiento:** Anotado con `@Transactional`. Si la deducción de capacidad o el registro de auditoría fallan, la transacción completa revierte (rollback total).
- **Rendimiento:** Ejecución completa de la asignación en menos de 200 ms.
- **Control de Bloqueos:** Uso de `@Version Long version` en la entidad `Despacho` para evitar bloqueos pesimistas que degraden la concurrencia de la base de datos.

---

## 9. Fuera de alcance

- Ruteo geográfico y secuencia de parada en calle (corresponde a F-03).
- Registro de salida del almacén físico hacia el vehículo.
- Modificación de datos del cliente o del pedido.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Integration Test | `@SpringBootTest` | Estado `ASIGNADO` y balance descontado en base de datos. |
| CA-02 | Business Rule Unit | JUnit 5 + Mockito | Excepción `CapacidadExcedidaException` capturada con `422`. |
| CA-03 | Mocked Rule | Mockito | Chofer `FUERA_DE_TURNO` provoca respuesta HTTP `409 Conflict`. |
| CA-04 | Concurrency Test | Testcontainers (Multi-thread) | 2 hilos simultáneos: 1 éxito (`200`) y 1 conflicto (`409`). |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El caso de uso esté implementado con `@Transactional` e inmutabilidad de estados.
2. Se verifiquen exitosamente las pruebas de concurrencia simulando accesos simultáneos.
3. Se garantice que ninguna asignación sobrepase los límites de peso o volumen vehicular.
