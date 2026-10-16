# Plan de ES-F03-06: Registro de entrega fallida

**Responsable:** Max Rojas

**Estado:** Borrador

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-06 |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-05 |
| Catálogo de motivos | [Gestión §4](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo) |
| Contrato | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| Patrones reutilizados | [ES-F03-04](../ES-F03-04-InicioTraslado/plan.md) (transición) y [ES-F03-05](../ES-F03-05-EntregaExitosaEvidencia/plan.md) (evidencia) |

## 2. Estrategia y responsabilidades

Combina el patrón de transición de ES-F03-04 y el registro de evidencia de ES-F03-05, y añade motivo validado e incremento del contador.

| Área | Responsabilidad |
|---|---|
| Web del repartidor | Formulario, carga de motivos, conservación de datos y envío |
| Backend de operación de reparto | Validación de motivo y archivo, evidencia, transición, contador e historial |
| Gestión de Despachos | Catálogo canónico de motivos |
| F-04 | Consumo del despacho `FALLIDO` (externo) |

## 3. Frontend

- Cargar los motivos desde el catálogo; no mantener lista local.
- Bloquear el envío sin motivo o fotografía.
- Conservar motivo, imagen y comentario ante error; reutilizar la clave en reintentos.

## 4. Backend e integraciones

- Validar el motivo contra el catálogo con `activo=true` y `seleccionableEnCampo=true`; rechazar `NO_INTENTADO`.
- Registrar la evidencia antes de la transición; sin referencia no hay transición.
- Persistir estado, motivo, evidencia, comentario, contador + 1 e historial en una transacción.
- Publicar el evento según RT-03.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Formulario con fixtures | ES-F03-05 I-01, DT-02 | CUI-01 a CUI-05 |
| I-02 | Incidencia backend probada | DT-01, DT-03, ES-F03-05 I-02 | CA-01 a CA-06 |
| I-03 | Recorrido integrado | I-01, I-02 | CA-01 a CA-06 y CUI-01 a CUI-05 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 | Transición, contador + 1 y datos persistidos | Real |
| CA-02 | Envío bloqueado sin motivo | Fixtures |
| CA-03 | Solo motivos seleccionables en UI y backend | Catálogo real o doble identificado |
| CA-04 | Estado conservado sin conexión | Fixtures |
| CA-05 | Reintento sin duplicar transición, contador ni historial | Real |
| CA-06 | Historial completo | Real |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Responsable | Bloquea |
|---|---|---|---|
| DT-01 | Ruta, payload y código de error para motivo no válido | Max Rojas con Backend | I-02, I-03 |
| DT-02 | Componentes compartidos aplicables | Max Rojas con responsables de componentes | I-01 |
| DT-03 | Forma de consulta del catálogo (en cada apertura o con caché) | Max Rojas con Gestión de Despachos | CA-03 |
| DT-04 | Diferencia entre «comentario» y «observaciones» del historial | Max Rojas con responsable de F-03 | CA-06 |

Los pendientes de evidencia (formato, tamaño, almacenamiento) son los de ES-F03-05 DT-01, DT-02 y DT-04.

## 8. Condiciones para cerrar

- [ ] Pendientes bloqueantes resueltos.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
