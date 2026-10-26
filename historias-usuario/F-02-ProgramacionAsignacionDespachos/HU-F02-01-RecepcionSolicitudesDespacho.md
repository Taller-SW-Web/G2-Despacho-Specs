# [HU-F02-01] Recepción de Solicitudes de Despacho e Integridad

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Integración, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `f-02`, `sdd`, `recepcion`, `idempotencia`, `productos`, `cobertura` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Sistema Comercial (Ventas y Postventa)  
**QUIERO** enviar una solicitud de despacho formal con los datos del pedido, destinatario, destino y las líneas (`sku` y `cantidad`)  
**PARA** que el módulo de despacho registre el paquete en cola con zona activa resuelta, datos físicos vigentes y código de rastreo único, de forma segura e idempotente.

---

## 2. Descripción y Contexto Técnico

- **Especificación SDD origen:** [ES-F02-01: Recepción de solicitudes de despacho](../../especificaciones/ES-F02-01-RecepcionSolicitudDespacho/spec.md).
- **Especificación funcional padre:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisitos `RF-01` y `RF-05`; Criterios `CA-01`, `CA-02`, `CA-11`, `CA-12`, `CA-21`).
- **Endpoints asociados:** `POST /api/v1/despachos` (detallado en [integraciones/api-contract.md §7.1](../../integraciones/api-contract.md#71-crear-un-despacho-para-un-pedido-listo-para-entrega)).
- **Autenticación:** token de servicio JWT emitido por Seguridad y Usuarios con `sub=modulo-ventas`, `aud=api-despacho` y scope `despachos:crear`.
- **Encabezados obligatorios:** `Authorization: Bearer <token>`, `Idempotency-Key: <UUID v4>`.
- **Reglas de negocio y cálculo:**
  - El payload debe incluir: `idPedido`, destinatario (`nombre`, `telefono`), destino (`direccion`, `distrito`) y arreglo `lineas` con al menos un elemento (`sku` obligatorio, `cantidad > 0`).
  - Ventas no envía peso, volumen, cantidad de paquetes ni fecha comprometida.
  - El sistema resuelve la zona con F-01 y valida que esté `ACTIVO`. Si no tiene cobertura activa, responde `422 Unprocessable Entity` (`DESP_ERROR_SIN_COBERTURA`).
  - Consulta en lote a Productos y Ofertas los datos físicos vigentes: calcula `pesoTotalKg` y `volumenTotalM3`. Si un SKU no existe o faltan datos físicos, responde `422` (`DESP_ERROR_PRODUCTO_NO_ENCONTRADO` / `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`). Si Productos no está disponible, responde `503` (`DESP_ERROR_PRODUCTOS_NO_DISPONIBLE`).
  - Fija `cantidadPaquetes = 1` y calcula `fechaProgramada` a partir del plazo de la zona y el calendario de operaciones.
  - Genera código operativo único (`DSP-XXXXXX`) y código de rastreo público (`TRK-XXXXX`).
  - Idempotencia: una solicitud repetida para el mismo `idPedido` o con la misma clave devuelve el despacho existente con HTTP `200 OK` sin duplicarlo.
  - No exige cotización previa ni lee o escribe `cotizaciones` para recibir el pedido; consulta el perfil físico vigente por la operación canónica del [contrato externo §5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas).
  - Agrupa cantidades, limita a 100 SKU únicos y valida el lote íntegro. La regla prevista para `INACTIVO` no rechaza automáticamente pedidos pagados; `BORRADOR` y demás precisiones siguen pendientes de homologación en §11.1 [cite: 1].

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-01: Recepción exitosa desde Ventas y Postventa**
  - **DADO** que Ventas y Postventa envía una solicitud con identificador de pedido no registrado previamente, destinatario, dirección, distrito y líneas con `sku` y `cantidad` válidos, el destino está cubierto por una zona activa de F-01 y Productos y Ofertas devuelve los datos físicos vigentes de cada SKU.
  - **CUANDO** la solicitud se procesa con un token de servicio válido con scope `despachos:crear` y un `Idempotency-Key` válido en `POST /api/v1/despachos`.
  - **ENTONCES** el sistema consulta los datos físicos en lote, calcula el peso y el volumen totales, registra la cantidad de paquetes en `1`, calcula la fecha programada, crea el despacho en `PENDIENTE_ASIGNACION`, genera el código operativo interno y de rastreo, registra la auditoría y responde `201 Created` con el recurso persistido.

- [ ] **CA-02: Rechazo de solicitud con datos incompletos o inconsistentes**
  - **DADO** una solicitud sin distrito, sin líneas, con una línea sin `sku` o con una `cantidad` menor o igual a cero.
  - **CUANDO** es evaluada por la capa de validación.
  - **ENTONCES** el sistema responde `400 Bad Request`, detalla los campos inválidos en la estructura estándar de error y no persiste registros parciales.

- [ ] **CA-11: Solicitud repetida para el mismo pedido (idempotencia)**
  - **DADO** que ya existe un despacho registrado para el pedido `PED-2026-00891`.
  - **CUANDO** Ventas y Postventa vuelve a enviar una solicitud con ese identificador de pedido.
  - **ENTONCES** el sistema no crea un nuevo despacho, no duplica registros y responde `200 OK` con el despacho existente, su código interno y su estado actual.

- [ ] **CA-12: Destino sin cobertura activa**
  - **DADO** una solicitud cuyo destino no pertenece a ninguna zona de cobertura activa de F-01.
  - **CUANDO** es evaluada por el backend.
  - **ENTONCES** el sistema responde `422 Unprocessable Entity` con el código `DESP_ERROR_SIN_COBERTURA` y no persiste el despacho.

- [ ] **CA-21: Rechazo por datos físicos no disponibles en Productos y Ofertas**
  - **DADO** un SKU inexistente en una respuesta íntegra, un error de negocio de datos físicos incompletos o el servicio de Productos temporalmente no disponible.
  - **CUANDO** el sistema intenta obtener los datos físicos de las líneas antes de persistir el despacho.
  - **ENTONCES** el sistema responde `422 Unprocessable Entity` con `DESP_ERROR_PRODUCTO_NO_ENCONTRADO` o `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`, o `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE`, respectivamente, y no crea el despacho.

- [ ] **CA-22 a CA-24: Lote, estado comercial y límite físico**
  - Escenarios en [F-02 RF-05](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md#rf-05-integridad-de-la-recepción), concretados por ES-F02-01 CA-08 a CA-10; pendientes de implementación, homologación y verificación [cite: 1].

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] DTOs de entrada y salida implementados y validados con `jakarta.validation`.
- [ ] Seguridad implementada exigiendo token de servicio y scope `despachos:crear`.
- [ ] Cliente REST hacia Productos y Ofertas integrado con manejo de errores y timeouts.
- [ ] Mecanismo de idempotencia verificado ante reintentos simultáneos con el mismo `idPedido`.
- [ ] Pruebas unitarias y de integración con `JUnit 5 + Mockito` y `Testcontainers` cubriendo `CA-01`, `CA-02`, `CA-11`, `CA-12` y `CA-21` a `CA-24`, con idempotencia previa a G6 y sin escritura en `cotizaciones`.
- [ ] Documentación y trazabilidad sincronizadas con [ES-F02-01](../../especificaciones/ES-F02-01-RecepcionSolicitudDespacho/spec.md).

[cite: 1] [Contrato externo §§5.2, 7.1 y 11.1](../../integraciones/api-contract.md#111-respuesta-propuesta-y-plan-de-homologación-física-g2g6). La actualización documental no acredita aceptación bilateral ni pruebas ejecutadas.
