# Especificación SPEC-F03-PROC-03: Corte Automático de Jornada de Respaldo (Batch)

**Tipo:** Proceso Interno Programado / Job Batch  
**Macro-funcionalidad:** F-03: Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Proceso Automático del Sistema (Scheduler)  

---

## 1. Contexto

Por olvido del repartidor, agotamiento de batería de su celular o imprevistos de fuerza mayor al terminar su día, una jornada puede quedar sin cerrarse manualmente. Si esto ocurre, los despachos quedarían congelados en `ASIGNADO` o `EN_CAMINO` indefinidamente. El sistema debe contar con un mecanismo de respaldo automático que barra los turnos vencidos y garantice la coherencia operativa del módulo.

---

## 2. Propósito

Implementar el proceso programado por lotes (*Scheduled Cron Job*) que se ejecuta diariamente a la hora de corte configurada (ej. 22:00 UTC-5), detecta turnos de repartidores no cerrados, transiciona todos los despachos pendientes a `FALLIDO` con motivo `NO_INTENTADO` sin consumir intentos del cliente, y cambia el estado de los operadores a `FUERA_DE_TURNO`.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Configuración de tarea programada con Spring `@Scheduled` (expresión cron configurable en `application.yml`).
- Consulta de jornadas del día actual con estado operativo distinto a `FUERA_DE_TURNO`.
- Búsqueda en lote de despachos asignados a dichas jornadas que permanezcan en estado `ASIGNADO` o `EN_CAMINO`.
- Transición en lote a estado `FALLIDO` con el motivo tipificado exclusivo del sistema: `NO_INTENTADO`.
- Preservación del contador de intentos (no se incrementa `numeroIntento`).
- Marcado del despacho como pendiente de retorno físico (`pendienteRetornoCentro = true`) para su control en F-04.
- Invocación a F-05 para cerrar el turno del repartidor y liberar el vehículo.
- Registro en el historial del despacho indicando que la transición fue ejecutada por el actor `SISTEMA_CORTE_AUTOMATICO`.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- El servicio backend debe estar en ejecución y el scheduler habilitado (`@EnableScheduling`).
- Hora del servidor sincronizada vía NTP.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| Spring Task Scheduler | Motor de ejecución del cron job. |
| F-05 (`FlotaCapacidadService`) | Solicitar el cierre forzado del turno del chofer. |
| `SPEC-TRANS-PROC-02` | Registro en el historial común de transiciones. |

### 4.3. Resultados
- 100% de los despachos de la jornada quedan en estados terminales o fallidos resueltos antes de comenzar el día siguiente.
- Repartidores liberados para asignaciones futuras.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Detección y transición automática
El job DEBE barrer todos los despachos inconclusos del día.

#### CA-01. Ejecución del corte sobre turnos abiertos
- **DADO** un repartidor que finalizó su turno sin cerrar la app, dejando 3 despachos en `ASIGNADO` y 1 en `EN_CAMINO`.
- **CUANDO** se dispara el proceso de corte a la hora configurada (22:00).
- **ENTONCES** los 4 despachos pasan a estado `FALLIDO` con `codigoMotivo = NO_INTENTADO`, su contador de intentos no sufre variación, el chofer pasa a `FUERA_DE_TURNO` y el historial registra al ejecutor `SISTEMA_CORTE_AUTOMATICO`.

#### CA-02. Jornadas previamente cerradas
- **DADO** que todos los repartidores cerraron manualmente su turno antes de las 22:00.
- **CUANDO** se ejecuta el job nocturno.
- **ENTONCES** el proceso no realiza cambios en base de datos y emite log informativo *"Corte automático finalizado: 0 despachos afectados"*.

---

## 6. Frontend

*N/A - Proceso exclusivamente de backend.*

---

## 7. Backend

### 7.1. Implementación del Job Batch (Java 21 / Spring Boot)
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class CorteAutomaticoJornadaBatch {

    private final DespachoRepository despachoRepository;
    private final FlotaService flotaService;
    private final HistorialDespachoService historialService;

    // Se ejecuta a las 22:00 todos los días
    @Scheduled(cron = "${despacho.corte-automatico.cron:0 0 22 * * *}")
    @Transactional
    public void ejecutarCorteAutomatico() {
        log.info("Iniciando job de corte automático de jornada...");
        
        List<Despacho> pendientes = despachoRepository.buscarDespachosInconclusosDelDia(
            LocalDate.now(), List.of(EstadoDespacho.ASIGNADO, EstadoDespacho.EN_CAMINO));

        for (Despacho despacho : pendientes) {
            despacho.setEstado(EstadoDespacho.FALLIDO);
            despacho.setCodigoMotivo("NO_INTENTADO");
            despacho.setPendienteRetornoCentro(true);
            despachoRepository.save(despacho);

            historialService.registrarTransicion(
                despacho.getIdDespacho(), 
                EstadoDespacho.FALLIDO, 
                "SISTEMA_CORTE_AUTOMATICO", 
                "Cierre nocturno automático por corte de jornada"
            );
        }

        // Poner a todos los repartidores activos del día en FUERA_DE_TURNO
        flotaService.cerrarTodasLasJornadasDelDia(LocalDate.now());

        log.info("Corte automático culminado. Despachos regularizados: {}", pendientes.size());
    }
}
```

---

## 8. Requisitos no funcionales

- **Resiliencia:** Si el job encuentra un error en un despacho individual, debe aislar el fallo y continuar con los restantes (procesamiento tolerante a fallos).
- **Idempotencia:** Si el job se ejecuta dos veces en la misma noche, la segunda ejecución no encuentra despachos inconclusos y termina sin efectos secundarios.
- **Configurabilidad:** Expresión cron y zona horaria parametrizables mediante variables de entorno (`SPRING_SCHEDULER_CRON`).

---

## 9. Fuera de alcance

- Asignación de sanciones o penalidades laborales a los choferes.
- Reprogramación automática de los pedidos (corresponde a F-04 al día siguiente).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Scheduled Task Test | Spring Boot Test + H2 | Invocación del método transiciona los 4 despachos a `NO_INTENTADO`. |
| CA-02 | Counter Protection Test | JUnit 5 | Se comprueba que `numeroIntento` se mantiene exactamente igual. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El job cron se ejecute según la expresión configurada.
2. Ningún despacho quede en `ASIGNADO` o `EN_CAMINO` tras el corte.
3. El historial identifique inequívocamente al sistema como ejecutor.
