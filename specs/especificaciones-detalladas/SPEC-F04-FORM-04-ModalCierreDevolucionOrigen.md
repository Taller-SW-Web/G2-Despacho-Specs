# Especificación SPEC-F04-FORM-04: Modal de Cierre como Devuelto a Origen

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-04: Entregas Fallidas y Reprogramaciones  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho  

---

## 1. Contexto

Cuando un despacho agota sus intentos de entrega permitidos por la política de la empresa, cuando el cliente rechaza irrevocablemente el bulto o cuando el pedido es cancelado formalmente desde Ventas, el ciclo de distribución a domicilio debe darse por concluido. El paquete permanecerá en el almacén del centro de despacho a disposición del área comercial.

---

## 2. Propósito

Proveer un diálogo modal para formalizar el cierre definitivo de un despacho fallido recibido en el centro, exigiendo una justificación operativa, transicionando el estado a `DEVUELTO_A_ORIGEN` y disparando la notificación correspondiente hacia el módulo de Ventas y Postventa.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Apertura del diálogo modal desde el panel de fallidos (`SPEC-F04-FORM-01`).
- Verificación previa de recepción física: solo se puede cerrar a origen si `recibidoEnCentro: true`.
- Selector obligatorio de motivo de cierre a origen:
  - `MAXIMO_INTENTOS_ALCANZADO`
  - `PEDIDO_ANULADO_COMERCIALMENTE`
  - `RECHAZO_DEFINITIVO_DESTINATARIO`
  - `DETERIORO_IRRECUPERABLE_MERCADERIA`
- Campo de texto obligatorio para justificación detallada (mínimo 10 caracteres).
- Advertencia visual crítica: *"Esta acción es definitiva e irreversible. No se programarán más intentos de transporte para este pedido."*
- Envío mediante `POST /api/v1/despachos/{idDespacho}/devolver-origen`.
- Transición de estado a `DEVUELTO_A_ORIGEN`.
- Disparo asíncrono del evento hacia Ventas y Postventa (`SPEC-F04-PROC-02`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Despacho en estado `FALLIDO` con recepción confirmada en el centro de despacho.
- Rol autenticado `GESTOR_DESPACHO` o `ADMIN`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `POST /api/v1/despachos/{idDespacho}/devolver-origen` | Endpoint backend que ejecuta el cierre y la auditoría (`SPEC-F04-PROC-01`). |
| `SPEC-F04-PROC-02` | Emisión del evento de integración hacia Ventas y Postventa. |

### 4.3. Resultados
- Despacho cerrado terminalmente en estado `DEVUELTO_A_ORIGEN`.
- Se genera el evento de devolución para que Ventas proceda con reembolsos o notas de crédito.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Justificación obligatoria y cierre
El modal DEBE exigir motivo y justificación antes de confirmar el cierre.

#### CA-01. Cierre exitoso con motivo tipificado
- **DADO** un despacho fallido con 2 intentos fallidos, recibido en el centro.
- **CUANDO** el gestor selecciona `MAXIMO_INTENTOS_ALCANZADO`, ingresa la justificación *"Cliente no habido en dos visitas coordinadas"* y confirma.
- **ENTONCES** el backend responde `200 OK`, el estado cambia a `DEVUELTO_A_ORIGEN`, se genera el evento hacia Ventas y el modal se cierra con notificación exitosa.

#### CA-02. Bloqueo por falta de justificación
- **DADO** que el gestor intenta confirmar el cierre sin seleccionar motivo o con texto en blanco.
- **CUANDO** pulsa confirmar.
- **ENTONCES** el formulario bloquea el botón y resalta los campos como obligatorios.

#### CA-03. Idempotencia ante cierres repetidos
- **DADO** un despacho que ya fue cerrado como `DEVUELTO_A_ORIGEN`.
- **CUANDO** se intenta reenviar la operación.
- **ENTONCES** el sistema responde `409 Conflict` indicando *"El despacho ya se encuentra cerrado como Devuelto a Origen"*.

---

## 6. Frontend

### 6.1. Componentes
- **`ReturnToOriginModal`**: Diálogo modal con barra superior en color rojo/advertencia.
- **`CloseReasonSelect`**: Dropdown con motivos normalizados.
- **`JustificationTextarea`**: Área de texto obligatoria con contador de caracteres.
- **`IrreversibleActionWarning`**: Banner visual con icono de alerta roja.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `POST /api/v1/despachos/{idDespacho}/devolver-origen`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Content-Type: application/json`
- **Cuerpo:**
```json
{
  "motivoCierre": "MAXIMO_INTENTOS_ALCANZADO",
  "justificacion": "Se realizaron dos visitas con cliente ausente verificado"
}
```
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idDespacho": "DSP-100234",
  "estado": "DEVUELTO_A_ORIGEN",
  "fechaCierre": "2026-09-19T18:45:00Z",
  "eventoVentasPublicado": true
}
```

---

## 8. Requisitos no funcionales

- **Consistencia Transaccional:** El cambio de estado local se persiste de forma atómica. Si falla la comunicación externa con Ventas, el estado local no se revierte pero se encola el evento para reintento.
- **Auditoría:** Registro inmutable del usuario gestor y la justificación textual.

---

## 9. Fuera de alcance

- Emisión de notas de crédito o reembolsos monetarios (competencia exclusiva de Ventas).
- Destrucción o donación de mercadería.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI Modal Test | RTL / Vitest | Confirmación válida envía payload y cierra diálogo. |
| CA-02 | Validation Test | Vitest | Justificación corta (< 10 caracteres) bloquea confirmación. |
| CA-03 | Conflict Check | MockMvc | Petición sobre despacho ya devuelto retorna `409 Conflict`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El modal exija justificativa operativa formal para el cierre.
2. El despacho transicione a `DEVUELTO_A_ORIGEN` de forma irreversible.
3. Se garantice la emisión del evento de comunicación externa hacia Ventas.
