# Plan de ES-F03-05: Registro de entrega exitosa con evidencia

**Responsable:** Max Rojas

**Estado:** Borrador

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-05 |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-05 |
| Contrato | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| Pendientes del equipo | [pendiente.md](../../funcionalidades/pendiente.md), sección F-03 |
| Patrón de transición | [ES-F03-04](../ES-F03-04-InicioTraslado/plan.md) |

## 2. Estrategia y responsabilidades

Reutiliza el patrón de transición de ES-F03-04 y añade el registro previo de la evidencia: sin referencia de evidencia no hay transición.

| Área | Responsabilidad |
|---|---|
| Web del repartidor | Captura, previsualización, conservación de datos ante error y envío |
| Backend de operación de reparto | Validación del archivo, registro en almacenamiento privado, transición e historial |
| Almacenamiento privado de evidencia | Conservación de la fotografía (mecanismo pendiente) |
| F-05 | Recálculo de ocupación (externo) |

## 3. Frontend

- Captura con la cámara del celular y previsualización.
- Conservar imagen y nombre en memoria ante error hasta un envío exitoso.
- Reutilizar la clave de idempotencia en los reintentos del mismo envío.

## 4. Backend e integraciones

- Validar presencia, formato y tamaño del archivo antes de almacenarlo.
- Registrar la evidencia; si falla o excede el tiempo de espera, no aplicar la transición.
- Aplicar la transición e historial en una transacción, con la referencia de evidencia.
- Definir el tratamiento de una evidencia almacenada cuya transición posterior falla (DT-04).
- Publicar el evento según RT-03.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Formulario con fixtures | ES-F03-03 I-01, DT-03 | CUI-01 a CUI-05 |
| I-02 | Evidencia y transición backend probadas | DT-01, DT-02, DT-04, ES-F03-04 I-02 | CA-01 a CA-05 |
| I-03 | Recorrido integrado | I-01, I-02 | CA-01 a CA-05 y CUI-01 a CUI-05 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 | Evidencia registrada y estado `ENTREGADO` | Almacenamiento real o doble identificado |
| CA-02 | Sin petición desde la UI; backend rechaza envío forzado sin archivo | Real |
| CA-03 | Error y tiempo de espera sin cambio de estado | Doble del almacenamiento |
| CA-04 | Archivo inválido rechazado y no guardado | Real |
| CA-05 | Historial completo; reintento sin duplicados | Real |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Responsable | Bloquea |
|---|---|---|---|
| DT-01 | Resuelta parcialmente: JPEG/PNG/WebP, máximo 2 MiB. Compresión y tratamiento EXIF siguen pendientes y no se aplican. | Contrato CR-17 | — para validar archivo |
| DT-02 | Resuelta: almacenamiento privado, URL firmada de carga y envío directo al bucket; la API recibe solo el identificador. | Contrato CR-17 | — |
| DT-03 | Resuelta: reutilizar `CapturaEvidencia` compartido. | CR-17 | — |
| DT-04 | Pendiente: limpieza recuperable de archivos cargados sin una transición confirmada. | Arquitectura/Backend | I-02 |
| DT-05 | Pendiente: contenido permitido de observaciones del historial; no copiar datos personales a la bandeja histórica. | Responsable F-03 | CA-05 |

## 8. Condiciones para cerrar

- [ ] Pendientes bloqueantes resueltos.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
