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

- Administración de zonas de cobertura: registro, edición, consulta, activación y desactivación mediante distritos y códigos postales.
- Matriz de tarifas: una regla vigente por zona con tarifa base, peso incluido, recargo por kilogramo adicional, factor volumétrico, moneda y plazo estimado en días hábiles.
- Consulta de los datos físicos de cada producto ante Productos y Ofertas, en lote y con token propio, para calcular el peso y el volumen cotizables.
- Cotización de envíos para Marketplace y Chatbot, y para Ventas y Postventa cuando lo requiera, con costo en soles y plazo estimado.
- Validación de cobertura y resolución de zona para un destino, como servicio interno para F-02 y F-05.
- Registro de auditoría de los cambios en zonas y tarifas.

Quedan fuera de la cotización la resolución por geometría o por polígonos, la definición de rangos de peso por tramos y la promoción de envíos gratuitos, que son responsabilidades de otros ámbitos o decisiones pendientes.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- Las operaciones de configuración requieren un token JWT con rol `GESTOR_DESPACHO`.
- La cotización requiere un token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`; no requiere token de usuario humano.
- Una solicitud de cotización debe identificar el destino con `distrito`; `direccion` y `codigoPostal` son opcionales.
- `lineas` es opcional. Si se omite, la operación solo confirma cobertura y zona. Si se envía, debe contener al menos un elemento con `sku` y `cantidad` mayor que cero.
- Cada producto cotizable debe tener identificador, peso mayor a cero y dimensiones válidas en Productos y Ofertas.
- Solo se cotiza contra zonas en estado `ACTIVO`.
- Un distrito o código postal no puede pertenecer a más de una zona activa.
- Los límites de cotización por consumidor y el tiempo de caché de los datos físicos de productos son acuerdos pendientes de cierre en el contrato.

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

- Una zona válida se guarda con identificador único, nombre único, distritos o códigos postales y estado `ACTIVO`.
- Una regla tarifaria válida queda asociada a su zona como tarifa vigente y se aplica a las cotizaciones siguientes; la tarifa anterior se conserva como histórico.
- Una consulta de cobertura retorna la disponibilidad, la zona y los datos del destino, con o sin costo según incluya `lineas`.
- Una cotización válida retorna la cobertura, la zona, el peso y el volumen totales, el costo, la moneda, el plazo estimado en días hábiles y la fecha estimada de entrega.
- Una resolución de zona retorna el identificador de la zona que cubre el destino o indica que no existe cobertura.
- La desactivación de una zona no modifica los despachos ya registrados en ella.
- Toda creación, edición, activación o desactivación de zonas y toda alta o sustitución de tarifas queda registrada con usuario y marca temporal.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Configuración de zonas de cobertura

El sistema DEBE permitir registrar, editar, consultar, activar y desactivar zonas por distritos o códigos postales, y mantenerlas activas o inactivas según la operación.

#### CA-01. Creación exitosa de una zona de cobertura

- **DADO** que un usuario con rol `GESTOR_DESPACHO` ingresa el nombre de la zona ("Lima Centro"), los distritos comprendidos (Miraflores, San Isidro, Lince) y el estado "Activo".
- **CUANDO** confirma la creación.
- **ENTONCES** el backend valida que los distritos y códigos postales no pertenezcan a otra zona activa y registra la zona con identificador único, nombre único y estado `ACTIVO`.

#### CA-03. Rechazo de zona o cobertura duplicada

- **DADO** que se intenta registrar una zona cuyo nombre, distrito o código postal ya está registrado en una zona activa.
- **CUANDO** se confirma la creación.
- **ENTONCES** el sistema responde `409 Conflict`, detalla la duplicidad y no persiste la zona.

#### CA-04. Acceso sin permisos requeridos

- **DADO** que un usuario sin rol `GESTOR_DESPACHO` intenta registrar, editar, consultar o modificar zonas o tarifas.
- **CUANDO** realiza la petición.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone información de configuración.

#### CA-15. Consulta del catálogo de zonas

- **DADO** que existen zonas registradas en distintos estados y con tarifas distintas.
- **CUANDO** el Gestor abre el panel de zonas y aplica filtros por nombre, distrito y estado.
- **ENTONCES** el sistema devuelve una página con las zonas que coinciden, mostrando nombre, distritos, códigos postales, tarifa vigente o la indicación de que no existe, estado y última modificación.

#### CA-16. Edición de una zona existente

- **DADO** una zona existente con nombre, distritos y códigos postales que no colisionan con otra zona activa.
- **CUANDO** el Gestor edita su nombre o su cobertura y confirma.
- **ENTONCES** el sistema conserva el identificador de la zona, persiste los cambios con usuario y marca temporal, y la zona resuelve cobertura con su nueva delimitación.

#### CA-17. Activación de una zona y conflicto de solapamiento

- **DADO** que una zona está en `INACTIVO` y sus distritos y códigos postales no pertenecen a ninguna otra zona activa.
- **CUANDO** el Gestor la activa.
- **ENTONCES** el sistema la cambia a `ACTIVO` y vuelve a atender cotizaciones y resoluciones de zona para su cobertura.
- **DADO** que la zona por activar comparte un distrito o código postal con una zona `ACTIVO`.
- **CUANDO** el Gestor intenta activarla.
- **ENTONCES** el sistema responde `409 Conflict`, identifica la zona activa en conflicto y conserva el estado `INACTIVO`.

#### CA-13. Desactivación de una zona con despachos registrados

- **DADO** una zona con despachos registrados que aún no han sido entregados.
- **CUANDO** el Gestor la desactiva.
- **ENTONCES** la zona deja de aceptar nuevas cotizaciones y nuevas solicitudes, pero los despachos existentes conservan su zona y continúan su ciclo sin cambios, incluidas sus reprogramaciones.

### RF-02. Matriz tarifaria y reglas de cobro

El sistema DEBE permitir parametrizar una tarifa vigente por zona con tarifa base, peso incluido, recargo por kilogramo adicional, factor volumétrico, moneda y plazo estimado en días hábiles.

#### CA-05. Configuración de tarifa mixta por peso y zona

- **DADO** que se configura para "Lima Norte" una tarifa base de 10.00 PEN hasta 3 kg y un recargo de 2.00 PEN por kilogramo adicional.
- **CUANDO** se guarda la regla.
- **ENTONCES** el sistema la asocia a la zona como tarifa vigente y la aplica a las cotizaciones siguientes para esa zona.

#### CA-06. Rechazo de regla tarifaria inválida

- **DADO** una regla con tarifa base negativa, peso incluido no positivo, zona inexistente o en `INACTIVO`.
- **CUANDO** se intenta guardar.
- **ENTONCES** el sistema responde `400 Bad Request`, detalla los campos inválidos y no persiste la regla.

#### CA-18. Sustitución de la tarifa vigente e histórico

- **DADO** que una zona tiene una tarifa vigente y se guarda una nueva regla para ella.
- **CUANDO** el sistema confirma la operación.
- **ENTONCES** la nueva regla queda como única tarifa vigente de la zona, la anterior queda inactiva y se conserva como histórico, y las cotizaciones posteriores usan la nueva.

### RF-03. Cotización en tiempo real para canales de venta

El sistema DEBE evaluar la cobertura de un destino y, cuando la solicitud incluye líneas, calcular el costo de envío y el plazo estimado a partir de la tarifa vigente de la zona y de los datos físicos de los productos.

La operación atiende tres consultas según el cuerpo recibido:

| Cuerpo recibido | Resultado | `tipoCotizacion` |
|---|---|---|
| Solo `destino` | Cobertura, zona y datos del destino | — |
| `destino` y `lineas` | Cobertura y costo calculado con los datos físicos de los productos | `EXACTA` |
| Destino sin cobertura | Cobertura y datos del destino, sin costo ni plazo | — |

Reglas de cálculo y de integración:

- La cobertura se evalúa primero. Si el destino no tiene cobertura, el sistema responde sin consultar a Productos y Ofertas ni validar las líneas.
- Con `lineas`, el sistema agrupa los SKU repetidos, consulta a Productos y Ofertas en lote y calcula los totales; el canal no envía peso ni volumen.
- El sistema utiliza su propio token de servicio (`modulo-despacho`) y no reenvía a Productos el token recibido del canal.
- El cálculo de los totales por línea es el siguiente:

```text
volumenUnitarioM3 = (largoCm / 100) × (anchoCm / 100) × (altoCm / 100)
pesoLineaKg = pesoKg × cantidad
volumenLineaM3 = volumenUnitarioM3 × cantidad
pesoTotalKg = Σ pesoLineaKg
volumenTotalM3 = Σ volumenLineaM3
pesoCotizableKg = pesoTotalKg + (volumenTotalM3 × factorVolumetrico)
costoEnvio = tarifaBase + (recargoKgAdicional × max(0, pesoCotizableKg − pesoIncluidoKg))
```

- El sistema calcula el plazo estimado en días hábiles y la fecha estimada de entrega. Ventas y Postventa pueden conservar la fecha estimada como referencia, pero no debe enviarla al crear el despacho.
- La cotización no crea un pedido ni un despacho y no requiere `Idempotency-Key`, porque solo calcula y no modifica recursos.
- Las promociones, incluido el envío gratuito, y el importe finalmente cobrado al cliente pertenecen a Ventas y Postventa y no modifican el costo logístico calculado por el módulo.
- El límite de solicitudes se aplica por `sub` del token de servicio e IP.

#### CA-07. Cotización exitosa dentro de cobertura

- **DADO** una solicitud con destino en un distrito de "Lima Centro" y las líneas `POL-NEG-M` por 5 y `ZAP-RUN-42` por 1, cuyos datos físicos fueron obtenidos de Productos y Ofertas.
- **CUANDO** un canal de venta solicita la cotización.
- **ENTONCES** el sistema calcula 2.65 kg y 0.021 m³ totales, aplica la tarifa vigente de la zona (10.00 PEN hasta 3 kg, 2.00 PEN por kg adicional, factor volumétrico 1.25) y retorna `tipoCotizacion=EXACTA`, costo de 10.00 PEN, moneda `PEN` y un plazo estimado de 2 días hábiles.

#### CA-08. Cotización con línea o cantidad inválida

- **DADO** una solicitud con `lineas` vacías, o con una línea cuya `cantidad` es menor o igual a cero.
- **CUANDO** se envía la cotización.
- **ENTONCES** el sistema responde `400 Bad Request` con `DESP_ERROR_LINEAS_VACIAS` o `DESP_ERROR_CANTIDAD_INVALIDA` y no calcula el costo.

#### CA-09. Cotización con datos físicos inválidos

- **DADO** una solicitud que contiene un producto sin peso mayor a cero o sin dimensiones válidas.
- **CUANDO** se envía la cotización.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`, identifica el producto incompleto y no calcula una cotización hasta que Productos y Ofertas proporcione sus datos físicos.

#### CA-10. Cotización sin cobertura de entrega

- **DADO** una solicitud con destino fuera de todas las zonas activas.
- **CUANDO** se envía la cotización, con o sin `lineas`.
- **ENTONCES** el sistema responde `200 OK` con `coberturaDisponible: false`, `nombreZona: null`, sin costo ni plazo, y con el mensaje de destino fuera de cobertura.

#### CA-11. Cotización con token de servicio

- **DADO** que un canal obtuvo un token técnico con `cotizaciones:calcular`.
- **CUANDO** envía la solicitud con `Authorization: Bearer <token>`.
- **ENTONCES** el sistema procesa la cotización sin requerir una sesión de usuario humano.

#### CA-14. Límite de solicitudes de cotización

- **DADO** que un mismo origen supera el límite de solicitudes de cotización configurado.
- **CUANDO** envía una nueva solicitud.
- **ENTONCES** el sistema responde `429 Too Many Requests` con `DESP_ERROR_LIMITE_COTIZACION` y sin procesar el cálculo.

#### CA-19. Consulta de cobertura sin productos

- **DADO** una solicitud que incluye solo el destino y omite `lineas`.
- **CUANDO** un canal de venta la envía.
- **ENTONCES** el sistema responde `200 OK` con la disponibilidad de cobertura, el nombre de la zona y los datos del destino, sin costo, sin plazo y sin `tipoCotizacion`.

#### CA-20. Cotización sin distrito de destino

- **DADO** una solicitud que no informa `distrito` en el destino.
- **CUANDO** se envía la cotización.
- **ENTONCES** el sistema responde `400 Bad Request` con `DESP_ERROR_DESTINO_REQUERIDO` y no evalúa la cobertura.

#### CA-21. Cotización con producto inexistente

- **DADO** una solicitud que incluye un `sku` que Productos y Ofertas no reconoce.
- **CUANDO** se envía la cotización.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con `DESP_ERROR_PRODUCTO_NO_ENCONTRADO`, identifica el `sku` y no calcula el costo.

#### CA-22. Cotización con productos no disponible

- **DADO** que no es posible consultar los datos físicos de los productos en Productos y Ofertas.
- **CUANDO** se envía una cotización con `lineas`.
- **ENTONCES** el sistema responde `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE` y no devuelve costo.

#### CA-23. Cotización en zona activa sin tarifa vigente

- **DADO** una zona en `ACTIVO` que no tiene tarifa vigente y una solicitud de cotización con `lineas`.
- **CUANDO** se procesa la solicitud.
- **ENTONCES** el sistema confirma la cobertura y la zona, no devuelve costo ni plazo y no inventa una regla tarifaria; el tratamiento exacto de esta situación permanece como acuerdo pendiente en el contrato de integración.

### RF-04. Resolución de zona para el módulo

El sistema DEBE ofrecer al resto del módulo la resolución de la zona que cubre un destino, como fuente única de cobertura. F-02 la utiliza al crear un despacho y F-05 al asignar la zona de trabajo de un repartidor; el módulo no mantiene una lógica de cobertura propia.

#### CA-12. Resolución de zona para una solicitud de despacho

- **DADO** que F-02 recibe una solicitud de despacho con destino en San Isidro, perteneciente a "Lima Centro".
- **CUANDO** solicita la resolución de zona.
- **ENTONCES** el sistema retorna el identificador y el nombre de "Lima Centro", y F-02 los asocia al despacho.

#### CA-02. Resolución de zona para un destino fuera de cobertura

- **DADO** que se resuelve un destino cuyo distrito o código postal no pertenece a ninguna zona activa.
- **CUANDO** el sistema evalúa el destino.
- **ENTONCES** retorna `200 OK` con `coberturaDisponible: false`, sin zona y con el mensaje de destino fuera de cobertura.

## 6. Frontend

La funcionalidad tendrá una experiencia web responsive compuesta por:

| Elemento | Responsabilidad |
|---|---|
| Panel de Gestión de Zonas | Listado paginado de zonas con filtros por nombre, distrito y estado, indicación de tarifa vigente y acciones de activación o desactivación. |
| Formulario de Zona | Registro o edición del nombre, distritos y códigos postales. |
| Formulario de Tarifas | Configuración de tarifa base, peso incluido, recargo por kilogramo, factor volumétrico y plazo estimado. |
| Confirmación de desactivación | Advertir que la zona dejará de aceptar cotizaciones y solicitudes nuevas y que los despachos existentes conservan su zona. |
| Retroalimentación | Informar resultados, duplicidades, validaciones y errores de red. |

La interfaz debe impedir acciones conocidas como inválidas, pero las mismas reglas siempre deben volver a validarse en el backend. Las cuatro pantallas, sus estados y el tratamiento visual de alta fidelidad se encuentran en `disenio/funcionalidades/f-01.md` y `disenio/SystemDesign/f-01-alta-fidelidad.md`. La cotización no tiene interfaz propia: la consumen los canales mediante API.

## 7. Backend

| Componente lógico | Responsabilidad |
|---|---|
| Gestión de zonas | Registrar, editar, listar y consultar zonas con validación de distritos y códigos postales duplicados, y autorización. |
| Estado de zonas | Activar y desactivar zonas validando el solapamiento con otras zonas activas. |
| Servicio de matriz tarifaria | Administrar una tarifa vigente por zona y validar su consistencia. |
| Integración con Productos y Ofertas | Obtener en lote, con token propio, el identificador, peso y dimensiones de los productos cotizados. |
| Motor de cotización | Calcular cobertura, costo y plazo a partir del destino y los datos físicos de los productos. |
| Resolución de zona | Determinar la zona activa que contiene el distrito o código postal; servicio interno para F-02 y F-05. |
| Control de límite de solicitudes | Aplicar el límite configurado por `sub` del cliente técnico e IP. |
| Persistencia y auditoría | Almacenar zonas, tarifas y sus cambios con usuario y marca temporal. |

Las rutas, cuerpos, respuestas, códigos de error y la operación de Productos y Ofertas se centralizan en `integraciones/api-contract.md` y se publicarán mediante Swagger UI desde el backend desplegado. Las entidades y sus restricciones se encuentran en `arquitectura/modelo-datos.md`.

## 8. Requisitos no funcionales

- **Rendimiento:** la cotización y la resolución de zona deben responder en menos de 100 ms.
- **Aislamiento:** no se accede a bases de datos de otros módulos; los datos físicos se obtienen mediante el contrato acordado con Productos y Ofertas.
- **Seguridad:** la configuración requiere JWT con rol `GESTOR_DESPACHO`. La cotización requiere token de servicio con `cotizaciones:calcular` y no expone configuración interna.
- **Comunicación:** la cotización es la única integración con otros módulos que responde de forma síncrona, porque el canal la necesita para mostrar el costo al cliente.
- **Trazabilidad:** toda creación, edición, activación o desactivación de zonas y toda alta o sustitución de tarifas registra usuario y marca temporal en UTC. Las tarifas se conservan por sustitución de la regla vigente, no por actualización destructiva.
- **Tolerancia a fallos:** si Productos y Ofertas no responde, la cotización informa la indisponibilidad sin devolver un costo estimado.

## 9. Fuera de alcance

- **Cobro del envío:** corresponde al proceso de pago de los canales y a Ventas y Postventa.
- **Envío gratuito y promociones:** pertenecen a Ventas y Postventa y no modifican el costo logístico.
- **Geometría, polígonos y PostGIS:** no forman parte del alcance; la cobertura se define por distritos y códigos postales.
- **Rangos de peso por tramos:** la tarifa vigente se define con peso incluido y recargo por kilogramo adicional.
- **Registro de despachos:** corresponde a F-02.
- **Asignación de repartidores:** corresponde a F-02 con información de F-05.
- **Ejecución de la entrega:** corresponde a F-03.

Las posibles ampliaciones de esta funcionalidad están centralizadas en [Pendientes](./pendiente.md), sección F-01. No forman parte de los criterios de completitud actuales.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01, CA-03 y CA-16 | Registrar y editar zonas válidas, duplicadas y con delimitación colidida. | Integración y unitaria | Zona creada en `ACTIVO`, `409` para nombres, distritos o códigos duplicados y persistencia de la edición con su auditoría. |
| CA-04 | Invocar la configuración sin credenciales o con rol incorrecto. | Integración de seguridad | `403 Forbidden` sin datos de configuración. |
| CA-15 | Consultar el catálogo con filtros combinados, paginación y zona sin tarifa. | Integración | Página con las coincidencias y metadatos de paginación. |
| CA-13 y CA-17 | Desactivar y activar una zona con y sin despachos, incluida la reactivación con solapamiento. | Integración | Estado actualizado, `409` ante conflicto y despachos existentes sin cambios tras la desactivación. |
| CA-05, CA-06 y CA-18 | Guardar tarifas válidas e inválidas y sustituir la tarifa vigente. | Unitaria e integración | Regla asociada a la zona, `400` para reglas inconsistentes y una sola tarifa vigente con histórico. |
| CA-07 | Cotizar productos con datos físicos válidos y contrastar el costo con la fórmula de la tarifa. | Unitaria e integración | `tipoCotizacion=EXACTA`, peso, volumen, costo, moneda y plazo esperados. |
| CA-08, CA-09 y CA-21 | Cotizar con líneas vacías, cantidad inválida, `sku` desconocido y datos físicos incompletos. | Unitaria e integración | `400` y `422` con los códigos de error correspondientes. |
| CA-10 y CA-02 | Consultar cobertura dentro y fuera de rango, con y sin `lineas`. | Integración | `200 OK` con `coberturaDisponible` en `true` y `false` y sin costo cuando no hay cobertura. |
| CA-11 y CA-14 | Cotizar con token de servicio válido, sin token y excediendo el límite. | Integración de seguridad | Cotización procesada, `401` sin token y `429` al exceder el límite. |
| CA-19 y CA-20 | Consultar cobertura sin `lineas` y cotizar sin `distrito`. | Integración | Respuesta de cobertura sin costo y `400` con `DESP_ERROR_DESTINO_REQUERIDO`. |
| CA-22 | Cotizar con Productos y Ofertas no disponible. | Integración | `503` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE`. |
| CA-23 | Cotizar con `lineas` en una zona activa sin tarifa vigente. | Integración | Cobertura confirmada sin costo ni plazo y sin regla implícita. |
| CA-12 | Resolver zona para un destino cubierto y otro sin cobertura. | Integración | Zona asociada al despacho y ausencia de cobertura declarada. |

Además, se ejecutarán dos recorridos funcionales completos:

1. Registro de zona → asociación de tarifa → cotización dentro de cobertura.
2. Solicitud de despacho en F-02 → resolución de zona → despacho registrado con zona asignada.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Los criterios `CA-01` a `CA-23` están implementados y cuentan con pruebas automatizadas exitosas.
- Los dos recorridos funcionales han sido verificados de extremo a extremo.
- La cotización y la resolución de zona devuelven resultados coherentes con la configuración vigente.
- F-02 obtiene la zona de cada despacho desde este servicio y no mantiene una lógica de cobertura propia.
- La interfaz muestra correctamente las zonas por distrito o código postal, los estados de carga y los errores.
- No se han incorporado alcances no especificados.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.