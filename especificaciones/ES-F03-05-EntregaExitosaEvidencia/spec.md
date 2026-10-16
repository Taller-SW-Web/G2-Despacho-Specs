# ES-F03-05: Registro de entrega exitosa con evidencia

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md)

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor

**UI:** Aplica; formulario de entrega de la web responsive del repartidor.

## 1. Contexto y objetivo

Permitir que el repartidor cierre un despacho como `ENTREGADO` solo con una fotografía como evidencia de recepción y, opcionalmente, el nombre de quien recibe. Deja prueba verificable de cada entrega y libera la ocupación del repartidor. Concreta RF-05, RF-11 y la sección 8 (Evidencia fotográfica) de F-03.

## 2. Alcance

- Incluye: captura y previsualización de la fotografía, nombre opcional del receptor, registro de la evidencia y transición `EN_CAMINO` → `ENTREGADO`.
- Fuera de alcance: firma digital y documento de identidad del receptor; decisión técnica sobre compresión, metadatos y almacenamiento de la fotografía (`pendiente.md`, sección F-03); notificación al cliente final.

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor en turno según ES-F03-01, con rol `REPARTIDOR`.
- Precondiciones: el despacho está en `EN_CAMINO`, asignado al repartidor del token y en la jornada en curso; el celular tiene cámara y conexión activa.
- Disparador: el repartidor pulsa «Confirmar entrega».
- Resultado exitoso: despacho en `ENTREGADO` con referencia de evidencia, nombre del receptor si se informó y registro en el historial.
- Resultado ante rechazo: error sin cambio de estado.

## 4. Flujo principal y alternativas

1. El repartidor abre el formulario, captura y previsualiza la fotografía y, opcionalmente, registra el nombre de quien recibe.
2. El repartidor pulsa «Confirmar entrega».
3. El backend recibe la solicitud con clave de idempotencia y valida token, turno, propiedad y archivo.
4. El backend registra la evidencia en el almacenamiento privado y obtiene su referencia.
5. El backend aplica la transición `EN_CAMINO` → `ENTREGADO` y persiste en una misma transacción estado, referencia de evidencia, nombre del receptor, marca temporal del servidor, ejecutor e historial.
6. El frontend muestra la confirmación de éxito.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Sin fotografía | No hay imagen adjunta | Botón deshabilitado; no se envía la petición | CA-02 |
| Fallo de almacenamiento | Error o tiempo de espera excedido | Estado sin cambio; error informado; imagen conservada para reintentar | CA-03 |
| Archivo inválido | Formato o tamaño fuera de lo definido | `400`; archivo no guardado; estado sin cambio | CA-04 |
| Origen no permitido | Estado distinto de `EN_CAMINO` | `409`; estado conservado | — |
| Sin conexión o reintento | Igual que ES-F03-04 RN-07 y RN-08 | — | — |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | La fotografía es obligatoria; la interfaz bloquea el envío sin ella y el backend valida su presencia. | F-03 CA-16 |
| RN-02 | Solo se permite desde `EN_CAMINO`; otro origen responde `409`. | F-03 Anexo A |
| RN-03 | Si el almacenamiento falla o excede el tiempo de espera, el estado no cambia y la imagen se conserva en el formulario. | F-03 CA-17 |
| RN-04 | Un archivo que incumple formato o tamaño responde `400`, no se guarda y el estado no cambia. | F-03 CA-18 |
| RN-05 | No modifica el contador de intentos. | F-03 RF-05 |
| RN-06 | Un despacho `ENTREGADO` deja de contar en la ocupación del repartidor (recalculada por F-05). | F-03 RF-05 |
| RN-07 | Turno, idempotencia, transacción con historial y manejo sin conexión siguen ES-F03-04 RN-04, RN-06, RN-07 y RN-08. | F-03 RF-11 |

| Campo de entrada | Obligatorio |
|---|---|
| Código del despacho | Sí |
| Fotografía de evidencia | Sí |
| Nombre de quien recibe | No |
| Clave de idempotencia | Sí |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| Almacenamiento privado de evidencia | Registro de la fotografía | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md); mecanismo pendiente (`pendiente.md`) |
| Máquina de estados, historial y eventos | Transición, registro y publicación | Overview, sección 6 y RT-03 |
| F-05 | Recálculo de ocupación | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |

## 6. Criterios de aceptación

### CA-01. Confirmación con evidencia válida

- **DADO** un despacho en `EN_CAMINO`.
- **CUANDO** el repartidor captura la fotografía, opcionalmente registra el nombre de quien recibe y pulsa «Confirmar entrega».
- **ENTONCES** el sistema registra la evidencia, persiste su referencia y cambia el estado a `ENTREGADO`.

### CA-02. Confirmación sin evidencia

- **DADO** el formulario de entrega sin fotografía.
- **CUANDO** el repartidor intenta confirmar.
- **ENTONCES** el botón permanece deshabilitado, se muestra el mensaje de evidencia obligatoria y no se envía la petición.

### CA-03. Fallo en la carga de la imagen

- **DADO** una confirmación con fotografía adjunta.
- **CUANDO** el almacenamiento responde con error o excede el tiempo de espera.
- **ENTONCES** el estado no cambia, se informa el error y la imagen se conserva en el formulario para reintentar.

### CA-04. Archivo inválido

- **DADO** un archivo que incumple el formato o el tamaño definidos para la evidencia.
- **CUANDO** llega al backend.
- **ENTONCES** se responde `400 Bad Request`, no se guarda el archivo y el estado no cambia.

### CA-05. Registro en el historial

- **DADO** una transición a `ENTREGADO` aceptada.
- **CUANDO** se persiste.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual, marca temporal del servidor, estado anterior, estado nuevo y observaciones.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: registro de evidencia y transición; si la evidencia no se registra, no hay transición.
- No funcionales: la evidencia nunca es pública (ES-F03-08).
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación

| Criterio | Tipo de comprobación | Datos o escenario |
|---|---|---|
| CA-01 | Integración y UI | Despacho `EN_CAMINO` con imagen válida, con y sin nombre |
| CA-02 | UI e integración | Formulario sin imagen; petición forzada sin archivo |
| CA-03 | Integración | Almacenamiento con error y con tiempo de espera excedido |
| CA-04 | Integración | Archivo de formato no permitido y archivo sobredimensionado |
| CA-05 | Integración | Transición aceptada; reintento con la misma clave |

Tareas en [tasks.md](./tasks.md); resultados en [evidence.md](./evidence.md).

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-05, RF-11, CA-15 a CA-18, CA-31 y sección 8.
2. [Pendientes](../../funcionalidades/pendiente.md), sección F-03.
3. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
4. Wireframe del formulario de entrega.
