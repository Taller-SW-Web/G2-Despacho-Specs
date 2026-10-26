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

**Integración con reprogramaciones de F-04:** una transición aceptada a `PENDIENTE_ASIGNACION` aparece inmediatamente en la cola, sujeta a sus filtros; no espera a la nueva fecha para incorporarse. Se utiliza `fechaProgramada` como fecha civil y «hoy» del servidor en `America/Lima`. Una fecha futura mantiene la fila en solo lectura y el comando de asignación la rechaza con `409`; desde su fecha puede asignarse si cumple las demás condiciones, incluida la liberación de toda reserva anterior conforme a Operación §5.1.

El filtro `tipoIntento` de la cola admite `TODOS`, `PRIMER_INTENTO` y `REINTENTOS`. `REINTENTOS` selecciona despachos con al menos una reprogramación aceptada en su historial; `PRIMER_INTENTO`, los que no tienen ninguna; `TODOS` no aplica esa restricción. No se deduce la reprogramación de `numeroIntentos > 1`: el acumulado cuenta fallos reales, permanece en uno tras el primer fallo reprogramado y puede seguir en cero con `NO_INTENTADO`. La etiqueta `Reintento` y el KPI correspondiente usan esa misma condición, sin incrementar el contador ni presentar una nueva salida como ya realizada. Las demás reglas de la cola se desarrollan en [ES-F02-03](../especificaciones/ES-F02-03-ConsultarColaPendientes/spec.md).

#### 3.2.1. Ruta y secuencia administrativa — ES-F02-05

`GET /api/v1/jornadas/{idJornada}/ruta` requiere JWT humano `GESTOR_DESPACHO`, sin cuerpo ni parámetros. Responde `200`, `Cache-Control: no-store` y `ETag`. Campos: `idJornada` (cadena opaca), `estadoJornada` (`ACTIVA`/`CERRADA`), `despachos` ordenados por `posicion`, `versionRuta` (igual al ETag, incluidas sus comillas) y `consultadoEn` UTC. Cada parada contiene `idDespacho` UUID, `codigoOperativo`, `codigoRastreoInterno`, `estado`, `posicion`, `version`, `destinatario` (nombre), `direccion`, `pesoKg`, `volumenM3`, `cantidadPaquetes` y `actualizadoEn` UTC.

Gestión consulta el estado de jornada mediante Operación §5.4 fuera de su transacción local. Jornada confirmada sin paradas: arreglo vacío; cerrada: solo lectura. Jornada desconocida o proveedor no disponible: `503 DESP_ERROR_OPERACION_NO_DISPONIBLE`; §5.4 no distingue inexistencia de indisponibilidad y no permite fabricar un `404`.

`PUT /api/v1/jornadas/{idJornada}/secuencia` conserva el cuerpo de §3.2 e incluye **todas** las paradas vigentes, una vez cada una (máximo 1000). Requiere `If-Match` con la `versionRuta` original e `Idempotency-Key` UUID v4; no admite parámetros. Ausencia/formato inválido, omisiones, ajenos, duplicados o posiciones inválidas: `400`; fotografía desactualizada, jornada cerrada o intento de mover una parada no `ASIGNADO`: `409`; sin token: `401`; sin rol humano: `403`.

**Posiciones e historia:** se permutan exactamente las posiciones vigentes, sin nuevos huecos ni duplicados. Una ruta nueva tiene `1..N`; los huecos históricos por retiro se conservan, sin renumerar paradas iniciadas/cerradas. Solo `ASIGNADO` cambia de posición. Esta precisión reemplaza la interpretación de compactación global de las guías anteriores y rige para futuras cancelaciones/reasignaciones.

La versión es una huella de identidades, versiones, estados y posiciones. Gestión serializa con la asignación por jornada, bloquea filas en orden determinista, compara la fotografía y persiste posiciones, versiones, historial y outbox atómicamente. La consulta previa de estado no constituye una transacción distribuida con F-06; sus reglas impiden cerrar una jornada con paradas asignadas.

Responde `200` con el esquema de ruta y ETag nuevo. Repetir actor, clave, jornada, If-Match y cuerpo recupera el resultado original aunque la ruta avance o la jornada cierre, sin efectos duplicados; otra solicitud con esa clave produce `409`. Tras perder respuesta el cliente conserva y reenvía exactamente ese comando, sin clave nueva ni aplicar la edición sobre otra fotografía.

Cada parada modificada registra `REORDENAMIENTO`, posiciones anterior/nueva, secuencias completas, jornada, usuario y UTC. Falla de historial revierte el lote. El outbox publica proyecciones versionadas para F-03; no genera evento comercial de cambio de estado a Ventas. El repartidor ve el orden tras procesar las proyecciones, no necesariamente en la primera consulta anterior a su entrega.

## 4. Catálogo único de motivos de fallo

- **Método y ruta:** `GET /api/v1/catalogos/motivos-fallo`.
- **Autorización:** JWT humano válido y rol `GESTOR_DESPACHO`, o perfil local de repartidor activo vinculado al `sub`. Consultar el catálogo no exige una jornada abierta.
- **Respuesta `200 OK`:** objeto con `motivos`, arreglo de objetos con `codigo`, `etiqueta`, `seleccionableEnCampo`, `consumeIntento` y `activo`. Los tres últimos campos son booleanos obligatorios. Orden por `codigo` ascendente. No recibe filtros ni paginación.
- Devuelve el catálogo completo, incluidos motivos inactivos conservados para consultas históricas. F-03 ofrece para registrar únicamente los que tengan `activo=true` y `seleccionableEnCampo=true`; F-04 admite todos los códigos como filtro. La validación del backend aplica la misma restricción al registrar un fallo.
- `NO_INTENTADO` tiene `seleccionableEnCampo=false` y `consumeIntento=false`; lo genera exclusivamente el cierre de jornada. No se mantiene un segundo catálogo para F-04.
- Token no aceptado: `401`; usuario sin autorización: `403`, conforme a Común §3.5. Una caída al consultar el catálogo muestra un error y permite reintentar; el frontend no fabrica motivos. Referencia: [Convenciones e integración externa](./api-contract.md#35-errores).
- Si la lectura local no está disponible, responde `503` con `DESP_ERROR_CONSULTA_NO_DISPONIBLE` y el formato compartido, sin motivos parciales ni detalles de infraestructura.

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

Si no puede ejecutarse la lectura canónica de Gestión, responde `503` con `DESP_ERROR_CONSULTA_NO_DISPONIBLE`, sin filas ni detalles de infraestructura. Un despacho fallido con referencia vigente ausente, ajena o incompatible, o una política de intentos inválida, responde `500` con `DESP_ERROR_DATOS_INCONSISTENTES`, sin resultados parciales. Se reutilizan los códigos de la consulta de incidencia de §5.3 y el formato de errores compartido; no se exponen SQL, credenciales ni mensajes internos.

### 5.2. Comandos de recepción, reprogramación y cierre

Los tres comandos requieren `idIncidencia` (cadena opaca) y `versionDespacho` (entero positivo) obtenidos del detalle o listado. Tras autenticar y reconocer una repetición exacta ya aceptada, Gestión compara ambos con la incidencia vigente y la versión actual; una diferencia responde `409` con `code=DESP_ERROR_DESPACHO_DESACTUALIZADO`, sin mutación. La UI vuelve a consultar y solicita una nueva confirmación; nunca reenvía automáticamente la decisión sobre otra incidencia. Campo ausente o formato inválido responde `400` normalizado por campo.

La identidad de un comando aceptado se compone de despacho, incidencia, tipo de operación y versión presentada; se compara además su contenido normalizado y el `sub` del ejecutor con los ya aceptados. Una repetición exacta conserva el resultado original y no vuelve a producir efectos; reutilizar esa identidad con contenido o ejecutor diferente responde `409`. Esta protección es local al comando y no requiere compartir una transacción con Operación; la recepción y su liberación recuperable se concretan en §5.2.1.

Confirmación de recepción:

```json
{
  "idIncidencia": "INC-0021",
  "versionDespacho": 8,
  "selloIntacto": true,
  "observacion": "Paquete recibido sin daño visible"
}
```

La recepción no cambia `FALLIDO`: registra el retorno físico y habilita las decisiones según recepción, intentos y anulación. La capacidad se libera de forma recuperable en Operación conforme a §5.2.1; no se promete una confirmación distribuida instantánea.

Reprogramación:

```json
{
  "idIncidencia": "INC-0021",
  "versionDespacho": 8,
  "nuevaFechaProgramada": "2026-09-26",
  "observacion": "Cliente confirmó disponibilidad"
}
```

Cierre:

```json
{
  "idIncidencia": "INC-0021",
  "versionDespacho": 8,
  "motivo": "MAXIMO_INTENTOS_ALCANZADO",
  "observacion": "Paquete queda a disposición de Ventas"
}
```

#### 5.2.1. Confirmar recepción en centro — ES-F04-03

- **Método y ruta:** `POST /api/v1/despachos/{idDespacho}/recepcion-centro`; JWT humano válido con `GESTOR_DESPACHO`. No requiere `Idempotency-Key`; aplica la identidad de operación de §5.2, con el ejecutor autenticado.
- **Cuerpo:** únicamente `idIncidencia`, `versionDespacho`, `selloIntacto` y `observacion` opcional, según el ejemplo de §5.2. Identificadores como cadenas opacas no vacías, versión entera positiva y sello booleano obligatorio; `false` es válido. No admite campos extra ni parámetros de consulta.
- `observacion`: cadena de hasta 500 puntos de código Unicode después de recortar espacios en extremos, conservando saltos de línea internos; omisión, `null` o texto de solo espacios se normalizan a `null`. Cualquier otro tipo o longitud excedida responde `400` por campo. Es opcional incluso con sello No.
- La solicitud nueva exige despacho `FALLIDO`, incidencia vigente y recepción pendiente. Gestión obtiene reserva, jornada y repartidor de la instantánea de esa incidencia. Usuario y fecha proceden del JWT y del servidor; no se aceptan como campos editables.
- La disponibilidad de Operación, el cierre de jornada, anulación del pedido, máximo de intentos, `NO_INTENTADO` o fotografía no condicionan la recepción física. Una inconsistencia local de referencias sí se rechaza antes de persistir.

**Transacción local:** registrar recepción, incrementar `despachos.version`, insertar un único historial `RECEPCION_EN_CENTRO` y una solicitud durable en `liberaciones_capacidad`. La solicitud fija despacho, incidencia, reserva y jornada originales, ejecutor, versión presentada, contenido normalizado y respuesta original. Todo se confirma o revierte junto; sin transacción aceptada no se invoca la liberación. No modifica intentos ni genera un evento a Ventas porque no cambia el estado del despacho.

**Respuesta nueva `202 Accepted`:** recepción ya persistida y liberación asíncrona pendiente; `Cache-Control: no-store`. Todos los campos siguientes son obligatorios y solo los declarados admiten `null`:

| Campo | Tipo | Contenido |
|---|---|---|
| `idDespacho`, `idIncidencia` | Cadenas | Identidades aceptadas. |
| `estado` | Enum | `FALLIDO`. |
| `versionDespacho` | Entero positivo | Versión posterior a registrar la recepción. |
| `recepcion` | Objeto | `estado=RECIBIDO_EN_CENTRO`, `confirmadaEn` UTC, `idUsuario` cadena, `selloIntacto` booleano, `observacion` cadena o `null` y `liberacionCapacidad` según §5.3. |

La respuesta original contiene liberación `PENDIENTE`, `requiereRevision=false` y `confirmadaEn=null`. Una repetición exacta del mismo ejecutor devuelve ese mismo `202` y cuerpo, aunque ya se haya liberado la reserva o resuelto el despacho; se conserva la respuesta durable, no solo una caché temporal. Para conocer la situación actual se usa el GET de §5.3. Una recepción existente recibida con una identidad nueva no se sobrescribe.

| HTTP | Código | Efecto |
|---|---|---|
| `400` | `DESP_ERROR_DATOS_RECEPCION_INVALIDOS` | Campos ausentes, extra o inválidos; `errores` por campo según Común §3.5; sin escrituras. |
| `401` / `403` | Convenciones compartidas | Sin datos ni cambios; autenticar antes de consultar existencia/resultados. |
| `404` | `DESP_ERROR_DESPACHO_NO_ENCONTRADO` | Despacho inexistente. |
| `409` | `DESP_ERROR_OPERACION_REUTILIZADA` | Identidad ya aceptada con contenido normalizado o ejecutor diferente. |
| `409` | `DESP_ERROR_DESPACHO_DESACTUALIZADO` | Incidencia/versión actuales distintas en una solicitud nueva. |
| `409` | `DESP_ERROR_ESTADO_INCOMPATIBLE` | Estado actual distinto de `FALLIDO`, una vez comprobada la versión. |
| `409` | `DESP_ERROR_RECEPCION_YA_CONFIRMADA` | Recepción existente ante una solicitud nueva; se consulta el resultado sin editarlo. |
| `500` | `DESP_ERROR_DATOS_INCONSISTENTES` | Falta referencia a reserva/jornada/repartidor de la incidencia o relación local inválida; no inventar otra referencia. |
| `503` | `DESP_ERROR_RECEPCION_NO_DISPONIBLE` | No se pudo confirmar el resultado al cliente; consultar el detalle antes de repetir exactamente la solicitud. |

El orden es autenticación/autorización, formato, repetición aceptada y, para una solicitud nueva, identidad/versión, estado, recepción pendiente e integridad local. Una transacción revertida no deja escrituras parciales. Si se desconoce el resultado de la confirmación o se perdió la respuesta, consultar el detalle antes de reenviar la misma solicitud original; no afirmar una reversión sin haberla comprobado.

**Entrega recuperable a Operación:** el procesador toma solicitudes pendientes con exclusión temporal y tiempo máximo de procesamiento; no mantiene una transacción de base abierta durante HTTP. Un reinicio permite retomarlas sin perder la solicitud y llamadas repetidas resultan seguras por `idReserva`.

- Primer intento tan pronto como se confirma la transacción. Tras fallo, esperas de 30 s, 2 min, 10 min, 30 min y luego 60 min entre intentos hasta confirmar; el calendario se configura en Gestión con ese valor inicial. Se conserva un próximo intento persistido, incluso después de reiniciar.
- Con timeout, `429`, `5xx` o respuesta perdida, conservar `PENDIENTE` y la misma reserva. Solo una respuesta `200` de Operación §5.2 con los identificadores esperados y `estado=LIBERADA` permite marcar `CONFIRMADA`.
- Ante `401/403`, `404/409`, otros `4xx` o respuesta incoherente, marcar también `requiereRevision=true`, dejar aviso operativo y limitar los siguientes intentos a uno cada 60 min hasta corregir la causa. No descartar la solicitud, sustituir su reserva ni afirmar capacidad libre; tras confirmación se limpia el aviso.
- La confirmación se guarda en la solicitud local con su fecha, sin otro historial de recepción ni incremento del contador/versión del despacho. Si se pierde esa actualización local, el siguiente intento recibe la misma reserva ya liberada y completa el registro.
- Una liberación pendiente no revierte el retorno ni bloquea por sí sola reprogramación/cierre. Operación sigue contando su reserva activa; una asignación nueva de F-02 se rechaza mientras esa reserva anterior permanezca activa. El GET no ejecuta reintentos.

#### 5.2.2. Reprogramar un despacho fallido — ES-F04-04

- **Método y ruta:** `POST /api/v1/despachos/{idDespacho}/reprogramacion`; JWT humano válido con `GESTOR_DESPACHO`. No requiere `Idempotency-Key`; utiliza la identidad de comando de §5.2.
- **Cuerpo:** únicamente `idIncidencia`, `versionDespacho`, `nuevaFechaProgramada` y `observacion` opcional, según el ejemplo de §5.2. Identificadores opacos no vacíos, versión entera positiva y fecha obligatoria. No admite campos extra ni parámetros de consulta.
- `nuevaFechaProgramada`: cadena de fecha civil real en formato exacto `YYYY-MM-DD`, sin hora, entre los años `0001` y `9999`. Para una solicitud nueva debe ser estrictamente posterior al día del servidor en `America/Lima`, calculado al validar dentro de la operación; no al recibir la página ni según UTC o el navegador. No se excluyen fines de semana/feriados ni se impone un plazo tarifario u otro horizonte de anticipación.
- `observacion`: cadena de hasta 500 puntos de código Unicode después de recortar espacios en extremos; conserva saltos internos. Omisión, `null` o solo espacios se normalizan a `null`; otros tipos o exceso de longitud responden `400` por campo. No modifica la observación de recepción ni la de asignación.
- Solicitud nueva: incidencia/versión vigentes, estado `FALLIDO`, recepción confirmada de esa incidencia, pedido no anulado y contador acumulado menor al máximo configurado vigente. Máximo inicial dos; ausente, no entero o no positivo es inconsistencia local. `NO_INTENTADO` no incrementa ni reinicia el contador y está sujeto al mismo límite.
- La liberación de capacidad pendiente/de revisión, jornada activa/cerrada, sello alterado, foto ausente o caída de Operación no bloquean la decisión. Se conserva la zona original aunque esté inactiva, sin recotizar ni consultar Productos o el estado comercial en Ventas.

**Transacción local:** actualizar a `PENDIENTE_ASIGNACION`, guardar `fecha_programada`, fijar `en_cola_desde` al instante UTC de aceptación e incrementar `despachos.version`. Retirar las referencias de asignación vigente (`repartidor_id_externo`, `asignacion_diaria_id_externa`, `reserva_capacidad_id_externa` y `secuencia_ruta` quedan `null`); conservar sus instantáneas históricas, `ultima_incidencia_id`, recepción y solicitud de liberación. Conservar identidad del despacho/pedido, zona, destino, carga, contador y marca de simulación.

En esa misma transacción insertar un historial `TRANSICION` de `FALLIDO` a `PENDIENTE_ASIGNACION`, funcionalidad `F-04`, origen `MANUAL`, ejecutor del JWT, observación normalizada y `datos` de reprogramación según §5.3; registrar el resultado durable del comando y, si no es simulado, un evento `DESPACHO_REPROGRAMADO`. Todo se confirma o revierte junto, incluida la comparación de versión al escribir. No libera ni reserva capacidad, no modifica la solicitud de ES-F04-03 y no realiza llamadas externas dentro de la transacción.

**Respuesta nueva `200 OK`:** decisión local confirmada; `Cache-Control: no-store`. Todos los campos son obligatorios; solo los declarados admiten `null`:

| Campo | Tipo | Contenido |
|---|---|---|
| `idDespacho`, `idIncidencia` | Cadenas | Identidades aceptadas. |
| `estado` | Enum | `PENDIENTE_ASIGNACION`. |
| `versionDespacho` | Entero positivo | Versión posterior a la transición. |
| `fechaProgramada` | Fecha civil | Fecha aceptada, `YYYY-MM-DD`. |
| `numeroIntentos` | Entero no negativo | Acumulado conservado. |
| `observacion` | Cadena o `null` | Texto normalizado de esta decisión. |
| `reprogramadoEn` | Instante UTC | Instante persistido; coincide con entrada a cola e historial de esta transición. |
| `idEvento` | Cadena o `null` | Evento registrado para envío; `null` únicamente si es simulado. No acredita entrega a Ventas. |

La respuesta original y su identidad, ejecutor y huella del contenido normalizado se conservan de forma durable, junto al historial, no solo en una caché de 24 horas. Una repetición exacta autorizada del mismo ejecutor devuelve ese mismo `200` y cuerpo, incluso si ya pasó la fecha, se asignó el despacho o hay otra incidencia; se reconoce antes de validar las precondiciones actuales. No vuelve a incrementar versión ni cambia entrada a cola, historial o evento. Para conocer la situación actual se consulta §5.3.

**Orden de evaluación:** autenticación/autorización, formato/tipos y normalización, reconocimiento de identidad ya aceptada y, para una solicitud nueva, existencia, coincidencia incidencia/versión, estado `FALLIDO`, recepción de esa incidencia, anulación, integridad/política vigente, límite y fecha futura. Una fecha con formato válido que ya no es futura no impide recuperar un resultado original. Si coinciden anulación y límite se informa primero anulación; si falta recepción se exige primero recibir. La UI sigue mostrando todos los bloqueos calculados por §5.3.

| HTTP | Código | Efecto |
|---|---|---|
| `400` | `DESP_ERROR_DATOS_REPROGRAMACION_INVALIDOS` | Campos ausentes, extra, de tipo/formato inválidos, observación excedida o fecha no futura para una solicitud nueva; `errores` por campo según Común §3.5; sin escrituras. |
| `401` / `403` | Convenciones compartidas | Sin datos ni cambios; autenticar antes de consultar existencia/resultados. |
| `404` | `DESP_ERROR_DESPACHO_NO_ENCONTRADO` | Despacho inexistente. |
| `409` | `DESP_ERROR_OPERACION_REUTILIZADA` | Identidad aceptada con contenido normalizado o ejecutor diferente. |
| `409` | `DESP_ERROR_DESPACHO_DESACTUALIZADO` | Incidencia/versión distintas o comparación de versión fallida al escribir. |
| `409` | `DESP_ERROR_ESTADO_INCOMPATIBLE` | Estado distinto de `FALLIDO` después de comprobar identidad/versión. |
| `409` | `DESP_ERROR_RECEPCION_PENDIENTE` | Sin recepción confirmada de esa incidencia. |
| `409` | `DESP_ERROR_PEDIDO_ANULADO` | F-02 registró anulación; corresponde cierre después de recibir. |
| `422` | `DESP_ERROR_MAXIMO_INTENTOS_ALCANZADO` | Contador igual o superior al máximo vigente; no consume otro intento. |
| `500` | `DESP_ERROR_DATOS_INCONSISTENTES` | Política o referencias locales inválidas, incluida recepción confirmada sin su solicitud durable; no inventar datos. |
| `503` | `DESP_ERROR_REPROGRAMACION_NO_DISPONIBLE` | No se pudo confirmar el resultado al cliente; consultar antes de repetir exactamente la solicitud original. |

Dos reprogramaciones diferentes, reprogramación/cierre o reprogramación/anulación compiten por la versión del mismo despacho. Solo una mutación puede confirmar sobre esa versión; la perdedora recibe `409` sin efectos parciales. Una repetición exacta concurrente se reconoce con el resultado durable ganador. Registrar anulación en `FALLIDO` también incrementa la versión, aunque no cambie el estado. Si ganó reprogramación, una nueva cancelación de F-02 evalúa el estado `PENDIENTE_ASIGNACION`; no se pierde silenciosamente la solicitud de Ventas.

Si se pierde la respuesta, consultar detalle antes de reenviar la misma identidad/contenido original; un GET por sí solo no prueba quién resolvió ni qué resultado recibió otro comando. No reutilizar automáticamente versión/incidencia nuevas. Tras `409/422`, volver a consultar y revisar antes de otra decisión. Un fallo de lectura después de un `200` no convierte el guardado aceptado en un rechazo.

**Integraciones:** F-02 ve la entrada a cola inmediatamente conforme a §3.2; asigna desde la fecha programada si cumple las condiciones de capacidad. La solicitud de liberación anterior continúa por §5.2.1 y no se sustituye por la nueva reserva. RT-03 entrega el evento fuera de la transacción conforme a [Común §7.3](./api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa), con `datos.nuevaFechaProgramada` como fecha civil: una caída de Ventas no revierte la reprogramación, los reintentos conservan `idEvento` y los simulados no generan eventos externos.

#### 5.2.3. Cerrar como devuelto a origen — ES-F04-05

- **Método y ruta:** `POST /api/v1/despachos/{idDespacho}/devolucion-origen`; JWT humano válido, `tipo=acceso` y rol `GESTOR_DESPACHO`. No requiere `Idempotency-Key`; utiliza la identidad de §5.2.
- **Cuerpo:** únicamente `idIncidencia`, `versionDespacho`, `motivo` y `observacion` opcional, según el ejemplo de §5.2; identificadores opacos no vacíos y versión entera positiva. No admite campos extra ni parámetros de consulta. Ejecutor y fecha proceden del JWT y del servidor.
- `motivo`: cadena obligatoria de 1 a 500 puntos de código Unicode después de recortar espacios en extremos, conservando saltos internos. Omisión, `null`, tipo incorrecto, vacío/solo espacios o exceso de longitud responden `400` por campo. Es texto libre: `MAXIMO_INTENTOS_ALCANZADO` en el ejemplo es un texto válido, no un catálogo cerrado ni una referencia al catálogo de motivos de fallo.
- `observacion`: cadena opcional de hasta 500 puntos de código Unicode después de recortar extremos; conserva saltos internos. Omisión, `null` o solo espacios se normalizan a `null`; tipo incorrecto o longitud excedida responde `400`. No sobrescribe el comentario del fallo ni la observación de recepción.
- Solicitud nueva: despacho en `FALLIDO`, incidencia/versión vigentes y recepción confirmada de esa incidencia. Se permite con máximo alcanzado/superado, pedido anulado, intentos disponibles o `NO_INTENTADO` sin intentos consumidos; siempre exige la decisión explícita del Gestor.
- Liberación pendiente/de revisión, jornada activa/cerrada, sello alterado, ausencia/fallo de fotografía o caída de Operación no añaden bloqueos. No se consulta Ventas ni su estado comercial como precondición del cierre. No existe cierre automático por esas condiciones.

**Transacción local:** cambiar a `DEVUELTO_A_ORIGEN`, incrementar `despachos.version` e insertar un historial `TRANSICION`, estados `FALLIDO` y `DEVUELTO_A_ORIGEN`, funcionalidad `F-04`, origen `MANUAL`, ejecutor del JWT e instante UTC. Guardar la observación normalizada y `datos.idIncidencia`/`datos.motivoCierre`; el motivo de fallo histórico no cambia. El motivo de cierre no se inserta en `motivo_codigo`, que referencia únicamente el catálogo de fallos.

En ese mismo historial conservar identidad, huella normalizada y respuesta original del comando en metadatos internos durables conforme al modelo; no se agrega una tabla de cierres. Si el despacho es real, registrar un único `DESPACHO_DEVUELTO_A_ORIGEN` en `eventos_salientes`; si es simulado, conservar marca e historial sin evento externo. Estado, versión, historial/resultado y evento se confirman o revierten juntos, con comparación de versión al escribir y unicidad del cierre. No se aceptan efectos parciales ni llamadas externas dentro de la transacción.

Se conservan identidad del despacho/pedido, zona, destino, carga, fecha programada, contador, última incidencia, recepción, referencias históricas y solicitud de liberación. Cerrar no consume intentos, libera otra vez capacidad, reserva carga ni modifica jornadas. Una solicitud de liberación anterior sigue su recuperación por §5.2.1 aunque el despacho ya sea final; no se sustituye por otra reserva.

**Respuesta nueva `200 OK`:** cierre local confirmado; `Cache-Control: no-store`. Todos los campos siguientes son obligatorios; solo los declarados admiten `null`:

| Campo | Tipo | Contenido |
|---|---|---|
| `idDespacho`, `idIncidencia` | Cadenas | Identidades aceptadas. |
| `estado` | Enum | `DEVUELTO_A_ORIGEN`. |
| `versionDespacho` | Entero positivo | Versión posterior a la transición. |
| `motivo` | Cadena | Motivo normalizado del cierre. |
| `observacion` | Cadena o `null` | Observación normalizada de esta decisión. |
| `numeroIntentos` | Entero no negativo | Acumulado conservado. |
| `cerradoEn` | Instante UTC | Instante persistido de la transición y su historial. |
| `idEvento` | Cadena o `null` | Evento registrado para envío; `null` únicamente si es simulado. No acredita entrega a Ventas ni liberación de capacidad. |

Una repetición exacta autorizada del mismo ejecutor devuelve ese mismo `200` y cuerpo originales, incluso después de reiniciar, transcurrir 24 horas o cambiar el estado de envío/liberación. El resultado se reconoce antes de validar las precondiciones actuales; no se reconstruye desde eventos o capacidad actuales ni incrementa nuevamente versión. Otro contenido normalizado o ejecutor con la misma identidad responde `409`. Una identidad nueva sobre un despacho final tampoco permite editar o reemplazar el cierre.

**Orden de evaluación:** autenticación/autorización, formato y normalización, reconocimiento de identidad aceptada y, para una solicitud nueva, existencia, coincidencia incidencia/versión, estado `FALLIDO`, recepción de esa incidencia e integridad local. Dos cierres distintos o cierre/reprogramación/anulación compiten por la versión canónica: solo una mutación confirma sobre esa versión; la perdedora responde `409` y exige nueva consulta/revisión. Un duplicado exacto concurrente recupera el resultado ganador. No se exige agotar intentos para cerrar ni se devuelve `422` por haber alcanzado el máximo.

| HTTP | Código | Efecto |
|---|---|---|
| `400` | `DESP_ERROR_DATOS_CIERRE_INVALIDOS` | Campos ausentes, extra o de tipo/formato/longitud inválidos; `errores` por campo según Común §3.5; sin escrituras. |
| `401` / `403` | Convenciones compartidas | Sin datos ni cambios; autenticar antes de consultar existencia/resultados. |
| `404` | `DESP_ERROR_DESPACHO_NO_ENCONTRADO` | Despacho inexistente. |
| `409` | `DESP_ERROR_OPERACION_REUTILIZADA` | Identidad aceptada con contenido normalizado o ejecutor diferente. |
| `409` | `DESP_ERROR_DESPACHO_DESACTUALIZADO` | Incidencia/versión distintas o comparación de versión fallida al escribir. |
| `409` | `DESP_ERROR_ESTADO_INCOMPATIBLE` | Estado distinto de `FALLIDO` después de comprobar identidad/versión. |
| `409` | `DESP_ERROR_RECEPCION_PENDIENTE` | Sin recepción confirmada de esa incidencia; una recepción anterior no sirve. |
| `500` | `DESP_ERROR_DATOS_INCONSISTENTES` | Referencias locales inválidas o recepción confirmada sin solicitud durable; no inventar otra referencia. |
| `503` | `DESP_ERROR_CIERRE_NO_DISPONIBLE` | No se pudo confirmar el resultado al cliente; consultar antes de repetir exactamente la solicitud original. |

Si se pierde la respuesta, consultar §5.3 antes de recuperar el comando original con la misma identidad/contenido. Una lectura del estado final no demuestra que otro ejecutor aceptó ese mismo comando. Tras `409` se vuelve a consultar y se revisa antes de una decisión nueva; no trasladar automáticamente el motivo a otra incidencia/versión. Un fallo al recargar después de un `200` no convierte el cierre aceptado en rechazo.

**Integración existente con Ventas:** se emite el mismo evento y payload de [Común §7.3](./api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa), con `datos.motivoCierre` igual al motivo normalizado. Se aplica también a cierres logísticos de `NO_INTENTADO` o con anulación ya registrada por F-02; Gestión comunica el hecho y no solicita una segunda cancelación comercial ni inventa una transición a `EN_CAMINO`. El efecto en el pedido pertenece al contrato de Ventas; esta operación no agrega estados/transiciones comerciales, no realiza reembolsos y no espera ese procesamiento para confirmar localmente. RT-03 entrega fuera de la transacción, conserva `idEvento` y expone `PENDIENTE`, `ENVIADO` o `ENVIO_FALLIDO` en §5.3; se mantienen los reintentos y reenvío manual ya acordados.

### 5.3. Consultar el detalle de una incidencia — ES-F04-02

- **Método y ruta:** `GET /api/v1/despachos/{idDespacho}/incidencia`; sin cuerpo ni parámetros de consulta y sin `Idempotency-Key`.
- **Autorización:** JWT humano válido, `tipo=acceso` y rol `GESTOR_DESPACHO`, antes de consultar existencia o datos. Aplican los errores de [Común §3.5](./api-contract.md#35-errores).
- Devuelve `200` si existe una incidencia histórica, aunque el despacho ya no esté `FALLIDO`. Selecciona `despachos.ultima_incidencia_id`, igual que §5.1; no selecciona por contador ni mezcla salidas. Fuera de `FALLIDO` la consulta es histórica y todas las acciones de resolución están bloqueadas.
- Estado, versión, incidencia, recepción, contador, máximo vigente, anulación e historial proceden de una misma lectura consistente de Gestión. Los datos de Operación se componen por su [lectura interna §5.4](./api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias); no se promete una transacción entre servicios.
- Respuestas con `Cache-Control: no-store`. La consulta no modifica datos de negocio, libera reservas, publica eventos ni reenvía comunicaciones.

#### Respuesta `200 OK`

Todos los campos siguientes están presentes. Los identificadores son cadenas opacas; los instantes son ISO 8601 UTC. Solo los campos declarados admiten `null`. La interfaz presenta fechas en `America/Lima`.

| Campo raíz | Tipo | Regla |
|---|---|---|
| `idDespacho`, `codigoRastreoInterno` | Cadenas | Identificación del despacho; el segundo se presenta como código operativo interno. |
| `estado` | Enum de despacho | Estado canónico actual conforme a [Común §6.1](./api-contract.md#61-consultar-por-identificador-de-pedido). |
| `versionDespacho` | Entero positivo | Versión leída; se conserva junto con la identidad de incidencia al iniciar un comando. |
| `actualizadoEn`, `ultimoCambioEstadoEn`, `consultadoEn` | Instantes | Última actualización del despacho, última transición registrada y elaboración de esta respuesta, respectivamente. |
| `numeroIntentos`, `maximoIntentos` | Enteros | Acumulado no negativo y máximo vigente positivo. `NO_INTENTADO` no reinicia ni aumenta el acumulado; contador igual o mayor al máximo bloquea reprogramación. |
| `pedidoAnulado` | Booleano | Derivado de la marca local de F-02; no consulta Ventas. |
| `incidencia` | Objeto | Última incidencia, con el esquema siguiente. |
| `historial` | Arreglo | Historial completo del despacho, sin truncamiento ni paginación en este incremento. |
| `comunicaciones` | Arreglo | Estado local de los eventos salientes del despacho destinados a Ventas. |
| `acciones` | Objeto | Contiene `confirmarRecepcion`, `reprogramar` y `cerrarComoDevueltoAOrigen`. |

| Campo de `incidencia` | Tipo | Regla |
|---|---|---|
| `idIncidencia`, `fechaIncidencia` | Cadena, instante | Identificador del registro enlazado y su `registrado_en`. |
| `motivo` | Objeto | `codigo` y `etiqueta` del catálogo de §4, aunque esté inactivo. |
| `comentario` | Cadena o `null` | Texto registrado; `null` se presenta como `Sin comentario`. |
| `consumeIntento` | Booleano | Condición de esta salida, independiente del acumulado. |
| `repartidor`, `jornada`, `retornoAtrasado` | Objetos y booleano o `null` | Mismos campos, nulabilidad y regla de §5.1, usando las referencias de esta incidencia. |
| `recepcion` | Objeto | `estado`: `PENDIENTE_RETORNO` o `RECIBIDO_EN_CENTRO`; `confirmadaEn`, `idUsuario`, `selloIntacto`, `observacion` y `liberacionCapacidad`. |
| `evidencia` | Objeto | `idEvidencia`: cadena o `null`; `estadoReferencia`: `REFERENCIADA`, `SIN_EVIDENCIA` o `REFERENCIA_AUSENTE`. No contiene fotografía ni URL firmada. |

En recepción pendiente, `confirmadaEn`, `idUsuario`, `selloIntacto` y `observacion` son `null`. En recepción confirmada, son respectivamente un instante UTC, una cadena de identificador, un booleano y una cadena o `null`; `selloIntacto=false` significa No. La recepción pertenece a esta incidencia, no a otra salida del despacho.

`liberacionCapacidad` es `null` antes de recibir. Después es un objeto con `idSolicitud` cadena, `estado` (`PENDIENTE` o `CONFIRMADA`), `requiereRevision` booleano, `actualizadaEn` UTC y `confirmadaEn` UTC o `null`. Pendiente exige `confirmadaEn=null`; confirmada exige fecha no nula y `requiereRevision=false`. Una pendiente muestra `Liberación de capacidad pendiente` o `Liberación de capacidad pendiente de revisión`; solo la confirmada muestra `Capacidad liberada`. Se consulta la solicitud de esa incidencia, incluso en detalle histórico; una recepción ya confirmada sin solicitud durable es inconsistencia local. Estos son estados de sincronización, no estados nuevos del despacho ni motivos adicionales de bloqueo de sus decisiones.

Con identificador de evidencia, `estadoReferencia=REFERENCIADA`: acredita la referencia local, no la disponibilidad de la imagen. Sin identificador y con `NO_INTENTADO`, vale `SIN_EVIDENCIA`; sin identificador en un fallo real, vale `REFERENCIA_AUSENTE`. Ninguno de esos estados de lectura altera el ciclo de vida de la evidencia. La autorización de lectura se solicita por separado a [Operación §3.4](./api-contract-operacion-reparto.md#34-autorizar-la-lectura-de-evidencia).

#### Historial y comunicaciones

Cada entrada de `historial` contiene `id`, `fechaServidor`, `tipoOperacion`, `estadoAnterior`, `estadoNuevo`, `funcionalidadOrigen`, `ejecutorTipo`, `ejecutorId`, `origen`, `motivo`, `observacion` y `datos`. `fechaServidor` es la marca persistida; orden ascendente por ella y desempate por `id` ascendente. No se ordena con la hora del navegador.

- `tipoOperacion`: `TRANSICION`, `REASIGNACION`, `REORDENAMIENTO`, `RECEPCION_EN_CENTRO` o `ANULACION_REGISTRADA`; estados y funcionalidad conservan sus valores canónicos.
- `estadoAnterior` es `null` solo en la creación; `estadoNuevo` siempre existe. Una recepción conserva `FALLIDO` en ambos y se describe como operación, no como un estado nuevo.
- `ejecutorTipo`: `USUARIO`, `SERVICIO` o `SISTEMA`; `ejecutorId` admite `null` para procesos sin identificador. `origen` es `MANUAL` o `AUTOMATICO`; no se inventan nombres de usuario.
- `motivo` es un objeto con `codigo` y `etiqueta` o `null` cuando no aplica; `observacion` es cadena o `null`. `datos` es un objeto de presentación con los campos registrados que correspondan a la operación, definidos a continuación; no se vuelca JSON interno arbitrario.

| Operación registrada | Campos permitidos en `datos`, presentes cuando se registraron |
|---|---|
| Fallo real o `NO_INTENTADO` | `idIncidencia`, `idRepartidor`, `idJornada`, `idReserva`, `consumeIntento`, `numeroIntentos`. Referencias como cadenas; consumo booleano y contador entero. |
| Recepción | `idIncidencia`, `idReserva`, `selloIntacto` booleano, `observacionRecepcion` cadena o `null`. |
| Reprogramación | `idIncidencia`, `nuevaFechaProgramada` como fecha civil `YYYY-MM-DD`. |
| Cierre a origen | `idIncidencia`, `motivoCierre` como cadena. |
| Asignación o reasignación | `idRepartidor`, `idJornada`, `idNuevoRepartidor`, `idNuevaJornada`, según corresponda. |
| Reordenamiento | `despachos`: arreglo de `idDespacho` y `posicion` entera positiva, conforme a §3.2. |

Los valores específicos se recuperan del registro histórico de la operación, nunca del último fallo para rellenar operaciones previas. Las entradas sin datos específicos usan `{}`; observaciones y motivos no aplicables usan `null`.

Cada comunicación contiene `idEvento`, `tipoEvento` y `estadoEnvio` como cadenas, `creadoEn` como instante y `enviadoEn` como instante o `null`. `estadoEnvio` es `PENDIENTE`, `ENVIADO` o `ENVIO_FALLIDO`, con el significado de [Común §7.3](./api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa). Orden por `creadoEn` e `idEvento` ascendentes; sin eventos usa `[]`, incluidos despachos simulados. No se devuelve `payload`, credenciales ni `ultimo_error`. El reenvío manual de RT-03 es una operación transversal separada, fuera de este GET.

#### Acciones, actualización y errores

Cada acción contiene `habilitada` booleano y `motivosBloqueo`, arreglo de códigos sin duplicados. Habilitada exige `[]`; bloqueada exige al menos un código. Se calculan con los datos locales de esta respuesta; no dependen del nombre, de la jornada recuperada ni del éxito del visor.

| Acción | Condición de habilitación en `FALLIDO` | Códigos de bloqueo aplicables |
|---|---|---|
| `confirmarRecepcion` | Recepción pendiente | `RECEPCION_YA_CONFIRMADA` si ya se recibió. |
| `reprogramar` | Recibido, pedido no anulado y contador menor al máximo | `RECEPCION_PENDIENTE`, `PEDIDO_ANULADO`, `MAXIMO_INTENTOS_ALCANZADO`, en ese orden. |
| `cerrarComoDevueltoAOrigen` | Recibido | `RECEPCION_PENDIENTE`. |

Con estado distinto de `FALLIDO`, las tres usan únicamente `ESTADO_NO_FALLIDO` y la UI oculta las acciones. Con recepción pendiente, anulación y límite no habilitan el cierre. Se devuelven todos los motivos aplicables para reprogramar. El texto visible lo presenta la UI; no compara mensajes para decidir permisos.

El cliente conserva `idIncidencia` y `versionDespacho`, compara la identidad al actualizar y descarta respuestas anteriores. Actualiza la vista activa como máximo cada 30 segundos y tras operaciones o `409`; ante fallo de actualización indica datos desactualizados y bloquea acciones hasta renovar. Los comandos de §5.2 reciben esa identidad y versión y vuelven a validar sus propias reglas y concurrencia conforme a Común §9; esta lectura no sustituye esa validación.

| HTTP | Código o tratamiento | Resultado |
|---|---|---|
| `400` | `DESP_ERROR_CONSULTA_INVALIDA` | Cuerpo o parámetros de consulta no admitidos; error normalizado por campo. |
| `401` / `403` | Convenciones compartidas de autenticación/autorización | Sin datos; `401` incluye `WWW-Authenticate: Bearer`. |
| `404` | `DESP_ERROR_DESPACHO_NO_ENCONTRADO` | Despacho inexistente. |
| `404` | `DESP_ERROR_INCIDENCIA_NO_ENCONTRADA` | Despacho existente, fuera de `FALLIDO`, que nunca tuvo incidencia. |
| `500` | `DESP_ERROR_DATOS_INCONSISTENTES` | `FALLIDO` sin incidencia enlazada, referencia rota/de otro despacho o política inválida; sin detalle parcial. |
| `200` degradado | Nombre `null`, jornada `DESCONOCIDA` y aviso en UI | Operación no disponible; no inventa atraso ni nombre y conserva los datos locales. |
| `503` | `DESP_ERROR_CONSULTA_NO_DISPONIBLE` | No puede obtenerse la lectura canónica; no devuelve un falso `404` ni vacío. |

Los fallos al autorizar o cargar la fotografía se resuelven en el visor mediante Operación §3.4 y no sustituyen el resultado de este GET.

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

Al aceptar un fallo, Gestión captura también la reserva de capacidad que ya conserva para la asignación y la vincula de forma inmutable a la incidencia junto con repartidor/jornada. No requiere un identificador de reserva editable enviado por el repartidor. El historial conserva esas referencias, condición de consumo y contador resultante conforme a §5.3. Las operaciones posteriores conservan su propia referencia a la incidencia; así el detalle y la liberación no usan una reserva de una salida posterior.


## 7. APIs de Operación consumidas por Gestión

Las definiciones completas están en [API interna de Operación](./api-contract-operacion-reparto.md#5-api-interna-provista-por-operación): reservas (§5.1), liberaciones (§5.2), proyección de despachos (§5.3) y lectura por lotes de incidencias (§5.4). La [API del repartidor y evidencia](./api-contract-operacion-reparto.md#3-api-de-f-03-operación-del-repartidor) describe el acceso autorizado a fotografías.

El catálogo `/api/v1/catalogos/motivos-fallo` y las operaciones de F-02 `/api/v1/jornadas/{idJornada}/secuencia` y `/api/v1/jornadas/{idJornada}/ruta` pertenecen a Gestión, aunque sus consumidores trabajen con repartidores o jornadas. El Gateway debe respetar esta propiedad por operación; el resto de jornadas y la evidencia pertenecen a Operación. Esta división documental no modifica la configuración desplegada.

## 8. Integraciones externas implementadas o consumidas

Las entradas de módulos externos se implementan en Gestión y conservan su definición única en el contrato externo: [cotización y Productos](./api-contract.md#5-f-01-cotización-para-marketplace-y-chatbot), [seguimiento](./api-contract.md#6-rt-04-seguimiento-para-marketplace-y-chatbot) y [creación, cancelación y eventos de Ventas](./api-contract.md#7-f-02-integración-con-ventas-y-postventa). La validación de identidad y los clientes técnicos siguen [Seguridad](./api-contract.md#8-integración-con-seguridad-y-usuarios).

La reorganización no acredita endpoints implementados ni pruebas de contrato. Las especificaciones funcionales y su evidencia mantienen el estado real de cada operación.
