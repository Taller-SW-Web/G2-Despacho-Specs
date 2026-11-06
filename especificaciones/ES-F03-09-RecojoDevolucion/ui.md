# UI de ES-F03-09: Recojo de una devolución en el domicilio

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** «Mi Ruta», detalle del recojo, formularios de recojo y no recojo, y resumen de jornada.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario y permisos: repartidor en turno, propietario del recojo.
- Contexto de uso: en la calle, desde el celular y con una mano.
- Objetivo visible: saber qué recoger y dónde, registrar el resultado y recordar llevar el producto al centro.
- Acceso y navegación: «Mi Ruta» → detalle del recojo → formulario → confirmación → «Mi Ruta».

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| Diseño visual compartido | [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | Campos, botones, etiquetas y avisos |
| Diseño de F-03 | [f-03](../../disenio/funcionalidades/f-03.md) y [alta fidelidad](../../disenio/SystemDesign/f-03-alta-fidelidad.md) | Se reutiliza la composición de ruta, detalle, entrega y fallo; aún no hay diseño propio del recojo |
| Componentes React compartidos | [componentes-react.md](../../disenio/componentes-react.md) | Componentes aplicables |

## 3. Pantallas e interacción

### UI-01. Recojo en «Mi Ruta»

Tarjeta en la misma lista de los despachos, en su posición de la secuencia, con la etiqueta «Recojo», dirección, contacto y estado.

### UI-02. Detalle del recojo

| Elemento | Contenido y comportamiento |
|---|---|
| Datos | Dirección, referencia, contacto con llamada directa, fecha y código |
| Productos | Lista de SKU y cantidades que debe recoger |
| Acción en `ASIGNADO` | «En camino» |
| Acciones en `EN_CAMINO` | «Registrar recojo» y «No se pudo recoger» |
| Estados `RECOGIDO` y `FALLIDO` | Solo lectura, sin teléfono ni dirección |

### UI-03. Formulario de recojo

| Elemento | Contenido y comportamiento |
|---|---|
| Fotografía | Captura, vista previa y opción de repetir; obligatoria |
| Comentario | Texto opcional |
| «Confirmar recojo» | Deshabilitado sin foto; evita doble envío |

### UI-04. Formulario de no recojo

| Elemento | Contenido y comportamiento |
|---|---|
| Motivo | Selector obligatorio con motivos de ámbito `RECOJO` o `AMBOS` |
| Fotografía | Obligatoria |
| Comentario | Texto opcional |
| «Confirmar» | Bloquea el envío si falta motivo o foto |

### UI-05. Resumen de jornada

Añade recojos realizados, recojos no realizados y la lista «Productos por entregar en el centro».

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Abrir «Mi Ruta» | Recojo con su etiqueta | CA-01 |
| 2 | Pulsar «En camino» | Estado actualizado sin recargar toda la vista | CA-02 |
| 3 | Confirmar con foto | Recordatorio de llevar el producto al centro | CA-03 |
| 4 | Confirmar sin foto o sin motivo | Envío bloqueado y campo resaltado | CA-04, CA-06 |
| 5 | Registrar el no recojo | «Recojo no realizado» y regreso a la ruta | CA-05 |
| 6 | Perder la señal | Datos conservados y «Reintentar» | CA-08 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Cargando | Indicador | Esperar | CA-01 |
| Incompleto | Campos obligatorios resaltados | Completar | CA-04, CA-06 |
| Enviando | Controles bloqueados | Esperar | CA-03, CA-05 |
| Éxito | Confirmación y recordatorio cuando corresponde | Volver a «Mi Ruta» | CA-03, CA-05 |
| Recojo actualizado | Aviso de cambio | Actualizar la ruta | CA-07 |
| Sin conexión | Aviso con datos conservados | «Reintentar» | CA-08 |
| Error de evidencia | Igual que ES-F03-05 | Reintentar o tomar otra foto | RN-05 |

## 5. Formularios y mensajes

| Campo | Obligatorio | Validación | Mensaje |
|---|---|---|---|
| Fotografía | Sí | Antes de enviar | «Agrega una foto para continuar.» |
| Motivo | Sí, en no recojo | Antes de enviar | «Selecciona un motivo.» |
| Comentario | No | Hasta 200 caracteres | «Máximo 200 caracteres.» |

| Resultado | Mensaje | Recuperación |
|---|---|---|
| Recojo registrado | «Recojo registrado. Lleva el producto al centro de despacho.» | — |
| No recojo registrado | «Recojo no realizado. El Gestor decidirá el siguiente paso.» | — |
| `409` | «Este recojo cambió. Actualizamos tu ruta.» | Volver a «Mi Ruta» |
| Sin conexión | «No se registró el cambio. Revisa tu señal e inténtalo de nuevo.» | «Reintentar» |

Los textos son propuesta.

## 6. Accesibilidad y adaptación

- Campos con etiqueta visible; errores asociados y anunciados.
- La etiqueta «Recojo» usa texto, no solo color.
- Objetivos táctiles de al menos 44 × 44 px y contraste suficiente bajo luz solar.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Ruta con despachos y un recojo | Recojo en su posición, con etiqueta | CA-01 |
| CUI-02 | Recojo en cada estado | Acciones y datos correctos para ese estado | CA-02, CA-03, CA-05 |
| CUI-03 | Confirmar sin foto o sin motivo | Envío bloqueado | CA-04, CA-06 |
| CUI-04 | Registrar el recojo | Recordatorio visible | CA-03 |
| CUI-05 | Simular falta de señal | Datos conservados y reintento | CA-08 |
| CUI-06 | Abrir el resumen con un recojo `RECOGIDO` | Producto listado por entregar | CA-10 |
| CUI-07 | Recorrer con lector de pantalla en móvil | Controles y errores anunciados | CA-01 a CA-06 |

- Pendientes de diseño: frames de Figma del recojo (DT-05 del plan).
- Evidencia prevista: pruebas de interacción y capturas de estados.

## 8. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Contrato de Operación §3.7](../../integraciones/api-contract-operacion-reparto.md#37-recojo-de-una-devolución).
