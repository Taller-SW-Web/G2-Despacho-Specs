# Evidencia de ES-F02-07: Cancelar despacho por anulación del pedido

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-08, CA-17, CA-18, CA-19).
- Contratos asociados: `integraciones/api-contract.md` (§7.2) y `integraciones/api-contract-operacion-reparto.md` (§5.1).
- Commits de implementación y entorno de pruebas: pendientes.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-06 | Cancelación exitosa de despacho PENDIENTE_ASIGNACION transicionando a CANCELADO. | EV-01 | No ejecutado |
| CA-02 | T-03, T-04, T-06 | Cancelación exitosa de despacho ASIGNADO liberando capacidad en F-06. | EV-01 | No ejecutado |
| CA-03 | T-03, T-06 | Cancelación de despacho FALLIDO responde 202 y setea pedidoAnulado=true. | EV-01 | No ejecutado |
| CA-04 | T-03, T-06 | Rechazo con 409 Conflict si el despacho se encuentra en EN_CAMINO. | EV-01 | No ejecutado |
| CA-05 | T-03, T-06 | Rechazo con 409 Conflict si el despacho ya está cerrado (ENTREGADO/DEVUELTO). | EV-01 | No ejecutado |
| CA-06 | T-05, T-06 | Petición repetida con la misma Idempotency-Key responde idénticamente sin duplicar. | EV-01 | No ejecutado |
| CA-07 | T-02, T-06 | Petición sin token o sin scope despachos:cancelar rechazada con 401/403. | EV-01 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración del caso de uso de cancelación
- Tareas asociadas: T-01 a T-06.
- Comando previsto: `./mvnw test -Dtest=CancelacionDespachoControllerTest`
- Resultado: **No ejecutado**.
