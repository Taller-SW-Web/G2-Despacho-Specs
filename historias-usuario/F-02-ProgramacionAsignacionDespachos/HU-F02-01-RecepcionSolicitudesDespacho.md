# [HU-F02-01] Recepción de Solicitudes de Despacho

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-02`, `sdd`, `recepcion`, `api` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Sistema Comercial (Ventas / Checkout)  
**QUIERO** enviar una solicitud de despacho formal con los datos del pedido, destinatario, destino y las líneas del pedido (`sku` y `cantidad`)  
**PARA** que el módulo de despacho registre el paquete en cola y genere un código de rastreo único para su entrega.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-01`).
- **Endpoints asociados:**
  - `POST /api/v1/despachos` (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md), Externo §7.1).
- **Autenticación:** token de servicio de `modulo-ventas` con `tipo=servicio`, `aud=api-despacho` y scope `despachos:crear`; la solicitud exige además un `Idempotency-Key` (UUID v4).
- **Reglas de negocio:**
  - El payload debe incluir obligatoriamente: `idPedido`, datos del destinatario (`nombre`, `telefono`), destino (`direccion`, `distrito`) y al menos una línea con `sku` y `cantidad` mayor que cero. Las coordenadas y el código postal son opcionales.
  - Ventas y Postventa no envía peso, volumen, cantidad de paquetes ni fecha comprometida. Antes de persistir el despacho, el módulo consulta en lote a Productos y Ofertas los datos físicos vigentes de cada SKU, calcula el peso y el volumen totales, registra internamente `cantidadPaquetes = 1` y calcula la fecha programada a partir de la zona y el calendario operativo.
  - Si un SKU no existe o no tiene datos físicos válidos, se responde `422 Unprocessable Entity`; si Productos y Ofertas no está disponible, se responde `503 Service Unavailable`; en ningún caso se crea el despacho.
  - Si la validación es exitosa, se genera automáticamente un código de rastreo único (`TRK-XXXXX`), se asigna el estado inicial `PENDIENTE_ASIGNACION` y se retorna HTTP `201 Created`. Un reintento con el mismo `idPedido` responde `200 OK` con el despacho existente sin duplicarlo.
  - Si faltan datos obligatorios o los valores son inválidos (por ejemplo, `cantidad <= 0`), la petición se rechaza con HTTP `400 Bad Request` sin persistencia parcial.
- **Entidades de datos involucradas:** `despachos`, `historial_estados_despacho`.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-01: Recepción exitosa desde sistema comercial**
  - **DADO** que un sistema externo envía una solicitud con identificador de pedido, datos del destinatario, destino y líneas (`sku` y `cantidad`) válidos, el destino está cubierto por una zona activa y Productos y Ofertas devuelve los datos físicos vigentes de cada SKU.
  - **CUANDO** la petición es procesada con un token de servicio válido con scope `despachos:crear` y un `Idempotency-Key` válido en `POST /api/v1/despachos`.
  - **ENTONCES** el sistema calcula el peso y el volumen totales, registra internamente `cantidadPaquetes = 1`, calcula la fecha programada, guarda el despacho con estado `PENDIENTE_ASIGNACION`, genera un código de rastreo único y responde con código `201 Created` y el cuerpo del despacho registrado.

- [ ] **CA-03: Rechazo de solicitud con datos incompletos o inconsistentes**
  - **DADO** que una solicitud carece de distrito, no incluye líneas o presenta una línea sin `sku` o con `cantidad` menor o igual a cero.
  - **CUANDO** la solicitud es evaluada por la capa de validación en `POST /api/v1/despachos`.
  - **ENTONCES** el sistema rechaza la operación con código `400 Bad Request`, detalla los campos inválidos en la estructura estándar de error y no persiste registros parciales en la base de datos.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Código implementado en Java 21 / Spring Boot siguiendo las convenciones de [AGENTS.md](../../AGENTS.md).
- [ ] DTOs de entrada validados con anotaciones `@NotNull`, `@NotBlank`, `@Positive` (`jakarta.validation`).
- [ ] Pruebas unitarias de validación y de servicio con `JUnit 5 + Mockito` aprobadas con cobertura >= 80%.
- [ ] Prueba de integración del endpoint `POST /api/v1/despachos` validada contra [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
