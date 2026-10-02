# ES-F04-05: Cerrar un despacho como devuelto a origen

**Funcionalidad padre:** F-04 — Entregas fallidas y reprogramaciones  
**Responsable:** Gerardo  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho cierre definitivamente un despacho fallido cuyo paquete regresó al centro y no tendrá otro intento. El cierre cambia el estado a `DEVUELTO_A_ORIGEN`, conserva la decisión y comunica el resultado a Ventas y Postventa para que el módulo dueño del pedido continúe el tratamiento comercial.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El despacho existe y su estado vigente es `FALLIDO`.
- La recepción física del paquete en el centro está confirmada.
- El Gestor proporciona un motivo de cierre.
- El cierre puede realizarse por decisión operativa, por límite de intentos o porque el pedido fue anulado.

## 3. Flujo principal

1. El Gestor abre el detalle de un despacho recibido y selecciona `Cerrar como devuelto a origen`.
2. El sistema advierte que el despacho no tendrá más intentos y solicita un motivo obligatorio.
3. El Gestor confirma la decisión.
4. El backend valida el rol, el estado vigente, la recepción y el motivo.
5. El sistema cambia el estado a `DEVUELTO_A_ORIGEN` y registra la trazabilidad de la decisión.
6. En la misma transacción se registra el evento `DESPACHO_DEVUELTO_A_ORIGEN` en la bandeja de salida.
7. El frontend informa el cierre; el paquete permanece en el centro a disposición del proceso que corresponda a Ventas y Postventa.

## 4. Reglas y validaciones

- Solo puede cerrarse un despacho cuyo estado vigente sea `FALLIDO` y cuya recepción esté confirmada.
- El motivo de cierre es obligatorio y no puede contener únicamente espacios.
- La transición válida es de `FALLIDO` a `DEVUELTO_A_ORIGEN`.
- Un pedido anulado no puede reprogramarse, pero sí debe poder cerrarse mediante esta operación.
- El máximo de intentos alcanzado impide reprogramar, pero no impide cerrar.
- El cambio de estado, el historial y el registro del evento se persisten en la misma transacción local.
- La indisponibilidad de Ventas y Postventa no revierte un cierre ya confirmado; el evento conserva su estado pendiente o fallido para reintento.
- Una repetición exacta es idempotente y no duplica la transición, la auditoría ni el evento.
- Si el despacho cambió a otro estado por una operación distinta, se responde `409 Conflict`; si ya fue cerrado por la misma operación, se devuelve el resultado vigente.
- El cierre no determina reembolso, cambio, reintegro de stock ni otra decisión comercial.

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador del despacho.
- Motivo obligatorio del cierre.
- Observación adicional cuando el contrato la permita.
- Identidad y roles obtenidos del JWT.

### Salidas

- Despacho en `DEVUELTO_A_ORIGEN`.
- Motivo, usuario y fecha de la decisión registrados.
- Registro de trazabilidad.
- Evento `DESPACHO_DEVUELTO_A_ORIGEN` preparado para envío a Ventas y Postventa.

### Integraciones

- Ventas y Postventa recibe el evento del cierre y decide el tratamiento posterior del pedido.
- El componente transversal de estados, historial y eventos garantiza la transición y la entrega asíncrona.
- La operación, el evento y sus reintentos se rigen por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Cierre exitoso

- **DADO** un despacho `FALLIDO` recibido en el centro.
- **CUANDO** el Gestor confirma el cierre e indica un motivo.
- **ENTONCES** el estado cambia a `DEVUELTO_A_ORIGEN`, se registra la trazabilidad y se genera un único evento para Ventas y Postventa.

### CA-02. Operación repetida

- **DADO** un despacho ya cerrado mediante la misma operación.
- **CUANDO** se repite exactamente la solicitud.
- **ENTONCES** el sistema devuelve el resultado vigente sin duplicar el cambio, la auditoría ni el evento.

### CA-03. Ventas y Postventa no disponible

- **DADO** un cierre confirmado localmente.
- **CUANDO** Ventas y Postventa no responde o devuelve un error.
- **ENTONCES** el estado `DEVUELTO_A_ORIGEN` se conserva y el evento queda registrado para los reintentos definidos por RT-03.

### CA-04. Recepción pendiente

- **DADO** un despacho `FALLIDO` cuyo paquete aún no fue recibido en el centro.
- **CUANDO** el Gestor intenta cerrarlo.
- **ENTONCES** el backend responde `409 Conflict` e indica que primero debe confirmarse la recepción.

### CA-05. Pedido anulado

- **DADO** un despacho fallido recibido cuyo pedido fue anulado.
- **CUANDO** el Gestor revisa las acciones permitidas y confirma el cierre.
- **ENTONCES** la reprogramación permanece bloqueada y el cierre como `DEVUELTO_A_ORIGEN` se procesa normalmente.

### CA-06. Motivo ausente

- **DADO** un despacho que cumple las condiciones de cierre.
- **CUANDO** el Gestor intenta confirmar sin proporcionar un motivo válido.
- **ENTONCES** el backend responde `400 Bad Request` y conserva el despacho en `FALLIDO`.

### CA-07. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta cerrar un despacho.
- **ENTONCES** el backend responde `403 Forbidden` y no produce cambios ni eventos.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Ejecutar reembolsos, cambios, notas de crédito o reclamos.
- Reingresar el paquete al inventario o reintegrar stock.
- Determinar el proceso físico posterior del paquete dentro del centro.
- Notificar directamente al cliente final.

### Referencias

- [cite: 1] `funcionalidades/F-04-GestionEntregasFallidas.md`, RF-04, RF-06, RF-07 y CA-10 a CA-12, CA-15 y CA-17.
- [cite: 2] `integraciones/api-contract.md`, secciones 7.3, 11 y 14.
- [cite: 3] `disenio/funcionalidades/f-04.md`, Pantalla 5: Cierre como Devuelto a Origen.
- [cite: 4] `overview.md`, RT-01 a RT-03.
