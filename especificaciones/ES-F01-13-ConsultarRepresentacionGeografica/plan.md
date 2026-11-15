# Plan de ES-F01-13

## 1. Solución

Leer [spec](./spec.md), [UI](./ui.md) y contrato referenciado. Adaptador JDBC/PostGIS de Gestión genera capas derivadas; React Leaflet diferido consume por Gateway. El proveedor de teselas es configurable y conserva atribución. No serializar entidades JPA ni incorporar geometrías a cotización.

## 2. Verificación

HTTP/PostGIS con Testcontainers para CA-01/03 y composición postal CA-02; componentes con APIs simuladas para recuperación CA-04. Navegador real aislado para layout/teclado. Ejecutar Maven `clean verify`, suites administrativas, typecheck y build. [Tareas](./tasks.md), [evidencia](./evidence.md).
