# Plan de ES-F01-15

## 1. Solución

Migración nueva con metadatos, propuestas e histórico. Reutilizar ComandosConfiguracion y bloqueo de configuración; comprobar versiones dentro de la transacción. Guardar el resultado idempotente junto al negocio y auditoría. Consumidor solo envía identidad de validación, nunca geometría modificada. Leer [spec](./spec.md), [UI](./ui.md) y contrato.

## 2. Verificación

HTTP/PostGIS con Testcontainers: primera carga, multipartes/huecos, reemplazo, auditoría, rollback, expiración, reintentos y concurrencia. Regresión de cotización con Productos y reloj controlados. Suites completas y navegador por Gateway aislado; distinguir simulaciones y aceptación humana en [evidencia](./evidence.md).
