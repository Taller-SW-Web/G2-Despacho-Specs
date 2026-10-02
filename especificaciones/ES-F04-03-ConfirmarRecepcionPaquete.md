# ES-F04-03: Confirmar la recepción del paquete

**Funcionalidad padre:** F-04 — Entregas fallidas y reprogramaciones  
**Responsable:** Gerardo  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Registrar que el paquete asociado a un despacho fallido regresó físicamente al centro de despacho. La confirmación deja constancia del estado del sello, libera la ocupación atribuida al repartidor y habilita al Gestor para reprogramar o cerrar el despacho, sin cambiar todavía su estado `FALLIDO`.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- El despacho existe y su estado vigente es `FALLIDO`.
- El paquete aparece como `Pendiente de retorno` y se encuentra físicamente en el centro de despacho.
- La identidad del usuario que confirma se obtiene de la sesión autenticada.
- Existe la información necesaria para liberar de forma idempotente la reserva u ocupación asociada en F-05.

## 3. Flujo principal

1. El Gestor selecciona `Confirmar recepción` desde el listado o el detalle.
2. El sistema muestra el identificador del despacho y solicita indicar si el sello está intacto, con una observación opcional.
3. El Gestor verifica físicamente el paquete y confirma la operación.
4. El backend valida el rol, el estado vigente y que la recepción no haya sido procesada previamente.
5. El sistema registra la fecha del servidor, el usuario, el estado del sello y la observación, manteniendo el despacho en `FALLIDO`.
6. La operación registra su trazabilidad y solicita la liberación idempotente de la ocupación en F-05.
7. El frontend informa el resultado y presenta el paquete como `Recibido en centro`.

## 4. Reglas y validaciones

- La recepción solo puede confirmarse para un despacho cuyo estado vigente sea `FALLIDO`.
- `selloIntacto` es obligatorio y admite los valores verdadero o falso.
- La observación es opcional, pero debe conservarse cuando el Gestor la proporciona.
- La marca temporal y el usuario que confirma proceden del servidor y del JWT; no pueden ser sustituidos por valores libres del cliente.
- La recepción no cambia el estado del despacho: el estado anterior y el vigente continúan siendo `FALLIDO`.
- La recepción habilita las decisiones posteriores, pero no las ejecuta automáticamente.
- Una repetición exacta es idempotente: devuelve el resultado vigente sin duplicar recepción, auditoría ni liberación de ocupación.
- Si otra operación modificó el despacho y ya no está `FALLIDO`, se responde `409 Conflict` y no se registra la recepción.
- La liberación de ocupación debe utilizar el mecanismo interno e idempotente definido con F-05.
- Un usuario sin el rol requerido obtiene `403 Forbidden`.

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador del despacho.
- Indicador obligatorio `selloIntacto`.
- Observación opcional sobre la condición del paquete.
- Identidad y roles obtenidos del JWT.

### Salidas

- Confirmación `Recibido en centro`.
- Fecha y usuario de recepción.
- Estado registrado del sello y observación.
- Despacho todavía en `FALLIDO`, ahora habilitado para una decisión.
- Liberación de la ocupación correspondiente en F-05.

### Integraciones

- F-05 recibe la liberación idempotente de la reserva por el motivo `RECEPCION_EN_CENTRO`.
- El componente transversal de historial registra la operación junto con su ejecutor y marca temporal.
- La solicitud y la integración interna se rigen por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Confirmación exitosa

- **DADO** un despacho `FALLIDO` marcado como `Pendiente de retorno` cuyo paquete llegó al centro.
- **CUANDO** el Gestor indica el estado del sello y confirma la recepción.
- **ENTONCES** el sistema lo marca como `Recibido en centro`, conserva el estado `FALLIDO`, registra la trazabilidad y deja de contar el paquete en la ocupación del repartidor.

### CA-02. Recepción con sello no intacto

- **DADO** un paquete retornado cuyo sello presenta una alteración.
- **CUANDO** el Gestor selecciona que el sello no está intacto y agrega una observación.
- **ENTONCES** el sistema registra ambos datos sin impedir la recepción ni decidir automáticamente el tratamiento comercial del paquete.

### CA-03. Operación repetida

- **DADO** un despacho cuya recepción ya fue confirmada.
- **CUANDO** se repite exactamente la confirmación.
- **ENTONCES** el sistema devuelve el resultado vigente sin duplicar la recepción, la auditoría ni la liberación de ocupación.

### CA-04. Estado incompatible

- **DADO** un despacho cuyo estado vigente ya no es `FALLIDO`.
- **CUANDO** se intenta confirmar su recepción usando información desactualizada.
- **ENTONCES** el backend responde `409 Conflict`, conserva el estado vigente y no registra una recepción nueva.

### CA-05. Datos incompletos

- **DADO** un despacho pendiente de retorno.
- **CUANDO** el Gestor intenta confirmar sin indicar el estado del sello.
- **ENTONCES** el backend responde `400 Bad Request` y la recepción permanece pendiente.

### CA-06. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta confirmar una recepción.
- **ENTONCES** el backend responde `403 Forbidden` y no produce cambios.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Reingresar el paquete al inventario o modificar el stock.
- Resolver daños, reclamos, reembolsos o cambios comerciales.
- Reprogramar o cerrar automáticamente el despacho.
- Registrar el fallo original o cerrar la jornada del repartidor.

### Referencias

- [cite: 1] `funcionalidades/F-04-GestionEntregasFallidas.md`, RF-07 y CA-16 a CA-18.
- [cite: 2] `integraciones/api-contract.md`, secciones 11, 13.2 y 14.
- [cite: 3] `disenio/funcionalidades/f-04.md`, Pantalla 3: Confirmación de Recepción en Centro.
- [cite: 4] `overview.md`, RT-02 e integración entre F-04 y F-05.
