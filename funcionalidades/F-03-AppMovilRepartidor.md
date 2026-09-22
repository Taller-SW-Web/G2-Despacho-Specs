# Especificación F-03: Web Responsive del Repartidor y Evidencia de Entrega

**Responsable:** Max Rojas
**Estado:** En especificación
**Actor principal:** Repartidor
**Lineamientos del curso:** Registro de entrega y evidencia de recepción; Gestión de entregas fallidas (registro en campo)

## 1. Contexto

La entrega ocurre en calle, donde el repartidor no dispone de un equipo de escritorio. El módulo de Despacho ofrece su propia interfaz de campo, autónoma respecto de Ventas y Postventa, implementada como vista web mobile-first y no como aplicación nativa, de modo que comparte backend y autenticación con el resto del módulo.

El repartidor recoge en el centro de despacho los paquetes sellados que F-02 le asignó y los lleva a destino. Los paquetes que no logra entregar regresan con él al centro de despacho.

Esta funcionalidad es el origen de las transiciones `EN_CAMINO`, `ENTREGADO` y `FALLIDO`. F-03 no crea ni asigna despachos: ejecuta y registra el resultado de los despachos que F-02 asigna al repartidor, en el orden que F-02 define. Los despachos fallidos que genera son resueltos por F-04, y la ocupación que liberan al cerrarse es recalculada por F-05 a partir del estado de los despachos.

## 2. Propósito

Permitir al repartidor consultar los despachos de su jornada, actualizar su estado desde el celular, registrar evidencia fotográfica obligatoria del resultado y cerrar su jornada sin dejar despachos en `ASIGNADO` ni `EN_CAMINO`, con trazabilidad de quién ejecutó cada transición y cuándo.

## 3. Alcance

Esta funcionalidad incluye:

- Acceso del repartidor con el JWT emitido por Seguridad y Usuarios, y validación de su habilitación operativa en F-05.
- Ruta de la jornada en curso, ordenada según la secuencia definida por F-02.
- Detalle del despacho con los datos necesarios para entregar y contactar al destinatario.
- Transición a `EN_CAMINO` al iniciar el traslado.
- Registro de entrega exitosa (`ENTREGADO`) con fotografía obligatoria y nombre opcional de quien recibe.
- Registro de entrega fallida (`FALLIDO`) con motivo del catálogo, fotografía obligatoria y comentario opcional.
- Incremento del contador de intentos solo cuando existió un intento real de entrega.
- Registro y consulta autorizada de la evidencia fotográfica; la estrategia de compresión, metadatos, límites y almacenamiento está pendiente de decisión del equipo.
- Cierre de jornada con resolución obligatoria de pendientes y corte automático de respaldo.
- Resumen de jornada del propio repartidor.
- Catálogo único de motivos de fallo para el módulo.
- Idempotencia en las operaciones de cambio de estado.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario está autenticado con un JWT válido con rol `REPARTIDOR`.
- El identificador de usuario del token está vinculado a un repartidor registrado en F-05.
- Para ejecutar transiciones, el repartidor tiene una asignación diaria activa y un estado operativo `DISPONIBLE`, `EN_RUTA` o `SATURADO`.
- El despacho existe, está asignado al repartidor del token y pertenece a la jornada en curso.
- La transición es válida según la máquina de estados común (Anexo A).
- Para cerrar un despacho como `ENTREGADO` o como `FALLIDO` por incidencia existe una fotografía cargada correctamente.
- Existe conexión activa; el sistema no opera sin red.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Emitir y validar el JWT con el identificador de usuario y el rol `REPARTIDOR`. |
| Monitoreo de Flota (F-05) | Resolver el repartidor vinculado al usuario del token, informar su estado operativo y cerrar su turno al finalizar la jornada. |
| Programación y Asignación (F-02) | Asignar los despachos con jornada, secuencia, destinatario, dirección y teléfono; reasignarlos o cancelarlos antes del traslado. |
| Entregas Fallidas (F-04) | Consumir los despachos `FALLIDO` con su motivo, contador de intentos y evidencia. |
| Requisitos transversales (overview, sección 6) | Validar cada transición, registrar el historial y publicar el evento hacia Ventas y Postventa. |
| Servicio de evidencia por definir | Almacenar y permitir la consulta autorizada de las fotografías según la decisión técnica pendiente. |

### 4.3. Resultados

- Un acceso válido presenta la ruta de la jornada ordenada por secuencia.
- Una transición aceptada cambia el estado, persiste la marca temporal del servidor y el repartidor ejecutor, y queda en el historial común.
- Un cierre como `ENTREGADO` persiste la referencia de la evidencia y, si se informa, el nombre de quien recibe.
- Un cierre como `FALLIDO` con intento real persiste motivo, evidencia y comentario, e incrementa el contador de intentos en uno.
- Un cierre de jornada deja todo despacho pendiente en `FALLIDO` con motivo `NO_INTENTADO`, sin incrementar el contador, y pone al repartidor en `FUERA_DE_TURNO`.
- Un despacho `ENTREGADO` deja de contar en la ocupación del repartidor; uno `FALLIDO` sigue contando hasta que el Gestor confirma su recepción en el centro de despacho (F-04).

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Autenticación y habilitación operativa

El sistema DEBE permitir el acceso solo a usuarios con rol `REPARTIDOR` vinculados a un repartidor activo, y restringir las transiciones a quienes estén en turno.

#### CA-01. Acceso exitoso

- **DADO** un repartidor vinculado, con asignación diaria activa y estado operativo `DISPONIBLE`.
- **CUANDO** se autentica desde su celular.
- **ENTONCES** el sistema muestra la vista "Mi Ruta" y habilita las acciones de cambio de estado.

#### CA-02. Credencial ausente o expirada

- **DADO** una solicitud sin token o con token vencido.
- **CUANDO** se invoca cualquier recurso de la funcionalidad.
- **ENTONCES** el backend responde `401 Unauthorized` y no expone información de despachos.

#### CA-03. Rol distinto o usuario no vinculado

- **DADO** un token válido cuyo rol no es `REPARTIDOR`, o cuyo usuario no está vinculado a un repartidor activo en F-05.
- **CUANDO** se invocan los recursos de operación de campo.
- **ENTONCES** el backend responde `403 Forbidden`.

#### CA-04. Repartidor fuera de turno

- **DADO** un repartidor activo cuyo estado operativo en F-05 es `FUERA_DE_TURNO`.
- **CUANDO** accede a la aplicación.
- **ENTONCES** el sistema permite consultar su ruta y su resumen del día, pero rechaza toda transición con `409 Conflict` e informa que su turno no está activo.

### RF-02. Consulta de la ruta asignada

El sistema DEBE mostrar al repartidor solo sus despachos de la jornada en curso, en el orden definido por F-02.

#### CA-05. Carga exitosa de la ruta del día

- **DADO** que el repartidor tiene despachos de la jornada actual.
- **CUANDO** abre "Mi Ruta".
- **ENTONCES** el sistema lista los despachos ordenados por secuencia con código de rastreo, dirección, destinatario, estado, número de intento y posición, y excluye los despachos `CANCELADO` o reasignados a otro repartidor.

#### CA-06. Jornada sin asignaciones

- **DADO** que el repartidor no tiene despachos en la jornada actual.
- **CUANDO** abre "Mi Ruta".
- **ENTONCES** el sistema muestra un mensaje de ruta vacía.

#### CA-07. Acceso a despachos de otro repartidor

- **DADO** que un repartidor manipula la petición para consultar la ruta de otro.
- **CUANDO** el backend recibe un identificador distinto al resuelto desde su token.
- **ENTONCES** responde `403 Forbidden` sin exponer datos.

#### CA-08. Despachos de jornadas anteriores

- **DADO** despachos de fechas anteriores que quedaron sin cierre por una falla del corte automático.
- **CUANDO** el repartidor carga su ruta.
- **ENTONCES** el sistema no los incorpora a la ruta vigente, los muestra en una bandeja de "pendientes de regularización" y no permite operarlos.

### RF-03. Consulta del detalle de un despacho

El sistema DEBE mostrar la información necesaria para ejecutar la entrega.

#### CA-09. Detalle exitoso

- **DADO** un despacho asignado al repartidor en `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** abre su detalle.
- **ENTONCES** ve dirección, referencia, destinatario, teléfono con llamada directa, intento actual sobre el máximo configurado, fecha programada y estado.

#### CA-10. Despacho de otro repartidor

- **DADO** un despacho asignado a otro repartidor.
- **CUANDO** se solicita su detalle.
- **ENTONCES** el backend responde `403 Forbidden`.

#### CA-11. Despacho inexistente

- **DADO** un código que no corresponde a ningún despacho.
- **CUANDO** se solicita su detalle.
- **ENTONCES** el backend responde `404 Not Found` sin datos parciales.

### RF-04. Inicio de traslado

El sistema DEBE permitir declarar el inicio del traslado de un despacho.

#### CA-12. Inicio de traslado exitoso

- **DADO** un despacho en `ASIGNADO`.
- **CUANDO** el repartidor pulsa "En camino".
- **ENTONCES** el estado cambia a `EN_CAMINO` con marca temporal del servidor y repartidor ejecutor, y la vista se actualiza sin recargarse por completo.

#### CA-13. Transición no permitida

- **DADO** un despacho ya `ENTREGADO`.
- **CUANDO** el repartidor intenta marcarlo "En camino".
- **ENTONCES** el backend responde `409 Conflict` y conserva el estado.

#### CA-14. Despacho reasignado o cancelado durante la jornada

- **DADO** que F-02 reasignó el despacho a otro repartidor o lo canceló por anulación del pedido mientras seguía en pantalla.
- **CUANDO** el repartidor intenta operarlo.
- **ENTONCES** el backend responde `409 Conflict`, la interfaz informa que el despacho fue actualizado y refresca la ruta sin aplicar cambios. Si el despacho fue cancelado y el paquete ya estaba en su poder, la interfaz le indica devolverlo al centro de despacho.

### RF-05. Registro de entrega exitosa con evidencia

El sistema DEBE exigir una fotografía para cerrar un despacho como entregado.

#### CA-15. Confirmación con evidencia válida

- **DADO** un despacho en `EN_CAMINO`.
- **CUANDO** el repartidor captura la fotografía, opcionalmente registra el nombre de quien recibe y pulsa "Confirmar entrega".
- **ENTONCES** el sistema registra la evidencia mediante el mecanismo aprobado, persiste su referencia y cambia el estado a `ENTREGADO`.

#### CA-16. Confirmación sin evidencia

- **DADO** el formulario de entrega sin fotografía.
- **CUANDO** el repartidor intenta confirmar.
- **ENTONCES** el botón permanece deshabilitado, se muestra el mensaje de evidencia obligatoria y no se envía la petición.

#### CA-17. Fallo en la carga de la imagen

- **DADO** una confirmación con fotografía adjunta.
- **CUANDO** el almacenamiento responde con error o excede el tiempo de espera.
- **ENTONCES** el estado no cambia, se informa el error y la imagen se conserva en el formulario para reintentar.

#### CA-18. Archivo inválido

- **DADO** un archivo que incumple el formato o el tamaño que el equipo defina para la evidencia.
- **CUANDO** llega al backend.
- **ENTONCES** se responde `400 Bad Request`, no se guarda el archivo y el estado no cambia.

### RF-06. Registro de entrega fallida

El sistema DEBE permitir declarar una entrega fallida con motivo del catálogo, fotografía obligatoria y comentario opcional.

#### CA-19. Incidencia con motivo tipificado

- **DADO** un despacho en `EN_CAMINO` que no pudo entregarse.
- **CUANDO** el repartidor elige "Marcar como fallido", selecciona `CLIENTE_AUSENTE`, adjunta la fotografía del domicilio y confirma.
- **ENTONCES** el estado cambia a `FALLIDO` ("No entregado, regresa al centro de despacho"), se guardan motivo, evidencia y comentario, el contador de intentos aumenta en uno, la interfaz recuerda al repartidor que debe devolver el paquete al centro y el despacho queda disponible para F-04.

#### CA-20. Motivo no seleccionado

- **DADO** el formulario de incidencia sin motivo.
- **CUANDO** el repartidor intenta confirmar.
- **ENTONCES** el envío se bloquea y el campo de motivo se resalta como obligatorio.

#### CA-21. Pérdida de conexión durante el envío

- **DADO** que el repartidor confirma una operación.
- **CUANDO** la petición no llega al backend por falta de señal.
- **ENTONCES** la interfaz informa que el cambio no se registró, conserva el estado anterior y exige un reintento explícito.

#### CA-22. Reintento idempotente

- **DADO** un reintento de una operación cuyo resultado se desconoce.
- **CUANDO** el backend recibe una segunda solicitud con la misma clave de idempotencia.
- **ENTONCES** devuelve el resultado original sin duplicar la transición, el incremento del contador ni el registro en el historial.

### RF-07. Cierre de jornada

El sistema DEBE garantizar que ningún despacho quede en `ASIGNADO` ni `EN_CAMINO` al finalizar la jornada, distinguiendo intentos reales de paquetes no intentados.

#### CA-23. Cierre con despachos pendientes

- **DADO** despachos en `ASIGNADO` o `EN_CAMINO` al terminar el turno.
- **CUANDO** el repartidor confirma el cierre, advertido de la cantidad de despachos afectados.
- **ENTONCES** esos despachos pasan a `FALLIDO` con motivo `NO_INTENTADO` sin incrementar el contador, la interfaz lista los paquetes que el repartidor debe devolver al centro de despacho, quedan disponibles para F-04 y F-05 pone al repartidor en `FUERA_DE_TURNO`.

#### CA-24. Corte automático de respaldo

- **DADO** que el repartidor no cerró su jornada antes de la hora de corte configurada.
- **CUANDO** se ejecuta el proceso automático.
- **ENTONCES** se aplica el tratamiento de CA-23 y el historial identifica la operación como automática.

#### CA-25. Cierre sin pendientes

- **DADO** que ningún despacho de la jornada está en `ASIGNADO` ni `EN_CAMINO`.
- **CUANDO** el repartidor confirma el cierre.
- **ENTONCES** se registra el cierre, el repartidor pasa a `FUERA_DE_TURNO` y se muestra el resumen sin generar fallos.

### RF-08. Resumen de la jornada

El sistema DEBE mostrar al repartidor el consolidado de su propio día.

#### CA-26. Consolidado correcto

- **DADO** un repartidor con despachos en distintos estados.
- **CUANDO** consulta el resumen.
- **ENTONCES** ve total asignado, entregados, fallidos con intento, no intentados y pendientes, coincidentes con el historial.

### RF-09. Acceso controlado a la evidencia

El sistema DEBE permitir ver la evidencia únicamente a usuarios autorizados, sin exponerla de forma pública.

#### CA-27. Consulta autorizada de evidencia

- **DADO** un despacho con evidencia.
- **CUANDO** el repartidor propietario o un usuario con rol `GESTOR_DESPACHO` solicita verla.
- **ENTONCES** el sistema permite visualizar la evidencia mediante el mecanismo de acceso autorizado que defina el equipo.

#### CA-28. Acceso sin autorización válida

- **DADO** un acceso directo o con una autorización ausente o vencida.
- **CUANDO** se solicita la evidencia.
- **ENTONCES** el acceso es denegado.

#### CA-29. Usuario no autorizado

- **DADO** un usuario que no es el repartidor propietario ni tiene rol `GESTOR_DESPACHO`.
- **CUANDO** solicita el enlace.
- **ENTONCES** el backend responde `403 Forbidden`.

### RF-10. Catálogo de motivos de fallo

El sistema DEBE mantener el catálogo de motivos como fuente única para el campo y para F-04.

#### CA-30. Consulta del catálogo

- **DADO** que la vista de campo o F-04 necesitan los motivos vigentes.
- **CUANDO** consultan el catálogo.
- **ENTONCES** reciben los motivos seleccionables con código y etiqueta (Anexo B), sin los de uso exclusivo del sistema.

### RF-11. Trazabilidad de las transiciones

El sistema DEBE registrar cada transición ejecutada en campo en el historial común del módulo (overview, RT-02).

#### CA-31. Registro en el historial

- **DADO** una transición aceptada.
- **CUANDO** se persiste.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual o automático, marca temporal del servidor, estado anterior, estado nuevo, motivo y observaciones.

## 6. Frontend

La funcionalidad tendrá una experiencia web mobile-first compuesta por:

| Elemento | Responsabilidad |
|---|---|
| Pantalla de acceso | Autenticar y comunicar el bloqueo por turno inactivo, rol incorrecto o usuario no vinculado. |
| Vista "Mi Ruta" | Listar los despachos por secuencia, con estados de carga, vacío y error, e indicador visual de estado. |
| Detalle del despacho | Dirección, referencia, destinatario, llamada directa, intento y fecha programada. |
| Acción "En camino" | Confirmar el inicio del traslado y actualizar el estado sin recargar toda la vista. |
| Formulario de entrega | Capturar y previsualizar la fotografía; campo opcional para quien recibe. El tratamiento técnico de la imagen queda pendiente de decisión. |
| Formulario de incidencia | Motivo obligatorio, fotografía y comentario opcional. |
| Cierre de jornada | Advertir cuántos despachos quedarán como no intentados antes de confirmar. |
| Resumen de jornada | Consolidado del día. |
| Retroalimentación | Éxito, validaciones, conflictos, ausencia de red y errores de evidencia. |

La interfaz debe impedir acciones conocidas como inválidas, pero las reglas siempre se validan en el backend.

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Identidad y habilitación | Validar el token, resolver el repartidor vinculado en F-05 y su estado operativo. |
| Consulta de ruta | Recuperar los despachos del repartidor para la jornada en curso, ordenados por secuencia. |
| Caso de uso de traslado | Solicitar a la máquina de estados común la transición a `EN_CAMINO`. |
| Caso de uso de entrega | Verificar la evidencia, persistir su referencia y solicitar la transición a `ENTREGADO`. |
| Caso de uso de incidencia | Validar el motivo, persistir evidencia y comentario, incrementar el contador y solicitar la transición a `FALLIDO`. |
| Cierre de jornada | Resolver pendientes como `NO_INTENTADO` y solicitar a F-05 el cierre del turno. |
| Proceso programado de corte | Ejecutar el cierre automático a la hora configurada. |
| Gestión de evidencia | Aplicar las validaciones acordadas, delegar el almacenamiento y controlar el acceso según la decisión técnica pendiente. |
| Control de idempotencia | Registrar la clave de operación y devolver el resultado original ante reintentos. |
| Catálogo de motivos | Exponer los motivos tipificados. |

Esta sección no prescribe clases ni paquetes. Las rutas, cuerpos y códigos se definen en `integraciones/api-contract.md`.

## 8. Requisitos no funcionales

- **Seguridad:** toda petición requiere JWT con rol `REPARTIDOR`; el backend resuelve el repartidor desde el token y no confía en identificadores enviados por el cliente.
- **Protección de datos del destinatario:** teléfono y dirección se muestran solo al repartidor propietario y solo mientras el despacho está en `ASIGNADO` o `EN_CAMINO`. No se ofrece exportación ni copia masiva.
- **Evidencia fotográfica:** la fotografía es obligatoria, pero la compresión, el tratamiento de metadatos, los límites de archivo y el mecanismo de almacenamiento están pendientes de decisión.
- **Usabilidad móvil:** operable con una mano, áreas táctiles de al menos 44 × 44 px y contraste suficiente bajo luz solar.
- **Rendimiento:** toda transición responde en menos de 2 segundos en red 4G, sin fijar todavía un algoritmo ni tamaño final para la fotografía.
- **Conectividad:** se asume conexión activa; ante falta de red se falla de forma explícita, sin cola de sincronización.
- **Idempotencia:** los cambios de estado y el cierre de jornada toleran reintentos mediante clave de idempotencia.
- **Consistencia:** el cambio de estado, el contador y el historial se persisten en una misma transacción.
- **Trazabilidad:** cada transición registra marca temporal del servidor y ejecutor (repartidor o proceso automático).

## 9. Fuera de alcance

- **Resolución de incidencias:** confirmar la recepción del paquete en el centro, reprogramar o cerrar como `DEVUELTO_A_ORIGEN` corresponde a F-04.
- **Asignación, reasignación, secuencia y cancelación:** corresponden a F-02.
- **Repartidores, vehículos, turnos y cálculo de ocupación:** corresponden a F-05.
- **Publicación de eventos a otros módulos:** corresponde al requisito transversal RT-03 del overview.
- **Cotización y cobertura:** corresponden a F-01.
- **Notificación al cliente final:** corresponde a los canales y a Ventas y Postventa.
- **Geolocalización y navegación:** no se captura GPS; se usan aplicaciones externas de mapas.
- **Operación sin conexión:** no hay almacenamiento local ni sincronización diferida.
- **Firma digital y documento de identidad del receptor:** la evidencia se limita a la fotografía y al nombre opcional de quien recibe.

La decisión técnica sobre fotografías y sus posibles ampliaciones están centralizadas en [Pendientes](./pendiente.md), sección F-03. La aplicación no calculará rutas ni ofrecerá navegación propia; el repartidor utilizará aplicaciones externas.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 a CA-04 | Acceder con token válido, ausente, de otro rol, no vinculado y fuera de turno. | Integración de seguridad | Acceso concedido; `401`, `403` y solo lectura fuera de turno. |
| CA-05 a CA-08 | Consultar rutas con y sin asignaciones, ajenas, con cancelados y con despachos antiguos. | Integración y frontend | Lista ordenada sin cancelados, estado vacío, `403` y bandeja de regularización. |
| CA-09 a CA-11 | Consultar detalle propio, ajeno e inexistente. | Integración y frontend | Datos completos, `403` y `404`. |
| CA-12 a CA-14 | Ejecutar transiciones válidas, inválidas y sobre despachos reasignados o cancelados. | Unitaria e integración | Cambio aplicado o `409` con estado conservado. |
| CA-15 a CA-18 | Entregar con evidencia válida, sin evidencia, con almacenamiento caído y con archivo inválido. | Unitaria, integración y frontend | `ENTREGADO` solo con evidencia persistida. |
| CA-19 a CA-22 | Registrar incidencias con y sin motivo, cortar la red y repetir la operación. | Unitaria e integración | Contador incrementado una sola vez. |
| CA-23 a CA-25 | Cerrar jornada con pendientes, por corte automático y sin pendientes. | Integración con proceso programado | `NO_INTENTADO` sin consumir intentos y repartidor `FUERA_DE_TURNO`. |
| CA-26 | Consultar el resumen tras una jornada mixta. | Integración | Cifras coincidentes con el historial. |
| CA-27 a CA-29 | Consultar evidencias con usuarios autorizados y no autorizados. | Integración de seguridad | Evidencia disponible solo para autorizados. |
| CA-30 | Consultar el catálogo. | Integración | Motivos seleccionables sin `NO_INTENTADO`. |
| CA-31 | Revisar el historial tras cada transición. | Integración con persistencia | Registro completo en el historial común. |

Además, se ejecutarán tres recorridos funcionales completos:

1. `ASIGNADO` → `EN_CAMINO` → entrega con evidencia → `ENTREGADO`.
2. `ASIGNADO` → `EN_CAMINO` → incidencia con motivo y evidencia → `FALLIDO` con intento incrementado y visible para F-04.
3. `ASIGNADO` → cierre de jornada → `FALLIDO` con motivo `NO_INTENTADO`, contador sin variación y repartidor `FUERA_DE_TURNO`.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Los criterios `CA-01` a `CA-31` están implementados y cuentan con pruebas exitosas.
- Los tres recorridos funcionales han sido verificados.
- Ninguna transición fuera del Anexo A es aceptada.
- El contador de intentos aumenta solo ante intentos reales y nunca por reintentos.
- Ningún despacho queda en `ASIGNADO` ni `EN_CAMINO` tras el cierre o el corte automático.
- La evidencia es inaccesible sin autorización vigente y está disponible para F-04 mediante el mecanismo que defina el equipo.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede relacionarse con cada criterio de aceptación.

## Anexo A. Transiciones que ejecuta F-03

| Estado origen | Estado destino | Disparador | Efecto sobre el contador de intentos |
|---|---|---|---|
| `ASIGNADO` | `EN_CAMINO` | Acción del repartidor | Sin efecto |
| `EN_CAMINO` | `ENTREGADO` | Confirmación con evidencia | Sin efecto |
| `EN_CAMINO` | `FALLIDO` | Incidencia con motivo y evidencia | Incrementa en uno |
| `ASIGNADO` o `EN_CAMINO` | `FALLIDO` (`NO_INTENTADO`) | Cierre de jornada o corte automático | Sin efecto |

Cualquier otra transición desde F-03 es rechazada con `409 Conflict`. La máquina de estados completa del módulo está definida en el overview (sección 5).

## Anexo B. Catálogo de motivos de fallo

| Código | Etiqueta | Seleccionable en campo | Consume intento |
|---|---|---|---|
| `CLIENTE_AUSENTE` | Cliente ausente | Sí | Sí |
| `DIRECCION_NO_UBICADA` | Dirección no localizada | Sí | Sí |
| `RECHAZO_DEL_PAQUETE` | Cliente rechaza el paquete | Sí | Sí |
| `DATOS_DE_CONTACTO_ERRONEOS` | Datos de contacto incorrectos | Sí | Sí |
| `ZONA_INACCESIBLE` | Zona inaccesible o insegura | Sí | Sí |
| `PAQUETE_DANADO` | Paquete dañado antes de la entrega | Sí | Sí |
| `NO_INTENTADO` | No intentado por fin de jornada | No | No |

## Anexo C. Acuerdos de integración pendientes con otros módulos

| Nº | Módulo | Acuerdo pendiente |
|---|---|---|
| 1 | Seguridad y Usuarios | Confirmar que el JWT incluye el identificador de usuario y el rol `REPARTIDOR`. El identificador de repartidor se resuelve dentro del módulo mediante F-05. |
| 2 | Ventas y Postventa | Confirmar que la solicitud de despacho incluye el teléfono del destinatario y la referencia de la dirección. |
