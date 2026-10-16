# Evidencia de ES-F03-01: Acceso y habilitación operativa del repartidor

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: sintéticos; sin datos personales reales ni tokens.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-04 | Acceso en turno con transiciones habilitadas | EV-01, EV-03 | Pendiente |
| CA-02 | T-03, T-04 | `401` sin token o vencido, sin datos | EV-01, EV-03 | Pendiente |
| CA-03 | T-03, T-04 | `403` por rol o falta de vínculo | EV-01, EV-03 | Pendiente |
| CA-04 | T-03, T-04 | Solo lectura y `409` fuera de turno | EV-01, EV-03 | Pendiente |
| CUI-01 a CUI-05 | T-01, T-04 | Modos, mensajes, accesibilidad y móvil | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Seguridad y contexto en backend

- Criterios: CA-01 a CA-04.
- Resultado esperado: `401`, `403` y `409` correctos; contexto resuelto solo desde el token.
- Dependencias simuladas: F-05 (identificar si es doble).
- Resultado observado: pendiente.

### EV-02. UI con fixtures

- Criterios: CUI-01 a CUI-05.
- Resultado esperado: modos y mensajes correctos en móvil. No valida la autorización real.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01 a CA-04 y CUI-01 a CUI-05.
- Resultado esperado: comportamiento completo con Seguridad y Usuarios y F-05 reales.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-01 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: autenticación con Seguridad y Usuarios | CA-01 a CA-03 | Bloquea integración real | Max Rojas con Arquitectura |
| DT-02: DTO y códigos de error | CA-03, CA-04 | Bloquea mensajes definitivos | Max Rojas con Backend |
| DT-03: consulta a F-05 | CA-01, CA-04 | Bloquea backend real | Max Rojas con F-05 |
| DT-05: estado en turno sin asignación diaria | CA-01, CA-04 | Regla incompleta | Max Rojas con F-05 |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
