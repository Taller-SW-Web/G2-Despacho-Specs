# Evidencia de ES-F03-07: Cierre de jornada y resumen del día

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: sintéticos; hora de corte de prueba documentada.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-05 | Pendientes a `NO_INTENTADO` y turno cerrado | EV-01, EV-03 | Pendiente |
| CA-02 | T-03, T-05 | Cierre sin fallos | EV-01, EV-03 | Pendiente |
| CA-03 | T-04 | Corte automático y reejecución | EV-01 | Pendiente |
| CA-04 | T-03, T-05 | Cifras iguales al historial | EV-01, EV-03 | Pendiente |
| CA-05 | T-03, T-04 | Historial manual y automático | EV-01 | Pendiente |
| CUI-01 a CUI-05 | T-01, T-05 | Diálogo, lista, resumen y accesibilidad | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Cierre, corte y resumen en backend

- Criterios: CA-01 a CA-05.
- Resultado esperado: RN-01 a RN-10 cumplidas.
- Dependencias simuladas: F-05 y reloj (identificar si son dobles).
- Resultado observado: pendiente.

### EV-02. UI con fixtures

- Criterios: CUI-01 a CUI-05.
- Resultado esperado: diálogo, lista y resumen correctos en móvil.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01, CA-02, CA-04 y CUI-01 a CUI-05.
- Resultado esperado: cierre real con F-05 y paso a solo lectura.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-07 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-02: fallo de F-05 tras las transiciones | CA-01, CA-02 | Riesgo de estado inconsistente | Max Rojas con Arquitectura y F-05 |
| DT-04: planificador y hora de corte | CA-03 | Bloquea corte automático | Max Rojas con Arquitectura y DevOps |
| DT-05: alcance de la lista de devolución | CA-01 | Regla incompleta | Max Rojas con responsable de F-03 |
| DT-06: operación concurrente con el corte | CA-03 | Riesgo de conflicto | Max Rojas con Arquitectura |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
