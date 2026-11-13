# Plan de ES-F01-09: Consultar distritos

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión pendiente. **UI:** Aplica.

## 1. Entradas

[Spec](./spec.md), [UI](./ui.md), [Gestión §3.1.1](../../integraciones/api-contract-gestion-despachos.md#311-administración-de-distritos--13112026), [modelo](../../arquitectura/modelo-datos.md) y [componentes React](../../disenio/componentes-react.md), revisión de trabajo del 13/11/2026 [cite: 1].

## 2. Solución y orden

1. Extender controlador, puerto y adaptador de distritos en `zonas/`; filtros validados y orden estable.
2. Reutilizar cliente API, ShellAdministrativo y EstadoVista para `features/distritos/PaginaDistritos`.
3. Mantener selector activo por defecto y detalle de zona independiente para asociaciones inactivas.

## 3. Verificación y cierre

CA-01 a CA-04: HTTP con PostgreSQL Testcontainers y componentes con API simulada. Ejecutar `./mvnw clean verify`, `npm run test:f01`, `npm run test:administrativo`, `npm run typecheck` y `npm run build`. Recorrido real por Gateway y navegador en base desechable. Revisión humana pendiente.

## 4. Referencias

- [cite: 1] [Spec](./spec.md), [tareas](./tasks.md), [evidencia](./evidence.md).
