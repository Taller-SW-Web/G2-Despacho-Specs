# Especificación SPEC-F03-FORM-02: Formulario de Entrega Exitosa y Captura Fotográfica

**Tipo:** Formulario / Vista (Mobile-First)  
**Macro-funcionalidad:** F-03: Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Repartidor  

---

## 1. Contexto

El momento culmen del proceso de despacho es la entrega física del paquete al cliente en su domicilio. Para cerrar la orden de forma incuestionable, prevenir fraudes y dar tranquilidad tanto al cliente como al comercio, es requisito reglamentario obligatorio capturar y registrar una fotografía nítida del paquete en el predio o en manos del receptor.

---

## 2. Propósito

Proveer un formulario móvil táctil para registrar la entrega exitosa de un despacho en estado `EN_CAMINO`, exigiendo la captura obligatoria de una fotografía de evidencia, aplicando compresión y sanitización de metadatos en el navegador del cliente y capturando opcionalmente los datos de quien recibe.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Apertura del formulario de confirmación desde la tarjeta de despacho en estado `EN_CAMINO`.
- Botón de cámara táctil con apertura directa de la cámara nativa del móvil (`<input type="file" accept="image/*" capture="environment">`).
- Procesamiento en el navegador mediante Canvas API:
  - Redimensionamiento proporcional a máximo 1280 píxeles en su lado mayor.
  - Compresión de calidad JPEG a un peso aproximado de 1 MB.
  - Eliminación estricta de metadatos EXIF (coordenadas GPS incrustadas, marca de dispositivo).
- Previsualización visual de la imagen capturada con opción de *"Tomar otra foto"*.
- Campo de texto opcional para el nombre de la persona que recibe el paquete (`nombreReceptor`).
- Bloqueo estricto del botón de confirmación mientras no exista una fotografía válida cargada.
- Generación de clave de idempotencia (`Idempotency-Key`) en el cliente para tolerar reintentos en zonas de baja cobertura.
- Envío mediante `POST /api/v1/despachos/{idDespacho}/entregar` y transición de estado a `ENTREGADO`.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- El despacho debe encontrarse exactamente en estado `EN_CAMINO` y asignado al repartidor autenticado.
- El dispositivo debe contar con cámara funcional y permisos del navegador concedidos.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `POST /api/v1/despachos/{idDespacho}/entregar` | Endpoint backend que valida y persiste la evidencia y cambia el estado (`SPEC-F03-PROC-01`). |
| `SPEC-F03-PROC-02` | Servicio de almacenamiento de objetos privados (Supabase Storage / S3). |

### 4.3. Resultados
- Fotografía subida de forma segura al bucket privado.
- Estado del despacho transicionado a `ENTREGADO`.
- Ocupación liberada en el balance del vehículo en F-05.
- Retorno a la pantalla de ruta con el despacho marcado en verde como completado.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Captura y obligatoriedad de la fotografía
El formulario DEBE exigir una imagen antes de permitir la confirmación.

#### CA-01. Botón deshabilitado sin evidencia
- **DADO** que el repartidor abre el formulario de entrega.
- **CUANDO** la fotografía aún no ha sido capturada.
- **ENTONCES** el botón *"Confirmar Entrega"* se muestra deshabilitado (gris), con el texto de ayuda *"Debes adjuntar una fotografía del paquete para confirmar"*.

#### CA-02. Captura y previsualización exitosa
- **DADO** que el repartidor acciona la cámara y toma una fotografía válida.
- **CUANDO** la imagen es procesada por el cliente.
- **ENTONCES** se muestra la imagen en el recuadro de previsualización, se habilitan los botones *"Confirmar Entrega"* y *"Cambiar foto"*, y la imagen resultante pesa menos de 1.5 MB sin metadatos EXIF.

### RF-02. Confirmación y transición de estado
El formulario DEBE enviar la evidencia y confirmar la transición.

#### CA-03. Confirmación exitosa de entrega
- **DADO** un despacho en `EN_CAMINO`, fotografía capturada y nombre de receptor "María Gómez".
- **CUANDO** el repartidor pulsa *"Confirmar Entrega"*.
- **ENTONCES** se envía la petición con `Idempotency-Key`, el backend responde `200 OK`, el despacho pasa a `ENTREGADO` y la interfaz retorna a la ruta mostrando un mensaje de felicitación/éxito.

#### CA-04. Tolerancia a cortes de red con idempotencia
- **DADO** que el repartidor confirma la entrega pero la señal móvil se interrumpe antes de recibir la confirmación HTTP.
- **CUANDO** el repartidor vuelve a pulsar *"Reintentar"* al recuperar cobertura.
- **ENTONCES** el frontend reenvía la solicitud con la misma clave de idempotencia y el backend retorna el resultado exitoso original sin duplicar transiciones ni registros en auditoría.

---

## 6. Frontend

### 6.1. Componentes
- **`DeliveryConfirmationModal`**: Pantalla completa mobile-first para concentración en la tarea.
- **`CameraCaptureZone`**: Área táctil grande de disparo de cámara con icono central.
- **`ImageCompressorUtil`**: Utilidad pura en JavaScript/TypeScript que emplea un elemento `<canvas>` en memoria para redimensionar y exportar a `Blob` JPEG eliminando EXIF.
- **`RecipientNameInput`**: Input de texto con sugerencia *"Nombre de quien recibe (opcional)"*.
- **`ConfirmDeliveryButton`**: Botón de confirmación prominente con barra de progreso de subida.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `POST /api/v1/despachos/{idDespacho}/entregar`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Idempotency-Key: <UUID>`, `Content-Type: multipart/form-data`
- **Parámetros del formulario (FormData):**
  - `fotoEvidencia`: Archivo binario (JPEG/PNG, máx. 2 MB).
  - `nombreReceptor`: String (opcional, máx. 100 caracteres).
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idDespacho": "DSP-100234",
  "estado": "ENTREGADO",
  "fechaEntrega": "2026-09-19T17:15:30Z",
  "evidenciaRegistrada": true,
  "nombreReceptor": "María Gómez"
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento de Compresión:** El procesamiento en cliente de la imagen tomada por la cámara debe tardar menos de 800 ms en un teléfono gama media.
- **Seguridad y Privacidad:** Las fotos no se almacenan en el almacenamiento local persistente del dispositivo; se limpian de memoria tras el envío.
- **Idempotencia:** Cabecera `Idempotency-Key` obligatoria generada mediante UUID v4.

---

## 9. Fuera de alcance

- Firma digital en pantalla táctil o captura de huella dactilar.
- Cobro en efectivo (contra entrega) o validación de vouchers de transferencia bancaria.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI State Test | RTL / Vitest | Botón submit deshabilitado si `imageBlob === null`. |
| CA-02 | Client Compression Test | Vitest (JSDOM Canvas) | Canvas procesa imagen, reduce dimensiones y remueve headers EXIF. |
| CA-03 | Multipart Form Test | Mock Service Worker | Envío de FormData con cabecera `Idempotency-Key` recibe `200 OK`. |
| CA-04 | Idempotency Retry Test | Cypress | Doble envío de petición con misma clave produce respuesta idéntica. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El formulario capture y comprima adecuadamente fotografías en dispositivos móviles reales.
2. No sea posible confirmar una entrega sin adjuntar evidencia fotográfica.
3. Se garantice la transición a `ENTREGADO` y la persistencia de la referencia multimedia.
