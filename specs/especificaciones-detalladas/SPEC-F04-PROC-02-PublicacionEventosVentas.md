# Especificación SPEC-F04-PROC-02: Publicación de Eventos de Devolución hacia Ventas y Postventa

**Tipo:** Proceso Interno de Backend / Integración Asíncrona  
**Macro-funcionalidad:** F-04: Entregas Fallidas y Reprogramaciones  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Servicio Integrador de Ventas / Worker Asíncrono  

---

## 1. Contexto

Cuando un despacho es cerrado definitivamente como devuelto a origen, el módulo de Despacho y Entrega a Domicilio culmina su responsabilidad física sobre la mercadería. En ese momento, el módulo de Ventas y Postventa (propietario del pedido y de la relación comercial con el cliente) debe ser notificado de inmediato para proceder con las acciones comerciales pertinentes: emisión de notas de crédito, reembolso dinerario o coordinación de recogida en tienda física.

---

## 2. Propósito

Implementar el componente de integración asíncrona basado en el patrón transaccional Outbox (*Transactional Outbox Pattern*) que emite el evento `DESPACHO_DEVUELTO_A_ORIGEN` hacia el módulo de Ventas y Postventa de forma desacoplada y garantizada, con política de reintentos exponenciales y registro de eventos fallidos.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Creación y estructuración del payload oficial del evento `DESPACHO_DEVUELTO_A_ORIGEN`.
- Persistencia síncrona del evento en la tabla local `eventos_outbox` dentro de la misma transacción en la que el despacho pasa a `DEVUELTO_A_ORIGEN`.
- Worker asíncrono en segundo plano (`@Async` o Scheduled Poller) que despacha las peticiones HTTP Webhook hacia el endpoint del módulo de Ventas.
- Política de reintentos con retroceso exponencial (*Exponential Backoff*):
  - Máximo 5 intentos de reenvío (intervalos: 2s, 10s, 1m, 5m, 15m).
- Tratamiento de indisponibilidad externa: si tras 5 intentos el servicio de Ventas no responde o arroja error HTTP 5xx, el evento se marca con estado `ENVIO_FALLIDO` para alerta y reenvío manual por el gestor.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- El despacho debe haber sido cerrado formalmente como `DEVUELTO_A_ORIGEN` (`SPEC-F04-PROC-01`).
- URL de integración o webhook del módulo de Ventas configurada en `application.yml`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| Módulo de Ventas y Postventa | Endpoint externo receptor del evento de devolución. |
| Tabla `eventos_outbox` | Almacenamiento local seguro para entrega garantizada (*At-Least-Once*). |
| `SPEC-TRANS-PROC-03` | Mecanismo outbox común del módulo. |

### 4.3. Resultados
- Notificación comercial entregada a Ventas sin bloquear ni degradar la experiencia de usuario del gestor.
- Registro auditable del ciclo de vida del evento (creado, enviado, confirmado o fallido).

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Generación y estructura del evento
El evento DEBE contener toda la información requerida por el área comercial.

#### CA-01. Estructura canónica del evento de devolución
- **DADO** un despacho cerrado como devuelto a origen con motivo `MAXIMO_INTENTOS_ALCANZADO`.
- **CUANDO** se confirma la transacción.
- **ENTONCES** se inserta un registro en la tabla outbox con: `idEvento` (UUID), `tipoEvento = DESPACHO_DEVUELTO_A_ORIGEN`, `idPedido`, `idDespacho`, `codigoRastreo`, `motivoCierre`, `justificacion`, `marcaTemporalUtc` y `estadoEnvio = PENDIENTE`.

### RF-02. Despacho asíncrono y reintentos
El worker DEBE procesar los eventos en segundo plano y reintentar ante fallos de red.

#### CA-02. Entrega exitosa a Ventas
- **DADO** un evento pendiente en la tabla outbox y el módulo de Ventas disponible.
- **CUANDO** el worker ejecuta el envío.
- **ENTONCES** Ventas responde `200 OK`, el evento se marca como `ENVIADO` con su marca temporal de confirmación y se actualiza el contador de intentos a 1.

#### CA-03. Indisponibilidad de Ventas y política de reintentos
- **DADO** que el endpoint de Ventas responde `503 Service Unavailable`.
- **CUANDO** el worker intenta el primer envío.
- **ENTONCES** el estado local del despacho no se altera, el evento se mantiene en `PENDIENTE_REINTENTO`, se programa el siguiente reintento exponencial y no se pierde información.

#### CA-04. Agotamiento de reintentos (Envío Fallido)
- **DADO** que el módulo de Ventas permanece caído tras los 5 intentos programados.
- **CUANDO** falla el quinto intento.
- **ENTONCES** el evento pasa a estado `ENVIO_FALLIDO`, se emite un log de alerta crítica y queda disponible para reenvío manual desde el panel del gestor.

---

## 6. Frontend

*N/A - Proceso de integración en backend.* En el panel del gestor se muestra un badge informativo sobre el estado del envío a Ventas.

---

## 7. Backend

### 7.1. Estructura del Payload JSON del Evento
```json
{
  "idEvento": "EVT-8921-UUID",
  "tipoEvento": "DESPACHO_DEVUELTO_A_ORIGEN",
  "fechaHoraUtc": "2026-09-19T18:45:00Z",
  "datos": {
    "idDespacho": "DSP-100234",
    "idPedido": "PED-2026-00891",
    "codigoRastreo": "TRK-78901",
    "motivoCierre": "MAXIMO_INTENTOS_ALCANZADO",
    "justificacion": "Se realizaron dos visitas con cliente ausente",
    "ubicacionPaquete": "CENTRO_DESPACHO_CENTRAL"
  }
}
```

### 7.2. Lógica del Dispatcher Outbox (Java 21 / Spring Boot)
```java
@Service
@RequiredArgsConstructor
@Slf4j
public class PublicadorEventosVentas {

    private final OutboxRepository outboxRepository;
    private final RestClient ventasRestClient;

    @Transactional
    public void emitirEventoDevolucion(Despacho despacho) {
        EventoOutbox evento = EventoOutbox.builder()
            .idDespacho(despacho.getIdDespacho())
            .tipoEvento("DESPACHO_DEVUELTO_A_ORIGEN")
            .payloadJson(serializarEvento(despacho))
            .estadoEnvio(EstadoEnvioEvento.PENDIENTE)
            .intentos(0)
            .build();
        outboxRepository.save(evento);
    }

    @Scheduled(fixedDelay = 5000)
    public void procesarEventosPendientes() {
        List<EventoOutbox> pendientes = outboxRepository.buscarEventosPorProcesar();
        for (EventoOutbox evento : pendientes) {
            try {
                ventasRestClient.post()
                    .uri("/api/v1/eventos-despacho")
                    .body(evento.getPayloadJson())
                    .retrieve()
                    .toBodilessEntity();
                
                evento.setEstadoEnvio(EstadoEnvioEvento.ENVIADO);
                evento.setFechaConfirmacion(Instant.now());
            } catch (Exception ex) {
                manejarFalloEnvio(evento, ex);
            }
            outboxRepository.save(evento);
        }
    }
}
```

---

## 8. Requisitos no funcionales

- **Desacoplamiento:** El cierre del despacho local jamás se bloquea por la lentitud o caída del servicio de Ventas.
- **Garantía de Entrega:** Entrega al menos una vez (*At-Least-Once Delivery*).
- **Seguridad:** Petición HTTP saliente autenticada mediante clave de servicio o token mTLS.

---

## 9. Fuera de alcance

- Lógica interna de Ventas para devolución de dinero o emisión de comprobantes fiscales.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Outbox Save Test | `@DataJpaTest` | Evento insertado en la misma transacción que el despacho. |
| CA-02 | Webhook Success | MockWebServer | Respuesta 200 de Ventas transiciona el evento a `ENVIADO`. |
| CA-03 | Retry Exponential | WireMock | Simulación de error 503 programa reintento con backoff. |
| CA-04 | Exhausted Retries | JUnit 5 | Quinto fallo transiciona el evento a `ENVIO_FALLIDO`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Ningún despacho cerrado como devuelto a origen omita la creación de su evento outbox.
2. El worker procese y reintente los envíos automáticamente.
3. Se garantice la resiliencia del módulo ante caídas prolongadas de Ventas.
