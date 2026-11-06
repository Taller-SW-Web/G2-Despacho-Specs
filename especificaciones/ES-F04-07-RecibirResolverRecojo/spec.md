# ES-F04-07: Recibir en el centro y resolver un recojo

**Funcionalidad padre:** [F-04 — Entregas Fallidas](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-08.

**Responsable:** Max Rojas; revisión de Gerardo (F-04) pendiente.

**Estado:** Borrador

**Actor principal:** Gestor de Despacho

**UI:** Aplica; vista de recojos del panel administrativo.

**Servicio propietario:** Gestión de Despachos; Operación libera la capacidad.

## 1. Contexto y objetivo

Cuando el repartidor trae un producto, el Gestor confirma que llegó al centro. Cuando no pudo recogerlo, el Gestor decide si lo reprograma o lo cierra.

## 2. Alcance

- Incluye: listar los recojos `RECOGIDO` y `FALLIDO`, confirmar la recepción, reprogramar y cerrar.
- Fuera de alcance: reembolso o cambio (Ventas y Postventa), ejecutar el recojo ([ES-F03-09](../ES-F03-09-RecojoDevolucion/spec.md)) y asignarlo de nuevo ([ES-F02-09](../ES-F02-09-RecibirAsignarRecojo/spec.md)).

## 3. Actor, precondiciones y resultados

- Actor y autorización: Gestor con rol `GESTOR_DESPACHO`.
- Precondiciones: recojo `RECOGIDO` para recibir; `FALLIDO` para reprogramar o cerrar.
- Resultado exitoso: `RECIBIDO_EN_CENTRO`, `PENDIENTE_ASIGNACION` o `CERRADO_SIN_RECOJO`, con historial.
- Resultado ante rechazo: el recojo no cambia.

## 4. Flujo principal y alternativas

1. El Gestor abre la vista y ve los recojos por resolver.
2. En un recojo `RECOGIDO`, confirma la recepción; se solicita liberar la capacidad.
3. En uno `FALLIDO`, reprograma con una fecha futura o cierra con un motivo.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Estado no admitido | El recojo cambió | `409` sin cambios | CA-05 |
| Operación no disponible | La liberación falla | Recepción conservada y reintento | CA-06 |
| Reintento | Misma clave | Resultado original | CA-07 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | La recepción libera la reserva con `RECEPCION_EN_CENTRO`, mediante una solicitud durable. | [ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/spec.md) |
| RN-02 | Un recojo `FALLIDO` ya liberó su capacidad; reprogramar o cerrar no libera otra vez. | [ES-F03-09 RN-08](../ES-F03-09-RecojoDevolucion/spec.md) |
| RN-03 | No hay máximo automático de intentos; decide el Gestor. | [ES-F03-09 DT-03](../ES-F03-09-RecojoDevolucion/plan.md#7-decisiones-y-pendientes) |
| RN-04 | Un recojo de prueba no genera eventos hacia Ventas; uno real registra `RECOJO_RECIBIDO` o `RECOJO_CERRADO`. | [Contrato externo §7.4](../../integraciones/api-contract.md#74-solicitar-y-cancelar-el-recojo-de-una-devolución) |

Contrato: [Gestión §3.3](../../integraciones/api-contract-gestion-despachos.md#33-recojos-de-devoluciones). Es una propuesta sujeta a revisión.

## 6. Criterios de aceptación

### CA-01. Recojos por resolver

- **DADO** recojos en distintos estados.
- **CUANDO** el Gestor abre la vista.
- **ENTONCES** ve los `RECOGIDO` y `FALLIDO`, con su evidencia y motivo.

### CA-02. Recepción

- **DADO** un recojo `RECOGIDO`.
- **CUANDO** el Gestor confirma la recepción.
- **ENTONCES** pasa a `RECIBIDO_EN_CENTRO` y se solicita liberar su capacidad.

### CA-03. Reprogramación

- **DADO** un recojo `FALLIDO`.
- **CUANDO** el Gestor indica una fecha futura.
- **ENTONCES** vuelve a `PENDIENTE_ASIGNACION` con esa fecha y aparece en la cola.

### CA-04. Cierre

- **DADO** un recojo `FALLIDO`.
- **CUANDO** el Gestor lo cierra con un motivo.
- **ENTONCES** pasa a `CERRADO_SIN_RECOJO`.

### CA-05. Estado no admitido

- **DADO** un recojo en otro estado o con una versión obsoleta.
- **CUANDO** se envía una de estas acciones.
- **ENTONCES** se responde `409` sin cambios y la vista se actualiza.

### CA-06. Liberación pendiente

- **DADO** que Operación no responde al liberar.
- **CUANDO** se confirma la recepción.
- **ENTONCES** la recepción se conserva y la liberación se reintenta sin duplicarse.

### CA-07. Reintento idempotente

- **DADO** una respuesta perdida.
- **CUANDO** se repite la acción con la misma clave.
- **ENTONCES** se devuelve el resultado original sin duplicar el historial.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: paquete de recojos en Gestión; liberación con el patrón de [ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/plan.md).
- No funcionales: los de F-04.
- Pendientes: [plan.md, sección 5](./plan.md#5-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración y UI | Recojos en distintos estados |
| CA-02 a CA-05 | Integración y UI | Recojos `RECOGIDO` y `FALLIDO` |
| CA-06, CA-07 | Integración | Operación caída y respuesta perdida |

- [ ] Todos los criterios cuentan con resultados comprobables en `evidence.md`.
- [ ] Los documentos, el contrato y el comportamiento implementado son consistentes.
- [ ] La revisión del responsable de F-04 está registrada.

## 9. Referencias

1. [F-04](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-08, CA-19 a CA-21.
2. [ES-F03-09](../ES-F03-09-RecojoDevolucion/spec.md) y [ES-F02-09](../ES-F02-09-RecibirAsignarRecojo/spec.md).
3. Archivos de esta especificación: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
