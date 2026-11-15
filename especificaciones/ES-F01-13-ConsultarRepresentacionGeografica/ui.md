# UI de ES-F01-13: Representación geográfica

## 1. Composición e interacción

Reutilizar ShellAdministrativo, EncabezadoPagina, EstadoVista y Mantine según [sistema de diseño](../../disenio/SYSTEM-DESIGN.md). Distritos conserva su formulario/listado y añade vista Mapa, búsqueda/estado, leyenda textual y lista accesible de selección/centrado. Ficha con nombre, ubigeo, estado, archivo, procedencia y versión. Indicador explícito «Sin geometría»; si no se declaró archivo, indicar carga directa por API.

## 2. Estados y accesibilidad

Carga diferida con indicador, vacío, error/reintento y acceso denegado sin datos. Activo, inactivo, selección y referencia postal se distinguen por texto y contorno además de color. Móvil apila paneles sin desbordamiento; teclado puede seleccionar/centrar mediante lista. La caída de teselas no elimina límites ni lista.

## 3. Referencia y criterios UI

Maqueta local `01-distritos-mapa.png` del plan backend; sus datos son ilustrativos. CUI-01: filtros/lista/ficha sincronizados. CUI-02: faltantes/errores y permisos. CUI-03: teclado, escritorio y móvil. Resultados en [evidencia](./evidence.md).
