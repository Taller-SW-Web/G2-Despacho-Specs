# Especificación F-03: Web Responsive del Repartidor y Evidencia de Entrega

## 1. Contexto

La ejecución física de la entrega ocurre en calle, donde el repartidor no dispone de un equipo de escritorio. Dado que el diseño exige una arquitectura orientada a microservicios sin acceso directo a base de datos entre módulos, el módulo de Despacho debe ofrecer su propia interfaz operativa de campo, autónoma respecto de Ventas y Postventa.

Esta capacidad es el **punto de origen de la información del ciclo de transporte**: aquí se generan las transiciones `EN_CAMINO`, `ENTREGADO` y `FALLIDO` que posteriormente consumen el Panel de Programación y Asignación (F-02), el Centro de Entregas Fallidas (F-04) y el Panel de Monitoreo de Flota (F-05) dentro del mismo módulo. F-03 no crea despachos ni los asigna: únicamente ejecuta y registra el resultado de los despachos que F-02 le entrega.

La interfaz se implementa como una vista web adaptada a dispositivos móviles (mobile-first, responsive), no como aplicación nativa, de modo que comparte backend y esquema de autenticación con el resto del módulo de Despacho.

## 2. Propósito

Permitir al Repartidor consultar los despachos asignados a su ruta de la jornada en curso, actualizar el estado de cada paquete en tiempo real desde su celular, registrar evidencia fotográfica obligatoria del resultado de la entrega y cerrar su jornada dejando todo despacho en un estado terminal, garantizando la trazabilidad de quién ejecutó cada transición y en qué momento.

## 3. Alcance

Esta funcionalidad incluye:

- Autenticación del repartidor mediante token JWT emitido por el módulo de Seguridad y validación de su habilitación operativa contra F-05.
- Listado ordenado de despachos asignados al repartidor autenticado para la jornada en curso, sin arrastre de jornadas anteriores.
- Detalle del despacho con dirección, referencia, destinatario, teléfono de contacto, número de intento y fecha de entrega comprometida.
- Transición de estado a `EN_CAMINO` al iniciar el traslado de un paquete.
- Registro de entrega exitosa (`ENTREGADO`) con evidencia fotográfica obligatoria.
- Registro de entrega fallida (`FALLIDO`) con motivo tipificado de catálogo, evidencia fotográfica y comentario opcional.
- Incremento del contador de intentos únicamente cuando existió intento real de entrega.
- Compresión de la imagen en el cliente, eliminación de metadatos EXIF y carga hacia el servicio de almacenamiento de objetos.
- Provisión de URL firmada bajo demanda para que F-04 visualice la evidencia sin exponer el objeto públicamente.
- Cierre de jornada con resolución obligatoria de los despachos pendientes y corte automático de respaldo.
- Resumen de jornada del propio repartidor.
- Exposición de la carga operativa vigente por repartidor para consumo de F-05.
- Exposición del catálogo de motivos de fallo para consumo de F-04.
- Validación de transiciones de estado permitidas y garantía de idempotencia en las operaciones de cambio de estado.
- Registro de bitácora auditable de cada transición.

Las rutas, cuerpos, respuestas y códigos específicos se definirán en el contrato único `specs/api-contract.md` y se publicarán mediante Swagger UI desde el backend desplegado.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario debe estar autenticado con un token JWT válido emitido por el módulo de Seguridad, con rol `REPARTIDOR`.
- El identificador de repartidor contenido en el token debe corresponder a un repartidor registrado en F-05.
- El repartidor debe encontrarse en un estado operativo habilitante (`DISPONIBLE` o `EN_RUTA`) para ejecutar transiciones de estado.
- El despacho debe existir, estar asignado al repartidor del token y pertenecer a la jornada en curso.
- La transición solicitada debe ser válida según la máquina de estados del Anexo A.
- Para cerrar un despacho como `ENTREGADO` o `FALLIDO` debe existir evidencia fotográfica cargada correctamente.
- Debe existir conexión activa; el sistema no opera sin red.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Emitir y validar el token JWT del repartidor, con `idRepartidor` y rol embebidos. |
| Monitoreo de Flota (F-05) | Mantener el alta del repartidor, su estado operativo y turno vigente; solicitar a Seguridad el alta de credenciales. F-03 consulta esta información para habilitar o bloquear la operación. |
| Programación y Asignación (F-02) | Crear los despachos, asignarlos al repartidor y definir la secuencia de ruta que F-03 respeta al ordenar la lista. |
| Entregas Fallidas (F-04) | Consumir los despachos en estado `FALLIDO` generados por F-03, junto con su motivo, contador de intentos y evidencia. |
| Ventas y Postventa (indirecta) | Origen de los datos del destinatario (nombre, dirección, teléfono) que viajan dentro del despacho creado por F-02. F-03 no consulta a Ventas directamente. |
| Servicio de almacenamiento de objetos | Alojar las fotografías de evidencia en un bucket privado y emitir URL firmadas con expiración. |

### 4.3. Resultados

- Un inicio de sesión válido devuelve la ruta de la jornada en curso ordenada por secuencia de entrega.
- Una transición aceptada cambia el estado del despacho, persiste timestamp de servidor e identificador del repartidor, y queda registrada en la bitácora con estado anterior y estado nuevo.
- Un cierre como `ENTREGADO` persiste la referencia de la evidencia asociada al despacho.
- Un cierre como `FALLIDO` con intento real persiste motivo, evidencia, comentario opcional e incrementa en uno el contador de intentos, dejando el despacho disponible para F-04.
- Un cierre de jornada deja todo despacho pendiente en estado `FALLIDO` con motivo `NO_INTENTADO`, sin incrementar el contador de intentos.
- La carga operativa vigente del repartidor queda disponible para consulta de F-05 inmediatamente después de cada transición.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Autenticación y habilitación operativa

El sistema DEBE permitir el acceso únicamente a usuarios con rol `REPARTIDOR` y restringir las operaciones de escritura a quienes se encuentren habilitados operativamente según F-05.

#### CA-01. Inicio de sesión exitoso
- **DADO** un repartidor registrado, con turno vigente y estado operativo habilitante.
- **CUANDO** se autentica desde su celular.
- **ENTONCES** el sistema le concede acceso a la vista "Mi Ruta" y habilita las acciones de cambio de estado.

#### CA-02. Credencial ausente o expirada
- **DADO** que la solicitud no incluye token o el token venció.
- **CUANDO** se invoca cualquier recurso de la funcionalidad.
- **ENTONCES** el backend responde `401 Unauthorized` y no expone información de despachos.

#### CA-03. Rol distinto al requerido
- **DADO** un token válido cuyo rol no es `REPARTIDOR`.
- **CUANDO** se invocan los recursos de operación de campo.
- **ENTONCES** el backend responde `403 Forbidden`.

#### CA-04. Repartidor sin turno activo
- **DADO** un repartidor cuyo estado en F-05 es `FUERA_DE_TURNO`, `EN_DESCANSO` o `INACTIVO`.
- **CUANDO** accede a la aplicación.
- **ENTONCES** el sistema permite la consulta de su historial del día pero rechaza toda transición de estado, informando que su turno no se encuentra activo.

### RF-02. Consulta de la ruta asignada

El sistema DEBE mostrar al repartidor autenticado únicamente los despachos asignados a su persona para la jornada en curso, ordenados según la secuencia definida por F-02.

#### CA-05. Carga exitosa de la ruta del día
- **DADO** que el repartidor posee despachos en estado `ASIGNADO` o `EN_CAMINO` para la fecha actual.
- **CUANDO** accede a la vista "Mi Ruta".
- **ENTONCES** el sistema despliega la lista con código de rastreo, dirección de destino, nombre del destinatario, estado actual, número de intento y posición en la secuencia de entrega.

#### CA-06. Jornada sin asignaciones
- **DADO** que el repartidor no tiene despachos asignados para la fecha actual.
- **CUANDO** accede a la vista "Mi Ruta".
- **ENTONCES** el sistema muestra un mensaje informativo de ruta vacía en lugar de una tabla sin registros.

#### CA-07. Acceso a despachos de otro repartidor
- **DADO** que un repartidor manipula la petición para solicitar despachos asignados a un compañero.
- **CUANDO** el backend recibe la solicitud con un identificador distinto al contenido en el token.
- **ENTONCES** el sistema rechaza la petición con `403 Forbidden` y no expone ningún dato del despacho solicitado.

#### CA-08. Ausencia de arrastre de jornadas anteriores
- **DADO** que existen despachos de fechas anteriores que quedaron sin cierre por una falla del proceso de corte.
- **CUANDO** el repartidor carga su ruta del día.
- **ENTONCES** el sistema no los incorpora a la ruta vigente y los expone en una bandeja separada de "pendientes de regularización", sin permitir su entrega directa.

### RF-03. Consulta del detalle de un despacho

El sistema DEBE mostrar la información necesaria para ejecutar la entrega y contactar al destinatario.

#### CA-09. Detalle exitoso
- **DADO** un despacho asignado al repartidor autenticado.
- **CUANDO** abre su detalle.
- **ENTONCES** visualiza dirección completa, referencia, nombre del destinatario, teléfono de contacto habilitado para llamada directa, número de intento actual sobre el máximo configurado, fecha de entrega comprometida y estado vigente.

#### CA-10. Despacho no perteneciente al repartidor
- **DADO** un código de despacho asignado a otro repartidor.
- **CUANDO** se solicita su detalle.
- **ENTONCES** el backend responde `403 Forbidden` sin revelar dato alguno del despacho.

#### CA-11. Despacho inexistente
- **DADO** un código de rastreo que no corresponde a ningún despacho.
- **CUANDO** se solicita su detalle.
- **ENTONCES** el sistema informa que el recurso no existe y no presenta datos parciales.

### RF-04. Marcado de inicio de traslado

El sistema DEBE permitir al repartidor declarar que inició el traslado de un paquete, cambiando su estado a `EN_CAMINO`.

#### CA-12. Inicio de traslado exitoso
- **DADO** que un despacho se encuentra en estado `ASIGNADO`.
- **CUANDO** el repartidor pulsa "En camino" sobre ese despacho.
- **ENTONCES** el sistema cambia el estado a `EN_CAMINO`, registra timestamp de servidor e identificador del repartidor, actualiza el indicador visual y refleja la nueva carga operativa para consulta de F-05.

#### CA-13. Transición de estado no permitida
- **DADO** que un despacho ya fue marcado previamente como `ENTREGADO`.
- **CUANDO** el repartidor intenta marcarlo nuevamente como "En camino".
- **ENTONCES** el backend rechaza la operación con `409 Conflict`, conserva el estado original y notifica que el despacho ya fue cerrado.

#### CA-14. Despacho retirado de la ruta durante la jornada
- **DADO** que F-02 reasignó el despacho a otro repartidor o F-04 lo derivó a almacén mientras permanecía en pantalla.
- **CUANDO** el repartidor intenta operarlo con información desactualizada.
- **ENTONCES** el sistema rechaza la operación, informa que el despacho fue actualizado y fuerza el refresco de la ruta sin aplicar ningún cambio local.

### RF-05. Registro de entrega exitosa con evidencia

El sistema DEBE exigir evidencia fotográfica para cerrar un despacho como entregado; sin imagen cargada correctamente no se permite la confirmación.

#### CA-15. Confirmación de entrega con evidencia válida
- **DADO** que un despacho se encuentra en estado `EN_CAMINO`.
- **CUANDO** el repartidor captura una fotografía desde la cámara del dispositivo y pulsa "Confirmar entrega".
- **ENTONCES** el sistema comprime la imagen, elimina sus metadatos EXIF, la carga en el almacenamiento de objetos, persiste la referencia resultante junto al despacho, cambia el estado a `ENTREGADO` y registra timestamp e identificador del repartidor.

#### CA-16. Intento de confirmación sin evidencia
- **DADO** que el repartidor abre el formulario de entrega sin adjuntar fotografía.
- **CUANDO** pulsa "Confirmar entrega".
- **ENTONCES** el sistema mantiene deshabilitado el botón, muestra el mensaje de evidencia obligatoria y no emite petición al backend.

#### CA-17. Fallo en la carga de la imagen
- **DADO** que el repartidor confirma la entrega con una fotografía adjunta.
- **CUANDO** el servicio de almacenamiento responde con error o agota el tiempo de espera.
- **ENTONCES** el sistema NO modifica el estado del despacho, informa que la evidencia no pudo cargarse y conserva la imagen seleccionada en el formulario para permitir un reintento manual.

#### CA-18. Archivo inválido detectado en backend
- **DADO** que se envía un archivo con tipo no permitido o que excede el tamaño máximo aceptado.
- **CUANDO** el backend recibe la solicitud.
- **ENTONCES** rechaza la operación con `400 Bad Request`, no persiste el archivo y conserva el estado del despacho.

### RF-06. Registro de entrega fallida

El sistema DEBE permitir declarar una entrega como fallida seleccionando un motivo del catálogo predefinido, adjuntando evidencia fotográfica e incrementando el contador de intentos del despacho.

#### CA-19. Reporte de incidencia con motivo tipificado
- **DADO** que el repartidor no logra completar la entrega de un despacho en estado `EN_CAMINO`.
- **CUANDO** selecciona "Marcar como fallido", elige el motivo `CLIENTE_AUSENTE`, adjunta la fotografía del domicilio y confirma.
- **ENTONCES** el sistema cambia el estado a `FALLIDO`, almacena motivo, referencia de evidencia y comentario opcional, incrementa en uno el contador de intentos y deja el registro disponible para F-04.

#### CA-20. Motivo no seleccionado
- **DADO** que el repartidor abre el formulario de incidencia.
- **CUANDO** intenta confirmar sin haber elegido un motivo del catálogo.
- **ENTONCES** el sistema bloquea el envío y resalta el campo de motivo como obligatorio.

#### CA-21. Pérdida de conexión durante el envío
- **DADO** que el repartidor confirma una entrega fallida.
- **CUANDO** la petición no alcanza el backend por ausencia de señal.
- **ENTONCES** el sistema muestra un aviso explícito de que el cambio no se registró, conserva el estado anterior en la interfaz y exige un reintento explícito del usuario.

#### CA-22. Reintento idempotente de la misma operación
- **DADO** que el repartidor reintenta una operación cuyo resultado no conoce por corte de red.
- **CUANDO** el backend recibe una segunda solicitud con la misma clave de idempotencia.
- **ENTONCES** devuelve el resultado de la operación original sin duplicar el cambio de estado, el incremento del contador ni el registro en la bitácora.

### RF-07. Cierre de jornada y resolución de pendientes

El sistema DEBE garantizar que ningún despacho permanezca en estado no terminal al finalizar la jornada del repartidor, distinguiendo los intentos reales de entrega de los paquetes que nunca fueron intentados.

#### CA-23. Cierre con despachos pendientes
- **DADO** que el repartidor conserva despachos en estado `ASIGNADO` o `EN_CAMINO` al terminar su turno.
- **CUANDO** confirma el cierre de jornada, advertido de la cantidad de paquetes afectados.
- **ENTONCES** el sistema cambia esos despachos a `FALLIDO` con motivo `NO_INTENTADO`, **no** incrementa el contador de intentos, registra la bitácora correspondiente y los deja disponibles para F-04.

#### CA-24. Corte automático de respaldo
- **DADO** que el repartidor no ejecutó el cierre de jornada antes de la hora de corte configurada.
- **CUANDO** se ejecuta el proceso automático de cierre.
- **ENTONCES** el sistema aplica el mismo tratamiento de CA-23, identifica la operación como automática en la bitácora y libera la carga operativa del repartidor.

#### CA-25. Cierre sin pendientes
- **DADO** que todos los despachos de la jornada se encuentran en estado terminal.
- **CUANDO** el repartidor confirma el cierre.
- **ENTONCES** el sistema registra el cierre y presenta el resumen de la jornada sin generar registros de fallo.

### RF-08. Resumen de la jornada

El sistema DEBE ofrecer al repartidor la consolidación de su propio desempeño del día.

#### CA-26. Consolidado correcto
- **DADO** un repartidor con despachos en distintos estados durante la jornada.
- **CUANDO** consulta el resumen.
- **ENTONCES** visualiza el total asignado, entregados, fallidos con intento, no intentados y pendientes, con cifras coincidentes con su bitácora.

### RF-09. Acceso controlado a la evidencia fotográfica

El sistema DEBE permitir la visualización posterior de la evidencia sin exponer públicamente los objetos almacenados.

#### CA-27. Emisión de enlace firmado bajo demanda
- **DADO** un despacho con evidencia registrada.
- **CUANDO** un usuario autorizado solicita visualizarla.
- **ENTONCES** el sistema emite en ese momento una URL firmada con expiración corta, válida para una única visualización razonable.

#### CA-28. Acceso directo al objeto sin firma
- **DADO** que se intenta acceder a la ruta del objeto sin firma válida o con firma vencida.
- **CUANDO** se realiza la petición al almacenamiento.
- **ENTONCES** el acceso es denegado.

#### CA-29. Solicitud por usuario no autorizado
- **DADO** un usuario que no es el repartidor propietario del despacho ni posee el rol `GESTOR_DESPACHO`.
- **CUANDO** solicita el enlace de evidencia.
- **ENTONCES** el backend responde `403 Forbidden`.

### RF-10. Exposición de la carga operativa para monitoreo

El sistema DEBE exponer la información de despachos vigentes por repartidor para que F-05 calcule la saturación de la flota, sin que F-05 acceda a la base de datos de F-03.

#### CA-30. Consulta de carga vigente
- **DADO** que F-05 requiere calcular la ocupación de un repartidor.
- **CUANDO** consulta el servicio expuesto por F-03.
- **ENTONCES** recibe la cantidad, peso y volumen de los despachos en estado `ASIGNADO` y `EN_CAMINO` de ese repartidor para la jornada en curso.

#### CA-31. Exclusión de despachos terminales
- **DADO** que un despacho pasó a `ENTREGADO` o `FALLIDO`.
- **CUANDO** F-05 vuelve a consultar la carga del repartidor.
- **ENTONCES** ese despacho ya no se contabiliza en la ocupación vigente.

### RF-11. Catálogo de motivos de fallo

El sistema DEBE mantener y exponer el catálogo tipificado de motivos, como fuente única para la captura en campo y para la visualización en F-04.

#### CA-32. Consulta del catálogo
- **DADO** que el cliente móvil o F-04 requieren los motivos vigentes.
- **CUANDO** consultan el servicio de catálogo.
- **ENTONCES** reciben el listado de motivos seleccionables con su código y etiqueta, excluyendo los motivos de uso exclusivo del sistema.

### RF-12. Trazabilidad de las transiciones

El sistema DEBE conservar una bitácora auditable de cada cambio de estado ejecutado en campo.

#### CA-33. Registro de bitácora
- **DADO** que se acepta cualquier transición de estado.
- **CUANDO** la operación se persiste.
- **ENTONCES** se registran identificador del despacho, usuario ejecutor, origen manual o automático, timestamp de servidor, estado anterior, estado nuevo, motivo y observaciones cuando apliquen.

## 6. Frontend

La funcionalidad tendrá una experiencia web mobile-first compuesta por:

| Elemento | Responsabilidad |
|---|---|
| Pantalla de acceso | Autenticar al repartidor y comunicar con claridad el bloqueo por turno inactivo o rol incorrecto. |
| Vista "Mi Ruta" | Listar los despachos de la jornada en orden de secuencia, con estados de carga, vacío y error, e indicador visual por estado. |
| Detalle del despacho | Presentar dirección, referencia, destinatario, acción de llamada directa, intento actual y fecha comprometida. |
| Acción "En camino" | Confirmar el inicio de traslado y reflejar el nuevo estado sin recargar la vista completa. |
| Formulario de entrega | Capturar la fotografía, comprimirla, previsualizarla y mantener deshabilitada la confirmación mientras no exista evidencia válida. |
| Formulario de incidencia | Obligar la selección de motivo del catálogo, adjuntar evidencia y admitir comentario libre opcional. |
| Cierre de jornada | Advertir la cantidad de despachos que quedarán como no intentados antes de confirmar. |
| Resumen de jornada | Mostrar el consolidado del día del propio repartidor. |
| Retroalimentación | Informar éxito, validaciones, conflictos de estado, ausencia de red y errores de carga de evidencia. |

La interfaz debe impedir acciones conocidas como inválidas, pero las mismas reglas siempre deben volver a validarse en el backend.

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Validación de identidad y habilitación | Verificar el token, extraer el identificador del repartidor y confirmar su estado operativo vigente contra F-05. |
| Consulta de ruta | Recuperar exclusivamente los despachos del repartidor del token para la jornada en curso, ordenados por secuencia. |
| Máquina de estados | Validar que la transición solicitada sea permitida y rechazar con conflicto cualquier transición fuera del Anexo A. |
| Caso de uso de entrega | Verificar la existencia de evidencia, persistir su referencia y cerrar el despacho como entregado. |
| Caso de uso de incidencia | Validar el motivo, persistir evidencia y comentario, e incrementar el contador de intentos. |
| Caso de uso de cierre de jornada | Resolver los despachos pendientes como no intentados sin consumir intentos. |
| Proceso programado de corte | Ejecutar el cierre automático a la hora configurada para los repartidores que no lo hicieron. |
| Gestión de evidencia | Recibir la imagen, validar tipo y tamaño, delegar el almacenamiento y emitir enlaces firmados bajo demanda. |
| Control de idempotencia | Registrar la clave de operación y devolver el resultado original ante reintentos equivalentes. |
| Servicio de carga operativa | Exponer a F-05 la ocupación vigente del repartidor. |
| Servicio de catálogo | Exponer los motivos tipificados a la vista de campo y a F-04. |
| Persistencia y bitácora | Guardar el estado y su trazabilidad de manera consistente en PostgreSQL. |

Esta sección no prescribe nombres de clases, paquetes ni archivos. Las rutas, cuerpos, respuestas y códigos específicos se definirán en `specs/api-contract.md`.

## 8. Requisitos no funcionales

- **Seguridad:** toda petición requiere token JWT válido con rol `REPARTIDOR`. El backend debe validar que el despacho solicitado esté efectivamente asignado al usuario del token, sin confiar en identificadores enviados por el cliente.
- **Protección de datos del destinatario:** el teléfono y la dirección se muestran únicamente al repartidor propietario del despacho y únicamente mientras el despacho permanece en un estado no terminal. Todo acceso queda registrado. La aplicación no ofrece exportación ni copia masiva de estos datos.
- **Almacenamiento de evidencia:** las fotografías se alojan en un bucket privado y la base de datos de Despacho persiste únicamente la referencia del objeto. El acceso se realiza siempre mediante URL firmada con expiración, emitida en el momento de la solicitud.
- **Privacidad de la imagen:** la compresión en cliente debe eliminar los metadatos EXIF, evitando que la evidencia transporte coordenadas geográficas que la funcionalidad declara fuera de alcance.
- **Usabilidad móvil:** interfaz operable con una sola mano, áreas táctiles de al menos 44x44 px y contraste suficiente para lectura bajo luz solar directa.
- **Rendimiento:** la imagen debe comprimirse en el cliente antes de la carga, con máximo aproximado de 1 MB y 1280 px en el lado mayor. Toda transición de estado debe responder en menos de 2 segundos bajo red móvil 4G.
- **Conectividad:** el sistema asume conexión activa. Ante ausencia de red falla de forma explícita y no simula un cambio de estado local; no se implementa cola de sincronización diferida.
- **Idempotencia:** los endpoints de cambio de estado y de cierre de jornada deben tolerar reintentos del mismo cliente mediante una clave de idempotencia generada por operación, sin duplicar transiciones, intentos ni registros de bitácora.
- **Consistencia:** el cambio de estado, el incremento del contador y su bitácora deben persistirse en una misma unidad transaccional.
- **Aislamiento:** no se accede directamente a bases de datos de otros módulos; toda información externa se obtiene por API.
- **Trazabilidad:** cada transición debe registrar timestamp generado por el servidor y el identificador del repartidor o del proceso automático que la ejecutó.

## 9. Fuera de alcance

- **Resolución de incidencias (reprogramar o derivar a almacén):** corresponde a F-04. F-03 solo genera el estado `FALLIDO`.
- **Asignación de despachos y optimización de la secuencia de ruta:** corresponde a F-02. F-03 respeta el orden recibido y no lo modifica.
- **Administración de repartidores, vehículos, turnos y cálculo de saturación:** corresponde a F-05. F-03 solo consulta la habilitación y expone su carga vigente.
- **Cotización, cobertura y tarifas:** corresponde a F-01.
- **Notificación al cliente final y gestión financiera del pedido:** el dueño de la entidad pedido es Ventas y Postventa.
- **Geolocalización y navegación asistida:** no se captura GPS ni se ofrece guiado turn-by-turn; el repartidor utiliza aplicaciones externas de mapas.
- **Operación sin conexión:** no se implementa almacenamiento local ni sincronización diferida de estados o imágenes.
- **Firma digital del destinatario:** la evidencia de conformidad se limita a la fotografía.
- **Recepción física en almacén de los paquetes no intentados:** F-03 registra el estado lógico; el movimiento de inventario corresponde al módulo de Almacén.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 a CA-04 | Autenticar con token válido, ausente, de rol incorrecto y de repartidor sin turno. | Integración de seguridad | Acceso concedido en el caso válido; `401` y `403` en los inválidos; bloqueo de escritura con turno inactivo. |
| CA-05 a CA-08 | Consultar rutas con y sin asignaciones, con identificador ajeno y con despachos de fechas anteriores. | Integración y frontend | Lista ordenada por secuencia, estado vacío, `403` y ausencia de arrastre. |
| CA-09 a CA-11 | Consultar detalle propio, ajeno e inexistente. | Integración y frontend | Datos completos en el caso válido, `403` y error controlado en los demás. |
| CA-12 a CA-14 | Ejecutar transiciones válidas, inválidas y sobre despachos modificados por F-02 o F-04. | Unitaria e integración | Cambio aplicado en el caso válido y `409` con estado conservado en los conflictos. |
| CA-15 a CA-18 | Confirmar entrega con evidencia válida, sin evidencia, con almacenamiento caído y con archivo inválido. | Unitaria, integración y frontend | Estado `ENTREGADO` solo con evidencia persistida; sin cambio de estado en los fallos. |
| CA-19 a CA-22 | Registrar incidencias con y sin motivo, simular corte de red y repetir la operación con la misma clave. | Unitaria e integración | Contador incrementado una sola vez y ausencia de registros duplicados. |
| CA-23 a CA-25 | Cerrar jornada con pendientes, dejar vencer el corte automático y cerrar sin pendientes. | Integración con proceso programado | Despachos en `FALLIDO` con motivo `NO_INTENTADO` y contador de intentos inalterado. |
| CA-26 | Consultar el resumen tras una jornada con estados mixtos. | Integración | Cifras coincidentes con la bitácora. |
| CA-27 a CA-29 | Solicitar enlace firmado, acceder al objeto sin firma y solicitarlo con usuario no autorizado. | Integración de seguridad | Enlace válido solo para usuarios autorizados y acceso denegado en el resto. |
| CA-30 y CA-31 | Consultar la carga operativa antes y después de cerrar despachos. | Integración | Ocupación consistente con los estados vigentes. |
| CA-32 | Consultar el catálogo de motivos. | Integración | Listado tipificado sin motivos de uso exclusivo del sistema. |
| CA-33 | Consultar la bitácora tras cada transición aceptada. | Integración con persistencia | Usuario, origen, fecha y transición almacenados correctamente. |

Adicionalmente se ejecutarán tres recorridos funcionales completos:

1. `ASIGNADO` → `EN_CAMINO` → entrega con evidencia → `ENTREGADO`.
2. `ASIGNADO` → `EN_CAMINO` → incidencia con motivo y evidencia → `FALLIDO` con intento incrementado y visible para F-04.
3. `ASIGNADO` → cierre de jornada → `FALLIDO` con motivo `NO_INTENTADO` y contador de intentos sin variación.

Las pruebas unitarias cubrirán la máquina de estados, el control de intentos y la idempotencia; las pruebas de integración cubrirán seguridad, persistencia, bitácora y manejo de evidencia; las pruebas de frontend cubrirán estados visuales, validaciones de formulario y comportamiento ante ausencia de red.


## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Todos los criterios `CA-01` a `CA-33` están implementados y cuentan con pruebas exitosas.
- Los tres recorridos funcionales completos han sido verificados.
- Ninguna transición inválida de la máquina de estados es aceptada por el backend.
- El contador de intentos se incrementa exclusivamente ante intentos reales de entrega y nunca de forma duplicada ante reintentos.
- Ningún despacho permanece en estado no terminal tras el cierre de jornada o el corte automático.
- La evidencia es inaccesible sin enlace firmado vigente y accesible para F-04 cuando lo solicita.
- La carga operativa expuesta a F-05 refleja los estados vigentes.
- La interfaz comunica correctamente carga, vacío, validaciones, conflictos, errores de evidencia y ausencia de red.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede relacionarse con cada criterio de aceptación.

## Anexo A. Transiciones que ejecuta F-03

| Estado origen | Estado destino | Disparador | Efecto sobre el contador de intentos |
|---|---|---|---|
| `ASIGNADO` | `EN_CAMINO` | Acción del repartidor | Sin efecto |
| `EN_CAMINO` | `ENTREGADO` | Confirmación con evidencia | Sin efecto |
| `EN_CAMINO` | `FALLIDO` | Incidencia con motivo y evidencia | Incrementa en uno |
| `ASIGNADO` o `EN_CAMINO` | `FALLIDO` (`NO_INTENTADO`) | Cierre de jornada o corte automático | Sin efecto |

Cualquier otra transición es rechazada con conflicto. Los estados `PENDIENTE_ASIGNACION` y `DEVUELTO_A_ALMACEN` no son producidos por F-03; corresponden a F-02 y F-04 respectivamente.

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

## Anexo C. Integraciones requeridas para `specs/api-contract.md`

| Nº | Dirección | Propósito | Acuerdo pendiente |
|---|---|---|---|
| 1 | F-03 consulta a F-05 | Validar estado operativo y turno del repartidor autenticado. | Definir si se consulta por repartidor o si el dato viaja en el token. |
| 2 | F-05 consulta a F-03 | Obtener la carga vigente por repartidor para el cálculo de saturación. | Definir forma de la respuesta y frecuencia de consulta bajo el límite de 200 ms de F-05. |
| 3 | F-03 consume datos de F-02 | Recibir despachos asignados con secuencia de ruta, destinatario, dirección y teléfono. | Confirmar que F-02 incluye el teléfono del destinatario en el payload del despacho. |
| 4 | F-04 consume de F-03 | Leer despachos `FALLIDO` con motivo, intento y evidencia. | Confirmar que F-04 usa el catálogo del Anexo B y no uno propio. |
| 5 | F-04 consulta a F-03 | Obtener enlace firmado de evidencia bajo demanda. | Definir vigencia del enlace y rol autorizado. |
| 6 | Seguridad emite para F-03 | Token JWT con `idRepartidor` y rol embebidos. | Confirmar los claims exactos del token con el responsable de Seguridad. |
