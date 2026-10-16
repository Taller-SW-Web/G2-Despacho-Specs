# Evidencia de ES-F03-06: Registro de entrega fallida

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: sintéticos; fotografías sin personas ni domicilios reales.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-04 | `FALLIDO`, contador + 1 y datos persistidos | EV-01, EV-03 | Pendiente |
| CA-02 | T-01 | Envío bloqueado sin motivo | EV-02 | Pendiente |
| CA-03 | T-01, T-03 | Solo motivos seleccionables | EV-01, EV-02 | Pendiente |
| CA-04 | T-01 | Estado conservado sin conexión | EV-02 | Pendiente |
| CA-05 | T-03 | Reintento sin duplicados | EV-01 | Pendiente |
| CA-06 | T-03 | Historial completo | EV-01 | Pendiente |
| CUI-01 a CUI-05 | T-01, T-04 | Formulario, estados y accesibilidad | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Incidencia en backend

- Criterios: CA-01, CA-03, CA-05 y CA-06.
- Resultado esperado: RN-01 a RN-09 cumplidas; contador nunca incrementado por reintentos.
- Dependencias simuladas: catálogo y almacenamiento (identificar si son dobles).
- Resultado observado: pendiente.

### EV-02. UI con fixtures

- Criterios: CA-02, CA-04 y CUI-01 a CUI-05.
- Resultado esperado: validaciones, conservación de datos y mensajes correctos.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01 y CUI-01 a CUI-05.
- Resultado esperado: incidencia real visible para F-04.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-06 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: contrato y error de motivo | CA-03 | Bloquea integración real | Max Rojas con Backend |
| DT-03: consulta del catálogo | CA-03 | Define carga del selector | Max Rojas con Gestión de Despachos |
| DT-04: comentario frente a observaciones | CA-06 | Regla incompleta | Max Rojas con responsable de F-03 |
| Pendientes de evidencia de ES-F03-05 | CA-01 | Bloquea backend | Ver ES-F03-05 |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
