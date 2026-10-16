# Evidencia de ES-F02-08: Registrar la trazabilidad de las operaciones

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

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
| CA-03 | T-03, T-04, T-05 | Registro atómico de auditoría en reordenamiento de ruta con secuencia. | EV-01 | No ejecutado |
| CA-04 | T-03, T-04, T-05 | Registro atómico de auditoría en reasignación con ambos choferes y motivo. | EV-01 | No ejecutado |
| CA-05 | T-03, T-04, T-05 | Registro atómico de auditoría en cancelación comercial desde Ventas. | EV-01 | No ejecutado |
| CA-06 | T-02, T-05 | Inmutabilidad de la tabla e integridad transaccional (rollback si falla auditoría). | EV-01 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración de persistencia de auditoría y rollback
- Tareas asociadas: T-01 a T-05.
- Comando previsto: `./mvnw test -Dtest=AuditoriaServiceTest`
- Resultado: **No ejecutado**.
