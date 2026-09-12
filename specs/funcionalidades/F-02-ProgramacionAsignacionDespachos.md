# Especificación F-02: Programación y Asignación de Despachos

**Responsable:** Tarqui
**Estado:** En especificación
**Actor principal:** Gestor de Despacho

## 1. Contexto

En la logística de última milla, una vez que un pedido es confirmado y pagado en los canales comerciales, debe incorporarse de forma inmediata y ordenada al flujo operativo de transporte. El módulo de Despacho y Entrega a Domicilio debe gestionar este proceso de manera autónoma, desacoplada y sin depender directamente de las bases de datos de otros módulos como Ventas, Inventario o Seguridad.

Para asegurar un desarrollo ágil y permitir que las pruebas de integración del equipo se ejecuten sin bloqueos externos, el sistema debe exponer una API receptora estándar y ofrecer una capacidad de generación directa de órdenes de prueba simuladas. Asimismo, el Gestor de Despacho requiere de un panel operativo centralizado que le permita evaluar la cola de pedidos pendientes de entrega y asignarlos de forma balanceada a los operadores de transporte disponibles, respetando estrictamente los límites de peso y volumen de cada vehículo y su turno de trabajo.

## 2. Propósito

Permitir que el Gestor de Despacho visualice y administre la cola de pedidos pendientes de entrega, genere órdenes de prueba para validaciones técnicas autónomas, y asigne los despachos a los repartidores habilitados garantizando que no se sobrepasen las capacidades de carga vehicular ni se asigne personal fuera de servicio.

## 3. Alcance

Esta funcionalidad incluye:

- API receptora de solicitudes de despacho provenientes de módulos externos (Ventas y Postventa o canales de comercio electrónico).
- Mecanismo de generación autónoma de despachos de prueba con datos simulados consistentes (mediante endpoint REST y acción directa en la interfaz de usuario).
- Panel (Dashboard) administrativo con la lista paginada y filtrable de despachos en estado `PENDIENTE_ASIGNACION`.
- Consulta en tiempo real de la disponibilidad de operadores y su balance de capacidad remanente (peso en kilogramos y volumen en metros cúbicos), consumiendo la información provista por Monitoreo de Flota (F-05).
- Asignación manual o asistida de un despacho pendiente a un repartidor en turno, transicionando el estado a `ASIGNADO` y descontando la capacidad del vehículo.
- Control de concurrencia y validación transaccional para impedir la doble asignación de un mismo despacho.
- Registro de auditoría para cada orden recibida, simulada y asignada.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario debe estar autenticado y autorizado con el rol de Gestor de Despacho (`GESTOR_DESPACHO`).
- Para la asignación, el despacho debe existir y encontrarse en estado `PENDIENTE_ASIGNACION`.
- La solicitud de despacho debe incluir datos obligatorios: código de pedido, dirección de destino, coordenadas geográficas, peso mayor a cero y volumen mayor a cero.
- El repartidor seleccionado debe existir, encontrarse en estado `DISPONIBLE` o `EN_RUTA` y contar con turno activo en la jornada.
- La suma del peso y volumen del despacho no debe superar la capacidad remanente del vehículo asignado al repartidor.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Proporcionar la identidad autenticada mediante token JWT y los permisos del Gestor de Despacho. |
| Ventas y Postventa | Emitir las solicitudes de despacho formales tras la confirmación de compra. |
| Monitoreo de Flota (F-05) | Proveer el catálogo de repartidores en turno con su vehículo y balance de capacidad (`GET /api/v1/repartidores/disponibles`). |
| Operación del Repartidor (F-03) | Recibir los despachos en estado `ASIGNADO` para su ejecución en ruta. |
| Entregas Fallidas (F-04) | Retornar a la cola de asignación (`PENDIENTE_ASIGNACION`) los despachos reprogramados tras un intento fallido. |

### 4.3. Resultados

- Una solicitud de despacho válida se registra en la base de datos con estado inicial `PENDIENTE_ASIGNACION`, código de rastreo único y marca temporal.
- La generación de prueba produce un despacho inmediatamente visible en la cola sin requerir comunicación con Ventas.
- Una asignación válida transiciona el estado del despacho a `ASIGNADO`, vincula el identificador del repartidor y descuenta su capacidad remanente.
- Toda operación de asignación registra fecha, usuario gestor, identificador del despacho, identificador del operador y observaciones.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Recepción y creación de solicitudes de despacho

El sistema DEBE permitir registrar solicitudes de despacho desde sistemas comerciales autorizados y proveer un mecanismo de simulación para desarrollo y pruebas independientes.

#### CA-01. Recepción exitosa desde sistema comercial

- **DADO** que un sistema externo envía una solicitud con identificador de pedido, datos del destinatario, dirección, coordenadas, peso y volumen válidos.
- **CUANDO** la petición es procesada con un token de autorización válido.
- **ENTONCES** el sistema guarda el despacho con estado `PENDIENTE_ASIGNACION`, genera un código de rastreo y responde con código `201 Created`.

#### CA-02. Generación autónoma de pedidos de prueba (testing)

- **DADO** que el Gestor de Despacho o desarrollador requiere generar carga de trabajo de prueba sin depender del módulo de Ventas.
- **CUANDO** solicita la generación de prueba mediante la interfaz o el endpoint de simulación.
- **ENTONCES** el sistema autogenera un pedido y despacho con datos consistentes en estado `PENDIENTE_ASIGNACION` y lo incorpora de inmediato a la cola de asignación.

#### CA-03. Rechazo de solicitud con datos incompletos o inconsistentes

- **DADO** que una solicitud carece de dirección de entrega o presenta un peso menor o igual a cero.
- **CUANDO** la solicitud es evaluada por la capa de validación.
- **ENTONCES** el sistema rechaza la operación con código `400 Bad Request`, detalla los campos inválidos y no persiste registros parciales.

### RF-02. Consultar la cola de despachos pendientes

El sistema DEBE permitir que el Gestor de Despacho consulte y filtre de forma paginada los despachos que esperan asignación de transporte.

#### CA-04. Listado con despachos pendientes

- **DADO** que existen despachos registrados en estado `PENDIENTE_ASIGNACION`.
- **CUANDO** el Gestor accede a la vista de Programación y Asignación.
- **ENTONCES** el sistema despliega la lista paginada mostrando código de rastreo, pedido, dirección, peso, volumen, fecha límite y tiempo en espera.

#### CA-05. Listado sin despachos pendientes

- **DADO** que no existen pedidos pendientes de asignación.
- **CUANDO** el Gestor consulta la vista.
- **ENTONCES** el sistema muestra un estado visual vacío indicando "No hay despachos pendientes de asignación".

#### CA-06. Acceso sin permisos requeridos

- **DADO** que un usuario sin el rol `GESTOR_DESPACHO` intenta acceder al listado.
- **CUANDO** realiza la petición al backend.
- **ENTONCES** el sistema rechaza la solicitud con código `403 Forbidden` y no expone información operativa.

### RF-03. Asignar despacho a un repartidor

El sistema DEBE permitir asignar un despacho en estado `PENDIENTE_ASIGNACION` a un repartidor disponible, verificando que no se exceda la capacidad de carga vehicular.

#### CA-07. Asignación exitosa dentro de la capacidad disponible

- **DADO** un despacho en estado `PENDIENTE_ASIGNACION` y un repartidor en estado `DISPONIBLE` cuya capacidad remanente cubre el peso y volumen del paquete.
- **CUANDO** el Gestor selecciona al repartidor y confirma la asignación.
- **ENTONCES** el sistema cambia el estado del despacho a `ASIGNADO`, descuenta la capacidad remanente del operador y registra la trazabilidad.

#### CA-08. Rechazo por capacidad de peso o volumen excedida

- **DADO** un despacho cuyo peso o volumen supera la capacidad remanente del repartidor seleccionado.
- **CUANDO** el Gestor intenta confirmar la asignación.
- **ENTONCES** el sistema bloquea la operación, responde con código `422 Unprocessable Entity`, alerta "Capacidad de carga del repartidor excedida" y mantiene el despacho en `PENDIENTE_ASIGNACION`.

#### CA-09. Rechazo por repartidor no disponible o fuera de turno

- **DADO** un repartidor que se encuentra en estado `FUERA_DE_TURNO`, `INACTIVO` o `SATURADO`.
- **CUANDO** se intenta asignar un despacho a dicho operador.
- **ENTONCES** el sistema rechaza la solicitud con código `409 Conflict` y mantiene el despacho en cola.

#### CA-10. Despacho en estado incompatible o ya asignado

- **DADO** un despacho que ya fue asignado previamente o cuyo estado no es `PENDIENTE_ASIGNACION`.
- **CUANDO** se intenta ejecutar una asignación concurrente o desactualizada.
- **ENTONCES** el sistema detecta el conflicto transaccional, rechaza la operación con `409 Conflict` y notifica que el despacho ya fue procesado.

### RF-04. Mantener trazabilidad y auditoría

El sistema DEBE registrar un historial auditable de cada asignación y cambio de estado realizado sobre el despacho.

#### CA-11. Registro de auditoría y actualización de carga operativa

- **DADO** que una asignación es aceptada exitosamente.
- **CUANDO** finaliza la transacción en el backend.
- **ENTONCES** se persiste un registro de auditoría con identificador del despacho, repartidor asignado, usuario gestor, marca temporal y nuevo balance de capacidad.

## 6. Frontend

La funcionalidad tendrá una experiencia web responsive compuesta por:

| Elemento | Responsabilidad |
|---|---|
| Panel de Programación (Dashboard) | Mostrar la cola de despachos en `PENDIENTE_ASIGNACION` con filtros por fecha, zona y paginación. |
| Modal de Asignación de Repartidor | Desplegar el catálogo de repartidores disponibles, mostrando vehículo, turno y barra de ocupación actual. |
| Botón "Generar Pedido de Prueba" | Permitir la simulación inmediata de despachos para pruebas locales sin salir de la vista. |
| Indicadores de Capacidad y Carga | Alertar visualmente si un paquete excede la capacidad del operador seleccionado antes de confirmar. |
| Retroalimentación y Notificaciones | Informar resultados exitosos, validaciones de sobrecarga, conflictos de concurrencia y errores de red. |

La interfaz debe deshabilitar acciones inválidas en cliente, pero todas las restricciones de negocio deben validarse de manera estricta en el backend.

## 7. Backend

El backend deberá cubrir las siguientes responsabilidades lógicas:

| Componente lógico | Responsabilidad |
|---|---|
| Controlador Receptor de Despachos | Exponer el endpoint para recibir órdenes externas y validar estructura de datos (`POST /api/v1/despachos/solicitudes`). |
| Servicio Generador de Simulación | Autogenerar datos válidos de prueba para permitir la autonomía del equipo (`POST /api/v1/despachos/solicitudes/simular`). |
| Consulta de Cola de Pendientes | Recuperar despachos en estado `PENDIENTE_ASIGNACION` con ordenamiento por fecha límite y soporte de paginación. |
| Caso de Uso de Asignación | Validar estado del despacho, disponibilidad del operador y capacidad de carga vehicular de forma transaccional. |
| Cliente de Integración con Flota | Consumir la API de Monitoreo de Flota (F-05) para verificar disponibilidad y capacidades actualizadas. |
| Persistencia y Auditoría | Almacenar transiciones de estado y registros de trazabilidad en PostgreSQL de forma consistente. |

Las rutas, cuerpos, respuestas y códigos específicos se encuentran centralizados en `specs/api-contract.md` y se publicarán mediante Swagger UI desde el backend desplegado.

## 8. Requisitos no funcionales

- **Seguridad:** Todas las operaciones administrativas requieren autenticación obligatoria mediante token JWT con rol verificado `GESTOR_DESPACHO`.
- **Aislamiento:** El módulo gestiona sus propios datos en PostgreSQL (Supabase) sin acceder directamente a bases de datos de otros módulos.
- **Concurrencia e Integridad Transaccional:** La asignación debe aplicar control transaccional o bloqueo optimista para impedir que dos gestores asignen el mismo paquete de forma simultánea.
- **Rendimiento:** El endpoint de consulta de cola de pendientes debe responder en menos de 250 ms para lotes de hasta 100 registros.
- **Trazabilidad:** Cada asignación debe registrar la marca temporal exacta (UTC) y el identificador del usuario gestor.
- **Usabilidad y Responsividad:** El panel debe ser adaptable a computadoras de escritorio y tablets operativas.

## 9. Fuera de alcance

- **Cálculo dinámico de rutas y optimización GPS:** La navegación calle por calle corresponde a herramientas cartográficas externas (Google Maps / Waze).
- **Ejecución y confirmación de entrega en calle:** Corresponde exclusivamente a la Web Responsive del Repartidor (F-03).
- **Gestión de incidencias y entregas fallidas:** Las reprogramaciones y derivaciones a almacén corresponden a Entregas Fallidas (F-04).
- **Administración del catálogo de flota y choferes:** El alta de repartidores, turnos y vehículos físicos corresponde a Monitoreo de Flota (F-05).
- **Facturación y cobro:** Pertenecen al módulo comercial de Ventas y Finanzas.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 a CA-03 | Enviar solicitudes válidas, simuladas e inválidas mediante HTTP client. | Integración y unitaria | Despacho creado con `201`, simulación autónoma exitosa y rechazo `400` para datos inválidos. |
| CA-04 y CA-05 | Consultar listado con y sin despachos pendientes en base de datos. | Integración y frontend | Visualización correcta de la tabla paginada y estado vacío amigable. |
| CA-06 | Invocar endpoints de asignación y cola sin credenciales o con rol incorrecto. | Integración de seguridad | Código `403 Forbidden` y bloqueo total de información sensible. |
| CA-07 a CA-10 | Ejecutar pruebas de asignación con capacidad suficiente, sobrecarga, operador fuera de turno y conflicto concurrente. | Unitaria e integración | Transición exitosa a `ASIGNADO` y rechazo controlado con `409` y `422` según corresponda. |
| CA-11 | Consultar la tabla de auditoría tras completar una asignación válida. | Integración con persistencia | Registro correcto de usuario gestor, despacho, chofer y nuevo balance de capacidad. |

Además, se ejecutarán dos recorridos funcionales completos:

1. `Recepción / Simulación de Pedido` → validación de datos → registro en cola con estado `PENDIENTE_ASIGNACION`.
2. `Despacho en Cola` → selección de repartidor disponible con capacidad suficiente → confirmación de asignación → estado `ASIGNADO` y actualización de capacidad remanente.

Las pruebas unitarias cubrirán las reglas de cálculo de capacidad y validación de estados; las pruebas de integración cubrirán seguridad, persistencia en Supabase y transaccionalidad; y las pruebas de frontend validarán el dashboard y diálogos de asignación.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Todos los criterios `CA-01` a `CA-11` están implementados y cuentan con pruebas automatizadas exitosas.
- Los dos recorridos funcionales completos han sido verificados de extremo a extremo.
- La generación de pedidos simulados opera de forma autónoma sin depender del módulo de Ventas.
- La validación de capacidad (peso y volumen) previene sobrecargas en cualquier vehículo asignado.
- La interfaz visual muestra correctamente estados de carga, lista paginada, alertas de sobrecarga y confirmaciones.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.

