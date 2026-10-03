# ES-F03-06: Registro de entrega fallida

**Funcionalidad padre:** F-03 — Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** Max Rojas  
**Estado:** Borrador  
**Actor principal:** Repartidor

## 1. Objetivo

Permitir que el repartidor declare un intento real de entrega no exitoso, cambiando el despacho de `EN_CAMINO` a `FALLIDO` con un motivo del catálogo, fotografía obligatoria y comentario opcional.

El despacho queda disponible para que F-04 lo resuelva, y el paquete regresa con el repartidor al centro de despacho.

## 2. Actor y precondiciones

- Actor: repartidor en turno.
- Rol requerido: `REPARTIDOR`.
- El despacho está en `EN_CAMINO`, asignado al repartidor del token y pertenece a la jornada en curso.
- El catálogo canónico de motivos publicado por Gestión de Despachos está disponible.
- Existe conexión activa.

## 3. Flujo principal

1. El repartidor pulsa "Marcar como fallido".
2. El repartidor selecciona un motivo del catálogo, adjunta la fotografía y, opcionalmente, escribe un comentario.
3. El repartidor confirma la incidencia.
4. El sistema recibe la solicitud con su clave de idempotencia y valida token, turno, propiedad del despacho, motivo y archivo.
5. El sistema registra la evidencia y solicita la transición `EN_CAMINO` → `FALLIDO`.
6. El sistema persiste, en una misma transacción, el estado, el motivo, la referencia de la evidencia, el comentario, el incremento del contador de intentos en uno, la marca temporal del servidor, el ejecutor y el historial.
7. El sistema confirma la operación y recuerda al repartidor que debe devolver el paquete al centro de despacho.

## 4. Reglas y validaciones

- El motivo es obligatorio y se valida contra el catálogo canónico de motivos, única fuente para el campo y para F-04.
- El formulario solo ofrece los motivos seleccionables, todos con consumo de intento: `CLIENTE_AUSENTE`, `DIRECCION_NO_UBICADA`, `RECHAZO_DEL_PAQUETE`, `DATOS_DE_CONTACTO_ERRONEOS`, `ZONA_INACCESIBLE` y `PAQUETE_DANADO`.
- `NO_INTENTADO` es de uso exclusivo del sistema: no se muestra en el formulario ni se acepta desde esta acción.
- La fotografía es obligatoria; se aplican las mismas validaciones de evidencia que en ES-F03-05.
- Solo se permite desde `EN_CAMINO`; otro estado de origen se rechaza con `409 Conflict`.
- El contador de intentos aumenta en uno solo cuando la transición se acepta, y nunca por reintentos.
- El estado se presenta al repartidor como "No entregado, regresa al centro de despacho".
- El despacho `FALLIDO` sigue contando en la ocupación del repartidor hasta que el Gestor confirma su recepción en el centro (F-04).
- Sin conexión: la interfaz informa que el cambio no se registró, conserva el estado anterior y exige un reintento explícito.
- Idempotencia: una segunda solicitud con la misma clave devuelve el resultado original sin duplicar la transición, el incremento del contador ni el historial.

## 5. Entradas, salidas e integraciones

### Entradas

- JWT del repartidor.
- Código del despacho.
- Código de motivo (obligatorio).
- Fotografía de evidencia (obligatoria).
- Comentario (opcional).
- Clave de idempotencia.

### Salidas

- Despacho en `FALLIDO` con motivo, evidencia, comentario, contador incrementado y registro en el historial.
- O la respuesta de rechazo correspondiente, sin cambio de estado.

### Integraciones

- F-04 Entregas Fallidas: consume el despacho `FALLIDO` con motivo, contador y evidencia.
- Gestión de Despachos: catálogo canónico de motivos de fallo.
- Servicio de evidencia (por definir).
- Máquina de estados, historial común y publicación de eventos (overview, sección 6 y RT-03).
- Ver `integraciones/api-contract.md`.

## 6. Criterios de aceptación

### CA-01. Incidencia con motivo tipificado (F-03 CA-19)

- **DADO** un despacho en `EN_CAMINO` que no pudo entregarse.
- **CUANDO** el repartidor elige "Marcar como fallido", selecciona `CLIENTE_AUSENTE`, adjunta la fotografía del domicilio y confirma.
- **ENTONCES** el estado cambia a `FALLIDO`, se guardan motivo, evidencia y comentario, el contador de intentos aumenta en uno, la interfaz recuerda que debe devolver el paquete al centro y el despacho queda disponible para F-04.

### CA-02. Motivo no seleccionado (F-03 CA-20)

- **DADO** el formulario de incidencia sin motivo.
- **CUANDO** el repartidor intenta confirmar.
- **ENTONCES** el envío se bloquea y el campo de motivo se resalta como obligatorio.

### CA-03. Motivos disponibles en el formulario (F-03 CA-30)

- **DADO** que el repartidor abre el formulario de incidencia.
- **CUANDO** se cargan los motivos del catálogo.
- **ENTONCES** el campo muestra los motivos seleccionables con código y etiqueta, sin los de uso exclusivo del sistema.

### CA-04. Pérdida de conexión durante el envío (F-03 CA-21)

- **DADO** que el repartidor confirma la operación.
- **CUANDO** la petición no llega al backend por falta de señal.
- **ENTONCES** la interfaz informa que el cambio no se registró, conserva el estado anterior y exige un reintento explícito.

### CA-05. Reintento idempotente (F-03 CA-22)

- **DADO** un reintento de una operación cuyo resultado se desconoce.
- **CUANDO** el backend recibe una segunda solicitud con la misma clave de idempotencia.
- **ENTONCES** devuelve el resultado original sin duplicar la transición, el incremento del contador ni el registro en el historial.

### CA-06. Registro en el historial (F-03 CA-31)

- **DADO** una transición a `FALLIDO` aceptada.
- **CUANDO** se persiste.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual, marca temporal del servidor, estado anterior, estado nuevo, motivo y observaciones.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Confirmar la recepción del paquete en el centro, reprogramar o cerrar como `DEVUELTO_A_ORIGEN` (F-04).
- Límite de intentos y su tratamiento (F-04).
- Administración (alta, baja o edición) de motivos del catálogo.
- Notificación al cliente final.

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-06, RF-10, RF-11, Anexo A y Anexo B.
- `integraciones/api-contract.md`.
- Wireframe del formulario de incidencia.
