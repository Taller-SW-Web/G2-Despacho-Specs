# Plan de ES-F01-12: Activar o desactivar un distrito

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión pendiente. **UI:** Aplica.

## 1. Entradas

[Spec](./spec.md), [UI](./ui.md), [Gestión §3.1.1](../../integraciones/api-contract-gestion-despachos.md#311-administración-de-distritos--13112026), ES-F01-02/05/06/07/08 y ES-F02-01/02, revisión del 13/11/2026 [cite: 1].

## 2. Solución y orden

1. DELETE y PATCH comparten GestionDistritos.cambiarEstado; no-op sin auditoría ni incremento.
2. ZonasAdaptadorJpa rechaza distrito informado inactivo antes del respaldo postal; ambas consultas JPA exigen distrito activo. Todos los consumidores usan esa resolución.
3. GestionZonas permite conservar/retirar asociaciones inactivas existentes, pero no ampliarlas. Exponer estado en detalle. Simulación filtra activos antes del LIMIT de elección de cobertura.
4. Modal de confirmación, actualización del catálogo y adaptación del formulario de zonas sin pérdida de selecciones ni de `soloCodigosPostales`.

## 3. Verificación y cierre

CA-01 a CA-08: recorrido de San Borja con reloj/productos controlados, códigos propios/ajenos, histórico y cero llamadas al quedar sin cobertura; recepción idempotente, simulación y reprogramación. `./mvnw clean verify`; suites F-01/administrativo, typecheck y build. Gateway/navegador en entorno desechable; revisión humana pendiente.

## 4. Referencias

- [cite: 1] [Spec](./spec.md), [tareas](./tasks.md), [evidencia](./evidence.md).
