# Evidencia de ES-F02-06: Reasignar despacho a otro repartidor

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-07, CA-15, CA-16).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2) y `integraciones/api-contract-operacion-reparto.md` (§5.1).
- Commits de implementación y entorno de pruebas: pendientes.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-03, T-04, T-05 | Reasignación exitosa de despacho ASIGNADO con motivo, cambio de chofer y ajuste en F-06. | EV-01, EV-03 | No ejecutado |
| CA-02 | T-04, T-05 | Rechazo con 400 Bad Request si el motivo está vacío o si se elige al mismo chofer. | EV-01 | No ejecutado |
| CA-03 | T-02, T-05 | Rechazo con 422 si el nuevo repartidor no tiene capacidad suficiente. | EV-01 | No ejecutado |
| CA-04 | T-03, T-05 | Rechazo con 409 si el despacho se encuentra en EN_CAMINO, ENTREGADO o FALLIDO. | EV-01 | No ejecutado |
| CA-05 | T-02, T-05 | Rechazo con 409 si el nuevo chofer se encuentra saturado o fuera de turno. | EV-01 | No ejecutado |
| CA-06 | T-03, T-05 | Rechazo con 409 ante conflicto de concurrencia (chofer inició traslado). | EV-01 | No ejecutado |
| CA-07 | T-04, T-05 | Petición sin rol GESTOR_DESPACHO rechazada con 403 Forbidden. | EV-01 | No ejecutado |
| CUI-01 | T-06 | Exclusión del chofer actual en la lista de candidatos del modal. | EV-02 | No ejecutado |
| CUI-02 | T-06 | Botón "Confirmar reasignación" deshabilitado si el motivo está en blanco. | EV-02 | No ejecutado |
| CUI-03 | T-06 | Barras de capacidad en rojo y bloqueo ante candidato sobrecargado. | EV-02 | No ejecutado |
| CUI-04 | T-06 | Control con spinner impidiendo dobles clics durante la mutación. | EV-02 | No ejecutado |
| CUI-05 | T-07 | Cierre de modal, toast emitido y recarga reactiva de rutas en UI. | EV-02, EV-03 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración de la API de reasignación
- Tareas asociadas: T-02, T-03, T-04, T-05.
- Comando previsto: `./mvnw test -Dtest=ReasignacionControllerTest`
- Resultado: **No ejecutado**.

### EV-02. Pruebas de componentes React del modal de reasignación
- Tareas asociadas: T-06, T-07.
- Comando previsto: `npm run test -- ModalReasignacionDespacho.test.tsx`
- Resultado: **No ejecutado**.

### EV-03. Pruebas de flujo E2E
- Tareas asociadas: T-05, T-07.
- Comando previsto: `npx playwright test tests/e2e/reasignacion-despacho.spec.ts`
- Resultado: **No ejecutado**.
