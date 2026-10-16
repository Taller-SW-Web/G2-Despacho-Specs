# Plan de ES-F03-07: Cierre de jornada y resumen del día

**Responsable:** Max Rojas

**Estado:** Borrador

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-05 |
| UI | [ui.md](./ui.md), UI-01 a UI-03 y CUI-01 a CUI-05 |
| Contrato | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| Patrón de transición | [ES-F03-04](../ES-F03-04-InicioTraslado/plan.md) |
| Dependencias | [ES-F03-01](../ES-F03-01-AccesoHabilitacionRepartidor/spec.md) (turno) y [ES-F03-02](../ES-F03-02-ConsultaRutaJornada/spec.md) (pendientes de regularización) |

## 2. Estrategia y responsabilidades

Un mismo caso de uso de cierre lo invocan el repartidor y el proceso programado, cambiando solo ejecutor y origen.

| Área | Responsabilidad |
|---|---|
| Web del repartidor | Diálogo, lista de devolución y resumen |
| Backend de operación de reparto | Caso de uso de cierre, proceso programado y consulta del resumen |
| F-05 | Cierre del turno (externo) |
| F-04 | Consumo de despachos `NO_INTENTADO` (externo) |

## 3. Frontend

- Consultar la cantidad de pendientes antes de mostrar el diálogo.
- Reutilizar la clave de idempotencia en reintentos del mismo cierre.
- Tras el cierre, pasar a modo solo lectura (ES-F03-01).

## 4. Backend e integraciones

- Caso de uso de cierre: seleccionar pendientes de la jornada, aplicar `FALLIDO` / `NO_INTENTADO` sin contador, historial por despacho en transacción y solicitud de cierre de turno a F-05.
- Proceso programado a la hora de corte: repartidores sin cierre; ejecutor y origen automáticos; reejecución sin efectos adicionales.
- Resumen calculado a partir del historial.
- Publicar eventos según RT-03.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Diálogo, lista y resumen con fixtures | ES-F03-02 I-01, DT-03 | CUI-01 a CUI-05 |
| I-02 | Cierre manual y resumen en backend | DT-01, DT-02, DT-05, ES-F03-04 I-02 | CA-01, CA-02, CA-04, CA-05 |
| I-03 | Corte automático | I-02, DT-04 | CA-03, CA-05 |
| I-04 | Recorrido integrado | I-01 a I-03 | CA-01 a CA-05 y CUI-01 a CUI-05 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 | Pendientes a `NO_INTENTADO` sin contador y turno cerrado | F-05 real o doble identificado |
| CA-02 | Cierre sin fallos generados | F-05 real o doble identificado |
| CA-03 | Corte a hora configurada; reejecución sin cambios | Reloj controlado en pruebas |
| CA-04 | Cifras iguales al historial | Real |
| CA-05 | Historial con origen manual y automático | Real |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Responsable | Bloquea |
|---|---|---|---|
| DT-01 | Ruta y DTO del cierre y del resumen | Max Rojas con Backend | I-02 |
| DT-02 | Comportamiento si F-05 falla tras aplicar las transiciones (reintento, compensación o cierre parcial) | Max Rojas con Arquitectura y F-05 | CA-01, CA-02 |
| DT-03 | Componentes compartidos aplicables | Max Rojas con responsables de componentes | I-01 |
| DT-04 | Planificador del proceso programado, configuración de la hora de corte y zona horaria (`America/Lima`) | Max Rojas con Arquitectura y DevOps | I-03 |
| DT-05 | Si la lista de devolución incluye también los `FALLIDO` con intento real (ES-F03-06) o solo los `NO_INTENTADO` | Max Rojas con responsable de F-03 | CA-01 |
| DT-06 | Tratamiento de un despacho que el repartidor está operando justo cuando se ejecuta el corte | Max Rojas con Arquitectura | CA-03 |

## 8. Condiciones para cerrar

- [ ] Pendientes bloqueantes resueltos.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
