# Plan de ES-F03-04: Inicio de traslado del despacho

**Responsable:** Max Rojas

**Estado:** Borrador

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-04 |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-04 |
| Contrato | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| Estados | [Diagrama de estados del despacho](../../arquitectura/diagrama-estados-despacho.md) |
| Dependencia | [ES-F03-01](../ES-F03-01-AccesoHabilitacionRepartidor/spec.md) (turno) |

## 2. Estrategia y responsabilidades

Primera transición de campo. Establece el patrón común de idempotencia, conflicto, historial atómico y manejo sin conexión que reutilizan ES-F03-05, ES-F03-06 y ES-F03-07.

| Área | Responsabilidad |
|---|---|
| Web del repartidor | Acción, clave de idempotencia por intento lógico, mensajes y refresco |
| Backend de operación de reparto | Validaciones, transición, historial atómico y publicación del evento |
| Máquina de estados común | Regla de transición `ASIGNADO` → `EN_CAMINO` |
| F-02 | Estado de asignación y cancelación (externo) |

## 3. Frontend

- Generar la clave de idempotencia al pulsar y reutilizarla en cada reintento del mismo intento.
- Actualizar el elemento afectado sin recargar la vista.
- Ante `409` por reasignación o cancelación, refrescar la ruta.

## 4. Backend e integraciones

- Validar token, turno (ES-F03-01), propiedad y estado de origen.
- Registrar la clave de idempotencia y devolver el resultado original en repeticiones.
- Persistir estado, marca temporal, ejecutor e historial en una transacción.
- Publicar el evento a Ventas y Postventa según RT-03.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Acción y mensajes con fixtures | ES-F03-02 I-01, DT-02 | CUI-01 a CUI-04 |
| I-02 | Transición backend probada | DT-01, DT-03, DT-04 | CA-01 a CA-04 |
| I-03 | Recorrido integrado | I-01, I-02 | CA-01 a CA-04 y CUI-01 a CUI-04 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 | Transición aceptada en menos de 2 s en 4G simulada | Real |
| CA-02 | Origen no permitido rechazado | Real |
| CA-03 | Reasignación y cancelación concurrentes | F-02 real o doble identificado |
| CA-04 | Historial completo; reintento sin duplicados | Real |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Responsable | Bloquea |
|---|---|---|---|
| DT-01 | Ruta, payload, encabezado de idempotencia y códigos de error que distingan las causas de `409` | Max Rojas con Backend | I-02, I-03 |
| DT-02 | Componentes compartidos aplicables | Max Rojas con responsables de componentes | I-01 |
| DT-03 | Vigencia y almacenamiento de las claves de idempotencia | Max Rojas con Arquitectura | I-02 |
| DT-04 | Mecanismo de publicación del evento (RT-03): en la transacción o con bandeja de salida | Max Rojas con Arquitectura | I-02 |

## 8. Condiciones para cerrar

- [ ] Pendientes bloqueantes resueltos.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
