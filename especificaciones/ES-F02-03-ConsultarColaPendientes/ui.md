# UI de ES-F02-03: Consultar la cola de despachos pendientes

**Responsable:** Tarqui.

**Estado:** Especificación de UI preparada el 16/10/2026; implementación pendiente.

**Aplicabilidad:** Página completa administrativa en la ruta `/programacion` (pestaña "Cola de pendientes").

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- **Usuario:** Gestor de Despacho con rol `GESTOR_DESPACHO`.
- **Contexto:** Trabajo continuo en centro de distribución; pantalla principal de escritorio (1440 × 1024 px) con adaptación a tableta (1024 × 768 px).
- **Objetivo:** Consultar la cola de paquetes pendientes, filtrar por zona/fecha/intento, supervisar los indicadores KPI y pulsar "Asignar" para abrir el modal de asignación de carga.
- **Componentes React asociados:** Mantine `Tabs`, `Table` (CR-07 TablaDatos), `Card` (CR-10 TarjetaKpi), `TextInput` / `Select` / `Chip.Group` (CR-06 BarraFiltros), `Badge` (CR-09 BadgeEstado), `EstadoVista` (CR-08).

## 2. Referencias visuales

- [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md): secciones 12.3, 16.2, 17, 18 y 21.
- [Diseño F-02](../../disenio/funcionalidades/f-02.md): Pantalla 1 (Panel de Programación - Cola de Pendientes).
- [Componentes React](../../disenio/componentes-react.md): CR-03, CR-05, CR-06, CR-07, CR-08, CR-09, CR-10.

## 3. Pantallas e interacción

### UI-01. Estructura general de la vista

- **Encabezado:** H1 "Programación y asignación", con botón secundario "Generar pedido de prueba" a la derecha (ES-F02-02).
- **Pestañas superiores (`Tabs`):**
  - "Cola de pendientes" (activa por omisión, con badge de conteo de pendientes).
  - "Rutas por repartidor" (enlace a ES-F02-05).
- **Tarjetas KPI interactivas (CR-10):**
  - "Pendientes para hoy": muestra el total programado para hoy o días anteriores. Al hacer clic, filtra la tabla mostrando solo pendientes de hoy.
  - "Programados a futuro": total reprogramado con fecha posterior a hoy. Al hacer clic, filtra mostrando despachos futuros.
  - "Reintentos": total de despachos con reprogramaciones previas. Al hacer clic, activa el filtro de reintentos.
  - Cada tarjeta seleccionada se resalta visualmente; un segundo clic retira el filtro rápido.
- **Barra de filtros (CR-06):**
  - Selector de rango de fechas (`DatePickerInput`).
  - Selector de Zona de cobertura (`Select` con zonas activas).
  - Selector de intentos (`Chip.Group`: "Todos", "Primer intento", "Reintentos").
  - Botón "Limpiar filtros": restablece todos los selectores y regresa a la página 1.
- **Tabla de datos (CR-07):**
  - Columnas: Código de rastreo (con `idPedido` debajo), Zona, Dirección (truncada con tooltip), Peso (kg), Volumen (m³), Paquetes (unidades físicas), Fecha programada, Intento (ej. "1 de 2" o badge "Reintento"), Tiempo en espera (ícono de alerta si excede 4 horas) y Acción ("Asignar").
  - En tableta (1024 × 768 px): se ocultan las columnas secundarias ("Pedido", "Volumen" y "Tiempo en espera"), visibles en el modal de asignación.
- **Paginador:** selector de tamaño de página (10, 20, 50, 100) y botones de navegación previa/siguiente.

### UI-02. Estados de la interfaz

- **Carga inicial (`loading`):** skeleton loader simulando las filas de la tabla (CR-08).
- **Estado vacío:** ilustración o icono neutral con el texto "No hay despachos pendientes de asignación" y botón centrado "Generar pedido de prueba".
- **Sin resultados por filtro:** texto "No se encontraron despachos con los filtros aplicados" y botón "Limpiar filtros".
- **Error de servidor o red:** alerta Mantine con mensaje explicativo y botón "Reintentar consulta".
- **Acceso denegado (403):** pantalla completa de acceso denegado (CR-08) sin exponer filas ni contadores.

## 4. Criterios de aceptación de interfaz (CUI)

### CUI-01. Despliegue de datos y columnas completas
- **DADO** un gestor autenticado que accede a `/programacion`.
- **CUANDO** la tabla carga exitosamente.
- **ENTONCES** se visualizan las columnas completas incluyendo peso, volumen y cantidad física de paquetes, con formato y alineación adecuados.

### CUI-02. Interacción con tarjetas KPI
- **DADO** que se muestran las tarjetas KPI con sus contadores.
- **CUANDO** el usuario pulsa la tarjeta "Reintentos".
- **ENTONCES** la tabla se filtra automáticamente mostrando únicamente despachos con reprogramaciones previas y la tarjeta adopta el estado activo.

### CUI-03. Restricción visual de fecha futura
- **DADO** un despacho con fecha programada posterior al día actual.
- **CUANDO** se renderiza la fila correspondiente.
- **ENTONCES** muestra el distintivo "Programado para [fecha]" y el botón "Asignar" aparece deshabilitado con tooltip explicativo.

### CUI-04. Distintivo de simulación
- **DADO** un despacho con `esSimulacion = true`.
- **CUANDO** aparece en la tabla.
- **ENTONCES** exhibe el badge con borde punteado "Simulado".

### CUI-05. Paginación y URL synchronization
- **DADO** que el usuario cambia de página o aplica filtros.
- **CUANDO** se actualiza la vista.
- **ENTONCES** los parámetros `pagina`, `zona`, `tipoIntento` se reflejan en los query params de la URL para permitir compartir o recargar la vista.

### CUI-06. Accesibilidad y responsive
- **DADO** un dispositivo con ancho de pantalla de 1024 px (tableta).
- **CUANDO** se visualiza la tabla.
- **ENTONCES** la barra lateral se colapsa a iconos y las columnas secundarias se ocultan sin desbordamiento horizontal.
