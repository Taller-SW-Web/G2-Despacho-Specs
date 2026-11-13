# Plan de ES-F01-11: Editar un distrito

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión pendiente. **UI:** Aplica.

## 1. Entradas

[Spec](./spec.md), [UI](./ui.md), [Gestión §3.1.1](../../integraciones/api-contract-gestion-despachos.md#311-administración-de-distritos--13112026) y [modelo](../../arquitectura/modelo-datos.md), revisión del 13/11/2026 [cite: 1].

## 2. Solución y orden

1. Añadir versión JPA en V11 y comprobar la versión presentada antes de escribir.
2. Serializar identidad/asociaciones con el bloqueo compartido de configuración. Consultar tanto asociaciones distritales como postales, incluyendo zonas inactivas. No auditar ediciones sin cambios.
3. Precargar detalle, bloquear nombre/ubigeo según `identidadEditable` y presentar el motivo. Conflictos no renuevan automáticamente la versión; ofrecer revisión conservando los datos.

## 3. Verificación y cierre

CA-01 a CA-05: integración PostgreSQL de protección, versión y rollback; componentes de restricciones y errores. Ejecutar las suites completas de Gestión y administrativo, typecheck y build. Revisión humana pendiente.

## 4. Referencias

- [cite: 1] [Spec](./spec.md), [tareas](./tasks.md), [evidencia](./evidence.md).
