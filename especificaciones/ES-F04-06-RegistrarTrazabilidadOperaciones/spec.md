# ES-F04-06: Registrar la trazabilidad de las operaciones

**Funcionalidad padre:** [F-04 — Entregas fallidas y reprogramaciones](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-05 y CA-13.

**Responsable:** Gerardo.

**Estado:** Preparación SDD completada; implementación y verificación pendientes.

**Actor principal:** Gestor de Despacho, mediante la operación de negocio que confirma. **Servicio propietario:** Gestión de Despachos.

**UI:** No aplica una interfaz nueva ni un cambio visual propio. La captura es interna y el historial ya se presenta en ES-F04-02; la ausencia de `ui.md` se justifica también en [plan.md](./plan.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md). Preparación del 16/10/2026 sobre la revisión funcional `c8e6e29`; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

Las recepciones, reprogramaciones y cierres de F-04 ya incluyen su historial dentro de la operación de negocio. Esta especificación concreta las garantías comunes de esos mismos registros y aplica el historial único de RT-02; no registra una segunda auditoría ni ejecuta un proceso posterior al éxito de la operación [cite: 1].

Permitir reconstruir qué operación se aceptó, sobre qué despacho/incidencia, quién la confirmó, cuándo y con qué resultado. La captura es automática dentro de la transacción que origina la decisión y la consulta se integra en el detalle del despacho.

## 2. Alcance

- Incluye un registro inmutable por recepción, reprogramación o cierre nuevo aceptado, sus datos históricos, vínculo con incidencia y garantías de atomicidad, idempotencia y consulta.
- Reutiliza el componente transversal y `historial_estados_despacho`, compartidos por las funcionalidades del mismo servicio Gestión, sin duplicar registros ni tablas de auditoría.
- ES-F04-01/02 consultan información; sus lecturas no generan decisiones ni entradas de historial.
- Reintentos técnicos de liberación y comunicación con Ventas mantienen sus solicitudes/eventos existentes, sin crear otra operación de negocio.
- Tipos, campos, nulabilidad, orden y datos expuestos se rigen por [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02); esta especificación no crea otro contrato HTTP [cite: 2].

### 2.1. Fuera de alcance

- Crear pantalla, endpoint o tabla exclusivos para auditar F-04.
- Editar/eliminar historiales, registrar rechazos como decisiones aceptadas o sustituir logs, métricas y trazas técnicas.
- Cambiar precondiciones, transiciones, respuestas o eventos de ES-F04-03/04/05.
- Definir auditoría interna de Ventas, alterar su contrato o gestionar reembolsos/stock.

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- La operación de origen tiene un Gestor autenticado y autorizado con `GESTOR_DESPACHO`, e identifica despacho, incidencia y versión según Gestión §5.2.
- Para una operación nueva, ES-F04-03/04/05 valida sus precondiciones dentro de la transacción local antes de confirmar efectos.
- Usuario y marca temporal se obtienen del JWT y del servidor; no se aceptan como datos de autoría enviados en campos libres.

### 3.2. Dependencias y resultados

- ES-F04-03/04/05 son los únicos productores de estas entradas F-04; llaman al componente común dentro de su transacción y reciben las garantías de RT-01/02.
- ES-F04-02 presenta el historial completo del despacho, incluidas entradas de F-02/F-03/F-04 y ciclos anteriores, desde los datos históricos persistidos; la sexta no agrega una consulta paralela.
- Resultado: una entrada original por operación nueva confirmada, vinculada al despacho/incidencia, inmutable y consultable sin volver a ejecutar la decisión.
- Un rechazo, transacción revertida o repetición exacta no agrega un registro de negocio aceptado. Los logs técnicos de esos casos pueden existir por separado.

## 4. Flujo principal y alternativas

1. El Gestor confirma una recepción, reprogramación o cierre mediante su caso de uso.
2. Gestión autentica, valida formato e identidad y reconoce una repetición ya aceptada conforme a la operación de origen.
3. Para una operación nueva válida prepara la entrada de historial, con datos del cambio y de la incidencia afectada; no deriva esos datos de una salida posterior.
4. Persiste el cambio y el conjunto de escrituras de origen en la misma transacción local. El historial no se confirma por separado ni se añade después de responder éxito.
5. Tras confirmar, queda disponible para el detalle autorizado. Mostrarlo o volver a consultarlo no lo modifica.

## 5. Reglas, datos e integraciones

### 5.1. Datos y origen

Los campos comunes y sus representaciones se definen en Gestión §5.3 y el modelo [cite: 2, 3]. Para las tres operaciones humanas de F-04 se conserva `funcionalidadOrigen=F-04`, `ejecutorTipo=USUARIO`, `ejecutorId=sub` y `origen=MANUAL`. La captura automática del historial no convierte la decisión del Gestor en una decisión de origen `AUTOMATICO`.

| Operación de origen | Tipo y estados registrados | Datos propios que se conservan |
|---|---|---|
| ES-F04-03: recepción | `RECEPCION_EN_CENTRO`; `FALLIDO` antes y después | Incidencia, reserva original, sello y observación de recepción normalizada; `false` significa sello No, no dato ausente. |
| ES-F04-04: reprogramación | `TRANSICION`; `FALLIDO` → `PENDIENTE_ASIGNACION` | Incidencia, nueva fecha civil aceptada y observación normalizada de la decisión. La fecha se conserva como día, sin convertirla en instante UTC. |
| ES-F04-05: cierre | `TRANSICION`; `FALLIDO` → `DEVUELTO_A_ORIGEN` | Incidencia, motivo de cierre y observación normalizada; el motivo pertenece a esta decisión y no sustituye al motivo de fallo. |

El motivo de cierre se conserva en `datos.motivoCierre`; no se inserta en `motivo_codigo`, que referencia el catálogo de fallos. La consulta presenta solo los datos específicos admitidos por el contrato; no rellena una operación anterior con la incidencia, fecha o recepción actuales.

### 5.2. Atomicidad y relación con resultados/eventos

- Recepción: recepción física, versión, único historial y solicitud durable de liberación se confirman o revierten juntos según Gestión §5.2.1. Conserva `FALLIDO` e intentos; no genera evento de cambio de estado hacia Ventas.
- Reprogramación: estado, fecha, entrada a cola, versión, único historial, resultado durable y evento si es real se confirman o revierten juntos según Gestión §5.2.2.
- Cierre: estado final, versión, único historial con resultado original y evento si es real se confirman o revierten juntos según Gestión §5.2.3.
- Si falla una escritura requerida, se revierte el conjunto: no existe una decisión aceptada sin historial ni una entrada que afirme una decisión revertida.
- Simulados conservan el mismo historial de negocio aplicable; no generan eventos externos. La existencia de historial no significa que Ventas haya recibido un evento ni que Operación haya liberado capacidad.
- No se llama a servicios externos dentro de esa transacción ni se comparte una base de datos con Operación o Ventas.

### 5.3. Idempotencia, concurrencia e inmutabilidad

- Se conserva la identidad de comando establecida en Gestión §5.2. Una repetición exacta autorizada del mismo ejecutor devuelve el resultado original y reutiliza su historial, sin otra fila ni cambio de fecha.
- Misma identidad con contenido/ejecutor diferente se rechaza; versiones obsoletas o decisiones concurrentes se resuelven según el comando de origen, sin agregar una auditoría que presente el rechazo como aceptación.
- Solo la mutación que confirma sobre la versión vigente produce la nueva entrada; una carrera con un duplicado exacto recupera la misma operación, no dos historiales.
- Los registros aceptados no se editan ni eliminan mediante F-04. Cambios posteriores del despacho y de su incidencia no alteran entradas previas.
- Los procesadores de liberación y envío actualizan `liberaciones_capacidad`/`eventos_salientes`, respectivamente; reintentos, reinicios, confirmación de capacidad o reenvío del mismo evento no cambian el historial original ni generan otra recepción/transición.
- La ubicación del resultado durable es la ya definida por cada operación y el modelo: esta especificación no agrega otro almacén de resultados ni sustituye sus reglas.

### 5.4. Consulta y separación de datos internos

- ES-F04-02 consulta el historial completo desde Gestión §5.3, incluso después de reprogramar o cerrar. Una consulta autorizada mantiene el orden ascendente por marca temporal persistida y desempate por identificador, definidos en ese contrato.
- Los instantes se conservan en UTC y se presentan en `America/Lima`; no se ordena con el reloj del navegador ni se inventan fechas/nombres de ejecutores.
- Se proyectan únicamente los campos públicos del contrato. `datos.controlCierre`, huellas, respuestas originales almacenadas y demás metadatos internos de recuperación no se exponen como datos del historial.
- Datos de negocio visibles y estado de comunicación/liberación son información distinta. La lectura no reenvía eventos, libera reservas ni crea entradas adicionales.
- Autorización, errores, actualización y presentación pertenecen a ES-F04-02; no se agrega otro endpoint, permiso o pantalla de auditoría.

## 6. Criterios de aceptación

### CA-01. Registro de recepción

- **DADO** una recepción nueva válida de la incidencia vigente.
- **CUANDO** se confirma la operación de ES-F04-03.
- **ENTONCES** guarda un único historial `RECEPCION_EN_CENTRO`, `FALLIDO` antes/después, usuario/fecha del servidor, incidencia, reserva, sello y observación, en la misma transacción que recepción, versión y solicitud de liberación; no publica evento a Ventas.

### CA-02. Registro de reprogramación

- **DADO** una reprogramación nueva válida.
- **CUANDO** se confirma ES-F04-04.
- **ENTONCES** guarda un único historial `TRANSICION`, `FALLIDO` → `PENDIENTE_ASIGNACION`, con usuario, instante, incidencia, nueva fecha civil y observación; confirma junto al cambio, versión, resultado durable y evento si es real.

### CA-03. Registro de cierre

- **DADO** un cierre nuevo válido.
- **CUANDO** se confirma ES-F04-05.
- **ENTONCES** guarda un único historial `TRANSICION`, `FALLIDO` → `DEVUELTO_A_ORIGEN`, usuario/fecha, incidencia, motivo de cierre y observación; el motivo queda separado del catálogo de fallos y se confirma junto al cambio, versión, resultado y evento si es real.

### CA-04. Operación rechazada

- **DADO** una recepción o decisión sin autorización, con datos inválidos, estado/versión incompatibles u otra regla incumplida.
- **CUANDO** el comando rechaza la solicitud.
- **ENTONCES** no registra una decisión de negocio aceptada; conserva los historiales anteriores y permite únicamente el diagnóstico técnico que corresponda.

### CA-05. Repetición idempotente

- **DADO** una operación aceptada con historial y resultado originales, incluso después de reiniciar o cambiar la incidencia.
- **CUANDO** se repite exactamente la solicitud con el mismo usuario autorizado.
- **ENTONCES** recupera el resultado original sin nueva entrada, modificación de su contenido/fecha ni repetición de efectos.

### CA-06. Consulta posterior

- **DADO** un despacho con operaciones F-02/F-03/F-04, varios ciclos y entradas con la misma marca temporal.
- **CUANDO** un Gestor autorizado consulta el detalle, incluso después de resolver.
- **ENTONCES** muestra el historial completo en el orden estable del contrato, con datos propios de cada operación sin mezclarlos con otra incidencia ni provocar efectos de negocio.

### CA-07. Fallo de persistencia

- **DADO** un fallo al escribir historial o cualquier otra escritura obligatoria del comando.
- **CUANDO** se intenta confirmar una recepción, reprogramación o cierre nuevos.
- **ENTONCES** revierte el conjunto conforme a la operación de origen: no hay decisión aceptada sin historial, historial de una decisión revertida, evento externo confirmado ni solicitud de liberación parcial.

### CA-08. Concurrencia y reutilización incompatible

- **DADO** decisiones distintas que compiten sobre la misma versión o una identidad aceptada presentada con otro contenido/ejecutor.
- **CUANDO** se procesan.
- **ENTONCES** solo la mutación ganadora registra su nueva entrada; los rechazos no agregan auditorías aceptadas ni alteran la existente. Duplicados exactos concurrentes dejan una sola entrada.

### CA-09. Inmutabilidad y autoría

- **DADO** un historial aceptado y posteriores operaciones, actualizaciones de incidencia o datos de autoría enviados por un cliente.
- **CUANDO** se registra otra operación o se consulta.
- **ENTONCES** conserva el historial original, toma ejecutor/fecha del contexto autenticado/servidor y representa la decisión humana como origen `MANUAL`, aunque la captura sea automática.

### CA-10. Reintentos técnicos

- **DADO** una recepción o decisión aceptada con liberación/envío pendiente o fallido.
- **CUANDO** se reintenta, reinicia o confirma un procesador, o se reenvía el mismo evento por RT-03.
- **ENTONCES** actualiza solo su solicitud/evento según su contrato; conserva número, contenido y marcas de las entradas de historial y no genera otra recepción/transición.

### CA-11. Datos internos y autorización de lectura

- **DADO** un historial con metadatos internos de recuperación y una consulta autorizada o sin autorización.
- **CUANDO** se solicita el detalle.
- **ENTONCES** la autorizada muestra solo campos permitidos por Gestión §5.3, sin huellas, respuestas originales ni `controlCierre`; la no autorizada se rechaza según ES-F04-02 sin revelar el historial.

### CA-12. Historial de simulados

- **DADO** una recepción, reprogramación o cierre válido de un despacho simulado.
- **CUANDO** se acepta.
- **ENTONCES** conserva la misma trazabilidad de negocio aplicable, una entrada por operación y sin eventos externos; no interpreta esa ausencia de eventos como ausencia de historial.

## 7. UI, backend y requisitos no funcionales

### 7.1. UI

No crea ni modifica UI propia. El historial y sus estados de consulta ya pertenecen a ES-F04-02 y a los componentes de detalle definidos allí; esta especificación solo garantiza los registros que consumen. Su verificación de lectura utiliza ese detalle, sin otra pantalla o formulario.

### 7.2. Backend

- El caso de uso de origen invoca la captura del componente RT-02 dentro de su misma transacción de Gestión; no responde éxito antes de asegurar el historial.
- Reutiliza `historial_estados_despacho`, tipos y referencias locales del modelo. Los registros de soporte de idempotencia y las solicitudes/eventos existentes mantienen sus responsabilidades.
- La consulta proyecta el esquema público de Gestión §5.3; no devuelve directamente el JSON interno almacenado.
- ES-F04-06 no incorpora controlador, endpoint, tabla ni procesador independiente de auditoría.

### 7.3. Requisitos no funcionales

- Atomicidad local, unicidad por operación aceptada, historial inmutable e idempotencia conforme a las operaciones productoras.
- Autoría del contexto autenticado y marcas temporales del servidor; fechas de operación conservadas aunque otra salida cambie datos del despacho.
- Autorización de consulta y separación entre información pública y metadatos internos; sin acceso directo a tablas de otros servicios.
- Trazabilidad consistente con RT-02 y la API de detalle, sin duplicar el registro de la operación ni los intentos técnicos de comunicación.

## 8. Verificación y completitud

- Integración con persistencia: CA-01 a CA-05 y CA-07/08/09/12; comprobar filas, datos, autoría, unicidad y transacción. Para fallos/concurrencia usar transacciones reales y fallos controlados, no solo mocks del método de auditoría.
- Integración de consulta/seguridad: CA-06/09/11; varios ciclos, marcas temporales iguales, consulta histórica y exclusión de metadatos internos.
- Procesadores de liberación y eventos: CA-10; reintento, respuesta perdida, reinicio y confirmación sin otra entrada ni cambio de historial.
- La evidencia debe distinguir componentes aislados, dobles y servicios reales. Revisar enlaces o Markdown no demuestra cumplimiento funcional.

La definición funcional y los documentos SDD están preparados. La implementación se considera completa cuando:

- [ ] CA-01 a CA-12 tienen resultados reales verificables.
- [ ] Las tres operaciones productoras y el detalle consumen el mismo historial, con transacciones y concurrencia comprobadas.
- [ ] La evidencia demuestra inmutabilidad, privacidad de metadatos y ausencia de duplicados por procesos técnicos.
- [ ] Plan y tareas ejecutados; documentación, código y evidencia revisados conservando criterios e identificadores.

## 9. Referencias

- [cite: 1] [F-04](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-05/CA-13; [overview](../../overview.md#rt-02-historial-del-despacho), RT-02/RT-CA-04.
- [cite: 2] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §§5.2.1/5.2.2/5.2.3 y [§5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02); [convenciones](../../integraciones/api-contract.md#9-reglas-de-idempotencia-y-concurrencia), idempotencia.
- [cite: 3] [Modelo](../../arquitectura/modelo-datos.md), historial y soporte de operaciones; [ES-F04-02](../ES-F04-02-ConsultarDetalleIncidencia/spec.md), [ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/spec.md), [ES-F04-04](../ES-F04-04-ReprogramarDespachoFallido/spec.md) y [ES-F04-05](../ES-F04-05-CerrarDespachoComoDevueltoAOrigen/spec.md).
- [cite: 4] [Diseño F-04](../../disenio/funcionalidades/f-04.md), Pantalla 2; [guía SDD](../../plantillas/sdd/README.md), aplicabilidad de UI y migración progresiva.
