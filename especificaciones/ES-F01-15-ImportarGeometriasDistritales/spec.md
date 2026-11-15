# ES-F01-15: Importar geometrías distritales

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión humana pendiente. **UI:** Aplica. **Servicio:** Gestión.

## 1. Objetivo y precondiciones

El mismo Gestor confirma una propuesta válida y vigente de ES-F01-14. Guardar límites completos con control concurrente, procedencia e histórico. Padre [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md); formatos en [Gestión §3.1.2](../../integraciones/api-contract-gestion-despachos.md#312-geometrías-y-mapas-administrativos--14112026) [cite: 1].

## 2. Criterios de aceptación

- **CA-01:** DADA una propuesta revisada, CUANDO confirma, ENTONCES guarda geometrías, versiones, procedencia y auditoría atómicamente con identidad/fecha del servidor.
- **CA-02:** DADO un reemplazo, CUANDO confirma, ENTONCES conserva límite previo completo e histórico de procedencia; omitidos no cambian.
- **CA-03:** DADA respuesta perdida, CUANDO repite clave y validación, ENTONCES recupera resultado exacto sin duplicar cambios; otra validación con misma clave se rechaza.
- **CA-04:** DADA propuesta de otro usuario, expirada, consumida o con versiones cambiadas, CUANDO confirma, ENTONCES rechaza sin mutaciones.
- **CA-05:** DADO fallo de persistencia/auditoría, CUANDO confirma un lote, ENTONCES revierte todo y nunca responde aceptación parcial.
- **CA-06:** DADA cotización controlada antes de importar/reemplazar, CUANDO repite después, ENTONCES conserva cobertura, costo, moneda, peso, volumen y plazo, sin campos nuevos. Un distrito sin geometría sigue cotizando.

## 3. Cierre

[UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md). El histórico no admite edición/borrado por API. No activa distritos ni zonas, no crea tarifas y no dibuja límites.
