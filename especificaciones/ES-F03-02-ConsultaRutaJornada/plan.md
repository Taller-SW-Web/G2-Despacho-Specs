# Plan de ES-F03-02: Consulta de la ruta de la jornada

**Responsable:** Max Rojas

**Estado:** Borrador

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-04 |
| UI | [ui.md](./ui.md), UI-01, UI-02 y CUI-01 a CUI-05 |
| Contrato | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| Funcionalidad | [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-02 y sección 8 |
| Dependencia | [ES-F03-01](../ES-F03-01-AccesoHabilitacionRepartidor/spec.md) |

## 2. Estrategia y responsabilidades

El backend filtra, ordena y protege los datos antes de responder; el frontend solo presenta lo recibido.

| Área | Responsabilidad |
|---|---|
| Web del repartidor | Lista, bandeja y estados |
| Backend de operación de reparto | Resolución desde el token, filtro por jornada, exclusiones, orden y ocultamiento de la dirección |
| F-02 | Jornada, secuencia, destinatario y dirección (externo) |
| F-05 | Resolución del repartidor (externo) |

## 3. Frontend

- Mostrar la ruta y la bandeja como secciones separadas.
- No reordenar ni filtrar localmente; respetar el orden recibido.
- Sin acciones de exportación o copia masiva.
- Antes del contrato cerrado se usan fixtures (con datos, vacío, pendientes, `403`).

## 4. Backend e integraciones

- Resolver el repartidor desde el token; rechazar con `403` un identificador distinto.
- Recuperar despachos de la jornada en curso; excluir `CANCELADO` y reasignados.
- Ordenar por la secuencia de F-02.
- Omitir la dirección en la respuesta fuera de `ASIGNADO` / `EN_CAMINO` (RN-05).
- Separar los despachos de jornadas anteriores sin cierre y marcarlos como no operables.
- Solo lectura; no publica eventos.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Lista y bandeja con fixtures | ES-F03-01 I-01, DT-03 | CUI-01 a CUI-05 |
| I-02 | Consulta backend probada | DT-01, DT-02, DT-04 | CA-01 a CA-04 |
| I-03 | Recorrido integrado | I-01, I-02 | CA-01 a CA-04 y CUI-01 a CUI-05 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 | Orden, campos y exclusiones correctos | F-02 real o doble identificado |
| CA-02 | Respuesta vacía con mensaje | Real |
| CA-03 | Identificador ajeno rechazado sin datos | Real |
| CA-04 | Despachos anteriores separados y no operables | F-02 real o doble identificado |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Responsable | Bloquea |
|---|---|---|---|
| DT-01 | Resuelta: la jornada en curso es la asignación activa del día según `America/Bogota` en Operación. | Contrato F-06 y backend | — |
| DT-02 | Resuelta para la ruta vigente: `GET /api/v1/repartidor/mi-ruta`; DTO con estado, posición, intentos y datos mínimos. El endpoint separado de regularización sigue pendiente. | Contrato de API | CA-04 |
| DT-03 | Resuelta: reutilizar `TarjetaDespacho` de componentes compartidos. | CR-16 | — |
| DT-04 | Resuelta: dirección y nombre solo en `ASIGNADO` o `EN_CAMINO`; regularización histórica no expone PII ni acciones. | Contrato F-03 | — |

## 8. Condiciones para cerrar

- [ ] Pendientes bloqueantes resueltos.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
