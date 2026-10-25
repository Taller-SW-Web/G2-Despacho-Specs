# ES-F03-06: Registro de entrega fallida

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md)

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor

**UI:** Aplica; formulario de incidencia de la web responsive del repartidor.

## 1. Contexto y objetivo

Permitir que el repartidor declare un intento real de entrega no exitoso, cambiando el despacho de `EN_CAMINO` a `FALLIDO` con un motivo del catálogo, fotografía obligatoria y comentario opcional. El despacho queda disponible para F-04 y el paquete regresa con el repartidor al centro de despacho. Concreta RF-06, RF-10, RF-11 y los Anexos A y B de F-03.

## 2. Alcance

- Incluye: selección de motivo seleccionable en campo, evidencia fotográfica, comentario opcional, transición `EN_CAMINO` → `FALLIDO` e incremento del contador de intentos.
- Fuera de alcance: confirmación de recepción en el centro, reprogramación y cierre como `DEVUELTO_A_ORIGEN` (F-04); límite de intentos y su tratamiento (F-04); administración del catálogo de motivos; notificación al cliente final.

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor en turno, con perfil local activo y vinculado resuelto desde el `sub` del JWT; no se exige rol global `REPARTIDOR`.
- Precondiciones: el despacho está en `EN_CAMINO`, asignado al repartidor del token y en la jornada en curso; el catálogo canónico de motivos de Gestión de Despachos está disponible; existe conexión activa.
- Disparador: el repartidor pulsa «Marcar como fallido».
- Resultado exitoso: despacho en `FALLIDO` con motivo, evidencia, comentario, contador incrementado y registro en el historial.
- Resultado ante rechazo: error sin cambio de estado.

## 4. Flujo principal y alternativas

1. El repartidor pulsa «Marcar como fallido».
2. El repartidor selecciona un motivo, adjunta la fotografía y, opcionalmente, escribe un comentario.
3. El repartidor confirma la incidencia.
4. El backend recibe la solicitud con clave de idempotencia y valida token, turno, propiedad, motivo y archivo.
5. El backend registra la evidencia y aplica la transición `EN_CAMINO` → `FALLIDO`.
6. El backend persiste en una misma transacción estado, motivo, referencia de evidencia, comentario, contador + 1, marca temporal del servidor, ejecutor e historial.
7. El frontend confirma y recuerda que debe devolver el paquete al centro de despacho.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Sin motivo | No se seleccionó motivo | Envío bloqueado; campo resaltado como obligatorio | CA-02 |
| Motivo no seleccionable | Se fuerza `NO_INTENTADO` u otro motivo no seleccionable | Rechazo en backend | CA-03 |
| Sin conexión | La petición no llega al backend | Aviso de cambio no registrado y reintento explícito | CA-04 |
| Reintento | Misma clave de idempotencia | Resultado original sin duplicados | CA-05 |
| Origen no permitido | Estado distinto de `EN_CAMINO` | `409`; estado conservado | — |
| Evidencia inválida o fallo de almacenamiento | Igual que ES-F03-05 RN-03 y RN-04 | — | — |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | El motivo es obligatorio y se valida contra el catálogo canónico de Gestión de Despachos, única fuente para este campo y para F-04. | F-03 Anexo B |
| RN-02 | El formulario solo ofrece motivos con `activo=true` y `seleccionableEnCampo=true`: `CLIENTE_AUSENTE`, `DIRECCION_NO_UBICADA`, `RECHAZO_DEL_PAQUETE`, `DATOS_DE_CONTACTO_ERRONEOS`, `ZONA_INACCESIBLE` y `PAQUETE_DANADO`; todos consumen intento. El backend aplica la misma restricción. | F-03 CA-30 |
| RN-03 | `NO_INTENTADO` es de uso exclusivo del sistema (ES-F03-07); no se muestra ni se acepta desde esta acción. | F-03 Anexo B |
| RN-04 | La fotografía es obligatoria, con las mismas validaciones que ES-F03-05 RN-01, RN-03 y RN-04. | F-03 RF-06 |
| RN-05 | Solo se permite desde `EN_CAMINO`; otro origen responde `409`. | F-03 Anexo A |
| RN-06 | El contador de intentos aumenta en uno solo cuando la transición se acepta, nunca por reintentos. | F-03 RF-10 |
| RN-07 | El estado se presenta al repartidor como «No entregado, regresa al centro de despacho». | F-03 RF-06 |
| RN-08 | El despacho `FALLIDO` sigue contando en la ocupación del repartidor hasta que el Gestor confirma su recepción en el centro (F-04). | F-03 RF-06 |
| RN-09 | Turno, idempotencia, transacción con historial y manejo sin conexión siguen ES-F03-04 RN-04, RN-06, RN-07 y RN-08. | F-03 RF-11 |

| Campo de entrada | Obligatorio |
|---|---|
| Código del despacho | Sí |
| Código de motivo | Sí |
| Fotografía de evidencia | Sí |
| Comentario | No |
| Clave de idempotencia | Sí |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| Catálogo canónico de motivos | Motivos seleccionables | [Gestión §4](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo) |
| Almacenamiento privado de evidencia | Registro de la fotografía | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md); mecanismo pendiente (`pendiente.md`) |
| Máquina de estados, historial y eventos | Transición, registro y publicación | Overview, sección 6 y RT-03 |
| F-04 Entregas Fallidas | Consume el despacho `FALLIDO` con motivo, contador y evidencia; puede consultar el catálogo completo | F-04 |

## 6. Criterios de aceptación

### CA-01. Incidencia con motivo tipificado

- **DADO** un despacho en `EN_CAMINO` que no pudo entregarse.
- **CUANDO** el repartidor elige «Marcar como fallido», selecciona `CLIENTE_AUSENTE`, adjunta la fotografía del domicilio y confirma.
- **ENTONCES** el estado cambia a `FALLIDO`, se guardan motivo, evidencia y comentario, el contador aumenta en uno, la interfaz recuerda devolver el paquete al centro y el despacho queda disponible para F-04.

### CA-02. Motivo no seleccionado

- **DADO** el formulario de incidencia sin motivo.
- **CUANDO** el repartidor intenta confirmar.
- **ENTONCES** el envío se bloquea y el campo de motivo se resalta como obligatorio.

### CA-03. Motivos disponibles en el formulario

- **DADO** que el repartidor abre el formulario de incidencia.
- **CUANDO** se cargan los motivos del catálogo.
- **ENTONCES** el campo ofrece solo los motivos con `activo=true` y `seleccionableEnCampo=true`, sin `NO_INTENTADO`, y el backend rechaza cualquier otro motivo aunque se fuerce la solicitud.

### CA-04. Pérdida de conexión durante el envío

- **DADO** que el repartidor confirma la operación.
- **CUANDO** la petición no llega al backend por falta de señal.
- **ENTONCES** la interfaz informa que el cambio no se registró, conserva el estado anterior y exige un reintento explícito.

### CA-05. Reintento idempotente

- **DADO** un reintento de una operación cuyo resultado se desconoce.
- **CUANDO** el backend recibe una segunda solicitud con la misma clave de idempotencia.
- **ENTONCES** devuelve el resultado original sin duplicar la transición, el incremento del contador ni el registro en el historial.

### CA-06. Registro en el historial

- **DADO** una transición a `FALLIDO` aceptada.
- **CUANDO** se persiste.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual, marca temporal del servidor, estado anterior, estado nuevo, motivo y observaciones.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: registro de evidencia, transición e incremento del contador en una misma operación.
- No funcionales: la evidencia nunca es pública (ES-F03-08).
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación

| Criterio | Tipo de comprobación | Datos o escenario |
|---|---|---|
| CA-01 | Integración y UI | Despacho `EN_CAMINO`, motivo `CLIENTE_AUSENTE`, fotografía válida |
| CA-02 | UI | Formulario sin motivo |
| CA-03 | Integración y UI | Catálogo con motivos inactivos, no seleccionables y `NO_INTENTADO`; solicitud forzada |
| CA-04 | UI | Falta de señal al confirmar |
| CA-05 | Integración | Dos solicitudes con la misma clave |
| CA-06 | Integración | Transición aceptada |

Tareas en [tasks.md](./tasks.md); resultados en [evidence.md](./evidence.md).

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-06, RF-10, RF-11, CA-19 a CA-22, CA-30, CA-31, Anexo A y Anexo B.
2. [Contrato de Gestión §4](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo).
3. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
4. Wireframe del formulario de incidencia.
