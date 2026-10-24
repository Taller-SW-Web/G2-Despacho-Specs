# Contrato de API: Operación de Reparto y Flota

## 1. Propósito y propiedad

Contrato del microservicio `servicio-operacion-reparto`, proveedor de F-03, F-05 y F-06: operación del repartidor, perfiles locales, furgonetas, jornadas, reservas, proyección móvil y evidencias. Sus rutas públicas se consumen por el API Gateway; las rutas `/internal/v1` son privadas.

## 2. Convenciones y contratos relacionados

Aplican las [convenciones compartidas](./api-contract.md#3-convenciones-comunes), [Seguridad y Usuarios](./api-contract.md#8-integración-con-seguridad-y-usuarios) y [reglas de idempotencia y concurrencia](./api-contract.md#9-reglas-de-idempotencia-y-concurrencia) del contrato externo. La administración de perfiles, vehículos y jornadas requiere `GESTOR_DESPACHO`; la operación de campo verifica el perfil local y la propiedad del recurso conforme a §3. Las APIs privadas requieren credencial de servicio y no se publican en el Gateway.

El estado canónico del despacho pertenece a [Gestión de Despachos](./api-contract-gestion-despachos.md). Operación solicita las transiciones y conserva únicamente su proyección confirmada; no modifica la base de Gestión. La identidad humana se resuelve por `sub` contra un perfil local activo y vinculado; no se exige el rol global `REPARTIDOR`.

## 3. API de F-03: operación del repartidor

Todos los recursos requieren un JWT humano con `tipo=acceso`. En las rutas `/repartidor/`, el backend toma el `sub`, resuelve el perfil local de repartidor vinculado y comprueba que esté activo; el cliente no puede elegir otro `idRepartidor`. No se exige un rol global `REPARTIDOR` ni un claim `idRepartidor`. La lectura de evidencia admite también al Gestor conforme a §3.5, sin exigirle perfil de repartidor.

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
| `GET` | `/api/v1/repartidor/motivos-fallo` | Consultar los motivos seleccionables en campo |
| `POST` | `/api/v1/evidencias/{idEvidencia}/acceso` | Obtener URL firmada de lectura |

Los comandos que cambian estado requieren `Idempotency-Key` UUID v4. La misma clave con el mismo contenido devuelve el resultado original; con otra operación o contenido responde `409` con `DESP_ERROR_CLAVE_REUTILIZADA`. Las consultas no requieren clave. La clave pertenece al `sub` autenticado; un rechazo definitivo (`4xx`) la libera, de modo que repetirla vuelve a validar y obtiene el mismo rechazo, mientras que un `503` la conserva para reintentar sin duplicar la transición.

### 3.1. Consultar ruta, detalle y resumen

`GET /api/v1/repartidor/mi-ruta` devuelve la jornada activa de hoy en `America/Bogota`. Si no hay jornada activa, responde `200` con `idJornada: null`, `estadoOperativo: "FUERA_DE_TURNO"` y `despachos: []`. La lista respeta la secuencia de F-02.

```json
{
  "idJornada": "d42d8d4b-1a80-481f-9f35-9ff0c6c935f1",
  "fecha": "2026-10-17",
  "estadoOperativo": "DISPONIBLE",
  "despachos": [{
    "idDespacho": "854e7b68-394e-4e5f-9ccf-5350d7d4e3e8",
    "codigoRastreoInterno": "TRK-001",
    "estado": "ASIGNADO",
    "secuenciaRuta": 1,
    "fechaProgramada": "2026-10-17",
    "numeroIntentos": 0,
    "maximoIntentos": 2,
    "destinatario": "Ana Mendoza",
    "direccion": "Av. Ejemplo 123",
    "distrito": "Centro",
    "motivoFallo": null,
    "hitos": {
      "asignadoEn": "2026-10-17T13:12:00Z",
      "enCaminoEn": null,
      "entregadoEn": null,
      "fallidoEn": null
    }
  }]
}
```

La ruta no entrega teléfono. Nombre y dirección solo se incluyen para `ASIGNADO` y `EN_CAMINO`; para otros estados se serializan como `null`. `maximoIntentos` procede de `MAXIMO_INTENTOS` en Gestión; proyecciones creadas antes de incorporar ese dato pueden devolverlo como `null` hasta recibir una proyección actualizada.

`GET /api/v1/repartidor/despachos/{idDespacho}` acepta un UUID y devuelve únicamente despachos de la jornada activa propia. Para `ASIGNADO` y `EN_CAMINO` devuelve destinatario y destino completos; para otros estados, ambos campos son `null`. Un despacho ajeno, no existente o de otra jornada responde `404` sin datos parciales.

`motivoFallo` es el código del catálogo de Gestión para un `FALLIDO` (incluido `NO_INTENTADO`) y `null` en otro caso; no es un dato personal y se entrega en todos los estados. `hitos` contiene las marcas del ciclo vigente informadas por Gestión, en UTC: `asignadoEn` (asignación de F-02), `enCaminoEn`, `entregadoEn` y `fallidoEn`. Siguen el orden asignado < en camino < entregado o fallido; un hito aún no ocurrido es `null`. Tras una reprogramación no se muestran hitos de salidas anteriores. Proyecciones creadas antes de incorporar estos campos pueden devolver `hitos: null`. La UI presenta las horas en `America/Lima`.

`GET /api/v1/repartidor/jornada/resumen` devuelve la jornada de hoy, incluso si ya está cerrada (ampliado para F-03, pantalla 11 de Figma):

```json
{
  "idJornada": "d42d8d4b-1a80-481f-9f35-9ff0c6c935f1",
  "fecha": "2026-10-17",
  "estadoJornada": "CERRADA",
  "cerradaEn": "2026-10-17T23:05:00Z",
  "asignados": 4,
  "entregados": 2,
  "fallidosConIntento": 0,
  "noIntentados": 2,
  "pendientes": 0,
  "paquetesPorDevolver": [{
    "idDespacho": "6f0c1d2e-3a4b-4c5d-8e9f-0a1b2c3d4e5f",
    "codigoRastreoInterno": "TRK-78910",
    "direccion": "Calle Los Pinos 345",
    "distrito": "San Isidro",
    "motivoFallo": "NO_INTENTADO"
  }]
}
```

- `fallidosConIntento` cuenta los `FALLIDO` con motivo distinto de `NO_INTENTADO`; `noIntentados`, los `FALLIDO` con `NO_INTENTADO`. Para proyecciones previas sin motivo se conserva la regla anterior, basada en el contador.
- `paquetesPorDevolver` lista los despachos `FALLIDO` de la jornada, con o sin intento consumido, porque el paquete regresa físicamente con el repartidor. Es la única excepción a la omisión de datos personales: incluye dirección y distrito, sin destinatario ni teléfono, para que el repartidor identifique cada paquete en el centro. La confirmación de recepción sigue perteneciendo a F-04.
- `estadoJornada` (`ACTIVA`/`CERRADA`) y `cerradaEn` (UTC o `null`) provienen de la jornada. Sin jornada responde `idJornada: null`, contadores en cero y lista vacía.

Las consultas responden con `Cache-Control: no-store`. La bandeja de regularización de jornadas anteriores es una lectura separada, de solo lectura y sin datos personales ni acciones; no forma parte de `mi-ruta` y su endpoint queda pendiente de implementación.

`GET /api/v1/repartidor/motivos-fallo` devuelve `{ "motivos": [...] }` con la forma del [catálogo de Gestión §4](./api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo), filtrada a `activo=true` y `seleccionableEnCampo=true`. Operación lo obtiene de Gestión con su credencial técnica después de validar el perfil de campo; no mantiene una copia propia. Si Gestión no responde: `503` con `DESP_ERROR_GESTION_NO_DISPONIBLE`, y la UI no fabrica motivos.

#### 3.1.1. Comandos y su coordinación con Gestión

El inicio de traslado, §3.3, §3.4 y §3.6 siguen el mismo procedimiento:

1. Registrar la clave del `sub` (tabla `comandos_repartidor`). Una clave completada devuelve la respuesta original.
2. En el primer intento, validar localmente perfil activo, jornada activa de hoy, propiedad y estado de origen en la proyección; para entrega y fallo, verificar además la evidencia (§3.2). Un reintento de una clave en proceso omite estas validaciones, porque la proyección pudo actualizarse con el resultado original.
3. Solicitar la transición a [Gestión §6.1](./api-contract-gestion-despachos.md#61-operación-solicita-una-transición-a-gestión) fuera de toda transacción local, reenviando la misma clave. Gestión aplica la máquina de estados bajo su bloqueo y es idempotente por clave.
4. Aplicar la respuesta a la proyección por versión, asociar la evidencia y completar la clave.

Errores comunes: `400` `DESP_ERROR_CAMPOS_INVALIDOS` (falta `Idempotency-Key` UUID v4 o el cuerpo no cumple), `403` sin perfil de campo, `404` `DESP_ERROR_DESPACHO_NO_ENCONTRADO` (ajeno o de otra jornada), `409` `DESP_ERROR_FUERA_DE_TURNO` (sin jornada activa), `409` `DESP_ERROR_ESTADO_INCOMPATIBLE` o `DESP_ERROR_DESPACHO_REASIGNADO` (el despacho cambió: la UI informa y actualiza la ruta) y `503` `DESP_ERROR_GESTION_NO_DISPONIBLE` (no se registró; reintentar con la misma clave). Si Gestión no responde en 1,5 s se trata como `503` (ES-F03-04 RN-09).

#### 3.1.2. Iniciar traslado

`POST /api/v1/repartidor/despachos/{idDespacho}/inicio-traslado`, sin cuerpo. Solo desde `ASIGNADO`; no modifica el contador. Responde `200` con el detalle de §3.1 en `EN_CAMINO`, con `hitos.enCaminoEn`.

### 3.2. Autorizar la carga de evidencia

```json
{
  "idDespacho": "854e7b68-394e-4e5f-9ccf-5350d7d4e3e8",
  "tipo": "ENTREGA",
  "contentType": "image/jpeg",
  "tamanioBytes": 845120
}
```

```json
{
  "idEvidencia": "f7d6a0fc-6546-4a57-a2c2-a944f8d2f98b",
  "urlCarga": "https://storage.example/signed-upload",
  "venceEn": "2026-09-23T19:25:00Z"
}
```

La fotografía se carga directamente al bucket privado. La API recibe después solamente `idEvidencia`; no recibe imágenes Base64.

Se aceptan `image/jpeg`, `image/png` e `image/webp`, hasta 2.097.152 bytes (2 MiB) por archivo. El bucket privado debe imponer los mismos tipos y límite. El endpoint valida los metadatos declarados para autorizar la carga; no comprime la imagen ni elimina EXIF.
Los identificadores `idDespacho` e `idEvidencia` de esta operación son UUID. La autorización exige el despacho propio en `EN_CAMINO` dentro de la jornada activa.

La app del repartidor reduce la foto antes de solicitar la autorización (lado mayor 1600 px, JPEG con calidad de 0,8 a 0,5 hasta quedar bajo 2 MiB) y la sube con `PUT` a `urlCarga` con su `Content-Type`. Re-codificar la imagen descarta los metadatos EXIF, incluida la ubicación. Esta decisión pertenece al cliente; el backend sigue sin comprimir y solo valida.

Antes de asociar una evidencia a una entrega o un fallo, Operación comprueba que pertenezca al mismo despacho, `sub` y tipo (`ENTREGA` o `FALLO`), que siga `AUTORIZADA` o `CARGADA`, y que el objeto exista en el bucket con un tipo y tamaño permitidos e igual al tipo autorizado (ES-F03-05 RN-03). Si el objeto aún no existe responde `409` `DESP_ERROR_EVIDENCIA_NO_CARGADA` sin cambiar el estado; si no corresponde o incumple la política, `400` `DESP_ERROR_EVIDENCIA_INVALIDA`; si el almacenamiento no responde, `503` `DESP_ERROR_EVIDENCIA_NO_DISPONIBLE`. Tras la transición aceptada, la evidencia queda `ASOCIADA`.

### 3.3. Registrar entrega

`POST /api/v1/repartidor/despachos/{idDespacho}/entrega`

```json
{
  "idEvidencia": "f7d6a0fc-6546-4a57-a2c2-a944f8d2f98b",
  "recibidoPor": "Ana Mendoza"
}
```

Solo desde `EN_CAMINO`. `idEvidencia` (UUID) es obligatorio; `recibidoPor` es opcional, hasta 120 caracteres. No modifica el contador. Responde `200` con el detalle de §3.1 en `ENTREGADO`, ya sin destinatario ni destino, con `hitos.entregadoEn`. Gestión solicita después la liberación de la reserva por §5.2 con motivo `ENTREGA` (ES-F03-05 RN-06).

No se captura firma ni geolocalización.

### 3.4. Registrar fallo

`POST /api/v1/repartidor/despachos/{idDespacho}/fallo`

```json
{
  "motivo": "CLIENTE_AUSENTE",
  "comentario": "No respondieron al teléfono",
  "idEvidencia": "0c4b1f62-77d2-4d1e-9a39-5b2f0e8c6a10"
}
```

Solo desde `EN_CAMINO`. `motivo` e `idEvidencia` son obligatorios; `comentario` es opcional, hasta 200 caracteres. Gestión incrementa el contador una sola vez al aceptar la transición. Responde `200` con el detalle de §3.1 en `FALLIDO`, con `motivoFallo`, `numeroIntentos` actualizado y `hitos.fallidoEn`. La reserva se conserva hasta la recepción en centro (F-04). Un motivo inexistente, inactivo o no seleccionable responde `400` `DESP_ERROR_MOTIVO_INVALIDO`.

Motivos permitidos para el repartidor:

- `CLIENTE_AUSENTE`.
- `DIRECCION_NO_UBICADA`.
- `RECHAZO_DEL_PAQUETE`.
- `DATOS_DE_CONTACTO_ERRONEOS`.
- `ZONA_INACCESIBLE`.
- `PAQUETE_DANADO`.

`NO_INTENTADO` es exclusivo del cierre manual o automático de jornada.

### 3.5. Autorizar la lectura de evidencia

- **Método y ruta:** `POST /api/v1/evidencias/{idEvidencia}/acceso`, sin cuerpo ni parámetros de consulta; no requiere `Idempotency-Key`.
- **Autorización:** JWT humano válido y rol `GESTOR_DESPACHO`, o perfil local de repartidor activo vinculado al `sub` y propietario del despacho en la proyección de Operación. No exige jornada abierta para leer evidencia. Autenticación y permisos se comprueban antes de devolver referencias o URLs.
- **Precondición:** evidencia `ASOCIADA` al despacho; no permite visualizar cargas pendientes de asociación. El Gestor puede consultar evidencia histórica aunque el despacho ya no esté `FALLIDO`.
- **Respuesta `200`:** objeto con `idEvidencia`, `idDespacho`, `urlLectura` y `venceEn`, todos obligatorios. Identificadores como cadenas, URL HTTPS firmada para lectura del objeto privado e instante de vencimiento en UTC.
- La vigencia se obtiene de `VIGENCIA_URL_FIRMADA_SEGUNDOS` de Operación (valor inicial `300` en el modelo de datos). `venceEn` corresponde al enlace emitido, no al vencimiento de una carga sin asociar. Una renovación vuelve a validar permisos y genera una URL nueva; no cambia el estado de evidencia, despacho ni historial de negocio.
- La respuesta incluye `Cache-Control: no-store`. No expone credenciales, una URL pública permanente ni un campo de ruta interna. La URL firmada es el único acceso temporal que se entrega; no se registra en logs, almacenamiento del navegador ni evidencia de pruebas.
- El frontend vincula la respuesta al despacho e identificador solicitados; una respuesta de un recurso anterior se descarta. Al cerrar el visor, cambiar de despacho/incidencia o perder autorización, retira imagen y URL.
- El vencimiento o fallo de imagen no se presenta como ausencia de fotografía. Se ofrece renovar/reintentar explícitamente, sin bucles de renovación ni construir rutas públicas. El error permanece dentro del visor y conserva el resto del detalle autorizado.

| HTTP | Código o tratamiento | Significado |
|---|---|---|
| `400` | `DESP_ERROR_CONSULTA_INVALIDA` | Cuerpo o parámetros no admitidos. |
| `401` / `403` | [Común §3.5](./api-contract.md#35-errores) | Token no aceptado o usuario sin autorización; no entrega URL. |
| `404` | `DESP_ERROR_EVIDENCIA_NO_ENCONTRADA` | Referencia de evidencia inexistente u objeto eliminado; no se sustituye por otra fotografía. |
| `409` | `DESP_ERROR_EVIDENCIA_NO_ASOCIADA` | La evidencia existe, pero aún no quedó asociada; permite reintentar. |
| `503` | `DESP_ERROR_EVIDENCIA_NO_DISPONIBLE` | No puede autorizarse/comprobarse la lectura por indisponibilidad temporal. |

El almacenamiento deniega accesos sin firma válida y enlaces vencidos. Un fallo de descarga se distingue en UI de los errores HTTP de esta autorización; `Volver a cargar` ejecuta nuevamente esta operación.

### 3.6. Cerrar la jornada propia

`POST /api/v1/repartidor/jornada/cierre` con `Idempotency-Key` y cuerpo `{ "idJornada": "<UUID>" }`. La jornada debe pertenecer al perfil del `sub` (`403` en otro caso).

Cada despacho `ASIGNADO` o `EN_CAMINO` se resuelve primero en Gestión como `FALLIDO` con motivo `NO_INTENTADO`, sin fotografía ni incremento del contador, con origen manual y el repartidor como ejecutor (ES-F03-07). Cada solicitud usa una clave derivada de forma estable de la clave del cierre y del despacho, de modo que un reintento no duplica transiciones. Después se cierra la jornada como en §4.2.1 y responde `200` con el recurso Jornada. Si algún despacho no pudo resolverse responde `503` y la jornada sigue abierta: se reintenta con la misma clave. Una jornada ya cerrada devuelve su estado sin cambios. El corte automático de fin de turno sigue pendiente de implementación.


## 4. API de F-05 y F-06: perfiles, flota y jornadas

### 4.1. Repartidores y furgonetas

Operación es propietaria del catálogo F-05 y de su auditoría. Todas las operaciones de esta sección requieren un JWT de acceso con rol `GESTOR_DESPACHO`; las escrituras obtienen del `sub` UUID la identidad del actor. Los tokens de servicio no sustituyen este permiso.

| Método | Ruta | Resultado exitoso |
|---|---|---|
| `GET` | `/api/v1/repartidores` | `200`, página de repartidores |
| `POST` | `/api/v1/repartidores` | `201`, repartidor creado y `Location` |
| `GET` | `/api/v1/repartidores/{idRepartidor}` | `200`, repartidor |
| `PUT` | `/api/v1/repartidores/{idRepartidor}` | `200`, repartidor actualizado |
| `PATCH` | `/api/v1/repartidores/{idRepartidor}/estado` | `204`, baja lógica; no permite reactivación |
| `PUT` | `/api/v1/repartidores/{idRepartidor}/vinculacion` | `204`, asociación manual de cuenta existente |
| `GET` | `/api/v1/furgonetas` | `200`, página de furgonetas |
| `POST` | `/api/v1/furgonetas` | `201`, furgoneta creada y `Location` |
| `PUT` | `/api/v1/furgonetas/{idFurgoneta}` | `200`, furgoneta con límites actualizados |
| `PATCH` | `/api/v1/furgonetas/{idFurgoneta}/estado` | `204`, cambio de estado confirmado |

#### 4.1.1. Consultas y paginación

- `pagina`: entero entre 1 y 2147483647; valor predeterminado 1.
- `tamanoPagina`: entero entre 1 y 100; valor predeterminado 50. La UI ofrece 20, 50 y 100.
- Filtros de repartidores: `estadoRegistro` (`ACTIVO`, `INACTIVO`), `estadoVinculacion` (`PENDIENTE`, `VINCULADO`) y `turnoHabitual` (`MANANA`, `TARDE`, `COMPLETO`).
- Filtros de furgonetas: `estado` (`DISPONIBLE`, `EN_MANTENIMIENTO`, `FUERA_DE_SERVICIO`) y `placa` de hasta diez caracteres. La búsqueda de placa es una coincidencia literal sin distinguir mayúsculas.
- Los filtros se combinan. Una consulta vacía devuelve `contenido=[]`, `totalElementos=0` y `totalPaginas=0`; no se transforma un error en un catálogo vacío.
- El orden es `creado_en` descendente e identificador como desempate; el contenido y el total se leen de forma consistente.
- La página solicitada se conserva en la respuesta, incluso si queda fuera del total. El frontend puede consultar la última página disponible.

La respuesta contiene `contenido`, `pagina`, `tamanoPagina`, `totalElementos` y `totalPaginas`. Esta última es el redondeo superior de total/tamaño, con cero para un catálogo vacío. Cada elemento utiliza el recurso definido a continuación.

#### 4.1.2. Repartidor

| Campo | Tipo y validación | Uso |
|---|---|---|
| `idRepartidor` | UUID | Solo respuesta y ruta |
| `nombres`, `apellidos` | Texto obligatorio, máximo 80 caracteres por campo | Alta; no editables |
| `dni` | Texto de ocho dígitos, único | Alta; no editable |
| `telefono` | Texto obligatorio, máximo 20 caracteres, mínimo seis dígitos; admite `+` inicial, espacios, paréntesis y guiones | Alta y edición |
| `correo` | Correo válido obligatorio, máximo 120 caracteres; único sin distinguir mayúsculas | Alta y edición; se almacena normalizado |
| `numeroBrevete` | Texto obligatorio, máximo 20 caracteres | Alta y edición |
| `turnoHabitual` | `MANANA`, `TARDE`, `COMPLETO` | Alta y edición |
| `estadoRegistro` | `ACTIVO`, `INACTIVO` | Respuesta; el alta usa `ACTIVO` |
| `estadoVinculacion` | `PENDIENTE`, `VINCULADO` | Respuesta; el alta usa `PENDIENTE` |
| `usuarioId` | UUID o `null` | Respuesta; `null` antes de la asociación |

El alta recibe los siete campos de datos personales/contacto/turno; la edición recibe únicamente teléfono, correo, brevete y turno, todos obligatorios. Los campos ajenos al comando se rechazan, incluidos DNI, nombres o estados en una edición. No se almacenan contraseñas.

El alta es local y no solicita crear una cuenta remota: una vez autorizado el JWT, su persistencia no depende de invocar la provisión de usuarios. El registro permanece pendiente hasta que el Gestor asocia el identificador comunicado por Seguridad.

#### 4.1.3. Vinculación manual y baja local

La vinculación recibe exclusivamente:

```json
{"usuarioId":"2f31c1b1-7568-41b8-bf91-342db68431df"}
```

La cuenta debe haber sido creada por el canal administrativo de Seguridad, conforme al [contrato externo §8.4](./api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor). El módulo asocia el UUID localmente y no prueba por sí mismo la activación remota de la cuenta.

- Perfil activo y pendiente: guarda el identificador único y cambia a `VINCULADO`, con auditoría.
- Mismo identificador ya asociado al mismo perfil activo: `204` sin duplicar auditoría.
- Cuenta ya asociada a otro perfil, cambio de cuenta sobre un perfil vinculado o perfil inactivo: `409`.
- UUID inválido o ausente: `400`. Perfil inexistente: `404`.
- No existen los estados locales `PENDIENTE_ACTIVACION` o `ERROR`, ni un comando de creación automática o reintento de provisión en F-05.
- `REPARTIDOR` no es un rol global: el acceso de campo utiliza el `sub` para comprobar un perfil local `ACTIVO` y `VINCULADO`.

La baja recibe `{"estado":"INACTIVO"}`. Si ya está inactivo, responde `204` sin otro cambio ni auditoría. Conserva identidad, vínculo e historial; no desactiva la cuenta global.

La baja rechaza despachos locales `ASIGNADO`/`EN_CAMINO` o reservas de capacidad activas, aunque la proyección falte o una jornada histórica ya figure cerrada. Si no hay carga, cierra las jornadas activas vacías y da de baja en una sola transacción. Las restricciones de persistencia impiden abrir jornadas con perfiles inactivos o pendientes; el filtro de campo deniega las rutas `/api/v1/repartidor/**` a perfiles no habilitados. Esto no reemplaza la comprobación de propiedad de cada entrega ni implementa las operaciones de F-03/F-06.

#### 4.1.4. Furgoneta y límites persistibles

| Campo | Tipo y validación | Uso |
|---|---|---|
| `idFurgoneta` | UUID | Solo respuesta y ruta |
| `placa` | Texto obligatorio, máximo diez caracteres, único sin distinguir mayúsculas | Alta; se almacena en mayúsculas y no se edita |
| `estado` | `DISPONIBLE`, `EN_MANTENIMIENTO`, `FUERA_DE_SERVICIO` | Respuesta; alta en `DISPONIBLE` |
| `capacidadPesoKg` | Número mayor que cero, máximo 9999999.999 y tres decimales | Alta y edición |
| `capacidadVolumenM3` | Número mayor que cero, máximo 999999.9999 y cuatro decimales | Alta y edición |
| `maximoPaquetes` | Entero entre 1 y 32767 | Alta y edición |

No se redondea silenciosamente una capacidad que exceda la precisión: se rechaza con `400`. La edición recibe únicamente las tres capacidades y conserva placa y estado. Solo cambia el maestro; las instantáneas de jornadas existentes se mantienen, y F-06 debe tomar el maestro al abrir futuras jornadas.

El cambio de estado recibe únicamente `estado`. Las transiciones son `DISPONIBLE → EN_MANTENIMIENTO/FUERA_DE_SERVICIO`, `EN_MANTENIMIENTO → DISPONIBLE/FUERA_DE_SERVICIO` y `FUERA_DE_SERVICIO → DISPONIBLE`. Solicitar el mismo estado es idempotente; pasar directamente de fuera de servicio a mantenimiento se rechaza con `409`.

Un retiro a mantenimiento o fuera de servicio comprueba despachos y reservas como la baja del repartidor. Sin carga, cierra las jornadas activas vacías en la misma transacción; con carga responde `409` sin cambiar vehículo ni jornada. El estado operativo fuera de turno se deriva del cierre, cuya presentación corresponde a F-06.

La API usa `FUERA_DE_SERVICIO`. Su valor persistido es `INACTIVA`, conforme al modelo de datos; esa traducción pertenece al adaptador JDBC y no crea un estado nuevo para el consumidor.

#### 4.1.5. Auditoría, errores y recepción

Las mutaciones y su auditoría se confirman o revierten juntas, con identidad del JWT, estados anterior/nuevo e instante UTC. No se duplica auditoría ante la repetición idempotente del estado o vínculo. La comprobación de carga se serializa con los escritores de jornadas/reservas/proyecciones; los fallos de acceso a datos no se interpretan como ausencia de carga.

Se usa [Problem Details del contrato externo §3.5](./api-contract.md#35-errores). La validación de campos puede incluir `errores` con `campo` y `motivo`; no se devuelve SQL ni información privada en los errores.

| HTTP | Código | Situación |
|---|---|---|
| `400` | `DESP_ERROR_CAMPOS_INVALIDOS` | Campos, tipos, estados, parámetros o formato no válidos |
| `401` | `DESP_ERROR_TOKEN_INVALIDO` | Token ausente o no aceptado |
| `403` | `DESP_ERROR_SCOPE_INSUFICIENTE` | Sin rol o perfil habilitado |
| `403` | `DESP_ERROR_IDENTIDAD_INVALIDA` | Actor de escritura sin `sub` UUID utilizable |
| `404` | `DESP_ERROR_RECURSO_NO_ENCONTRADO` | Perfil o vehículo inexistente |
| `409` | `DESP_ERROR_CONFLICTO_FLOTA` | Duplicado, transición inválida, carga pendiente o vínculo incompatible |
| `503` | `DESP_ERROR_OPERACION_NO_DISPONIBLE` | No puede completarse la operación o comprobarse el perfil local |

El frontend confirma el resultado con la respuesta válida y la consulta posterior. Ante timeout, `5xx` o respuesta no verificable después de una mutación, conserva el formulario y exige consultar el estado antes de repetir. Los estados futuros desconocidos se presentan sin habilitar transiciones que el cliente no conoce.

### 4.2. Jornadas y monitoreo

Proveedor F-06: Operación. Las rutas administrativas requieren JWT `tipo=acceso`, rol `GESTOR_DESPACHO` y `sub` UUID para mutaciones. Los identificadores del proveedor son UUID. El Gateway enruta `/api/v1/jornadas/**`, `/api/v1/flota/**` y `/api/v1/repartidores/disponibles` a Operación.

| Método | Ruta | Resultado |
|---|---|---|
| `POST` | `/api/v1/jornadas` | `201` con jornada creada y `Location` |
| `GET` | `/api/v1/jornadas/{idJornada}` | `200` con jornada, ocupación y despachos proyectados |
| `POST` | `/api/v1/jornadas/{idJornada}/cierre` | `200` con cierre confirmado, idempotente |
| `GET` | `/api/v1/flota/monitoreo` | `200` con página, resumen global e instante de consulta |
| `GET` | `/api/v1/repartidores/disponibles` | `200`, objeto `repartidores` con candidatos |
| `GET` | `/api/v1/repartidor/jornada` | `200`, contexto propio; requiere perfil activo/vinculado, sin rol global ficticio |
| `POST` | `/api/v1/repartidor/jornada/cierre` | `200`, cierre propio sin pendientes; F-03 resuelve antes los pendientes |

#### 4.2.1. Apertura y cierre

La apertura recibe exclusivamente `idRepartidor`, `idFurgoneta`, `idZona` (UUID) y `fecha` ISO. La fecha debe ser hoy en `America/Bogota`, obtenida del servidor. La zona se comprueba por `GET /api/v1/zonas/{idZona}` de Gestión, propagando el JWT humano por HTTPS fuera de la transacción; solo una respuesta válida con ese identificador y `id` coincidente y `estado=ACTIVO` habilita la apertura. Una caída no demuestra zona activa.

Se exige perfil activo/vinculado, vehículo disponible y ausencia de otra jornada activa del mismo recurso, incluso de fecha anterior; también se rechaza carga histórica reservada pendiente de liberar. Se guardan las capacidades del vehículo como instantánea. Creación y auditoría son atómicas. La UI no reenvía automáticamente una apertura incierta: consulta antes el estado.

El cierre administrativo no recibe cuerpo. Rechaza despachos `ASIGNADO`/`EN_CAMINO` y reservas activas todavía sin una proyección terminal confirmada con `409`; F-03 es responsable de resolver sus pendientes como `NO_INTENTADO` antes del cierre. Conserva reservas de retornos y proyecciones, no reabre turnos ni inventa liberaciones. Repetir un cierre devuelve el primer resultado sin cambiar instante ni duplicar auditoría. La existencia de una reserva histórica activa impide reutilizar el recurso hasta su liberación confirmada.

Jornada: `idJornada`, `idRepartidor`, `idFurgoneta`, `placa`, `idZona`, `fecha`, `estado` (`ACTIVA`/`CERRADA`), `cerradaEn` (UTC o null), `limites`, `ocupacion`, `capacidadRemanente`, `porcentajeOcupacion`. Las tres capacidades usan `{pesoKg, volumenM3, paquetes}`. Los porcentajes usan `{peso, volumen, paquetes}` y no se recortan silenciosamente a 100. El detalle agrega `despachos` con `idDespacho`, `estado` y `secuenciaRuta`, sin exponer teléfonos o direcciones en el monitoreo.

#### 4.2.2. Consultas y estado derivado

Monitoreo acepta `fecha` ISO (hoy por defecto), `pagina` desde 1, `tamanoPagina` de 1 a 100 (50 por defecto), `estadoOperativo` opcional y `idZona` UUID opcional. Devuelve `contenido`, `pagina`, `tamanoPagina`, `totalElementos`, `totalPaginas`, `resumen` y `consultadoEn` UTC. Cada fila tiene `idRepartidor`, `nombre`, `estadoOperativo` y `jornada` (objeto anterior o null). Incluye los perfiles locales activos; el resumen `{disponible,enRuta,saturado,fueraDeTurno}` cuenta el conjunto completo de fecha/zona antes de filtrar por estado y paginar. No se agrega un total a partir de una sola página. Una jornada activa de fecha anterior debe cerrarse antes de reutilizar el recurso.

Ocupación suma exclusivamente reservas `ACTIVA`, incluidas las de paquetes fallidos pendientes de retorno o sincronización. Remanente = límite menos ocupación, sin fabricar capacidad cuando faltan datos. Prioridad del estado: sin jornada activa `FUERA_DE_TURNO`; cualquier límite alcanzado `SATURADO`; si no, algún despacho `EN_CAMINO` implica `EN_RUTA`; en otro caso `DISPONIBLE`.

Disponibilidad acepta `fecha` e `idZona`; devuelve únicamente jornadas de esa fecha que estén activas con perfil activo/vinculado, vehículo disponible y remanente positivo en las tres dimensiones. Cada candidato tiene `idRepartidor`, `idJornada`, `nombre`, `idZona`, `idFurgoneta`, `placa`, `estadoOperativo`, `limites`, `ocupacion`, `capacidadRemanente` y `porcentajeOcupacion`. Sin candidatos devuelve `{"repartidores":[]}`. Esta lectura no reserva capacidad; F-02 debe confirmar mediante §5.1. Objetivo de respuesta menor de 200 ms, pendiente de medición identificada.

El contexto propio devuelve `idRepartidor`, `estadoOperativo` y `jornada` activa de hoy o null. El cierre propio recibe exclusivamente `{"idJornada":"UUID"}` obtenido del contexto consultado; resuelve el perfil por `sub` y verifica la propiedad de esa jornada. Repetir el cierre de una jornada anterior no cierra una nueva jornada del mismo repartidor. No recibe identificadores de usuario y rechaza jornadas ajenas con `403`.

#### 4.2.3. Errores y actualización de UI

Usar Problem Details común: `400 DESP_ERROR_CAMPOS_INVALIDOS`; `401/403` de Seguridad; `404 DESP_ERROR_JORNADA_NO_ENCONTRADA`; `409 DESP_ERROR_CONFLICTO_JORNADA` por recursos ocupados/carga/pendientes; `422 DESP_ERROR_RECURSO_NO_APTO` por perfil, zona o fecha no aptos; `503 DESP_ERROR_OPERACION_NO_DISPONIBLE` por dependencia o datos no disponibles. No retornar SQL ni mensajes remotos sin filtrar.

El tablero actualiza cada 30 segundos mientras sea visible, cancela/descarta solicitudes obsoletas y permite actualización manual. Un fallo de refresco conserva los datos previos identificados como desactualizados y bloquea mutaciones; una pérdida de autorización los retira. Tras mutar, confirma respuesta y consulta nuevamente; una salida incierta exige reconciliar antes de repetir.

## 5. API interna provista por Operación

Estas rutas las implementa Operación y las consume Gestión con credencial de servicio. No se exponen mediante el Gateway.

### 5.1. Gestión consulta y reserva capacidad en Operación

Autorización: JWT de servicio con `sub=modulo-despacho`, audiencia `api-despacho` y scope `operacion:capacidad:reservar`. Su concesión real depende de Seguridad. Los identificadores reales son UUID y las cargas positivas respetan precisión de tres decimales para peso, cuatro para volumen y paquetes enteros hasta 32767. Solo se reserva en jornada de hoy activa y perfil habilitado/vehículo disponible. La operación se serializa con F-05, aperturas, cierres y liberaciones.

La repetición con la misma clave y contenido devuelve el resultado original persistido, aun si luego se liberó la reserva. Cambiar despacho, repartidor, jornada o carga con esa clave responde `409 DESP_ERROR_CLAVE_REUTILIZADA`. El resultado es durable; no se recalcula un remanente diferente para una repetición. Un perfil/jornada no habilitados responde `409 DESP_ERROR_REPARTIDOR_NO_HABILITADO`.

- **Método:** `POST`
- **Ruta:** `/internal/v1/capacidad/reservas`
- **Idempotencia:** `Idempotency-Key` obligatorio, UUID v4 generado y conservado por Gestión para cada operación de asignación. Repetir clave y contenido devuelve la reserva original; otra carga con esa clave responde `409`. Operación conserva esa clave con la reserva incluso liberada, no solo en caché temporal. Una salida/asignación nueva usa otra clave; `idDespacho` garantiza una sola reserva activa, no una única reserva para toda la vida del despacho.

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

Una capacidad insuficiente responde `422` con `DESP_ERROR_CAPACIDAD_EXCEDIDA`. Si otra operación intenta reservar un despacho cuya reserva anterior sigue activa, responde `409` con `DESP_ERROR_RESERVA_ANTERIOR_ACTIVA`, sin crear otra reserva ni reutilizarla como éxito de una asignación nueva. Una repetición reconocida por su clave se resuelve antes de esa comprobación. La cancelación, reasignación, entrega o recepción debe liberar o actualizar su reserva de manera idempotente; una reserva liberada no se reactiva para una salida nueva.

### 5.2. Gestión libera una reserva en Operación

Autorización: JWT de servicio con `sub=modulo-despacho`, audiencia `api-despacho` y scope `operacion:capacidad:liberar`; su concesión real sigue pendiente. La operación usa el mismo orden de bloqueo que las reservas y F-05.

- **Método:** `POST`
- **Ruta:** `/internal/v1/capacidad/reservas/{idReserva}/liberacion`
- **Idempotencia:** `idReserva`; repetir la liberación devuelve el resultado vigente.

```json
{
  "motivo": "RECEPCION_EN_CENTRO",
  "idDespacho": "DSP-100234"
}
```

Los motivos iniciales son `ENTREGA`, `CANCELACION`, `RECEPCION_EN_CENTRO`, `REASIGNACION` y `COMPENSACION`. Con `RECEPCION_EN_CENTRO`, Gestión invoca esta operación únicamente después de persistir el retorno físico y su solicitud durable conforme a [Gestión §5.2.1](./api-contract-gestion-despachos.md#521-confirmar-recepción-en-centro--es-f04-03).

- Validar credencial técnica y existencia de `idReserva`; comprobar que su despacho coincide con `idDespacho`. No buscar ni sustituir otra reserva si la referencia no coincide.
- Si está `ACTIVA`, marcarla `LIBERADA` en una transacción local con motivo y fecha del servidor; peso, volumen y paquetes se obtienen de esa reserva. Si ya está liberada, devolverla sin alterar fecha, motivo ni ocupación por segunda vez.
- Respuesta `200`: `idReserva`, `idDespacho`, `estado=LIBERADA`, `motivoLiberacion` y `liberadaEn`, todos obligatorios; identificadores/motivo como cadenas y fecha UTC. Conserva los datos de la primera liberación, aunque otro motivo posterior solicite liberar la misma reserva ya liberada.
- `400` por datos inválidos, `401/403` por credencial técnica, `404` con `DESP_ERROR_RESERVA_NO_ENCONTRADA`, `409` con `DESP_ERROR_RESERVA_NO_COINCIDE` si pertenece a otro despacho y `503` con `DESP_ERROR_OPERACION_NO_DISPONIBLE` ante indisponibilidad. Aplicar Común §3.5; ningún rechazo libera otra reserva.
- F-06 calcula ocupación con reservas `ACTIVA`: no anticipa una liberación por recibir `FALLIDO`, cerrar jornada o consultar el detalle. Tras la liberación confirmada refleja el resultado en la siguiente consulta, sin reabrir ni modificar jornadas.

### 5.3. Gestión comunica el estado confirmado a Operación

Autorización: JWT de servicio con `sub=modulo-despacho`, audiencia `api-despacho` y scope `operacion:proyecciones:escribir`. Respuesta `204` para versión nueva, repetida o anterior; las dos últimas no sobrescriben datos. `409 DESP_ERROR_PROYECCION_INCOMPATIBLE` si reserva, jornada o despacho no coinciden. `400` por formato inválido y `503` por indisponibilidad. Una proyección terminal no libera una reserva por sí sola: se confirma §5.2.

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
  "maximoIntentos": 2,
  "motivoFallo": null,
  "hitos": { "asignadoEn": "2026-09-23T19:10:00Z" },
  "version": 2,
  "actualizadoEn": "2026-09-23T19:10:00Z"
}
```

`motivoFallo` (código del catálogo o `null`) y `hitos` (`asignadoEn`, `enCaminoEn`, `entregadoEn`, `fallidoEn`, cada uno UTC u omitido) son opcionales por compatibilidad: Gestión los envía desde F-03 y Operación conserva `null` cuando faltan. Un `FALLIDO` del cierre llega con `motivoFallo: "NO_INTENTADO"`; Operación no usa un estado `NO_INTENTADO`.

Al asignar o reasignar se envía la información completa necesaria para la ruta móvil. En cambios posteriores puede enviarse el mismo esquema actualizado. La proyección no es el estado canónico: una versión repetida se ignora y una versión anterior nunca reemplaza una posterior.

### 5.4. Gestión consulta repartidores y jornadas de incidencias

- **Método y ruta:** `POST /internal/v1/operacion/consulta-incidencias`.
- **Proveedor:** Operación de Reparto y Flota; consumidor autorizado: Gestión de Despachos, con credencial de servicio conforme a Gestión §6, Operación §5. No se expone en el Gateway. Referencia: [Gestión](./api-contract-gestion-despachos.md#6-api-interna-provista-por-gestión), [Operación](./api-contract-operacion-reparto.md#5-api-interna-provista-por-operación).
- Es una lectura por lotes; no modifica datos ni requiere clave de idempotencia.
- Autorización interna: JWT válido con `tipo=servicio`, `sub=modulo-despacho`, audiencia `api-despacho` y scope `operacion:incidencias:leer`. Es un permiso de la comunicación interna de G2; su concesión en Seguridad real debe configurarse en ese entorno. No acredita una concesión ya confirmada por G7 ni habilita otros scopes.
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
