# Evidencia de ES-F02-04: Asignar despacho a un repartidor

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-03, RF-06; CA-06 a CA-09).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2) y `integraciones/api-contract-operacion-reparto.md` (§5.1).
- Commits de implementación y entorno de pruebas: pendientes.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-03, T-05, T-06 | Asignación exitosa con reserva tridimensional en F-06 y estado ASIGNADO con secuencia. | EV-01, EV-03 | No ejecutado |
| CA-02 | T-02, T-06 | Rechazo con 422 ante capacidad excedida en peso, volumen o paquetes. | EV-01 | No ejecutado |
| CA-03 | T-02, T-06 | Rechazo con 409 ante repartidor no habilitado (fuera de turno o saturado). | EV-01 | No ejecutado |
| CA-04 | T-03, T-06 | Rechazo con 409 por colisión de versión optimista ante asignación concurrente. | EV-01 | No ejecutado |
| CA-05 | T-03, T-06 | Rechazo con 409 al intentar asignar despacho con fecha programada futura. | EV-01 | No ejecutado |
| CA-06 | T-02, T-06 | Rechazo con 409 si la reserva previa de un reprogramado no se ha liberado. | EV-01 | No ejecutado |
| CA-07 | T-05, T-06 | Petición sin rol GESTOR_DESPACHO rechazada con 403 Forbidden. | EV-01 | No ejecutado |
| CUI-01 | T-07 | Modal muestra datos de carga completos del despacho al abrirse. | EV-02 | No ejecutado |
| CUI-02 | T-07 | Repartidores agrupados priorizando los de la zona de destino. | EV-02 | No ejecutado |
| CUI-03 | T-07 | Proyección sombreada en barras de capacidad al seleccionar repartidor. | EV-02 | No ejecutado |
| CUI-04 | T-07 | Bloqueo visual de tarjeta y botón de confirmación ante sobrecarga. | EV-02 | No ejecutado |
| CUI-05 | T-07 | Spinner en botón "Confirmar" impidiendo dobles clics. | EV-02 | No ejecutado |
| CUI-06 | T-08 | Cierre de modal, toast emitido y retiro de la cola tras asignación exitosa. | EV-02, EV-03 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración del caso de uso de asignación
- Tareas asociadas: T-02, T-03, T-04, T-05, T-06.
- Comando previsto: `./mvnw test -Dtest=AsignarDespachoIntegrationTest`
- Resultado: **No ejecutado**.

### EV-02. Pruebas de componentes React del modal de asignación
- Tareas asociadas: T-07, T-08.
- Comando previsto: `npm run test -- ModalAsignacionDespacho.test.tsx`
- Resultado: **No ejecutado**.

### EV-03. Pruebas de flujo E2E
- Tareas asociadas: T-06, T-08.
- Comando previsto: `npx playwright test tests/e2e/asignacion-despacho.spec.ts`
- Resultado: **No ejecutado**.
