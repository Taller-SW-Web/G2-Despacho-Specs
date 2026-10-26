# UI de ES-F02-05: Consultar y reordenar la secuencia de ruta

**Responsable:** Tarqui.

**Estado:** Implementada y verificada en React y navegador con servicios G2 reales; aceptación humana pendiente. Resultados en evidence.md.

**Precisión vigente (26/10/2026):** se muestran los números de posición persistidos, conservando huecos históricos y paradas fijas conforme a Gestión §3.2.1. Se usa arrastre HTML nativo con alternativa subir/bajar por teclado; no se incorpora una biblioteca DND. La acción de reasignar permanece fuera de esta entrega hasta completar ES-F02-06. Respuesta perdida conserva clave, versión y cuerpo, bloquea descarte/cambio de jornada y ofrece «Recuperar guardado». Conflicto descarta edición y consulta ruta vigente.

**Aplicabilidad:** Pestaña "Rutas por repartidor" dentro del Panel de Programación (`/programacion`).

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- **Usuario:** Gestor de Despacho con rol `GESTOR_DESPACHO`.
- **Contexto:** Panel de control de rutas en centro de distribución. El Gestor supervisa a los repartidores en turno y ajusta el orden óptimo de entrega antes de que inicien sus traslados.
- **Objetivo:** Consultar la lista secuencial de paradas de una jornada, reordenar despachos `ASIGNADO` mediante arrastre o botones subir/bajar, contar con confirmación clara mediante barra fija inferior y disponer de acción "Reasignar" para derivar un paquete a otro conductor (ES-F02-06).
- **Componentes React asociados:** Mantine `Tabs`, Mantine Drag & Drop (`@hello-pangea/dnd` o `@dnd-kit`), `BarraAccionesFija` (CR-13), `TarjetaDespacho` (CR-16), `BadgeEstado` (CR-09), `Button` (CR-01).

## 2. Referencias visuales

- [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md): secciones 14, 16.2, 17, 18 y 21.
- [Diseño F-02](../../disenio/funcionalidades/f-02.md): Pantalla 3 (Rutas por Repartidor - Secuencia de Entrega).
- [Componentes React](../../disenio/componentes-react.md): CR-01, CR-09, CR-13, CR-16, CR-19.

## 3. Pantallas e interacción

### UI-01. Selector superior de jornada / repartidor

- Selector desplegable (`Select`) con la lista de repartidores en turno para hoy (muestra: nombre, placa de furgoneta y resumen de paradas).
- Al seleccionar: carga la ruta del chofer y sus métricas de jornada (total paradas, completadas, pendientes).

### UI-02. Lista secuencial de paradas

- Lista vertical de tarjetas de despacho numeradas correlativamente (`#1`, `#2`, `#3`, ...):
  - **Identificador y estado:** código de rastreo, badge de estado (`ASIGNADO`, `EN_CAMINO`, `ENTREGADO`, `FALLIDO`).
  - **Datos clave:** destinatario, dirección de entrega, peso, volumen y tiempo estimado.
  - **Controles de reordenamiento:**
    - Manija de arrastre (*drag handle*) a la izquierda con icono de seis puntos (`IconGripVertical`).
    - Botones de flecha para subir (`IconChevronUp`) y bajar (`IconChevronDown`) accesibles por teclado.
    - **Regla de bloqueo:** los despachos en `EN_CAMINO`, `ENTREGADO` o `FALLIDO` no tienen manija de arrastre ni botones de flecha; se muestran bloqueados con opacidad sutil y candado.
  - **Acción secundaria:** botón compacto "Reasignar" (solo visible para `ASIGNADO`), que abre el modal de reasignación (ES-F02-06).

### UI-03. Barra inferior de cambios pendientes (CR-13)

- Permanece oculta hasta que el usuario altera la posición de al menos un despacho.
- Al activarse: franja flotante fija en la parte inferior de la ventana (sin cubrir contenido útil ni controles de foco):
  - Texto informativo: *"Hay N cambios sin guardar en la secuencia de ruta"*.
  - Botón secundario `subtle`: "Descartar cambios" (revierte inmediatamente la lista al orden original).
  - Botón primario: "Guardar orden" (envía la mutación al backend mostrando spinner mientras procesa).

### UI-04. Actualización y feedback

- Al confirmar con éxito:
  - Toast de confirmación Mantine: *"Secuencia de ruta actualizada exitosamente"*.
  - La barra fija se oculta.
  - La numeración de paradas `#1..#N` se consolida.

## 4. Criterios de aceptación de interfaz (CUI)

### CUI-01. Visualización ordenada de paradas
- **DADO** un repartidor con despachos asignados.
- **CUANDO** se carga la pestaña de rutas.
- **ENTONCES** las paradas se presentan en orden numérico correlativo con su estado visible y accesible.

### CUI-02. Bloqueo de paradas no reordenables
- **DADO** un despacho en estado `EN_CAMINO`.
- **CUANDO** se visualiza en la lista.
- **ENTONCES** no muestra controles de arrastre ni flechas, y el usuario no puede cambiar su posición en la ruta.

### CUI-03. Activación y descarte en barra fija de cambios
- **DADO** que el usuario mueve una parada `ASIGNADO`.
- **CUANDO** suelta la tarjeta en una nueva posición.
- **ENTONCES** aparece la barra inferior fija; al pulsar "Descartar", la lista vuelve al orden previo y la barra desaparece.

### CUI-04. Accesibilidad por teclado en reordenamiento
- **DADO** un usuario navegando exclusivamente con teclado.
- **CUANDO** enfoca los botones subir/bajar de una tarjeta.
- **ENTONCES** puede presionar `Enter` o `Espacio` para intercambiar la posición del despacho de forma accesible.

### CUI-05. Guardado exitoso y feedback
- **DADO** que existen cambios pendientes en la secuencia.
- **CUANDO** el usuario pulsa "Guardar orden".
- **ENTONCES** el botón muestra spinner y tras recibir 200 OK se emite toast de confirmación y se oculta la barra de cambios.
