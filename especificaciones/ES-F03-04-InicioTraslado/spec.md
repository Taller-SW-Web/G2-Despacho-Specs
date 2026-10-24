# ES-F03-04: Inicio de traslado del despacho

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md)

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor

**UI:** Aplica; acción «En camino» en la web responsive del repartidor.

## 1. Contexto y objetivo

Permitir que el repartidor declare que recogió el paquete y salió del centro de despacho, cambiando el despacho de `ASIGNADO` a `EN_CAMINO`. La transición confirma que el paquete está en su poder y fuera del centro, y deja trazabilidad de quién la ejecutó y cuándo. Concreta RF-04 y RF-11 de F-03.

## 2. Alcance

- Incluye: transición `ASIGNADO` → `EN_CAMINO`, validaciones de origen, turno y propiedad, idempotencia, historial y publicación del evento.
- Fuera de alcance: asignación, reasignación y cancelación (F-02); captura de GPS o seguimiento en tiempo real; operación sin conexión (cola local de cambios).

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor en turno, con perfil local activo y vinculado resuelto desde el `sub` del JWT; no se exige rol global `REPARTIDOR`.
- Precondiciones: el despacho está en `ASIGNADO`, asignado al repartidor del token y en la jornada en curso; el repartidor recogió el paquete sellado; existe conexión activa.
- Disparador: el repartidor pulsa «En camino».
- Resultado exitoso: despacho en `EN_CAMINO` con marca temporal del servidor, ejecutor y registro en el historial.
- Resultado ante rechazo: `409 Conflict` sin cambio de estado.

## 4. Flujo principal y alternativas

1. El repartidor pulsa «En camino».
2. El backend recibe la solicitud con clave de idempotencia y valida token, turno y propiedad.
3. El backend solicita a la máquina de estados común la transición `ASIGNADO` → `EN_CAMINO`.
4. El backend persiste en una misma transacción estado, marca temporal del servidor, ejecutor e historial.
5. El frontend actualiza la vista sin recargarla por completo.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Origen no permitido | Estado distinto de `ASIGNADO` | `409`; estado conservado | CA-02 |
| Reasignado o cancelado | F-02 lo reasignó o canceló mientras estaba en pantalla | `409`; aviso de despacho actualizado y refresco de la ruta | CA-03 |
| Fuera de turno | Repartidor `FUERA_DE_TURNO` | `409` (ES-F03-01 RN-05) | — |
| Sin conexión | La petición no llega al backend | Aviso de cambio no registrado, estado anterior conservado y reintento explícito | — |
| Reintento | Misma clave de idempotencia | Resultado original sin duplicar transición ni historial | — |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Solo se permite desde `ASIGNADO`; otro origen responde `409` y conserva el estado. | F-03 CA-13 |
| RN-02 | Un despacho reasignado o cancelado por F-02 responde `409`; la interfaz informa y refresca la ruta sin aplicar cambios. | F-03 CA-14 |
| RN-03 | F-02 solo puede cancelar mientras el despacho está en `ASIGNADO` y en el centro. | F-03 Anexo A |
| RN-04 | Un repartidor fuera de turno recibe `409`. | ES-F03-01 RN-05 |
| RN-05 | No modifica el contador de intentos. | F-03 RF-04 |
| RN-06 | Estado, marca temporal, ejecutor e historial se persisten en una misma transacción. | F-03 RF-11 |
| RN-07 | Una solicitud repetida con la misma clave devuelve el resultado original sin duplicar transición ni historial. | F-03 RF-11 |
| RN-08 | Sin conexión, la interfaz informa que el cambio no se registró, conserva el estado anterior y exige reintento explícito. | F-03 RF-11 |
| RN-09 | La transición responde en menos de 2 segundos en red 4G. | F-03 §7 |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| Máquina de estados e historial común | Transición y registro | Overview, sección 6; [diagrama de estados](../../arquitectura/diagrama-estados-despacho.md) |
| Ventas y Postventa | Recepción del evento de cambio de estado | Overview, RT-03 |
| F-02 | Estado de asignación y cancelación | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |

## 6. Criterios de aceptación

### CA-01. Inicio de traslado exitoso

- **DADO** un despacho en `ASIGNADO`.
- **CUANDO** el repartidor recoge el paquete, sale del centro y pulsa «En camino».
- **ENTONCES** el estado cambia a `EN_CAMINO` con marca temporal del servidor y repartidor ejecutor, y la vista se actualiza sin recargarse por completo.

### CA-02. Transición no permitida

- **DADO** un despacho ya `ENTREGADO`.
- **CUANDO** el repartidor intenta marcarlo «En camino».
- **ENTONCES** el backend responde `409 Conflict` y conserva el estado.

### CA-03. Despacho reasignado o cancelado durante la jornada

- **DADO** que F-02 reasignó el despacho a otro repartidor o lo canceló por anulación del pedido mientras seguía en pantalla.
- **CUANDO** el repartidor intenta operarlo.
- **ENTONCES** el backend responde `409 Conflict`, la interfaz informa que el despacho fue actualizado y refresca la ruta sin aplicar cambios.

### CA-04. Registro en el historial

- **DADO** una transición a `EN_CAMINO` aceptada.
- **CUANDO** se persiste.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual, marca temporal del servidor, estado anterior y estado nuevo.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: transición atómica con historial y publicación del evento.
- No funcionales: RN-09.
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación

| Criterio | Tipo de comprobación | Datos o escenario |
|---|---|---|
| CA-01 | Integración y UI | Despacho propio en `ASIGNADO`, repartidor en turno |
| CA-02 | Integración | Despacho en `ENTREGADO` |
| CA-03 | Integración y UI | Despacho reasignado y despacho cancelado tras cargar la vista |
| CA-04 | Integración | Transición aceptada; reintento con la misma clave |

Tareas en [tasks.md](./tasks.md); resultados en [evidence.md](./evidence.md).

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-04, RF-11, CA-12 a CA-14, CA-31 y Anexo A.
2. [Diagrama de estados del despacho](../../arquitectura/diagrama-estados-despacho.md).
3. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
