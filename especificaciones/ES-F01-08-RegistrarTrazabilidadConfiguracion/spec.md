# ES-F01-08: Registrar la trazabilidad de la configuración

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Gestor de Despacho

**UI:** No aplica. Es la captura automática de cambios; la última modificación y las vistas de configuración se mantienen en las UI de ES-F01-01 a ES-F01-04, sin interacción visual nueva en esta especificación.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación de la revisión `91db8f8`, migrada al flujo SDD el 16/10/2026; conserva los criterios CA-01 a CA-06.

## 1. Contexto y objetivo

Garantizar que cada cambio aceptado sobre zonas y tarifas deje un registro auditable que permita reconstruir qué se cambió, quién lo ejecutó y cuándo. La trazabilidad se genera automáticamente como parte de la operación de configuración y se apoya en las marcas de auditoría de las entidades y en el histórico de tarifas; no requiere una pantalla independiente de administración.

## 2. Alcance

- Incluye: capturar cambios aceptados de zonas y tarifas con identidad y fecha confiables; conservar el histórico y evitar auditorías duplicadas.
- Fuera de alcance: pantalla exclusiva de auditoría; edición o eliminación del histórico; registro de rechazos como éxitos; sustitución de logs, métricas o trazas; auditoría de consultas y cotizaciones.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con un JWT que incluye el rol `GESTOR_DESPACHO` al iniciar la operación de configuración.
- La creación, edición, activación, desactivación o alta de tarifa superó todas sus validaciones y será aceptada.
- La identidad del ejecutor procede del JWT y la marca temporal procede del servidor.
- Las marcas temporales se persisten en UTC y los registros son de solo inserción.
- Disparador: una operación de configuración válida está lista para confirmarse.
- Resultado exitoso: negocio y auditoría persistidos de manera consistente, con un registro por operación aceptada.
- Resultado ante rechazo o fallo transaccional: no queda auditoría que presente como aceptado un cambio no confirmado.

## 4. Flujo principal y alternativas

1. El Gestor confirma la creación, edición, cambio de estado o alta de tarifa.
2. El caso de uso correspondiente valida la solicitud.
3. Antes de confirmar la transacción, el sistema prepara la auditoría con la entidad afectada, el tipo de operación, el ejecutor y la marca temporal.
4. La operación de negocio y su auditoría se persisten de manera consistente.
5. El registro queda disponible para revisión junto a la zona o a la tarifa.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Rechazo | Incumple una regla de negocio | No genera auditoría de operación aceptada | CA-04 |
| Repetición | Misma operación ya aceptada | Conserva un único registro | CA-05 |
| Estado sin cambio | El estado solicitado ya está vigente | Sin auditoría adicional | Regla de no duplicación |
| Mutación del histórico | Intento de editar o eliminar registros | Operación no disponible; registros inalterados | CA-06 |

## 5. Reglas, datos e integraciones

### Reglas y validaciones

- Toda operación aceptada produce exactamente un registro de auditoría.
- La auditoría de una zona incluye identificador, operación, usuario, marca temporal del servidor en UTC y los valores afectados.
- La auditoría de una tarifa incluye la zona, el identificador de la regla, si queda vigente o inactiva, el usuario y la marca temporal.
- La identidad del usuario nunca se toma de un campo libre enviado por el cliente.
- Una operación rechazada no se registra como una decisión de negocio aceptada.
- Una repetición idempotente de una operación no genera un segundo registro.
- Un cambio de estado que no modifica el estado vigente no genera auditoría adicional.
- Los registros no pueden editarse ni eliminarse desde las operaciones de esta funcionalidad.
- Las marcas temporales se almacenan en UTC y el orden de los registros se basa en la marca persistida por el servidor, no en el reloj del cliente.

### Entradas

- Identificador de la zona o de la tarifa afectada.
- Tipo de operación aceptada: creación, edición, activación, desactivación o alta de tarifa.
- Valores modificados o registrados.
- Identidad autenticada del ejecutor.
- Marca temporal del servidor.

### Salidas

- Un registro de auditoría asociado a la zona o a la tarifa.
- Historial de tarifas vigente e inactivas consultable.
- Evidencia suficiente para verificar la secuencia de cambios de configuración.

### Integraciones

- [ES-F01-02](../ES-F01-02-RegistrarZonaCobertura/spec.md), [ES-F01-03](../ES-F01-03-ActivarDesactivarZona/spec.md) y [ES-F01-04](../ES-F01-04-ConfigurarTarifaZona/spec.md) originan los registros de esta especificación.
- Seguridad y Usuarios emite el JWT del cual se obtiene la identidad del ejecutor.
- Las operaciones administrativas se definen en el [contrato de Gestión §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas) y las convenciones compartidas del contrato externo [cite: 2]. El contrato no define aún una consulta específica del histórico de tarifas o de auditoría; su exposición queda pendiente, sin inventar una ruta en esta carpeta.

## 6. Criterios de aceptación

### CA-01. Registro de una creación de zona

- **DADO** una creación de zona aceptada.
- **CUANDO** se confirma la operación.
- **ENTONCES** se registra la zona, la operación, el usuario y la marca temporal del servidor en UTC.

### CA-02. Registro de un cambio de estado

- **DADO** una activación o desactivación aceptada.
- **CUANDO** se confirma el cambio.
- **ENTONCES** se registra la zona, el estado anterior, el nuevo, el usuario y la marca temporal.

### CA-03. Registro de un alta de tarifa

- **DADO** una nueva tarifa guardada para una zona que ya tenía una regla vigente.
- **CUANDO** se confirma la operación.
- **ENTONCES** se registra la nueva regla como vigente, la anterior como inactiva y el usuario y la marca temporal de ambas.

### CA-04. Operación rechazada

- **DADO** una operación de configuración que incumple una regla de negocio.
- **CUANDO** el backend rechaza la solicitud.
- **ENTONCES** no se crea un registro que la presente como operación aceptada.

### CA-05. Repetición idempotente

- **DADO** una operación aceptada que ya posee su registro de auditoría.
- **CUANDO** se repite exactamente la misma solicitud.
- **ENTONCES** no se crea un segundo registro de configuración.

### CA-06. Integridad de los registros

- **DADO** registros de configuración existentes.
- **CUANDO** se intenta editarlos o eliminarlos desde las operaciones de esta funcionalidad.
- **ENTONCES** la operación no está disponible y los registros permanecen inalterados.

## 7. UI, backend y requisitos no funcionales

- UI: no aplica; no se añade una pantalla ni se modifica el comportamiento visual. Las UI existentes de catálogo y configuración son responsables de presentar última modificación e información autorizada. No se incluye `ui.md`.
- Backend: registro interno dentro de la transacción local de configuración, con valores anteriores/nuevos e histórico tarifario conservado por sustitución.
- Requisitos no funcionales: identidad del JWT, reloj del servidor, instantes UTC, inmutabilidad y consistencia entre cambio y auditoría [cite: 1, 3].
- Pendientes: identidad de operaciones repetidas, representación de sustituciones de tarifa y consulta del histórico; detalle y responsables en [plan.md §7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración transaccional | Creación de zona aceptada con JWT conocido |
| CA-02 | Integración | Activación/desactivación y estados anterior/nuevo |
| CA-03 | Integración | Sustitución de una regla vigente por otra |
| CA-04 | Integración de rechazos | Operación inválida sin cambio ni auditoría de éxito |
| CA-05 | Integración de repetición | Solicitud ya aceptada y duplicado concurrente |
| CA-06 | Integridad | Intentos de modificar o borrar el histórico desde la funcionalidad |

- [ ] CA-01 a CA-06 cuentan con evidencia reproducible en [evidence.md](./evidence.md).
- [ ] Se verifican edición de zona, estado sin cambio y reversión ante fallo de auditoría.
- [ ] Histórico, consulta autorizada e idempotencia respetan el contrato y el modelo revisados.
- [ ] Commits y revisión funcional y técnica están enlazados.

El trabajo está en [tasks.md](./tasks.md); la migración documental no acredita implementación.

## 9. Referencias

- [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-01, RF-02, CA-16, CA-17, CA-18 y trazabilidad de §8.
- [cite: 2] [Contrato de Gestión §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas); [roles §3.3](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio) e [idempotencia §9](../../integraciones/api-contract.md#9-reglas-de-idempotencia-y-concurrencia).
- [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), tablas `zonas`, `tarifas_zona` y `auditoria_configuracion`.
- [cite: 4] [Visión general](../../overview.md), RT-02 sobre historial auditable.
- [cite: 5] [Diseño de F-01](../../disenio/funcionalidades/f-01.md), Pantalla 1, columna de última modificación.
- Documentos SDD: [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
