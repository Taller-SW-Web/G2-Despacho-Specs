# Especificación: App Móvil del Repartidor y Evidencia de Entrega

## 1. Contexto
La ejecución física de la entrega ocurre en calle, donde el repartidor no dispone de un equipo de escritorio. Dado que el diseño exige una arquitectura orientada a microservicios sin acceso directo a base de datos entre módulos, el módulo de Despacho debe ofrecer su propia interfaz operativa de campo, autónoma respecto de Ventas y Postventa. Esta capacidad corresponde al punto de origen de la información del ciclo de transporte: es aquí donde se generan los estados `EN_CAMINO`, `ENTREGADO` y `FALLIDO` que posteriormente consumen el Panel de Asignación y el Centro de Entregas Fallidas dentro del mismo módulo.

La interfaz se implementa como una vista web adaptada a dispositivos móviles (mobile-first, responsive), no como una aplicación nativa, de modo que comparte backend y esquema de autenticación con el resto del módulo de Despacho.

## 2. Propósito
Permitir al Repartidor consultar los despachos asignados a su ruta del día, actualizar el estado de cada paquete en tiempo real desde su celular y registrar evidencia fotográfica obligatoria del resultado de la entrega, garantizando la trazabilidad de quién ejecutó cada transición y en qué momento.

## 3. Alcance
Incluye:
- Autenticación del repartidor mediante token JWT emitido por el módulo de Seguridad.
- Listado de despachos asignados al repartidor autenticado para la jornada en curso.
- Transición de estado a `EN_CAMINO` al iniciar el traslado de un paquete.
- Registro de entrega exitosa (`ENTREGADO`) con evidencia fotográfica obligatoria.
- Registro de entrega fallida (`FALLIDO`) con motivo tipificado, evidencia fotográfica y comentario opcional.
- Compresión de la imagen en el cliente y carga hacia el servicio de almacenamiento de objetos.
- Registro de timestamp e identificador del repartidor en cada cambio de estado.
- Validación de transiciones de estado permitidas.

## 4. Requisitos

### Requisito 1: Consulta de la Ruta Asignada
El sistema DEBE mostrar al repartidor autenticado únicamente los despachos asignados a su persona para la jornada en curso, ordenados según la secuencia de ruta definida por el Panel de Asignación.

#### Escenario: Carga exitosa de la ruta del día
- DADO que el repartidor posee despachos en estado `ASIGNADO` para la fecha actual.
- CUANDO inicia sesión desde su celular y accede a la vista "Mi Ruta".
- ENTONCES el sistema despliega una lista con el ID de rastreo, dirección de destino, nombre del destinatario, estado actual y posición en la secuencia de entrega.

#### Escenario: Intento de acceso a despachos de otro repartidor
- DADO que un repartidor manipula la petición para solicitar los despachos asignados a un compañero.
- CUANDO el backend recibe la solicitud con un ID de repartidor distinto al contenido en el token JWT.
- ENTONCES el sistema rechaza la petición con un error `403 Forbidden` y no expone ningún dato del despacho solicitado.

#### Escenario: Jornada sin asignaciones
- DADO que el repartidor no tiene despachos asignados para la fecha actual.
- CUANDO accede a la vista "Mi Ruta".
- ENTONCES el sistema muestra un mensaje informativo de ruta vacía en lugar de una tabla sin registros.

### Requisito 2: Marcado de Inicio de Traslado
El sistema DEBE permitir al repartidor declarar que inició el traslado de un paquete, cambiando su estado a `EN_CAMINO`.

#### Escenario: Inicio de traslado exitoso
- DADO que un despacho se encuentra en estado `ASIGNADO`.
- CUANDO el repartidor pulsa "En camino" sobre ese despacho.
- ENTONCES el sistema cambia el estado a `EN_CAMINO`, registra el timestamp del servidor junto con el ID del repartidor y actualiza el indicador visual en la lista.

#### Escenario: Transición de estado no permitida
- DADO que un despacho ya fue marcado previamente como `ENTREGADO`.
- CUANDO el repartidor intenta marcarlo nuevamente como "En camino".
- ENTONCES el backend rechaza la operación con un error `409 Conflict`, conserva el estado original y notifica al usuario que el despacho ya fue cerrado.

### Requisito 3: Registro de Entrega Exitosa con Evidencia
El sistema DEBE exigir evidencia fotográfica para cerrar un despacho como entregado; sin imagen cargada no se permite la confirmación.

#### Escenario: Confirmación de entrega con evidencia válida
- DADO que un despacho se encuentra en estado `EN_CAMINO`.
- CUANDO el repartidor captura una fotografía desde la cámara del dispositivo y pulsa "Confirmar entrega".
- ENTONCES el sistema comprime la imagen, la carga en el servicio de almacenamiento, persiste la URL resultante junto al despacho, cambia el estado a `ENTREGADO` y registra timestamp e ID del repartidor.

#### Escenario: Intento de confirmación sin evidencia
- DADO que el repartidor abre el formulario de entrega pero no adjunta ninguna fotografía.
- CUANDO pulsa "Confirmar entrega".
- ENTONCES el sistema mantiene deshabilitado el botón de confirmación y muestra el mensaje "La evidencia fotográfica es obligatoria", sin emitir petición al backend.

#### Escenario: Fallo en la carga de la imagen
- DADO que el repartidor confirma la entrega con una fotografía adjunta.
- CUANDO el servicio de almacenamiento responde con error o agota el tiempo de espera.
- ENTONCES el sistema NO modifica el estado del despacho, informa que la evidencia no pudo cargarse y conserva la imagen seleccionada en el formulario para permitir un reintento manual.

### Requisito 4: Registro de Entrega Fallida
El sistema DEBE permitir declarar una entrega como fallida seleccionando un motivo de un catálogo predefinido, adjuntando evidencia fotográfica e incrementando el contador de intentos del despacho.

#### Escenario: Reporte de incidencia con motivo tipificado
- DADO que el repartidor no logra completar la entrega de un despacho en estado `EN_CAMINO`.
- CUANDO selecciona "Marcar como fallido", elige el motivo "Cliente ausente" del catálogo, adjunta la fotografía del domicilio y confirma.
- ENTONCES el sistema cambia el estado a `FALLIDO`, almacena el motivo, la URL de la evidencia y el comentario opcional, incrementa en uno el contador de intentos y deja el registro disponible para el Centro de Entregas Fallidas.

#### Escenario: Motivo no seleccionado
- DADO que el repartidor abre el formulario de incidencia.
- CUANDO intenta confirmar sin haber elegido un motivo del catálogo.
- ENTONCES el sistema bloquea el envío y resalta el campo de motivo como obligatorio.

#### Escenario: Pérdida de conexión durante el envío
- DADO que el repartidor confirma una entrega fallida.
- CUANDO la petición no alcanza el backend por ausencia de señal.
- ENTONCES el sistema muestra un aviso de "Sin conexión: el cambio no se registró", conserva el estado anterior en la interfaz y exige un reintento explícito del usuario, evitando así que el repartidor asuma un cierre que no se persistió.

## 5. Requisitos no funcionales
- **Seguridad:** Toda petición debe incluir un token JWT válido emitido por el módulo de Seguridad. El backend debe validar que el rol sea "Repartidor" y que el despacho solicitado esté efectivamente asignado al usuario del token.
- **Almacenamiento de evidencia:** Las fotografías se alojan en un servicio de almacenamiento de objetos externo y la base de datos de Despacho persiste únicamente la URL. Las URL deben ser de acceso restringido o firmadas con expiración, para evitar exposición pública de domicilios de clientes.
- **Usabilidad móvil:** Interfaz mobile-first, operable con una sola mano, con áreas táctiles de al menos 44x44 px y contraste suficiente para lectura bajo luz solar directa.
- **Rendimiento:** La imagen debe comprimirse en el cliente antes de la carga (máximo aproximado de 1 MB y 1280 px en el lado mayor). Toda transición de estado debe responder en menos de 2 segundos bajo red móvil 4G.
- **Conectividad:** El sistema asume conexión activa. Ante ausencia de red, la aplicación falla de forma explícita y no simula un cambio de estado local; no se implementa cola de sincronización diferida.
- **Trazabilidad:** Cada transición de estado debe registrar timestamp generado por el servidor y el ID del repartidor que la ejecutó.
- **Idempotencia:** Los endpoints de cambio de estado deben tolerar reintentos del mismo cliente sin generar registros duplicados en la bitácora de intentos.

## 6. Fuera de alcance
- **Resolución de incidencias (reprogramar o devolver a almacén)** — Corresponde al Centro de Entregas Fallidas y Reprogramaciones (Integrante 1).
- **Asignación de despachos a repartidores y optimización de la secuencia de ruta** — Corresponde al Panel de Asignación (Integrante 2).
- **Notificación al módulo de Ventas y gestión financiera del pedido** — El dueño de la entidad pedido es el módulo de Ventas y Postventa.
- **Geolocalización y navegación asistida** — No se captura GPS ni se ofrece guiado turn-by-turn; el repartidor utiliza aplicaciones externas de mapas.
- **Operación sin conexión** — No se implementa almacenamiento local ni sincronización diferida de estados o imágenes.
- **Firma digital del destinatario** — La evidencia de conformidad se limita a la fotografía.

## Criterio de completitud
La capacidad se considera correctamente implementada cuando:
- Todos los requisitos están implementados.
- Todos los escenarios definidos se cumplen.
- Los requisitos no funcionales aplicables se cumplen.
- No se han incorporado funcionalidades fuera del alcance.
