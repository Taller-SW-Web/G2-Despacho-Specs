# ES-F06-09: Elegir el tipo de operación de la jornada

**Funcionalidad padre:** [F-06 — Disponibilidad y Capacidad Diaria](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), RF-05.

**Responsable:** Max Rojas; revisión de Kevin Rhamses Bohorquez (F-06) pendiente.

**Estado:** Borrador

**Actor principal:** Gestor de Despacho

**UI:** Aplica; apertura de jornada y monitoreo del panel administrativo.

**Servicio propietario:** Operación de Reparto y Flota.

## 1. Contexto y objetivo

Cada jornada es de entregas o de recojos, nunca de ambos. El Gestor lo elige al abrirla, así que una misma persona puede hacer entregas un día y recojos otro. La aplicación del repartidor usa ese dato para mostrar su trabajo.

## 2. Alcance

- Incluye: guardar y mostrar el tipo, filtrar la disponibilidad y rechazar reservas de otro tipo.
- Fuera de alcance: cambiar el tipo de una jornada abierta, mezclar ambos trabajos, asignar ([ES-F02-04](../ES-F02-04-AsignarDespachoRepartidor/spec.md) y [ES-F02-09](../ES-F02-09-RecibirAsignarRecojo/spec.md)) y operar en campo ([ES-F03-09](../ES-F03-09-RecojoDevolucion/spec.md)).

## 3. Actor, precondiciones y resultados

- Actor y autorización: Gestor con JWT de acceso y rol `GESTOR_DESPACHO`.
- Precondiciones: las de [ES-F06-01](../ES-F06-01-AbrirJornada/spec.md).
- Disparador: el Gestor confirma la apertura de una jornada.
- Resultado exitoso: jornada activa con `tipoOperacion`.
- Resultado ante rechazo: no se crea la jornada ni la reserva.

## 4. Flujo principal y alternativas

1. El Gestor elige repartidor, furgoneta, zona y tipo.
2. Operación crea la jornada con ese tipo.
3. La disponibilidad ofrece la jornada solo para su tipo de trabajo.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Cliente sin el campo | `tipoOperacion` no llega | Se usa `ENTREGAS` | CA-02 |
| Tipo no válido | Otro valor | `400` sin crear | CA-03 |
| Reserva cruzada | Trabajo y jornada de distinto tipo | `409` sin reservar | CA-05 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | El tipo es `ENTREGAS` o `RECOJOS` y no cambia después de abrir. | F-06 RF-05 |
| RN-02 | Las jornadas existentes quedan como `ENTREGAS`, sin otros cambios. | F-06 RF-05 |
| RN-03 | El panel exige elegir el tipo; la API usa `ENTREGAS` si se omite, para no romper a clientes actuales. | Decisión de esta especificación |
| RN-04 | Sin `tipoOperacion`, la disponibilidad devuelve solo jornadas `ENTREGAS`. | Decisión de esta especificación |
| RN-05 | Un despacho solo reserva en `ENTREGAS` y un recojo solo en `RECOJOS`. También aplica a transferencias. | F-06 CA-18 |
| RN-06 | La ocupación y el estado operativo se calculan igual en ambos tipos. | [ES-F06-04](../ES-F06-04-CalcularOcupacionEstado/spec.md) |

Contrato: [Operación §4.2.4](../../integraciones/api-contract-operacion-reparto.md#424-tipo-de-operación-de-la-jornada). Datos: [modelo §3.6](../../arquitectura/modelo-datos.md#36-recojos-de-devoluciones). Es una propuesta sujeta a revisión.

## 6. Criterios de aceptación

### CA-01. Apertura con tipo

- **DADO** recursos aptos.
- **CUANDO** el Gestor abre una jornada y elige «Recojos».
- **ENTONCES** se crea con `tipoOperacion=RECOJOS`, se audita y se muestra en el monitoreo.

### CA-02. Compatibilidad

- **DADO** una jornada abierta antes de este cambio, o una apertura sin `tipoOperacion`.
- **CUANDO** se consulta.
- **ENTONCES** su tipo es `ENTREGAS` y el resto de sus datos no cambia.

### CA-03. Tipo no válido

- **DADO** un `tipoOperacion` distinto de `ENTREGAS` y `RECOJOS`.
- **CUANDO** se solicita la apertura.
- **ENTONCES** se responde `400 DESP_ERROR_CAMPOS_INVALIDOS` sin crear la jornada.

### CA-04. Disponibilidad por tipo

- **DADO** jornadas disponibles de ambos tipos.
- **CUANDO** se consulta la disponibilidad con `tipoOperacion=RECOJOS`, o sin el parámetro.
- **ENTONCES** se devuelven solo jornadas `RECOJOS` o, sin el parámetro, solo `ENTREGAS`.

### CA-05. Reserva de otro tipo

- **DADO** un recojo y una jornada `ENTREGAS`, o un despacho y una jornada `RECOJOS`.
- **CUANDO** Gestión solicita la reserva o la transferencia.
- **ENTONCES** se responde `409 DESP_ERROR_TIPO_JORNADA_INCOMPATIBLE` sin reservar ni liberar.

### CA-06. Cierre con recojos pendientes

- **DADO** una jornada `RECOJOS` con un recojo `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor intenta cerrarla.
- **ENTONCES** se responde `409 DESP_ERROR_CONFLICTO_JORNADA` sin cambios.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: migración incremental y validación bajo el mismo bloqueo de reservas.
- No funcionales: los de F-06, sección 8.
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración y UI | Recursos aptos |
| CA-02 | Integración de migración | Jornada anterior en una base desechable |
| CA-03 | Integración | Valor no válido |
| CA-04 | Integración y UI | Jornadas de ambos tipos |
| CA-05 | Integración | Reserva y transferencia cruzadas |
| CA-06 | Integración | Jornada con recojo pendiente |

- [ ] Todos los criterios cuentan con resultados comprobables en `evidence.md`.
- [ ] Los documentos, el contrato y el comportamiento implementado son consistentes.
- [ ] La revisión del responsable de F-06 está registrada.

## 9. Referencias

1. [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), RF-05, CA-16 a CA-18.
2. [ES-F06-01](../ES-F06-01-AbrirJornada/spec.md), [ES-F06-03](../ES-F06-03-ConsultarDisponibilidad/spec.md) y [ES-F06-06](../ES-F06-06-ReservarCapacidad/spec.md).
3. Archivos de esta especificación: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
