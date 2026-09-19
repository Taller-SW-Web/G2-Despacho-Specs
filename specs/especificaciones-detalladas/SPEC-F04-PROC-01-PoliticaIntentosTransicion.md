# Especificación SPEC-F04-PROC-01: Evaluación de Política de Intentos y Transición de Fallidos

**Tipo:** Proceso Interno / Reglas de Negocio Backend  
**Macro-funcionalidad:** F-04: Entregas Fallidas y Reprogramaciones  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho (Lógica de Dominio)  

---

## 1. Contexto

La gestión de entregas que no se concretaron en su primer intento requiere un balance riguroso entre el nivel de servicio al cliente y el costo logístico de transportar repetidamente un paquete. El sistema debe aplicar reglas estrictas de negocio que impidan reprogramaciones infinitas, garanticen la recepción física del bulto y procesen las excepciones de pedidos cancelados o no intentados.

---

## 2. Propósito

Implementar el servicio de dominio y lógica transaccional de backend que evalúa las precondiciones de recepción física, valida el número de intentos consumidos frente a la política máxima configurable (valor inicial: 2 intentos), verifica si el pedido fue cancelado comercialmente y ejecuta de forma atómica la transición a `PENDIENTE_ASIGNACION` o a `DEVUELTO_A_ORIGEN`.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Validación de precondición física: verificación estricta de `recibidoEnCentro == true`. Si el paquete no ha reingresado físicamente, se rechaza cualquier decisión con HTTP `409 Conflict`.
- Verificación de la política de intentos:
  - Lectura del parámetro configurable `despacho.politica.max-intentos` (por defecto 2).
  - Si `numeroIntento >= maximoIntentos`, se bloquea cualquier intento de reprogramación respondiendo HTTP `422 Unprocessable Entity`.
- Manejo de casos especiales:
  - Despachos con `codigoMotivo == "NO_INTENTADO"`: se autoriza la reprogramación sin importar intentos previos y no consumen intento.
  - Despachos con `pedidoAnulado == true`: se bloquea la reprogramación con HTTP `409 Conflict` y solo se admite el cierre a origen.
- Ejecución atómica de la transición de estado:
  - Reprogramación: cambio a `PENDIENTE_ASIGNACION`, actualización de `fechaEstimadaEntrega`, persistencia en cola de F-02.
  - Cierre: cambio a `DEVUELTO_A_ORIGEN`, bloqueo permanente de nuevos intentos y llamado síncrono al generador de eventos hacia Ventas (`SPEC-F04-PROC-02`).
- Registro en la tabla de auditoría común (`SPEC-TRANS-PROC-02`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Despacho en estado `FALLIDO`.
- Usuario autenticado con rol `GESTOR_DESPACHO`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `DespachoRepository` | Carga y persistencia del estado del despacho. |
| `SPEC-TRANS-PROC-01` | Validación de máquina de estados. |
| `SPEC-F04-PROC-02` | Encolamiento del evento de devolución hacia Ventas. |

### 4.3. Resultados
- Despacho transicionado de forma segura sin inconsistencias de negocio.
- Los intentos del cliente se respetan de acuerdo a las políticas de la empresa.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Validación de recepción física previa
Ninguna decisión DEBE tomarse sin la previa recepción física en el centro.

#### CA-01. Rechazo por paquete pendiente de retorno
- **DADO** un despacho en estado `FALLIDO` con `recibidoEnCentro = false`.
- **CUANDO** se invoca el endpoint de reprogramación o cierre a origen.
- **ENTONCES** el backend responde `409 Conflict` con el mensaje *"No se puede reprogramar ni cerrar el despacho: el paquete aún no ha sido recibido físicamente en el centro de despacho"*.

### RF-02. Aplicación de la política de intentos
El backend DEBE bloquear reprogramaciones cuando se alcance el límite máximo.

#### CA-02. Reprogramación permitida en primer intento
- **DADO** un despacho fallido recibido en almacén con `numeroIntento = 1` y máximo configurado de 2.
- **CUANDO** se solicita reprogramación con fecha válida.
- **ENTONCES** el backend transiciona a `PENDIENTE_ASIGNACION`, mantiene `numeroIntento = 1` y responde `200 OK`.

#### CA-03. Bloqueo al alcanzar el máximo de intentos
- **DADO** un despacho fallido recibido en almacén con `numeroIntento = 2`.
- **CUANDO** se intenta invocar la reprogramación.
- **ENTONCES** el backend responde `422 Unprocessable Entity` con el mensaje *"Límite máximo de intentos alcanzado para este despacho (2 de 2). Solo se permite el cierre como Devuelto a Origen"*.

### RF-03. Casos especiales de negocio
El sistema DEBE diferenciar paquetes no intentados y órdenes anuladas.

#### CA-04. Reprogramación de despacho no intentado
- **DADO** un despacho en `FALLIDO` con motivo `NO_INTENTADO` recibido en centro.
- **CUANDO** el gestor lo reprograma.
- **ENTONCES** el despacho vuelve a `PENDIENTE_ASIGNACION` y el contador de intentos permanece en cero (o en el valor previo que tenía).

#### CA-05. Despacho fallido con pedido comercial anulado
- **DADO** un despacho fallido sobre el cual Ventas notificó la cancelación del pedido.
- **CUANDO** se intenta reprogramar.
- **ENTONCES** el sistema rechaza la solicitud con `409 Conflict` informando *"El pedido ha sido anulado por el canal de ventas. Solo es posible su devolución a origen"*.

---

## 6. Frontend

*N/A - Lógica interna de backend.* Invocada por los modales `SPEC-F04-FORM-03` y `SPEC-F04-FORM-04`.

---

## 7. Backend

### 7.1. Servicio de Reglas de Dominio (Java 21 / Spring Boot)
```java
@Service
@RequiredArgsConstructor
public class ResolucionFallidosService {

    private final DespachoRepository despachoRepository;
    private final PublicadorEventosVentas publicadorEventos;
    private final HistorialService historialService;

    @Value("${despacho.politica.max-intentos:2}")
    private int maximoIntentosPermitidos;

    @Transactional
    public void reprogramarDespacho(UUID idDespacho, LocalDate nuevaFecha, String usuario) {
        Despacho despacho = obtenerDespachoFallido(idDespacho);
        
        validarRecepcionCentro(despacho);

        if (despacho.isPedidoAnulado()) {
            throw new ConflictoNegocioException("El pedido comercial fue anulado. Solo se admite devolución a origen.");
        }

        // Si fue intento real, verificar límite
        if (!"NO_INTENTADO".equals(despacho.getCodigoMotivo())) {
            if (despacho.getNumeroIntento() >= maximoIntentosPermitidos) {
                throw new LimiteIntentosExcedidoException("Límite máximo de intentos alcanzado (" + maximoIntentosPermitidos + ")");
            }
        }

        despacho.setEstado(EstadoDespacho.PENDIENTE_ASIGNACION);
        despacho.setFechaEstimadaEntrega(nuevaFecha);
        despacho.setPendienteRetornoCentro(false);
        despachoRepository.save(despacho);

        historialService.registrar(despacho, usuario, "Reprogramación autorizada para " + nuevaFecha);
    }

    @Transactional
    public void cerrarDevueltoOrigen(UUID idDespacho, String motivoCierre, String justificacion, String usuario) {
        Despacho despacho = obtenerDespachoFallido(idDespacho);
        validarRecepcionCentro(despacho);

        despacho.setEstado(EstadoDespacho.DEVUELTO_A_ORIGEN);
        despacho.setMotivoCierre(motivoCierre);
        despacho.setObservacionesCierre(justificacion);
        despachoRepository.save(despacho);

        // Encolar evento hacia Ventas
        publicadorEventos.emitirEventoDevolucion(despacho);

        historialService.registrar(despacho, usuario, "Cierre como Devuelto a Origen: " + motivoCierre);
    }

    private void validarRecepcionCentro(Despacho despacho) {
        if (!despacho.isRecibidoEnCentro()) {
            throw new ConflictoNegocioException("El paquete físico aún no ha sido recibido en el centro.");
        }
    }
}
```

---

## 8. Requisitos no funcionales

- **Trazabilidad:** Cada decisión registra usuario gestor, timestamp UTC y justificación.
- **Configurabilidad:** El número máximo de intentos se define centralmente mediante configuración de entorno sin recompilación.
- **Concurrencia:** Bloqueo optimista `@Version` para evitar reprogramaciones y cierres simultáneos.

---

## 9. Fuera de alcance

- Alteración del límite máximo de intentos de forma individual por despacho (la política es uniforme a nivel de centro).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Rule Test | JUnit 5 | Paquete con `recibidoEnCentro = false` arroja `ConflictoNegocioException`. |
| CA-02 | Reschedule Logic | JUnit 5 | Despacho pasa a `PENDIENTE_ASIGNACION` y preserva intentos. |
| CA-03 | Max Attempts Test | JUnit 5 | Segundo intento fallido bloquea reprogramación con código `422`. |
| CA-04 | Special Case Test | JUnit 5 | `NO_INTENTADO` se reprograma sin consumir intentos. |
| CA-05 | Cancelled Order Test | JUnit 5 | Pedido anulado bloquea reprogramación con código `409`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. La regla de previa recepción en centro se cumpla sin excepción en el backend.
2. Se respete estrictamente la política de máximo 2 intentos.
3. Se garantice la transición a `DEVUELTO_A_ORIGEN` con emisión de evento hacia Ventas.
