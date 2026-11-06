# ES-F02-09: Recibir y asignar un recojo

**Funcionalidad padre:** [F-02 — Programación y Asignación](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-10.

**Responsable:** Max Rojas; revisión de Tarqui (F-02) pendiente.

**Estado:** Borrador

**Actor principal:** Gestor de Despacho

**UI:** Aplica; cola y modal de asignación del panel administrativo.

**Servicio propietario:** Gestión de Despachos; Operación confirma la capacidad.

## 1. Contexto y objetivo

Un recojo debe llegar a la cola y asignarse a un repartidor con jornada de recojos para que aparezca en su aplicación. Mientras no haya acuerdo con Ventas y Postventa, el Gestor genera recojos de prueba sobre despachos simulados.

## 2. Alcance

- Incluye: generar un recojo de prueba, verlo en la cola y asignarlo a una jornada `RECOJOS`.
- Fuera de alcance: la solicitud real de Ventas ([contrato externo §7.4](../../integraciones/api-contract.md#74-solicitar-y-cancelar-el-recojo-de-una-devolución)), hasta acordarla; reordenar y reasignar recojos ([Pendientes](../../funcionalidades/pendiente.md)); ejecutar el recojo ([ES-F03-09](../ES-F03-09-RecojoDevolucion/spec.md)).

## 3. Actor, precondiciones y resultados

- Actor y autorización: Gestor con rol `GESTOR_DESPACHO`.
- Precondiciones: despacho `ENTREGADO` sin recojo activo; para asignar, una jornada `RECOJOS` activa con capacidad.
- Resultado exitoso: recojo `ASIGNADO`, con reserva y copia en la ruta del repartidor.
- Resultado ante rechazo: el recojo no cambia y no queda reserva.

## 4. Flujo principal y alternativas

1. El Gestor genera el recojo de prueba; queda en `PENDIENTE_ASIGNACION`.
2. La cola lo muestra con la etiqueta «Recojo».
3. El modal ofrece solo jornadas `RECOJOS`.
4. Al confirmar, Operación reserva la capacidad y el recojo pasa a `ASIGNADO`.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| No permitido | El despacho no está `ENTREGADO` o ya tiene recojo activo | `409` sin crear | CA-02 |
| Jornada de otro tipo | Jornada `ENTREGAS` | `409` sin reserva | CA-05 |
| Sin capacidad | La carga no cabe | `422` sin cambios | CA-06 |
| Reintento | Misma clave | Resultado original | CA-07 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Un despacho tiene como máximo un recojo activo. | [Modelo §3.6](../../arquitectura/modelo-datos.md#36-recojos-de-devoluciones) |
| RN-02 | Un recojo de prueba no genera eventos hacia Ventas. | [Contrato externo §7.4](../../integraciones/api-contract.md#74-solicitar-y-cancelar-el-recojo-de-una-devolución) |
| RN-03 | El recojo toma la siguiente posición de su jornada. | [ES-F03-09 DT-04](../ES-F03-09-RecojoDevolucion/plan.md#7-decisiones-y-pendientes) |
| RN-04 | La reserva usa el patrón durable de [ES-F02-04](../ES-F02-04-AsignarDespachoRepartidor/spec.md): fuera de la transacción local, con compensación. | ES-F02-04 |
| RN-05 | Toda transición queda en `historial_estados_recojo` en la misma transacción. | Modelo §3.6 |

Contratos: [Gestión §3.3](../../integraciones/api-contract-gestion-despachos.md#33-recojos-de-devoluciones) y [Operación §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación). Son una propuesta sujeta a revisión.

## 6. Criterios de aceptación

### CA-01. Recojo de prueba

- **DADO** un despacho simulado `ENTREGADO` sin recojo activo.
- **CUANDO** el Gestor genera el recojo.
- **ENTONCES** se crea en `PENDIENTE_ASIGNACION` sin eventos hacia Ventas.

### CA-02. Recojo no permitido

- **DADO** un despacho que no está `ENTREGADO`, o con un recojo activo.
- **CUANDO** se genera el recojo.
- **ENTONCES** se responde `409` sin crear otro.

### CA-03. Recojo en la cola

- **DADO** un recojo en `PENDIENTE_ASIGNACION`.
- **CUANDO** el Gestor abre la cola.
- **ENTONCES** lo ve con la etiqueta «Recojo», junto a los despachos pendientes.

### CA-04. Asignación

- **DADO** una jornada `RECOJOS` activa con capacidad.
- **CUANDO** el Gestor confirma la asignación.
- **ENTONCES** el recojo pasa a `ASIGNADO`, se reserva la capacidad, toma la siguiente posición y aparece en la ruta del repartidor.

### CA-05. Jornada de otro tipo

- **DADO** un recojo y una jornada `ENTREGAS`, o un despacho y una jornada `RECOJOS`.
- **CUANDO** se intenta asignar.
- **ENTONCES** se responde `409 DESP_ERROR_TIPO_JORNADA_INCOMPATIBLE`, sin cambios, y el modal no ofrece esa jornada.

### CA-06. Capacidad insuficiente

- **DADO** una jornada sin capacidad para la carga.
- **CUANDO** se confirma la asignación.
- **ENTONCES** se responde `422 DESP_ERROR_CAPACIDAD_EXCEDIDA` y el recojo sigue en la cola.

### CA-07. Reintento idempotente

- **DADO** una respuesta perdida.
- **CUANDO** se repite la asignación con la misma clave.
- **ENTONCES** se devuelve el resultado original, sin duplicar la reserva ni el historial.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: paquete nuevo de recojos en Gestión.
- No funcionales: los de F-02.
- Pendientes: [plan.md, sección 5](./plan.md#5-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01, CA-02 | Integración y UI | Despachos simulados en distintos estados |
| CA-03 | Integración y UI | Cola con despachos y recojos |
| CA-04 a CA-07 | Integración | Jornadas de ambos tipos, con y sin capacidad |

- [ ] Todos los criterios cuentan con resultados comprobables en `evidence.md`.
- [ ] Los documentos, el contrato y el comportamiento implementado son consistentes.
- [ ] La revisión del responsable de F-02 está registrada.

## 9. Referencias

1. [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-10, CA-28 a CA-31.
2. [ES-F06-09](../ES-F06-09-TipoOperacionJornada/spec.md) y [ES-F03-09](../ES-F03-09-RecojoDevolucion/spec.md).
3. Archivos de esta especificación: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
