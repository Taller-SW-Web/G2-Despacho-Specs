# UI de ES-F03-05: Registro de entrega exitosa con evidencia

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** Formulario de entrega, abierto desde el detalle de un despacho `EN_CAMINO`.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario: repartidor en turno.
- Contexto: en el domicilio del destinatario, desde el celular.
- Objetivo visible: dejar prueba fotográfica y cerrar la entrega.

## 2. Referencias visuales

| Fuente | Aplicación |
|---|---|
| Wireframe del formulario de entrega de F-03 | Composición del formulario |
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | Campos, botones y notificaciones |
| [Componentes React](../../disenio/componentes-react.md) | Componentes compartidos aplicables (DT-03 del plan) |

## 3. Pantallas e interacción

### UI-01. Formulario de entrega

| Elemento | Contenido y comportamiento |
|---|---|
| Fotografía | Captura con la cámara, previsualización y opción de repetir |
| Nombre de quien recibe | Campo de texto opcional |
| «Confirmar entrega» | Deshabilitado sin fotografía; bloquea doble envío |
| Mensaje obligatorio | «La fotografía de evidencia es obligatoria.» visible mientras falte |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Abrir el formulario | Botón deshabilitado y mensaje obligatorio | CA-02 |
| 2 | Capturar la fotografía | Previsualización; botón habilitado | CA-01 |
| 3 | Confirmar | Indicador de envío | CA-01 |
| 4 | Respuesta exitosa | Confirmación y estado `ENTREGADO` | CA-01 |
| 5 | Fallo de almacenamiento | Error; imagen y nombre conservados | CA-03 |
| 6 | `400` por archivo inválido | Mensaje; solicita nueva captura | CA-04 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Sin fotografía | Botón deshabilitado y mensaje obligatorio | Capturar | CA-02 |
| Con fotografía | Previsualización y botón habilitado | Confirmar o repetir | CA-01 |
| Enviando | Indicador; controles bloqueados | Esperar | CA-01 |
| Éxito | «Entrega registrada.» | Volver a «Mi Ruta» | CA-01 |
| Error de almacenamiento | Mensaje con datos conservados | «Reintentar» | CA-03 |
| Archivo inválido | Mensaje de formato o tamaño | Capturar de nuevo | CA-04 |
| Sin conexión | «No se registró la entrega.» con datos conservados | «Reintentar» | ES-F03-04 RN-08 |

## 5. Mensajes

| Respuesta | Mensaje | Recuperación |
|---|---|---|
| Éxito | «Entrega registrada.» | — |
| Error o tiempo de espera de almacenamiento | «No se pudo guardar la fotografía. Inténtalo de nuevo.» | «Reintentar» |
| `400` | «La fotografía no cumple el formato o tamaño permitido.» | Capturar de nuevo |
| `409` | «Este despacho ya no puede marcarse como entregado.» | Volver a «Mi Ruta» |

Los textos son propuesta; formatos y límites dependen de DT-01.

## 6. Accesibilidad

- Botón de captura y confirmación con nombre accesible y objetivo táctil amplio.
- Mensaje obligatorio asociado al campo y anunciado a lectores de pantalla.
- Previsualización con texto alternativo.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Abrir sin fotografía | Botón deshabilitado y mensaje visible | CA-02 |
| CUI-02 | Capturar y confirmar | Confirmación de éxito | CA-01 |
| CUI-03 | Simular fallo de almacenamiento | Imagen y nombre conservados; reintento disponible | CA-03 |
| CUI-04 | Recibir `400` | Mensaje y nueva captura | CA-04 |
| CUI-05 | Recorrer con lector de pantalla en móvil | Controles y mensajes anunciados | CA-01 a CA-04 |

## 8. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. Wireframe del formulario de entrega de F-03.
