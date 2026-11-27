# Plan de ES-F02-09

## 1. Solución

- Backend: caso de uso `AdelantarDespacho`, puerto de almacenamiento y adaptación transaccional. Reutilizar `claves_idempotencia` e historial existentes; no requiere migración de esquema.
- Serializar por clave de comando y despacho; comprobar versión y cercos durables de asignación/cancelación. Fecha y auditoría `ADELANTO_PROGRAMACION` se confirman con la respuesta recuperable en la misma transacción.
- API: seguir el [contrato canónico](../../integraciones/api-contract-gestion-despachos.md#323-adelantar-un-despacho-a-hoy). Conservar la protección del gestor y el enrutamiento genérico del gateway.
- Frontend: acción de fila y modal local Mantine, cliente API existente y validación de respuesta; mantener clave, versión y motivo ante resultado incierto. No instalar dependencias.
- No publicar eventos durante el adelanto. Probar regresión de asignación posterior y no modificar el transporte de progreso.

## 2. Verificación

Pruebas de reglas, formato, permisos, idempotencia, auditoría, rollback y eventos con PostgreSQL Testcontainers desechable. `./mvnw clean verify` en Gestión. Frontend: pruebas F-02/administración, typecheck, build y navegador con APIs simuladas; distinguirlas de integración real y aceptación humana.
