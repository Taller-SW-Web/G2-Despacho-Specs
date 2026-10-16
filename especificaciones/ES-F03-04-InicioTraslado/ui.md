# UI de ES-F03-04: Inicio de traslado del despacho

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** Acción «En camino» en «Mi Ruta» y en el detalle del despacho.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario: repartidor en turno.
- Contexto: al salir del centro de despacho, desde el celular.
- Objetivo visible: marcar en un toque que el paquete va en camino.

## 2. Referencias visuales

| Fuente | Aplicación |
|---|---|
| Wireframes de «Mi Ruta» y del detalle de F-03 | Ubicación de la acción |
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | Botones, badges y notificaciones |
| [Componentes React](../../disenio/componentes-react.md) | Componentes compartidos aplicables (DT-02 del plan) |

## 3. Pantallas e interacción

### UI-01. Acción «En camino»

| Elemento | Contenido y comportamiento |
|---|---|
| Botón | Visible solo en despachos `ASIGNADO` y en modo operativo |
| Envío | Bloquea el botón y evita doble envío; reutiliza la misma clave al reintentar |
| Éxito | Badge cambia a `EN_CAMINO` sin recargar la vista |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Pulsar «En camino» | Indicador de envío | CA-01 |
| 2 | Respuesta exitosa | Estado actualizado en la vista | CA-01 |
| 3 | `409` por origen no permitido | Mensaje y estado conservado | CA-02 |
| 4 | `409` por reasignación o cancelación | «Este despacho fue actualizado» y refresco de la ruta | CA-03 |
| 5 | Sin conexión | «El cambio no se registró» y botón «Reintentar» | RN-08 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Disponible | Botón «En camino» | Pulsar | CA-01 |
| Enviando | Botón deshabilitado con indicador | Esperar | CA-01 |
| Éxito | Badge `EN_CAMINO` | Continuar | CA-01 |
| Conflicto | Mensaje según causa | Aceptar | CA-02, CA-03 |
| Sin conexión | Aviso persistente con estado anterior | «Reintentar» | RN-08 |

## 5. Mensajes

| Respuesta | Mensaje | Recuperación |
|---|---|---|
| Éxito | «Despacho en camino.» | — |
| `409` origen | «Este despacho ya no puede marcarse en camino.» | Aceptar |
| `409` reasignado o cancelado | «Este despacho fue actualizado. Se refrescó tu ruta.» | Refresco automático |
| `409` fuera de turno | «Tu turno no está activo. Solo puedes consultar tu ruta.» | Solo lectura (ES-F03-01) |
| Sin conexión | «No se registró el cambio. Revisa tu señal e inténtalo de nuevo.» | «Reintentar» |

Los textos son propuesta; los códigos definitivos provienen del contrato (DT-01).

## 6. Accesibilidad

- Botón con objetivo táctil amplio y nombre accesible.
- Mensajes anunciados a lectores de pantalla.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Pulsar en despacho `ASIGNADO` | Estado actualizado sin recarga completa | CA-01 |
| CUI-02 | Pulsar varias veces seguidas | Un solo envío | CA-04 |
| CUI-03 | Recibir cada tipo de `409` | Mensaje correcto; refresco en reasignación o cancelación | CA-02, CA-03 |
| CUI-04 | Simular falta de señal | Estado anterior conservado y reintento explícito | RN-08 |

## 8. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
