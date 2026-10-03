# ES-F02-01: Recepción de solicitudes de despacho

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Módulo de Ventas y Postventa (token de servicio)

## 1. Objetivo

Recibir, validar e incorporar de forma segura e idempotente en el Módulo de Despacho las solicitudes de entrega a domicilio emitidas por el módulo de Ventas y Postventa cuando un pedido ha sido pagado y su paquete está sellado en el centro de despacho. El sistema resuelve la zona de cobertura mediante F-01, crea el despacho en estado inicial `PENDIENTE_ASIGNACION`, asigna los códigos únicos de operación y rastreo y responde de inmediato con la confirmación.

## 2. Actor y precondiciones

- El sistema llamante se autentica mediante un token de servicio JWT emitido por Seguridad y Usuarios con el scope `despachos:crear` y audiencia `aud=api-despacho`.
- El pedido correspondiente se encuentra pagado, preparado y sellado físicamente en el centro de despacho de la tienda.
- La solicitud contiene los datos obligatorios del pedido: identificador del pedido, datos del destinatario, dirección física de entrega, peso, volumen, cantidad de paquetes físicos y fecha comprometida.
- El servicio de Zonas Geográficas (F-01) se encuentra disponible para la resolución del destino.

## 3. Flujo principal

1. Ventas y Postventa invoca el endpoint `POST /api/v1/despachos` enviando la información del pedido sellado junto a su token de servicio.
2. El backend de Despacho valida la autenticidad del token, el scope `despachos:crear` y el formato de los datos recibidos.
3. El sistema comprueba de forma atómica si ya existe un despacho registrado con ese `idPedido`.
4. Si no existe, invoca la resolución de cobertura de F-01 a partir del distrito o código postal de destino.
5. Al verificar que el destino está dentro de una zona activa, el sistema genera un código operativo interno único y un código de rastreo (ej. `TRK-XXXXX`).
6. El sistema crea la entidad despacho con estado `PENDIENTE_ASIGNACION`, asigna la zona resuelta, establece la fecha programada igual a la fecha comprometida e inicia el contador de intentos en cero.
7. Se persiste el despacho y su registro de auditoría inicial de forma transaccional.
8. El backend responde `201 Created` con el identificador del despacho, código de rastreo, estado y zona asignada.

## 4. Reglas y validaciones

- **Datos requeridos:** `idPedido`, destinatario (nombre completo, teléfono de contacto), dirección de destino (dirección, distrito), peso en kilogramos (decimal mayor a 0), volumen en metros cúbicos (decimal mayor a 0), cantidad de paquetes (entero mayor o igual a 1) y fecha comprometida (formato ISO-8601).
- **Datos opcionales:** coordenadas geográficas (latitud, longitud) y referencias domiciliarias.
- **Resolución de cobertura:** el destino debe corresponder a una zona de cobertura en estado `ACTIVO` en F-01. Si el destino no cuenta con cobertura activa, la solicitud se rechaza con `422 Unprocessable Entity` y el código de error `DESP_ERROR_SIN_COBERTURA`.
- **Idempotencia:** si el sistema recibe una solicitud con un `idPedido` para el cual ya existe un despacho creado, no genera un duplicado ni altera el registro existente; responde `200 OK` con los datos del despacho previo y su estado actual.
- **Estado inicial:** todo despacho nuevo nace estrictamente en estado `PENDIENTE_ASIGNACION`.
- **Generación de códigos:** se asigna un código operativo interno único y un código de rastreo alfanumérico público para consulta de los canales de venta.

## 5. Entradas, salidas e integraciones

### Entradas

- Payload JSON con la estructura definida en `integraciones/api-contract.md`:
  - `idPedido` (alfanumérico, ej. `PED-2026-00891`).
  - `destinatario`: `nombre`, `telefono`, `correo` (opcional).
  - `destino`: `direccion`, `distrito`, `codigoPostal` (opcional), `referencia` (opcional), `coordenadas` (opcional).
  - `datosFisicos`: `pesoKg`, `volumenM3`, `cantidadPaquetes`.
  - `fechaComprometida`: fecha en formato `YYYY-MM-DD`.
- Encabezado `Authorization: Bearer <token_servicio>`.

### Salidas

- Respuesta HTTP `201 Created` con los datos del despacho creado:
  - `idDespacho`: identificador único interno.
  - `codigoRastreo`: código para seguimiento.
  - `estado`: `PENDIENTE_ASIGNACION`.
  - `idZona`: zona de cobertura asignada.
  - `fechaProgramada`: fecha de entrega inicial.
- Respuesta HTTP `200 OK` en caso de reintento idempotente.
- Errores normalizados `400 Bad Request`, `401 Unauthorized`, `403 Forbidden` o `422 Unprocessable Entity`.

### Integraciones

- **Ventas y Postventa:** emite la solicitud de entrega al confirmar el paquete sellado.
- **Zonas y Cotizador (F-01):** resuelve la zona de cobertura mediante el distrito o código postal.
- **Seguridad y Usuarios:** valida la firma y vigencia del token de servicio.
- Las rutas, formatos y códigos siguen exclusivamente `integraciones/api-contract.md` (Sección 7).

## 6. Criterios de aceptación

### CA-01. Recepción exitosa con cobertura activa

- **DADO** que Ventas y Postventa envía una solicitud completa con un `idPedido` no registrado previamente y un destino ubicado en una zona activa de F-01.
- **CUANDO** se procesa la petición con un token de servicio válido con scope `despachos:crear`.
- **ENTONCES** el sistema crea el despacho en `PENDIENTE_ASIGNACION`, genera el código operativo y de rastreo, fija la fecha programada igual a la comprometida, registra la auditoría y retorna `201 Created`.

### CA-02. Rechazo por destino sin cobertura activa

- **DADO** una solicitud cuyo destino no coincide con ninguna zona de cobertura activa en F-01.
- **CUANDO** la solicitud es evaluada por el backend.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con código `DESP_ERROR_SIN_COBERTURA`, no persiste ningún despacho y detalla la causa.

### CA-03. Solicitud repetida para el mismo pedido (idempotencia)

- **DADO** que ya existe un despacho registrado para el pedido `PED-2026-00891`.
- **CUANDO** Ventas y Postventa vuelve a enviar una solicitud con el mismo `idPedido`.
- **ENTONCES** el sistema no crea un nuevo despacho, no duplica registros y responde `200 OK` retornando el despacho existente con su estado actual.

### CA-04. Rechazo por datos incompletos o inconsistentes

- **DADO** una solicitud donde falta la dirección, o con peso, volumen o cantidad de paquetes menor o igual a cero.
- **CUANDO** es validada por el sistema.
- **ENTONCES** el sistema responde `400 Bad Request`, especifica los campos inválidos y no persiste registros parciales.

### CA-05. Petición sin permisos requeridos

- **DADO** una solicitud enviada sin token, con token expirado o sin el scope `despachos:crear`.
- **CUANDO** se procesa la solicitud.
- **ENTONCES** el sistema responde `401 Unauthorized` o `403 Forbidden` y no procesa la orden.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Cobro y facturación del envío (responsabilidad de Ventas y Postventa).
- Preparación y sellado físico del paquete (ocurre en el almacén previo a la solicitud).
- Asignación a repartidor o definición de ruta (corresponde a ES-F02-04 y ES-F02-05).

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-01 y RF-05).
- Contrato de API: `integraciones/api-contract.md` (Sección 7).
- Requisito transversal de estados: `arquitectura/diagrama-estados-despacho.md`.
