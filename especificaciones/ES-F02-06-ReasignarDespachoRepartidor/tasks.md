# Tareas de ES-F02-06: Reasignar despacho a otro repartidor

**Responsable de coordinación:** Tarqui.

**Estado:** Coordinación durable y modal implementados y verificados localmente; aceptación humana pendiente.

**Avance 26/10/2026:** la intención/cerco de Gestión §3.2.2 completa la coordinación con Operación §5.3.1. Se recupera hacia adelante, nunca con una reserva inicial duplicada ni una compensación de la transferencia. Evidencia: 9 pruebas HTTP/persistencia de reasignación, 9 del modal y recorrido real G2; consultar evidence.md para límites y regresiones.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoint de reasignación documentado en Gestión §3.2. | Contrato | api-contract-gestion-despachos.md | CA-01, CA-02 | Completada |
| T-02 | Transferencia con intención/cerco durable y recuperación hacia adelante. | Backend / Integración | Operación §5.3.1; Gestión §3.2.2 | CA-01, CA-03 | Completada localmente |
| T-03 | `ReasignarDespacho`, versiones, orden determinista de bloqueos y posición al final del destino. | Backend / Dominio | T-02 | CA-01, CA-04, CA-05 | Completada localmente |
| T-04 | `ControladorReasignacion`, autorización humana y validación estricta de cuerpo/cabeceras. | Backend / API | T-03 | CA-02, CA-06, CA-07 | Completada localmente |
| T-05 | HTTP JDK controlado, MockMvc y PostgreSQL/Testcontainers: rechazo, timeout, pérdida de respuesta, rollback y recuperación. | Calidad / Backend | T-04 | CA-01 a CA-07 | 9 pruebas aprobadas y regresión verde |
| T-06 | Modal con exclusión de origen, motivo, métricas reales, bloqueo y recuperación exacta. | Frontend / UI | CR-02, CR-11, CR-12, CR-20 | CUI-01 a CUI-04 | 9 pruebas aprobadas; navegador real verificado |
| T-07 | Hooks existentes, notificación, recarga de rutas y consultas F-03/capacidad real. | Integración UI | T-04, T-06 | CUI-05 | Recorrido integrado aprobado localmente |

## 2. Detalle de tareas

### T-01. Confirmar contrato
- Alcance: verificar payload `{ idNuevoRepartidor, idNuevaJornada, motivo }` en [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).
- Comprobación: contrato revisado.

### T-02. Transferencia de capacidad
- Alcance: transferencia canónica de F-06, fuera de transacción; mismo ID durable en reintentos y cerco hasta confirmación/rechazo definitivo.
- Comprobación: servidor HTTP JDK controlado y pruebas de reserva F-06 con PostgreSQL; no se añade WireMock.

### T-03. Caso de uso
- Alcance: `ReasignarDespacho` y `ReasignacionesPersistencia`, `@Version`, estado/cercos y posición final del destino sin renumerar el origen.
- Comprobación: pruebas unitarias con JUnit 5.

### T-04. Controlador REST
- Alcance: `POST /api/v1/despachos/{idDespacho}/reasignacion` con validaciones de motivo y rol `GESTOR_DESPACHO`.
- Comprobación: pruebas con MockMvc verificando errores 400 y 403.

### T-05. Pruebas de integración
- Alcance: suite completa verificando éxito, chofer inhabilitado y concurrencia ante inicio de traslado en F-03.
- Comprobación: 100% de tests aprobados.

### T-06. Componente Modal React
- Alcance: modal Mantine con exclusión del conductor actual, validación visual de motivo no vacío y barras de ocupación proyectadas.
- Comprobación: tests de UI con Testing Library.

### T-07. Integración frontend
- Alcance: apertura desde "Reasignar", hooks existentes (sin React Query nuevo), mutación, feedback Mantine y recuperación de comando original.
- Comprobación: verificación manual o E2E con Playwright.
