# Especificación F-01: Gestor de Zonas Geográficas y Cotizador de Envíos

**Responsable:** Valqui
**Estado:** En especificación
**Actor principal:** Gestor de Despacho / Administrador
**Lineamiento del curso:** Gestión de zonas y tarifas de entrega

## 1. Contexto

Todos los envíos de la tienda salen de un único centro de despacho. La determinación de la cobertura y del costo de envío desde ese centro es el primer paso del ciclo de despacho. Antes de que un pedido se confirme, Ventas y Postventa y los canales de venta necesitan saber si la dirección del cliente está dentro de la cobertura y cuánto cuesta el envío.

Esta funcionalidad opera sobre sus propias tablas de zonas y tarifas dentro de la base de datos del módulo. No requiere información de clientes ni del estado de los pedidos, pero sí utiliza el identificador, el peso y las dimensiones de cada producto proporcionados por Productos y Ofertas para calcular el peso y el volumen cotizables.

Además de atender a los canales, F-01 es la fuente única de cobertura dentro del módulo: Programación y Asignación (F-02) la utiliza para asignar una zona a cada despacho recibido, y Monitoreo de Flota (F-05) la utiliza para asignar una zona de trabajo a cada repartidor en su jornada.

## 2. Propósito

Permitir la configuración de las zonas de cobertura y de la matriz tarifaria, exponer a los canales de venta un servicio de cotización en tiempo real y proveer al resto del módulo la resolución de la zona correspondiente a un destino.

## 3. Alcance

Esta funcionalidad incluye:

- Administración de zonas de cobertura: registro, edición, activación y desactivación mediante distritos y códigos postales.
- Matriz de tarifas: reglas de precio por zona con tarifa base, recargo por kilogramo adicional y factor volumétrico.
- Uso del identificador, peso y dimensiones de cada producto, obtenidos de Productos y Ofertas, para calcular el peso y volumen de la cotización.
- Cotización de envíos para Ventas y Postventa y los canales de venta, con costo en soles y plazo estimado.
- Validación de cobertura y resolución de zona para un destino, como servicio interno para F-02 y F-05.
- Registro de auditoría de los cambios en zonas y tarifas.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- Las operaciones de configuración requieren un token JWT con rol `GESTOR_DESPACHO`.
- La cotización requiere un token de servicio con scope `cotizaciones:calcular`; no requiere token de usuario humano.
- Cada producto cotizable debe tener identificador, peso mayor a cero y dimensiones válidas en Productos y Ofertas.
- Una solicitud de cotización debe incluir los productos y cantidades, además de un destino identificable mediante distrito o código postal.
- Solo se cotiza contra zonas en estado `ACTIVO`.
- Un distrito o código postal no puede pertenecer a más de una zona activa.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Emitir el JWT humano con `GESTOR_DESPACHO` y los tokens de servicio con scopes. |
| Productos y Ofertas | Proveer para cada producto su identificador, peso y dimensiones vigentes. |
| Ventas y Postventa | Consumir la cotización e incorporar el costo de despacho al total del pedido. |
| Canal Marketplace y Canal Chatbot | Solicitar o mostrar la cotización durante el checkout o la conversación, según el acuerdo de integración con Ventas y Postventa. |
| Programación y Asignación (F-02) | Solicitar la resolución de zona al recibir una solicitud de despacho y rechazar destinos sin cobertura. |
| Monitoreo de Flota (F-05) | Utilizar el catálogo de zonas activas para asignar la zona de trabajo del repartidor en la jornada. |

### 4.3. Resultados

- Una zona válida se guarda con identificador único, distritos o códigos postales y estado `ACTIVO`.
- Una regla tarifaria válida queda asociada a su zona y se aplica a las cotizaciones siguientes.
- Una cotización válida retorna la cobertura, el costo, la moneda y el plazo estimado en días hábiles.
- Una resolución de zona retorna el identificador de la zona que cubre el destino o indica que no existe cobertura.
- La desactivación de una zona no modifica los despachos ya registrados en ella.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Configuración de zonas de cobertura

El sistema DEBE permitir registrar zonas por distritos o códigos postales, y mantenerlas activas o inactivas según la operación.

#### CA-01. Creación exitosa de una zona de cobertura

- **DADO** que un usuario con rol `GESTOR_DESPACHO` ingresa el nombre de la zona ("Lima Centro"), los distritos comprendidos (Miraflores, San Isidro, Lince) y el estado "Activo".
- **CUANDO** confirma la creación.
- **ENTONCES** el backend valida que los distritos no pertenezcan a otra zona activa y registra la zona con identificador único y estado `ACTIVO`.

#### CA-02. Consulta de cobertura para dirección fuera de rango

- **DADO** que se consulta la cobertura de un distrito que no pertenece a ninguna zona activa.
- **CUANDO** el sistema evalúa el destino.
- **ENTONCES** retorna `200 OK` con `coberturaDisponible: false` y el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura".

#### CA-03. Rechazo de zona o cobertura duplicada

- **DADO** que se intenta registrar una zona cuyo nombre, distrito o código postal ya está registrado en una zona activa.
- **CUANDO** se confirma la creación.
- **ENTONCES** el sistema responde `409 Conflict`, detalla la duplicidad y no persiste la zona.

#### CA-04. Acceso sin permisos requeridos

- **DADO** que un usuario sin rol `GESTOR_DESPACHO` intenta registrar o modificar zonas o tarifas.
- **CUANDO** realiza la petición.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone información de configuración.

### RF-02. Matriz tarifaria y reglas de cobro

El sistema DEBE permitir parametrizar las tarifas por zona con tarifa base, recargo por kilogramo adicional y factor volumétrico.

#### CA-05. Configuración de tarifa mixta por peso y zona

- **DADO** que se configura para "Lima Norte" una tarifa base de 10.00 PEN hasta 3 kg y un recargo de 2.00 PEN por kilogramo adicional.
- **CUANDO** se guarda la regla.
- **ENTONCES** el sistema la asocia a la zona y la aplica a las cotizaciones siguientes para esa zona.

#### CA-06. Rechazo de regla tarifaria inválida

- **DADO** una regla con tarifa base negativa, zona inexistente o rangos de peso inconsistentes.
- **CUANDO** se intenta guardar.
- **ENTONCES** el sistema responde `400 Bad Request`, detalla los campos inválidos y no persiste la regla.

### RF-03. Cotización en tiempo real para canales de venta

El sistema DEBE calcular el costo de envío y el plazo estimado a partir del destino y de los pesos y dimensiones de los productos, evaluando primero la cobertura.

#### CA-07. Cotización exitosa dentro de cobertura

- **DADO** una solicitud cuyos productos tienen identificador, peso y dimensiones válidas, con un peso total de 5 kg y destino en un distrito de "Lima Centro".
- **CUANDO** un canal de venta solicita la cotización.
- **ENTONCES** el sistema calcula el costo según la tarifa activa de la zona y retorna el monto, la moneda y el plazo estimado (ej. "Entrega estimada en 24 a 48 horas").

#### CA-08. Cotización con peso inválido

- **DADO** una solicitud con peso negativo o igual a cero.
- **CUANDO** se envía la cotización.
- **ENTONCES** el sistema responde `400 Bad Request` con el mensaje "El peso del paquete debe ser mayor a cero".

#### CA-09. Cotización con datos físicos inválidos

- **DADO** una solicitud que contiene un producto sin identificador, peso o dimensiones válidas.
- **CUANDO** se envía la cotización.
- **ENTONCES** el sistema responde `422 Unprocessable Entity`, identifica el producto incompleto y no calcula una cotización hasta que Productos y Ofertas proporcione sus datos físicos.

#### CA-10. Cotización sin cobertura de entrega

- **DADO** una solicitud con destino fuera de todas las zonas activas.
- **CUANDO** se envía la cotización.
- **ENTONCES** el sistema responde `200 OK` con `coberturaDisponible: false`, sin costo ni plazo, y con el mensaje de destino fuera de cobertura.

#### CA-11. Cotización con token de servicio

- **DADO** que un canal obtuvo un token técnico con `cotizaciones:calcular`.
- **CUANDO** envía la solicitud con `Authorization: Bearer <token>`.
- **ENTONCES** el sistema procesa la cotización sin requerir una sesión de usuario humano.

### RF-04. Resolución de zona para el módulo

El sistema DEBE ofrecer al resto del módulo la resolución de la zona que cubre un destino, como fuente única de cobertura.

#### CA-12. Resolución de zona para una solicitud de despacho

- **DADO** que F-02 recibe una solicitud de despacho con destino en San Isidro, perteneciente a "Lima Centro".
- **CUANDO** solicita la resolución de zona.
- **ENTONCES** el sistema retorna el identificador y el nombre de "Lima Centro", y F-02 los asocia al despacho.

#### CA-13. Desactivación de una zona con despachos registrados

- **DADO** una zona con despachos registrados que aún no han sido entregados.
- **CUANDO** el Gestor la desactiva.
- **ENTONCES** la zona deja de aceptar nuevas cotizaciones y nuevas solicitudes, pero los despachos existentes conservan su zona y continúan su ciclo sin cambios, incluidas sus reprogramaciones.

#### CA-14. Límite de solicitudes de cotización

- **DADO** que un mismo origen supera el límite de solicitudes de cotización configurado.
- **CUANDO** envía una nueva solicitud.
- **ENTONCES** el sistema responde `429 Too Many Requests` sin procesar el cálculo.

## 6. Frontend

La funcionalidad tendrá una experiencia web responsive compuesta por:

| Elemento | Responsabilidad |
|---|---|
| Panel de Gestión de Zonas | Listado paginado de zonas con filtros por nombre, distrito y estado, y acciones de activación o desactivación. |
| Formulario de Zona | Registro o edición del nombre, distritos y códigos postales. |
| Formulario de Tarifas | Configuración de tarifa base, recargo por kilogramo, rangos de peso y factor volumétrico. |
| Confirmación de desactivación | Advertir que la zona dejará de aceptar cotizaciones y solicitudes nuevas. |
| Retroalimentación | Informar resultados, duplicidades, validaciones y errores de red. |

La interfaz debe impedir acciones conocidas como inválidas, pero las mismas reglas siempre deben volver a validarse en el backend.

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Gestión de zonas | CRUD de zonas con validación de distritos y códigos postales duplicados, y autorización. |
| Servicio de matriz tarifaria | Administrar las reglas por zona y validar su consistencia. |
| Integración con Productos y Ofertas | Obtener o validar el identificador, peso y dimensiones de los productos cotizados. |
| Motor de cotización | Calcular costo y plazo a partir del destino y los datos físicos de los productos. |
| Resolución de zona | Determinar la zona activa que contiene el distrito o código postal; servicio interno para F-02. |
| Control de límite de solicitudes | Aplicar el límite configurado por `sub` del cliente técnico e IP. |
| Persistencia y auditoría | Almacenar zonas, tarifas y sus cambios con usuario y marca temporal. |

Las rutas, cuerpos, respuestas y códigos específicos se centralizan en `integraciones/api-contract.md` y se publicarán mediante Swagger UI desde el backend desplegado.

## 8. Requisitos no funcionales

- **Rendimiento:** la cotización y la resolución de zona deben responder en menos de 100 ms.
- **Aislamiento:** no se accede a bases de datos de otros módulos; los datos físicos se obtienen mediante el contrato acordado con Productos y Ofertas.
- **Seguridad:** la configuración requiere JWT con rol `GESTOR_DESPACHO`. La cotización requiere token de servicio con `cotizaciones:calcular` y no expone configuración interna.
- **Comunicación:** la cotización es la única integración con otros módulos que responde de forma síncrona, porque el canal la necesita para mostrar el costo al cliente.
- **Trazabilidad:** toda creación, modificación o desactivación de zonas y tarifas registra usuario y marca temporal en UTC.

## 9. Fuera de alcance

- **Cobro del envío:** corresponde al proceso de pago de los canales y a Ventas y Postventa.
- **Registro de despachos:** corresponde a F-02.
- **Asignación de repartidores:** corresponde a F-02 con información de F-05.
- **Ejecución de la entrega:** corresponde a F-03.

Las posibles ampliaciones de esta funcionalidad están centralizadas en [Pendientes](./pendiente.md), sección F-01. No forman parte de los criterios de completitud actuales.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 a CA-03 | Registrar zonas válidas y duplicadas; consultar cobertura fuera de rango. | Integración y unitaria | Zona creada en `ACTIVO`, `409` para distritos o códigos duplicados y `coberturaDisponible: false` fuera de rango. |
| CA-04 | Invocar la configuración sin credenciales o con rol incorrecto. | Integración de seguridad | `403 Forbidden` sin datos de configuración. |
| CA-05 y CA-06 | Guardar reglas válidas e inválidas. | Unitaria e integración | Regla asociada a la zona y `400` para reglas inconsistentes. |
| CA-07 a CA-11 | Cotizar productos con datos físicos válidos e inválidos, dentro y fuera de cobertura, sin token. | Unitaria e integración | Costo correcto, `200`, `400` o `422` según corresponda. |
| CA-12 y CA-13 | Resolver zona para un destino cubierto y desactivar una zona con despachos. | Integración | Zona asociada al despacho; despachos existentes sin cambios tras la desactivación. |
| CA-14 | Superar el límite de solicitudes desde un mismo origen. | Integración | `429 Too Many Requests`. |

Además, se ejecutarán dos recorridos funcionales completos:

1. Registro de zona → asociación de tarifa → cotización dentro de cobertura.
2. Solicitud de despacho en F-02 → resolución de zona → despacho registrado con zona asignada.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Los criterios `CA-01` a `CA-14` están implementados y cuentan con pruebas automatizadas exitosas.
- Los dos recorridos funcionales han sido verificados de extremo a extremo.
- La cotización y la resolución de zona devuelven resultados coherentes con la configuración vigente.
- F-02 obtiene la zona de cada despacho desde este servicio y no mantiene una lógica de cobertura propia.
- La interfaz muestra correctamente las zonas por distrito o código postal, los estados de carga y los errores.
- No se han incorporado alcances no especificados.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.
