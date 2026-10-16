# ES-F03-07: Cierre de jornada y resumen del día

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md)

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor; proceso programado en el corte automático.

**UI:** Aplica; cierre de jornada y resumen del día de la web responsive del repartidor.

## 1. Contexto y objetivo

Garantizar que ningún despacho quede en `ASIGNADO` ni `EN_CAMINO` al terminar la jornada. Los pendientes pasan a `FALLIDO` con motivo `NO_INTENTADO` sin consumir intentos, para distinguirlos de los intentos reales. El cierre lo ejecuta el repartidor o, si no lo hace, un corte automático a la hora configurada. El repartidor puede consultar el resumen de su jornada al cerrar y en cualquier momento del día. Concreta RF-07, RF-08, RF-11, la sección 7 y el Anexo A de F-03.

## 2. Alcance

- Incluye: cierre manual con advertencia, corte automático de respaldo, transición masiva a `FALLIDO` / `NO_INTENTADO`, solicitud de cierre de turno a F-05, lista de paquetes a devolver y resumen de la jornada.
- Fuera de alcance: recepción física de los paquetes devueltos (F-04); gestión de jornadas y turnos más allá de solicitar el cierre (F-05); definición del valor de la hora de corte; regularización de despachos que el corte no logró cerrar; reportes de flota o de otros repartidores y exportación del resumen.

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor en turno con rol `REPARTIDOR` (cierre manual); proceso programado del módulo (corte automático). El resumen se consulta también fuera de turno (ES-F03-01).
- Precondiciones: asignación diaria activa; hora de corte configurada; conexión activa (cierre manual).
- Disparador: el repartidor pulsa «Cerrar jornada», o llega la hora de corte.
- Resultado exitoso: pendientes en `FALLIDO` / `NO_INTENTADO` con historial, repartidor en `FUERA_DE_TURNO`, lista de paquetes a devolver y resumen.

## 4. Flujo principal y alternativas

1. El repartidor pulsa «Cerrar jornada».
2. El sistema identifica los despachos de la jornada en `ASIGNADO` o `EN_CAMINO` y advierte cuántos quedarán como no intentados.
3. El repartidor confirma.
4. El backend recibe la solicitud con clave de idempotencia y pasa cada pendiente a `FALLIDO` con motivo `NO_INTENTADO`, sin incrementar el contador, registrando cada transición en el historial.
5. El backend solicita a F-05 el cierre del turno; el repartidor pasa a `FUERA_DE_TURNO`.
6. El frontend lista los paquetes a devolver al centro y muestra el resumen.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Sin pendientes | Ningún despacho en `ASIGNADO` ni `EN_CAMINO` | Solo se registra el cierre; sin fallos | CA-02 |
| Corte automático | El repartidor no cerró antes de la hora de corte | El proceso ejecuta los pasos 4 y 5 por cada repartidor; origen automático | CA-03 |
| Corte fallido | El corte no se ejecuta o no completa | Los despachos abiertos aparecen al día siguiente como pendientes de regularización (ES-F03-02 CA-04) | — |
| Sin conexión | La solicitud no llega al backend | Aviso de cierre no registrado y reintento explícito | — |
| Reintento | Misma clave de idempotencia | Resultado original sin duplicar transiciones | — |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | El cierre se permite con o sin pendientes; sin pendientes no se generan fallos. | F-03 CA-25 |
| RN-02 | `NO_INTENTADO` no requiere fotografía ni incrementa el contador de intentos. | F-03 Anexo B |
| RN-03 | Los despachos `NO_INTENTADO` quedan disponibles para F-04. | F-03 RF-07 |
| RN-04 | Estado e historial de cada despacho se persisten en una misma transacción. | F-03 RF-11 |
| RN-05 | En el corte automático, el ejecutor es el proceso automático y el origen es automático. | F-03 CA-24 |
| RN-06 | Los despachos ya resueltos no se reprocesan; repetir el corte no genera transiciones adicionales. | F-03 RF-07 |
| RN-07 | Repetir el cierre manual con la misma clave devuelve el resultado original sin duplicar transiciones. | F-03 RF-11 |
| RN-08 | Sin conexión, la interfaz informa que el cierre no se registró y exige reintento explícito. | F-03 RF-11 |
| RN-09 | El resumen muestra asignados, entregados, fallidos con intento, no intentados y pendientes, coincidentes con el historial. | F-03 CA-26 |
| RN-10 | El resumen es solo del propio repartidor y se consulta también fuera de turno. | F-03 RF-08 |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| F-05 Monitoreo de Flota | Cierre del turno | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| F-04 Entregas Fallidas | Consume los despachos `NO_INTENTADO` | F-04 |
| Máquina de estados, historial y eventos | Transiciones, registro y publicación | Overview, sección 6, RT-02 y RT-03 |

## 6. Criterios de aceptación

### CA-01. Cierre con despachos pendientes

- **DADO** despachos en `ASIGNADO` o `EN_CAMINO` al terminar el turno.
- **CUANDO** el repartidor confirma el cierre, advertido de la cantidad de despachos afectados.
- **ENTONCES** esos despachos pasan a `FALLIDO` con motivo `NO_INTENTADO` sin incrementar el contador, la interfaz lista los paquetes que debe devolver al centro, quedan disponibles para F-04 y F-05 pone al repartidor en `FUERA_DE_TURNO`.

### CA-02. Cierre sin pendientes

- **DADO** que ningún despacho de la jornada está en `ASIGNADO` ni `EN_CAMINO`.
- **CUANDO** el repartidor confirma el cierre.
- **ENTONCES** se registra el cierre, el repartidor pasa a `FUERA_DE_TURNO` y se muestra el resumen sin generar fallos.

### CA-03. Corte automático de respaldo

- **DADO** que el repartidor no cerró su jornada antes de la hora de corte configurada.
- **CUANDO** se ejecuta el proceso automático.
- **ENTONCES** se aplica el tratamiento de CA-01 y el historial identifica la operación como automática.

### CA-04. Consolidado correcto del resumen

- **DADO** un repartidor con despachos en distintos estados.
- **CUANDO** consulta el resumen.
- **ENTONCES** ve total asignado, entregados, fallidos con intento, no intentados y pendientes, coincidentes con el historial.

### CA-05. Registro en el historial

- **DADO** un despacho resuelto como `NO_INTENTADO` por el cierre manual o el corte automático.
- **CUANDO** se persiste la transición.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual o automático, marca temporal del servidor, estado anterior, estado nuevo y motivo `NO_INTENTADO`.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: cierre manual, proceso programado y consulta del resumen.
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación

| Criterio | Tipo de comprobación | Datos o escenario |
|---|---|---|
| CA-01 | Integración y UI | Despachos en `ASIGNADO`, `EN_CAMINO` y `ENTREGADO` |
| CA-02 | Integración y UI | Jornada sin pendientes |
| CA-03 | Integración | Hora de corte alcanzada sin cierre manual; ejecución repetida |
| CA-04 | Integración y UI | Despachos en todos los estados finales y pendientes |
| CA-05 | Integración | Cierre manual y automático |

Tareas en [tasks.md](./tasks.md); resultados en [evidence.md](./evidence.md).

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-07, RF-08, RF-11, CA-23 a CA-26, CA-31, sección 7 y Anexo A.
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
3. Wireframes del cierre y del resumen de jornada.
