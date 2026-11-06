# Evidencia de ES-F03-09: Recojo de una devolución en el domicilio

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
| CA-01 | T-04, T-05 | Recojo visible en la secuencia | EV-01, EV-02, EV-03 | Pendiente |
| CA-02 | T-04, T-05 | `ASIGNADO` a `EN_CAMINO` | EV-01, EV-02, EV-03 | Pendiente |
| CA-03 | T-04, T-05 | `RECOGIDO` con evidencia; despacho sin cambios | EV-01, EV-03 | Pendiente |
| CA-04 | T-05 | Envío bloqueado sin foto | EV-02 | Pendiente |
| CA-05 | T-03, T-04, T-05 | `FALLIDO`, contador y liberación de reserva | EV-01, EV-03 | Pendiente |
| CA-06 | T-03, T-05 | Motivo ausente o no permitido | EV-01, EV-02 | Pendiente |
| CA-07 | T-04, T-05 | Recojo ajeno, cancelado o reasignado | EV-01, EV-02 | Pendiente |
| CA-08 | T-05 | Datos conservados sin conexión | EV-02 | Pendiente |
| CA-09 | T-03, T-04 | Reintento sin duplicados | EV-01 | Pendiente |
| CA-10 | T-04, T-05 | Cierre de jornada mixto | EV-01, EV-02 | Pendiente |
| CA-11 | T-03 | Historial completo | EV-01 | Pendiente |
| CUI-01 a CUI-07 | T-05, T-06 | Pantallas, estados y accesibilidad | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con API simulada no acredita integración real.

## 3. Registros

### EV-01. Backend

- Criterios: CA-01 a CA-03, CA-05 a CA-07 y CA-09 a CA-11.
- Resultado esperado: RN-01 a RN-10 cumplidas; el despacho original no cambia.
- Dependencias simuladas: Storage y Ventas (identificar si son dobles).
- Resultado observado: pendiente.

### EV-02. UI con API simulada

- Criterios: CA-01, CA-02, CA-04, CA-06 a CA-08, CA-10 y CUI-01 a CUI-07.
- Resultado esperado: validaciones, conservación de datos y mensajes correctos.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01 a CA-03, CA-05 y CUI-01 a CUI-07.
- Resultado esperado: recojo real asignado, registrado y recibido en el centro.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Redacción documental en formato SDD | Claude, 06/11/2026 | F-03, plantillas SDD, contratos, modelo de datos y ES-F03-04 a ES-F03-07 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: acuerdo con Ventas y Postventa | CA-03, CA-05 | Bloquea integración real | Max Rojas con Ventas |
| DT-02: devolución parcial | CA-01 | Define productos y capacidad | Max Rojas con Ventas |
| DT-03: límite de intentos | CA-05 | Define la decisión del Gestor | Max Rojas con Gerardo |
| DT-04: secuencia compartida | CA-01 | Afecta a F-02 | Max Rojas con Tarqui |
| Bucket real de evidencias | CA-03, CA-05 | Mismo pendiente de ES-F03-05 | Ver [Pendientes](../../funcionalidades/pendiente.md) |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
