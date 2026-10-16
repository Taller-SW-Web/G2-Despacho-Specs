# Evidencia de ES-F03-02: Consulta de la ruta de la jornada

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: sintéticos; sin datos personales reales.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-04 | Orden, campos y exclusiones | EV-01, EV-03 | Pendiente |
| CA-02 | T-03, T-04 | Ruta vacía | EV-01, EV-03 | Pendiente |
| CA-03 | T-03 | `403` por identificador ajeno | EV-01 | Pendiente |
| CA-04 | T-03, T-04 | Bandeja de pendientes no operable | EV-01, EV-03 | Pendiente |
| CUI-01 a CUI-05 | T-01, T-04 | Lista, bandeja, estados y accesibilidad | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Consulta backend

- Criterios: CA-01 a CA-04.
- Resultado esperado: RN-01 a RN-07 cumplidas; sin datos ante `403`.
- Dependencias simuladas: F-02 y F-05 (identificar si son dobles).
- Resultado observado: pendiente.

### EV-02. UI con fixtures

- Criterios: CUI-01 a CUI-05.
- Resultado esperado: lista, bandeja y estados correctos en móvil.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01 a CA-04 y CUI-01 a CUI-05.
- Resultado esperado: ruta real del repartidor desde F-02.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-02 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: definición de jornada en curso | CA-01, CA-04 | Bloquea backend | Max Rojas con Arquitectura |
| DT-02: ruta y DTO | CA-01 a CA-04 | Bloquea integración real | Max Rojas con Backend |
| DT-04: dirección en la bandeja | CA-04 | Regla incompleta | Max Rojas con responsable de F-03 |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
