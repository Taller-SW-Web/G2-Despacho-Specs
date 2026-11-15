# ES-F01-14: Validar importación de geometrías

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión humana pendiente. **UI:** Aplica. **Servicio:** Gestión.

## 1. Objetivo y flujo

El Gestor carga un GeoJSON individual o de varios distritos, declara fuente/revisión, revisa correspondencias y solicita validación. El backend prepara un informe y una propuesta temporal sin modificar límites. Padre: [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) [cite: 1].

## 2. Reglas y criterios

- **CA-01:** DADO un archivo válido, CUANDO valida, ENTONCES obtiene comparación actual/propuesta y versiones, sin cambios en geometría, histórico ni auditoría.
- **CA-02:** DADO ubigeo válido existente, CUANDO valida, ENTONCES conserva ceros iniciales y asocia al UUID vigente; nombres del archivo no editan el catálogo.
- **CA-03:** DADO un archivo sin ubigeo, CUANDO hay coincidencia nominal, ENTONCES solo se sugiere y requiere correspondencia explícita antes de validar.
- **CA-04:** DADAS geometrías inválidas, vacías, fuera de ámbito, proyectadas o códigos desconocidos/duplicados, CUANDO valida, ENTONCES informa incidencias por entidad sin reparar ni habilitar confirmación.
- **CA-05:** DADOS cuerpos o complejidad superiores al máximo, CUANDO carga, ENTONCES rechaza tanto en Gateway como Gestión, incluso sin longitud declarada.
- **CA-06:** DADO acceso sin Gestor humano, CUANDO valida, ENTONCES recibe 401/403.

## 3. Contrato y cierre

Formatos y límites exclusivamente en [Gestión §3.1.2](../../integraciones/api-contract-gestion-despachos.md#312-geometrías-y-mapas-administrativos--14112026) [cite: 1]. [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md). Validar PostGIS en base desechable; no en Supabase ni base local persistente.
