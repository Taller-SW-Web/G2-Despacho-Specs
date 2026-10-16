# UI de ES-F03-06: Registro de entrega fallida

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** Formulario de incidencia, abierto desde el detalle de un despacho `EN_CAMINO`.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario: repartidor en turno.
- Contexto: en el domicilio del destinatario, desde el celular.
- Objetivo visible: registrar por qué no se pudo entregar y saber que debe devolver el paquete.

## 2. Referencias visuales

| Fuente | Aplicación |
|---|---|
| Wireframe del formulario de incidencia de F-03 | Composición del formulario |
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | Campos, selector, botones y notificaciones |
| [Componentes React](../../disenio/componentes-react.md) | Componentes compartidos aplicables (DT-02 del plan) |

## 3. Pantallas e interacción

### UI-01. Formulario de incidencia

| Elemento | Contenido y comportamiento |
|---|---|
| Motivo | Selector obligatorio con los motivos de RN-02; sin `NO_INTENTADO` |
| Fotografía | Captura, previsualización y opción de repetir; obligatoria |
| Comentario | Texto opcional |
| «Confirmar incidencia» | Bloquea el envío si falta motivo o fotografía; evita doble envío |
| Confirmación | «No entregado, regresa al centro de despacho» |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Pulsar «Marcar como fallido» | Formulario con motivos cargados | CA-03 |
| 2 | Confirmar sin motivo | Envío bloqueado; motivo resaltado | CA-02 |
| 3 | Completar y confirmar | Indicador de envío | CA-01 |
| 4 | Respuesta exitosa | Estado «No entregado» y recordatorio de devolución | CA-01 |
| 5 | Sin conexión | «El cambio no se registró» con datos conservados y «Reintentar» | CA-04 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Cargando motivos | Selector con indicador | Esperar | CA-03 |
| Error al cargar motivos | Mensaje sin detalle técnico | «Reintentar» | CA-03 |
| Incompleto | Campos obligatorios resaltados al intentar confirmar | Completar | CA-02 |
| Enviando | Controles bloqueados | Esperar | CA-01 |
| Éxito | «No entregado, regresa al centro de despacho» | Volver a «Mi Ruta» | CA-01 |
| Sin conexión | Aviso con datos conservados | «Reintentar» | CA-04 |
| Error de evidencia | Igual que ES-F03-05 | Reintentar o capturar de nuevo | RN-04 |

## 5. Mensajes

| Respuesta | Mensaje | Recuperación |
|---|---|---|
| Éxito | «Incidencia registrada. Devuelve el paquete al centro de despacho.» | — |
| Motivo faltante | «Selecciona un motivo.» | Completar |
| Motivo rechazado por backend | «El motivo seleccionado ya no está disponible.» | Recargar motivos |
| `409` | «Este despacho ya no puede marcarse como fallido.» | Volver a «Mi Ruta» |
| Sin conexión | «No se registró la incidencia. Revisa tu señal e inténtalo de nuevo.» | «Reintentar» |

Los textos son propuesta.

## 6. Accesibilidad

- Selector y campos con etiqueta visible y nombre accesible.
- Errores de campo asociados y anunciados a lectores de pantalla.
- Objetivos táctiles amplios.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Abrir el formulario | Solo motivos seleccionables, sin `NO_INTENTADO` | CA-03 |
| CUI-02 | Confirmar sin motivo o sin fotografía | Envío bloqueado y campos resaltados | CA-02 |
| CUI-03 | Registrar con éxito | Recordatorio de devolución visible | CA-01 |
| CUI-04 | Simular falta de señal | Datos conservados y reintento explícito | CA-04 |
| CUI-05 | Recorrer con lector de pantalla en móvil | Controles y errores anunciados | CA-01 a CA-04 |

## 8. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. Wireframe del formulario de incidencia de F-03.
