# Plan de ES-F01-14

## 1. Solución

Validación estructural acotada antes de PostGIS, correspondencias explícitas por índice y catálogo propio. Guardar propuestas válidas con propietario, expiración, geometrías y versiones. Proceso reproducible de exportación con manifiesto de procedencia fuera de migraciones. Leer [spec](./spec.md) y [UI](./ui.md).

## 2. Verificación

Testcontainers PostGIS, límites por HTTP/Gateway, geometrías con huecos y partes separadas, desconocidos/duplicados y sugerencias. Componentes con API simulada; navegador con servicios reales locales. Maven `clean verify`, suites frontend, typecheck y build. [Evidencia](./evidence.md).
