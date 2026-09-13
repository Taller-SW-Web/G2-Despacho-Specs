# Especificación F-01: Gestor de Zonas Geográficas y Cotizador de Envíos

**Responsable:** Valqui
**Estado:** En especificación
**Actor principal:** Gestor de Despacho / Administrador de Zonas

## 1. Contexto

La determinación precisa de las tarifas y la cobertura de entrega es el primer paso en el ciclo de despacho comercial. Antes de que una orden sea pagada y enviada a programación, las aplicaciones de venta (tienda web, marketplace, chatbot o carrito de compras) necesitan conocer si la dirección del cliente se encuentra dentro del rango de cobertura y cuál es el costo exacto del flete logístico.

El Gestor de Zonas Geográficas y Cotizador de Envíos opera como un servicio autónomo dentro del módulo de Despacho. Trabaja sobre sus propias tablas maestras de polígonos/distritos y matrices de tarifas, garantizando total independencia operativa al no requerir información de clientes ni depender del estado de las órdenes en curso para realizar sus cálculos.

## 2. Propósito

Permitir la configuración administrativa de las zonas de cobertura logística y la matriz tarifaria de envíos, y exponer un endpoint público y ágil de cotización para calcular el costo de entrega en función del destino, peso, volumen o distancia, proveyendo esta información en tiempo real a los canales de venta.

## 3. Alcance

Esta funcionalidad incluye:

- Administración de Zonas Geográficas: registro, delimitación y activación/desactivación de distritos, sectores o códigos postales de cobertura.
- Matriz de Tarifas: configuración de reglas de precio basadas en peso (kg), volumen (m³), distancia kilométrica o tarifa plana por zona.
- Endpoint de Cotización de Envíos (`POST /api/v1/zonas/cotizar`): servicio consultado por el carrito de compras o módulos comerciales para obtener el costo de envío y el tiempo estimado de entrega.
- Validación de Cobertura: verificación inmediata de si una dirección o coordenadas geográficas se encuentran dentro de las zonas activas de despacho.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario debe estar autenticado y autorizado con el rol de Administrador (`ADMIN`) o Gestor de Despacho (`GESTOR_DESPACHO`) para las operaciones de configuración de zonas y tarifas.
- El endpoint de cotización es de acceso público o protegido mediante API Key de canal comercial; no requiere token JWT de usuario.
- La solicitud de cotización debe incluir datos válidos: peso mayor a cero, volumen mayor o igual a cero y un destino identificable (distrito, código postal o coordenadas).
- Para cotizar contra una zona, la zona debe existir y encontrarse en estado `ACTIVO`.
- La configuración de una nueva zona no debe generar solapamientos conflictivos con zonas ya registradas.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Proporcionar la identidad autenticada mediante token JWT y los permisos de Administrador o Gestor de Despacho. |
| Ventas y Postventa | Consumir el endpoint de cotización desde el carrito de compras y los canales comerciales antes de confirmar una orden. |
| Programación y Asignación (F-02) | Utilizar las zonas activas para filtrar la cola de despachos pendientes y dar coherencia a los pedidos simulados. |
| Monitoreo de Flota (F-05) | Asociar repartidores y vehículos a las zonas de cobertura registradas para atender los despachos asignados. |

### 4.3. Resultados

- Un registro válido de zona se guarda con identificador único, su delimitación geográfica y estado `ACTIVO`, sin solapamientos conflictivos.
- Una regla tarifaria configurada se asocia a la zona correspondiente y se aplica a todas las cotizaciones futuras para ese sector.
- Una solicitud de cotización válida retorna el costo de envío calculado, la moneda, el plazo estimado y los días hábiles de entrega.
- Una consulta de cobertura retorna la bandera `coberturaDisponible` y, cuando corresponde, el identificador y nombre de la zona coincidente.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Configuración de zonas de cobertura

El sistema DEBE permitir al administrador registrar y delimitar zonas geográficas de atención logística asociadas a distritos, sectores o polígonos de servicio, y mantenerlas activas o inactivas según la operación.

#### CA-01. Creación exitosa de una zona de cobertura

- **DADO** que un usuario administrador ingresa el nombre de la zona (ej. "Lima Centro"), distritos comprendidos (Miraflores, San Isidro, Lince) y estado "Activo".
- **CUANDO** confirma la creación de la zona en el sistema.
- **ENTONCES** el backend valida que no existan solapamientos conflictivos y registra la zona con identificador único y estado `ACTIVO`.

#### CA-02. Consulta de cobertura para dirección fuera de rango

- **DADO** que se consulta la cobertura para un distrito no registrado en ninguna zona activa (ej. provincia no cubierta).
- **CUANDO** el cotizador evalúa la dirección.
- **ENTONCES** el sistema retorna código `200 OK` con bandera `coberturaDisponible: false` y un mensaje: "La dirección se encuentra fuera de nuestra zona de cobertura".

#### CA-03. Rechazo de zona duplicada o solapada

- **DADO** que se intenta registrar una zona cuyo nombre, distrito o polígono ya se encuentra cubierto por una zona activa existente.
- **CUANDO** el administrador confirma la creación.
- **ENTONCES** el sistema rechaza la operación con código `409 Conflict`, detalla el solapamiento detectado y no persiste la zona duplicada.

#### CA-04. Acceso sin permisos requeridos

- **DADO** que un usuario sin el rol `ADMIN` ni `GESTOR_DESPACHO` intenta registrar o modificar zonas o tarifas.
- **CUANDO** realiza la petición al backend.
- **ENTONCES** el sistema rechaza la solicitud con código `403 Forbidden` y no expone información de configuración.

### RF-02. Matriz tarifaria y reglas de cobro

El sistema DEBE permitir parametrizar las reglas de tarificación por zona, soportando esquemas de costo base, recargo por kilogramo adicional y factor de cubicaje volumétrico.

#### CA-05. Configuración de tarifa mixta por peso y zona

- **DADO** que se configura para la zona "Lima Norte" una tarifa base de 10.00 PEN hasta 3 kg, más 2.00 PEN por cada kg adicional.
- **CUANDO** se guarda la regla tarifaria.
- **ENTONCES** el sistema asocia la regla a la zona y la aplica a todas las cotizaciones futuras para ese sector.

#### CA-06. Rechazo de regla tarifaria inválida

- **DADO** que se configura una regla con tarifa base negativa, una zona inexistente o rangos de peso inconsistentes.
- **CUANDO** el administrador intenta guardar la regla.
- **ENTONCES** el sistema rechaza la operación con código `400 Bad Request`, detalla los campos inválidos y no persiste la regla.

### RF-03. Cotización en tiempo real para canales de venta

El sistema DEBE calcular y retornar el costo de envío estimado y los días hábiles de entrega a partir del destino, peso y dimensiones del paquete, evaluando primero si el destino se encuentra dentro de la cobertura activa.

#### CA-07. Cotización exitosa dentro de cobertura

- **DADO** un paquete de 5 kg con destino a un distrito dentro de la zona "Lima Centro".
- **CUANDO** el carrito de compras invoca el endpoint `POST /api/v1/zonas/cotizar`.
- **ENTONCES** el sistema calcula el flete conforme a la matriz tarifaria activa y retorna el monto total calculado junto con la promesa de entrega (ej. "Entrega estimada en 24 a 48 horas").

#### CA-08. Cotización con parámetros de peso inválidos

- **DADO** una solicitud de cotización con peso negativo o cero.
- **CUANDO** se envía al endpoint de cotización.
- **ENTONCES** el sistema rechaza la petición con código `400 Bad Request` indicando "El peso del paquete debe ser mayor a cero".

#### CA-09. Cotización con volumen inválido

- **DADO** una solicitud de cotización con volumen negativo.
- **CUANDO** se envía al endpoint de cotización.
- **ENTONCES** el sistema rechaza la petición con código `400 Bad Request` indicando "El volumen del paquete debe ser mayor o igual a cero".

#### CA-10. Cotización sin cobertura de entrega

- **DADO** una solicitud de cotización para un destino fuera de todas las zonas activas.
- **CUANDO** se envía al endpoint de cotización.
- **ENTONCES** el sistema retorna código `200 OK` con `coberturaDisponible: false`, sin costo de envío ni plazo estimado, y con el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura".

#### CA-11. Cotización sin token de usuario

- **DADO** que el endpoint de cotización es de acceso público o protegido por API Key de canal comercial.
- **CUANDO** un canal de venta envía una solicitud sin token JWT de usuario.
- **ENTONCES** el sistema procesa la cotización normalmente y no exige autenticación de usuario.

## 6. Frontend

La funcionalidad tendrá una experiencia web responsive compuesta por:

| Elemento | Responsabilidad |
|---|---|
| Panel de Gestión de Zonas | Mostrar el listado paginado de zonas con filtros por nombre, distrito y estado, y acciones para activar o desactivar coberturas. |
| Formulario de Zona | Registrar o editar una zona con su nombre, distritos comprendidos, códigos postales y delimitación sobre mapa. |
| Mapa de Delimitación | Permitir dibujar o seleccionar polígonos de cobertura sobre un mapa (ej. Leaflet) y previsualizar el área registrada. |
| Formulario de Tarifas | Configurar tarifa base, recargo por kilogramo, rangos de peso y factor de cubicaje por zona. |
| Retroalimentación y Notificaciones | Informar resultados exitosos, solapamientos detectados, validaciones de campos y errores de red. |

La interfaz debe impedir acciones conocidas como inválidas, pero las mismas reglas siempre deben volver a validarse en el backend.

## 7. Backend

El backend deberá cubrir las siguientes responsabilidades lógicas:

| Componente lógico | Responsabilidad |
|---|---|
| Controlador de Zonas | Exponer el CRUD de zonas de cobertura (`GET /api/v1/zonas`) y validar estructura de datos y autorización. |
| Servicio de Matriz Tarifaria | Administrar las reglas de precio por zona y validar su consistencia antes de persistir. |
| Motor de Cotización | Calcular el costo de envío y el plazo estimado a partir del destino, peso y dimensiones del paquete. |
| Validación de Cobertura | Determinar si un distrito, código postal o coordenadas se encuentran dentro de las zonas activas mediante cálculo geoespacial (PostGIS). |
| Caché de Tarifas | Mantener las tablas maestras de zonas y tarifas en memoria caché o base de datos local para responder cotizaciones sin acoplamientos externos. |
| Persistencia y Auditoría | Almacenar zonas, tarifas y cambios de estado de manera consistente en PostgreSQL (Supabase). |

Los cuerpos, respuestas y códigos específicos se encuentran centralizados en `specs/api-contract.md` y se publicarán mediante Swagger UI desde el backend desplegado.

## 8. Requisitos no funcionales

- **Rendimiento:** El endpoint de cotización debe procesar la solicitud en menos de 100 ms para no perjudicar la experiencia de usuario en el checkout de ventas.
- **Alta Disponibilidad e Independencia:** El motor de cálculo debe operar sobre sus propias tablas maestras de tarifas en memoria caché o base de datos local sin acoplamientos externos.
- **Seguridad:** Los endpoints de administración y configuración de zonas requieren token JWT con rol `ADMIN` o `GESTOR_DESPACHO`. El endpoint de cotización para clientes es de acceso público o protegido por API Key de aplicación.
- **Trazabilidad:** Cada creación, modificación o desactivación de zonas y tarifas debe registrar el usuario y la marca temporal correspondientes.

## 9. Fuera de alcance

- **Procesamiento de pagos:** El cobro efectivo del costo de envío cotizado corresponde a la pasarela de pagos del módulo de Ventas.
- **Generación de despachos:** La creación de la orden de envío formal se produce tras el pago y corresponde a la funcionalidad F-02.
- **Ruteo y asignación:** La asignación de choferes para la zona corresponde a F-02 y F-05.
- **Ejecución de la entrega en calle:** La confirmación final de la entrega corresponde exclusivamente a la Web Responsive del Repartidor (F-03).

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 a CA-03 | Registrar zonas válidas, duplicadas o solapadas mediante HTTP client y consultar cobertura fuera de rango. | Integración y unitaria | Zona creada con identificador único y estado `ACTIVO`, rechazo `409` para duplicados y `200` con `coberturaDisponible: false` fuera de rango. |
| CA-04 | Invocar los endpoints de administración sin credenciales o con rol incorrecto. | Integración de seguridad | Código `403 Forbidden` y bloqueo total de información de configuración. |
| CA-05 y CA-06 | Guardar reglas tarifarias válidas e inválidas y verificar su aplicación. | Unitaria e integración | Regla asociada correctamente a la zona y rechazo `400` para reglas inconsistentes. |
| CA-07 a CA-10 | Ejecutar cotizaciones con peso y volumen válidos e inválidos, dentro y fuera de cobertura. | Unitaria e integración | Cálculo correcto del flete según la matriz, codificación `200` y `400` según corresponda. |
| CA-11 | Invocar el endpoint de cotización sin token de usuario. | Integración de seguridad | Respuesta exitosa y cobertura validada sin autenticación de usuario. |

Además, se ejecutarán dos recorridos funcionales completos:

1. `Configuración de Zona + Tarifa` → registro de zona activa → asociación de regla tarifaria → cotización exitosa dentro de cobertura.
2. `Cotización Sin Cobertura` → solicitud con destino fuera de rango → respuesta `200 OK` con `coberturaDisponible: false`.

Las pruebas unitarias cubrirán las reglas de cálculo tarifario y validación de cobertura; las pruebas de integración cubrirán seguridad, persistencia PostgreSQL y transaccionalidad; y las pruebas de frontend validarán el panel de zonas, el mapa y los formularios de tarifas.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Todos los criterios `CA-01` a `CA-11` están implementados y cuentan con pruebas automatizadas exitosas.
- Los dos recorridos funcionales completos han sido verificados de extremo a extremo.
- El registro de zonas y tarifas funciona sin inconsistencias y sin solapamientos conflictivos.
- El endpoint de cotización devuelve tarifas correctas conforme a las reglas configuradas.
- Se valida adecuadamente la cobertura geográfica, tanto dentro como fuera de rango.
- La interfaz visual muestra correctamente el mapa de delimitación, estados de carga y errores.
- No se han incorporado alcances no especificados.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.