# ES-F03-02: Consulta de la ruta de la jornada

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md)

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor

**UI:** Aplica; vista «Mi Ruta» de la web responsive del repartidor.

## 1. Contexto y objetivo

Mostrar al repartidor, en «Mi Ruta», solo sus despachos de la jornada en curso, ordenados por la secuencia definida en F-02, para que sepa qué entregar y en qué orden. Concreta RF-02 y la sección 8 (Protección de datos) de F-03.

## 2. Alcance

- Incluye: consulta de los despachos de la jornada del repartidor resuelto desde el token, su orden por secuencia, la protección de la dirección del destinatario y la bandeja de pendientes de regularización.
- Fuera de alcance: definición de secuencia, asignación, reasignación y cancelación (F-02); cálculo de rutas o navegación (se usan aplicaciones externas de mapas); regularización de despachos de jornadas anteriores; acceso y habilitación operativa (ES-F03-01).

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor autenticado según ES-F03-01, con rol `REPARTIDOR`, en turno o fuera de turno.
- Precondiciones: F-02 asignó los despachos con jornada y secuencia.
- Disparador: el repartidor abre «Mi Ruta».
- Resultado exitoso: lista ordenada de despachos de la jornada, mensaje de ruta vacía y, si existen, bandeja de pendientes de regularización.
- Resultado ante rechazo: `403 Forbidden` sin datos.

## 4. Flujo principal y alternativas

1. El repartidor abre «Mi Ruta».
2. El backend resuelve el repartidor desde el token.
3. El backend recupera sus despachos de la jornada en curso.
4. El backend excluye los `CANCELADO` y los reasignados a otro repartidor.
5. El frontend presenta la lista ordenada por secuencia con el indicador visual de estado.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Ruta vacía | Sin despachos en la jornada | Mensaje de ruta vacía | CA-02 |
| Ruta de otro repartidor | La petición incluye un identificador distinto al del token | `403 Forbidden` sin datos | CA-03 |
| Jornadas anteriores sin cierre | Despachos de fechas pasadas no cerrados por falla del corte automático | Bandeja de pendientes de regularización, sin operación | CA-04 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Solo se muestran despachos del repartidor resuelto desde el token y de la jornada en curso. | F-03 RF-02 |
| RN-02 | Se excluyen los despachos `CANCELADO` y los reasignados a otro repartidor. | F-03 CA-05 |
| RN-03 | El orden es la secuencia definida por F-02. | F-03 RF-02 |
| RN-04 | Cada elemento muestra código operativo interno, dirección, destinatario, estado, número de intento y posición en la secuencia. | F-03 CA-05 |
| RN-05 | La dirección solo se muestra en `ASIGNADO` o `EN_CAMINO`; no hay exportación ni copia masiva. | F-03 §8 |
| RN-06 | Un identificador de repartidor distinto al del token se rechaza con `403` sin exponer datos. | F-03 CA-07 |
| RN-07 | Los despachos de jornadas anteriores sin cierre no entran en la ruta vigente; van a la bandeja de pendientes de regularización y no pueden operarse. | F-03 CA-08 |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| F-02 Programación y Asignación | Jornada, secuencia, destinatario y dirección | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| F-05 Monitoreo de Flota | Resolución del repartidor | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| ES-F03-01 | Autenticación y modo operativo o de solo lectura | [ES-F03-01](../ES-F03-01-AccesoHabilitacionRepartidor/spec.md) |

## 6. Criterios de aceptación

### CA-01. Ruta del día

- **DADO** que el repartidor tiene despachos en la jornada actual.
- **CUANDO** abre «Mi Ruta».
- **ENTONCES** el sistema lista los despachos ordenados por secuencia con código operativo interno, dirección, destinatario, estado, número de intento y posición, y excluye los `CANCELADO` o reasignados a otro repartidor.

### CA-02. Jornada sin asignaciones

- **DADO** que el repartidor no tiene despachos en la jornada actual.
- **CUANDO** abre «Mi Ruta».
- **ENTONCES** el sistema muestra un mensaje de ruta vacía.

### CA-03. Ruta de otro repartidor

- **DADO** que un repartidor manipula la petición para consultar la ruta de otro.
- **CUANDO** el backend recibe un identificador distinto al resuelto desde su token.
- **ENTONCES** responde `403 Forbidden` sin exponer datos.

### CA-04. Despachos de jornadas anteriores

- **DADO** despachos de fechas anteriores sin cierre por una falla del corte automático.
- **CUANDO** el repartidor carga su ruta.
- **ENTONCES** el sistema no los incorpora a la ruta vigente, los muestra en la bandeja de pendientes de regularización y no permite operarlos.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: consulta de solo lectura; no modifica despachos ni publica eventos.
- No funcionales: protección de la dirección según RN-05; uso móvil.
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación

| Criterio | Tipo de comprobación | Datos o escenario |
|---|---|---|
| CA-01 | Integración y UI | Despachos en varios estados, uno `CANCELADO` y uno reasignado |
| CA-02 | Integración y UI | Repartidor sin despachos en la jornada |
| CA-03 | Seguridad | Petición con identificador de otro repartidor |
| CA-04 | Integración y UI | Despachos de una fecha anterior sin cierre |

Tareas en [tasks.md](./tasks.md); resultados en [evidence.md](./evidence.md).

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-02, CA-05 a CA-08 y sección 8.
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
3. Wireframe de la vista «Mi Ruta».
