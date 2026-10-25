# ES-F04-04: Reprogramar un despacho fallido

**Funcionalidad padre:** [F-04 — Entregas fallidas y reprogramaciones](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-03/05/06/07.

**Responsable:** Gerardo.

**Estado:** Implementación local de Gestión y frontend verificada; aceptación conjunta pendiente según [evidence.md](./evidence.md).

**Actor principal:** Gestor de Despacho. **Servicio propietario:** Gestión de Despachos.

**UI:** Aplica; modal administrativo descrito en [ui.md](./ui.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md) y [UI](./ui.md). Preparación del 16/10/2026 sobre la revisión funcional `c8e6e29`; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

ES-F04-01 permite localizar el despacho fallido, ES-F04-02 presenta su incidencia vigente y ES-F04-03 confirma que el paquete regresó físicamente al centro. Con esa recepción, el Gestor puede decidir otra entrega si el pedido no está anulado y el contador todavía es menor al máximo vigente [cite: 1].

Fijar una nueva fecha sobre el mismo despacho, devolverlo inmediatamente a la cola de F-02 y conservar incidencia, recepción e historial. Programar otra salida no representa un intento realizado ni una asignación de repartidor.

## 2. Alcance

- Incluye fecha futura, observación opcional, transición a `PENDIENTE_ASIGNACION`, auditoría, idempotencia y registro del evento para Ventas cuando corresponda.
- Comprende conflictos con otra reprogramación, cierre o anulación, y recuperación cuando se pierde la respuesta.
- El contrato HTTP se define únicamente en [Gestión §5.2.2](../../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04); aquí se referencian sus resultados sin mantener otro esquema [cite: 2].

### 2.1. Fuera de alcance

- Asignar repartidor, reservar capacidad futura, ordenar ruta o asignar automáticamente al llegar la fecha.
- Modificar zona, dirección, productos o condiciones comerciales; incrementar contador antes de otro fallo real.
- Editar recepción o decisión aceptadas, alterar sello/stock, notificar al cliente final o resolver reembolsos.

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones de una solicitud nueva

- JWT humano válido con `GESTOR_DESPACHO`; ejecutor y marcas temporales proceden del token y del servidor.
- Despacho existente en `FALLIDO`, con `idIncidencia` vigente y `versionDespacho` obtenidos del detalle actualizado.
- Recepción confirmada de esa misma incidencia; una recepción de otra salida no es suficiente.
- Pedido no anulado y contador acumulado menor al máximo vigente, cuyo valor inicial es dos.
- Fecha civil válida estrictamente posterior al día actual del servidor en `America/Lima`.

### 3.2. Dependencias

- ES-F04-01/02 actualizan listado, indicadores, detalle y acciones después de resolver; ES-F04-03 conserva la recepción y su solicitud de liberación.
- F-02 consume la nueva entrada en cola y realiza la asignación cuando corresponde; registra la anulación sobre el despacho canónico.
- F-03 origina resultados de campo; Gestión conserva contador e incidencia canónicos. F-05/F-06 aportan perfiles, jornadas y capacidad para una asignación posterior.
- RT-01/02/03 aportan transición, historial y comunicación durable con Ventas; no se accede a tablas de otro servicio [cite: 3].

### 3.3. Resultados

- Mismo despacho y pedido, estado `PENDIENTE_ASIGNACION`, nueva fecha persistida, versión incrementada y nueva marca de entrada a cola.
- Contador sin cambios; zona, destino, datos físicos, incidencia y recepción histórica conservados.
- Una transición y un historial; evento `DESPACHO_REPROGRAMADO` pendiente para despachos reales. Los simulados conservan su marca y no generan eventos externos.
- Visible inmediatamente en F-02, sujeto a sus filtros, con asignación bloqueada mientras la fecha sea futura. Aunque llegue la fecha, la reserva anterior debe haberse liberado antes de aceptar otra asignación.

## 4. Flujo principal y alternativas

1. El Gestor abre `Reprogramar` desde un detalle actualizado cuya acción está habilitada. El modal conserva despacho, incidencia y versión seleccionados.
2. Presenta código operativo interno, motivo, intentos consumidos sobre el máximo vigente, fecha obligatoria y observación opcional. Explica que se mantiene el contador y que la asignación corresponde a F-02.
3. El Gestor selecciona una fecha futura y confirma explícitamente. Mientras se envía se evita una segunda confirmación.
4. Gestión autentica, valida formato y reconoce primero una repetición exacta aceptada. Para una solicitud nueva comprueba versión/incidencia, estado, recepción, anulación, política vigente y fecha conforme al orden contractual.
5. En una transacción local persiste transición, fecha, entrada a cola, incremento de versión, historial, resultado durable del comando y evento cuando corresponda; si falla una escritura se revierte el conjunto.
6. Responde `200`. La UI informa la fecha aceptada y vuelve al listado con filtros/página de origen, actualizando filas e indicadores; sin origen previo abre el listado inicial.
7. RT-03 entrega el evento después del commit, sin bloquear la respuesta ni revertir la decisión ante una caída de Ventas. El detalle permanece disponible como consulta histórica.

## 5. Reglas, datos e integraciones

### 5.1. Fecha y observación

- `nuevaFechaProgramada` es una fecha civil `YYYY-MM-DD`, sin hora ni conversión a UTC. El backend calcula «hoy» en `America/Lima` al validar la solicitud nueva, independientemente de la zona del host o del navegador.
- El selector usa como referencia `consultadoEn` del detalle convertido a esa zona; la validación del servidor prevalece si cambia el día antes de confirmar. No hay fecha preseleccionada.
- La regla vigente exige una fecha futura; no añade exclusión de fines de semana/feriados, plazo tarifario ni horizonte máximo de anticipación.
- Observación opcional, hasta 500 puntos de código Unicode normalizados como en el contrato; no sustituye ni sobrescribe observaciones de recepción o de asignaciones anteriores.

### 5.2. Intentos, recepción y capacidad

- Reprogramar no incrementa ni reinicia el contador. Este cuenta fallos con intento real; una entrega exitosa o un `NO_INTENTADO` no lo incrementa, conforme a F-03/RT-01.
- `NO_INTENTADO` permite reprogramar solo si también cumple recepción, anulación y límite; nunca evade un máximo ya alcanzado por fallos anteriores.
- Se lee el máximo configurado vigente al decidir, no un valor fijo del frontend. Una configuración ausente/inválida es inconsistencia, no permiso para reprogramar.
- Recepción confirmada habilita la decisión aunque su liberación esté `PENDIENTE` o requiera revisión. No se exige jornada cerrada, sello intacto, foto disponible ni servicio de Operación disponible.
- Reprogramar no libera otra vez capacidad, modifica la solicitud de liberación, abre/cierra jornadas ni reserva el siguiente reparto. La solicitud original conserva su reserva aunque el despacho cambie de estado.
- Se retiran las referencias de asignación vigente del despacho canónico; repartidor, jornada y reserva de la salida anterior permanecen en su incidencia, historial y solicitud. La nueva asignación usará otra reserva [cite: 3].

### 5.3. Consistencia, idempotencia e integraciones

- Se conserva la zona original incluso inactiva; no se recotiza ni se consultan Productos o Ventas para recrear el pedido. Se conservan identidad, destino, carga y condición de simulación.
- La identidad del comando es despacho, incidencia, operación y versión presentada, junto con contenido normalizado y `sub` para reconocer la repetición; no requiere `Idempotency-Key` adicional.
- Una repetición exacta autorizada devuelve el `200` y cuerpo originales, incluso después de medianoche, asignación o un nuevo fallo; no vuelve a aplicar fecha/estado vigentes a ese resultado ni repite efectos. La UI consulta después la situación actual.
- Misma identidad con otro contenido o ejecutor responde `409`. Dos solicitudes nuevas que compiten por la misma versión no pueden aceptar dos decisiones; un cierre o anulación concurrente participa en el mismo control del despacho.
- Ante `409`, actualizar y pedir revisión/confirmación explícita; no reemplazar automáticamente incidencia/versión ni trasladar la decisión a otra salida. Ante respuesta desconocida, consultar antes de repetir exactamente la solicitud original.
- Historial `TRANSICION`, origen `MANUAL`, funcionalidad `F-04`, ejecutor, instante UTC, estados y datos propios según Gestión §5.3. La nueva fecha queda en ese historial aunque se cambie en otro ciclo.
- Evento y datos a Ventas según [Común §7.3](../../integraciones/api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa): actualiza fecha estimada y conserva estado comercial. El estado de envío se consulta en el detalle; el modal no promete entrega del webhook [cite: 2].

## 6. Criterios de aceptación

### CA-01. Reprogramación válida

- **DADO** un despacho `FALLIDO`, recibido, no anulado, con incidencia/versión actuales, un intento consumido y máximo dos.
- **CUANDO** el Gestor confirma fecha futura y observación opcional.
- **ENTONCES** responde `200`, queda `PENDIENTE_ASIGNACION` con nueva fecha/entrada a cola y versión incrementada, conserva contador en uno y persiste historial, resultado del comando y evento pendiente si es real.

### CA-02. Fecha inválida

- **DADO** una solicitud nueva que cumple las demás condiciones.
- **CUANDO** la fecha es hoy/pasada en `America/Lima`, inexistente o de formato inválido.
- **ENTONCES** responde `400` por campo sin escrituras; incluye cambio de día entre abrir y confirmar y diferencia de día respecto de UTC/navegador.

### CA-03. Límite de intentos alcanzado

- **DADO** un despacho recibido, no anulado y con contador igual o superior al máximo vigente.
- **CUANDO** se consulta o se intenta reprogramar con identidad/versión actuales.
- **ENTONCES** la UI bloquea la acción y el comando responde `422`; solo se ofrece cierre. También aplica si el máximo cambió desde abrir el formulario.

### CA-04. Estado o identidad desactualizados

- **DADO** una solicitud nueva con estado no `FALLIDO`, versión obsoleta o incidencia sustituida, aunque el estado vuelva a ser `FALLIDO`.
- **CUANDO** se intenta reprogramar.
- **ENTONCES** responde `409`, conserva los datos actuales y requiere revisarlos antes de otra confirmación, sin reutilizar recepción de una salida anterior.

### CA-05. Recepción pendiente

- **DADO** un `FALLIDO` con recepción pendiente de su incidencia vigente, aunque tenga otra recepción histórica.
- **CUANDO** se intenta reprogramar con identidad/versión actuales.
- **ENTONCES** responde `409` y exige recibir primero; no habilita la decisión por tener jornada cerrada, anulación o límite alcanzado.

### CA-06. Despacho no intentado

- **DADO** un despacho recibido con `NO_INTENTADO`, no anulado y contador cero o uno sobre máximo dos.
- **CUANDO** se confirma fecha futura.
- **ENTONCES** vuelve a `PENDIENTE_ASIGNACION` conservando el acumulado; si ya alcanzó el máximo, aplica CA-03.

### CA-07. Pedido anulado

- **DADO** un despacho fallido recibido con anulación registrada por F-02.
- **CUANDO** se consulta o se intenta reprogramar con identidad/versión actuales, incluso con límite alcanzado.
- **ENTONCES** la UI bloquea la acción al consultar y el comando responde `409` al ejecutarlo, por anulación antes que `422` por límite; solo permite cierre. No consulta Ventas para autorizar otra salida.

### CA-08. Operación repetida

- **DADO** una reprogramación aceptada, incluso con fecha ya alcanzada o despacho que cambió de estado/incidencia.
- **CUANDO** el mismo usuario autorizado repite exactamente el comando original.
- **ENTONCES** devuelve el `200` y cuerpo originales sin duplicar transición, versión, entrada a cola, historial ni evento; la UI consulta el estado actual.

### CA-09. Formato y observación

- **DADO** identidad/versión incompletas o inválidas, fecha ausente, campo extra, parámetros no admitidos u observación inválida/mayor de 500 caracteres normalizados.
- **CUANDO** se envía el comando.
- **ENTONCES** responde `400` por campo sin cambios; observación omitida, `null` o espacios se acepta como `null`, y texto válido conserva saltos internos sin alterar la recepción.

### CA-10. Identidad de operación reutilizada

- **DADO** una reprogramación aceptada.
- **CUANDO** se presenta su misma identidad con fecha/observación normalizadas diferentes o desde otro ejecutor.
- **ENTONCES** responde `409` sin sobrescribir el resultado ni generar otra decisión.

### CA-11. Decisiones concurrentes

- **DADO** dos reprogramaciones distintas, reprogramación y cierre, o reprogramación y anulación que compiten sobre un despacho.
- **CUANDO** intentan persistir sobre la misma versión vigente.
- **ENTONCES** solo una mutación sobre esa versión se confirma; la otra obtiene `409`. Si ganó la anulación, la nueva consulta impide reprogramar; si ganó reprogramación, F-02 evalúa una cancelación nueva sobre `PENDIENTE_ASIGNACION`.

### CA-12. Retorno a F-02 y nueva salida

- **DADO** una reprogramación aceptada.
- **CUANDO** se consultan sin filtros excluyentes fallidos, detalle y cola de F-02.
- **ENTONCES** sale de fallidos, conserva detalle histórico sin decisiones y aparece inmediatamente en cola como reprogramado, también con cero/un intento consumido; asignar queda bloqueado hasta su fecha y hasta liberar la reserva anterior, sin incremento anticipado del contador.

### CA-13. Liberación pendiente y referencias históricas

- **DADO** recepción confirmada con liberación pendiente/de revisión, jornada activa/cerrada, sello alterado o evidencia no disponible.
- **CUANDO** se reprograma cumpliendo las condiciones de negocio.
- **ENTONCES** se acepta sin depender de Operación; conserva incidencia/recepción/solicitud originales, retira asignación vigente y no descuenta capacidad ni crea reserva. El siguiente fallo crea otra incidencia con recepción pendiente.

### CA-14. Persistencia y comunicación externa

- **DADO** un fallo de escritura local o caída de Ventas después del commit.
- **CUANDO** se procesa la reprogramación.
- **ENTONCES** el fallo local revierte todos los efectos; la caída externa conserva la decisión y deja el evento recuperable por RT-03, sin un segundo evento al repetir el comando.

### CA-15. Seguridad y existencia

- **DADO** token no aceptado, usuario sin rol o despacho inexistente consultado por un Gestor autorizado.
- **CUANDO** se intenta reprogramar o recuperar un resultado previo.
- **ENTONCES** responde `401`, `403` o `404`, respectivamente, sin escrituras ni datos protegidos para quien no tiene autorización.

### CA-16. Conservación y simulaciones

- **DADO** un despacho reprogramable con zona original luego desactivada, real o simulado.
- **CUANDO** se confirma la operación.
- **ENTONCES** conserva identidad, zona, destino, carga y contador sin recotizar; registra historial y solo el real genera evento a Ventas.

### CA-17. Modal, recuperación y navegación

- **DADO** un formulario abierto, rechazo recuperable, conflicto, pérdida de respuesta o fallo al recargar tras un `200`.
- **CUANDO** se confirma o recupera la consulta.
- **ENTONCES** cumple §§4/5.3/7: conserva entradas recuperables, evita doble envío y repetición automática sobre datos nuevos, restaura origen y distingue confirmación aceptada de fallo de lectura posterior.

### CA-18. Política inválida

- **DADO** configuración del máximo ausente, no entera o no positiva.
- **CUANDO** se procesa una reprogramación nueva.
- **ENTONCES** responde `500` por inconsistencia local, sin reemplazarla silenciosamente por dos ni persistir efectos.

## 7. UI, backend y requisitos no funcionales

### 7.1. UI

- Modal accesible con resumen, contador dinámico, fecha sin valor inicial, observación opcional, Cancelar y Confirmar; sin fecha válida no permite enviar. Teclado, errores asociados al campo, foco inicial y retorno de foco al cancelar.
- Al actualizar el detalle se aplica ES-F04-02: no enviar mientras los datos estén desactualizados; cambios de incidencia/versión exigen revisión, sin sustituir silenciosamente el contexto del modal.
- `400` conserva entradas para corregir; `409/422` actualizan detalle y acciones antes de otra decisión. Errores de comunicación conservan la solicitud original para recuperar el resultado.
- Después del `200`, mensaje `Despacho reprogramado para [fecha]` y regreso al listado actualizado. Si falla esa lectura, mostrar `Reprogramación registrada. No se pudo actualizar el listado`, con opción de actualizar; no presentar rechazo del guardado ni reenviar.
- `401/403` retiran datos protegidos. Mensajes no dependen solo del color. Diseño: Pantalla 4 [cite: 4]; el detalle de componentes se concreta en [ui.md](./ui.md).

### 7.2. Backend

- Gestión aplica validaciones y transacción local del contrato, con comparación de versión al escribir y resultado durable independiente de una caché temporal.
- F-02 consulta la misma entrada canónica; no se crea otro despacho ni una tarea de medianoche para incorporarlo a cola. `en_cola_desde` se fija al aceptar, sin cambiar en replays.
- RT-03 transmite el evento externo fuera de la transacción. La liberación de ES-F04-03 continúa con su propia solicitud e identidad; no hay transacción distribuida.

### 7.3. Requisitos no funcionales

- Autorización en backend antes de consultar existencia/resultados; respuesta sin caché compartida.
- Instantes UTC para auditoría y fecha civil en `America/Lima` para decidir; reloj del cliente no autoriza operaciones.
- Atomicidad local, control de versión e idempotencia durable; sin tablas compartidas ni llamadas externas dentro de la transacción.
- Trazabilidad de transición y comunicación, sin exponer credenciales o payloads internos en UI.

## 8. Verificación y completitud

- Contrato e integración con persistencia: CA-01 a CA-11 y CA-14/15/16/18, incluyendo dos transacciones concurrentes, reinicio y replay posterior a medianoche/nueva incidencia.
- Integración F-02/F-03/F-06: CA-12/13/16, con cola visible inmediatamente, asignación futura rechazada, reserva anterior pendiente y nueva reserva/incidencia sin heredar recepción.
- UI y reloj controlado: CA-02/03/05/07/09/12/17; fechas distintas entre UTC/Lima/navegador, cambio de día, teclado, foco, entradas y retorno con filtros.
- Fallos de persistencia/respuesta/servicios: CA-08/10/11/13/14/17; comprobar ausencia de efectos parciales, un historial/evento y recuperación desde resultado durable.
- Estas comprobaciones están previstas; revisar Markdown y enlaces no demuestra una integración ejecutada.

- [ ] CA-01 a CA-18 implementados y con evidencia real.
- [ ] Contrato y recorridos con F-02/F-03/F-06 y RT-03 verificados, distinguiendo dobles de servicios reales.
- [ ] Plan y tareas ejecutados y revisados; evidencia real registrada sin confundirla con la preparación documental.

## 9. Referencias

- [cite: 1] [F-04](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-03/05/06/07; [ES-F04-01](../ES-F04-01-ConsultarEntregasFallidas/spec.md), [ES-F04-02](../ES-F04-02-ConsultarDetalleIncidencia/spec.md), [ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/spec.md) y [ES-F04-05](../ES-F04-05-CerrarDespachoComoDevueltoAOrigen/spec.md).
- [cite: 2] [Gestión §5.2.2](../../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04), §§5.2/5.3; [convenciones](../../integraciones/api-contract.md), §§3/7.3/9.
- [cite: 3] [Cola F-02](../ES-F02-03-ConsultarColaPendientes/spec.md), [asignación F-02](../ES-F02-04-AsignarDespachoRepartidor/spec.md), [modelo](../../arquitectura/modelo-datos.md), §§3.3/3.4/3.5, y [overview](../../overview.md), RT-01/02/03.
- [cite: 4] [Diseño F-04](../../disenio/funcionalidades/f-04.md), Pantalla 4; [componentes compartidos](../../disenio/componentes-react.md) y [guía SDD](../../plantillas/sdd/README.md).
