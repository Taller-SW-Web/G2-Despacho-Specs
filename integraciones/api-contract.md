# Contrato de Comunicación del Módulo de Despacho

## 1. Propósito

Este documento define las comunicaciones del módulo de Despacho y Entrega con los canales, los demás módulos del Marketplace y sus dos microservicios internos. Se alinea con F-01 a F-05 y con los requisitos transversales de seguimiento, historial y eventos.

Este contrato establece:

1. Despacho es responsable de calcular la cotización.
2. Marketplace, Chatbot o Ventas envían destino y líneas con `sku` y `cantidad`; no calculan peso, volumen ni tarifa.
3. Para cotizar, Despacho consulta en lote a Productos y Ofertas los datos físicos vigentes de cada SKU.
4. La cotización se protege con un token de servicio y el scope `cotizaciones:calcular`. No requiere un JWT de usuario ni una API key adicional.
5. El seguimiento para canales se unifica por `idPedido`, exige un token de servicio con el scope `seguimientos:leer` y no expone coordenadas ni datos personales.
6. Ventas y Postventa solicita el despacho solamente después de que el pedido esté pagado, preparado y listo para entrega. La solicitud contiene las líneas del pedido (`sku` y `cantidad`); Despacho obtiene de Productos los datos físicos y calcula el peso y volumen operativos.
7. Cada `idPedido` puede originar como máximo un despacho.
8. Despacho no emite credenciales. Seguridad y Usuarios emite los JWT de usuario y los tokens de servicio OAuth 2.0 mediante `client_credentials`.
9. Gestión de Despachos es la única fuente del estado canónico del despacho.
10. Los cambios de estado se comunican a Ventas y Postventa de manera asíncrona e idempotente.
11. Para el alcance inicial, cada pedido representa un despacho y un paquete lógico; `cantidadPaquetes` se registra internamente con valor `1` y no forma parte de la solicitud de Ventas.

## 2. Límites y responsabilidades

| Participante | Es dueño de | Envía a Despacho | Recibe de Despacho |
|---|---|---|---|
| Marketplace | Experiencia del canal | Destino, SKU y cantidad; `idPedido` para seguimiento | Cobertura, cotización, plazo y estado resumido |
| Chatbot | Conversación con el cliente | Destino, SKU y cantidad; `idPedido` para seguimiento | Cobertura, cotización, plazo y estado resumido |
| Ventas y Postventa | Pedido, pago, preparación, anulaciones y tratamiento comercial | Pedido listo para entrega con destinatario, destino y líneas (`sku`, `cantidad`); cancelaciones | Identificador del despacho y eventos de estado |
| Productos y Ofertas | Catálogo, SKU, peso y dimensiones del producto | Datos físicos vigentes consultados por Despacho | Consulta de SKUs realizada por Despacho |
| Seguridad y Usuarios | Identidades, credenciales y roles globales | JWT de usuario, tokens de servicio, JWKS e identificadores de usuario | Ninguna credencial; el alta global la realiza `ADMIN_SISTEMA` y Despacho conserva únicamente el vínculo local con `usuario_id` |
| Gestión de Despachos | Zonas, tarifas, despacho, estado e historial | Comandos y estados confirmados para Operación | Disponibilidad, capacidad y transiciones solicitadas |
| Operación de Reparto y Flota | Repartidores, furgonetas, jornadas, capacidad y evidencias | Disponibilidad y comandos de transición de campo | Asignaciones y estados confirmados |

Despacho no administra pagos, stock, embalaje, cuentas de usuario, navegación GPS, guías de remisión, reembolsos ni notificaciones al cliente final. Una solicitud autenticada de Ventas declara que el pedido ya cumple las condiciones comerciales y de preparación; Despacho no consulta el estado interno del pedido ni modifica sus existencias.

## 3. Convenciones comunes

### 3.1. URL y formato

- Prefijo público: `/api/v1`.
- Prefijo entre microservicios: `/internal/v1`.
- Formato: `application/json; charset=UTF-8`.
- Campos JSON: `camelCase`.
- Enumeraciones: `UPPER_SNAKE_CASE`.
- Fechas y horas: ISO 8601 en UTC.
- Importes: número decimal y moneda ISO 4217.
- Identificadores: cadenas opacas; los clientes no deben inferir información desde ellas.

### 3.2. Encabezados

| Encabezado | Uso |
|---|---|
| `Authorization: Bearer <token>` | Operaciones con JWT de usuario o token de servicio |
| `Idempotency-Key: <uuid>` | Reintentos seguros en los comandos que lo declaren; es obligatorio como UUID v4 de hasta 128 caracteres al crear o cancelar despachos desde Ventas |
| `X-Correlation-Id: <uuid>` | Opcional; trazabilidad entre módulos. El Gateway lo genera si no llega |
| `Content-Type: application/json` | Cuerpos JSON |

La obtención de un token de servicio es la excepción al último encabezado: `POST /api/v1/auth/token` utiliza `Content-Type: application/x-www-form-urlencoded`, conforme al contrato de Seguridad y Usuarios.

### 3.3. Roles humanos y tokens de servicio

| Rol global | Uso |
|---|---|
| `GESTOR_DESPACHO` | Todas las operaciones administrativas: zonas, tarifas, programación, asignación, incidencias, repartidores, furgonetas y jornadas |

`REPARTIDOR` no forma parte del catálogo global de roles de Seguridad. Es un perfil local de Despacho enlazado al `sub` del usuario mediante el `usuario_id` almacenado por F-05. Las operaciones de campo se autorizan verificando que ese perfil exista, esté activo y sea propietario de la ruta o del recurso solicitado.

Los módulos externos no utilizan un rol humano `SERVICIO_INTEGRACION`. Seguridad emite tokens de servicio en los que:

- `sub` contiene el `client_id`, por ejemplo `modulo-chatbot` o `modulo-ventas`.
- `tipo` vale `servicio`.
- `scope` contiene los permisos concedidos al cliente.
- `aud` contiene las APIs dueñas de esos scopes, por ejemplo `api-despacho`.
- `iss` identifica al emisor de Seguridad.
- `iat`, `exp` y `jti` permiten validar emisión, vencimiento y unicidad del token.

Los tokens de usuarios humanos llevan `tipo=acceso`, un UUID de usuario en `sub` y sus roles en `roles`. Los tokens de refresco no se aceptan en las APIs de negocio.

El valor de `iss` se obtiene del campo `issuer` publicado por `GET /api/v1/auth/.well-known/openid-configuration`; no se fija manualmente porque cambia según el entorno. En el JWT de servicio, `scope` es un texto con valores separados por espacios y `aud` identifica las APIs destinatarias. El token de servicio dura una hora y no tiene token de refresco. Despacho exige `aud=api-despacho` en sus endpoints de integración. El contrato actual de Seguridad no garantiza `aud` en los tokens humanos de acceso, por lo que esa validación se aplica únicamente a los tokens de servicio.

### 3.4. Scopes de servicio de Despacho

| Scope | Consumidores previstos | Operación autorizada |
|---|---|---|
| `cotizaciones:calcular` | Marketplace y Chatbot | Calcular cobertura, costo y plazo |
| `seguimientos:leer` | Marketplace, Chatbot y Ventas | Consultar seguimiento por `idPedido` |
| `despachos:crear` | Ventas | Crear un despacho para un pedido pagado, preparado y listo para entrega |
| `despachos:cancelar` | Ventas | Solicitar cancelación por anulación del pedido |

Estos scopes pertenecen a la API de Despacho: Despacho define su significado y Seguridad los registra y concede a cada `client_id`. En cambio, `usuarios:leer` y `direcciones:leer` pertenecen a la API de Seguridad y ya están concedidos a `modulo-despacho`. Para consultar datos físicos, Productos y Ofertas acordó el scope `productos:fisicos:leer`, perteneciente a `api-productos`, que deberá concederse al cliente técnico `modulo-despacho`.

La integración con Ventas utiliza permisos distintos según la dirección de la llamada. `modulo-ventas` llama a `api-despacho` con `despachos:crear`, `despachos:cancelar` o `seguimientos:leer`. En la dirección contraria, `modulo-despacho` llama al webhook de `api-ventas` con `ventas:pedidos:estado`. No se utiliza el scope propuesto inicialmente `despachos:eventos:recibir`, porque Ventas confirmó la reutilización de `ventas:pedidos:estado`.

### 3.5. Errores

Las respuestas de error usan `Content-Type: application/problem+json`, siguiendo el mismo enfoque RFC 7807 adoptado por Seguridad y Usuarios. Los consumidores deben tomar decisiones por `status` y `code`, no comparando el texto de `detail`.

```json
{
  "type": "https://despacho.example.com/problemas/sin-cobertura",
  "title": "Destino sin cobertura",
  "status": 422,
  "code": "DESP_ERROR_SIN_COBERTURA",
  "detail": "El destino no pertenece a una zona de cobertura activa",
  "instance": "/api/v1/cotizaciones",
  "errores": [
    {
      "campo": "destino.distrito",
      "motivo": "Distrito no cubierto"
    }
  ],
  "correlationId": "35ac19fa-4b25-4a98-bbdd-882234ec1a2c",
  "timestamp": "2026-09-23T18:30:00Z"
}
```

| Código HTTP | Significado |
|---|---|
| `400 Bad Request` | Formato o validación básica inválida |
| `401 Unauthorized` | Token ausente, firma inválida, token vencido o claims de seguridad no aceptados; para tokens de servicio incluye `iss`, `aud` y `tipo` incorrectos |
| `403 Forbidden` | Token válido, pero sin el scope, rol o propiedad del recurso requerido |
| `404 Not Found` | Recurso inexistente |
| `409 Conflict` | Estado incompatible, duplicado o modificación concurrente |
| `422 Unprocessable Entity` | Solicitud válida, pero no procesable por una regla del negocio |
| `429 Too Many Requests` | Límite de cotizaciones excedido |
| `503 Service Unavailable` | Dependencia necesaria temporalmente no disponible |

Todos los endpoints protegidos aplican esta distinción antes de ejecutar la operación de negocio. Una respuesta `401` incluye el encabezado `WWW-Authenticate: Bearer` y no indica si el recurso solicitado existe. Una respuesta `403` tampoco expone datos del pedido, despacho, destinatario o repartidor.

Ejemplo de token no aceptado:

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/problem+json
WWW-Authenticate: Bearer
```

```json
{
  "type": "https://despacho.example.com/problemas/token-invalido",
  "title": "Token no aceptado",
  "status": 401,
  "code": "DESP_ERROR_TOKEN_INVALIDO",
  "detail": "No fue posible autenticar la solicitud",
  "instance": "/api/v1/seguimientos/pedidos/PED-2026-00891",
  "correlationId": "35ac19fa-4b25-4a98-bbdd-882234ec1a2c",
  "timestamp": "2026-09-23T18:30:00Z"
}
```

Ejemplo de token válido sin el scope exigido por la operación:

```http
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json
```

```json
{
  "type": "https://despacho.example.com/problemas/permiso-insuficiente",
  "title": "Permiso insuficiente",
  "status": 403,
  "code": "DESP_ERROR_SCOPE_INSUFICIENTE",
  "detail": "El cliente no tiene permiso para realizar esta operación",
  "instance": "/api/v1/seguimientos/pedidos/PED-2026-00891",
  "correlationId": "35ac19fa-4b25-4a98-bbdd-882234ec1a2c",
  "timestamp": "2026-09-23T18:30:00Z"
}
```

Para cerrar la integración se deben probar, como mínimo, los casos sin token, token inválido o vencido, audiencia incorrecta, scope ausente y scope correcto. Una audiencia que no contenga `api-despacho` se rechaza con `401 Unauthorized` antes de ejecutar la operación de negocio.

## 4. Matriz de comunicaciones externas

| Origen | Destino | Comunicación | Seguridad | Mecanismo |
|---|---|---|---|---|
| Marketplace o Chatbot | Despacho | Solicitar cotización | Token de servicio con `cotizaciones:calcular` | REST síncrono |
| Marketplace o Chatbot | Despacho | Consultar seguimiento por `idPedido` | Token de servicio con `seguimientos:leer` | REST síncrono |
| Despacho | Productos y Ofertas | Consultar datos físicos por SKU | Token de `modulo-despacho` con `aud=api-productos` y scope `productos:fisicos:leer` | REST síncrono en lote |
| Ventas y Postventa | Despacho | Crear despacho de pedido listo para entrega | Token de `modulo-ventas` con `aud=api-despacho` y scope `despachos:crear` | REST síncrono e idempotente |
| Ventas y Postventa | Despacho | Cancelar por anulación | Token de `modulo-ventas` con `aud=api-despacho` y scope `despachos:cancelar` | REST síncrono e idempotente |
| Despacho | Ventas y Postventa | Informar cambios de estado | Token de `modulo-despacho` con `aud=api-ventas` y scope `ventas:pedidos:estado` | Webhook con outbox y reintentos |
| Despacho | Seguridad y Usuarios | Obtener claves públicas | HTTPS | JWKS con caché |
| Seguridad y Usuarios | Despacho | Notificar cambios de estado o roles de usuarios | Credenciales y permisos del broker pendientes de publicación | Eventos RabbitMQ previstos por Seguridad |

## 5. F-01: cotización para Marketplace y Chatbot

### 5.1. Solicitar cotización

- **Método:** `POST`
- **Ruta:** `/api/v1/cotizaciones`
- **Autenticación:** token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`.
- **Identidad del consumidor:** claim `sub` del token, por ejemplo `modulo-chatbot`.
- **Límite:** configurable por `sub` e IP.
- **Idempotencia:** no requiere `Idempotency-Key`, porque solo calcula y no modifica recursos.

La misma operación atiende tres consultas según el cuerpo recibido:

| Cuerpo | Resultado | `tipoCotizacion` |
|---|---|---|
| Solo `destino` | Cobertura, zona y datos del destino | — |
| `destino` y `lineas` | Cobertura y costo calculado con los datos físicos de los productos | `EXACTA` |
| Destino sin cobertura | Solo cobertura y datos del destino, sin costo ni plazo | — |

Solicitud sin productos (solo cobertura):

```json
{
  "destino": {
    "direccion": "Av. Javier Prado Este 2465",
    "distrito": "San Borja",
    "codigoPostal": "15036"
  }
}
```

Solicitud con productos:

```json
{
  "destino": {
    "direccion": "Av. Javier Prado Este 2465",
    "distrito": "San Borja",
    "codigoPostal": "15036"
  },
  "lineas": [
    { "sku": "POL-NEG-M", "cantidad": 5 },
    { "sku": "ZAP-RUN-42", "cantidad": 1 }
  ]
}
```

Reglas:

- Debe informarse `distrito`; `direccion`, `codigoPostal` y los demás datos del destino son opcionales.
- `lineas` es opcional. Si se omite, la respuesta confirma únicamente la cobertura, la zona y los datos del destino, sin costo ni plazo. Si se envía, debe contener al menos un elemento.
- En cada línea, `sku` es obligatorio y `cantidad` debe ser mayor que cero.
- Despacho evalúa primero la cobertura. Si el destino no tiene cobertura, responde sin consultar a Productos ni validar las líneas.
- Con `lineas`, Despacho agrupa los SKU repetidos, consulta a Productos en lote y calcula el peso y volumen totales; el canal no envía esos totales.
- La cotización no crea un pedido ni un despacho.

Respuesta con cobertura, sin productos (`200 OK`):

```json
{
  "coberturaDisponible": true,
  "nombreZona": "Lima Centro",
  "distrito": "San Borja",
  "codigoPostal": "15036"
}
```

Respuesta con cobertura, con productos (`200 OK`):

```json
{
  "coberturaDisponible": true,
  "tipoCotizacion": "EXACTA",
  "nombreZona": "Lima Centro",
  "direccion": "Av. Javier Prado Este 2465",
  "distrito": "San Borja",
  "codigoPostal": "15036",
  "pesoTotalKg": 2.65,
  "volumenTotalM3": 0.021,
  "costoEnvio": 10.0,
  "moneda": "PEN",
  "plazoEstimadoDiasHabiles": 2,
  "fechaEstimadaEntrega": "2026-09-25",
  "cotizadoEn": "2026-09-23T18:30:00Z"
}
```

Respuesta sin cobertura (`200 OK`), con o sin productos:

```json
{
  "coberturaDisponible": false,
  "nombreZona": null,
  "distrito": "San Borja",
  "codigoPostal": "15036",
  "mensaje": "La dirección se encuentra fuera de nuestra zona de cobertura"
}
```

El costo, el plazo y la `fechaEstimadaEntrega` solo se devuelven con `tipoCotizacion=EXACTA`, es decir, cuando el cuerpo incluye `lineas`. Si se omite `lineas`, la respuesta confirma únicamente la cobertura, la zona y los datos del destino; los canales validan la cobertura en pantalla y, si no hay cobertura, se muestra el mensaje correspondiente sin costo ni plazo. Despacho calcula tanto el plazo como la fecha estimada de entrega. Los canales pueden comunicar `fechaEstimadaEntrega` al cliente y Ventas puede conservarla como referencia, pero no debe enviarla al crear el despacho. Las promociones, incluido el envío gratuito, y el importe finalmente cobrado al cliente pertenecen a Ventas y Postventa y no modifican el costo logístico calculado por Despacho.

Errores propios:

| Código | HTTP | Condición |
|---|---|---|
| `DESP_ERROR_DESTINO_REQUERIDO` | `400` | No se informó `distrito` |
| `DESP_ERROR_LINEAS_VACIAS` | `400` | Se envió `lineas` sin elementos |
| `DESP_ERROR_CANTIDAD_INVALIDA` | `400` | Cantidad menor o igual a cero |
| `DESP_ERROR_PRODUCTO_NO_ENCONTRADO` | `422` | Productos no reconoce un SKU |
| `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS` | `422` | Falta peso o dimensiones válidas |
| `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE` | `503` | No fue posible consultar Productos |
| `DESP_ERROR_LIMITE_COTIZACION` | `429` | El canal excedió su límite |


### 5.2. Integración de Despacho con Productos y Ofertas

Esta operación pertenece a Productos y Ofertas. Ambos equipos acordaron la ruta, las unidades y la autorización descritas a continuación.

- **Método:** `POST`
- **Ruta:** `/api/v1/productos/datos-fisicos/consulta`
- **Consumidor:** backend de Despacho, identificado por el `client_id` `modulo-despacho`.
- **Autenticación:** token de servicio con `aud=api-productos` y scope `productos:fisicos:leer`.
- **Unidades:** peso en kilogramos (`pesoKg`) y dimensiones en centímetros (`dimensionesCm`).

```json
{
  "skus": [
    "POL-NEG-M",
    "ZAP-RUN-42"
  ]
}
```

```json
{
  "productos": [
    {
      "sku": "POL-NEG-M",
      "estado": "ACTIVO",
      "pesoKg": 0.25,
      "dimensionesCm": {
        "largo": 30,
        "ancho": 25,
        "alto": 3
      },
      "actualizadoEn": "2026-09-22T14:00:00Z"
    },
    {
      "sku": "ZAP-RUN-42",
      "estado": "ACTIVO",
      "pesoKg": 1.4,
      "dimensionesCm": {
        "largo": 35,
        "ancho": 22,
        "alto": 13
      },
      "actualizadoEn": "2026-09-20T10:00:00Z"
    }
  ],
  "noEncontrados": []
}
```

Despacho calcula por cada línea:

```text
volumenUnitarioM3 = (largoCm / 100) × (anchoCm / 100) × (altoCm / 100)
pesoLineaKg = pesoKg × cantidad
volumenLineaM3 = volumenUnitarioM3 × cantidad
```

No se accede directamente a la base de datos de Productos. La consulta debe ser en lote para evitar una llamada por línea. Puede utilizarse una caché breve, pero los datos siguen siendo propiedad de Productos y Ofertas.

Despacho no reenvía a Productos el token recibido de Marketplace o Chatbot. Obtiene y utiliza su propio token de servicio, porque Productos autoriza a `modulo-despacho`, no al canal que inició la cotización.

## 6. RT-04: seguimiento para Marketplace y Chatbot

### 6.1. Consultar por identificador de pedido

- **Método:** `GET`
- **Ruta:** `/api/v1/seguimientos/pedidos/{idPedido}`
- **Autenticación:** token de servicio con `tipo=servicio` y scope `seguimientos:leer`.
- **Consumidores:** Marketplace, Chatbot y Ventas y Postventa.

```json
{
  "idPedido": "PED-2026-00891",
  "estado": "EN_CAMINO",
  "estadoEtiqueta": "En camino",
  "fechaProgramada": "2026-09-25",
  "distrito": "San Borja",
  "hitos": [
    {
      "estado": "PENDIENTE_ASIGNACION",
      "etiqueta": "En centro de despacho",
      "fecha": "2026-09-23T10:00:00Z"
    },
    {
      "estado": "ASIGNADO",
      "etiqueta": "Asignado a repartidor",
      "fecha": "2026-09-23T14:30:00Z"
    },
    {
      "estado": "EN_CAMINO",
      "etiqueta": "En camino",
      "fecha": "2026-09-23T16:00:00Z"
    }
  ],
  "actualizadoEn": "2026-09-23T16:00:00Z"
}
```

El campo `estado` utiliza el siguiente catálogo. `FALLIDO` representa un intento no completado y no debe interpretarse como el cierre definitivo del despacho.

| Estado | Significado para el consumidor | Final |
|---|---|---|
| `PENDIENTE_ASIGNACION` | El despacho fue creado y espera la asignación de un repartidor. | No |
| `ASIGNADO` | El despacho ya tiene repartidor, pero todavía no ha salido del centro. | No |
| `EN_CAMINO` | El repartidor recogió el paquete y comenzó el traslado al destinatario. | No |
| `FALLIDO` | La entrega no se completó o terminó la jornada sin realizarla; todavía puede reprogramarse. | No |
| `ENTREGADO` | La entrega fue confirmada correctamente. | Sí |
| `DEVUELTO_A_ORIGEN` | El paquete regresó al centro y la operación terminó sin entrega; no habrá otro intento. | Sí |
| `CANCELADO` | Ventas anuló el pedido antes de completar el despacho. | Sí |

Los estados finales son `ENTREGADO`, `DEVUELTO_A_ORIGEN` y `CANCELADO`; no admiten nuevas transiciones. Para consultar las transiciones, precondiciones y efectos completos, véase el [diagrama de estados del despacho](../arquitectura/diagrama-estados-despacho.md).

`estadoEtiqueta` y las etiquetas de los hitos proporcionan una descripción pública sin detalles operativos sensibles. Cada canal puede adaptar su redacción para la interfaz.

La respuesta nunca incluye:

- Coordenadas.
- Dirección completa o referencia.
- Teléfono, correo o nombre del destinatario.
- Identidad, teléfono o ubicación del repartidor.
- Motivo o comentario interno de un fallo.
- Evidencias fotográficas.

Un fallo reprogramado muestra hitos con etiquetas públicas como `No entregado, regresando al centro` y `Entrega reprogramada`, sin exponer el motivo operativo.

## 7. F-02: integración con Ventas y Postventa

### 7.1. Crear un despacho para un pedido listo para entrega

- **Método:** `POST`
- **Ruta:** `/api/v1/despachos`
- **Autenticación:** token de servicio con `tipo=servicio`, `sub=modulo-ventas`, `aud=api-despacho` y scope `despachos:crear`.
- **Idempotencia:** `Idempotency-Key` es obligatorio, debe ser un UUID v4 de hasta 128 caracteres y se combina con la unicidad de negocio por `idPedido`. Un reintento con la misma clave devuelve el resultado original sin crear otro despacho.

```json
{
  "idPedido": "PED-2026-00891",
  "destinatario": {
    "nombre": "Carlos Mendoza",
    "telefono": "+51987654321"
  },
  "destino": {
    "direccion": "Av. Javier Prado Este 2465",
    "referencia": "Frente al parque",
    "departamento": "Lima",
    "provincia": "Lima",
    "distrito": "San Borja",
    "codigoPostal": "15036",
    "coordenadas": {
      "latitud": -12.08945,
      "longitud": -77.00342
    }
  },
  "lineas": [
    {
      "sku": "POL-NEG-M",
      "cantidad": 5
    },
    {
      "sku": "ZAP-RUN-42",
      "cantidad": 1
    }
  ]
}
```

`lineas` es el arreglo de todos los productos incluidos en el pedido. Cada elemento identifica un producto por `sku` y expresa cuántas unidades contiene mediante `cantidad`. Las líneas no representan paquetes físicos: por ejemplo, cinco polos dentro de una misma bolsa se informan como una línea con cantidad `5` y el despacho continúa consumiendo un solo paquete lógico.

Las coordenadas y `codigoPostal` son opcionales. Debe enviarse al menos una línea, cada `sku` es obligatorio y cada `cantidad` debe ser mayor que cero.

La llamada autenticada con `sub=modulo-ventas` declara que el pedido está pagado, preparado y listo para entrega. Despacho no consulta el estado del pedido en Ventas: valida su propia cobertura y los datos recibidos y, si son correctos, crea inmediatamente el despacho en `PENDIENTE_ASIGNACION`. La creación no asigna todavía un repartidor ni incorpora el pedido a una ruta.

Antes de persistir el despacho, Despacho consulta en lote a Productos los datos físicos de las líneas y calcula `pesoTotalKg` y `volumenTotalM3` conforme a la sección 5.2. Esos valores se guardan para la asignación y el control de capacidad de la furgoneta. `cantidadPaquetes` no se recibe de Ventas: se registra internamente con valor `1`. Esta consulta obtiene únicamente datos físicos; Despacho no consulta, reserva ni modifica stock.

Despacho calcula `fechaProgramada` al crear el despacho a partir de la zona, el plazo aplicable y el calendario operativo.

Respuesta de creación, `201 Created`:

```json
{
  "idDespacho": "DSP-100234",
  "idPedido": "PED-2026-00891",
  "codigoRastreoInterno": "TRK-78901",
  "estado": "PENDIENTE_ASIGNACION",
  "idZona": "ZONA-LIMA-CENTRO",
  "fechaProgramada": "2026-09-25",
  "creadoEn": "2026-09-23T18:45:00Z"
}
```

Si el pedido ya tiene despacho, se responde `200 OK` con el recurso existente y no se crea otro. Si el destino no tiene cobertura, se responde `422` con `DESP_ERROR_SIN_COBERTURA`. Los SKU inexistentes o sin datos físicos responden con los errores definidos en la sección 5.1; si Productos no está disponible, se responde `503` y no se crea el despacho.

### 7.2. Cancelar por anulación del pedido

- **Método:** `POST`
- **Ruta:** `/api/v1/despachos/pedidos/{idPedido}/cancelacion`
- **Autenticación:** token de servicio con `tipo=servicio`, `sub=modulo-ventas`, `aud=api-despacho` y scope `despachos:cancelar`.
- **Idempotencia:** `Idempotency-Key` es obligatorio y debe ser un UUID v4 de hasta 128 caracteres. Una repetición con la misma clave conserva el resultado original y no duplica la transición, la auditoría ni el evento.

```json
{
  "motivo": "PEDIDO_ANULADO",
  "observacion": "Anulación confirmada por Ventas"
}
```

Comportamiento:

| Estado actual | Resultado |
|---|---|
| `PENDIENTE_ASIGNACION` | Cambia a `CANCELADO` |
| `ASIGNADO` | Cambia a `CANCELADO` y libera capacidad |
| `EN_CAMINO` | `409 Conflict`; no se cancela |
| `FALLIDO` | `202 Accepted`; registra la anulación y obliga al cierre en F-04 |
| `ENTREGADO`, `DEVUELTO_A_ORIGEN` o `CANCELADO` | `409 Conflict` o respuesta idempotente si ya estaba cancelado |

```json
{
  "idPedido": "PED-2026-00891",
  "idDespacho": "DSP-100234",
  "estado": "CANCELADO",
  "procesadoEn": "2026-09-23T19:00:00Z"
}
```

### 7.3. Eventos salientes hacia Ventas y Postventa

Despacho registra el evento en una bandeja de salida dentro de la misma transacción del cambio. La entrega inicial se realizará por webhook HTTPS. La URL pertenece a Ventas y debe configurarse mediante una variable segura.

- **Método:** `POST`
- **Ruta confirmada por Ventas:** `/api/v1/integraciones/despachos/eventos`
- **Autenticación:** token de servicio emitido por Seguridad con `tipo=servicio`, `sub=modulo-despacho`, `aud=api-ventas` y scope `ventas:pedidos:estado`.
- **Idempotencia:** Ventas deduplica por `idEvento`.

```json
{
  "idEvento": "EVT-8e191bab-6ec4-4fa4-b70e-d90e83bd48df",
  "tipo": "DESPACHO_EN_CAMINO",
  "idPedido": "PED-2026-00891",
  "idDespacho": "DSP-100234",
  "estadoAnterior": "ASIGNADO",
  "estadoNuevo": "EN_CAMINO",
  "ocurridoEn": "2026-09-23T19:20:00Z",
  "datos": {}
}
```

| Estado nuevo | Tipo de evento | Datos adicionales | Efecto acordado en Ventas |
|---|---|---|---|
| `ASIGNADO` | `DESPACHO_ASIGNADO` | `fechaProgramada` | Conserva `EN_PREPARACION`; registra el hito. |
| `EN_CAMINO` | `DESPACHO_EN_CAMINO` | Ninguno | Cambia `EN_PREPARACION` a `DESPACHADO`. |
| `ENTREGADO` | `DESPACHO_ENTREGADO` | `fechaEntrega`, `recibidoPor` opcional | Cambia `DESPACHADO` a `ENTREGADO`. |
| `FALLIDO` | `DESPACHO_FALLIDO` | `motivo`, `numeroIntento` | Conserva `DESPACHADO`; registra el intento para auditoría. |
| `PENDIENTE_ASIGNACION` reprogramado | `DESPACHO_REPROGRAMADO` | `nuevaFechaProgramada` | Conserva el estado comercial y actualiza la fecha estimada de entrega. |
| `DEVUELTO_A_ORIGEN` | `DESPACHO_DEVUELTO_A_ORIGEN` | `motivoCierre` | Cambia `DESPACHADO` a `ANULADO` y habilita el tratamiento comercial correspondiente. |
| `CANCELADO` | `DESPACHO_CANCELADO` | Ninguno | Confirma idempotentemente la cancelación solicitada; no reabre ni vuelve a modificar un pedido ya anulado. |

Los siete tipos anteriores son eventos logísticos aceptados por Ventas, no siete estados adicionales de su pedido. Ventas conserva su propia máquina de estados comercial y aplica el efecto indicado para cada evento.

La política de intentos pertenece a Despacho: el máximo inicial es `2`, puede configurarse dentro del módulo y no se recibe desde Ventas. `DESPACHO_FALLIDO` informa un intento no exitoso, pero no representa necesariamente un cierre definitivo. Solo `DESPACHO_DEVUELTO_A_ORIGEN` comunica que la operación logística terminó sin entrega y permite que Ventas y Postventa decida la anulación, devolución comercial o reembolso que corresponda.

Despacho no envía una `guiaRemision`, no solicita reembolsos y no informa importes a devolver. Esas responsabilidades permanecen fuera de este contrato.

Si Ventas no responde con `2xx`, Despacho realiza hasta cinco reintentos con espera creciente. El mismo `idEvento` se conserva. Tras agotarlos, el evento queda como `ENVIO_FALLIDO` y puede reenviarse manualmente. Los despachos simulados no generan eventos externos.

## 8. Integración con Seguridad y Usuarios

### 8.1. Validación local de tokens

Despacho valida los JWT localmente, sin consultar a Seguridad en cada solicitud:

1. Obtiene la configuración desde `GET /api/v1/auth/.well-known/openid-configuration`.
2. Obtiene las claves públicas desde `GET /api/v1/auth/.well-known/jwks.json` y las mantiene en caché.
3. Verifica firma, algoritmo permitido, vencimiento y emisor.
4. Para una persona gestora, exige `tipo=acceso` y el rol `GESTOR_DESPACHO`.
5. Para un repartidor, exige `tipo=acceso` y resuelve mediante `sub` un perfil local activo vinculado al usuario.
6. Para un módulo, exige `tipo=servicio`, que `aud` contenga `api-despacho` y el scope propio de la operación.

No se exige el rol ficticio `SERVICIO_INTEGRACION` ni un claim separado `clientId`: la identidad técnica ya está en `sub`. Tampoco se combina el token con una API key.

Ejemplo conceptual de token de usuario:

```json
{
  "sub": "2f31c1b1-7568-41b8-bf91-342db68431df",
  "tipo": "acceso",
  "roles": ["GESTOR_DESPACHO"],
  "iss": "https://seguridad.example.com/api/v1/auth",
  "iat": 1789273200,
  "exp": 1789276800,
  "jti": "7f22750a-8365-48da-93cf-6e063159ec60"
}
```

Ejemplo conceptual de token de servicio:

```json
{
  "sub": "modulo-chatbot",
  "tipo": "servicio",
  "scope": "cotizaciones:calcular seguimientos:leer",
  "aud": ["api-despacho"],
  "iss": "https://seguridad.example.com/api/v1/auth",
  "iat": 1789273200,
  "exp": 1789276800,
  "jti": "ad6b5dda-c481-4ad3-907a-04a56d392de7"
}
```

Los valores de `iss` mostrados son ilustrativos y no deben copiarse en la configuración. Cada despliegue obtiene el emisor real mediante el documento de descubrimiento de su propio entorno. Seguridad confirmó `scope` como texto separado por espacios dentro del JWT de servicio y `aud` como la lista de APIs dueñas de los scopes concedidos.

### 8.2. Obtención de un token de servicio

Antes de llamar a otro módulo, cada backend obtiene su propio token de Seguridad. Las credenciales de cliente se conservan exclusivamente en el servidor y nunca se exponen al navegador, aplicación móvil ni módulo receptor.

- **Método:** `POST`
- **Ruta de Seguridad:** `/api/v1/auth/token`
- **Content-Type:** `application/x-www-form-urlencoded`

```text
grant_type=client_credentials
client_id=modulo-chatbot
client_secret=<secreto-del-chatbot>
scope=cotizaciones:calcular seguimientos:leer
```

Respuesta esperada:

```json
{
  "accessToken": "<jwt-de-servicio>",
  "tokenType": "Bearer",
  "expiresIn": 3600,
  "scopes": [
    "cotizaciones:calcular",
    "seguimientos:leer"
  ]
}
```

El arreglo `scopes` pertenece a la respuesta HTTP de emisión. Dentro del JWT emitido, el claim `scope` contiene esos valores separados por espacios. El canal utiliza después `Authorization: Bearer <jwt-de-servicio>` al llamar a Despacho. Del mismo modo, `modulo-despacho` solicita otro token con sus propias credenciales y el scope aceptado por Productos; nunca reutiliza el token del canal.

### 8.3. Introspección de un usuario antes de una operación sensible

Seguridad ofrece `POST /api/v1/auth/introspeccion` para que un backend compruebe un token humano antes de una operación sensible. Esa ruta recibe el token humano en el cuerpo y se protege con el token de servicio del módulo que realiza la comprobación y el scope `tokens:introspeccion`.

Por ejemplo, si una persona administradora autoriza anular un pedido, Ventas valida o introspecciona el token de esa persona y luego llama a Despacho con el token técnico de `modulo-ventas` y `despachos:cancelar`. Despacho valida ese token de servicio localmente; no necesita introspeccionar el token técnico ni recibir el token humano de Ventas.

Seguridad todavía no ha concedido `tokens:introspeccion` a `modulo-despacho`; no se incluye como dependencia hasta que exista un caso de uso propio que lo requiera.

### 8.4. Creación y vinculación de un usuario repartidor

Seguridad confirmó que `REPARTIDOR` no será un rol global, que no incluirá un claim `idRepartidor` y que no expondrá un endpoint para crear cuentas de repartidores mediante el token de servicio de Despacho. Una persona con rol `ADMIN_SISTEMA` crea cada cuenta en Seguridad y Despacho mantiene el perfil operativo en su propia base de datos.

El flujo de vinculación esperado, pendiente de confirmación operativa por Seguridad, es el siguiente:

1. F-05 registra al repartidor local con `vinculacion=PENDIENTE`.
2. Un `ADMIN_SISTEMA` crea su cuenta en Seguridad mediante el procedimiento administrativo que ese módulo defina.
3. Despacho recibe el `usuario_id` generado por Seguridad y lo asocia al repartidor local.
4. Cuando llega un token humano, el backend utiliza su claim `sub` para localizar al repartidor vinculado.
5. El acceso a rutas y operaciones de campo depende del estado local del repartidor y de la propiedad del recurso.

Despacho almacena solamente el `usuario_id`, el vínculo y los estados operativos; nunca almacena ni transporta la contraseña definitiva. La entrega o activación de las credenciales pertenece a Seguridad. No se abre una jornada mientras el repartidor no esté vinculado y habilitado.

La baja lógica local impide nuevas jornadas, asignaciones y operaciones, pero no desactiva por sí sola la cuenta global. La desactivación o el bloqueo global corresponde a Seguridad. Todavía deben confirmar el canal administrativo para solicitar el alta o la baja global, cómo se comunicará el `usuario_id`, cómo se entregarán las credenciales iniciales y qué valor llevará `roles` en el token de una cuenta vinculada como repartidor.

### 8.5. Eventos de usuarios publicados por Seguridad

Despacho prevé consumir los eventos `usuario.desactivado`, `usuario.bloqueado`, `usuario.reactivado`, `usuario.desbloqueado` y `usuario.roles_cambiados` para mantener actualizado el acceso de los usuarios vinculados. Son notificaciones de cambios ya realizados por Seguridad, no comandos de Despacho ni scopes OAuth.

- `usuario.desactivado` y `usuario.bloqueado` impiden iniciar jornadas, recibir nuevas asignaciones o ejecutar operaciones.
- `usuario.reactivado` y `usuario.desbloqueado` actualizan el estado global, pero no revierten automáticamente una baja local.
- `usuario.roles_cambiados` actualiza oportunamente el acceso administrativo de quienes ejercen como `GESTOR_DESPACHO`.

Seguridad ha previsto publicar estos cambios mediante RabbitMQ, pero el contrato asíncrono todavía debe definir disponibilidad, exchange, routing keys, payloads, credenciales, permisos de consumo y política de reentrega. Hasta que ese contrato esté disponible, Despacho no asume que los eventos puedan consumirse en producción.

## 9. API administrativa de F-01 y F-02

### 9.1. Zonas y tarifas

| Método | Ruta | Roles | Propósito |
|---|---|---|---|
| `GET` | `/api/v1/zonas` | `GESTOR_DESPACHO` | Listar zonas |
| `POST` | `/api/v1/zonas` | `GESTOR_DESPACHO` | Crear zona |
| `GET` | `/api/v1/zonas/{idZona}` | `GESTOR_DESPACHO` | Consultar zona |
| `PUT` | `/api/v1/zonas/{idZona}` | `GESTOR_DESPACHO` | Editar zona |
| `PATCH` | `/api/v1/zonas/{idZona}/estado` | `GESTOR_DESPACHO` | Activar o desactivar |
| `GET` | `/api/v1/zonas/{idZona}/tarifa` | `GESTOR_DESPACHO` | Consultar tarifa vigente |
| `PUT` | `/api/v1/zonas/{idZona}/tarifa` | `GESTOR_DESPACHO` | Crear o reemplazar tarifa |

Ejemplo de tarifa:

```json
{
  "tarifaBase": 10,
  "pesoIncluidoKg": 3,
  "recargoKgAdicional": 2,
  "factorVolumetrico": 1.25,
  "moneda": "PEN",
  "plazoEstimadoDiasHabiles": 2
}
```

### 9.2. Programación y asignación

| Método | Ruta | Roles | Propósito |
|---|---|---|---|
| `POST` | `/api/v1/despachos/simulaciones` | `GESTOR_DESPACHO` | Crear un despacho de prueba |
| `GET` | `/api/v1/despachos/pendientes` | `GESTOR_DESPACHO` | Consultar cola paginada |
| `GET` | `/api/v1/despachos/{idDespacho}` | `GESTOR_DESPACHO` | Consultar detalle e historial |
| `POST` | `/api/v1/despachos/{idDespacho}/asignacion` | `GESTOR_DESPACHO` | Asignar a un repartidor |
| `POST` | `/api/v1/despachos/{idDespacho}/reasignacion` | `GESTOR_DESPACHO` | Cambiar repartidor antes del traslado |
| `PUT` | `/api/v1/jornadas/{idJornada}/secuencia` | `GESTOR_DESPACHO` | Reordenar despachos `ASIGNADO` |
| `GET` | `/api/v1/jornadas/{idJornada}/ruta` | `GESTOR_DESPACHO` | Consultar seguimiento operativo completo |

Asignación:

```json
{
  "idRepartidor": "REP-0012",
  "idJornada": "JOR-20260923-0012",
  "observacion": "Entrega prioritaria"
}
```

Reasignación:

```json
{
  "idNuevoRepartidor": "REP-0018",
  "idNuevaJornada": "JOR-20260923-0018",
  "motivo": "Falla de la furgoneta"
}
```

Secuencia:

```json
{
  "despachos": [
    {
      "idDespacho": "DSP-100234",
      "posicion": 1
    },
    {
      "idDespacho": "DSP-100240",
      "posicion": 2
    }
  ]
}
```

## 10. API de F-03: operación del repartidor

Todos los recursos requieren un JWT humano con `tipo=acceso`. El backend toma el `sub`, resuelve el perfil local de repartidor vinculado y comprueba que esté activo; el cliente no puede elegir otro `idRepartidor`. No se exige un rol global `REPARTIDOR` ni un claim `idRepartidor`.

| Método | Ruta | Propósito |
|---|---|---|
| `GET` | `/api/v1/repartidor/mi-ruta` | Consultar la ruta de la jornada actual |
| `GET` | `/api/v1/repartidor/despachos/{idDespacho}` | Consultar un despacho propio |
| `POST` | `/api/v1/repartidor/despachos/{idDespacho}/inicio-traslado` | Cambiar `ASIGNADO` a `EN_CAMINO` |
| `POST` | `/api/v1/repartidor/evidencias/autorizaciones` | Obtener URL firmada de carga |
| `POST` | `/api/v1/repartidor/despachos/{idDespacho}/entrega` | Registrar `ENTREGADO` |
| `POST` | `/api/v1/repartidor/despachos/{idDespacho}/fallo` | Registrar `FALLIDO` |
| `POST` | `/api/v1/repartidor/jornada/cierre` | Cerrar la jornada |
| `GET` | `/api/v1/repartidor/jornada/resumen` | Consultar el resumen propio |
| `GET` | `/api/v1/catalogos/motivos-fallo` | Consultar catálogo y selección permitida según §10.4 |
| `POST` | `/api/v1/evidencias/{idEvidencia}/acceso` | Obtener URL firmada de lectura |

Los comandos de transición deben ser idempotentes. Se recomienda enviar `Idempotency-Key`; su obligatoriedad como encabezado común aún debe acordarse.

### 10.1. Autorizar la carga de evidencia

```json
{
  "idDespacho": "DSP-100234",
  "tipo": "ENTREGA",
  "contentType": "image/jpeg",
  "tamanioBytes": 845120
}
```

```json
{
  "idEvidencia": "EVI-92812",
  "urlCarga": "https://storage.example/signed-upload",
  "venceEn": "2026-09-23T19:25:00Z"
}
```

La fotografía se carga directamente al bucket privado. La API recibe después solamente `idEvidencia`; no recibe imágenes Base64.

### 10.2. Registrar entrega

```json
{
  "idEvidencia": "EVI-92812",
  "recibidoPor": "Ana Mendoza"
}
```

No se captura firma ni geolocalización.

### 10.3. Registrar fallo

```json
{
  "motivo": "CLIENTE_AUSENTE",
  "comentario": "No respondieron al teléfono",
  "idEvidencia": "EVI-92813"
}
```

Motivos permitidos para el repartidor:

- `CLIENTE_AUSENTE`.
- `DIRECCION_NO_UBICADA`.
- `RECHAZO_DEL_PAQUETE`.
- `DATOS_DE_CONTACTO_ERRONEOS`.
- `ZONA_INACCESIBLE`.
- `PAQUETE_DANADO`.

`NO_INTENTADO` es exclusivo del cierre manual o automático de jornada.

### 10.4. Catálogo único de motivos de fallo

- **Método y ruta:** `GET /api/v1/catalogos/motivos-fallo`.
- **Autorización:** JWT humano válido y rol `GESTOR_DESPACHO`, o perfil local de repartidor activo vinculado al `sub`. Consultar el catálogo no exige una jornada abierta.
- **Respuesta `200 OK`:** objeto con `motivos`, arreglo de objetos con `codigo`, `etiqueta`, `seleccionableEnCampo`, `consumeIntento` y `activo`. Los tres últimos campos son booleanos obligatorios. Orden por `codigo` ascendente. No recibe filtros ni paginación.
- Devuelve el catálogo completo, incluidos motivos inactivos conservados para consultas históricas. F-03 ofrece para registrar únicamente los que tengan `activo=true` y `seleccionableEnCampo=true`; F-04 admite todos los códigos como filtro. La validación del backend aplica la misma restricción al registrar un fallo.
- `NO_INTENTADO` tiene `seleccionableEnCampo=false` y `consumeIntento=false`; lo genera exclusivamente el cierre de jornada. No se mantiene un segundo catálogo para F-04.
- Token no aceptado: `401`; usuario sin autorización: `403`, conforme a §3.5. Una caída al consultar el catálogo muestra un error y permite reintentar; el frontend no fabrica motivos.

Ejemplo de un elemento de `motivos`:

```json
{
  "codigo": "NO_INTENTADO",
  "etiqueta": "No intentado por fin de jornada",
  "seleccionableEnCampo": false,
  "consumeIntento": false,
  "activo": true
}
```

## 11. API de F-04: entregas fallidas

Todos los recursos requieren JWT con rol `GESTOR_DESPACHO`.

| Método | Ruta | Propósito |
|---|---|---|
| `GET` | `/api/v1/despachos/fallidos` | Listar fallidos con filtros y paginación |
| `GET` | `/api/v1/despachos/{idDespacho}/incidencia` | Consultar detalle, intentos, recepción e historial |
| `POST` | `/api/v1/despachos/{idDespacho}/recepcion-centro` | Confirmar el retorno físico |
| `POST` | `/api/v1/despachos/{idDespacho}/reprogramacion` | Reprogramar un nuevo intento |
| `POST` | `/api/v1/despachos/{idDespacho}/devolucion-origen` | Cerrar como `DEVUELTO_A_ORIGEN` |

### 11.1. Consultar entregas fallidas — ES-F04-01

`GET /api/v1/despachos/fallidos` es una consulta de solo lectura y no requiere `Idempotency-Key`. Devuelve únicamente despachos cuyo estado actual es `FALLIDO`, sin limitar las fechas al abrir la pantalla. No es una consulta del historial completo.

Se devuelve una fila por despacho. `idIncidencia` identifica el registro de `intentos_entrega` enlazado por `despachos.ultima_incidencia_id`, correspondiente a su última transición aceptada a `FALLIDO`, incluso si fue `NO_INTENTADO`. Motivo, fecha, repartidor, jornada, recepción e indicador de evidencia proceden de ese mismo registro. El contador acumulado y el máximo configurado son datos distintos de la identidad de la incidencia. No se selecciona una incidencia por el contador ni se reutiliza la recepción de una anterior.

#### Parámetros de consulta

| Parámetro | Tipo y valor por defecto | Regla |
|---|---|---|
| `pagina` | Entero; `1` | Mínimo `1`. |
| `tamanoPagina` | Entero; `20` | De `1` a `100`. |
| `motivo` | Código del catálogo; omitido | Un único código exacto de §10.4, incluido `NO_INTENTADO` o un motivo inactivo. Omitir no restringe el motivo. |
| `fechaDesde` | Fecha `YYYY-MM-DD`; omitida | Inicio inclusivo del día en `America/Lima`, aplicado a la incidencia vigente. |
| `fechaHasta` | Fecha `YYYY-MM-DD`; omitida | Incluye todo el día en `America/Lima`; internamente se excluye el inicio del día siguiente. |
| `recepcion` | Enum; `TODOS` | `TODOS`, `PENDIENTE_RETORNO` o `RECIBIDO_EN_CENTRO`. |
| `soloRetornosAtrasados` | Booleano; `false` | `true` exige recepción pendiente y jornada confirmada como cerrada. Puede combinarse con recepción omitida, `TODOS` o `PENDIENTE_RETORNO`. |

Los límites de fecha son independientes: puede enviarse solo uno o ninguno. Si se envían ambos, `fechaDesde` no puede superar `fechaHasta`. Una fecha futura válida puede producir cero coincidencias. Los instantes de respuesta se expresan en UTC; esta regla de fechas civiles especifica cómo aplicar el filtro de días.

Parámetros desconocidos, repetidos, vacíos, formatos incorrectos, códigos/enum no admitidos, enteros fuera de rango o `soloRetornosAtrasados=true` junto con `recepcion=RECIBIDO_EN_CENTRO` responden `400` con `code=DESP_ERROR_FILTROS_INVALIDOS` y `errores` por campo según §3.5. Los booleanos aceptan solo `true` o `false`. No se admite orden libre: el orden contractual es fijo.

#### Orden, paginación e indicadores

1. Construir una base con un registro vigente por despacho `FALLIDO` y aplicar motivo y fechas.
2. Calcular los indicadores sobre toda esa base, sin aplicar recepción, `soloRetornosAtrasados` ni paginación.
3. Aplicar recepción y retorno atrasado a las filas; calcular `totalElementos` con esos filtros.
4. Ordenar primero `RECIBIDO_EN_CENTRO` y luego `PENDIENTE_RETORNO`; dentro de cada grupo, `fechaIncidencia` ascendente y, como desempate estable, `idDespacho` ascendente. Este orden también se conserva al filtrar.
5. Paginar el resultado. Una página posterior a la última devuelve `contenido=[]` conservando los totales y la página solicitada; si no hay coincidencias, `totalPaginas=0`.

| Indicador | Significado |
|---|---|
| `pendientesRetorno` | Cantidad de filas de la base sin recepción confirmada. |
| `recibidosCentro` | Cantidad de filas de la base con recepción confirmada. |
| `retornosAtrasados` | Subconjunto de pendientes cuya jornada de esa incidencia está confirmada como cerrada. Es `null` si alguna jornada pendiente de la base no puede confirmarse. |
| `retornosSinJornadaConfirmada` | Número de pendientes de la base cuya jornada no pudo confirmarse; `0` con información completa. |

Los dos primeros indicadores particionan la base; los atrasados ya están incluidos en pendientes y no se suman como un tercer grupo. Pulsar una tarjeta cambia el filtro de las filas y reinicia la página, conservando las cifras de las otras tarjetas mientras no cambien motivo o fechas. Los totales se calculan antes de paginar; el frontend no los deduce de las filas visibles.

#### Respuesta `200 OK`

```json
{
  "contenido": [
    {
      "idDespacho": "DSP-100234",
      "idIncidencia": "INC-0021",
      "versionDespacho": 8,
      "codigoRastreoInterno": "TRK-78901",
      "fechaIncidencia": "2026-10-14T23:00:00Z",
      "motivo": {
        "codigo": "NO_INTENTADO",
        "etiqueta": "No intentado por fin de jornada"
      },
      "numeroIntentos": 1,
      "maximoIntentos": 2,
      "consumeIntento": false,
      "repartidor": {
        "idRepartidor": "REP-0012",
        "nombre": "Juan Pérez"
      },
      "recepcion": "PENDIENTE_RETORNO",
      "jornada": {
        "idJornada": "JOR-20261014-0012",
        "estado": "CERRADA",
        "cerradaEn": "2026-10-14T23:00:00Z",
        "consultadaEn": "2026-10-15T14:30:00Z"
      },
      "retornoAtrasado": true,
      "tieneEvidencia": false,
      "pedidoAnulado": false
    }
  ],
  "pagina": 1,
  "tamanoPagina": 20,
  "totalElementos": 1,
  "totalPaginas": 1,
  "indicadores": {
    "pendientesRetorno": 1,
    "recibidosCentro": 0,
    "retornosAtrasados": 1,
    "retornosSinJornadaConfirmada": 0
  },
  "consultadoEn": "2026-10-15T14:30:01Z"
}
```

Todos los campos del ejemplo son obligatorios. Identificadores y textos son cadenas; versión, contadores y metadatos son enteros; los indicadores de evidencia/anulación y `consumeIntento` son booleanos. `recepcion` usa los dos valores operativos de la tabla de filtros. `motivo` conserva el código y etiqueta del catálogo aun si está inactivo. `numeroIntentos` es el acumulado del despacho y no se pone a cero por `NO_INTENTADO`; el ejemplo representa un fallo anterior seguido de una salida no intentada. La UI titula la columna `Intentos consumidos`, presenta `1 de 2` y añade `No intentado en esta salida`.

`jornada.estado` es `ACTIVA`, `CERRADA` o `DESCONOCIDA`. `cerradaEn` solo tiene valor con cierre confirmado; `consultadaEn` es la marca UTC de la respuesta de Operación o `null` si no se obtuvo. `repartidor.nombre` puede ser `null` si ese dato no se recuperó: se conserva su identificador y se muestra `Nombre del repartidor no disponible`. Las referencias de repartidor/jornada pertenecen a la incidencia vigente, no a la jornada actual del repartidor.

La respuesta no contiene fotografía, URL firmada, comentario del repartidor, condición del sello, teléfono ni dirección del destinatario. Son datos del detalle autorizado. La selección de incidencias, los contadores locales y las filas proceden de una misma lectura consistente de Gestión; un cambio concurrente se observa al volver a consultar. `consultadoEn` identifica la elaboración de la respuesta, sin prometer una transacción compartida con Operación.

#### Jornada desconocida y degradación de la consulta

Gestión consulta los datos operativos mediante §13.5. No interpreta una ausencia de información como jornada activa ni infiere cierre por medianoche o por el reloj del navegador.

- Con recepción confirmada, `retornoAtrasado=false` aunque no se pueda consultar la jornada.
- Con recepción pendiente y jornada `ACTIVA`, vale `false`; con jornada `CERRADA`, vale `true`; con jornada `DESCONOCIDA`, vale `null` y la fila muestra `No se pudo confirmar el cierre de jornada`.
- La consulta normal conserva `200`, las filas y los indicadores locales exactos aunque Operación falle. Si existe alguna jornada pendiente desconocida en la base, `indicadores.retornosAtrasados=null`: se muestra `No disponible`, nunca cero ni una cifra parcial. La tarjeta de atrasados permanece visible y deshabilitada; las otras dos siguen disponibles. Se informa `retornosSinJornadaConfirmada` y se ofrece reintentar la consulta.
- Si se pidió `soloRetornosAtrasados=true` y falta confirmar alguna jornada pendiente de la base, se responde `503` con `code=DESP_ERROR_JORNADAS_NO_DISPONIBLES`; no se devuelve una página parcial ni un total inventado. Si la base no tiene pendientes, el filtro devuelve cero coincidencias sin necesitar esa dependencia.
- `401` y `403` se aplican antes de consultar y nunca devuelven filas ni indicadores. Los filtros válidos sin coincidencias responden `200` con contenido vacío; los fallos no se presentan como un estado vacío.

### 11.2. Comandos de recepción, reprogramación y cierre

Confirmación de recepción:

```json
{
  "selloIntacto": true,
  "observacion": "Paquete recibido sin daño visible"
}
```

La recepción no cambia el estado `FALLIDO`, pero libera la capacidad de la furgoneta y habilita la reprogramación o el cierre.

Reprogramación:

```json
{
  "nuevaFechaProgramada": "2026-09-26",
  "observacion": "Cliente confirmó disponibilidad"
}
```

Cierre:

```json
{
  "motivo": "MAXIMO_INTENTOS_ALCANZADO",
  "observacion": "Paquete queda a disposición de Ventas"
}
```

## 12. API de F-05: flota y capacidad

### 12.1. Repartidores y furgonetas

| Método | Ruta | Roles | Propósito |
|---|---|---|---|
| `GET` | `/api/v1/repartidores` | `GESTOR_DESPACHO` | Listar repartidores |
| `POST` | `/api/v1/repartidores` | `GESTOR_DESPACHO` | Registrar perfil local pendiente de vinculación |
| `GET` | `/api/v1/repartidores/{idRepartidor}` | `GESTOR_DESPACHO` | Consultar detalle |
| `PUT` | `/api/v1/repartidores/{idRepartidor}` | `GESTOR_DESPACHO` | Editar |
| `PATCH` | `/api/v1/repartidores/{idRepartidor}/estado` | `GESTOR_DESPACHO` | Alta o baja lógica |
| `PUT` | `/api/v1/repartidores/{idRepartidor}/vinculacion` | `GESTOR_DESPACHO` | Asociar el `usuario_id` creado previamente en Seguridad |
| `GET` | `/api/v1/furgonetas` | `GESTOR_DESPACHO` | Listar furgonetas |
| `POST` | `/api/v1/furgonetas` | `GESTOR_DESPACHO` | Registrar furgoneta |
| `PUT` | `/api/v1/furgonetas/{idFurgoneta}` | `GESTOR_DESPACHO` | Editar límites |
| `PATCH` | `/api/v1/furgonetas/{idFurgoneta}/estado` | `GESTOR_DESPACHO` | Cambiar disponibilidad o mantenimiento |

La vinculación recibe el identificador de la cuenta global y no crea ni modifica credenciales:

```json
{
  "usuarioId": "2f31c1b1-7568-41b8-bf91-342db68431df"
}
```

Furgoneta:

```json
{
  "placa": "ABC-123",
  "capacidadPesoKg": 500,
  "capacidadVolumenM3": 4,
  "maximoPaquetes": 80
}
```

### 12.2. Jornadas y monitoreo

| Método | Ruta | Roles | Propósito |
|---|---|---|---|
| `POST` | `/api/v1/jornadas` | `GESTOR_DESPACHO` | Abrir jornada repartidor-furgoneta-zona |
| `POST` | `/api/v1/jornadas/{idJornada}/cierre` | `GESTOR_DESPACHO` | Cerrar jornada sin despachos en curso |
| `GET` | `/api/v1/flota/monitoreo` | `GESTOR_DESPACHO` | Consultar ocupación y estados |
| `GET` | `/api/v1/repartidores/disponibles` | `GESTOR_DESPACHO` | Consultar capacidad remanente |

Apertura de jornada:

```json
{
  "idRepartidor": "REP-0012",
  "idFurgoneta": "FUR-0045",
  "idZona": "ZONA-LIMA-CENTRO",
  "fecha": "2026-09-23"
}
```

Disponibilidad:

```json
{
  "repartidores": [
    {
      "idRepartidor": "REP-0012",
      "idJornada": "JOR-20260923-0012",
      "nombre": "Juan Pérez",
      "idZona": "ZONA-LIMA-CENTRO",
      "estadoOperativo": "DISPONIBLE",
      "capacidadRemanente": {
        "pesoKg": 320,
        "volumenM3": 2.7,
        "paquetes": 52
      }
    }
  ]
}
```

## 13. Comunicación entre los microservicios de Despacho

Estas rutas son internas, requieren credencial de servicio y no se publican mediante el Gateway.

### 13.1. Gestión consulta y reserva capacidad en Operación

- **Método:** `POST`
- **Ruta:** `/internal/v1/capacidad/reservas`
- **Idempotencia:** `idDespacho`.

```json
{
  "idDespacho": "DSP-100234",
  "idRepartidor": "REP-0012",
  "idJornada": "JOR-20260923-0012",
  "requerido": {
    "pesoKg": 2.65,
    "volumenM3": 0.021,
    "paquetes": 1
  }
}
```

```json
{
  "idReserva": "RES-28719",
  "estado": "CONFIRMADA",
  "capacidadRemanente": {
    "pesoKg": 317.35,
    "volumenM3": 2.679,
    "paquetes": 51
  }
}
```

Una capacidad insuficiente responde `422` con `DESP_ERROR_CAPACIDAD_EXCEDIDA`. La cancelación, reasignación, entrega o recepción de un paquete fallido debe liberar o actualizar la reserva de manera idempotente.

### 13.2. Gestión libera una reserva en Operación

- **Método:** `POST`
- **Ruta:** `/internal/v1/capacidad/reservas/{idReserva}/liberacion`
- **Idempotencia:** `idReserva`; repetir la liberación devuelve el resultado vigente.

```json
{
  "motivo": "RECEPCION_EN_CENTRO",
  "idDespacho": "DSP-100234"
}
```

Los motivos iniciales son `ENTREGA`, `CANCELACION`, `RECEPCION_EN_CENTRO`, `REASIGNACION` y `COMPENSACION`. Un despacho `FALLIDO` no libera capacidad hasta que F-04 confirma su recepción física.

### 13.3. Operación solicita una transición a Gestión

- **Método:** `POST`
- **Ruta:** `/internal/v1/despachos/{idDespacho}/transiciones`
- **Consumidor:** Operación de Reparto y Flota.
- **Idempotencia:** clave de operación obligatoria; puede transportarse en `Idempotency-Key` cuando se apruebe la convención común.

```json
{
  "estadoDestino": "ENTREGADO",
  "idRepartidor": "REP-0012",
  "idJornada": "JOR-20260923-0012",
  "idEvidencia": "EVI-92812",
  "recibidoPor": "Ana Mendoza"
}
```

Gestión valida la máquina de estados, modifica el estado, incrementa el intento cuando corresponda, escribe el historial y registra el evento para Ventas. Operación nunca modifica directamente la base de datos de Gestión.

Al aceptar `FALLIDO`, Gestión crea el registro de incidencia en `intentos_entrega` y actualiza `despachos.ultima_incidencia_id` dentro de esa transacción. La misma regla se aplica a `NO_INTENTADO`, aunque no incremente el contador. Esa referencia es la utilizada por la consulta de §11.1 y no se sustituye por la jornada actual del repartidor.

### 13.4. Gestión comunica el estado confirmado a Operación

- **Método:** `POST`
- **Ruta:** `/internal/v1/proyecciones/despachos/{idDespacho}`
- **Idempotencia:** versión del despacho.

```json
{
  "idDespacho": "DSP-100234",
  "idPedido": "PED-2026-00891",
  "codigoRastreoInterno": "TRK-78901",
  "estado": "ASIGNADO",
  "idJornada": "JOR-20260923-0012",
  "idReserva": "RES-28719",
  "secuenciaRuta": 3,
  "destinatario": {
    "nombre": "Carlos Mendoza",
    "telefono": "+51987654321"
  },
  "destino": {
    "direccion": "Av. Javier Prado Este 2465",
    "referencia": "Frente al parque",
    "distrito": "San Borja"
  },
  "fechaProgramada": "2026-09-25",
  "numeroIntentos": 0,
  "version": 2,
  "actualizadoEn": "2026-09-23T19:10:00Z"
}
```

Al asignar o reasignar se envía la información completa necesaria para la ruta móvil. En cambios posteriores puede enviarse el mismo esquema actualizado. La proyección no es el estado canónico: una versión repetida se ignora y una versión anterior nunca reemplaza una posterior.

### 13.5. Gestión consulta repartidores y jornadas de incidencias

- **Método y ruta:** `POST /internal/v1/operacion/consulta-incidencias`.
- **Proveedor:** Operación de Reparto y Flota; consumidor autorizado: Gestión de Despachos, con credencial de servicio conforme a §13. No se expone en el Gateway.
- Es una lectura por lotes; no modifica datos ni requiere clave de idempotencia.
- Cuerpo obligatorio: `idsRepartidor` e `idsJornada`, arreglos de identificadores opacos únicos, de `0` a `100` elementos cada uno; al menos uno debe contener elementos. Elementos vacíos, duplicados, límites excedidos o campos desconocidos responden `400` con el formato de §3.5.

```json
{
  "idsRepartidor": ["REP-0012"],
  "idsJornada": ["JOR-20261014-0012"]
}
```

Respuesta `200 OK`:

```json
{
  "repartidores": [
    { "idRepartidor": "REP-0012", "nombre": "Juan Pérez" }
  ],
  "jornadas": [
    {
      "idJornada": "JOR-20261014-0012",
      "estado": "CERRADA",
      "cerradaEn": "2026-10-14T23:00:00Z"
    }
  ],
  "consultadoEn": "2026-10-15T14:30:00Z"
}
```

Se responde exactamente un elemento por identificador solicitado, sin elementos adicionales y conservando su orden. Un repartidor inexistente tiene `nombre=null`; uno dado de baja conserva su nombre histórico disponible. Una jornada inexistente tiene `estado=DESCONOCIDA` y `cerradaEn=null`; una activa tiene `estado=ACTIVA` y `cerradaEn=null`; una cerrada tiene `estado=CERRADA` y su fecha de cierre. La respuesta no incluye datos de contacto. El cierre manual o automático produce la misma condición `CERRADA`.

Gestión deduplica las jornadas de todas las incidencias pendientes de retorno de la base definida en §11.1 y las consulta en lotes de hasta 100 antes de filtrar atrasados o paginar. Así no calcula ese indicador con una sola página. Para los nombres basta consultar los repartidores de la página devuelta. Si solo faltan nombres, conserva filas y totales. No se efectúa una petición por fila ni se consultan tablas de Operación desde Gestión.

Cada lote obtenido aporta su `consultadoEn`. Una omisión o respuesta incoherente se trata como dato desconocido para los elementos afectados. Un timeout o indisponibilidad del servicio convierte en desconocidos los elementos del lote no obtenido y aplica la degradación de §11.1; no se usa como confirmación una copia antigua de una jornada activa. Si Operación no puede ejecutar su lectura, responde `503` con `code=DESP_ERROR_OPERACION_NO_DISPONIBLE`. Las credenciales inválidas se rechazan según §3.5; Gestión no omite la autenticación ni expone errores internos al usuario.

## 14. Reglas de idempotencia y concurrencia

- La idempotencia de negocio es obligatoria en todos los comandos que modifican estado.
- Crear despacho es único por `idPedido`; reenviar el mismo pedido devuelve el despacho existente.
- Cancelar, asignar, reasignar, iniciar traslado, entregar, fallar, recibir, reprogramar y cerrar deben reconocer una repetición segura mediante la clave de negocio, la versión o una clave de operación.
- `Idempotency-Key` es obligatorio como UUID v4 de hasta 128 caracteres para `POST /api/v1/despachos` y `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion`. En los demás comandos `POST` se exige únicamente cuando la operación lo declara expresamente.
- Una repetición exacta devuelve el resultado original sin duplicar historial, intento, reserva ni evento.
- Toda transición utiliza control de versión. Si otra operación modificó el despacho, se responde `409 Conflict` con el estado vigente.
- Los eventos conservan el mismo `idEvento` en cada reintento.
- Ningún fallo al enviar eventos revierte una transición ya confirmada.

## 15. Flujos de referencia

### 15.1. Cotización

```text
Marketplace/Chatbot -> Seguridad: client_credentials + scopes solicitados
Seguridad -> Marketplace/Chatbot: token de servicio
Marketplace/Chatbot -> Despacho: destino + líneas (SKU, cantidad) + Bearer token
Despacho -> Seguridad: client_credentials de modulo-despacho
Seguridad -> Despacho: token de servicio para Productos
Despacho -> Productos: consulta física en lote + Bearer token propio
Productos -> Despacho: peso + dimensiones por SKU
Despacho -> Despacho: calcula totales, cobertura, tarifa y plazo
Despacho -> Marketplace/Chatbot: cotización
```

### 15.2. Creación y entrega

```text
Ventas -> Despacho: pedido pagado y preparado + destinatario + destino + líneas (SKU, cantidad)
Despacho -> Productos: consulta física en lote por SKU
Productos -> Despacho: peso y dimensiones por SKU
Despacho: calcula peso/volumen, registra cantidadPaquetes=1 y crea PENDIENTE_ASIGNACION
Despacho -> Ventas: idDespacho + estado PENDIENTE_ASIGNACION
Gestor -> Despacho: asignar repartidor
Despacho -> Operación: reservar capacidad y proyectar ruta
Repartidor -> Operación: iniciar/entregar/fallar
Operación -> Despacho: solicitar transición
Despacho -> Ventas: evento asíncrono de estado
```

### 15.3. Seguimiento

```text
Chatbot/Marketplace -> Seguridad: obtiene token de servicio
Chatbot/Marketplace -> Despacho: GET seguimiento por idPedido
Despacho -> Canal: estado, fecha, distrito e hitos sin coordenadas ni PII
```

## 16. Acuerdos externos que aún deben confirmarse

El contrato funcional con Ventas y Postventa está cerrado: se confirmaron el momento de creación, el payload sin `cantidadPaquetes`, la cancelación, los siete eventos, la ruta y el scope del webhook y la convención de `Idempotency-Key`. Solo quedan el aprovisionamiento o verificación de credenciales por ambiente y las pruebas de contrato.

| Equipo | Acuerdo pendiente |
|---|---|
| Seguridad y Usuarios | Registrar los scopes de `api-despacho` y asignarlos a cada `client_id`; en particular, incorporar `despachos:cancelar` para `modulo-ventas` si aún conserva la configuración anterior y verificar `ventas:pedidos:estado` para `modulo-despacho` con `aud=api-ventas`; confirmar el valor de `roles` para la cuenta del repartidor; definir el canal de alta y baja global, la comunicación de `usuario_id`, la entrega de credenciales y el contrato RabbitMQ de eventos de usuario |
| Productos y Ofertas | Registrar en Seguridad la concesión de `productos:fisicos:leer` a `modulo-despacho` para `api-productos` y ejecutar las pruebas de contrato entre ambos backends |
| Marketplace y Chatbot | Registrar sus clientes técnicos con `cotizaciones:calcular` y `seguimientos:leer`; custodiar el `client_secret`; usar solamente `idPedido` para seguimiento |
| Equipo de Despacho | Tiempo de caché; límites de cotización; expiración de URLs firmadas y estrategia final para eventos internos |

