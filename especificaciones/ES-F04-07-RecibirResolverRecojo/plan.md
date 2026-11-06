# Plan de ES-F04-07: Recibir en el centro y resolver un recojo

**Responsable:** Max Rojas

**Estado:** Borrador; pendiente de revisión técnica.

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-07 |
| Contrato | [Gestión §3.3](../../integraciones/api-contract-gestion-despachos.md#33-recojos-de-devoluciones) |
| Patrones reutilizados | [ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/plan.md), [ES-F04-04](../ES-F04-04-ReprogramarDespachoFallido/plan.md) y [ES-F04-05](../ES-F04-05-CerrarDespachoComoDevueltoAOrigen/plan.md) |

## 2. Estrategia y responsabilidades

| Área | Responsabilidad | Archivos o componentes previstos |
|---|---|---|
| Gestión | Lista, recepción, reprogramación y cierre | Paquete de recojos |
| Operación | Liberar la reserva | `POST /internal/v1/capacidad/reservas/{id}/liberacion` |
| Panel del Gestor | Vista y modales | Sección nueva de recojos |

## 3. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Lista y acciones en Gestión | [ES-F03-09](../ES-F03-09-RecojoDevolucion/plan.md), I-02 | CA-01 a CA-05, CA-07 |
| I-02 | Liberación durable | I-01 | CA-02, CA-06 |
| I-03 | Vista del panel | I-01 | CUI-01 a CUI-03 |

## 4. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 a CA-05, CA-07 | Pruebas HTTP con base desechable | Real |
| CA-06 | Prueba con Operación simulada caída | Simulada |
| CUI-01 a CUI-03 | Pruebas de interacción | API simulada |

## 5. Decisiones y pendientes

| ID | Decisión o pregunta | Propuesta actual | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | Revisión del responsable de F-04 | Revisar antes de integrar a `develop` | Max Rojas con Gerardo | Integración |

## 6. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
