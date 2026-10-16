# UI de ES-F02-04: Asignar despacho a un repartidor

**Responsable:** Tarqui.

**Estado:** Especificación de UI preparada el 16/10/2026; implementación pendiente.

**Aplicabilidad:** Modal interactivo de asignación invocado desde la cola de pendientes (`/programacion`).

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- **Usuario:** Gestor de Despacho con rol `GESTOR_DESPACHO`.
- **Contexto:** Modal centrado que se abre sobre la pantalla de Programación al hacer clic en el botón "Asignar" de una fila pendiente habilitada para hoy.
- **Objetivo:** Visualizar el resumen de carga del despacho, revisar el catálogo de repartidores en jornada agrupados por zona (priorizando los de la zona de entrega), evaluar la proyección de las barras tridimensionales de ocupación y confirmar la asignación con un clic.
- **Componentes React asociados:** Mantine `Modal` (CR-12), `Card` de Repartidor (CR-20 TarjetaRepartidor), `Progress` tridimensional (CR-11 BarraOcupacion), `Textarea` (CR-02 CamposFormulario), `Button` (CR-01 AccionesUi), `NotificacionOperacion` (CR-15).

## 2. Referencias visuales

- [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md): secciones 13.4, 16.4, 17, 18 y 21.
- [Diseño F-02](../../disenio/funcionalidades/f-02.md): Pantalla 2 (Modal de Asignación de Despacho a Repartidor).
- [Componentes React](../../disenio/componentes-react.md): CR-01, CR-02, CR-11, CR-12, CR-15, CR-20.

## 3. Pantallas e interacción

### UI-01. Resumen superior del despacho

- Muestra tarjeta compacta con:
  - Código de rastreo (destacado) y pedido.
  - Dirección completa y zona resuelta.
  - Tres píldoras de carga: **Peso:** `X.X kg`, **Volumen:** `X.XXX m³`, **Paquetes:** `N bultos`.

### UI-02. Catálogo de repartidores y proyección de carga

- Lista o tarjetas de repartidores en jornada (CR-20):
  - **Agrupación:** primero los repartidores asignados a la misma zona del despacho; luego los repartidores de otras zonas disponibles.
  - **Detalle de cada repartidor:** nombre del chofer, placa de furgoneta, zona habitual y estado operativo (`DISPONIBLE` o `EN_RUTA`).
  - **Tres barras de ocupación simultáneas (CR-11):**
    1. Peso: `ocupado / límite kg` (`%`).
    2. Volumen: `ocupado / límite m³` (`%`).
    3. Paquetes: `ocupado / límite paquetes` (`%`).
  - **Proyección de carga:** al pasar el cursor o seleccionar un repartidor, la porción que sumaría el despacho se visualiza con un rayado diagonal o color diferenciado sobre la barra.
  - **Indicador de sobrecarga:** si el despacho excede cualquiera de los tres límites, la barra correspondiente se pinta en rojo, se muestra badge "Sobrecarga" y la tarjeta queda deshabilitada para selección con tooltip explicativo.

### UI-03. Formulario y confirmación

- Campo de texto opcional: "Instrucciones u observaciones de entrega" (`Textarea`, máx. 250 caracteres).
- Botones de pie de modal:
  - "Cancelar": cierra el modal sin alterar datos.
  - "Confirmar asignación": botón primario Mantine. Deshabilitado si no hay repartidor seleccionado o si el repartidor seleccionado sobrepasa la capacidad. Al pulsar, muestra spinner (`loading`) para impedir doble clic (CCR-01-01).

### UI-04. Feedback y actualización de la vista

- Éxito (HTTP 200):
  - Toast de confirmación: *"Despacho asignado al repartidor [Nombre] (Parada #N)"*.
  - El modal se cierra automáticamente.
  - El despacho desaparece de la tabla de pendientes y el contador KPI de hoy se actualiza.
- Conflicto (HTTP 409):
  - Modal muestra alerta: *"El despacho ya fue asignado o el repartidor cambió de estado"*. Se ofrece botón "Cerrar y recargar cola".

## 4. Criterios de aceptación de interfaz (CUI)

### CUI-01. Apertura con datos del despacho
- **DADO** un gestor en la cola de pendientes.
- **CUANDO** pulsa el botón "Asignar" de un despacho programado para hoy.
- **ENTONCES** se abre el modal mostrando el código de rastreo, dirección, peso, volumen y cantidad física de paquetes.

### CUI-02. Agrupación inteligente de repartidores
- **DADO** un despacho con destino en "Lima Centro".
- **CUANDO** se despliega el listado de repartidores.
- **ENTONCES** aparecen agrupados en primer lugar los repartidores cuya zona operativa sea "Lima Centro", seguidos de los de otras zonas.

### CUI-03. Proyección visual de barras de capacidad
- **DADO** un repartidor seleccionado con 70% de peso y 50% de volumen.
- **CUANDO** se selecciona para el despacho.
- **ENTONCES** las tres barras reflejan la proyección sumando la carga del paquete con sombreado diferenciado.

### CUI-04. Bloqueo visual por sobrecarga tridimensional
- **DADO** un repartidor con capacidad libre de 1 paquete, y un despacho de 2 paquetes.
- **CUANDO** se renderiza la tarjeta del repartidor.
- **ENTONCES** la barra de paquetes se marca en sobrecarga, la tarjeta queda bloqueada para selección y el botón "Confirmar" permanece deshabilitado.

### CUI-05. Prevención de doble confirmación
- **DADO** que el usuario hace clic en "Confirmar asignación".
- **CUANDO** la petición HTTP se envía.
- **ENTONCES** el botón entra en estado de carga con spinner y no permite nuevos clics hasta recibir respuesta.

### CUI-06. Cierre y actualización tras éxito
- **DADO** que el backend confirma la asignación.
- **CUANDO** la respuesta es procesada.
- **ENTONCES** el modal se cierra, se emite toast de éxito y la tabla de pendientes remueve el registro.
