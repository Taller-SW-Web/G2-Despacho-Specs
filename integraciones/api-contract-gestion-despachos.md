# Contrato de API: Gestión de Despachos

## 1. Propósito y propiedad

Contrato del microservicio `servicio-gestion-despachos`, proveedor de F-01, F-02 y F-04. Gestión es dueño de zonas, tarifas, despacho canónico, incidencias, historial y eventos salientes. Sus rutas públicas se consumen a través del API Gateway; sus rutas `/internal/v1` son privadas.

## 2. Convenciones y contratos relacionados

Aplican las [convenciones compartidas](./api-contract.md#3-convenciones-comunes), [Seguridad y Usuarios](./api-contract.md#8-integración-con-seguridad-y-usuarios) y [reglas de idempotencia y concurrencia](./api-contract.md#9-reglas-de-idempotencia-y-concurrencia) del contrato externo. Los recursos administrativos requieren JWT humano con `GESTOR_DESPACHO`; el catálogo distingue los consumidores autorizados en §4. Las APIs privadas requieren credencial de servicio y no se publican en el Gateway.

El contrato de [Operación de Reparto y Flota](./api-contract-operacion-reparto.md) es la fuente de las operaciones de capacidad, proyecciones, jornadas y evidencia que Gestión consume. No se comparten tablas ni entidades JPA.

## 3. API administrativa de F-01 y F-02

### 3.1. Zonas y tarifas

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

### 3.2. Programación y asignación

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

## 4. Catálogo único de motivos de fallo

- **Método y ruta:** `GET /api/v1/catalogos/motivos-fallo`.
- **Autorización:** JWT humano válido y rol `GESTOR_DESPACHO`, o perfil local de repartidor activo vinculado al `sub`. Consultar el catálogo no exige una jornada abierta.
- **Respuesta `200 OK`:** objeto con `motivos`, arreglo de objetos con `codigo`, `etiqueta`, `seleccionableEnCampo`, `consumeIntento` y `activo`. Los tres últimos campos son booleanos obligatorios. Orden por `codigo` ascendente. No recibe filtros ni paginación.
- Devuelve el catálogo completo, incluidos motivos inactivos conservados para consultas históricas. F-03 ofrece para registrar únicamente los que tengan `activo=true` y `seleccionableEnCampo=true`; F-04 admite todos los códigos como filtro. La validación del backend aplica la misma restricción al registrar un fallo.
- `NO_INTENTADO` tiene `seleccionableEnCampo=false` y `consumeIntento=false`; lo genera exclusivamente el cierre de jornada. No se mantiene un segundo catálogo para F-04.
- Token no aceptado: `401`; usuario sin autorización: `403`, conforme a Común §3.5. Una caída al consultar el catálogo muestra un error y permite reintentar; el frontend no fabrica motivos. Referencia: [Convenciones e integración externa](./api-contract.md#35-errores).

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

## 5. API de F-04: entregas fallidas

Todos los recursos requieren JWT con rol `GESTOR_DESPACHO`.

| Método | Ruta | Propósito |
|---|---|---|
| `GET` | `/api/v1/despachos/fallidos` | Listar fallidos con filtros y paginación |
| `GET` | `/api/v1/despachos/{idDespacho}/incidencia` | Consultar detalle, intentos, recepción e historial |
| `POST` | `/api/v1/despachos/{idDespacho}/recepcion-centro` | Confirmar el retorno físico |
| `POST` | `/api/v1/despachos/{idDespacho}/reprogramacion` | Reprogramar un nuevo intento |
| `POST` | `/api/v1/despachos/{idDespacho}/devolucion-origen` | Cerrar como `DEVUELTO_A_ORIGEN` |

### 5.1. Consultar entregas fallidas — ES-F04-01

`GET /api/v1/despachos/fallidos` es una consulta de solo lectura y no requiere `Idempotency-Key`. Devuelve únicamente despachos cuyo estado actual es `FALLIDO`, sin limitar las fechas al abrir la pantalla. No es una consulta del historial completo.

Se devuelve una fila por despacho. `idIncidencia` identifica el registro de `intentos_entrega` enlazado por `despachos.ultima_incidencia_id`, correspondiente a su última transición aceptada a `FALLIDO`, incluso si fue `NO_INTENTADO`. Motivo, fecha, repartidor, jornada, recepción e indicador de evidencia proceden de ese mismo registro. El contador acumulado y el máximo configurado son datos distintos de la identidad de la incidencia. No se selecciona una incidencia por el contador ni se reutiliza la recepción de una anterior.

#### Parámetros de consulta

| Parámetro | Tipo y valor por defecto | Regla |
|---|---|---|
| `pagina` | Entero; `1` | Mínimo `1`. |
| `tamanoPagina` | Entero; `20` | De `1` a `100`. |
| `motivo` | Código del catálogo; omitido | Un único código exacto de Gestión §4, incluido `NO_INTENTADO` o un motivo inactivo. Omitir no restringe el motivo. Referencia: [Gestión](./api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo). |
| `fechaDesde` | Fecha `YYYY-MM-DD`; omitida | Inicio inclusivo del día en `America/Lima`, aplicado a la incidencia vigente. |
| `fechaHasta` | Fecha `YYYY-MM-DD`; omitida | Incluye todo el día en `America/Lima`; internamente se excluye el inicio del día siguiente. |
| `recepcion` | Enum; `TODOS` | `TODOS`, `PENDIENTE_RETORNO` o `RECIBIDO_EN_CENTRO`. |
| `soloRetornosAtrasados` | Booleano; `false` | `true` exige recepción pendiente y jornada confirmada como cerrada. Puede combinarse con recepción omitida, `TODOS` o `PENDIENTE_RETORNO`. |

Los límites de fecha son independientes: puede enviarse solo uno o ninguno. Si se envían ambos, `fechaDesde` no puede superar `fechaHasta`. Una fecha futura válida puede producir cero coincidencias. Los instantes de respuesta se expresan en UTC; esta regla de fechas civiles especifica cómo aplicar el filtro de días.

Parámetros desconocidos, repetidos, vacíos, formatos incorrectos, códigos/enum no admitidos, enteros fuera de rango o `soloRetornosAtrasados=true` junto con `recepcion=RECIBIDO_EN_CENTRO` responden `400` con `code=DESP_ERROR_FILTROS_INVALIDOS` y `errores` por campo según Común §3.5. Los booleanos aceptan solo `true` o `false`. No se admite orden libre: el orden contractual es fijo. Referencia: [Convenciones e integración externa](./api-contract.md#35-errores).

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

Gestión consulta los datos operativos mediante Operación §5.4. No interpreta una ausencia de información como jornada activa ni infiere cierre por medianoche o por el reloj del navegador. Referencia: [Operación](./api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias).

- Con recepción confirmada, `retornoAtrasado=false` aunque no se pueda consultar la jornada.
- Con recepción pendiente y jornada `ACTIVA`, vale `false`; con jornada `CERRADA`, vale `true`; con jornada `DESCONOCIDA`, vale `null` y la fila muestra `No se pudo confirmar el cierre de jornada`.
- La consulta normal conserva `200`, las filas y los indicadores locales exactos aunque Operación falle. Si existe alguna jornada pendiente desconocida en la base, `indicadores.retornosAtrasados=null`: se muestra `No disponible`, nunca cero ni una cifra parcial. La tarjeta de atrasados permanece visible y deshabilitada; las otras dos siguen disponibles. Se informa `retornosSinJornadaConfirmada` y se ofrece reintentar la consulta.
- Si se pidió `soloRetornosAtrasados=true` y falta confirmar alguna jornada pendiente de la base, se responde `503` con `code=DESP_ERROR_JORNADAS_NO_DISPONIBLES`; no se devuelve una página parcial ni un total inventado. Si la base no tiene pendientes, el filtro devuelve cero coincidencias sin necesitar esa dependencia.
- `401` y `403` se aplican antes de consultar y nunca devuelven filas ni indicadores. Los filtros válidos sin coincidencias responden `200` con contenido vacío; los fallos no se presentan como un estado vacío.

### 5.2. Comandos de recepción, reprogramación y cierre

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

## 6. API interna provista por Gestión

Estas rutas las implementa Gestión y las consume Operación con credencial de servicio. No se exponen mediante el Gateway.

### 6.1. Operación solicita una transición a Gestión

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

Al aceptar `FALLIDO`, Gestión crea el registro de incidencia en `intentos_entrega` y actualiza `despachos.ultima_incidencia_id` dentro de esa transacción. La misma regla se aplica a `NO_INTENTADO`, aunque no incremente el contador. Esa referencia es la utilizada por la consulta de Gestión §5.1 y no se sustituye por la jornada actual del repartidor. Referencia: [Gestión](./api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01).


## 7. APIs de Operación consumidas por Gestión

Las definiciones completas están en [API interna de Operación](./api-contract-operacion-reparto.md#5-api-interna-provista-por-operación): reservas (§5.1), liberaciones (§5.2), proyección de despachos (§5.3) y lectura por lotes de incidencias (§5.4). La [API del repartidor y evidencia](./api-contract-operacion-reparto.md#3-api-de-f-03-operación-del-repartidor) describe el acceso autorizado a fotografías.

El catálogo `/api/v1/catalogos/motivos-fallo` y las operaciones de F-02 `/api/v1/jornadas/{idJornada}/secuencia` y `/api/v1/jornadas/{idJornada}/ruta` pertenecen a Gestión, aunque sus consumidores trabajen con repartidores o jornadas. El Gateway debe respetar esta propiedad por operación; el resto de jornadas y la evidencia pertenecen a Operación. Esta división documental no modifica la configuración desplegada.

## 8. Integraciones externas implementadas o consumidas

Las entradas de módulos externos se implementan en Gestión y conservan su definición única en el contrato externo: [cotización y Productos](./api-contract.md#5-f-01-cotización-para-marketplace-y-chatbot), [seguimiento](./api-contract.md#6-rt-04-seguimiento-para-marketplace-y-chatbot) y [creación, cancelación y eventos de Ventas](./api-contract.md#7-f-02-integración-con-ventas-y-postventa). La validación de identidad y los clientes técnicos siguen [Seguridad](./api-contract.md#8-integración-con-seguridad-y-usuarios).

La reorganización no acredita endpoints implementados ni pruebas de contrato. Las especificaciones funcionales y su evidencia mantienen el estado real de cada operación.
