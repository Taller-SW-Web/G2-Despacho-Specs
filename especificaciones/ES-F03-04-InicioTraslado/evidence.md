# Evidencia de ES-F03-04: Inicio de traslado del despacho

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: sintéticos.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-04 | Transición aceptada y vista actualizada | EV-01, EV-03 | Pendiente |
| CA-02 | T-03 | `409` por origen no permitido | EV-01 | Pendiente |
| CA-03 | T-03, T-04 | `409` por reasignación o cancelación y refresco | EV-01, EV-03 | Pendiente |
| CA-04 | T-03 | Historial completo y reintento sin duplicados | EV-01 | Pendiente |
| CUI-01 a CUI-04 | T-01, T-04 | Acción, mensajes y sin conexión | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Transición backend

- Criterios: CA-01 a CA-04.
- Resultado esperado: RN-01 a RN-07 cumplidas; evento publicado.
- Dependencias simuladas: F-02 y Ventas y Postventa (identificar si son dobles).
- Resultado observado: pendiente.

### EV-02. UI con fixtures

- Criterios: CUI-01 a CUI-04.
- Resultado esperado: mensajes y reintento correctos.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01, CA-03 y CUI-01 a CUI-04.
- Resultado esperado: transición real en menos de 2 s en 4G.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-04 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: contrato y códigos de `409` | CA-02, CA-03 | Bloquea integración real | Max Rojas con Backend |
| DT-03: claves de idempotencia | CA-04 | Bloquea backend | Max Rojas con Arquitectura |
| DT-04: publicación del evento | CA-01 | Bloquea backend | Max Rojas con Arquitectura |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
