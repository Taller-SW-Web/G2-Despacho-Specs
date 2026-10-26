# ES-F02-01: Recepción de solicitudes de despacho

**Funcionalidad padre:** [F-02 — Programación y asignación de despachos](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-01 y RF-05.

**Responsable:** Tarqui.

**Estado:** Backend implementado y verificado localmente; integración con proveedores reales pendiente. Ver [evidence.md](./evidence.md).

**Actor principal:** Módulo de Ventas y Postventa (token de servicio).

**Servicio propietario:** Gestión de Despachos.

**UI:** No aplica una interfaz web ni un cambio visual directo. La recepción es una integración externa de servicio a servicio mediante API REST invocada por Ventas y Postventa; la ausencia de `ui.md` se justifica también en [plan.md](./plan.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md). Preparación del 16/10/2026 sobre la especificación funcional de F-02; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

Todos los pedidos de la tienda se preparan en un único centro de despacho. Cuando un pedido ya fue pagado y su paquete está sellado y listo en ese centro, el módulo de Ventas y Postventa solicita a Despacho su entrega a domicilio. A partir de esa solicitud nace la entidad despacho en estado `PENDIENTE_ASIGNACION` ("En centro de despacho").

El objetivo es recibir, validar e incorporar de forma segura, atómica e idempotente en el Módulo de Despacho las solicitudes de entrega emitidas por Ventas y Postventa. El sistema resuelve la zona de cobertura mediante F-01, consulta en lote a Productos y Ofertas los datos físicos vigentes de las líneas del pedido, calcula el peso y el volumen totales y la fecha programada de entrega, crea el despacho con un paquete lógico (`cantidadPaquetes = 1`), asigna códigos únicos de operación y rastreo y responde de inmediato con la confirmación [cite: 1].

## 2. Alcance

- Incluye: validación sintáctica y de negocio del payload; autenticación con token de servicio y scope `despachos:crear`; validación de clave de idempotencia (`Idempotency-Key`); resolución de zona activa con F-01; consulta en lote de datos físicos a Productos y Ofertas; cálculo de peso total, volumen total y fecha programada; creación de entidad despacho en `PENDIENTE_ASIGNACION`; asignación de código operativo y código de rastreo; registro de auditoría inicial (RT-02).
- Fuera de alcance: asignación de repartidor o jornada (ES-F02-04); creación de turnos o furgonetas (F-05); preparación física o sellado del bulto (operación previa de almacén); cobros o facturación comercial (Ventas y Postventa).

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- El sistema emisor se autentica mediante token de servicio JWT emitido por Seguridad y Usuarios con `sub=modulo-ventas`, `aud=api-despacho` y el scope `despachos:crear`.
- La petición incluye un encabezado obligatorio `Idempotency-Key` con formato UUID v4 de hasta 128 caracteres.
- La llamada declara que el pedido correspondiente está pagado, preparado y listo para entrega; Despacho no consulta el estado interno del pedido en Ventas.
- La solicitud contiene identificador de pedido (`idPedido`), datos del destinatario (`nombre`, `telefono`), destino (`direccion`, `distrito`) y un arreglo `lineas` con al menos un elemento (`sku` no vacío y `cantidad` entera positiva).
- Ventas y Postventa no envía peso, volumen, cantidad de paquetes ni fecha comprometida.
- El servicio de Zonas Geográficas (F-01) se encuentra disponible y el destino debe pertenecer a una zona en estado `ACTIVO`.
- El servicio de Productos y Ofertas se encuentra disponible para la consulta en lote de los datos físicos vigentes de cada SKU (`productos:fisicos:leer`).

### 3.2. Dependencias

- **Ventas y Postventa:** emite la solicitud de entrega según [api-contract.md §7.1](../../integraciones/api-contract.md#71-crear-un-despacho-para-un-pedido-listo-para-entrega).
- **Zonas y Cotizador (F-01):** resuelve la zona de cobertura a partir del distrito o código postal.
- **Productos y Ofertas:** provee peso y dimensiones vigentes por SKU según [api-contract.md §5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas).
- **Seguridad y Usuarios:** valida firma y claims del token entrante y emite token para consultar Productos.
- **Cola de pendientes (ES-F02-03):** expone el despacho persistido a los gestores de despacho.
- **Trazabilidad (ES-F02-08 / RT-02):** persiste el registro inicial de creación.

### 3.3. Resultados

- Solicitud válida: despacho creado en estado `PENDIENTE_ASIGNACION`, código operativo interno único (ej. `DSP-100234`), código de rastreo (ej. `TRK-78901`), zona resuelta, peso y volumen calculados, `cantidadPaquetes = 1`, fecha programada calculada, auditoría registrada y respuesta `201 Created`.
- Solicitud repetida para el mismo `idPedido`: respuesta `200 OK` con el despacho existente, sin duplicar registros.
- Destino sin zona activa: respuesta `422 Unprocessable Entity` con código `DESP_ERROR_SIN_COBERTURA`.
- SKU desconocido o sin datos físicos válidos: respuesta `422 Unprocessable Entity` con `DESP_ERROR_PRODUCTO_NO_ENCONTRADO` o `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`.
- Productos y Ofertas no disponible: respuesta `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE`.

## 4. Flujo principal y alternativas

1. Ventas y Postventa invoca `POST /api/v1/despachos` enviando el pedido listo para entrega con encabezados de autorización e `Idempotency-Key`.
2. Gestión de Despachos valida el token JWT, el scope `despachos:crear` y la presencia de `Idempotency-Key`.
3. Valida la estructura del payload (datos obligatorios de destinatario, destino y líneas válidas).
4. Verifica de forma atómica en base de datos si ya existe un despacho registrado con ese `idPedido` o `Idempotency-Key`.
5. Si no existe, invoca la resolución de cobertura de F-01 a partir del distrito o código postal.
6. Con zona activa confirmada, agrupa los SKU de las líneas y consulta en lote a Productos y Ofertas los datos físicos vigentes (`pesoKg`, `dimensiones`).
7. Calcula `pesoTotalKg` como la suma de `pesoUnitario * cantidad` y `volumenTotalM3` como la suma de `volumenUnitario * cantidad`.
8. Registra internamente `cantidadPaquetes = 1` y calcula `fechaProgramada` a partir de la zona, el plazo aplicable y el calendario operativo.
9. Genera el código interno (`DSP-XXXXXX`) y el código de rastreo (`TRK-XXXXX`).
10. Persiste el despacho y su registro de auditoría inicial de forma transaccional.
11. Responde `201 Created` con el recurso creado.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Reintento idempotente | Ya existe despacho con el mismo `idPedido` | Devuelve `200 OK` con el despacho persistido sin crear duplicado ni mutar estado | CA-04 |
| Sin cobertura | El destino no pertenece a una zona activa de F-01 | Responde `422 Unprocessable Entity` con `DESP_ERROR_SIN_COBERTURA` | CA-02 |
| Datos incompletos | Faltan campos obligatorios o `cantidad <= 0` | Responde `400 Bad Request` detallando errores de validación | CA-03 |
| SKU inválido o sin datos | SKU desconocido o dimensiones nulas en Productos | Responde `422 Unprocessable Entity` (`DESP_ERROR_PRODUCTO_NO_ENCONTRADO` / `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`) | CA-05 |
| Caída de Productos | Productos y Ofertas responde error 5xx o timeout | Responde `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE` | CA-06 |
| Sin autorización | Token ausente, expirado o sin scope | Responde `401 Unauthorized` o `403 Forbidden` | CA-07 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Unicidad absoluta por pedido: no puede existir más de un despacho por `idPedido`. | F-02 RF-05, CA-11 |
| RN-02 | Todo despacho nace estrictamente en estado `PENDIENTE_ASIGNACION`. | F-02 RF-01, RT-01 |
| RN-03 | `cantidadPaquetes` se fija internamente en `1` para el alcance inicial; Ventas no envía este dato. | F-02 RF-01, api-contract §7.1 |
| RN-04 | Peso y volumen no se reciben de Ventas; se calculan en lote consultando Productos y Ofertas. | F-02 RF-05, CA-21 |
| RN-05 | Fecha programada se calcula internamente con base en zona y calendario; no se acepta fecha externa. | F-02 RF-01, api-contract §7.1 |
| RN-06 | Requiere encabezado `Idempotency-Key` (UUID v4 de hasta 128 caracteres). | F-02 RNF Idempotencia, api-contract §7.1 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `POST /api/v1/despachos` | Endpoint canónico de recepción externa. | [api-contract.md §7.1](../../integraciones/api-contract.md#71-crear-un-despacho-para-un-pedido-listo-para-entrega) |
| Resolución de zona (F-01) | Obtener zona activa y plazo estimado. | [F-01-Gestor_ZonasGeograficas.md](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) |
| `POST /api/v1/productos/datos-fisicos/consulta` | Obtener peso y dimensiones en lote. | [api-contract.md §5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas) |
| Auditoría transaccional (RT-02) | Registrar creación con usuario de servicio. | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) |

## 6. Criterios de aceptación

### CA-01. Recepción exitosa con cobertura activa y datos físicos de productos

- **DADO** que Ventas y Postventa envía una solicitud completa con un `idPedido` no registrado previamente, líneas con `sku` y `cantidad` válidos y un destino ubicado en una zona activa de F-01, y Productos y Ofertas devuelve los datos físicos vigentes de cada SKU.
- **CUANDO** se procesa la petición en `POST /api/v1/despachos` con un token de servicio válido con scope `despachos:crear` y un `Idempotency-Key` válido.
- **ENTONCES** el sistema consulta los datos físicos en lote, calcula el peso y el volumen totales, registra la cantidad de paquetes en `1`, calcula la fecha programada a partir de la zona y el calendario operativo, crea el despacho en `PENDIENTE_ASIGNACION`, genera el código operativo y de rastreo, registra la auditoría y retorna `201 Created` con el cuerpo del despacho.

### CA-02. Rechazo por destino sin cobertura activa

- **DADO** una solicitud cuyo destino no coincide con ninguna zona de cobertura activa en F-01.
- **CUANDO** la solicitud es evaluada por el backend.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con código `DESP_ERROR_SIN_COBERTURA`, no persiste ningún despacho y detalla la causa del rechazo.

### CA-03. Rechazo por solicitud con datos incompletos o inconsistentes

- **DADO** una solicitud sin distrito, sin líneas, con una línea sin `sku` o con una `cantidad` menor o igual a cero.
- **CUANDO** la solicitud es validada en el controlador.
- **ENTONCES** el sistema responde `400 Bad Request`, detalla los campos inválidos en la estructura estándar de error y no persiste registros parciales en base de datos.

### CA-04. Solicitud repetida para el mismo pedido (idempotencia)

- **DADO** que ya existe un despacho registrado para el pedido `PED-2026-00891`.
- **CUANDO** Ventas y Postventa vuelve a enviar una solicitud con el mismo `idPedido`.
- **ENTONCES** el sistema no crea un nuevo despacho, no duplica registros y responde `200 OK` retornando el despacho existente con su estado actual.

### CA-05. Rechazo por SKU inexistente o sin datos físicos válidos

- **DADO** una solicitud que incluye un `sku` que Productos y Ofertas no reconoce o cuyo peso o dimensiones son nulos o menores o iguales a cero.
- **CUANDO** el backend intenta obtener los datos físicos antes de la persistencia.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con `DESP_ERROR_PRODUCTO_NO_ENCONTRADO` o `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS` y no crea el despacho.

### CA-06. Rechazo por indisponibilidad de Productos y Ofertas

- **DADO** que el servicio de Productos y Ofertas responde con error 5xx o agota el tiempo de espera (timeout).
- **CUANDO** se procesa la solicitud de creación de despacho.
- **ENTONCES** el sistema responde `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE` y no persiste el despacho.

### CA-07. Acceso sin autenticación o con scope insuficiente

- **DADO** una petición a `POST /api/v1/despachos` sin token de autorización, con token expirado o sin el scope `despachos:crear`.
- **CUANDO** es evaluada por la capa de seguridad.
- **ENTONCES** el sistema responde `401 Unauthorized` o `403 Forbidden` y no procesa la creación.

## 7. Referencias

1. [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md): especificación funcional padre.
2. [api-contract.md §7.1](../../integraciones/api-contract.md#71-crear-un-despacho-para-un-pedido-listo-para-entrega): contrato canónico de recepción externa.
3. [api-contract.md §5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas): contrato de consulta de datos físicos en lote.
