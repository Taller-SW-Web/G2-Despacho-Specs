# Plan de ES-F06-09: Elegir el tipo de operación de la jornada

**Responsable:** Max Rojas

**Estado:** Borrador; pendiente de revisión técnica.

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-06 |
| Contrato | [Operación §4.2.4](../../integraciones/api-contract-operacion-reparto.md#424-tipo-de-operación-de-la-jornada) |
| Datos | [Modelo §3.6](../../arquitectura/modelo-datos.md#36-recojos-de-devoluciones) |

## 2. Estrategia y responsabilidades

| Área | Responsabilidad | Archivos o componentes previstos |
|---|---|---|
| Operación | Guardar, devolver y validar el tipo | Paquete `jornadas` y migración nueva |
| Panel del Gestor | Selector y tipo visible | `features/jornadas` |
| Gestión | Traducir el nuevo `409` | `CapacidadProgramacionHttp` |

## 3. Backend y datos

- Migración: añadir `tipo_operacion` con valor por defecto `ENTREGAS`; no reescribe otros datos.
- `GestorJornadas`: validar el tipo en `reservar` y `transferir`, y filtrar `consultarDisponibles`.
- Reserva: el tipo requerido se deduce de la presencia de `idRecojo`.

## 4. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Migración y tipo en jornada | Ninguna | CA-01 a CA-03 |
| I-02 | Disponibilidad, reserva y transferencia por tipo | I-01 | CA-04, CA-05 |
| I-03 | Cierre con recojos pendientes | [ES-F03-09](../ES-F03-09-RecojoDevolucion/plan.md), I-03 | CA-06 |
| I-04 | Selector y monitoreo | I-01 | CUI-01, CUI-02 |

## 5. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 a CA-04 | Pruebas HTTP con base desechable | Real |
| CA-05, CA-06 | Reservas, transferencia y cierre con base desechable | Real |
| CUI-01, CUI-02 | Pruebas de interacción | API simulada |

## 6. Riesgos

- Las jornadas abiertas durante el despliegue quedan como `ENTREGAS`, sin riesgo para la operación actual.
- Sin una jornada `RECOJOS` abierta, los recojos esperan en la cola.

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Propuesta actual | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | Dónde vive el tipo | En la jornada, no en el repartidor; decisión confirmada por Max Rojas el 06/11/2026 | Max Rojas | No |
| DT-02 | Revisión del responsable de F-06 | Revisar antes de integrar a `develop` | Max Rojas con Kevin | Integración |

## 8. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
