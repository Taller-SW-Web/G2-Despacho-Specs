# Evidencia de ES-F03-03: Consulta del detalle de un despacho

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: sintéticos; sin teléfonos ni direcciones reales.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-04 | Campos completos y protección por estado | EV-01, EV-03 | Pendiente |
| CA-02 | T-03 | `403` por despacho ajeno | EV-01 | Pendiente |
| CA-03 | T-03 | `404` sin datos parciales | EV-01 | Pendiente |
| CUI-01 a CUI-04 | T-01, T-04 | Detalle, llamada, estados y accesibilidad | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Consulta backend

- Criterios: CA-01 a CA-03.
- Resultado esperado: RN-01 a RN-05 cumplidas.
- Dependencias simuladas: F-02 y Ventas y Postventa (identificar si son dobles).
- Resultado observado: pendiente.

### EV-02. UI con fixtures

- Criterios: CUI-01 a CUI-04.
- Resultado esperado: detalle y estados correctos en móvil.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01 a CA-03 y CUI-01 a CUI-04.
- Resultado esperado: detalle real desde «Mi Ruta».
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-03 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: origen de teléfono y referencia | CA-01 | Bloquea integración real | Max Rojas con Ventas y Postventa |
| DT-02: fuente del máximo de intentos | CA-01 | Campo incompleto | Max Rojas con F-04 |
| DT-04: despacho propio de otra jornada | CA-01 | Regla incompleta | Max Rojas con responsable de F-03 |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
