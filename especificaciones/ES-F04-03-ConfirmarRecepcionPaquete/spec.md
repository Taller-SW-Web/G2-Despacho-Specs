# ES-F04-03: Confirmar la recepción del paquete

**Funcionalidad padre:** [F-04 — Entregas fallidas y reprogramaciones](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-07.

**Responsable:** Gerardo.

**Estado:** Recepción en Gestión y frontend implementados y verificados localmente; integración real y aceptación pendientes. Avance al 24/10/2026 en [evidence.md](./evidence.md).

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; modal desde listado o detalle. **Servicio propietario:** Gestión de Despachos.

## 1. Contexto y objetivo

Al terminar el recorrido, el repartidor normalmente vuelve al centro con los paquetes no entregados. El Gestor verifica cada paquete y confirma su retorno físico, condición del sello y observación opcional. El cierre de jornada no confirma automáticamente ninguna recepción; tampoco se exige jornada cerrada si el paquete de una incidencia `FALLIDO` ya regresó.

La recepción conserva `FALLIDO` y habilita las decisiones de F-04 según intentos y anulación. Gestión registra el retorno y solicita que Operación deje de contar la reserva de esa salida; ambos hechos se distinguen cuando la comunicación está pendiente [cite: 1].

## 2. Alcance

- Incluye recepción individual, auditoría, protección ante concurrencia y solicitud durable de liberación de la reserva original, con recuperación automática y estado consultable.
- No realiza recepción masiva al cerrar jornada, reprogramación/cierre automático, reingreso a stock, tratamiento comercial ni edición de una recepción ya aceptada.
- No modifica el contador de intentos ni publica un evento de cambio de estado a Ventas por recibir. La sincronización de capacidad tiene su propia solicitud interna.
- La carpeta SDD prepara este comportamiento para su desarrollo; su documentación no acredita código ni pruebas ejecutadas.

## 3. Actor, precondiciones y resultados

- JWT humano válido con `GESTOR_DESPACHO`; usuario y fecha se obtienen del token y del servidor.
- Para una confirmación nueva: despacho `FALLIDO`, incidencia vigente con recepción pendiente, identidad/versión actuales y paquete físicamente en el centro.
- La incidencia conserva repartidor, jornada y reserva de la salida fallida. Una referencia local inconsistente se informa antes de escribir; no se adivina otra reserva.
- Pedido anulado, máximo alcanzado, `NO_INTENTADO`, falta de foto o jornada cerrada no impiden recibir un paquete que cumple esas precondiciones.
- Resultado: recepción persistida y solicitud de liberación pendiente; la ocupación se reduce cuando Operación confirma liberar la reserva, incluso si esto ocurre después de la respuesta HTTP.

## 4. Flujo principal y alternativas

1. Desde ES-F04-01/02 se abre el modal con código operativo interno, incidencia, repartidor y fecha; se conserva la pantalla de origen.
2. El Gestor verifica el paquete, selecciona explícitamente sello Sí/No, añade observación opcional y confirma. Sin selección no se envía la solicitud.
3. Gestión autentica, valida el formato y reconoce primero una repetición exacta ya aceptada; para una solicitud nueva valida incidencia, versión, estado y recepción pendiente.
4. En una sola transacción guarda recepción, auditoría, incremento de versión y solicitud única de liberación con la reserva/jornada originales; no espera a Operación dentro de esa transacción.
5. Devuelve `202 Accepted`: el paquete ya está recibido y la liberación queda pendiente. El frontend vuelve a consultar y actualiza origen e indicadores.
6. Un procesador de Gestión entrega la solicitud a Operación. Con confirmación válida marca la liberación confirmada; si falla o pierde la respuesta, conserva y reintenta la misma solicitud/reserva.
7. Listado y detalle mantienen `Recibido en centro` aunque la liberación siga pendiente. El detalle informa la sincronización; no obliga a repetir la recepción física.

## 5. Reglas, datos e integraciones

### 5.1. Registro, validaciones e identidad

- `selloIntacto` es un booleano obligatorio: `false` es válido; ausencia, `null`, números o cadenas no lo sustituyen. No hay valor inicial en el modal.
- La observación es opcional también con sello alterado: omisión, `null` o espacios se normalizan a `null`; texto se recorta en extremos, conserva saltos de línea y admite hasta 500 caracteres según el contrato. La UI no muestra un asterisco de obligación.
- El sello alterado se registra sin rechazar el retorno ni resolver automáticamente daños, reembolsos o restricciones comerciales.
- La recepción se guarda sobre `idIncidencia`, que debe coincidir con `ultima_incidencia_id`. La reserva se obtiene de la instantánea de esa incidencia; no de la asignación actual ni del contador.
- Recepción, historial `RECEPCION_EN_CENTRO`, nueva versión y solicitud durable se confirman o revierten juntos. Los estados anterior/nuevo del historial son `FALLIDO`; incluye identidad de incidencia/reserva, sello, observación y ejecutor.
- La primera recepción aceptada es inmutable para estas operaciones. Dos gestores no pueden sustituir entre sí usuario, fecha, sello u observación. Una versión obsoleta responde `409` aunque el estado siga siendo `FALLIDO`.
- Una repetición exacta autorizada devuelve la respuesta original aun si el despacho cambió después; contenido diferente con la misma identidad responde `409`. Después se consulta el estado actual, sin reutilizar automáticamente una decisión sobre otra salida.

### 5.2. Capacidad y recuperación

- La solicitud durable identifica despacho, incidencia, reserva y jornada originales; existe una sola por incidencia. Sus reintentos nunca sustituyen esos identificadores por los de una salida posterior.
- Operación libera por `idReserva`, valida su pertenencia al despacho y modifica una única reserva; peso, volumen y paquetes proceden de ella. Repetir una liberación ya realizada no vuelve a descontar ni cambia su fecha/motivo original.
- Gestión conserva `PENDIENTE` hasta una respuesta válida que confirme esa reserva como `LIBERADA`; luego marca `CONFIRMADA`. La UI no interpreta `202`, cierre de jornada o recepción física como confirmación de capacidad.
- Caídas, timeouts o reinicios no pierden solicitudes. Los reintentos, calendario, errores que requieren revisión y campos de consulta se definen en Gestión §5.2.1 y Operación §5.2; el GET no dispara el envío [cite: 2].
- Mientras hay sincronización pendiente, Operación conserva la reserva activa y su ocupación; el detalle muestra aviso. Tras la confirmación, F-06 refleja la reducción en su siguiente consulta, sin alterar el cierre de jornada.
- La recepción habilita reprogramación/cierre según ES-F04-02 aun con liberación pendiente. F-02 no puede confirmar una asignación nueva si la reserva anterior sigue activa; una salida nueva utiliza otra reserva una vez liberada la anterior.

### 5.3. UI, contrato e integraciones

- Rutas, payload, respuesta, errores y normalización: [Gestión §5.2.1](../../integraciones/api-contract-gestion-despachos.md#521-confirmar-recepción-en-centro--es-f04-03). Liberación interna: [Operación §5.2](../../integraciones/api-contract-operacion-reparto.md#52-gestión-libera-una-reserva-en-operación).
- Listado ES-F04-01 cuenta el retorno físico: una recepción aceptada sale de pendientes/atrasados aunque su sincronización siga pendiente. Detalle ES-F04-02 presenta el estado de liberación sin añadir prohibiciones a su matriz.
- Durante el envío se evita doble confirmación. Un error recuperable conserva lo ingresado; si se desconoce el resultado, se consulta antes de repetir exactamente la solicitud original, con su misma identidad/versión.
- Ante `409`, actualizar origen y pedir revisión; no sustituir silenciosamente la incidencia/versión ni repetir una recepción con otro contenido. Una recepción registrada por otro gestor se muestra sin permitir sobrescritura.
- Tras `202`, informar `Paquete recibido. Liberación de capacidad pendiente`, cerrar el modal y refrescar filas, indicadores, historial y acciones. Si la lectura posterior falla, conservar la confirmación y ofrecer actualizar; no presentar el guardado como rechazado.
- Fecha del servidor en UTC, presentación en `America/Lima`. `401/403` retira datos protegidos; sin autorización no se permite consultar resultados previos.
- La llamada a Operación usa credencial técnica del backend; no se comparten tablas. F-03 origina la incidencia y Gestión captura su reserva; F-06 calcula ocupación desde sus reservas activas [cite: 3].

## 6. Criterios de aceptación

### CA-01. Confirmación exitosa

- **DADO** un despacho `FALLIDO`, pendiente de retorno, con incidencia/versión vigentes y paquete en el centro.
- **CUANDO** el Gestor indica el sello y confirma.
- **ENTONCES** responde `202`, persiste recepción, historial, versión y solicitud pendiente; conserva `FALLIDO` e intentos. Al confirmar Operación la liberación, F-06 reduce la ocupación correspondiente.

### CA-02. Recepción con sello no intacto

- **DADO** un paquete retornado con sello alterado.
- **CUANDO** el Gestor selecciona No, con observación o sin ella.
- **ENTONCES** guarda `false` y la observación normalizada, sin impedir el retorno ni decidir tratamiento comercial.

### CA-03. Operación repetida

- **DADO** una confirmación ya aceptada, incluso si el despacho dejó de estar `FALLIDO` o la capacidad ya se liberó.
- **CUANDO** el mismo usuario autorizado repite exactamente la solicitud original.
- **ENTONCES** recibe el mismo resultado original sin nueva recepción, auditoría, solicitud ni descuento; después consulta los datos actuales.

### CA-04. Estado o versión incompatibles

- **DADO** una solicitud nueva con estado no `FALLIDO`, versión obsoleta o incidencia sustituida.
- **CUANDO** se intenta confirmar.
- **ENTONCES** responde `409`, conserva los datos vigentes y exige revisar la información sin trasladar la confirmación a otra salida.

### CA-05. Datos incompletos o inválidos

- **DADO** sello omitido/`null`/de tipo incorrecto, identidad incompleta, campo no admitido u observación mayor de 500 caracteres.
- **CUANDO** se solicita la recepción.
- **ENTONCES** responde `400` normalizado por campo, sin escrituras; `false` y observación opcional vacía siguen siendo válidos.

### CA-06. Acceso sin permisos

- **DADO** token no aceptado o usuario válido sin `GESTOR_DESPACHO`.
- **CUANDO** intenta confirmar o recuperar el resultado.
- **ENTONCES** recibe `401` o `403`, respectivamente, sin datos protegidos, cambios ni solicitudes de liberación.

### CA-07. Reserva de la salida correcta

- **DADO** un despacho con varias salidas y reservas históricas diferentes.
- **CUANDO** se recibe la incidencia vigente o se reintenta una liberación antigua.
- **ENTONCES** solo se afecta la reserva capturada en esa incidencia/solicitud; nunca se libera la reserva de una salida posterior.

### CA-08. Atomicidad local e inconsistencias

- **DADO** un fallo al persistir recepción, historial, versión o solicitud, o una referencia local inconsistente.
- **CUANDO** se procesa la confirmación nueva.
- **ENTONCES** no queda una recepción parcial ni se llama a Operación sin solicitud durable; responde el error contractual sin afirmar éxito.

### CA-09. Operación no disponible o respuesta perdida

- **DADO** una recepción aceptada y Operación caída, timeout, respuesta perdida o reinicio del procesador.
- **CUANDO** se intenta o reanuda la entrega de la solicitud.
- **ENTONCES** la recepción permanece registrada, se muestra liberación pendiente y se reintenta la misma reserva hasta confirmar, sin doble descuento ni pérdida de solicitudes.

### CA-10. Dos confirmaciones diferentes

- **DADO** dos gestores o dos contenidos que compiten por la misma recepción.
- **CUANDO** se procesan concurrentemente.
- **ENTONCES** solo una recepción nueva se acepta; la otra recibe `409` sin sobrescribir datos ni duplicar historial/solicitud.

### CA-11. Casos especiales de retorno

- **DADO** un `FALLIDO` con `NO_INTENTADO`, pedido anulado, máximo alcanzado, foto ausente o jornada cerrada/activa.
- **CUANDO** su paquete llegó al centro y se confirma con datos válidos.
- **ENTONCES** registra la recepción; mantiene el contador, no cambia la jornada y habilita solo las decisiones de ES-F04-02.

### CA-12. Modal, resultado desconocido y actualización

- **DADO** confirmación desde listado o detalle, o pérdida de respuesta después de enviarla.
- **CUANDO** se obtiene el resultado o se recupera la conexión.
- **ENTONCES** cumple §5.3: conserva datos ante rechazo recuperable, consulta antes de repetir, distingue recepción de liberación y actualiza la pantalla de origen sin confirmar automáticamente otros paquetes.

## 7. UI, backend y requisitos no funcionales

- Modal accesible con resumen, sello Sí/No sin valor inicial, observación opcional y botones Cancelar/Confirmar; teclado, foco inicial y retorno de foco al cerrar. Aplicar diseño vigente, Pantalla 3 [cite: 3].
- Backend: consulta y escritura locales consistentes, versión optimista, identidad de operación y procesador durable; ninguna transacción distribuida ni autorización solo en frontend.
- UI y accesibilidad: [ui.md](./ui.md); solución técnica, incrementos y dependencias: [plan.md](./plan.md).

## 8. Verificación y completitud

- Verificar CA-01/03/04/05/06/07/08/10 mediante integración PostgreSQL y seguridad; CA-09 con fallos/reinicio y Operación; CA-02/11/12 también mediante UI, fechas y navegación.
- Comprobar booleano `false`, dos gestores, misma versión con contenido distinto, solicitud original tras resolver, historial único y ausencia de eventos a Ventas. Distinguir dobles de servicios reales.
- [ ] CA-01 a CA-12 tienen evidencia real y las integraciones están verificadas.
- [ ] El plan y las tareas están ejecutados y revisados; la evidencia distingue componentes aislados, dobles e integraciones reales.

## 9. Referencias

- [cite: 1] [F-04](../../funcionalidades/F-04-GestionEntregasFallidas.md), RF-07; [ES-F04-01](../ES-F04-01-ConsultarEntregasFallidas/spec.md) y [ES-F04-02](../ES-F04-02-ConsultarDetalleIncidencia/spec.md).
- [cite: 2] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §5.2.1; [Operación](../../integraciones/api-contract-operacion-reparto.md), §5.2; [convenciones comunes](../../integraciones/api-contract.md), §§3/9.
- [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), §3.4; [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), §4.5/CA-15; [diseño](../../disenio/funcionalidades/f-04.md), Pantalla 3; [sistema de diseño](../../disenio/SYSTEM-DESIGN.md), P3.
- [cite: 4] [Visión general](../../overview.md), RT-02; [trazabilidad F-04](../ES-F04-06-RegistrarTrazabilidadOperaciones/spec.md).
- Documentos SDD: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
