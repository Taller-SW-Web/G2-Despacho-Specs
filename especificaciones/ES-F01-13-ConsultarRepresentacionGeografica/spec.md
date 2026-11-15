# ES-F01-13: Consultar representación geográfica

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión humana pendiente. **UI:** Aplica. **Servicio:** Gestión.

## 1. Objetivo y alcance

Consultar límites de distritos activos/inactivos y composición derivada de zonas, con procedencia y datos faltantes. Complementa [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md); no modifica cotización ni configura cobertura [cite: 1].

## 2. Precondiciones y flujo

El Gestor autenticado abre Tabla/Mapa, filtra, selecciona y centra un distrito. Se muestran nombre, ubigeo, estado, fuente y versión. La consulta incluye distritos sin geometría y conserva el catálogo habitual liviano.

## 3. Criterios de aceptación

- **CA-01:** DADO un catálogo mixto, CUANDO consulta la capa, ENTONCES obtiene geometrías y registros sin geometría, con filtros y procedencia.
- **CA-02:** DADA una zona con asociaciones postales/inactivas, CUANDO consulta su composición, ENTONCES distingue referencia postal, inactividad y límites faltantes sin cambiar cobertura.
- **CA-03:** DADO acceso anónimo, otro rol o token técnico, CUANDO consulta, ENTONCES recibe 401/403 sin configuración.
- **CA-04:** DADA una falla cartográfica, CUANDO trabaja, ENTONCES conserva lista y formulario y puede reintentar.

## 4. Contrato, UI y verificación

Formatos exclusivamente en [Gestión §3.1.2](../../integraciones/api-contract-gestion-despachos.md#312-geometrías-y-mapas-administrativos--14112026) [cite: 1]. [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md). Se requieren HTTP/PostGIS, componentes y navegador; aceptación humana pendiente.
