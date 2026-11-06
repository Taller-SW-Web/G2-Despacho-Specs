# UI de ES-F04-07: Recibir en el centro y resolver un recojo

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** vista «Recojos» del panel administrativo.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario y permisos: Gestor con rol `GESTOR_DESPACHO`.
- Objetivo visible: confirmar los productos que llegan y decidir sobre los recojos no realizados.
- Acceso: panel administrativo → Recojos.

## 2. Pantallas e interacción

### UI-01. Lista

Tabla con código, repartidor, estado, motivo y fecha, con filtro por estado. Reutiliza la composición de entregas fallidas.

### UI-02. Acciones

| Estado | Acciones |
|---|---|
| `RECOGIDO` | «Confirmar recepción» |
| `FALLIDO` | «Reprogramar» con fecha, y «Cerrar» con motivo |
| Otros | Solo lectura |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Abrir la vista | Recojos por resolver | CA-01 |
| 2 | Confirmar la recepción | Estado actualizado | CA-02 |
| 3 | Reprogramar o cerrar | Confirmación y lista actualizada | CA-03, CA-04 |
| 4 | Recojo desactualizado | Aviso y lista actualizada | CA-05 |

## 3. Accesibilidad

- Los modales tienen foco controlado y errores anunciados.
- Los estados usan texto, no solo color.

## 4. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Recojos en cada estado | Acciones correctas | CA-01 a CA-04 |
| CUI-02 | Reprogramar sin fecha o cerrar sin motivo | Envío bloqueado | CA-03, CA-04 |
| CUI-03 | Respuesta `409` | Aviso y actualización | CA-05 |

## 5. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
