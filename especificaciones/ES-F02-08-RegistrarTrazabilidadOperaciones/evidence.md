# Evidencia de ES-F02-08: Registrar la trazabilidad de las operaciones

**Estado:** Auditoría y protección UPDATE/DELETE de Flyway V8 verificadas con PostgreSQL desechable. Revisión de privilegios reales de despliegue pendiente.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

### Incremento del 30/10/2026

- Reejecución posterior con Docker disponible: Gestión `clean verify` **194 pruebas aprobadas**, sin fallos/errores/omitidas. Se verificaron V8, rechazo JDBC de UPDATE/DELETE, conservación del contenido y regresiones de rollback/cierre. El bloqueo de Docker del primer intento quedó resuelto; CA-06 conserva pendiente la comprobación del rol real de ejecución sin propiedad, DDL/TRUNCATE ni superusuario.

- `feature/f02-cierre-criterios`, desde backend `develop` `e4f8ee1`, sin commit/push de esta ejecución. V8 agrega trigger contra UPDATE/DELETE y revoca mutación/TRUNCATE públicos.
- `ProgramacionHttpTests.historialRechazaUpdateYDeleteInclusoDesdeJdbc` comprueba escrituras directas rechazadas y contenido intacto. Las pruebas previas de corrupción de metadatos se conservan: solo su preparación en PostgreSQL desechable desactiva temporalmente el trigger con privilegio de DBA, restableciéndolo en `finally`.
- `clean verify` no pudo verificar PostgreSQL por ausencia de daemon Docker. CA-06 no se cierra: falta ejecutar esta regresión y comprobar rol real de aplicación no propietario, sin DDL/TRUNCATE/superusuario. Un DBA puede alterar triggers; no se promete protección contra ese actor.
- Las auditorías de rutas, reasignación y cancelación están implementadas en backend integrado; no es necesario crear un segundo servicio/tabla para volver a registrarlas. La matriz histórica siguiente requiere reconciliación con los reportes al ejecutar la regresión completa.

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
