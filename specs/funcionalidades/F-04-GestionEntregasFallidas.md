# Especificación: Centro de Entregas Fallidas y Reprogramaciones

## 1. Contexto
En la logística de última milla, un porcentaje de las entregas no puede completarse debido a factores como la ausencia del cliente, direcciones inubicables o rechazo del paquete. Como el diseño exige una arquitectura orientada a microservicios donde no hay acceso a base de datos entre los módulos[cite: 2], el módulo de Despacho debe gestionar el ciclo de vida del transporte de forma autónoma. Se requiere una capacidad para que el Gestor resuelva estas excepciones y se comunique de forma asíncrona mediante APIs con el módulo de Ventas y Postventa (dueño de la entidad pedido)[cite: 2] cuando un paquete se declara como pérdida o devolución definitiva.

## 2. Propósito
Permitir al Gestor de Despacho visualizar las incidencias de ruta en tiempo real y tomar decisiones operativas sobre cada paquete fallido: reprogramar una nueva fecha de entrega o cancelar definitivamente el despacho, notificando de manera automatizada al módulo de Ventas.

## 3. Alcance
Incluye:
- Panel (Dashboard) de despachos en estado `FALLIDO` con bitácora de intentos y motivos.
- Lógica de validación de reintentos máximos permitidos por despacho.
- Funcionalidad de reprogramación de fecha (regresa el paquete a la cola de asignación).
- Funcionalidad de cancelación definitiva (cambio a estado `DEVUELTO_A_ALMACEN`).
- Notificación asíncrona hacia la API del módulo de Ventas y Postventa al confirmar una cancelación[cite: 2].

## 4. Requisitos

### Requisito 1: Panel de Monitoreo de Incidencias
El sistema DEBE listar todos los despachos cuyo estado actual sea `FALLIDO`, mostrando el motivo reportado por el repartidor y el número de intento actual.

#### Escenario: Visualización exitosa de incidencias
- DADO que existen despachos marcados como fallidos en la base de datos de Despacho.
- CUANDO el Gestor de Despacho ingresa a la vista "Entregas Fallidas".
- ENTONCES el sistema despliega una tabla con el ID de rastreo, fecha del incidente, motivo, número de intento y evidencia fotográfica asociada.

#### Escenario: Acceso denegado por rol incorrecto
- DADO que un usuario con rol de "Repartidor" intenta acceder al endpoint de listado de fallos.
- CUANDO el frontend solicita los datos enviando el token JWT.
- ENTONCES el backend rechaza la petición con un error `403 Forbidden` indicando privilegios insuficientes.

### Requisito 2: Reprogramación de Despacho
El sistema DEBE permitir al Gestor asignar una nueva fecha de entrega, siempre y cuando no se haya superado el límite máximo de reintentos.

#### Escenario: Reprogramación dentro del límite permitido
- DADO que un despacho fallido tiene 1 intento registrado (límite máximo = 2).
- CUANDO el Gestor selecciona "Reprogramar" y elige la fecha de mañana.
- ENTONCES el sistema actualiza la fecha, cambia el estado a `PENDIENTE_ASIGNACION` y mantiene el contador en 1.

#### Escenario: Intento de reprogramación excediendo el límite
- DADO que un despacho fallido tiene 2 intentos registrados (límite máximo = 2).
- CUANDO el Gestor abre el detalle del despacho.
- ENTONCES el sistema deshabilita el botón "Reprogramar", muestra una alerta de "Límite de intentos superado" y solo permite la opción "Devolver a Almacén".

### Requisito 3: Cancelación Definitiva y Notificación a Ventas
El sistema DEBE permitir marcar un despacho como incobrable/inubicable y emitir un evento asíncrono para que el módulo de Ventas asuma el control financiero.

#### Escenario: Devolución exitosa con notificación asíncrona
- DADO que el Gestor determina que un paquete no podrá ser entregado.
- CUANDO hace clic en "Devolver a Almacén" y confirma la acción.
- ENTONCES el sistema localiza el despacho, cambia su estado interno a `DEVUELTO_A_ALMACEN` y publica un evento/mensaje asíncrono dirigido al módulo de Ventas indicando que el pedido asociado falló definitivamente[cite: 1, 2].

#### Escenario: Falla temporal de comunicación con Ventas
- DADO que se confirma una devolución a almacén.
- CUANDO el backend de Despacho intenta notificar a Ventas mediante un Webhook asíncrono, pero el servidor remoto no responde.
- ENTONCES el sistema guarda el estado `DEVUELTO_A_ALMACEN` en la base de datos local de Despacho y encola la notificación en un esquema de reintentos para enviarla en cuanto la red se restablezca.

## 5. Requisitos no funcionales
- **Seguridad:** Todas las peticiones al backend deben incluir un token JWT válido emitido por el módulo de Seguridad, y el componente debe aplicar autenticación y desarrollo seguro[cite: 2].
- **Integración:** La comunicación con el módulo de Ventas y Postventa debe realizarse mediante APIs de forma asíncrona (ej. Webhooks con código HTTP 202 o colas de mensajería)[cite: 1, 2].
- **Trazabilidad:** Cada cambio de estado debe registrar un timestamp y el ID del usuario (Gestor) que tomó la decisión de reprogramar o cancelar.

## 6. Fuera de alcance
- **Gestión de Reembolsos y Notas de Crédito** — El dueño de la entidad pedido y sus flujos financieros es el módulo de Ventas y Postventa[cite: 2].
- **Captura en campo del estado "Fallido"** — La acción de marcar inicialmente el paquete como inubicable mediante GPS/cámara le corresponde a la App del Repartidor (Integrante 3).
- **Enrutamiento de paquetes reprogramados** — Esta funcionalidad solo devuelve el paquete a la cola; la reasignación a un nuevo vehículo le corresponde al Panel de Asignación (Integrante 2).

## Criterio de completitud
La capacidad se considera correctamente implementada cuando:
- Todos los requisitos están implementados.
- Todos los escenarios definidos se cumplen.
- Los requisitos no funcionales aplicables se cumplen.
- No se han incorporado funcionalidades fuera del alcance.