# Evidencia de ES-F03-05: Registro de entrega exitosa con evidencia

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: sintéticos; las fotografías de prueba no muestran personas ni domicilios reales.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-04 | Evidencia registrada y estado `ENTREGADO` | EV-01, EV-03 | Pendiente |
| CA-02 | T-01, T-03 | Envío bloqueado sin fotografía | EV-01, EV-02 | Pendiente |
| CA-03 | T-03 | Fallo de almacenamiento sin cambio de estado | EV-01 | Pendiente |
| CA-04 | T-03 | `400` y archivo no guardado | EV-01 | Pendiente |
| CA-05 | T-03 | Historial completo y reintento sin duplicados | EV-01 | Pendiente |
| CUI-01 a CUI-05 | T-01, T-04 | Formulario, estados y accesibilidad | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Evidencia y transición en backend

- Criterios: CA-01 a CA-05.
- Resultado esperado: RN-01 a RN-07 cumplidas; sin transición si la evidencia no se registra.
- Dependencias simuladas: almacenamiento (doble para error y tiempo de espera).
- Resultado observado: pendiente.

### EV-02. UI con fixtures

- Criterios: CUI-01 a CUI-05.
- Resultado esperado: bloqueo sin fotografía y conservación de datos ante error.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01 y CUI-01 a CUI-05.
- Resultado esperado: entrega real con cámara y almacenamiento privado.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-05 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: formatos, tamaño, compresión y metadatos | CA-04 | Bloquea validación | Equipo F-03 |
| DT-02: mecanismo de almacenamiento | CA-01, CA-03 | Bloquea backend | Max Rojas con Arquitectura |
| DT-04: evidencias huérfanas | CA-03 | Riesgo de archivos sin despacho | Max Rojas con Arquitectura |
| DT-05: contenido de «observaciones» | CA-05 | Regla incompleta | Max Rojas con responsable de F-03 |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
