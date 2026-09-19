# Especificación SPEC-TRANS-PROC-03: Mecanismo Outbox Transaccional hacia Ventas y Canales

**Tipo:** Proceso Interno de Backend / Componente Transversal  
**Macro-funcionalidad:** Capacidades Transversales del Módulo (overview.md)  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Servicios Externos Integrados (Ventas y Postventa, Chatbot, Marketplace)  

---

## 1. Contexto

En una arquitectura de microservicios o módulos desacoplados, la actualización de la base de datos local y la notificación a sistemas externos no pueden ejecutarse de forma ingenua mediante llamadas HTTP síncronas directas. Si la base de datos confirma pero la red externa falla, o si la red confirma pero la base de datos hace rollback, el sistema entra en un estado de inconsistencia crítica (el problema del *Dual-Write*). Se requiere un mecanismo de entrega garantizada basado en el patrón Transaccional Outbox.

---

## 2. Propósito

Implementar el componente transversal de backend basado en el patrón *Transactional Outbox* que garantiza que cada evento del ciclo de vida del despacho (`DESPACHO_CREADO`, `DESPACHO_ASIGNADO`, `DESPACHO_EN_CAMINO`, `DESPACHO_ENTREGADO`, `DESPACHO_FALLIDO`, `DESPACHO_DEVUELTO_A_ORIGEN`, `DESPACHO_CANCELADO`) se persista atómicamente junto al cambio de estado local y se despache de forma asíncrona hacia Ventas y Postventa con tolerancia a fallos y reintentos exponenciales.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Definición de la tabla transaccional `eventos_outbox` en la misma base de datos PostgreSQL del módulo.
- Servicio genérico `OutboxPublisherService` invocado en cada transición de estado: inserta el evento en la misma transacción (`@Transactional`) de negocio.
- Worker asíncrono (*Background Poller*) que lee eventos con estado `PENDIENTE` en lotes (batch de 50 registros) y los despacha mediante cliente HTTP Webhook o publicador a broker de mensajería.
- Política de reintentos exponenciales:
  - Hasta 5 intentos de retransmisión con backoff multiplicativo (2s, 10s, 1m, 5m, 15m).
  - Si el destino agota los 5 intentos, el evento pasa a estado `ENVIO_FALLIDO` (Dead Letter) para intervención manual sin afectar la operación local.
- Garantía de entrega: *At-Least-Once* (al menos una vez), requiriendo que los consumidores externos apliquen idempotencia mediante el `idEvento`.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Base de datos PostgreSQL compartida entre la entidad de negocio y la tabla outbox.
- Worker programado activo en segundo plano.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| PostgreSQL (Supabase) | Garantizar atomicidad ACID entre la tabla `despachos` y `eventos_outbox`. |
| Módulo de Ventas y Postventa | Endpoint receptor de eventos de actualización de pedidos. |

### 4.3. Resultados
- Cero pérdida de eventos de integración ante caídas temporales de red o indisponibilidad de Ventas.
- Aislamiento total: la lentitud externa no degrada el tiempo de respuesta a los gestores o choferes.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Persistencia atómica en la tabla Outbox
El evento DEBE guardarse en la misma transacción que el cambio de estado del despacho.

#### CA-01. Atomicidad de inserción outbox
- **DADO** una transición de estado en cualquier punto del ciclo de vida (ej. `ENTREGADO`).
- **CUANDO** se comitea la transacción en el backend.
- **ENTONCES** en una sola operación ACID se actualiza la tabla `despachos` y se inserta una fila en `eventos_outbox` con `estadoEnvio = PENDIENTE`.
- **DADO** que la transacción hace rollback por cualquier error.
- **ENTONCES** ni el despacho cambia de estado ni se genera el evento outbox.

### RF-02. Despacho asíncrono y reintentos
El worker DEBE procesar los eventos y tolerar interrupciones de red.

#### CA-02. Despacho exitoso y actualización de estado
- **DADO** eventos con estado `PENDIENTE` en la tabla outbox.
- **CUANDO** el poller los envía exitosamente hacia el endpoint configurado y recibe `200 OK`.
- **ENTONCES** el estado del evento pasa a `ENVIADO` y se registra la marca temporal de confirmación.

#### CA-03. Aislamiento ante caída externa
- **DADO** que el módulo de Ventas está fuera de servicio por 30 minutos.
- **CUANDO** los repartidores entregan pedidos en calle.
- **ENTONCES** las entregas locales se confirman con total normalidad, los eventos se acumulan de forma segura en `eventos_outbox` y se van reintentando sin pérdida de datos.

---

## 6. Frontend

*N/A - Proceso puramente de infraestructura de backend.*

---

## 7. Backend

### 7.1. Modelo de la Tabla Outbox (Java 21 / Spring Boot)
```java
@Entity
@Table(name = "eventos_outbox", indexes = {
    @Index(name = "idx_outbox_estado_intentos", columnList = "estado_envio, proximo_intento")
})
@Getter
@Setter
@NoArgsConstructor
public class EventoOutbox {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id_evento", updatable = false, nullable = false)
    private UUID idEvento;

    @Column(name = "tipo_evento", nullable = false)
    private String tipoEvento; // DESPACHO_CREADO, DESPACHO_ENTREGADO, etc.

    @Column(name = "aggregate_id", nullable = false)
    private UUID aggregateId; // idDespacho

    @Column(name = "payload_json", nullable = false, columnDefinition = "TEXT")
    private String payloadJson;

    @Enumerated(EnumType.STRING)
    @Column(name = "estado_envio", nullable = false)
    private EstadoEnvioEvento estadoEnvio; // PENDIENTE, ENVIADO, ENVIO_FALLIDO

    @Column(name = "intentos", nullable = false)
    private int intentos;

    @Column(name = "proximo_intento")
    private Instant proximoIntento;

    @Column(name = "fecha_creacion", nullable = false, updatable = false)
    private Instant fechaCreacion;

    @Column(name = "fecha_confirmacion")
    private Instant fechaConfirmacion;
}
```

---

## 8. Requisitos no funcionales

- **Garantía de Entrega:** *At-Least-Once Delivery* con persistencia local garantizada.
- **Rendimiento:** Worker con polling eficiente mediante `fixedDelay` o disparador por eventos de aplicación de Spring (`ApplicationEventPublisher`).
- **Resiliencia:** Reintentos exponenciales con jitter para prevenir el efecto estampida (*Thundering Herd*) cuando el servicio de Ventas se restablece.

---

## 9. Fuera de alcance

- Procesamiento o consumo del evento en el lado de Ventas (responsabilidad del módulo receptor).
- Brokers de mensajería empresarial complejos (Kafka); la solución se basa en la tabla Outbox sobre PostgreSQL, compatible con Supabase.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Transactional Test | `@DataJpaTest` | Rollback de negocio también revierte la inserción del evento outbox. |
| CA-02 | Poller Success Test | WireMock | Poller envía batch, recibe 200 y actualiza eventos a `ENVIADO`. |
| CA-03 | Network Failure Test | WireMock | Simulación de timeout programa `proximoIntento` con cálculo exponencial. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Todas las transiciones del ciclo de vida generen su evento en `eventos_outbox` de forma transaccional.
2. El worker asíncrono procese y reintente los envíos sin bloquear las APIs de usuario.
3. Se garantice la resiliencia del módulo ante caídas de módulos externos.
