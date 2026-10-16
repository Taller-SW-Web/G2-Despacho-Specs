# ES-F04-05: Cerrar un despacho como devuelto a origen

**Funcionalidad padre:** [F-04 — Entregas fallidas y reprogramaciones](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-04/05/06/07.

**Responsable:** Gerardo.

**Estado:** Preparación SDD completada; implementación y verificación pendientes.

**Actor principal:** Gestor de Despacho. **Servicio propietario:** Gestión de Despachos.

**UI:** Aplica; modal administrativo descrito en [ui.md](./ui.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md) y [UI](./ui.md). Preparación del 16/10/2026 sobre la revisión funcional `c8e6e29`; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

Después de una entrega fallida, el paquete vuelve al centro y se confirma su recepción mediante ES-F04-03. El caso habitual de cierre es que se agotaron los intentos o que F-02 registró la anulación del pedido. Se conserva la posibilidad ya establecida de una decisión operativa del Gestor aunque queden intentos; nunca se cierra automáticamente por límite, sello alterado o cierre de jornada [cite: 1].

Finalizar el tratamiento logístico del mismo despacho mediante `FALLIDO` → `DEVUELTO_A_ORIGEN`, registrar por qué no habrá otra entrega y comunicarlo a Ventas y Postventa mediante el evento existente. El paquete queda en el centro a disposición del tratamiento posterior del pedido.

## 2. Alcance

- Incluye confirmación individual con motivo, observación opcional, transición final, historial, resultado recuperable y evento externo si el despacho es real.
- Incluye protección ante versión/incidencia desactualizadas, decisiones concurrentes, repetición de la solicitud y pérdida de respuesta.
- Conserva las reglas de recepción y liberación de ES-F04-03, la consulta histórica de ES-F04-02 y el contrato externo de Ventas.
- La definición canónica de ruta, cuerpo, respuestas y errores se encuentra en [Gestión §5.2.3](../../integraciones/api-contract-gestion-despachos.md#523-cerrar-como-devuelto-a-origen--es-f04-05); no se mantiene otro esquema HTTP aquí [cite: 2].

### 2.1. Fuera de alcance

- Reembolsos, cambios, reclamos, notas de crédito, reintegro de stock y proceso físico posterior del paquete.
- Nuevos estados o comandos comerciales de Ventas; notificar directamente al cliente.
- Cancelar directamente desde `PENDIENTE_ASIGNACION`/`ASIGNADO` por anulación o registrar fallos en campo; corresponden a F-02/F-03.
- Reabrir decisiones finales, recibir automáticamente, asignar otro intento o crear infraestructura de eventos adicional.

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones de una solicitud nueva

- JWT humano válido con `GESTOR_DESPACHO`; usuario y hora se obtienen del token y del servidor.
- Despacho existente en `FALLIDO`, con `idIncidencia` vigente y `versionDespacho` obtenidos del detalle actualizado.
- Recepción confirmada de esa incidencia; no basta una recepción histórica de otra salida.
- Motivo de cierre obligatorio y confirmación explícita del Gestor.

### 3.2. Dependencias

- ES-F04-01/02 aportan listado, detalle, identidad/versión, recepción, historial y acciones.
- ES-F04-03 conserva retorno físico y solicitud durable de liberación; el cierre no la sustituye.
- F-02 registra la anulación y compite por la versión canónica; ES-F04-04 puede competir con el cierre mientras el despacho siga fallido.
- RT-01/02/03 aportan transición, historial y entrega asíncrona del evento a Ventas. Operación y F-06 continúan la liberación pendiente por la reserva original [cite: 3].

### 3.3. Resultados

- Mismo despacho/pedido en `DEVUELTO_A_ORIGEN`, versión incrementada, motivo/observación y fecha/ejecutor persistidos.
- Contador, carga, zona, destino, incidencia, recepción y referencias históricas conservados; no se crea otro intento.
- Una transición y un historial; un evento `DESPACHO_DEVUELTO_A_ORIGEN` para un despacho real. Un simulado conserva historial y marca de prueba sin evento externo.
- Desaparece del listado de fallidos y no vuelve a la cola de F-02. El detalle histórico sigue accesible, sin acciones de resolución.
- Ningún fallo de entrega del webhook revierte un cierre local aceptado.

## 4. Flujo principal y alternativas

1. Desde un detalle actualizado en `FALLIDO` con recepción confirmada, el Gestor abre `Cerrar como devuelto a origen`. El modal conserva despacho, incidencia y versión seleccionados.
2. Presenta código operativo interno, motivo de fallo, intentos consumidos y advertencia de que no habrá más entregas. Solicita motivo de cierre en texto libre y permite observación adicional.
3. El Gestor confirma; durante el envío se evita una segunda confirmación.
4. Gestión autentica, valida y normaliza el cuerpo; reconoce primero una repetición exacta aceptada. Para una solicitud nueva valida identidad/versión, estado, recepción e integridad local.
5. En una transacción local confirma estado, nueva versión, historial y resultado original del comando; registra el evento si es real. Un fallo de escritura revierte todo el conjunto.
6. Responde `200`; la UI informa el cierre y vuelve al listado actualizado con los filtros/página de origen. Sin origen previo abre el listado inicial.
7. RT-03 envía el evento fuera de la transacción y permite consultar su comunicación en el detalle. La solicitud de liberación de ES-F04-03 continúa independientemente hasta confirmar su propia reserva.

## 5. Reglas, datos e integraciones

### 5.1. Motivo, recepción y efectos

- El motivo es texto libre obligatorio, hasta 500 puntos de código Unicode después de recortar extremos; se conserva el texto normalizado. No se crea un catálogo de cierre ni se usa el catálogo de motivos de fallo como catálogo de esta decisión.
- La observación es opcional y se normaliza como en el contrato; no sobrescribe el motivo de fallo, comentario del repartidor ni observación de recepción. El ejemplo contractual `MAXIMO_INTENTOS_ALCANZADO` es un texto admitido, no un enum obligatorio.
- Alcanzar/superar el máximo o tener pedido anulado bloquea reprogramar, pero permite cerrar después de recibir. También puede cerrarse un `NO_INTENTADO` con cero intentos o un despacho con intentos disponibles, por decisión explícita.
- La liberación pendiente o pendiente de revisión, jornada activa/cerrada, sello alterado o fotografía ausente/no disponible no añaden bloqueos. No se exige consultar Operación ni Ventas para aceptar el cierre.
- No se modifica contador, fecha programada, identidad, destino o carga. No se libera capacidad otra vez, no se crea reserva, no se modifica jornada y no se elimina la recepción/solicitud original.
- `DEVUELTO_A_ORIGEN` es final: el Gestor no puede reabrirlo, reprogramarlo, editar el motivo ni volver a decidir desde esta operación. El tratamiento posterior pertenece a Ventas.

### 5.2. Concurrencia y recuperación

- Los tres comandos de F-04 comparten la identidad de Gestión §5.2. Una repetición exacta autorizada del mismo ejecutor devuelve el `200` y cuerpo originales antes de validar las precondiciones actuales.
- El historial guarda la identidad y el resultado aceptados en metadatos internos durables, según el modelo; no se depende solo de una caché temporal ni se requiere una tabla nueva para este cierre.
- Misma identidad con contenido normalizado o ejecutor diferente responde `409`. Un cierre nuevo contra un estado ya final o reprogramado tampoco sobrescribe la decisión anterior.
- Cierre, reprogramación y registro de anulación compiten sobre la versión del despacho; solo una mutación puede confirmar sobre una versión. Si otra operación ganó, se consulta otra vez antes de confirmar una decisión nueva.
- Ante `409`, no reemplazar silenciosamente incidencia/versión ni reenviar el motivo sobre otra salida. Si la respuesta se pierde, consultar antes de repetir exactamente el comando original; el GET por sí solo no demuestra quién decidió.
- La respuesta original conserva el identificador del evento, no una promesa de entrega a Ventas; el estado actual de comunicación se obtiene del detalle.

### 5.3. Integración con Ventas y otras funcionalidades

- Se mantiene `DESPACHO_DEVUELTO_A_ORIGEN`, el mismo webhook, autenticación, campos y reintentos de [Común §7.3](../../integraciones/api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa). `datos.motivoCierre` contiene el motivo normalizado; no se envía una cancelación comercial adicional [cite: 2].
- El cierre comunica el fin logístico también si F-02 ya registró anulación o la incidencia fue `NO_INTENTADO`. Gestión no consulta ni impone un estado comercial previo para emitir ese evento; no inventa una transición a `EN_CAMINO` ni consume intentos para ajustar estados.
- La aplicación del evento al pedido pertenece a Ventas y al contrato externo existente. Esta especificación no agrega estados, transiciones comerciales ni un resultado comercial garantizado para esos casos; la aceptación local no espera ese procesamiento.
- Fallos de envío conservan el cierre y el mismo `idEvento`; RT-03 aplica su límite y reenvío manual. No se promete reintento automático indefinido ni se duplican eventos por repetir el comando.
- ES-F04-01 actualiza filas e indicadores; ES-F04-02 conserva el historial y la liberación de esa incidencia incluso después de cerrar. ES-F04-06 registra la misma transición, sin otra auditoría paralela [cite: 1, 3].

## 6. Criterios de aceptación

### CA-01. Cierre exitoso

- **DADO** un despacho real `FALLIDO`, recibido en su incidencia vigente, con identidad/versión actuales.
- **CUANDO** el Gestor confirma con motivo válido y observación opcional.
- **ENTONCES** responde `200`, cambia a `DEVUELTO_A_ORIGEN`, incrementa versión y guarda motivo, usuario, instante, un historial con resultado original y un evento pendiente en la misma transacción; conserva el contador.

### CA-02. Operación repetida

- **DADO** un cierre aceptado, incluso después de reiniciar el servicio o cambiar el estado de envío/liberación.
- **CUANDO** el mismo usuario autorizado repite exactamente la solicitud original.
- **ENTONCES** devuelve el mismo `200` y cuerpo originales sin otra transición, incremento de versión, auditoría ni evento; después se consulta la situación actual.

### CA-03. Ventas y Postventa no disponible

- **DADO** un cierre local aceptado de un despacho real.
- **CUANDO** Ventas no responde o devuelve error.
- **ENTONCES** mantiene `DEVUELTO_A_ORIGEN` y entrega el mismo evento mediante RT-03; al agotar los reintentos queda `ENVIO_FALLIDO` consultable, sin repetir la decisión.

### CA-04. Recepción pendiente

- **DADO** un `FALLIDO` cuya incidencia vigente no fue recibida, aunque otra incidencia sí lo haya sido.
- **CUANDO** se intenta cerrar con identidad/versión actuales.
- **ENTONCES** responde `409` y exige confirmar esa recepción, incluso con pedido anulado o máximo alcanzado; no cambia estado ni genera evento.

### CA-05. Pedido anulado

- **DADO** un despacho fallido recibido con anulación registrada por F-02.
- **CUANDO** el Gestor consulta y confirma el cierre con datos vigentes.
- **ENTONCES** reprogramar permanece bloqueado y el cierre se acepta; registra el mismo evento logístico sin solicitar otra cancelación comercial ni esperar respuesta de Ventas.

### CA-06. Motivo ausente o datos inválidos

- **DADO** motivo omitido/`null`/vacío/solo espacios, tipo incorrecto, texto excedido, identidad/versión inválidas, observación inválida o campos/parámetros extra.
- **CUANDO** se intenta confirmar.
- **ENTONCES** responde `400` normalizado por campo sin efectos; motivo y observación válidos se recortan y conservan saltos internos, y observación omitida/`null`/espacios se guarda como `null`.

### CA-07. Acceso sin permisos y existencia

- **DADO** token no aceptado, usuario sin `GESTOR_DESPACHO` o despacho inexistente solicitado por un Gestor autorizado.
- **CUANDO** intenta cerrar o recuperar un resultado previo.
- **ENTONCES** responde `401`, `403` o `404`, respectivamente, sin cambios ni eventos y sin revelar datos a quien no tiene autorización.

### CA-08. Intentos y decisión explícita

- **DADO** un despacho recibido con máximo alcanzado/superado, con intentos disponibles o con `NO_INTENTADO` y contador cero.
- **CUANDO** el Gestor decide cerrarlo con motivo válido.
- **ENTONCES** se acepta sin aumentar ni reiniciar el contador; límite o anulación no ejecutan cierre automático, y sello alterado no sustituye la confirmación.

### CA-09. Identidad o estado desactualizados

- **DADO** una solicitud nueva con versión obsoleta, otra incidencia, estado reprogramado o final.
- **CUANDO** intenta cerrar.
- **ENTONCES** responde `409`, conserva la decisión vigente y exige revisar los datos, sin heredar recepción de otra salida ni reabrir el despacho.

### CA-10. Decisiones concurrentes y contenido diferente

- **DADO** dos cierres diferentes, cierre/reprogramación o cierre/anulación sobre la misma versión, o una identidad aceptada reutilizada con otro contenido/ejecutor.
- **CUANDO** se procesan.
- **ENTONCES** solo una mutación confirma sobre esa versión; el otro comando responde `409` sin efectos parciales. Un duplicado exacto del mismo ejecutor recupera el resultado ganador.

### CA-11. Capacidad pendiente y continuidad de la recepción

- **DADO** recepción confirmada con liberación pendiente/de revisión, incluso con jornada activa, sello alterado o foto no disponible.
- **CUANDO** se cierra el despacho.
- **ENTONCES** se acepta sin llamada a Operación; preserva recepción, incidencia, referencias y solicitud original. Sus reintentos continúan después del cierre y no descuentan otra reserva ni modifican la versión del despacho.

### CA-12. Atomicidad y datos inconsistentes

- **DADO** una referencia local inconsistente, recepción sin su solicitud durable o fallo al escribir estado, versión, historial/resultado o evento.
- **CUANDO** se procesa un cierre nuevo.
- **ENTONCES** se informa el error contractual sin afirmar éxito; una transacción fallida no deja efectos parciales ni envía un evento no confirmado.

### CA-13. Conservación y simulación

- **DADO** un despacho reprogramable o no, real o simulado, recibido y vigente en `FALLIDO`.
- **CUANDO** se cierra.
- **ENTONCES** conserva identidad, fecha, zona, destino, carga e historial; solo el real registra evento externo. El simulado mantiene su marca y responde con evento `null`.

### CA-14. Modal, respuesta perdida y navegación

- **DADO** un modal abierto, rechazo recuperable, conflicto, respuesta perdida o fallo al actualizar después de un `200`.
- **CUANDO** el Gestor confirma o recupera el resultado.
- **ENTONCES** se aplica §7: evita doble envío, conserva entradas recuperables y solicitud original, exige revisión tras conflicto y distingue cierre aceptado de lectura fallida; vuelve al origen con filtros/página e indicadores actualizados.

### CA-15. Consulta posterior y estado final

- **DADO** un cierre aceptado.
- **CUANDO** se consultan fallidos, cola de F-02 y detalle histórico.
- **ENTONCES** no figura en las dos listas; el detalle muestra estado final, motivo/historial y comunicación/liberación actuales sin acciones de resolución ni metadatos internos del comando.

## 7. UI, backend y requisitos no funcionales

### 7.1. UI

- Modal de confirmación desde ES-F04-02: código operativo interno, fallo, contador dinámico, advertencia de cierre definitivo, motivo obligatorio en `Textarea` y observación opcional. Sin motivo normalizado válido no permite enviar.
- Usar el patrón vigente de SYSTEM-DESIGN P5; teclado, foco visible, errores por campo y retorno de foco al cancelar. El motivo permanece como texto libre, sin selector ni catálogo nuevo.
- Conservar contexto del comando; actualizaciones del detalle no sustituyen silenciosamente incidencia/versión. `409` requiere nueva lectura y revisión; errores recuperables conservan entradas. `401/403` retiran datos protegidos.
- Tras `200`, informar `Despacho cerrado como devuelto a origen`, cerrar el modal y volver al listado con filtros/página de origen. La comunicación externa se consulta en el detalle; no se afirma que Ventas ya procesó el evento.
- Si falla la lectura posterior, mostrar `Cierre registrado. No se pudo actualizar el listado` y ofrecer actualizar sin repetir el guardado. Si se perdió la respuesta, consultar y recuperar el comando original antes de decidir nuevamente.
- Mensajes de notificación pendiente/fallida siguen el estado consultado: `ENVIO_FALLIDO` informa revisión/reenvío manual según RT-03, sin prometer reintentos automáticos indefinidos [cite: 4].

### 7.2. Backend

- Gestión valida el contrato, compara versión al escribir y confirma la transición final, historial/resultado y evento en una transacción local.
- Reutiliza `historial_estados_despacho` para la decisión y su resultado durable; el modelo define metadatos internos y unicidad del cierre. No se agrega una tabla de cierres.
- Mantiene `ultima_incidencia_id`, recepción y solicitud de liberación para consulta/recuperación; no transforma el cierre en otra recepción ni llama a Operación para descontar capacidad.
- La bandeja de salida existente entrega a Ventas fuera de la transacción; la respuesta HTTP acredita el cierre local.

### 7.3. Requisitos no funcionales

- Autenticación/autorización antes de consultar existencia o resultados; respuesta sin caché compartida.
- Instantes del servidor en UTC y presentación en `America/Lima`; no se acepta fecha/usuario editable del cliente.
- Idempotencia durable, integridad local, control de versión y ausencia de transacciones distribuidas o acceso directo a tablas ajenas.
- Historial inmutable y separación entre datos de presentación y metadatos internos; no exponer huellas, respuestas almacenadas, credenciales o errores externos.

## 8. Verificación y completitud

- Contrato, seguridad y persistencia: CA-01/02/04/05/06/07/08/09/10/12/13; cubrir normalización Unicode, replay tras reinicio, escrituras fallidas y dos transacciones concurrentes.
- Integración de recepción/liberación y consultas: CA-04/11/15; comprobar continuidad de la solicitud original y reserva correcta después de cerrar.
- Eventos: CA-01/03/05/08/13; comprobar payload acordado y mismo identificador, entrega fallida y ausencia de comunicación para simulados. Distinguir pruebas con dobles de la entrega real.
- UI: CA-06/07/09/14/15; teclado/foco, doble confirmación, respuesta desconocida, datos desactualizados y retorno con filtros.
- Las verificaciones funcionales están pendientes; validar Markdown/JSON/enlaces no acredita código ni aceptación de Ventas.

La definición funcional y la preparación documental SDD están listas para desarrollar. La implementación se considera completa solo cuando:

- [ ] CA-01 a CA-15 tienen evidencia real y revisión.
- [ ] Contrato, UI, persistencia, recepción/liberación y evento se verificaron, distinguiendo dobles de servicios reales.
- [ ] Plan y tareas ejecutados, documentos coherentes con el código y revisión de la evidencia registrada.

## 9. Referencias

- [cite: 1] [F-04](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-04/05/06/07; [ES-F04-01](../ES-F04-01-ConsultarEntregasFallidas/spec.md), [ES-F04-02](../ES-F04-02-ConsultarDetalleIncidencia/spec.md), [ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/spec.md) y [ES-F04-04](../ES-F04-04-ReprogramarDespachoFallido/spec.md).
- [cite: 2] [Gestión §5.2.3](../../integraciones/api-contract-gestion-despachos.md#523-cerrar-como-devuelto-a-origen--es-f04-05), §§5.2/5.3; [Común](../../integraciones/api-contract.md), §§3/7.3/9.
- [cite: 3] [Modelo](../../arquitectura/modelo-datos.md), §3.4; [estados](../../arquitectura/diagrama-estados-despacho.md), estado final y transiciones; [trazabilidad F-04](../ES-F04-06-RegistrarTrazabilidadOperaciones/spec.md); [overview](../../overview.md), RT-01/02/03.
- [cite: 4] [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md), P5 de F-04; [diseño F-04](../../disenio/funcionalidades/f-04.md), Pantalla 5; [guía SDD](../../plantillas/sdd/README.md).
