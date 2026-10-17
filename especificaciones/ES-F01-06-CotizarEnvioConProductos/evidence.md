# Evidencia de ES-F01-06: Cotizar el envío con datos físicos de productos

**Estado:** Pendiente; la preparación documental no acredita implementación.

**Responsable de verificación:** Valqui.

**Última verificación funcional:** Pendiente.

## 1. Versión y entorno verificados

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), preparación del 16/10/2026 a partir de `91db8f8`.
- Repositorios y commits de código: pendientes, Gestión de Despachos y Gateway.
- Entorno, despliegue, datos y preparación: pendientes.
- Dependencias: Productos, Seguridad y canales no utilizados en esta preparación; simulaciones y servicios reales por identificar al ejecutar.
- Alcance efectivamente verificado: ningún criterio funcional ejecutado; solo preparación documental SDD.
- UI: no aplica; API consumida por canales, sin `ui.md`.

## 2. Cobertura de criterios

| Criterio | Tarea | Prueba o comprobación | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02 a T-05 | Totales, costo, moneda, plazo y fecha esperados | EV-02, EV-03, EV-04 | Pendiente |
| CA-02 | T-02, T-03, T-05 | Sin cobertura: sin costo ni llamada a Productos | EV-02, EV-03 | Pendiente |
| CA-03 | T-02, T-03, T-05 | Líneas/cantidades inválidas en destino cubierto | EV-02, EV-03 | Pendiente |
| CA-04 | T-03, T-05 | SKU inexistente identificado sin costo | EV-03 | Pendiente |
| CA-05 | T-03, T-05 | Datos físicos incompletos sin costo | EV-03 | Pendiente |
| CA-06 | T-03, T-05 | Indisponibilidad sin costo estimado | EV-03 | Pendiente |
| CA-07 | T-01, T-03, T-05 | Zona activa sin tarifa: cobertura sin costo ni plazo | EV-01, EV-03 | Pendiente |
| CA-08 | T-03 a T-05 | Token técnico sin sesión humana ni creación de recursos | EV-03, EV-04 | Pendiente |
| CA-09 | T-04, T-05 | Exceso de límite rechazado sin cálculo | EV-04 | Pendiente |
| CA-10 | T-02, T-03, T-05 | Peso/volumen del cliente no cambian el cálculo | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Un doble no acredita integración con el proveedor real.

## 3. Registros de verificación

### EV-01. Revisión de contrato y datos

- Tareas y criterios: T-01; soporte de todos, en particular CA-01 y CA-07.
- Preparación y pasos previstos: revisar contrato §§5.1/5.2, modelo, precisión del ejemplo, calendario y decisiones DT-01 a DT-03; enlazar documentos revisados.
- Resultado esperado: respuesta sin tarifa y cálculo definidos en documentos canónicos.
- Fecha, persona, revisión/commit y entorno: pendientes.
- Resultado observado y artefacto de revisión: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: no se han utilizado; la revisión documental no verifica el backend.

### EV-02. Motor y validaciones

- Tareas y criterios: T-02/T-05; CA-01 a CA-05 y CA-10.
- Preparación y pasos previstos: datos físicos y tarifa del ejemplo, reloj/calendario controlados; ejecutar pruebas de cálculo, recargo, SKU repetidos, líneas inválidas y cobertura previa a validación.
- Resultado esperado: totales/costo según precisión acordada, sin datos físicos autoritativos del cliente ni consulta al proveedor fuera de cobertura.
- Fecha, persona, commit, entorno y comando exacto de la suite: pendientes.
- Resultado observado y reporte: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: doble de Productos previsto; no acredita disponibilidad ni autorización reales.

### EV-03. Endpoint, seguridad e integración

- Tareas y criterios: T-03/T-05; CA-01 a CA-08 y CA-10.
- Preparación y pasos previstos: PostgreSQL aislado, tokens de prueba y proveedor controlado; probar respuestas, distrito ausente, token inválido/sin scope, fallos/timeout y token propio saliente; inspeccionar ausencia de escrituras de negocio.
- Resultado esperado: contrato respetado, lote con SKU únicos y errores sin costo; zona sin tarifa según acuerdo.
- Fecha, persona, commit, entorno y comando exacto de la suite: pendientes.
- Resultado observado y reporte: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: proveedor controlado previsto; indicar cuáles casos también se ejecutaron con Productos real.

### EV-04. Tasa, rendimiento y recorrido real

- Tareas y criterios: T-04/T-05; recorrido de CA-01 a CA-10, especialmente CA-08/09 y requisito de latencia.
- Preparación y pasos previstos: Gateway y servicios reales identificados, consumidores técnicos, configuración de tasa/caché y carga acordada; superar límite y medir latencias de solicitudes admitidas.
- Resultado esperado: rechazo por tasa sin cálculo y respuestas conformes; contrastar latencia con menos de 100 ms según F-01 §8.
- Fecha, persona, commits, entorno y comandos/pasos exactos: pendientes.
- Resultado observado, métricas y artefactos: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: por registrar; ninguna simulación sustituye este recorrido real.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| Migración y preparación SDD | OpenCode, 16/10/2026 | Original, F-01, contratos y modelo en `91db8f8`; plantillas SDD y modelo ES-F01-05 | Completar las carpetas ES-F01-06, ES-F01-07 y ES-F01-08 según el modelo existente | Pendiente de revisión humana |

Se trasladaron las reglas y criterios y se prepararon plan, tareas y registros pendientes; este uso de IA no acredita ejecución de T-01 a T-05.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| DT-01: zona sin tarifa sin respuesta contractual completa | CA-07 | Bloquea adaptador de ese caso | Valqui con Backend y canales |
| DT-02: redondeo y calendario pendientes; ejemplo suma `0.02126 m³` antes de redondear | CA-01 | Bloquea aceptación del cálculo y fecha | Valqui con Arquitectura y canales |
| DT-03: modelo de cobertura/tarifa por conciliar | CA-01, CA-02, CA-07 | Lectura local sin concretar | Valqui con Arquitectura |
| DT-04: tasa, timeout, caché y medición pendientes | CA-06, CA-09 y rendimiento | Bloquea verificación operativa | Valqui con DevOps y Productos |
| DT-05: tokens y entorno real sin verificar | CA-01 a CA-10 | Integración real pendiente | Valqui con Seguridad, Productos y canales |

No hay resultados de implementación ejecutados en esta preparación.

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor, fecha y resultado de revisión: pendientes.
- Estado del alcance: Pendiente.
- Integraciones reales pendientes: Gateway, Seguridad, Productos y canales.

## 7. Referencias

1. [cite: 1] [Especificación](./spec.md), CA-01 a CA-10.
2. [cite: 2] [Plan](./plan.md) y [tareas](./tasks.md).
3. [Contrato externo](../../integraciones/api-contract.md) y [flujo SDD](../../plantillas/sdd/README.md).
