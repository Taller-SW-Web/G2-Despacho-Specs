# ES-F02-01: Recepción de solicitudes de despacho

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Módulo de Ventas y Postventa (token de servicio)

## 1. Objetivo

Recibir, validar e incorporar de forma segura e idempotente en el Módulo de Despacho las solicitudes de entrega a domicilio emitidas por el módulo de Ventas y Postventa cuando un pedido está pagado, preparado y listo para entrega. El sistema resuelve la zona de cobertura mediante F-01, obtiene de Productos y Ofertas los datos físicos vigentes de las líneas del pedido, calcula el peso y el volumen totales y la fecha programada, crea el despacho en estado inicial `PENDIENTE_ASIGNACION` con un paquete lógico, asigna los códigos únicos de operación y rastreo y responde de inmediato con la confirmación.

## 2. Actor y precondiciones

- El sistema llamante se autentica mediante un token de servicio JWT emitido por Seguridad y Usuarios con `sub=modulo-ventas`, el scope `despachos:crear` y audiencia `aud=api-despacho`; la solicitud exige además un encabezado `Idempotency-Key` con un UUID v4.
- La llamada declara que el pedido correspondiente está pagado, preparado y listo para entrega; Despacho no consulta el estado interno del pedido en Ventas.
- La solicitud contiene los datos obligatorios del pedido: identificador del pedido, datos del destinatario, destino y las líneas del pedido con `sku` y `cantidad`. Ventas y Postventa no envía peso, volumen, cantidad de paquetes ni fecha comprometida.
- El servicio de Zonas Geográficas (F-01) se encuentra disponible para la resolución del destino.
- Productos y Ofertas se encuentra disponible para la consulta en lote de los datos físicos vigentes de cada SKU; el módulo utiliza su propio token de servicio con el scope `productos:fisicos:leer`.

## 3. Flujo principal

1. Ventas y Postventa invoca el endpoint `POST /api/v1/despachos` enviando el pedido listo para entrega con destinatario, destino y líneas (`sku`, `cantidad`), junto a su token de servicio y su `Idempotency-Key`.
2. El backend de Despacho valida la autenticidad del token, el scope `despachos:crear`, la clave de idempotencia y el formato de los datos recibidos.
3. El sistema comprueba de forma atómica si ya existe un despacho registrado con ese `idPedido` o con esa clave de idempotencia.
4. Si no existe, invoca la resolución de cobertura de F-01 a partir del distrito o código postal de destino.
5. Con zona activa resuelta, el sistema agrupa los SKU repetidos de las líneas y consulta en lote a Productos y Ofertas los datos físicos vigentes de cada SKU, con su propio token de servicio.
6. El sistema calcula `pesoTotalKg` y `volumenTotalM3` a partir de los datos físicos recibidos; si un SKU no existe, faltan datos físicos válidos o Productos y Ofertas no está disponible, se responde el error correspondiente y no se crea el despacho.
7. Al verificar cobertura y datos físicos válidos, el sistema genera un código operativo interno único y un código de rastreo (ej. `TRK-XXXXX`).
8. El sistema crea la entidad despacho con estado `PENDIENTE_ASIGNACION`, asigna la zona resuelta, registra la cantidad de paquetes en `1` (paquete lógico del alcance inicial), calcula la fecha programada a partir de la zona, el plazo aplicable y el calendario operativo e inicia el contador de intentos en cero.
9. Se persiste el despacho y su registro de auditoría inicial de forma transaccional.
10. El backend responde `201 Created` con el identificador del despacho, el pedido, el código de rastreo, el estado, la zona asignada y la fecha programada.

## 4. Reglas y validaciones

- **Datos requeridos:** `idPedido`, destinatario (nombre completo, teléfono de contacto), destino (dirección, distrito) y al menos una línea con `sku` obligatorio y `cantidad` mayor que cero.
- **Datos opcionales:** código postal, referencias domiciliarias y coordenadas geográficas (latitud, longitud).
- **Datos que no se reciben:** peso, volumen, cantidad de paquetes y fecha comprometida no forman parte de la solicitud; el sistema los obtiene o los calcula conforme a las reglas siguientes.
- **Datos físicos:** antes de persistir el despacho, el sistema consulta en lote a Productos y Ofertas los datos físicos vigentes de cada SKU y calcula `pesoTotalKg` y `volumenTotalM3`. Un SKU no reconocido responde `422 Unprocessable Entity` con `DESP_ERROR_PRODUCTO_NO_ENCONTRADO`; un producto sin peso mayor a cero o sin dimensiones válidas responde `422 Unprocessable Entity` con `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`; si Productos y Ofertas no está disponible, se responde `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE`. En ninguno de los tres casos se crea el despacho.
- **Cantidad de paquetes:** para el alcance inicial, cada pedido representa un despacho y un paquete lógico; el sistema registra internamente `cantidadPaquetes = 1` y no existe una entrada que lo modifique.
- **Fecha programada:** el sistema calcula la fecha de entrega a partir de la zona resuelta, el plazo aplicable y el calendario operativo; no se recibe ni se copia una fecha comprometida.
- **Resolución de cobertura:** el destino debe corresponder a una zona de cobertura en estado `ACTIVO` en F-01. Si el destino no cuenta con cobertura activa, la solicitud se rechaza con `422 Unprocessable Entity` y el código de error `DESP_ERROR_SIN_COBERTURA`.
- **Idempotencia:** la solicitud exige un `Idempotency-Key` con un UUID v4. Si el sistema recibe una solicitud con un `idPedido` para el cual ya existe un despacho creado, no genera un duplicado ni altera el registro existente; responde `200 OK` con los datos del despacho previo y su estado actual.
- **Estado inicial:** todo despacho nuevo nace estrictamente en estado `PENDIENTE_ASIGNACION`.
- **Generación de códigos:** se asigna un código operativo interno único y un código de rastreo alfanumérico público para consulta de los canales de venta.

## 5. Entradas, salidas e integraciones

### Entradas

- Payload JSON con la estructura definida en `integraciones/api-contract.md`:
  - `idPedido` (alfanumérico, ej. `PED-2026-00891`).
  - `destinatario`: `nombre`, `telefono`.
  - `destino`: `direccion`, `distrito`, `codigoPostal` (opcional), `referencia` (opcional), `coordenadas` (opcional).
  - `lineas`: arreglo con al menos un elemento; cada uno con `sku` obligatorio y `cantidad` mayor que cero.
- Encabezados `Authorization: Bearer <token_servicio>` e `Idempotency-Key: <uuid v4>`.

### Salidas

- Respuesta HTTP `201 Created` con los datos del despacho creado:
  - `idDespacho`: identificador único interno.
  - `idPedido`: pedido atendido.
  - `codigoRastreoInterno`: código para seguimiento.
  - `estado`: `PENDIENTE_ASIGNACION`.
  - `idZona`: zona de cobertura asignada.
  - `fechaProgramada`: fecha de entrega calculada por el sistema.
  - `creadoEn`: marca temporal de creación.
- Respuesta HTTP `200 OK` en caso de reintento idempotente, con el despacho existente.
- Errores normalizados `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `422 Unprocessable Entity` o `503 Service Unavailable`.

### Integraciones

- **Ventas y Postventa:** emite la solicitud de entrega cuando el pedido está pagado, preparado y listo para entrega.
- **Zonas y Cotizador (F-01):** resuelve la zona de cobertura mediante el distrito o código postal.
- **Productos y Ofertas:** provee en lote el peso y las dimensiones vigentes de cada SKU; los datos siguen siendo de su propiedad.
- **Seguridad y Usuarios:** valida la firma y vigencia del token de servicio y emite el token propio que el módulo utiliza contra Productos y Ofertas.
- Las rutas, formatos y códigos siguen exclusivamente `integraciones/api-contract.md` (Sección 7).

## 6. Criterios de aceptación

### CA-01. Recepción exitosa con cobertura activa

- **DADO** que Ventas y Postventa envía una solicitud completa con un `idPedido` no registrado previamente, líneas con `sku` y `cantidad` válidos y un destino ubicado en una zona activa de F-01, y Productos y Ofertas devuelve los datos físicos vigentes de cada SKU.
- **CUANDO** se procesa la petición con un token de servicio válido con scope `despachos:crear` y un `Idempotency-Key` válido.
- **ENTONCES** el sistema consulta los datos físicos en lote, calcula el peso y el volumen totales, registra la cantidad de paquetes en `1`, calcula la fecha programada a partir de la zona y el calendario operativo, crea el despacho en `PENDIENTE_ASIGNACION`, genera el código operativo y de rastreo, registra la auditoría y retorna `201 Created`.

### CA-02. Rechazo por destino sin cobertura activa

- **DADO** una solicitud cuyo destino no coincide con ninguna zona de cobertura activa en F-01.
- **CUANDO** la solicitud es evaluada por el backend.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con código `DESP_ERROR_SIN_COBERTURA`, no persiste ningún despacho y detalla la causa.

### CA-03. Solicitud repetida para el mismo pedido (idempotencia)

- **DADO** que ya existe un despacho registrado para el pedido `PED-2026-00891`.
- **CUANDO** Ventas y Postventa vuelve a enviar una solicitud con el mismo `idPedido`.
- **ENTONCES** el sistema no crea un nuevo despacho, no duplica registros y responde `200 OK` retornando el despacho existente con su estado actual.

### CA-04. Rechazo por datos incompletos o inconsistentes

- **DADO** una solicitud sin distrito, sin líneas, con una línea sin `sku` o con una `cantidad` menor o igual a cero.
- **CUANDO** es validada por el sistema.
- **ENTONCES** el sistema responde `400 Bad Request`, especifica los campos inválidos y no persiste registros parciales.

### CA-05. Petición sin permisos requeridos

- **DADO** una solicitud enviada sin token, con token expirado o sin el scope `despachos:crear`.
- **CUANDO** se procesa la solicitud.
- **ENTONCES** el sistema responde `401 Unauthorized` o `403 Forbidden` y no procesa la orden.

### CA-06. Rechazo por datos físicos no disponibles

- **DADO** una solicitud con un `sku` que Productos y Ofertas no reconoce o sin peso o dimensiones válidos, o con Productos y Ofertas temporalmente no disponible.
- **CUANDO** el sistema intenta obtener los datos físicos de las líneas antes de persistir el despacho.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con `DESP_ERROR_PRODUCTO_NO_ENCONTRADO` o `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`, o `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE`, respectivamente, y no crea el despacho.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Cobro y facturación del envío (responsabilidad de Ventas y Postventa).
- Preparación y sellado físico del paquete (ocurre en el almacén previo a la solicitud).
- Asignación a repartidor o definición de ruta (corresponde a ES-F02-04 y ES-F02-05).

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-01 y RF-05).
- Contrato de API: `integraciones/api-contract.md` (Sección 7).
- Requisito transversal de estados: `arquitectura/diagrama-estados-despacho.md`.
