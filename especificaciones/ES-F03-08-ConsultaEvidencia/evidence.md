# Evidencia de ES-F03-08: Consulta autorizada de la evidencia

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: fotografías sintéticas; sin URLs firmadas reales en los registros.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-03 | URL emitida, visualización y renovación | EV-01, EV-03 | Pendiente |
| CA-02 | T-03 | Acceso sin firma o vencido denegado | EV-03 | Pendiente |
| CA-03 | T-02 | `403` para usuario no autorizado | EV-01 | Pendiente |
| CUI-01 a CUI-04 | T-01, T-03 | Visor, vencimiento y mensajes | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Autorización en backend

- Criterios: CA-01 y CA-03.
- Resultado esperado: RN-01 a RN-04 cumplidas.
- Dependencias simuladas: almacenamiento (identificar si es doble).
- Resultado observado: pendiente.

### EV-02. Visor con fixtures

- Criterios: CUI-01 a CUI-04.
- Resultado esperado: vencimiento, renovación y descarte de imagen correctos.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01, CA-02 y CUI-01 a CUI-04.
- Resultado esperado: almacenamiento privado rechaza accesos sin firma válida.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-08 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: almacenamiento, firma y vigencia | CA-01, CA-02 | Bloquea backend | Max Rojas con Arquitectura |
| DT-03: evidencias de jornadas anteriores para el repartidor | CA-01 | Regla incompleta | Max Rojas con responsable de F-03 |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
