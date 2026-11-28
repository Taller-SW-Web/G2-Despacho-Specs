# API Management del Gateway de Despacho

**Estado** · Propuesta para revisión del próximo hito, 22/11/2026.

El Gateway es la entrada pública acordada para las APIs de negocio de Despacho. Aplica políticas comunes antes de reenviar a Gestión de Despachos u Operación de Reparto y Flota. Seguridad y Usuarios (G7) autentica a las personas, gestiona el MFA y emite los tokens. Los servicios de Despacho conservan la responsabilidad de autorizar la operación de negocio y comprobar el acceso a cada recurso. Los [contratos vigentes](../README.md#mapa-de-documentación) definen la interfaz que consumen los equipos [cite: 1, 2].

## 1. Punto de partida

El estado siguiente se basa en la configuración y el código del repositorio. Los valores efectivos y la exposición de servicios en Render se comprueban antes de publicar el cambio [cite: 3, 4].

| Capacidad | Estado en el repositorio |
|---|---|
| Enrutamiento | El Gateway publica rutas de negocio bajo `/api/v1` y las dirige por capacidad. Las rutas `/internal/v1/**` se reservan para llamadas entre servicios. |
| Autenticación | El Gateway valida el JWT de las operaciones protegidas. Los permisos por operación y el acceso al recurso se comprueban en los microservicios. Ambos frontends admiten configurar un origen de G7 para la sesión y recurren al Gateway si no está configurado. |
| Límite de cotizaciones | Gestión cuenta en memoria por combinación de `sub` del JWT e IP, en ventanas fijas de un minuto. El valor por defecto es 60. El exceso produce el `429` contractual. |
| Validación y trazabilidad | El Gateway controla el tamaño de solicitud, limita los tiempos de conexión y respuesta y propaga `X-Correlation-Id`. Los servicios validan el contenido de negocio. La exposición HTTP de Actuator incluye `health` e `info`. |
| Red de despliegue | El perfil de Render incluye destinos `onrender.com` por defecto para Gestión y Operación. El aislamiento de red se verifica en el entorno de despliegue. |
| Mensajería interna | RabbitMQ está integrado entre Gestión y Operación, pero deshabilitado por configuración. AMQP no pasa por el Gateway ni expone una ruta `/api/v1`. El Gateway solo publica REST [cite: 11]. |

## 2. Políticas propuestas

### 2.1. Autenticación y permisos por operación

- Configurar `VITE_SEGURIDAD_URL` en los dos frontends para usar el origen acordado de G7 en login, OTP y gestión de sesión. `VITE_API_BASE_URL` sigue identificando al Gateway de negocio. Comprobar login, OTP, renovación, cierre y CORS desde ambas aplicaciones antes de retirar el proxy de autenticación del entorno publicado. La integración local puede seguir usando Seguridad temporal. En el Gateway, `SEGURIDAD_URL` sigue siendo necesario para el descubrimiento y la validación del JWT [cite: 1, 3, 5].
- Aplicar en el Gateway los requisitos vigentes de tipo de token, rol o *scope* por método y ruta, empezando por las operaciones de la matriz. Verificar firma, algoritmo configurado, emisor y vigencia, y validar la audiencia `api-despacho` para los tokens de servicio según el contrato. Conservar `401` para falta o invalidez de credencial y `403` para un permiso insuficiente cuando así lo especifica la operación.
- Mantener en Gestión y Operación los controles de autorización. Operación comprueba, por ejemplo, si el despacho pertenece a la jornada activa del repartidor identificado por `sub`. La ruta de campo conserva el requisito de perfil local activo y vinculado. Probar el Gateway con los tokens que ya usan los consumidores y verificar que los rechazos en el borde no se reenvíen [cite: 1, 2].

### 2.2. Límite de solicitudes

El Gateway aplicará **una cuota general por consumidor para todas las rutas públicas de negocio**. Las operaciones que requieran un control adicional tendrán también **una cuota específica**. Una petición debe tener cupo en todas las reglas que le correspondan. Así, por ejemplo, cotización y seguimiento consumen de la misma cuota general de Chatbot. Cotizaciones conserva además el límite que ya existe en Gestión, porque puede consultar a Productos y escribir una instantánea [cite: 4, 6, 7, 10].

| Regla | Qué agrupa | Configuración para validar |
|---|---|---|
| General | Todas las solicitudes públicas de negocio admitidas por el limitador para una misma identidad autenticada. La clave usa el emisor y el `sub` del JWT validado. | Ventana de un minuto. **600 solicitudes por minuto** como valor inicial propuesto para pruebas de capacidad. La cifra compartida se acuerda con los consumidores a partir del tráfico medido. |
| Específica de cotizaciones | Solo `POST /api/v1/cotizaciones`, con la combinación vigente de `sub` e IP confiable. | Ventana fija de un minuto. Usar **60 solicitudes por minuto** como valor por defecto de referencia y comprobar la cuota efectiva antes de trasladarla. |
| Otras cuotas específicas | Operaciones cuyo costo o patrón de tráfico justifique una cuota propia. | Seguimiento, consultas de reparto y comandos de Ventas quedan cubiertos por la regla general. Medirlos para decidir si necesitan una regla adicional. |

**Aplicación en Spring Cloud Gateway.** Autenticar y autorizar primero. Después de identificar la ruta, un `GlobalFilter` evalúa las cuotas aplicables antes de reenviar al microservicio. La comprobación y el registro del consumo deben ser atómicos. Una solicitud admitida consume una unidad de cada cuota aplicable. Una solicitud rechazada por cuota se registra en métricas y no consume otra cuota. El contador general se comparte entre rutas, por lo que su clave no incluye el identificador de ruta [cite: 7].

- **Almacenamiento.** Limitar y expirar los contadores. Una instancia aislada puede usar memoria local. Si varias réplicas deben aplicar una cuota común, utilizar un almacén compartido y comprobar que las solicitudes concurrentes respeten los límites [cite: 7].
- **Identidad e IP.** La cuota general se carga a la identidad autenticada aunque sus instancias salgan por IP distintas. La cuota específica de cotizaciones conserva el uso de IP. Obtenerla de la cadena de proxies de confianza. Confirmar el ingreso y la configuración antes de activar esa regla.
- **Respuesta.** Al agotar una cuota, devolver `429 Too Many Requests` antes de reenviar. Para cotizaciones se conserva `DESP_ERROR_LIMITE_COTIZACION` y el formato contractual. Para las demás operaciones se propone `DESP_ERROR_LIMITE_SOLICITUDES`, que debe quedar acordado y documentado antes de activar el nuevo rechazo público. Las métricas distinguen qué cuota se agotó. `Retry-After` se incorpora al contrato si el equipo acuerda publicarlo [cite: 1].
- **Cobertura.** Los controles de salud del Gateway y las solicitudes CORS de preflight quedan fuera de la cuota de negocio. G7 gestiona los límites de login y OTP. Los servicios proveedores controlan la capacidad de sus rutas privadas.
- **Migración.** Medir solicitudes admitidas, picos y ráfagas por consumidor antes de activar la cuota general en un entorno compartido. Para trasladar la cuota específica de cotizaciones al Gateway, verificar que el comportamiento coincide con el límite efectivo de Gestión. Desde el corte, una sola capa aplica esa cuota específica. Si aparecen rechazos no previstos, restaurar el límite de cotizaciones en Gestión y desactivar la política de rechazo en el Gateway hasta ajustar los parámetros.

### 2.3. Red privada y publicación de rutas

- Conservar el origen público del Gateway y las rutas contractuales `/api/v1/...`. El nombre del recurso público describe la operación y el Gateway resuelve el servicio de destino [cite: 1, 2].
- Configurar direcciones privadas en `GESTION_DESPACHOS_URL` y `OPERACION_REPARTO_URL` donde corresponda. Antes de restringir el acceso público directo, probar desde la red de Render los recorridos Gateway a servicio y Gestión a Operación. Revisar además los monitores y la verificación de despliegue que consultan la salud directamente. Verificar que los destinos internos queden inaccesibles desde Internet y que el Gateway siga respondiendo [cite: 3, 8, 9].
- Conservar las credenciales de servicio para las llamadas privadas. Configurar orígenes y credenciales en el entorno correspondiente. Las variables públicas `VITE_*` almacenan orígenes y configuración de cliente, y las credenciales privadas quedan en la configuración de servidor.

### 2.4. Catálogo de APIs y compatibilidad

Mantener un catálogo de método, ruta, consumidor, política, proveedor y prueba. La matriz siguiente sirve como punto de partida. Si se cambia una ruta pública, un permiso exigido, una cuota efectiva o una respuesta contractual, acordar el cambio con los consumidores y actualizar la definición canónica antes de activarlo. La propuesta usa los contratos de Despacho existentes [cite: 1, 2].

| Operación | Consumidor y control acordado | Proveedor | Límite para el hito | Verificación prevista |
|---|---|---|---|---|
| `POST /api/v1/cotizaciones` | Marketplace y Chatbot, token técnico con `cotizaciones:calcular` | Gestión | General y específica de cotizaciones | `401`, `403`, `200` y `429`. Confirmar que el exceso se rechace antes de llegar a Gestión. |
| `GET /api/v1/seguimientos/pedidos/{idPedido}` | Canales y Ventas, token técnico con `seguimientos:leer` | Gestión | General | Comprobar que consume de la misma cuota general que cotizaciones para un canal que tiene ambos permisos. |
| `POST /api/v1/despachos` | Ventas, token técnico con `despachos:crear` e `Idempotency-Key` según el contrato | Gestión | General | Comprobar autorización e idempotencia con el consumidor existente. |
| `GET /api/v1/distritos` | Frontend administrativo, token humano con `GESTOR_DESPACHO` | Gestión | General | Un gestor autorizado obtiene el listado y un usuario sin el rol recibe `403`. |
| `GET /api/v1/repartidor/despachos/{idDespacho}` | Frontend del repartidor, token humano y perfil local activo y vinculado. Operación verifica la propiedad del despacho | Operación | General | El repartidor consulta uno propio y obtiene `404` ante uno ajeno. |
| `POST /internal/v1/capacidad/reservas` | Gestión, credencial técnica conforme al contrato interno | Operación | Política a cargo del proveedor | La operación funciona en la red privada para el servicio autorizado y el Gateway público no la enruta. |

### 2.5. Mensajería interna fuera del Gateway

La futura activación de RabbitMQ no cambia las rutas públicas ni las políticas del Gateway. El protocolo AMQP se gestiona entre Gestión y Operación con credenciales del broker, independientes de los JWT y de `X-Despacho-Interno`. La cabecera compartida no constituye red privada: las rutas `/internal/v1/**` quedan fuera de ese filtro y dependen de su autenticación técnica.

Antes de habilitar el transporte, el despliegue debe garantizar broker disponible, TLS y permisos mínimos, topología declarada, migración V8 de Operación aplicada, observabilidad de colas y DLQ, política de retención y procedimiento de conciliación al volver a HTTP. Un `/actuator/health` saludable no acredita por sí solo la disponibilidad del broker ni el procesamiento de mensajes [cite: 11].

### 2.6. Monitoreo y evidencia

- Medir conteo, latencia y estados HTTP de las rutas públicas. Spring Cloud Gateway agrupa las métricas por ruta configurada. Para distinguir cotización y seguimiento, usar identificadores propios o etiquetas por método y patrón estable. Contar en la capa de seguridad los rechazos anteriores al enrutamiento. El limitador registra los `429` por tipo de regla, general o específica, sin incluir la identidad de cada consumidor en las etiquetas [cite: 3, 7].
- Consultar las métricas de Actuator por un acceso protegido. Agregar un recolector y un tablero compartido cuando el equipo necesite historial. Usar `X-Correlation-Id` en registros para seguir solicitudes. Las etiquetas de métricas usan patrones como `/api/v1/seguimientos/pedidos/{idPedido}`. Mantener fuera de las etiquetas y de los registros operativos los JWT, las credenciales, los cuerpos de solicitud y los identificadores de usuarios o pedidos.
- Incluir en la verificación un `400` por entrada inválida de la operación y un `413` por exceso del tamaño permitido. Comprobar que los rechazos mantengan el formato acordado y que los errores públicos omitan trazas internas [cite: 1, 3].

## 3. Orden de trabajo y criterios del hito

1. Acordar la matriz de operaciones y verificar con G7 la sesión directa desde ambas aplicaciones. Confirmar los tokens vigentes de Marketplace, Chatbot y Ventas como línea base.
2. Aplicar los permisos acordados y el límite general a las rutas públicas de negocio, con una regla específica para cotizaciones. Verificar ambos límites, la separación entre consumidores, el formato de los errores y que los rechazos no lleguen al microservicio. Registrar la prueba específica de cotizaciones bajo CA-09, T-04 y EV-04 de F-01 [cite: 6].
3. Mostrar en métricas el tráfico permitido y rechazado de al menos dos operaciones de negocio. Registrar para cada comprobación el entorno, la revisión y el resultado. Un recorrido con dobles acredita el comportamiento del Gateway en ese entorno. La integración con G7, Productos y los canales se acredita con pruebas de esos proveedores y consumidores.
4. Preparar la migración a red privada. Activarla tras verificar los consumidores, las llamadas entre servicios y los monitores. Actualizar [C4](./c4-contenedores.md) con la topología efectivamente desplegada.

Quedan por confirmar con los responsables de cada integración la cuota efectiva publicada, el origen de G7 y el CORS de ambas aplicaciones, la cadena de proxies de confianza y la disponibilidad de red privada en Render. Esta propuesta registra criterios y decisiones por revisar. Las comprobaciones quedan pendientes hasta realizar las pruebas correspondientes.

## 4. Presentación y demostración

1. **Arquitectura y responsabilidades.** Mostrar en el C4 el acceso a G7 para iniciar sesión y el Gateway como entrada a las APIs de negocio. Explicar qué permisos se verifican en el Gateway y qué controles de propiedad quedan en los microservicios.
2. **Catálogo y compatibilidad.** Usar cotización y seguimiento como ejemplos de operaciones con consumidores y permisos vigentes. Mostrar que conservan sus rutas y cómo se documenta el nuevo `429` antes de habilitarlo en el ambiente compartido.
3. **Demostración de seguridad y tasa.** En un entorno aislado, usar una cuota general de **5 por minuto** y una específica de **3 cotizaciones por minuto**. Preparar dos consumidores con permisos y datos que permitan respuestas `200`. Empezar con contadores vacíos y ejecutar las llamadas de Chatbot desde la misma IP de prueba y dentro de la misma ventana.
4. **Resultado y despliegue.** Mostrar `401`, `403` y métricas para ambas clases de `429`. Terminar con el estado de la red privada y las condiciones para publicar. Identificar cuáles comprobaciones ya se ejecutaron y en qué entorno.

| Paso de la demostración | Resultado esperado |
|---|---|
| Enviar una cotización sin JWT y luego con un JWT válido sin el permiso | `401` y `403`. Las solicitudes no llegan a Gestión. |
| Chatbot hace tres cotizaciones válidas y luego una cuarta | Las tres primeras reciben `200`. La cuarta devuelve `429` por la cuota específica. Se consumieron tres de las cinco solicitudes generales. |
| Chatbot hace dos consultas válidas de seguimiento y luego una tercera | Las primeras dos reciben `200` y completan la cuota general. La tercera devuelve `429` en una operación que solo usa la regla general. |
| Marketplace realiza una consulta válida de seguimiento | Recibe `200` porque su contador general es independiente. |
| Revisar métricas y correlación | Se pueden distinguir los rechazos de autorización y los excesos de cuota general y específica sin registrar credenciales. |

## 5. Referencias

1. [Contrato externo de Despacho](../integraciones/api-contract.md), convenciones comunes, cotización, seguimiento, F-02 y acceso humano con G7.
2. [Contrato de Gestión](../integraciones/api-contract-gestion-despachos.md) y [contrato de Operación](../integraciones/api-contract-operacion-reparto.md), rutas públicas y privadas y autorización por operación.
3. [Configuración base](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/main/api-gateway/src/main/resources/application.yaml), [perfil de Render](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/main/api-gateway/src/main/resources/application-render.yaml) y [control de acceso del Gateway](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/main/api-gateway/src/main/java/com/modulodespacho/api_gateway/seguridad/ConfiguracionSeguridad.java).
4. [Filtro vigente de cotizaciones en Gestión](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/main/servicio-gestion-despachos/src/main/java/com/modulodespacho/gestiondespachos/servicio_gestion_despachos/cotizacion/infrastructure/FiltroLimiteCotizaciones.java).
5. [Configuración de las aplicaciones web](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/main/README.md) y [contrato de acceso humano con G7](../integraciones/api-contract.md#86-acceso-humano-de-ambas-aplicaciones).
6. F-01. [CA-09](../especificaciones/ES-F01-06-CotizarEnvioConProductos/spec.md#ca-09-exceso-de-límite-de-solicitudes), [T-04](../especificaciones/ES-F01-06-CotizarEnvioConProductos/tasks.md#t-04-verificar-tasa-rendimiento-y-consumo-real) y [EV-04](../especificaciones/ES-F01-06-CotizarEnvioConProductos/evidence.md#ev-04-tasa-rendimiento-y-recorrido-real).
7. Spring Cloud Gateway. [Filtros globales y métricas](https://docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webflux/global-filters.html) y [RequestRateLimiter](https://docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webflux/gatewayfilter-factories/requestratelimiter-factory.html).
8. Render. [Red privada](https://render.com/docs/private-network) y [servicios privados](https://render.com/docs/private-services).
9. [Verificación de despliegue del backend](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/main/docs/despliegue.md).
10. [OWASP API4:2023 y políticas de consumo por operación](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).
11. [Contrato externo §3.6](../integraciones/api-contract.md#36-mensajería-interna-con-rabbitmq) y [backend `develop` `859c5c3`](https://github.com/Taller-SW-Web/G2-Despacho-Backend/tree/859c5c37abd6f9543c70d6c7f456b3d7d651435a). RabbitMQ está integrado; su activación y verificación están pendientes.
