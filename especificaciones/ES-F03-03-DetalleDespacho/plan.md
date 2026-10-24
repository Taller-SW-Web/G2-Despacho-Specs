# Plan de ES-F03-03: Consulta del detalle de un despacho

**Responsable:** Max Rojas

**Estado:** Borrador

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-03 |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-04 |
| Contrato | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| Funcionalidad | [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-03 y sección 8 |
| Dependencias | [ES-F03-01](../ES-F03-01-AccesoHabilitacionRepartidor/spec.md) y [ES-F03-02](../ES-F03-02-ConsultaRutaJornada/spec.md) |

## 2. Estrategia y responsabilidades

El backend verifica propiedad y filtra los datos personales según estado antes de responder; el frontend solo presenta lo recibido.

| Área | Responsabilidad |
|---|---|
| Web del repartidor | Vista de detalle, llamada directa y estados |
| Backend de operación de reparto | Propiedad, `403` / `404` y omisión de teléfono y dirección según RN-02 |
| F-02 | Datos del despacho (externo) |
| Ventas y Postventa | Teléfono y referencia (externo, Anexo C n.º 2) |

## 3. Frontend

- Navegación desde «Mi Ruta» por código del despacho.
- Llamada directa con enlace `tel:`.
- Acciones visibles según estado y modo de ES-F03-01.
- Fixtures antes del contrato cerrado (estados `ASIGNADO`, `EN_CAMINO`, `ENTREGADO`, `403`, `404`).

## 4. Backend e integraciones

- Resolver el repartidor desde el token y verificar la propiedad del despacho.
- Responder `404` sin datos parciales para códigos inexistentes.
- Omitir teléfono y dirección fuera de `ASIGNADO` / `EN_CAMINO`.
- Solo lectura; no publica eventos.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Detalle con fixtures | ES-F03-02 I-01, DT-03 | CUI-01 a CUI-04 |
| I-02 | Consulta backend probada | DT-01, DT-02 | CA-01 a CA-03 |
| I-03 | Recorrido integrado | I-01, I-02 | CA-01 a CA-03 y CUI-01 a CUI-04 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 | Campos completos y protección por estado | F-02 real o doble identificado |
| CA-02 | Despacho ajeno rechazado | Real |
| CA-03 | Código inexistente sin datos parciales | Real |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Responsable | Bloquea |
|---|---|---|---|
| DT-01 | Resuelta: teléfono y referencia llegan en la proyección F-02 desde Gestión; Operación no consulta Ventas directamente. | Contrato F-02/F-03 | — |
| DT-02 | Resuelta: `MAXIMO_INTENTOS` es propiedad de Gestión y se propaga en la proyección; proyecciones anteriores pueden carecer del valor hasta actualizarse. | Parámetro canónico de Gestión | — |
| DT-03 | Resuelta: reutilizar `TarjetaDespacho` para navegación desde ruta; el detalle usa los componentes Mantine existentes. | CR-16 | — |
| DT-04 | Resuelta: un despacho ajeno o fuera de la jornada activa responde `404` sin datos parciales. | Contrato de API | — |

## 8. Condiciones para cerrar

- [ ] Pendientes bloqueantes resueltos.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
