# ES-F01-16: Seleccionar distritos en mapa

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión humana pendiente. **UI:** Aplica. **Servicio:** Gestión como proveedor de datos.

## 1. Objetivo y alcance

Complementar [ES-F01-02](../ES-F01-02-RegistrarZonaCobertura/spec.md) con selección administrativa de distritos mediante mapa. El formulario conserva un único estado; solo Guardar zona persiste asociaciones. Padre [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) [cite: 1].

## 2. Criterios de aceptación

- **CA-01:** DADO un distrito activo, CUANDO selecciona en mapa, ENTONCES actualiza el selector y viceversa, sin solicitudes de escritura.
- **CA-02:** DADA una selección con códigos postales y cobertura exclusiva, CUANDO cambia otros distritos, ENTONCES conserva esos datos y distingue referencia postal.
- **CA-03:** DADO un distrito inactivo asociado, CUANDO edita, ENTONCES sigue visible y puede retirarse, pero no añadirse como asociación nueva.
- **CA-04:** DADO conflicto de cobertura, CUANDO selecciona/guarda, ENTONCES se identifica visualmente y el backend mantiene la validación existente sin persistencia parcial.
- **CA-05:** DADA geometría faltante o fallo cartográfico, CUANDO edita, ENTONCES puede continuar por lista y conservar borrador.
- **CA-06:** DADO uso por teclado/móvil, CUANDO configura, ENTONCES accede a las mismas acciones y guarda solo al confirmar.

## 3. Contrato y cierre

Consultar capas y guardar zonas según [Gestión](../../integraciones/api-contract-gestion-despachos.md); no se crea otra API de cobertura [cite: 1]. [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md).
