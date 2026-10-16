# UI de ES-F03-07: Cierre de jornada y resumen del día

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** Acción «Cerrar jornada», confirmación, lista de devolución y resumen del día.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario: repartidor (cierre en turno; resumen en turno o fuera de turno).
- Contexto: al final de la jornada, desde el celular.
- Objetivo visible: cerrar el día sabiendo qué despachos quedan como no intentados y qué paquetes devolver.

## 2. Referencias visuales

| Fuente | Aplicación |
|---|---|
| Wireframes del cierre y del resumen de jornada de F-03 | Composición de las vistas |
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | Diálogos, listas, cifras y notificaciones |
| [Componentes React](../../disenio/componentes-react.md) | Componentes compartidos aplicables (DT-03 del plan) |

## 3. Pantallas e interacción

### UI-01. Confirmación de cierre

| Elemento | Contenido y comportamiento |
|---|---|
| Acción | «Cerrar jornada», visible en modo operativo |
| Diálogo | Con pendientes: «N despachos quedarán como no intentados». Sin pendientes: «No tienes despachos pendientes». |
| Botones | «Confirmar cierre» y «Cancelar»; bloqueo de doble envío |

### UI-02. Lista de devolución

| Elemento | Contenido y comportamiento |
|---|---|
| Lista | Paquetes a devolver al centro con código operativo interno (alcance según DT-05) |
| Ubicación | Tras confirmar el cierre, antes del resumen |

### UI-03. Resumen del día

| Elemento | Contenido y comportamiento |
|---|---|
| Cifras | Asignados, entregados, fallidos con intento, no intentados y pendientes |
| Acceso | Tras el cierre y desde «Mi Ruta» en cualquier momento |
| Exportación | No disponible |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Pulsar «Cerrar jornada» | Diálogo con la cantidad afectada | CA-01, CA-02 |
| 2 | Confirmar | Indicador de envío | CA-01 |
| 3 | Respuesta exitosa | Lista de devolución, resumen y modo solo lectura | CA-01, CA-02 |
| 4 | Sin conexión | «El cierre no se registró» y «Reintentar» | RN-08 |
| 5 | Abrir el resumen fuera de turno | Cifras del día | CA-04 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Confirmación | Diálogo con cantidad afectada | Confirmar o cancelar | CA-01, CA-02 |
| Enviando | Controles bloqueados | Esperar | CA-01 |
| Cerrado | Lista de devolución y resumen | Consultar | CA-01, CA-02 |
| Sin conexión | Aviso sin cambios aplicados | «Reintentar» | RN-08 |
| Resumen cargando | Skeleton de cifras | Esperar | CA-04 |
| Error del resumen | Mensaje sin detalle técnico | «Reintentar» | CA-04 |

## 5. Mensajes

| Respuesta | Mensaje | Recuperación |
|---|---|---|
| Éxito con pendientes | «Jornada cerrada. Devuelve estos paquetes al centro de despacho.» | — |
| Éxito sin pendientes | «Jornada cerrada.» | — |
| Sin conexión | «No se registró el cierre. Revisa tu señal e inténtalo de nuevo.» | «Reintentar» |

Los textos son propuesta.

## 6. Accesibilidad

- Diálogo con foco atrapado y cierre con teclado.
- Cifras del resumen con etiqueta textual, no solo color o icono.
- Mensajes anunciados a lectores de pantalla.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Cerrar con pendientes | Cantidad correcta en el diálogo y lista de devolución | CA-01 |
| CUI-02 | Cerrar sin pendientes | Diálogo sin advertencia y resumen | CA-02 |
| CUI-03 | Simular falta de señal | Sin cambios y reintento explícito | RN-08 |
| CUI-04 | Abrir el resumen en turno y fuera de turno | Cifras coherentes con la ruta | CA-04 |
| CUI-05 | Recorrer con lector de pantalla en móvil | Diálogo y cifras anunciados | CA-01 a CA-04 |

## 8. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. Wireframes del cierre y del resumen de jornada de F-03.
