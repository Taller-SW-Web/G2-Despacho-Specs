# ES-F02-08: Registrar la trazabilidad de las operaciones

**Funcionalidad padre:** [F-02 — Programación y asignación de despachos](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-04, CA-10 y requisito transversal RT-02.

**Responsable:** Tarqui.

**Estado:** Preparación SDD completada; implementación y verificación pendientes.

**Actor principal:** Sistema / Gestor de Despacho (mediante las operaciones que ejecuta).

**Servicio propietario:** Gestión de Despachos.

**UI:** No aplica una interfaz web propia ni formulario independiente. La auditoría se captura de forma interna y atómica dentro de cada transacción y se expone en la consulta de detalle del despacho ([api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación)); la ausencia de `ui.md` se justifica también en [plan.md](./plan.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md). Preparación del 16/10/2026; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

Toda acción operativa ejecutada sobre los despachos de F-02 (recepción, simulación, asignación, reordenamiento, reasignación y cancelación) debe dejar un rastro inmutable y auditable que permita reconstruir qué ocurrió, qué usuario o sistema externo ejecutó la acción, en qué instante UTC se procesó y cuáles fueron los recursos o balances asociados.

El objetivo es garantizar la captura atómica, la integridad y la inmutabilidad de la auditoría en todas las operaciones de F-02, dando cumplimiento al requisito transversal de trazabilidad (RT-02), sin duplicar tablas de auditoría ni requerir una transacción manual separada [cite: 1].

## 2. Alcance

- Incluye: registro atómico en la tabla `historial_estados_despacho` para cada operación de recepción, simulación, asignación, reordenamiento, reasignación y cancelación; captura de usuario (humano vía JWT o identificador de servicio externo), marca temporal precisa en UTC, estado anterior, estado nuevo, observaciones, y variables operativas (repartidor, jornada, secuencia, ocupación vehicular); atomicidad transaccional estricta (rollback de la operación si la auditoría falla); inmutabilidad del historial (prohibición de `UPDATE` o `DELETE`).
- Fuera de alcance: pantallas o formularios exclusivos para auditar; auditoría interna de otros servicios (Operación o Ventas); alteración o borrado de eventos pasados.

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- La operación de negocio que origina el registro (ES-F02-01 a ES-F02-07) ha validado exitosamente sus precondiciones y se encuentra dentro de su bloque `@Transactional`.
- La identidad del usuario ejecutor se extrae del contexto de seguridad autenticado (`SecurityContextHolder` o token de servicio).
- La marca temporal se genera en el servidor en tiempo universal coordinado (UTC).

### 3.2. Dependencias

- **Operaciones de negocio de F-02:** ES-F02-01 (Recepción), ES-F02-02 (Simulación), ES-F02-04 (Asignación), ES-F02-05 (Reordenamiento), ES-F02-06 (Reasignación), ES-F02-07 (Cancelación).
- **Componente común de auditoría (RT-02):** gestiona el repositorio de `historial_estados_despacho`.
- **Detalle de despacho:** expone el historial en `GET /api/v1/despachos/{idDespacho}`.

### 3.3. Resultados

- Entrada inmutable persistida en `historial_estados_despacho` dentro de la misma transacción de base de datos.
- Reconstrucción cronológica exacta del ciclo de vida del despacho disponible para auditorías o consultas operativas.

## 4. Flujo principal y alternativas

1. Una operación de negocio de F-02 se ejecuta válidamente (ej. asignación de despacho).
2. El servicio de aplicación invoca el componente transversal `AuditoriaService.registrar()`.
3. Se extrae el usuario autenticado (ej. `gestor.logistica@empresa.com` o `sub=modulo-ventas`).
4. Se instancia el registro inmutable con marca temporal UTC, despacho, estado anterior, estado nuevo, jornada, repartidor, secuencia, observaciones y balance resultante.
5. Se inserta en PostgreSQL dentro de la transacción activa.
6. Si la persistencia de la auditoría es exitosa, la transacción completa confirma (`commit`).

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Fallo en persistencia de auditoría | Error de base de datos al insertar el historial | Toda la transacción de negocio se revierte (`rollback`), impidiendo operaciones huérfanas | CA-06 |
| Operación rechazada | La operación de negocio falla por validación (400, 409, 422) | No se genera ninguna entrada de historial de negocio exitoso | CA-06 |
| Consulta de historial | Gestor consulta el detalle de un despacho | Retorna la lista cronológica de eventos de auditoría ordenados por fecha ascendente | CA-01 a CA-05 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Inmutabilidad: los registros de auditoría son de solo inserción (`INSERT-only`); no existen métodos de edición o borrado. | RT-02, F-02 RF-04 |
| RN-02 | Atomicidad: la auditoría se guarda en la misma transacción `@Transactional` de la mutación; si falla, la mutación se deshace. | F-02 RF-04, CA-10 |
| RN-03 | Las marcas temporales se guardan obligatoriamente en UTC (`Instant.now()`). | F-02 RNF Trazabilidad |
| RN-04 | El ejecutor se obtiene del token verificado, no de campos manipulables enviados en el body. | F-02 RNF Seguridad |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| Tabla `historial_estados_despacho` | Tabla relacional compartida de auditoría. | [modelo-datos.md §3.1](../../arquitectura/modelo-datos.md#31-entidad-despachos) |
| `GET /api/v1/despachos/{idDespacho}` | Exposición del historial de auditoría al Gestor. | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) |

## 6. Criterios de aceptación

### CA-01. Registro atómico de auditoría en recepción y creación

- **DADO** una solicitud de creación de despacho procesada exitosamente (sea real de Ventas o simulada).
- **CUANDO** culmina la transacción de creación.
- **ENTONCES** se persiste una entrada en el historial con estado anterior nulo, estado nuevo `PENDIENTE_ASIGNACION`, usuario o servicio emisor, marca temporal exacta en UTC y observaciones.

### CA-02. Registro atómico de auditoría en asignación

- **DADO** que una asignación a repartidor es aceptada.
- **CUANDO** finaliza la transacción en el backend.
- **ENTONCES** se registra una entrada con estado anterior `PENDIENTE_ASIGNACION`, estado nuevo `ASIGNADO`, identificador del repartidor, jornada, posición de secuencia de ruta, usuario gestor, fecha UTC y balance de capacidad vehicular resultante.

### CA-03. Registro atómico de auditoría en reordenamiento de ruta

- **DADO** que se confirma un nuevo orden en la secuencia de ruta de una jornada.
- **CUANDO** se persiste la mutación.
- **ENTONCES** se genera un registro de auditoría indicando la jornada, el usuario gestor, la marca temporal UTC y la lista de despachos afectados con sus posiciones anterior y nueva.

### CA-04. Registro atómico de auditoría en reasignación de despacho

- **DADO** una reasignación confirmada entre dos repartidores.
- **CUANDO** finaliza la transacción.
- **ENTONCES** se persiste un registro que especifica el repartidor y jornada origen, el repartidor y jornada destino, el usuario gestor, la nueva secuencia y el motivo obligatorio de la reasignación.

### CA-05. Registro atómico de auditoría en cancelación

- **DADO** una cancelación procesada por anulación de pedido desde Ventas.
- **CUANDO** se confirma el cambio en base de datos.
- **ENTONCES** se registra la transición al estado resultante (`CANCELADO` o la marca `pedidoAnulado = true` en `FALLIDO`), el sistema emisor `modulo-ventas`, la marca temporal UTC y el motivo comercial.

### CA-06. Inmutabilidad e integridad transaccional

- **DADO** una operación de negocio de F-02 donde la inserción en la tabla de auditoría genera una excepción.
- **CUANDO** la capa de persistencia procesa el fallo.
- **ENTONCES** la transacción completa se revierte (`rollback`), no se persiste ningún cambio en el despacho y no se permite ninguna modificación o eliminación sobre registros de auditoría preexistentes.

## 7. Referencias

1. [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md): requisito RF-04 y criterio CA-10.
2. [overview.md §6](../../overview.md): requisito transversal RT-02 de auditoría.
3. [modelo-datos.md §3.1](../../arquitectura/modelo-datos.md#31-entidad-despachos): definición de la tabla de historial de estados.
