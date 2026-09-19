# Especificación SPEC-F04-FORM-02: Formulario de Confirmación de Recepción en Centro de Despacho

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-04: Entregas Fallidas y Reprogramaciones  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho  

---

## 1. Contexto

Todo paquete que no pudo ser entregado en calle debe retornar físicamente a las instalaciones del centro de despacho. Antes de que el Gestor de Despacho pueda autorizar una reprogramación para otro día o decidir que el paquete sea devuelto a la tienda de origen, debe existir constancia formal de que el bulto reingresó al centro y se verificó el estado físico de su precinto de seguridad.

---

## 2. Propósito

Proveer un formulario modal que permita al Gestor de Despacho certificar el retorno físico de un paquete sellado al centro de despacho, registrar el estado del precinto/sello de seguridad y observaciones de recepción, desvinculando la carga del vehículo del chofer en F-05 y habilitando la toma de decisiones sobre el despacho.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Apertura del diálogo modal desde el panel de entregas fallidas (`SPEC-F04-FORM-01`).
- Identificación del paquete a recibir: Código de rastreo, pedido, fecha de fallo, chofer que lo entrega.
- Formulario de inspección física:
  - Casilla de verificación obligatoria: *"¿Sello o precinto de seguridad intacto?"* (`selloIntacto: boolean`).
  - Selector de estado físico del empaque: `INTACTO`, `DETERIORO_LEVE`, `DETERIORO_GRAVE`.
  - Campo de texto libre para observaciones del inventario (máx. 250 caracteres).
- Envío mediante `POST /api/v1/despachos/{idDespacho}/recepcion-centro`.
- Efectos inmediatos:
  - El despacho permanece en estado `FALLIDO` pero se marca con `recibidoEnCentro: true`.
  - El paquete deja de computar en la ocupación y carga del repartidor en F-05 (`SPEC-F05-PROC-01`).
  - Se registra auditoría inmutable de recepción.
  - Se habilitan las opciones de reprogramar o devolver en la interfaz.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- El despacho debe estar en estado `FALLIDO` y con `recibidoEnCentro = false`.
- Usuario autenticado con rol `GESTOR_DESPACHO` o `ADMIN`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `POST /api/v1/despachos/{idDespacho}/recepcion-centro` | Endpoint backend que registra la recepción y audita la acción. |
| F-05 (Flota y Capacidad) | Descontar el paquete de la ocupación del chofer al liberarse de su custodia. |

### 4.3. Resultados
- Constancia formal de reingreso al almacén.
- El chofer queda eximido de la custodia del bulto físico.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Confirmación de inspección física
El formulario DEBE registrar fielmente las condiciones del paquete recibido.

#### CA-01. Recepción conforme con sello intacto
- **DADO** un despacho fallido retornado por el chofer con sello intacto y caja en perfecto estado.
- **CUANDO** el gestor marca la casilla de sello intacto, selecciona estado `INTACTO` y confirma la recepción.
- **ENTONCES** el backend responde `200 OK`, el despacho se actualiza a `recibidoEnCentro = true`, se descuenta de la carga del chofer en F-05 y el modal se cierra con notificación de éxito.

#### CA-02. Recepción con sello roto o caja deteriorada
- **DADO** un paquete retornado cuyo precinto fue violado o presenta caja rota.
- **CUANDO** el gestor desmarca la casilla de sello intacto, selecciona `DETERIORO_GRAVE` e ingresa la nota *"Empaque abierto, se requiere inspección de contenido"*.
- **ENTONCES** el sistema persiste la recepción con la alerta de inspección y audita la incidencia sin impedir el registro físico del reingreso.

### RF-02. Idempotencia y prevención de doble recepción
El sistema DEBE evitar recepciones duplicadas sobre el mismo bulto.

#### CA-03. Paquete previamente recibido
- **DADO** un despacho cuya recepción ya fue registrada hace instantes.
- **CUANDO** se intenta confirmar una segunda recepción.
- **ENTONCES** el backend responde `409 Conflict` indicando *"El paquete ya fue recibido previamente en el centro de despacho"*.

---

## 6. Frontend

### 6.1. Componentes
- **`PackageReceptionModal`**: Diálogo modal accesible desde la tabla de fallidos.
- **`PackageVerificationSummary`**: Resumen del paquete (bulto, remitente, chofer).
- **`SealVerificationCheckbox`**: Checkbox prominente con icono de candado para certificar la integridad del precinto.
- **`DamageSelector`**: Radio group con opciones visuales de estado del empaque.
- **`ReceptionNotesTextarea`**: Textarea para observaciones.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `POST /api/v1/despachos/{idDespacho}/recepcion-centro`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Content-Type: application/json`
- **Cuerpo:**
```json
{
  "selloIntacto": true,
  "condicionFisica": "INTACTO",
  "observaciones": "Paquete recibido conforme en ventanilla de retornos"
}
```
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idDespacho": "DSP-100234",
  "recibidoEnCentro": true,
  "fechaRecepcionCentro": "2026-09-19T18:10:00Z",
  "usuarioRecepcion": "tarqui@tienda.com",
  "estadoDespacho": "FALLIDO"
}
```

---

## 8. Requisitos no funcionales

- **Integridad Transaccional:** La recepción, la auditoría y la liberación de ocupación en F-05 se ejecutan en una sola transacción `@Transactional`.
- **Trazabilidad:** Se almacena el ID del gestor autenticado y la fecha/hora UTC exacta de recepción.

---

## 9. Fuera de alcance

- Reingreso de stock a inventario de productos (responsabilidad de Ventas e Inventario si el despacho es devuelto definitivamente).
- Apertura o conteo de contenido interior (el centro solo recibe el paquete sellado externamente).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI Modal Test | RTL / Vitest | Confirmación envía payload JSON y cierra modal. |
| CA-02 | Service Integration | MockMvc | `recibidoEnCentro` pasa a `true` y estado permanece en `FALLIDO`. |
| CA-03 | Conflict Check | JUnit 5 | Segunda invocación sobre el mismo despacho retorna `409 Conflict`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Ningún despacho pueda reprogramarse o cerrarse sin haber sido recibido primero en el centro.
2. La recepción libere la ocupación del vehículo del chofer en F-05.
3. Se persista la inspección física y el estado del sello en auditoría.
