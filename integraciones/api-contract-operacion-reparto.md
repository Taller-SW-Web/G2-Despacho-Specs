# Contrato de API: Operación de Reparto y Flota

## 1. Propósito y propiedad

Contrato del microservicio `servicio-operacion-reparto`, proveedor de F-03, F-05 y F-06: operación del repartidor, perfiles locales, furgonetas, jornadas, reservas, proyección móvil y evidencias. Sus rutas públicas se consumen por el API Gateway; las rutas `/internal/v1` son privadas.

## 2. Convenciones y contratos relacionados

Aplican las [convenciones compartidas](./api-contract.md#3-convenciones-comunes), [Seguridad y Usuarios](./api-contract.md#8-integración-con-seguridad-y-usuarios) y [reglas de idempotencia y concurrencia](./api-contract.md#9-reglas-de-idempotencia-y-concurrencia) del contrato externo. La administración de perfiles, vehículos y jornadas requiere `GESTOR_DESPACHO`; la operación de campo verifica el perfil local y la propiedad del recurso conforme a §3. Las APIs privadas requieren credencial de servicio y no se publican en el Gateway.

El estado canónico del despacho pertenece a [Gestión de Despachos](./api-contract-gestion-despachos.md). Operación solicita las transiciones y conserva únicamente su proyección confirmada; no modifica la base de Gestión.

## 3. API de F-03: operación del repartidor

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
| `POST` | `/api/v1/evidencias/{idEvidencia}/acceso` | Obtener URL firmada de lectura |

Los comandos de transición deben ser idempotentes. Se recomienda enviar `Idempotency-Key`; su obligatoriedad como encabezado común aún debe acordarse.

### 3.1. Autorizar la carga de evidencia

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

### 3.2. Registrar entrega

```json
{
  "idEvidencia": "EVI-92812",
  "recibidoPor": "Ana Mendoza"
}
```

No se captura firma ni geolocalización.

### 3.3. Registrar fallo

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


## 4. API de F-05 y F-06: perfiles, flota y jornadas

### 4.1. Repartidores y furgonetas

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

### 4.2. Jornadas y monitoreo

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

## 5. API interna provista por Operación

Estas rutas las implementa Operación y las consume Gestión con credencial de servicio. No se exponen mediante el Gateway.

### 5.1. Gestión consulta y reserva capacidad en Operación

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

### 5.2. Gestión libera una reserva en Operación

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

### 5.3. Gestión comunica el estado confirmado a Operación

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

### 5.4. Gestión consulta repartidores y jornadas de incidencias

- **Método y ruta:** `POST /internal/v1/operacion/consulta-incidencias`.
- **Proveedor:** Operación de Reparto y Flota; consumidor autorizado: Gestión de Despachos, con credencial de servicio conforme a Gestión §6, Operación §5. No se expone en el Gateway. Referencia: [Gestión](./api-contract-gestion-despachos.md#6-api-interna-provista-por-gestión), [Operación](./api-contract-operacion-reparto.md#5-api-interna-provista-por-operación).
- Es una lectura por lotes; no modifica datos ni requiere clave de idempotencia.
- Cuerpo obligatorio: `idsRepartidor` e `idsJornada`, arreglos de identificadores opacos únicos, de `0` a `100` elementos cada uno; al menos uno debe contener elementos. Elementos vacíos, duplicados, límites excedidos o campos desconocidos responden `400` con el formato de Común §3.5. Referencia: [Convenciones e integración externa](./api-contract.md#35-errores).

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

Gestión deduplica las jornadas de todas las incidencias pendientes de retorno de la base definida en Gestión §5.1 y las consulta en lotes de hasta 100 antes de filtrar atrasados o paginar. Así no calcula ese indicador con una sola página. Para los nombres basta consultar los repartidores de la página devuelta. Si solo faltan nombres, conserva filas y totales. No se efectúa una petición por fila ni se consultan tablas de Operación desde Gestión. Referencia: [Gestión](./api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01).

Cada lote obtenido aporta su `consultadoEn`. Una omisión o respuesta incoherente se trata como dato desconocido para los elementos afectados. Un timeout o indisponibilidad del servicio convierte en desconocidos los elementos del lote no obtenido y aplica la degradación de Gestión §5.1; no se usa como confirmación una copia antigua de una jornada activa. Si Operación no puede ejecutar su lectura, responde `503` con `code=DESP_ERROR_OPERACION_NO_DISPONIBLE`. Las credenciales inválidas se rechazan según Común §3.5; Gestión no omite la autenticación ni expone errores internos al usuario. Referencia: [Gestión](./api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01), [Convenciones e integración externa](./api-contract.md#35-errores).


## 6. APIs de Gestión e integraciones externas consumidas

Operación utiliza el [catálogo común de motivos](./api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo) para F-03 y solicita las [transiciones canónicas](./api-contract-gestion-despachos.md#61-operación-solicita-una-transición-a-gestión). El catálogo es de Gestión; el formulario del repartidor filtra los motivos activos seleccionables en campo, sin una segunda definición del endpoint.

El reordenamiento y la consulta de ruta administrativa de F-02 se documentan en [programación y asignación de Gestión](./api-contract-gestion-despachos.md#32-programación-y-asignación), aunque utilicen identificadores de jornada. Las demás operaciones de jornada de §4.2 son provistas por Operación.

Las comunicaciones con [Seguridad y Usuarios](./api-contract.md#8-integración-con-seguridad-y-usuarios), incluidos usuario vinculado y eventos de usuario, se definen en el contrato externo. Los eventos logísticos hacia Ventas son responsabilidad de Gestión y se describen en [integración con Ventas](./api-contract.md#73-eventos-salientes-hacia-ventas-y-postventa).

La reorganización no acredita endpoints implementados ni pruebas de contrato. Las especificaciones funcionales y su evidencia mantienen el estado real de cada operación.
