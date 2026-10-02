# ES-F04-04: Reprogramar un despacho fallido

**Funcionalidad padre:** F-04 — Entregas fallidas y reprogramaciones  
**Responsable:** Gerardo  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho programe un nuevo intento de entrega para un paquete fallido que ya regresó al centro y todavía cumple la política de intentos. Una reprogramación válida fija una fecha futura, devuelve el despacho a la cola de asignación de F-02 y conserva toda su trazabilidad.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El despacho existe y su estado vigente es `FALLIDO`.
- La recepción física del paquete en el centro está confirmada.
- El pedido no está marcado como anulado.
- El contador de intentos es menor que el máximo configurable, cuyo valor inicial es dos.
- La nueva fecha programada es posterior a la fecha actual del servidor.

## 3. Flujo principal

1. El Gestor abre el detalle de un despacho recibido y selecciona `Reprogramar`.
2. El sistema muestra el intento actual, el máximo permitido y un selector de fecha.
3. El Gestor elige una fecha futura, agrega una observación opcional y confirma.
4. El backend vuelve a validar el rol, el estado, la recepción, la anulación, la fecha y la política de intentos.
5. El sistema cambia el estado a `PENDIENTE_ASIGNACION`, guarda la nueva fecha programada y conserva el contador de intentos.
6. En la misma operación se registra la trazabilidad y el evento `DESPACHO_REPROGRAMADO` para Ventas y Postventa.
7. El despacho vuelve a estar disponible para la cola de F-02 en la fecha programada y deja de aparecer en el listado de fallidos.

## 4. Reglas y validaciones

- Solo puede reprogramarse un despacho cuyo estado vigente sea `FALLIDO` y cuya recepción esté confirmada.
- La nueva fecha debe ser estrictamente posterior a la fecha actual del servidor.
- El contador de intentos debe ser menor que el máximo configurado.
- Reprogramar no incrementa el contador; el contador solo cambia cuando F-03 registra un intento real.
- Un fallo con motivo `NO_INTENTADO` no consume intentos y puede reprogramarse conservando su contador.
- Un pedido anulado no puede reprogramarse; solo puede cerrarse como `DEVUELTO_A_ORIGEN`.
- La zona registrada originalmente se conserva y no vuelve a validarse contra la cobertura activa, porque no se trata de una solicitud nueva.
- La transición válida es de `FALLIDO` a `PENDIENTE_ASIGNACION`.
- El cambio de estado, la nueva fecha, el historial y el evento pendiente se persisten de manera consistente.
- Una repetición exacta no duplica la transición, la auditoría ni el evento.
- Una modificación concurrente responde `409 Conflict` y conserva el estado vigente.
- El backend aplica todas las reglas aunque el frontend haya deshabilitado previamente una acción inválida.

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador del despacho.
- Nueva fecha programada.
- Observación opcional.
- Identidad y roles obtenidos del JWT.

### Salidas

- Despacho en `PENDIENTE_ASIGNACION`.
- Nueva fecha programada persistida.
- Contador de intentos sin incremento.
- Registro de trazabilidad.
- Evento `DESPACHO_REPROGRAMADO` registrado para envío.
- Disponibilidad del despacho en la cola de F-02.

### Integraciones

- F-02 consume el despacho reprogramado en su cola de programación y asignación.
- F-03 es la fuente del motivo y del contador de intentos; `NO_INTENTADO` no incrementa dicho contador.
- Ventas y Postventa recibe el resultado mediante el evento asíncrono definido por RT-03.
- La operación y el evento se rigen por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Reprogramación válida

- **DADO** un despacho `FALLIDO`, recibido en el centro, con un intento y un máximo configurado de dos.
- **CUANDO** el Gestor selecciona una fecha futura y confirma.
- **ENTONCES** el estado cambia a `PENDIENTE_ASIGNACION`, se guarda la fecha, el contador permanece en uno y se registran la trazabilidad y el evento correspondiente.

### CA-02. Fecha inválida

- **DADO** un despacho que cumple las demás condiciones de reprogramación.
- **CUANDO** el Gestor selecciona la fecha actual o una fecha pasada.
- **ENTONCES** el backend responde `400 Bad Request`, explica la validación y conserva el despacho en `FALLIDO`.

### CA-03. Límite de intentos alcanzado

- **DADO** un despacho cuyo contador es igual al máximo configurado.
- **CUANDO** el Gestor consulta el detalle o intenta reprogramarlo.
- **ENTONCES** el frontend deshabilita la acción, el backend responde `422 Unprocessable Entity` ante el intento y solo queda disponible el cierre.

### CA-04. Estado desactualizado

- **DADO** un despacho que dejó de estar en `FALLIDO`.
- **CUANDO** se intenta reprogramar con información desactualizada.
- **ENTONCES** el backend responde `409 Conflict` y conserva el estado vigente.

### CA-05. Recepción pendiente

- **DADO** un despacho `FALLIDO` cuyo paquete aún no fue recibido en el centro.
- **CUANDO** el Gestor intenta reprogramarlo.
- **ENTONCES** el backend responde `409 Conflict` e indica que primero debe confirmarse la recepción.

### CA-06. Despacho no intentado

- **DADO** un despacho recibido cuyo motivo es `NO_INTENTADO`.
- **CUANDO** el Gestor lo reprograma con una fecha futura.
- **ENTONCES** el despacho vuelve a `PENDIENTE_ASIGNACION` sin incrementar el contador de intentos.

### CA-07. Pedido anulado

- **DADO** un despacho fallido sobre el cual F-02 registró la anulación del pedido.
- **CUANDO** el Gestor intenta reprogramarlo.
- **ENTONCES** el frontend mantiene la acción deshabilitada y el backend responde `409 Conflict`, dejando disponible únicamente el cierre.

### CA-08. Operación repetida

- **DADO** una reprogramación ya aceptada.
- **CUANDO** se repite exactamente la operación.
- **ENTONCES** el sistema devuelve el resultado vigente sin duplicar transición, historial ni evento.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Asignar inmediatamente un repartidor o definir la secuencia de su ruta.
- Incrementar el contador antes de que ocurra un nuevo intento real.
- Modificar la zona, dirección o datos comerciales del pedido.
- Notificar directamente al cliente final.

### Referencias

- [cite: 1] `funcionalidades/F-04-GestionEntregasFallidas.md`, RF-03, RF-06, RF-07 y CA-06 a CA-09, CA-14, CA-15 y CA-17.
- [cite: 2] `integraciones/api-contract.md`, secciones 7.3, 11 y 14.
- [cite: 3] `disenio/funcionalidades/f-04.md`, Pantalla 4: Reprogramación.
- [cite: 4] `overview.md`, RT-01 a RT-03 e integración entre F-04 y F-02.
