# Plan de ES-F01-10: Registrar un distrito

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión pendiente. **UI:** Aplica.

## 1. Entradas

[Spec](./spec.md), [UI](./ui.md), [Gestión §3.1.1](../../integraciones/api-contract-gestion-despachos.md#311-administración-de-distritos--13112026), [modelo](../../arquitectura/modelo-datos.md) y ES-F01-08, revisión del 13/11/2026 [cite: 1].

## 2. Solución y orden

1. Migración V11 nueva: estado activo inicial, versión y marca del catálogo base; preservar UUID, datos y relaciones.
2. GestionDistritos valida datos y unicidad bajo el mismo bloqueo de configuración de zonas; base impone unicidad normalizada. Registro y auditoría comparten transacción.
3. Formulario con React Hook Form/Zod y campos Mantine dentro del panel unificado; errores por campo y valores conservados. El coordinador notifica, limpia y consulta de nuevo manteniendo filtros, informa registros ocultos y distingue éxito de escritura de fallo posterior de lectura.
4. Coordinar confirmaciones de descarte para limpiar, editar o regresar y aviso de cierre/recarga con pendientes.

## 3. Verificación y cierre

CA-01 a CA-05: altas, geografía, duplicados concurrentes, rechazo de permisos y rollback de auditoría. `./mvnw clean verify`; suites F-01/administrativo, typecheck y build del frontend. No se aplican migraciones a bases compartidas para probar. Revisión humana pendiente.

## 4. Referencias

- [cite: 1] [Spec](./spec.md), [tareas](./tasks.md), [evidencia](./evidence.md).
