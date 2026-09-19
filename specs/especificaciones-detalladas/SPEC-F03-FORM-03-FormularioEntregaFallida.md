# Especificación SPEC-F03-FORM-03: Formulario de Reporte de Incidencias en Campo (Entrega Fallida)

**Tipo:** Formulario / Vista (Mobile-First)  
**Macro-funcionalidad:** F-03: Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Repartidor  

---

## 1. Contexto

Cuando un repartidor se traslada al domicilio pero no puede concretar la entrega por causas imputables al destinatario (ausencia, rechazo, datos erróneos) o de fuerza mayor (zona inaccesible, paquete deteriorado), debe documentar formalmente el motivo y la evidencia fotográfica de la visita para respaldar la gestión posterior de incidencias y reprogramaciones (F-04).

---

## 2. Propósito

Proveer un formulario móvil táctil para reportar una entrega fallida sobre un despacho en estado `EN_CAMINO`, exigiendo la selección de un motivo tipificado del catálogo oficial, la captura obligatoria de fotografía de evidencia de la visita y observaciones complementarias, alertando al operador sobre la obligación de retornar el paquete físico al centro de despacho.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Acceso desde la tarjeta de despacho mediante el botón secundario *"Reportar Incidencia / No entregado"*.
- Selector obligatorio de motivos tipificados del catálogo (`GET /api/v1/motivos-fallo`), excluyendo motivos internos del sistema (como `NO_INTENTADO`).
- Captura fotográfica obligatoria de evidencia del intento de entrega (fachada del predio, notificación de visita, aviso de puerta o daño).
- Procesamiento en navegador (compresión, remoción de metadatos EXIF mediante Canvas API).
- Campo de texto opcional para observaciones adicionales (máximo 250 caracteres).
- Advertencia visual prominente: *"El paquete continuará bajo tu responsabilidad hasta que lo entregues en el centro de despacho"*.
- Envío mediante `POST /api/v1/despachos/{idDespacho}/fallar` con clave de idempotencia.
- Transición a estado `FALLIDO` e incremento en 1 del contador de intentos.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Despacho en estado `EN_CAMINO` asignado al repartidor autenticado.
- Jornada activa en la fecha.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/motivos-fallo` | Catálogo centralizado de motivos seleccionables en campo. |
| `POST /api/v1/despachos/{idDespacho}/fallar` | Endpoint backend que valida el motivo, persiste la evidencia y cambia el estado (`SPEC-F03-PROC-01`). |
| F-04 (Entregas Fallidas) | Módulo que recibirá el despacho para confirmar su retorno y reprogramarlo. |

### 4.3. Resultados
- Despacho transicionado a `FALLIDO` con incremento de su contador de intentos.
- Paquete marcado visualmente en la ruta como "Fallido - Pendiente de retorno".
- El paquete continúa contabilizando en la ocupación del repartidor en F-05 hasta su recepción en centro.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Validación de campos obligatorios
El formulario DEBE exigir tanto el motivo tipificado como la fotografía de evidencia.

#### CA-01. Bloqueo por falta de motivo o fotografía
- **DADO** que el repartidor abre el formulario de incidencia.
- **CUANDO** no ha seleccionado un motivo del desplegable o no ha capturado la fotografía.
- **ENTONCES** el botón *"Confirmar Fallo"* permanece deshabilitado y se resaltan en rojo los campos obligatorios pendientes.

#### CA-02. Selección exitosa de motivo tipificado
- **DADO** un intento fallido porque nadie abrió la puerta.
- **CUANDO** el repartidor despliega la lista y selecciona `CLIENTE_AUSENTE`.
- **ENTONCES** el sistema asocia el código exacto y muestra el texto legible *"Cliente ausente"*.

### RF-02. Envío y confirmación de incidencia
El formulario DEBE procesar la incidencia y recordar la custodia del paquete.

#### CA-03. Registro exitoso de entrega fallida
- **DADO** un despacho en `EN_CAMINO`, motivo `CLIENTE_AUSENTE`, foto de la fachada adjunta y nota *"Se tocó timbre 3 veces durante 10 minutos"*.
- **CUANDO** el repartidor pulsa *"Confirmar Fallo"*.
- **ENTONCES** se envía la petición con `Idempotency-Key`, el backend responde `200 OK`, el despacho pasa a `FALLIDO`, el contador de intentos aumenta en 1, y la interfaz muestra una alerta informativa *"Incidencia registrada. Debes devolver este paquete al centro de despacho al culminar tu jornada"*.

---

## 6. Frontend

### 6.1. Componentes
- **`FailureReportModal`**: Pantalla completa móvil con cabecera de alerta ámbar/roja.
- **`FailureReasonSelect`**: Menú desplegable o lista de botones de selección única con los motivos del catálogo:
  - `CLIENTE_AUSENTE`
  - `DIRECCION_NO_UBICADA`
  - `RECHAZO_DEL_PAQUETE`
  - `DATOS_DE_CONTACTO_ERRONEOS`
  - `ZONA_INACCESIBLE`
  - `PAQUETE_DANADO`
- **`EvidencePhotoCapture`**: Componente de cámara con visor de imagen comprimida.
- **`FailureNotesTextarea`**: Textarea con contador reactivo de caracteres restantes.
- **`ReturnWarningBanner`**: Banner informativo con icono de advertencia sobre el retorno físico del paquete.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `POST /api/v1/despachos/{idDespacho}/fallar`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Idempotency-Key: <UUID>`, `Content-Type: multipart/form-data`
- **Form Data:**
  - `codigoMotivo`: String obligatorio (enum `CLIENTE_AUSENTE`, etc.).
  - `fotoEvidencia`: Archivo binario obligatorio (máx. 2 MB).
  - `observaciones`: String opcional (máx. 250 caracteres).
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idDespacho": "DSP-100234",
  "estado": "FALLIDO",
  "codigoMotivo": "CLIENTE_AUSENTE",
  "numeroIntento": 2,
  "maximoIntentos": 2,
  "pendienteRetornoCentro": true,
  "fechaRegistroFallo": "2026-09-19T17:40:00Z"
}
```

---

## 8. Requisitos no funcionales

- **Consistencia:** El incremento del contador de intentos y el registro del motivo se ejecutan en la misma transacción ACID de base de datos.
- **Trazabilidad:** Se registra en el historial común que el fallo fue declarado por el repartidor en campo.
- **Idempotencia:** Ante múltiples clics o reintentos con la misma clave, el contador de intentos NO se incrementa más de una vez.

---

## 9. Fuera de alcance

- Declaración del motivo `NO_INTENTADO` (reservado exclusivamente para el cierre de jornada o corte automático).
- Decisión de reprogramación o anulación del paquete (competencia del Gestor de Despacho en F-04).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI Validation Test | RTL / Vitest | Submit deshabilitado si falta foto o motivo. |
| CA-02 | Select Catalog Test | MSW | Dropdown muestra exactamente los 6 motivos seleccionables en campo. |
| CA-03 | Multipart Post Test | MockMvc / Cypress | Despacho cambia a `FALLIDO` y `numeroIntento` incrementa en 1. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El formulario impida registrar fallos sin foto de evidencia o sin motivo del catálogo.
2. El backend transicione el estado a `FALLIDO` e incremente el contador de intentos atómicamente.
3. El frontend presente el recordatorio obligatorio de devolución al centro.
