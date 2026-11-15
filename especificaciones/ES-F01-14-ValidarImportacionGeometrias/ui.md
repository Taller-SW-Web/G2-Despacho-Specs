# UI de ES-F01-14: Validación geográfica

## 1. Flujo y componentes

Acción «Importar geometrías» en Distritos, modal responsive con selector GeoJSON, fuente y versión obligatorias. Mostrar cantidad de entidades, tamaño, correspondencias por ubigeo y sugerencias con selector explícito del catálogo. Validar mediante backend y mostrar errores por entidad, resumen de primeras cargas/reemplazos y mapa comparativo actual/propuesto. Cambiar archivo/fuente/versión/correspondencias invalida el informe anterior.

## 2. Estados y criterios UI

CUI-01: lectura inválida muestra mensaje y permite corregir. CUI-02: sugerencia nunca se confirma automáticamente. CUI-03: informe inválido deshabilita confirmación y mantiene entradas. CUI-04: error de red permite reintentar; 401/403 retira datos. CUI-05: foco/modal, teclado y móvil. Reutilizar controles Mantine y EstadoVista según [diseño](../../disenio/SYSTEM-DESIGN.md). Maquetas 03/04/06 del plan backend.
