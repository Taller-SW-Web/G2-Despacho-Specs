# ES-F01-08: Registrar la trazabilidad de la configuración

**Funcionalidad padre:** F-01 — Gestor de zonas geográficas y cotizador de envíos  
**Responsable:** Valqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Garantizar que cada cambio aceptado sobre zonas y tarifas deje un registro auditable que permita reconstruir qué se cambió, quién lo ejecutó y cuándo. La trazabilidad se genera automáticamente como parte de la operación de configuración y se apoya en las marcas de auditoría de las entidades y en el histórico de tarifas; no requiere una pantalla independiente de administración.

## 2. Actor y precondiciones

- El actor está autenticado con un JWT que incluye el rol `GESTOR_DESPACHO` al iniciar la operación de configuración.
- La creación, edición, activación, desactivación o alta de tarifa superó todas sus validaciones y será aceptada.
- La identidad del ejecutor procede del JWT y la marca temporal procede del servidor.
- Las marcas temporales se persisten en UTC y los registros son de solo inserción.

## 3. Flujo principal

1. El Gestor confirma la creación, edición, cambio de estado o alta de tarifa.
2. El caso de uso correspondiente valida la solicitud.
3. Antes de confirmar la transacción, el sistema prepara la auditoría con la entidad afectada, el tipo de operación, el ejecutor y la marca temporal.
4. La operación de negocio y su auditoría se persisten de manera consistente.
5. El registro queda disponible para revisión junto a la zona o a la tarifa.

## 4. Reglas y validaciones

- Toda operación aceptada produce exactamente un registro de auditoría.
- La auditoría de una zona incluye identificador, operación, usuario, marca temporal del servidor en UTC y los valores afectados.
- La auditoría de una tarifa incluye la zona, el identificador de la regla, si queda vigente o inactiva, el usuario y la marca temporal.
- La identidad del usuario nunca se toma de un campo libre enviado por el cliente.
- Una operación rechazada no se registra como una decisión de negocio aceptada.
- Una repetición idempotente de una operación no genera un segundo registro.
- Un cambio de estado que no modifica el estado vigente no genera auditoría adicional.
- Los registros no pueden editarse ni eliminarse desde las operaciones de esta funcionalidad.
- Las marcas temporales se almacenan en UTC y el orden de los registros se basa en la marca persistida por el servidor, no en el reloj del cliente.

## 5. Entradas, salidas e integraciones

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

- ES-F01-02, ES-F01-03 y ES-F01-04 originan los registros de esta especificación.
- Seguridad y Usuarios emite el JWT del cual se obtiene la identidad del ejecutor.
- Las rutas y respuestas se rigen por `integraciones/api-contract.md` [cite: 2].

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

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Crear una pantalla exclusiva para administrar auditorías.
- Editar o eliminar registros históricos.
- Registrar como exitosa una operación rechazada.
- Sustituir los logs técnicos, las métricas o las trazas de infraestructura.
- Auditar las consultas de los canales y las cotizaciones emitidas.

### Referencias

- [cite: 1] `funcionalidades/F-01-Gestor_ZonasGeograficas.md`, RF-01, RF-02, CA-16, CA-17, CA-18 y requisito de trazabilidad de la sección 8.
- [cite: 2] `integraciones/api-contract.md`, secciones 3.2, 9.1 y 14.
- [cite: 3] `arquitectura/modelo-datos.md`, tablas `zonas`, `tarifas_zona` y `auditoria_configuracion`.
- [cite: 4] `overview.md`, RT-02 sobre historial auditable.
- [cite: 5] `disenio/funcionalidades/f-01.md`, Pantalla 1, columna de última modificación.