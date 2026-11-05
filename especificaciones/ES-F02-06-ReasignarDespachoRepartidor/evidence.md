# Evidencia de ES-F02-06: Reasignar despacho a otro repartidor

**Estado:** Consumidor de reasignación verificado localmente con API simulada; persistencia, servicios publicados y aceptación pendientes.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** 05/11/2026, consumidor con API simulada y Chromium; integración persistente pendiente.

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
| CUI-01 | T-06 | Exclusión del chofer actual en la lista de candidatos del modal. | EV-04 | Verificado con API simulada |
| CUI-02 | T-06 | Botón "Confirmar reasignación" deshabilitado si el motivo está en blanco. | EV-04 | Verificado con API simulada |
| CUI-03 | T-06 | Barras de capacidad en rojo y bloqueo ante candidato sobrecargado. | EV-04 | Verificado con API simulada |
| CUI-04 | T-06 | Control con spinner impidiendo dobles clics durante la mutación. | EV-04 | Verificado con API simulada |
| CUI-05 | T-07 | Cierre de modal, toast emitido y recarga reactiva de rutas en UI. | EV-04 | Verificado con API simulada; persistencia y proyección reales pendientes |

## 3. Registros de verificación

### EV-01. Pruebas de integración de la API de reasignación
- Tareas asociadas: T-02, T-03, T-04, T-05.
- Comando previsto: `./mvnw test -Dtest=ReasignacionControllerTest`
- Resultado: **No ejecutado**.

### EV-04. Reasignación desde Administración · 05/11/2026

- Misma rama, bases, entorno y límites del [incremento de rutas EV-04](../ES-F02-05-ConsultarReordenarSecuenciaRuta/evidence.md#ev-04-incremento-seguro-de-rutas-del-hito-4--05112026). No existe un SHA nuevo aprobado ni un despliegue de este incremento.
- `ModalReasignacion.tsx` se abre únicamente desde una parada `ASIGNADO` de jornada activa, sin cerco local ni cambios de orden pendientes. Identifica carga y conductor de origen; excluye al conductor actual, muestra las tres barras y bloquea sobrecarga. Exige motivo no vacío de hasta 500 puntos de código Unicode, sin introducir el mínimo de cinco del plan antiguo.
- El adaptador verifica todas las identidades de origen/destino y la versión posterior antes de notificar éxito. Usa `If-Match` con versión **numérica** del despacho entre comillas e `Idempotency-Key` UUID v4. Una respuesta perdida/incoherente o `503` conserva el comando inmutable; la recuperación explícita reutiliza clave, versión y contenido. No hay POST automático con una identidad nueva. Un `422` renueva candidatos y exige otra selección; un conflicto definitivo exige consultar. `401/403` retiran contenido y modal; resultados tardíos de otra sesión se ignoran.
- Después de confirmar, se consultan de nuevo origen y catálogo. El destino se obtiene con GET al seleccionarlo: no se conserva una ruta destino desactualizada en caché. Una transferencia que deja huecos en el origen no fuerza renumeración ni habilita reordenamiento controvertido.
- `RutasProgramacion.test.tsx` cubre exclusión, carga/motivo, prevención de doble clic, rechazo de capacidad, respuesta incierta, identidad ajena y revocación/cambio de sesión. Chromium verifica en tres tamaños una transferencia simulada cuyo primer intento pierde la respuesta: se recupera el mismo comando, desaparece del origen y aparece en la ruta destino, sin segunda transferencia.
- Resultado de regresión frontend: **209 pruebas administrativas aprobadas**, tipos/build correctos y **7 recorridos Chromium** con APIs interceptadas. Estos resultados no acreditan las reservas de Operación, las proyecciones reales de F-03 ni G7. Los registros EV-01/02/03 y los CA de backend siguen pendientes de integración real; los CUI tienen cobertura local descrita aquí, no aceptación humana. La revisión de capturas detectó compresión vertical de tarjetas en el modal móvil: se impide su contracción en el listado desplazable y Chromium comprueba también que el contenido de cada tarjeta no se desborde verticalmente.
- Backend: Gateway `render` corregido y **29 pruebas aprobadas**, incluidas conservación de las cabeceras/cuerpo de reasignación y denegación de las rutas técnicas. Se documentó la transferencia **existente** en [Operación §5.5](../../integraciones/api-contract-operacion-reparto.md#55-gestión-transfiere-una-reserva-en-operación) y su transporte público en [Gestión §3.2.2](../../integraciones/api-contract-gestion-despachos.md#322-transporte-de-reasignación-y-recuperación). No se modificaron el mecanismo de transferencia ni los controles/scopes internos; el acuerdo de identidad sigue pendiente.

### EV-02. Pruebas de componentes React del modal de reasignación
- Tareas asociadas: T-06, T-07.
- Comando previsto: `npm run test -- ModalReasignacionDespacho.test.tsx`
- Resultado: **No ejecutado**.

### EV-03. Pruebas de flujo E2E
- Tareas asociadas: T-05, T-07.
- Comando previsto: `npx playwright test tests/e2e/reasignacion-despacho.spec.ts`
- Resultado: **No ejecutado**.
