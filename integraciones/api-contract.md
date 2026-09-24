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
| Seguridad y Usuarios | Identidades, credenciales y roles | JWT de usuario, tokens de servicio, JWKS e identificadores de usuario | Solicitud de creación o vinculación de repartidores, pendiente de acuerdo |
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
| `Idempotency-Key: <uuid>` | Reintentos seguros en los comandos que lo declaren; la obligatoriedad general queda pendiente de acuerdo |
| `X-Correlation-Id: <uuid>` | Opcional; trazabilidad entre módulos. El Gateway lo genera si no llega |
| `Content-Type: application/json` | Cuerpos JSON |

La obtención de un token de servicio es la excepción al último encabezado: `POST /api/v1/auth/token` utiliza `Content-Type: application/x-www-form-urlencoded`, conforme al contrato de Seguridad y Usuarios.

### 3.3. Roles humanos y tokens de servicio

| Rol | Uso |
|---|---|
| `GESTOR_DESPACHO` | Todas las operaciones administrativas: zonas, tarifas, programación, asignación, incidencias, repartidores, furgonetas y jornadas |
| `REPARTIDOR` | Ruta propia, evidencia y operaciones de campo; su incorporación al catálogo de Seguridad está pendiente de acuerdo |

Los módulos externos no utilizan un rol humano `SERVICIO_INTEGRACION`. Seguridad emite tokens de servicio en los que:

- `sub` contiene el `client_id`, por ejemplo `modulo-chatbot` o `modulo-ventas`.
- `tipo` vale `servicio`.
- `scope` contiene los permisos concedidos al cliente.
- `iss` identifica al emisor de Seguridad.
- `iat`, `exp` y `jti` permiten validar emisión, vencimiento y unicidad del token.

Los tokens de usuarios humanos llevan `tipo=acceso`, un UUID de usuario en `sub` y sus roles en `roles`. Los tokens de refresco no se aceptan en las APIs de negocio.

El valor definitivo de `iss` y la representación del scope dentro del JWT (`scope` como texto o `scopes` como arreglo) deben confirmarse con Seguridad. No se exigirá `aud` mientras no forme parte de su contrato definitivo.

### 3.4. Scopes de servicio de Despacho

| Scope | Consumidores previstos | Operación autorizada |
|---|---|---|
| `cotizaciones:calcular` | Marketplace, Chatbot y, si lo requiere, Ventas | Calcular cobertura, costo y plazo |
| `seguimientos:leer` | Marketplace, Chatbot y Ventas | Consultar seguimiento por `idPedido` |
| `despachos:crear` | Ventas | Crear un despacho para un pedido pagado, preparado y listo para entrega |
| `despachos:cancelar` | Ventas | Solicitar cancelación por anulación del pedido |

Estos scopes pertenecen a la API de Despacho: Despacho define su significado y Seguridad los registra y concede a cada `client_id`. En cambio, `usuarios:leer` y `direcciones:leer` pertenecen a la API de Seguridad y ya están concedidos a `modulo-despacho`. El acceso de Despacho a datos físicos deberá usar el scope que defina Productos y Ofertas, propuesto provisionalmente como `productos:fisicos:leer`.

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
| `401 Unauthorized` | Credencial ausente, inválida o vencida |
| `403 Forbidden` | Credencial válida sin el rol o propiedad requerida |
| `404 Not Found` | Recurso inexistente |
| `409 Conflict` | Estado incompatible, duplicado o modificación concurrente |
| `422 Unprocessable Entity` | Solicitud válida, pero no procesable por una regla del negocio |
| `429 Too Many Requests` | Límite de cotizaciones excedido |
| `503 Service Unavailable` | Dependencia necesaria temporalmente no disponible |

## 4. Matriz de comunicaciones externas

| Origen | Destino | Comunicación | Seguridad | Mecanismo |
|---|---|---|---|---|
| Marketplace o Chatbot | Despacho | Solicitar cotización | Token de servicio con `cotizaciones:calcular` | REST síncrono |
| Marketplace o Chatbot | Despacho | Consultar seguimiento por `idPedido` | Token de servicio con `seguimientos:leer` | REST síncrono |
| Despacho | Productos y Ofertas | Consultar datos físicos por SKU | Token de `modulo-despacho` con scope definido por Productos | REST síncrono en lote |
| Ventas y Postventa | Despacho | Crear despacho de pedido listo para entrega | Token de servicio con `despachos:crear` | REST síncrono e idempotente |
| Ventas y Postventa | Despacho | Cancelar por anulación | Token de servicio con `despachos:cancelar` | REST síncrono e idempotente |
| Despacho | Ventas y Postventa | Informar cambios de estado | Token de servicio con scope definido por Ventas | Webhook con outbox y reintentos |
| Despacho | Seguridad y Usuarios | Obtener claves públicas | HTTPS | JWKS con caché |
| Despacho | Seguridad y Usuarios | Crear o vincular usuario de repartidor | Token de servicio; ruta y scope pendientes | REST síncrono con reintento manual |

## 5. F-01: cotización para Marketplace, Chatbot y Ventas

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
| Solo `destino` | Cobertura y tarifa base de la zona | `BASE` |
| `destino` y `lineas` | Cobertura y costo calculado con los datos físicos de los productos | `EXACTA` |
| Destino sin cobertura | Solo la cobertura, sin costo ni plazo | — |

Solicitud sin productos (cobertura y tarifa base):

```json
{
  "destino": {
    "distrito": "San Borja",
    "codigoPostal": "15036"
  }
}
```

Solicitud con productos:

```json
{
  "destino": {
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

- Debe informarse al menos `distrito` o `codigoPostal`.
- `lineas` es opcional. Si se omite, la cotización es `BASE`. Si se envía, debe contener al menos un elemento.
- En cada línea, `sku` es obligatorio y `cantidad` debe ser mayor que cero.
- Despacho evalúa primero la cobertura. Si el destino no tiene cobertura, responde sin consultar a Productos ni validar las líneas.
- Con `lineas`, Despacho agrupa los SKU repetidos, consulta a Productos en lote y calcula el peso y volumen totales; el canal no envía esos totales.
- La cotización `BASE` corresponde a la tarifa base de la zona y es un monto mínimo: el costo final puede aumentar según el peso y volumen reales.
- La cotización no crea un pedido ni un despacho.

Respuesta con cobertura, sin productos (`200 OK`):

```json
{
  "coberturaDisponible": true,
  "tipoCotizacion": "BASE",
  "idZona": "ZONA-LIMA-CENTRO",
  "nombreZona": "Lima Centro",
  "costoEnvio": 10.0,
  "pesoBaseKg": 3.0,
  "moneda": "PEN",
  "plazoEstimadoDiasHabiles": 2,
  "fechaEstimadaEntrega": "2026-09-25",
  "cotizadoEn": "2026-09-23T18:30:00Z"
}
```

Respuesta con cobertura, con productos (`200 OK`):

```json
{
  "coberturaDisponible": true,
  "tipoCotizacion": "EXACTA",
  "idZona": "ZONA-LIMA-CENTRO",
  "nombreZona": "Lima Centro",
  "pesoTotalKg": 2.65,
  "volumenTotalM3": 0.017,
  "costoEnvio": 14.5,
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
  "tipoCotizacion": null,
  "costoEnvio": null,
  "moneda": "PEN",
  "plazoEstimadoDiasHabiles": null,
  "fechaEstimadaEntrega": null,
  "mensaje": "La dirección se encuentra fuera de nuestra zona de cobertura"
}
```

Con `tipoCotizacion=BASE`, los canales deben presentar el monto como precio mínimo (por ejemplo, "desde S/ 10.00"). Despacho calcula tanto el plazo como la fecha estimada de entrega. Los canales pueden comunicar `fechaEstimadaEntrega` al cliente y Ventas puede conservarla como referencia, pero no debe enviarla al crear el despacho. Las promociones, incluido el envío gratuito, y el importe finalmente cobrado al cliente pertenecen a Ventas y Postventa y no modifican el costo logístico calculado por Despacho.

Errores propios:

| Código | HTTP | Condición |
|---|---|---|
| `DESP_ERROR_DESTINO_REQUERIDO` | `400` | No se informó `distrito` ni `codigoPostal` |
| `DESP_ERROR_LINEAS_VACIAS` | `400` | Se envió `lineas` sin elementos |
| `DESP_ERROR_CANTIDAD_INVALIDA` | `400` | Cantidad menor o igual a cero |
| `DESP_ERROR_PRODUCTO_NO_ENCONTRADO` | `422` | Productos no reconoce un SKU |
| `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS` | `422` | Falta peso o dimensiones válidas |
| `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE` | `503` | No fue posible consultar Productos |
| `DESP_ERROR_LIMITE_COTIZACION` | `429` | El canal excedió su límite |


### 5.2. Integración de Despacho con Productos y Ofertas

Esta operación pertenece a Productos y Ofertas. La ruta definitiva debe ser confirmada por ese equipo; Despacho requiere como mínimo un contrato equivalente al siguiente.

- **Método propuesto:** `POST`
- **Ruta propuesta:** `/api/v1/productos/datos-fisicos/consulta`
- **Consumidor:** backend de Despacho.
- **Autenticación:** token de servicio propio de `modulo-despacho`, con el scope que defina Productos; se propone `productos:fisicos:leer`.

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
- **Autenticación:** token de servicio con `tipo=servicio`, `sub=modulo-ventas` y scope `despachos:crear`.
- **Idempotencia:** unicidad obligatoria por `idPedido`. El uso de `Idempotency-Key` queda recomendado y pendiente de convención común entre módulos.

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
- **Autenticación:** token de servicio con `tipo=servicio`, `sub=modulo-ventas` y scope `despachos:cancelar`.
- **Idempotencia:** la repetición debe conservar el mismo resultado. El uso de `Idempotency-Key` queda recomendado y pendiente de convención común entre módulos.

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

- **Método esperado:** `POST`
- **Ruta propuesta de Ventas:** `/api/v1/integraciones/despachos/eventos`
- **Autenticación:** token de servicio de `modulo-despacho` emitido por Seguridad, con el scope de recepción que defina Ventas.
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

| Estado nuevo | Tipo de evento | Datos adicionales |
|---|---|---|
| `ASIGNADO` | `DESPACHO_ASIGNADO` | `fechaProgramada` |
| `EN_CAMINO` | `DESPACHO_EN_CAMINO` | Ninguno |
| `ENTREGADO` | `DESPACHO_ENTREGADO` | `fechaEntrega`, `recibidoPor` opcional |
| `FALLIDO` | `DESPACHO_FALLIDO` | `motivo`, `numeroIntento` |
| `PENDIENTE_ASIGNACION` reprogramado | `DESPACHO_REPROGRAMADO` | `nuevaFechaProgramada` |
| `DEVUELTO_A_ORIGEN` | `DESPACHO_DEVUELTO_A_ORIGEN` | `motivoCierre` |
| `CANCELADO` | `DESPACHO_CANCELADO` | Ninguno |

La política de intentos pertenece a Despacho: el máximo inicial es `2`, puede configurarse dentro del módulo y no se recibe desde Ventas. `DESPACHO_FALLIDO` informa un intento no exitoso, pero no representa necesariamente un cierre definitivo. Solo `DESPACHO_DEVUELTO_A_ORIGEN` comunica que la operación logística terminó sin entrega y permite que Ventas y Postventa decida la anulación, devolución comercial o reembolso que corresponda.

Despacho no envía una `guiaRemision`, no solicita reembolsos y no informa importes a devolver. Esas responsabilidades permanecen fuera de este contrato.

Si Ventas no responde con `2xx`, Despacho realiza hasta cinco reintentos con espera creciente. El mismo `idEvento` se conserva. Tras agotarlos, el evento queda como `ENVIO_FALLIDO` y puede reenviarse manualmente. Los despachos simulados no generan eventos externos.

## 8. Integración con Seguridad y Usuarios

### 8.1. Validación local de tokens

Despacho valida los JWT localmente, sin consultar a Seguridad en cada solicitud:

1. Obtiene la configuración desde `GET /api/v1/auth/.well-known/openid-configuration`.
2. Obtiene las claves públicas desde `GET /api/v1/auth/.well-known/jwks.json` y las mantiene en caché.
3. Verifica firma, algoritmo permitido, vencimiento y emisor.
4. Para una persona, exige `tipo=acceso` y el rol humano correspondiente.
5. Para un módulo, exige `tipo=servicio` y el scope propio de la operación.

No se exige el rol ficticio `SERVICIO_INTEGRACION` ni un claim separado `clientId`: la identidad técnica ya está en `sub`. Tampoco se combina el token con una API key.

Ejemplo conceptual de token de usuario:

```json
{
  "sub": "2f31c1b1-7568-41b8-bf91-342db68431df",
  "tipo": "acceso",
  "roles": ["GESTOR_DESPACHO"],
  "iss": "auth-service",
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
  "iss": "auth-service",
  "iat": 1789273200,
  "exp": 1789276800,
  "jti": "ad6b5dda-c481-4ad3-907a-04a56d392de7"
}
```

`iss=auth-service` y el campo `scope` son ilustrativos. Seguridad debe confirmar el valor exacto del emisor y si entrega `scope` como texto o `scopes` como arreglo. Su contrato actual no documenta `aud`, por lo que Despacho no debe inventarlo como requisito.

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
  "access_token": "<jwt-de-servicio>",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "cotizaciones:calcular seguimientos:leer"
}
```

El canal utiliza después `Authorization: Bearer <jwt-de-servicio>` al llamar a Despacho. Del mismo modo, `modulo-despacho` solicita otro token con sus propias credenciales y el scope aceptado por Productos; nunca reutiliza el token del canal.

### 8.3. Introspección de un usuario antes de una operación sensible

Seguridad ofrece `POST /api/v1/auth/introspeccion` para que un backend compruebe un token humano antes de una operación sensible. Esa ruta recibe el token humano en el cuerpo y se protege con el token de servicio del módulo que realiza la comprobación y el scope `tokens:introspeccion`.

Por ejemplo, si una persona administradora autoriza anular un pedido, Ventas valida o introspecciona el token de esa persona y luego llama a Despacho con el token técnico de `modulo-ventas` y `despachos:cancelar`. Despacho valida ese token de servicio localmente; no necesita introspeccionar el token técnico ni recibir el token humano de Ventas.

Seguridad todavía no ha concedido `tokens:introspeccion` a `modulo-despacho`; no se incluye como dependencia hasta que exista un caso de uso propio que lo requiera.

### 8.4. Creación y vinculación de un usuario repartidor

El contrato actual de Seguridad todavía no contiene el rol `REPARTIDOR` ni una operación específica para que Despacho cree o vincule esa cuenta. Por tanto, lo siguiente es una propuesta pendiente, no una API confirmada:

- **Método propuesto:** `POST`
- **Ruta propuesta:** `/api/v1/usuarios/integraciones/repartidores`
- **Consumidor:** `modulo-despacho`.
- **Autenticación propuesta:** token de servicio con un scope que Seguridad deberá definir, por ejemplo `usuarios:crear:repartidor`.
- **Idempotencia:** unicidad por `idRepartidor` y correo.

```json
{
  "idRepartidor": "REP-0012",
  "nombres": "Juan",
  "apellidos": "Pérez",
  "documentoIdentidad": "71234567",
  "correo": "juan.perez@example.com",
  "telefono": "+51987654321",
  "rol": "REPARTIDOR"
}
```

```json
{
  "idUsuario": "USR-9021",
  "idRepartidor": "REP-0012",
  "rol": "REPARTIDOR",
  "estado": "PENDIENTE_ACTIVACION"
}
```

Seguridad no devuelve un token al crear la cuenta. Debe enviar una invitación o permitir que el repartidor defina sus credenciales; el token se emite recién cuando inicia sesión. Despacho almacena solamente `idUsuario`, el vínculo y el estado operativo, nunca la contraseña.

Si Seguridad no está disponible, F-05 conserva al repartidor con `vinculacion=PENDIENTE` o `ERROR`. Cuando la cuenta existe pero espera al usuario, usa `PENDIENTE_ACTIVACION`; solo cambia a `VINCULADO` cuando Seguridad confirma que puede iniciar sesión. No se abre una jornada antes de `VINCULADO`. Dar de baja al repartidor en Despacho impide asignarle jornadas; bloquear su acceso es una operación separada cuya API pertenece a Seguridad.

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

Todos los recursos requieren JWT con rol `REPARTIDOR`. El backend obtiene el usuario desde el token y resuelve el repartidor vinculado; el cliente no puede elegir otro `idRepartidor`.

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
| `GET` | `/api/v1/catalogos/motivos-fallo` | Consultar motivos seleccionables |
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

## 11. API de F-04: entregas fallidas

Todos los recursos requieren JWT con rol `GESTOR_DESPACHO`.

| Método | Ruta | Propósito |
|---|---|---|
| `GET` | `/api/v1/despachos/fallidos` | Listar fallidos con filtros y paginación |
| `GET` | `/api/v1/despachos/{idDespacho}/incidencia` | Consultar detalle, intentos, recepción e historial |
| `POST` | `/api/v1/despachos/{idDespacho}/recepcion-centro` | Confirmar el retorno físico |
| `POST` | `/api/v1/despachos/{idDespacho}/reprogramacion` | Reprogramar un nuevo intento |
| `POST` | `/api/v1/despachos/{idDespacho}/devolucion-origen` | Cerrar como `DEVUELTO_A_ORIGEN` |

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
| `POST` | `/api/v1/repartidores` | `GESTOR_DESPACHO` | Registrar y solicitar vinculación |
| `GET` | `/api/v1/repartidores/{idRepartidor}` | `GESTOR_DESPACHO` | Consultar detalle |
| `PUT` | `/api/v1/repartidores/{idRepartidor}` | `GESTOR_DESPACHO` | Editar |
| `PATCH` | `/api/v1/repartidores/{idRepartidor}/estado` | `GESTOR_DESPACHO` | Alta o baja lógica |
| `POST` | `/api/v1/repartidores/{idRepartidor}/vinculacion/reintento` | `GESTOR_DESPACHO` | Reintentar alta en Seguridad |
| `GET` | `/api/v1/furgonetas` | `GESTOR_DESPACHO` | Listar furgonetas |
| `POST` | `/api/v1/furgonetas` | `GESTOR_DESPACHO` | Registrar furgoneta |
| `PUT` | `/api/v1/furgonetas/{idFurgoneta}` | `GESTOR_DESPACHO` | Editar límites |
| `PATCH` | `/api/v1/furgonetas/{idFurgoneta}/estado` | `GESTOR_DESPACHO` | Cambiar disponibilidad o mantenimiento |

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
    "pesoKg": 2.8,
    "volumenM3": 0.02,
    "paquetes": 1
  }
}
```

```json
{
  "idReserva": "RES-28719",
  "estado": "CONFIRMADA",
  "capacidadRemanente": {
    "pesoKg": 317.2,
    "volumenM3": 2.68,
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

## 14. Reglas de idempotencia y concurrencia

- La idempotencia de negocio es obligatoria aunque todavía no se adopte un encabezado común.
- Crear despacho es único por `idPedido`; reenviar el mismo pedido devuelve el despacho existente.
- Cancelar, asignar, reasignar, iniciar traslado, entregar, fallar, recibir, reprogramar y cerrar deben reconocer una repetición segura mediante la clave de negocio, la versión o una clave de operación.
- `Idempotency-Key` se recomienda para comandos `POST`, especialmente desde clientes móviles, pero su obligatoriedad queda pendiente de acuerdo entre los equipos.
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

| Equipo | Acuerdo pendiente |
|---|---|
| Seguridad y Usuarios | Valor exacto de `iss`; representación de scopes; registrar los cuatro scopes de Despacho y asignarlos a cada `client_id`; incorporar `REPARTIDOR`; definir alta, invitación, baja y vinculación de su cuenta |
| Productos y Ofertas | Ruta y esquema definitivo de la consulta física en lote; unidades; scope requerido, propuesto como `productos:fisicos:leer` |
| Ventas y Postventa | Registrar `modulo-ventas` con `despachos:crear`, `despachos:cancelar` y `seguimientos:leer`; invocar la creación solo cuando el pedido esté pagado, preparado y listo para entrega; proporcionar la URL y definir el scope de recepción del webhook; autorizar al usuario antes de solicitar una cancelación |
| Marketplace y Chatbot | Registrar sus clientes técnicos con `cotizaciones:calcular` y `seguimientos:leer`; custodiar el `client_secret`; usar solamente `idPedido` para seguimiento |
| Equipo de Despacho | Convención final de `Idempotency-Key`; tiempo de caché; límites de cotización; expiración de URLs firmadas y estrategia final para eventos internos |

