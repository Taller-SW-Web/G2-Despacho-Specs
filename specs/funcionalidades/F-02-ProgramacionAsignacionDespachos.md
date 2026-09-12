# Especificación: F-02 - Panel de Programación y Asignación de Despachos

## 1. Contexto
En una arquitectura orientada a microservicios para la gestión logística de última milla, el módulo de Despacho debe gestionar de manera autónoma el ciclo de vida de los envíos sin depender directamente de las bases de datos de otros módulos como Ventas o Facturación[cite: 2].

Una vez confirmado un pedido en el sistema comercial, este debe transformarse en una solicitud de despacho. Para asegurar la continuidad operativa y permitir el desarrollo e integración ágil sin bloqueos entre equipos de trabajo, el módulo de Despacho debe exponer una API receptora estándar y ofrecer una capacidad de generación directa de despachos de prueba (mediante herramientas como Postman o una acción en la interfaz de usuario). Asimismo, el Gestor de Despacho requiere de un panel centralizado que le permita evaluar la carga de trabajo pendiente y asignar eficientemente los despachos a los operadores logísticos según su disponibilidad de turno y capacidad de transporte (información provista por el subsistema de Flota, F-06).

## 2. Propósito
Proveer al Gestor de Despacho de un panel operativo administrativo para monitorear la cola de pedidos pendientes de entrega y asignarlos de forma balanceada y controlada a los repartidores disponibles, garantizando el respeto de los límites de peso y volumen de cada vehículo y habilitando la generación independiente de órdenes de prueba para pruebas operativas.

## 3. Alcance
Incluye:
- Endpoint receptor de solicitudes de despacho externas provenientes de sistemas de pedidos o ventas.
- Mecanismo de generación de pedidos/despachos de prueba (mediante endpoint de testing o botón "Generar Pedido de Prueba" en la interfaz) para garantizar la independencia técnica del módulo.
- Panel (Dashboard) administrativo de monitoreo de la cola de despachos en estado `PENDIENTE_ASIGNACION`.
- Consumo del catálogo de repartidores con estado de turno (`DISPONIBLE`, `OCUPADO`, `FUERA_DE_TURNO`) y balance de capacidad operativa provisto por el componente de Monitoreo de Flota (F-06).
- Asignación operativa de un despacho a un repartidor determinado, realizando la transición de estado a `ASIGNADO` y la reserva de capacidad del vehículo.

## 4. Requisitos

### Requisito 1: Recepción y Generación de Solicitudes de Despacho
El sistema DEBE proveer un mecanismo estándar para recibir solicitudes de despacho desde sistemas externos y permitir la generación autónoma de solicitudes de prueba con datos simulados válidos.

#### Escenario: Recepción exitosa de solicitud de despacho
- DADO que un sistema autorizado (o cliente REST) envía una solicitud de creación de despacho con identificador de pedido, dirección de destino, coordenadas geográficas, peso en kilogramos y volumen en metros cúbicos.
- CUANDO la petición ingresa al endpoint receptor con un token de autenticación válido.
- ENTONCES el sistema valida la completitud de los datos, registra el despacho en la base de datos con estado inicial `PENDIENTE_ASIGNACION` y retorna un código `201 Created` junto con el identificador único del despacho generado.

#### Escenario: Generación de pedido de prueba para desarrollo independiente
- DADO que el Gestor de Despacho o desarrollador requiere generar carga de trabajo de prueba sin depender del módulo de Ventas.
- CUANDO presiona el botón "Generar Pedido de Prueba" en el panel o invoca el endpoint de generación de prueba.
- ENTONCES el sistema genera automáticamente un pedido con datos aleatorios consistentes dentro del rango operativo, crea el despacho asociado en estado `PENDIENTE_ASIGNACION` y actualiza inmediatamente la cola del panel.

#### Escenario: Rechazo de solicitud con datos incompletos o inconsistentes
- DADO que se envía una solicitud de despacho con peso menor o igual a cero o sin dirección de entrega.
- CUANDO la petición es evaluada por la capa de validación del backend.
- ENTONCES el sistema rechaza la solicitud con un código `400 Bad Request` y un mensaje descriptivo de las restricciones incumplidas.

### Requisito 2: Monitoreo de Cola de Despachos Pendientes
El sistema DEBE listar de forma paginada y en tiempo real los despachos cuyo estado sea `PENDIENTE_ASIGNACION`, permitiendo filtrar y ordenar por fecha estimada de entrega, zona y volumen/peso.

#### Escenario: Consulta exitosa de despachos pendientes
- DADO que existen despachos registrados en estado `PENDIENTE_ASIGNACION`.
- CUANDO el usuario con rol "Gestor de Despacho" ingresa a la vista del panel de programación.
- ENTONCES el sistema despliega la lista de despachos pendientes mostrando identificador, pedido de origen, dirección de destino, peso, volumen, fecha límite de entrega y tiempo de espera en cola.

#### Escenario: Restricción de acceso por rol no autorizado
- DADO que un usuario autenticado pero sin rol de "Gestor de Despacho" (por ejemplo, rol "Repartidor" o usuario externo) intenta consultar la cola administrativa de asignación.
- CUANDO realiza la petición al backend adjuntando su token JWT.
- ENTONCES el sistema deniega el acceso respondiendo con código de estado `403 Forbidden`.

### Requisito 3: Asignación de Despacho a Repartidor según Capacidad y Disponibilidad
El sistema DEBE permitir al Gestor de Despacho asignar un despacho pendiente a un repartidor habilitado, comprobando que el repartidor esté disponible y que la adición del paquete no sobrepase sus capacidades máximas de carga (peso en kilogramos y volumen en metros cúbicos).

#### Escenario: Asignación exitosa dentro de la capacidad disponible
- DADO un despacho en estado `PENDIENTE_ASIGNACION` con peso de 15 kg y volumen de 0.1 m³, y un repartidor en estado `DISPONIBLE` con capacidad remanente de 50 kg y 0.8 m³.
- CUANDO el Gestor selecciona al repartidor y confirma la acción "Asignar Despacho".
- ENTONCES el sistema asocia el despacho al repartidor, transiciona el estado del despacho a `ASIGNADO`, descuenta la capacidad remanente del repartidor y emite un evento de confirmación de asignación.

#### Escenario: Rechazo de asignación por superación de capacidad de carga
- DADO un despacho con peso de 30 kg y un repartidor cuya capacidad remanente es de únicamente 20 kg.
- CUANDO el Gestor intenta asignar dicho despacho al repartidor.
- ENTONCES el sistema bloquea la operación, retorna un código `422 Unprocessable Entity` alertando "Capacidad de peso del repartidor excedida" y mantiene el despacho en estado `PENDIENTE_ASIGNACION`.

#### Escenario: Rechazo de asignación por operador no disponible
- DADO un repartidor cuyo estado actual es `FUERA_DE_TURNO` u `OCUPADO`.
- CUANDO el Gestor intenta seleccionarlo para una nueva asignación manual.
- ENTONCES el sistema muestra el operador como deshabilitado y rechaza cualquier solicitud de asignación con código `409 Conflict`.

## 5. Requisitos no funcionales
- **Seguridad:** Todas las operaciones de consulta y asignación requieren autenticación obligatoria mediante token JWT con rol verificado `GESTOR_DESPACHO` emitido por el módulo central de Seguridad[cite: 2].
- **Concurrencia e Integridad Transaccional:** La operación de asignación debe ejecutarse bajo control transaccional o bloqueo optimista para prevenir condiciones de carrera (evitar asignar el mismo despacho a dos repartidores de forma simultánea).
- **Rendimiento:** El tiempo de respuesta para la carga del panel de despachos pendientes no debe exceder los 300 ms en condiciones normales para lotes de hasta 100 registros.
- **Trazabilidad:** Cada asignación debe registrar la marca temporal exacta (timestamp ISO 8601) y el identificador del usuario gestor que realizó la asignación.

## 6. Fuera de alcance
- **Cálculo y optimización de rutas dinámicas:** La generación de polilíneas y ordenamiento geográfico detallado de paradas corresponde al componente de ruteo/mapas.
- **Ejecución y registro de entrega en campo:** El seguimiento en ruta, captura de firma y confirmación final de entrega corresponde a la App del Repartidor (Integrante 3).
- **Gestión de incidencias y entregas fallidas:** La reprogramación y derivación a devolución tras intentos fallidos corresponde al Centro de Entregas Fallidas (F-05, Integrante 5)[cite: 2].
- **Administración de catálogo de flota y vehículos:** El registro, altas/bajas y mantenimiento de operadores y unidades vehiculares corresponde al Monitoreo de Flota (F-06, Integrante 6).

## Criterio de completitud
La capacidad se considera correctamente implementada cuando:
- Todos los requisitos están implementados.
- Todos los escenarios definidos se cumplen.
- Los requisitos no funcionales aplicables se cumplen.
- No se han incorporado funcionalidades fuera del alcance.
