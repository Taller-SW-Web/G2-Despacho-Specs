# ES-F01-11: Editar un distrito

**Funcionalidad padre:** [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión y aceptación pendientes.

**Actor principal:** Gestor de Despacho. **UI:** Aplica. **Servicio propietario:** Gestión de Despachos.

## 1. Contexto y objetivo

Editar datos permitidos sin invalidar nombres usados por Chatbot ni referencias de cobertura [cite: 1].

## 2. Alcance

Edición protegida y concurrente; el estado solo cambia mediante ES-F01-12.

## 3. Actor, precondiciones y resultados

El Gestor abre el detalle y conserva su versión. Edición y auditoría se confirman juntas; ante conflicto mantiene los valores del formulario para revisar.

## 4. Flujo principal y alternativas

1. Consultar detalle y restricciones vigentes.
2. Enviar datos con su versión.
3. Validar protección, geografía y unicidad y confirmar atómicamente.

## 5. Reglas, datos e integraciones

Nombre/ubigeo del catálogo base no cambian. En registros nuevos solo cambian sin asociaciones distritales ni postales, incluidas zonas inactivas. Aplican formatos y conflictos de [Gestión §3.1.1](../../integraciones/api-contract-gestion-despachos.md#311-administración-de-distritos--13112026) [cite: 2].

## 6. Criterios de aceptación

- **CA-01:** DADO un distrito nuevo sin asociaciones, CUANDO se edita con versión vigente, ENTONCES conserva UUID y audita antes/después.
- **CA-02:** DADO un distrito base o asociado, CUANDO se cambia nombre/ubigeo, ENTONCES `409` sin cambios ni auditoría.
- **CA-03:** DADO una vista obsoleta, CUANDO se guarda, ENTONCES `409` con versión actual; no sobrescribe cambios ajenos.
- **CA-04:** DADO datos idénticos y versión vigente, CUANDO se guarda, ENTONCES no incrementa versión ni duplica auditoría.
- **CA-05:** DADO datos inválidos/duplicados o falta de permisos, CUANDO se guarda, ENTONCES rechaza sin mutaciones parciales.

## 7. UI, backend y requisitos no funcionales

UI en [ui.md](./ui.md). Backend revalida protección frente a asociaciones concurrentes, no confía en indicadores del cliente.

## 8. Verificación y completitud

Integración de protección, concurrencia y rollback; componentes de formulario y conflicto. Evidencia en [evidence.md](./evidence.md).

## 9. Referencias

- [cite: 1] [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).
- [cite: 2] [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md).
- [Plan](./plan.md), [tareas](./tasks.md), [UI](./ui.md), [evidencia](./evidence.md).
