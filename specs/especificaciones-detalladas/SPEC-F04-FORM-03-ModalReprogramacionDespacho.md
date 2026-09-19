# Especificación SPEC-F04-FORM-03: Modal de Reprogramación de Despacho

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-04: Entregas Fallidas y Reprogramaciones  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho  

---

## 1. Contexto

Cuando un intento de entrega falla pero el cliente solicita una nueva visita o cuando un paquete no fue intentado por término de jornada, el Gestor de Despacho puede conceder una segunda oportunidad de reparto fijando una fecha futura. El despacho debe reincorporarse de forma limpia y ordenada a la cola de programación de F-02.

---

## 2. Propósito

Proveer un diálogo modal interactivo para fijar una nueva fecha futura de entrega sobre un despacho fallido previamente recibido en el centro, validando que no se haya superado la política de intentos máximos (máximo 2) ni exista anulación comercial del pedido, transicionando el despacho de vuelta a `PENDIENTE_ASIGNACION`.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Apertura del modal desde la fila del despacho en el panel de fallidos (`SPEC-F04-FORM-01`).
- Validaciones previas de disponibilidad:
  - El paquete debe estar marcado como `recibidoEnCentro: true`.
  - El contador de intentos debe ser menor al máximo configurado (`numeroIntento < maximoIntentos`). Si alcanzó el límite, el modal se bloquea y solo permite cerrar a origen (`SPEC-F04-FORM-04`).
  - El pedido no debe estar anulado por Ventas.
- Formulario de reprogramación:
  - Selector de nueva fecha de entrega (restringido a fechas estrictamente posteriores a hoy).
  - Selector de turno preferente (Mañana / Tarde / Indistinto).
  - Campo de observaciones o instrucciones para el nuevo intento.
- Envío mediante `POST /api/v1/despachos/{idDespacho}/reprogramar`.
- Transición de estado: `FALLIDO` → `PENDIENTE_ASIGNACION`.
- Conservación del contador de intentos (no se resetea a cero).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Despacho en estado `FALLIDO` con recepción física confirmada en el centro.
- Intentos consumidos inferiores al límite configurado (típicamente 1 de 2).
- Nueva fecha seleccionada posterior a la fecha actual.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `POST /api/v1/despachos/{idDespacho}/reprogramar` | Endpoint backend que valida las reglas y transiciona el despacho (`SPEC-F04-PROC-01`). |
| F-02 (Programación y Asignación) | Cola de pendientes donde reaparecerá el despacho reprogramado. |

### 4.3. Resultados
- Despacho en estado `PENDIENTE_ASIGNACION` con nueva fecha programada.
- El despacho desaparece del panel de fallidos y se incorpora a la cola de F-02 para el día fijado.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Validación de fecha y límites de política
El modal DEBE impedir fechas pasadas o reprogramaciones sobre límites vencidos.

#### CA-01. Reprogramación válida con fecha futura
- **DADO** un despacho fallido con 1 intento consumido de un máximo de 2, recibido en almacén.
- **CUANDO** el gestor selecciona la fecha de mañana y confirma.
- **ENTONCES** el backend responde `200 OK`, el despacho transiciona a `PENDIENTE_ASIGNACION`, se guarda la nueva fecha programada, el contador se mantiene en 1 y se muestra notificación de éxito.

#### CA-02. Bloqueo por selección de fecha actual o pasada
- **DADO** un intento de seleccionar la fecha de hoy o una fecha anterior.
- **CUANDO** el usuario intenta confirmar.
- **ENTONCES** el datepicker restringe la selección (fechas deshabilitadas) y el formulario bloquea el botón con el mensaje *"La nueva fecha debe ser posterior al día de hoy"*.

#### CA-03. Bloqueo por límite de intentos alcanzado
- **DADO** un despacho con contador igual a 2 (de máximo 2).
- **CUANDO** se intenta acceder a reprogramar.
- **ENTONCES** el modal muestra una alerta roja: *"Límite máximo de intentos alcanzado (2/2). Este paquete debe cerrarse como Devuelto a Origen"*, y el botón de reprogramar permanece deshabilitado.

---

## 6. Frontend

### 6.1. Componentes
- **`RescheduleModal`**: Diálogo modal con diseño de calendario.
- **`DeliveryDatePicker`**: Selector de fecha con atributo `min={fechaManana}`.
- **`ShiftPreferenceSelect`**: Selector de turno (Mañana / Tarde).
- **`AttemptsIndicatorBadge`**: Chip visual que muestra *"Intento actual: X de Y"*.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `POST /api/v1/despachos/{idDespacho}/reprogramar`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Content-Type: application/json`
- **Cuerpo:**
```json
{
  "nuevaFechaEntrega": "2026-09-21",
  "turnoPreferente": "MAÑANA",
  "observaciones": "Cliente solicitó entrega en horario matutino"
}
```
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idDespacho": "DSP-100234",
  "estado": "PENDIENTE_ASIGNACION",
  "nuevaFechaEntrega": "2026-09-21",
  "numeroIntento": 1,
  "mensaje": "Despacho reprogramado e incorporado a la cola de asignación"
}
```

---

## 8. Requisitos no funcionales

- **Integridad:** La transición y la conservación de métricas se ejecutan atómicamente con auditoría.
- **Seguridad:** Rol `GESTOR_DESPACHO` verificado mediante token JWT.

---

## 9. Fuera de alcance

- Asignación inmediata de repartidor en este paso (el despacho vuelve a la cola general de F-02).
- Modificación de la dirección original de entrega (si la dirección cambia, corresponde a un proceso comercial de Ventas).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI Reschedule Test | RTL / Vitest | Confirmación con fecha futura emite POST y recibe `200`. |
| CA-02 | Date Validation | Vitest | Fechas pasadas arrojan error de validación en cliente. |
| CA-03 | Max Attempts Block | Mock Service Worker | Despacho con `2/2` deshabilita reprogramación. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El modal valide que el paquete esté recibido y cuente con intentos disponibles.
2. El despacho transicione a `PENDIENTE_ASIGNACION` conservando su historial previo.
3. Se garantice su visibilidad en la cola de asignación de F-02.
