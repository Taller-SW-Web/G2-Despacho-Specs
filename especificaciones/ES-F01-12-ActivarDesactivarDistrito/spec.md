# ES-F01-12: Activar o desactivar un distrito

**Funcionalidad padre:** [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión y aceptación pendientes.

**Actor principal:** Gestor de Despacho. **UI:** Aplica. **Servicio propietario:** Gestión de Despachos.

## 1. Contexto y objetivo

Suspender y recuperar cobertura nueva mediante baja lógica, conservando operaciones históricas [cite: 1].

## 2. Alcance

Estado, cobertura y efectos sobre nuevas solicitudes. No altera despachos existentes ni reprogramaciones.

## 3. Actor, precondiciones y resultados

El Gestor confirma el efecto usando la versión consultada. El cambio conserva identidad, asociaciones, tarifas e históricos.

## 4. Flujo principal y alternativas

1. Mostrar confirmación que explica cotizaciones y despachos nuevos.
2. Enviar estado y versión; DELETE usa el mismo caso de baja.
3. Confirmar estado y auditoría juntos y refrescar el catálogo.

## 5. Reglas, datos e integraciones

Un distrito inactivo informado bloquea también códigos postales ajenos. La reactivación no activa zonas ni crea tarifas. Se conserva exclusividad entre zonas. Contrato canónico en [Gestión §3.1.1](../../integraciones/api-contract-gestion-despachos.md#311-administración-de-distritos--13112026) [cite: 2].

## 6. Criterios de aceptación

- **CA-01:** DADO San Borja cubierto, CUANDO se desactiva, ENTONCES cotización devuelve sin cobertura, sin costo/plazo, sin Productos ni fila histórica nueva, con o sin código postal propio/ajeno.
- **CA-02:** DADO otro distrito activo de su zona, CUANDO se cotiza, ENTONCES conserva su cobertura.
- **CA-03:** DADO baja confirmada, CUANDO llega un despacho nuevo, ENTONCES `422 DESP_ERROR_SIN_COBERTURA`, aun con cotización anterior; una creación ya aceptada recupera su resultado idempotente.
- **CA-04:** DADO despachos e históricos existentes, CUANDO se desactiva, ENTONCES conservan datos y ciclo, incluidas reprogramaciones.
- **CA-05:** DADO distrito reactivado con zona activa y tarifa vigente, CUANDO se cotiza con reloj y productos controlados, ENTONCES recupera costo, moneda, carga y plazo anteriores.
- **CA-06:** DADO estado ya coincidente, CUANDO se repite, ENTONCES no cambia versión/fecha ni duplica auditoría; una transición con versión obsoleta rechaza.
- **CA-07:** DADO cobertura exclusivamente postal o simulación, CUANDO se resuelve, ENTONCES solo elige distritos activos; zona inactiva sigue sin cobertura.
- **CA-08:** DADO una zona con asociaciones inactivas, CUANDO se edita, ENTONCES puede conservarlas/retirarlas, pero no añadir ni ampliar cobertura de un inactivo.

## 7. UI, backend y requisitos no funcionales

UI en [ui.md](./ui.md). Resolución compartida entre cotización, consulta y recepción; transacción local con auditoría y control de versión.

## 8. Verificación y completitud

Pruebas HTTP/PostgreSQL, regresión de F-02/F-04 y recorrido por Gateway/navegador. Evidencia en [evidence.md](./evidence.md); aceptación humana pendiente.

## 9. Referencias

- [cite: 1] [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).
- [cite: 2] [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md).
- [Plan](./plan.md), [tareas](./tasks.md), [UI](./ui.md), [evidencia](./evidence.md).
