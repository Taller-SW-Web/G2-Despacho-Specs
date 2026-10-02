# ES-F04-06: Registrar la trazabilidad de las operaciones

**Funcionalidad padre:** F-04 — Entregas fallidas y reprogramaciones  
**Responsable:** Gerardo  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Garantizar que cada recepción, reprogramación y cierre aceptado de F-04 deje un registro auditable que permita reconstruir qué ocurrió, quién lo ejecutó y cuándo. La trazabilidad se genera automáticamente como parte de la operación de negocio y se consulta dentro del historial del despacho; no requiere una pantalla independiente.

## 2. Actor y precondiciones

- El Gestor está autenticado con el rol `GESTOR_DESPACHO` al iniciar la operación de negocio.
- La recepción, reprogramación o cierre superó todas sus validaciones y será aceptada.
- La identidad del ejecutor procede del JWT y la marca temporal procede del servidor.
- El despacho y la operación que origina el registro pueden relacionarse de manera inequívoca.

## 3. Flujo principal

1. El Gestor confirma una recepción, reprogramación o cierre.
2. El caso de uso correspondiente valida la solicitud.
3. Antes de confirmar la transacción, el sistema prepara el registro de trazabilidad con el despacho, la operación, el ejecutor, los estados y los datos relevantes.
4. La operación de negocio y su registro se persisten de manera consistente.
5. El registro queda disponible en el historial consultado desde el detalle de la incidencia.

## 4. Reglas y validaciones

- Toda recepción, reprogramación o cierre aceptado debe producir exactamente un registro de negocio.
- El registro incluye como mínimo identificador del despacho, funcionalidad origen, tipo de operación, usuario, fecha del servidor en UTC, estado anterior, estado nuevo y observaciones aplicables.
- En una recepción, que no cambia el estado del despacho, el estado anterior y el nuevo se registran como `FALLIDO`, junto con el estado del sello y la observación.
- En una reprogramación se registra la nueva fecha programada y la transición de `FALLIDO` a `PENDIENTE_ASIGNACION`.
- En un cierre se registra el motivo y la transición de `FALLIDO` a `DEVUELTO_A_ORIGEN`.
- La identidad del usuario nunca se toma de un campo libre enviado por el cliente.
- Una operación rechazada no se registra como una decisión de negocio aceptada.
- Una repetición idempotente no genera un segundo registro.
- La trazabilidad no puede editarse ni eliminarse mediante las operaciones de F-04.
- El orden mostrado en el historial se basa en la marca temporal persistida por el servidor.

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador del despacho.
- Tipo de operación aceptada.
- Estado anterior y estado nuevo.
- Identidad autenticada del ejecutor.
- Datos propios de la operación: sello y observación, nueva fecha o motivo de cierre.
- Marca temporal del servidor.

### Salidas

- Un registro de trazabilidad asociado al despacho y a la operación aceptada.
- Historial consultable desde el detalle de la incidencia.
- Evidencia suficiente para verificar la secuencia de recepciones y decisiones.

### Integraciones

- Las especificaciones ES-F04-03, ES-F04-04 y ES-F04-05 originan los registros.
- El componente transversal de historial definido por RT-02 persiste y expone la trazabilidad.
- La consulta del historial forma parte del detalle definido en ES-F04-02 y respeta `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Registro de recepción

- **DADO** una confirmación de recepción aceptada.
- **CUANDO** se confirma la operación.
- **ENTONCES** se registra el usuario, la fecha, el estado `FALLIDO` antes y después, el estado del sello y la observación aplicable.

### CA-02. Registro de reprogramación

- **DADO** una reprogramación aceptada.
- **CUANDO** se confirma la transición.
- **ENTONCES** se registra el usuario, la fecha, la transición a `PENDIENTE_ASIGNACION` y la nueva fecha programada.

### CA-03. Registro de cierre

- **DADO** un cierre aceptado.
- **CUANDO** se confirma la transición.
- **ENTONCES** se registra el usuario, la fecha, la transición a `DEVUELTO_A_ORIGEN` y el motivo del cierre.

### CA-04. Operación rechazada

- **DADO** una recepción o decisión que incumple una regla de negocio.
- **CUANDO** el backend rechaza la solicitud.
- **ENTONCES** no se crea un registro que la presente como operación aceptada.

### CA-05. Repetición idempotente

- **DADO** una operación aceptada que ya posee su registro de trazabilidad.
- **CUANDO** se repite exactamente la solicitud.
- **ENTONCES** no se crea un segundo registro de negocio.

### CA-06. Consulta posterior

- **DADO** un despacho con una o más operaciones de F-04 aceptadas.
- **CUANDO** el Gestor consulta el detalle de la incidencia.
- **ENTONCES** el historial permite identificar la secuencia, el ejecutor, la fecha y los datos relevantes de cada operación.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Crear una pantalla exclusiva para administrar auditorías.
- Editar o eliminar registros históricos.
- Registrar como exitosa una operación rechazada.
- Sustituir los logs técnicos, métricas o trazas de infraestructura.

### Referencias

- [cite: 1] `funcionalidades/F-04-GestionEntregasFallidas.md`, RF-05 y CA-13.
- [cite: 2] `integraciones/api-contract.md`, secciones 11 y 14.
- [cite: 3] `overview.md`, RT-02 sobre historial auditable.
- [cite: 4] `disenio/funcionalidades/f-04.md`, historial de la Pantalla 2.
