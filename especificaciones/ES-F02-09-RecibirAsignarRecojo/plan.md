# Plan de ES-F02-09: Recibir y asignar un recojo

**Responsable:** Max Rojas

**Estado:** Borrador; pendiente de revisión técnica.

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-07 |
| Contratos | [Gestión §3.3](../../integraciones/api-contract-gestion-despachos.md#33-recojos-de-devoluciones) y [Operación §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación) |
| Patrón reutilizado | [ES-F02-04](../ES-F02-04-AsignarDespachoRepartidor/plan.md) |

## 2. Estrategia y responsabilidades

| Área | Responsabilidad | Archivos o componentes previstos |
|---|---|---|
| Gestión | Crear, listar y asignar recojos | Paquete nuevo de recojos y migración |
| Operación | Reservar y recibir la copia | Paquete `jornadas` |
| Panel del Gestor | Cola y modal | `features/programacion` |

## 3. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Recojo de prueba y cola | Migración de [ES-F03-09](../ES-F03-09-RecojoDevolucion/plan.md) | CA-01 a CA-03 |
| I-02 | Asignación con reserva | I-01, [ES-F06-09](../ES-F06-09-TipoOperacionJornada/plan.md) | CA-04 a CA-07 |
| I-03 | Panel | I-01 | CUI-01 a CUI-03 |

## 4. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 a CA-03 | Pruebas HTTP con base desechable | Real |
| CA-04 a CA-07 | Pruebas HTTP con Operación simulada, y recorrido local | Simulada y real |
| CUI-01 a CUI-03 | Pruebas de interacción | API simulada |

## 5. Decisiones y pendientes

| ID | Decisión o pregunta | Propuesta actual | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | Solicitud real de Ventas | Fuera de este incremento hasta acordarla | Max Rojas con Ventas | Integración real |
| DT-02 | Revisión del responsable de F-02 | Revisar antes de integrar a `develop` | Max Rojas con Tarqui | Integración |

## 6. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
