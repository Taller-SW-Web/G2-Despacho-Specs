# ES-F01-09: Consultar distritos

**Funcionalidad padre:** [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión y aceptación pendientes.

**Actor principal:** Gestor de Despacho. **UI:** Aplica. **Servicio propietario:** Gestión de Despachos.

## 1. Contexto y objetivo

Consultar el catálogo administrable y sus restricciones de identidad sin romper el selector existente de zonas [cite: 1].

## 2. Alcance

- Incluye listado, búsqueda por nombre, filtro de estado y detalle.
- Las mutaciones pertenecen a ES-F01-10 a ES-F01-12.

## 3. Actor, precondiciones y resultados

El Gestor autenticado abre Distritos. Recibe registros reales o un estado vacío, error o acceso denegado, sin fabricar datos.

## 4. Flujo principal y alternativas

1. Consultar activos por defecto.
2. Aplicar nombre y estado; mantener un arreglo compatible.
3. Abrir un detalle para consultar versión y restricciones vigentes.

## 5. Reglas, datos e integraciones

Los formatos, orden y permisos se definen únicamente en [Gestión §3.1.1](../../integraciones/api-contract-gestion-despachos.md#311-administración-de-distritos--13112026) [cite: 2].

## 6. Criterios de aceptación

- **CA-01:** DADO un catálogo mixto, CUANDO se consulta sin estado, ENTONCES devuelve únicamente activos como arreglo y conserva los campos del selector.
- **CA-02:** DADO un nombre y estado, CUANDO se filtra, ENTONCES devuelve las coincidencias ordenadas o un arreglo vacío.
- **CA-03:** DADO un identificador existente o desconocido, CUANDO se consulta, ENTONCES devuelve detalle vigente o `404`.
- **CA-04:** DADO un usuario sin credencial o autorización, CUANDO consulta, ENTONCES recibe `401/403` sin datos.

## 7. UI, backend y requisitos no funcionales

UI en [ui.md](./ui.md). El backend aplica filtros y autorización; no se auditan consultas. Fechas UTC presentadas en America/Lima.

## 8. Verificación y completitud

Integración PostgreSQL/HTTP y componentes para CA-01 a CA-04. Resultados reales en [evidence.md](./evidence.md); aceptación humana pendiente.

## 9. Referencias

- [cite: 1] [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).
- [cite: 2] [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md).
- [Plan](./plan.md), [tareas](./tasks.md), [UI](./ui.md), [evidencia](./evidence.md).
