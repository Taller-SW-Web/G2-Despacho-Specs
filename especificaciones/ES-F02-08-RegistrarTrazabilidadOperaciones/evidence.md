# Evidencia de ES-F02-08: Registrar la trazabilidad de las operaciones

**Estado:** Recepción, simulación, asignación, reordenamiento, reasignación y cancelación auditados. Inmutabilidad integral pendiente.

**Avance del 26/10/2026:** `RutasHttpTests` verifica historial de cada parada modificada con secuencias anterior/nueva, actor, UTC y jornada; una excepción inducida al insertar historial revierte posiciones, versiones, resultado durable y outbox. Repetir el guardado no duplica historial ni proyecciones. La suite completa de Gestión terminó con 164 pruebas aprobadas y sin omitidas en esta ejecución. No se declara cerrado CA-06: todavía falta demostrar inmutabilidad integral de toda la tabla, además del rollback comprobado.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** 26/10/2026 para cancelación/historial/outbox/rollback; inmutabilidad integral pendiente.

**Incremento de cancelación:** `CancelacionHttpTests` verifica historial de `CANCELACION_POR_ANULACION` con servicio emisor, motivo, UTC y referencias operativas. Los fallos inducidos al guardar historial, outbox, estado o resultado revierten la confirmación local y conservan el cerco si F-06 ya liberó. Reintentar no duplica auditoría ni evento; la marca en `FALLIDO` se registra sin transición comercial. Gestión terminó con **188 pruebas aprobadas**. Detalle y límites en [ES-F02-07](../ES-F02-07-CancelarDespachoPorAnulacion/evidence.md); esto no cierra CA-06.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-04, CA-10; RT-02).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2).
- Commits de implementación y entorno de pruebas: pendientes.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-04, T-05 | Registro atómico de auditoría en recepción y simulación. | EV-01 | No ejecutado |
| CA-02 | T-03, T-04, T-05 | Registro atómico de auditoría en asignación con operador, jornada y balances. | EV-01 | No ejecutado |
| CA-03 | T-03, T-04, T-05 | Registro atómico de auditoría en reordenamiento de ruta con secuencia. | RutasHttpTests; EV-01 de ES-F02-05 | Aprobado localmente el 26/10/2026 |
| CA-04 | T-03, T-04, T-05 | Historial REASIGNACION, ambos repartidores/jornadas/reservas, motivo y remanente; rollback e idempotencia. | ReasignacionHttpTests; ES-F02-06 EV-01 | Aprobado localmente el 26/10/2026 |
| CA-05 | T-03, T-04, T-05 | Historial de cancelación/marca con servicio emisor, motivo, UTC y liberación; rollback e idempotencia. | CancelacionHttpTests; ES-F02-07 EV-01 | Aprobado localmente el 26/10/2026 |
| CA-06 | T-02, T-05 | Inmutabilidad de la tabla e integridad transaccional (rollback si falla auditoría). | EV-01 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración de persistencia de auditoría y rollback
- Tareas asociadas: T-01 a T-05.
- Comando previsto: `./mvnw test -Dtest=AuditoriaServiceTest`
- Resultado: **No ejecutado**.
