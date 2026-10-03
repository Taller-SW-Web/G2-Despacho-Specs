# ES-F03-05: Registro de entrega exitosa con evidencia

**Funcionalidad padre:** F-03 — Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** Max Rojas  
**Estado:** Borrador  
**Actor principal:** Repartidor

## 1. Objetivo

Permitir que el repartidor cierre un despacho como `ENTREGADO` solo cuando adjunta una fotografía como evidencia de recepción, con el nombre de quien recibe como dato opcional.

Esto deja prueba verificable de cada entrega y libera la ocupación del repartidor.

## 2. Actor y precondiciones

- Actor: repartidor en turno.
- Rol requerido: `REPARTIDOR`.
- El despacho está en `EN_CAMINO`, asignado al repartidor del token y pertenece a la jornada en curso.
- El repartidor dispone de cámara en el celular y conexión activa.

## 3. Flujo principal

1. El repartidor abre el formulario de entrega, captura y previsualiza la fotografía y, opcionalmente, registra el nombre de quien recibe.
2. El repartidor pulsa "Confirmar entrega".
3. El sistema recibe la solicitud con su clave de idempotencia y valida token, turno, propiedad del despacho y archivo.
4. El sistema registra la evidencia mediante el mecanismo aprobado y obtiene su referencia.
5. El sistema solicita la transición `EN_CAMINO` → `ENTREGADO` y persiste, en una misma transacción, el estado, la referencia de la evidencia, el nombre del receptor, la marca temporal del servidor, el ejecutor y el historial.
6. El sistema devuelve el resultado y muestra confirmación de éxito.

## 4. Reglas y validaciones

- La fotografía es obligatoria; sin ella el botón "Confirmar entrega" permanece deshabilitado y no se envía la petición. El backend valida igualmente su presencia.
- Solo se permite desde `EN_CAMINO`; otro estado de origen se rechaza con `409 Conflict`.
- Si el almacenamiento de evidencia falla o excede el tiempo de espera, el estado no cambia, se informa el error y la imagen se conserva en el formulario para reintentar.
- Un archivo que incumple el formato o tamaño definidos responde `400 Bad Request`, no se guarda y el estado no cambia.
- La compresión, el tratamiento de metadatos, los límites de archivo y el mecanismo de almacenamiento están pendientes de decisión del equipo (`pendiente.md`, sección F-03).
- No modifica el contador de intentos.
- Un despacho `ENTREGADO` deja de contar en la ocupación del repartidor (recalculada por F-05).
- Idempotencia y comportamiento ante pérdida de conexión: iguales a ES-F03-04.

## 5. Entradas, salidas e integraciones

### Entradas

- JWT del repartidor.
- Código del despacho.
- Fotografía de evidencia (obligatoria).
- Nombre de quien recibe (opcional).
- Clave de idempotencia.

### Salidas

- Despacho en `ENTREGADO` con referencia de evidencia persistida, nombre del receptor si se informó y registro en el historial.
- O la respuesta de rechazo correspondiente, sin cambio de estado.

### Integraciones

- Servicio de evidencia (por definir): almacenamiento de la fotografía.
- Máquina de estados, historial común y publicación de eventos (overview, sección 6 y RT-03).
- F-05: recálculo de ocupación a partir del estado.
- Ver `integraciones/api-contract.md`.

## 6. Criterios de aceptación

### CA-01. Confirmación con evidencia válida (F-03 CA-15)

- **DADO** un despacho en `EN_CAMINO`.
- **CUANDO** el repartidor captura la fotografía, opcionalmente registra el nombre de quien recibe y pulsa "Confirmar entrega".
- **ENTONCES** el sistema registra la evidencia mediante el mecanismo aprobado, persiste su referencia y cambia el estado a `ENTREGADO`.

### CA-02. Confirmación sin evidencia (F-03 CA-16)

- **DADO** el formulario de entrega sin fotografía.
- **CUANDO** el repartidor intenta confirmar.
- **ENTONCES** el botón permanece deshabilitado, se muestra el mensaje de evidencia obligatoria y no se envía la petición.

### CA-03. Fallo en la carga de la imagen (F-03 CA-17)

- **DADO** una confirmación con fotografía adjunta.
- **CUANDO** el almacenamiento responde con error o excede el tiempo de espera.
- **ENTONCES** el estado no cambia, se informa el error y la imagen se conserva en el formulario para reintentar.

### CA-04. Archivo inválido (F-03 CA-18)

- **DADO** un archivo que incumple el formato o el tamaño que el equipo defina para la evidencia.
- **CUANDO** llega al backend.
- **ENTONCES** se responde `400 Bad Request`, no se guarda el archivo y el estado no cambia.

### CA-05. Registro en el historial (F-03 CA-31)

- **DADO** una transición a `ENTREGADO` aceptada.
- **CUANDO** se persiste.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual, marca temporal del servidor, estado anterior, estado nuevo y observaciones.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Firma digital y documento de identidad del receptor.
- Decisión técnica sobre compresión, metadatos y almacenamiento de la fotografía.
- Notificación al cliente final.

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-05, RF-11 y sección 8 (Evidencia fotográfica).
- `funcionalidades/pendiente.md`, sección F-03.
- `integraciones/api-contract.md`.
- Wireframe del formulario de entrega.
