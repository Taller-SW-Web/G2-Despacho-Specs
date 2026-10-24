# ES-F04-02: Consultar el detalle de una incidencia

**Funcionalidad padre:** [F-04 — Entregas fallidas y reprogramaciones](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-02.

**Responsable:** Gerardo.

**Estado:** Código de consulta implementado en frontend y backend; pruebas locales con dobles disponibles. Verificación integral y formularios propietarios pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; detalle en la aplicación administrativa.

**Servicio propietario:** Gestión de Despachos.

## 1. Contexto y objetivo

Reunir la incidencia más reciente, recepción, intentos consumidos e historial de un despacho para que el Gestor decida cómo resolverlo. Se ofrece acceso autorizado a su fotografía y se explican las acciones permitidas. Después de una reprogramación o cierre, la información sigue consultable para trazabilidad, mostrando el estado actual [cite: 1].

## 2. Alcance

- Incluye la consulta de la última incidencia y del historial completo del despacho, sus restricciones operativas y el estado de comunicación con Ventas.
- No crea fallos, confirma recepciones, libera capacidad, reprograma, cierra ni reenvía eventos. Esas operaciones pertenecen a ES-F04-03/04/05/06 y a RT-03.
- La fotografía principal pertenece a la última incidencia; no se sustituye por una foto anterior. Un explorador de fotografías históricas queda fuera de este incremento.
- Esta carpeta aplica las plantillas SDD: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md). La preparación documental no acredita implementación.

## 3. Actor, precondiciones y resultados

- El usuario tiene JWT humano válido y rol `GESTOR_DESPACHO`; la autorización precede a cualquier consulta o exposición de datos.
- El despacho existe y conserva al menos una incidencia aceptada por Gestión a partir de F-03, incluido `NO_INTENTADO`.
- Solo un despacho actualmente `FALLIDO` puede ofrecer acciones de resolución; un despacho en otro estado conserva la consulta histórica sin esas acciones.
- El resultado reúne datos locales consistentes y distingue datos operativos desconocidos. Ausencia de despacho o de incidencia y errores de autenticación se diferencian según el contrato [cite: 2].

## 4. Flujo principal y alternativas

1. Desde el listado, el Gestor abre el detalle; se conserva la consulta de origen. También se admite acceso directo por identificador.
2. Gestión valida autorización, existencia y referencia a la última incidencia; obtiene estado, contador, política vigente, recepción e historial.
3. Consulta en Operación el nombre y la jornada referenciados por esa incidencia, sin acceder a su base de datos.
4. Devuelve los datos y las acciones habilitadas con todos sus motivos de bloqueo. El frontend muestra el estado actual, no el que conservaba el listado.
5. Si hay referencia de evidencia, el contenedor solicita a Operación el acceso temporal y presenta la fotografía; sus fallos se muestran dentro del visor.
6. Abrir un formulario deriva al caso de uso correspondiente. Tras recibir, se actualiza el detalle; tras reprogramar o cerrar desde él, se vuelve al listado actualizado.
7. Al regresar se restauran filtros, página y tamaño de la URL; sin origen previo se abre el listado inicial de ES-F04-01.

## 5. Reglas, datos e integraciones

### 5.1. Incidencia, contador y trazabilidad

- Se usa `ultima_incidencia_id`, como en ES-F04-01. Motivo, comentario, fecha, repartidor, jornada, evidencia y recepción pertenecen a esa misma salida; nunca se hereda una recepción anterior.
- Se muestran código operativo interno, estado actual, fecha de actualización, motivo del catálogo aunque esté inactivo, comentario, repartidor y `Intentos consumidos` sobre el máximo vigente.
- `NO_INTENTADO` muestra `No intentado en esta salida`: no aumenta ni reinicia el acumulado. Son válidos `0 de 2` y `1 de 2`; no se presenta como `Intento 0`.
- La recepción pendiente no tiene datos de confirmación. La confirmada muestra fecha, identificador del usuario, sello intacto Sí/No y observación; `false` significa No, y un comentario ausente se presenta como `Sin comentario`.
- Tras recibir se distingue `Liberación de capacidad pendiente`, pendiente de revisión o `Capacidad liberada`, según la solicitud de esa incidencia. La sincronización no revierte el retorno ni añade bloqueos a las decisiones; una asignación nueva espera a que la reserva anterior se libere, conforme a ES-F04-03.
- El historial incluye todas las transiciones, recepciones, reasignaciones, reordenamientos y anulaciones registradas; identifica ejecutor, origen manual/automático y datos de cada operación. Recibir no crea un estado nuevo: conserva `FALLIDO`.
- Se ordena por fecha del servidor y desempate estable del contrato. Los instantes se transportan en UTC y se presentan en `America/Lima`; no se fabrican fechas ni nombres.
- Las comunicaciones muestran el estado local del envío a Ventas, sin consultar su disponibilidad ni reenviar automáticamente desde esta lectura. No se exponen payloads ni errores internos.

### 5.2. Acciones y restricciones combinadas

| Situación actual | Confirmar recepción | Reprogramar | Cerrar como devuelto a origen |
|---|---|---|---|
| `FALLIDO`, recepción pendiente, incluso con anulación o máximo alcanzado | Habilitado | Bloqueado | Bloqueado |
| `FALLIDO`, recibido, pedido no anulado y contador menor que el máximo | Oculto | Habilitado | Habilitado |
| `FALLIDO`, recibido, pedido anulado o contador igual/superior al máximo | Oculto | Bloqueado | Habilitado |
| Estado distinto de `FALLIDO` | Oculto | Oculto | Oculto |

- Recepción pendiente siempre bloquea ambas decisiones; anulación y límite añaden sus motivos de bloqueo a la reprogramación. Se explican todos los que apliquen y el máximo se muestra dinámicamente.
- Un sello alterado o un fallo del visor no añaden prohibiciones automáticas a esta matriz. La condición del paquete queda visible para la decisión del Gestor.
- Gestión calcula las acciones con sus datos locales. El frontend las presenta y los comandos vuelven a validar estado, incidencia y concurrencia; una acción habilitada no reserva el derecho a ejecutarla después.

### 5.3. Evidencia y degradación

- `NO_INTENTADO` sin referencia muestra `No intentado — sin foto`. Un fallo real sin referencia muestra `Falta la referencia de evidencia`; no se presenta como una ausencia normal ni se utiliza una foto anterior.
- Referencia existente, carga en curso, enlace expirado, error y acceso denegado son situaciones diferentes. `Volver a cargar` solicita una autorización nueva; nunca genera una URL pública.
- No se guardan URLs firmadas en almacenamiento del navegador ni en logs. Al cerrar el visor, cambiar de despacho/incidencia o perder autorización se retiran imagen y URL anteriores.
- Si Operación no responde, se conservan los datos locales: nombre no disponible y jornada desconocida con aviso. El atraso usa la misma regla de ES-F04-01: recepción pendiente y cierre confirmado de la jornada de la incidencia.
- El error de evidencia no se convierte en error de todo el detalle. Un error de datos canónicos sí muestra recuperación; nunca se presenta como recurso inexistente o detalle vacío.

### 5.4. Actualización e integraciones

- Mientras la vista esté activa se actualizan estado e historial como máximo cada 30 segundos, conforme a RT-CA-11; se vuelve a consultar después de operaciones o conflictos.
- Si cambia la incidencia desde la selección del listado o durante la consulta, se avisa, se retira su evidencia anterior y se presenta la nueva antes de permitir otra decisión. Respuestas antiguas no reemplazan la consulta vigente.
- Durante una actualización se bloquean nuevas acciones; si falla, se conservan solo datos todavía autorizados con aviso y las acciones permanecen bloqueadas hasta obtener datos actuales.
- Gestión es dueño de incidencia, recepción, historial, contador, política y marca local de anulación registrada por F-02. No consulta Ventas para reconstruir esa marca.
- Operación provee perfiles F-05 y jornadas F-06 mediante su lectura interna por lotes; F-03 origina el fallo y Operación autoriza la evidencia. La consulta no altera jornadas ni capacidad.
- Campos, nulabilidad, acciones y errores: [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02). Evidencia y datos operativos: [Operación §§3.5 y 5.4](../../integraciones/api-contract-operacion-reparto.md#35-autorizar-la-lectura-de-evidencia) [cite: 2].

## 6. Criterios de aceptación

### CA-01. Consulta exitosa

- **DADO** un despacho `FALLIDO` con incidencia registrada.
- **CUANDO** el Gestor abre su detalle.
- **ENTONCES** visualiza identificación, estado, motivo, comentario, fechas, repartidor, intentos consumidos, recepción, historial, comunicaciones y acciones correspondientes a los datos actuales.

### CA-02. Evidencia disponible

- **DADO** que la incidencia tiene fotografía asociada y el Gestor está autorizado.
- **CUANDO** solicita verla o renueva un enlace vencido.
- **ENTONCES** Operación concede una URL temporal nueva; el visor permite verla y ampliarla sin persistir ni reutilizar enlaces vencidos.

### CA-03. Evidencia ausente

- **DADO** un `NO_INTENTADO` sin fotografía o un fallo real sin referencia.
- **CUANDO** se consulta el detalle.
- **ENTONCES** distingue los dos mensajes de §5.3 y mantiene disponibles los demás datos, sin recuperar fotografías de otra incidencia.

### CA-04. Despacho inexistente

- **DADO** un identificador sin despacho o un despacho que nunca tuvo incidencia.
- **CUANDO** el Gestor consulta el detalle.
- **ENTONCES** responde `404` con el código correspondiente, sin información parcial ni datos conservados de otra consulta.

### CA-05. Acceso sin permisos

- **DADO** un token ausente/no aceptado o un usuario autenticado sin el rol requerido.
- **CUANDO** solicita o actualiza el detalle.
- **ENTONCES** recibe `401` o `403`, respectivamente, antes de consultar datos; la UI retira detalle, imagen y URL protegidos.

### CA-06. Una incidencia vigente por despacho

- **DADO** un fallo recibido, su reprogramación y otro fallo con distinta jornada, evidencia y recepción pendiente.
- **CUANDO** se abre el detalle.
- **ENTONCES** presenta los datos del último fallo sin heredar recepción ni fotografía; el historial conserva el ciclo anterior.

### CA-07. Contador y acciones combinadas

- **DADO** las cuatro situaciones de la matriz, incluido `NO_INTENTADO` con cero/un fallo previo y máximo configurable.
- **CUANDO** se presenta el detalle.
- **ENTONCES** contador, acciones y explicaciones coinciden con §§5.1/5.2, también ante anulación y límite simultáneos o contador superior al máximo.

### CA-08. Historial y consulta posterior a la resolución

- **DADO** operaciones manuales/automáticas, una recepción sin transición y un despacho ya reprogramado o cerrado.
- **CUANDO** el Gestor vuelve a consultar.
- **ENTONCES** ve el estado actual y el historial completo en orden estable, con datos de cada operación; fuera de `FALLIDO` no se ofrecen acciones de resolución.

### CA-09. Dependencias no disponibles

- **DADO** un fallo al recuperar nombre/jornada o autorizar/cargar una fotografía.
- **CUANDO** se consulta el detalle.
- **ENTONCES** conserva los datos canónicos, indica qué dato no pudo obtener, distingue desconocimiento de ausencia y ofrece reintento sin inventar valores.

### CA-10. Actualización y navegación

- **DADO** una consulta con filtros de origen y cambios concurrentes de recepción, anulación, estado o incidencia.
- **CUANDO** se actualiza, se resuelve un formulario o se vuelve al listado.
- **ENTONCES** cumple §5.4, actualiza las acciones y retira evidencia anterior; al volver restaura la consulta y recarga filas e indicadores.

### CA-11. Consulta sin efectos de negocio

- **DADO** un despacho con historial, contador, recepción y eventos conocidos.
- **CUANDO** se consulta repetidamente el detalle o se solicita acceso a la foto.
- **ENTONCES** esos datos y la capacidad permanecen sin cambios; mostrar `PENDIENTE` o `ENVIO_FALLIDO` no ejecuta un reenvío.

## 7. UI, backend y requisitos no funcionales

- UI: interacción y criterios propios en [ui.md](./ui.md), ruta `/entregas-fallidas/:idDespacho`; carga, datos, consulta histórica, error con reintento, inexistencia y acceso denegado diferenciados. Los fallos secundarios se muestran en su bloque.
- Reutilizar estructura administrativa, `EstadoVista`, `BadgeEstado`, `VisorEvidencia` e `HistorialEstados`; el panel de decisiones permanece local. Diseño vigente: `SYSTEM-DESIGN.md`, §23, y contratos CR-18/19 [cite: 3].
- Permitir teclado, foco visible, ampliación con retorno de foco, razones de bloqueo visibles y asociadas al botón, texto además de color y disposición de una columna en móvil.
- Backend: lectura consistente de Gestión, composición por APIs y respuestas sin caché compartida; no expone datos de destinatario innecesarios ni credenciales.

## 8. Verificación y completitud

- Verificar CA-01/04/05/06/08/11 mediante integración de consulta, autorización y persistencia; CA-02/03/07/09/10 mediante contrato y UI, incluyendo fallos y restricciones combinadas.
- Comprobar teclado, móvil, fechas locales, renovación de evidencia y retirada de datos ante cambio de recurso o autorización; distinguir fixtures de servicios reales.
- [ ] CA-01 a CA-11 cuentan con evidencia real y las integraciones se verificaron.
- [ ] El plan y las tareas están ejecutados y revisados; la evidencia distingue componentes aislados, simulaciones e integraciones reales.

## 9. Referencias

- [cite: 1] [F-04](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-02/03/05/06/07; [ES-F04-01](../ES-F04-01-ConsultarEntregasFallidas/spec.md), incidencia vigente y navegación.
- [cite: 2] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §5.3; [Operación](../../integraciones/api-contract-operacion-reparto.md), §§3.4 y 5.4; [convenciones compartidas](../../integraciones/api-contract.md), §§3 y 9.
- [cite: 3] [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md), §23; [componentes React](../../disenio/componentes-react.md), CR-18/19; [diseño F-04](../../disenio/funcionalidades/f-04.md), Pantalla 2.
- [cite: 4] [Visión general](../../overview.md), RT-02/03/04 y RT-CA-11; [modelo de datos](../../arquitectura/modelo-datos.md), §3.4.
