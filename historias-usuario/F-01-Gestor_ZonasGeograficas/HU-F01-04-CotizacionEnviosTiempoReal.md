# [HU-F01-04] Cotización de Envíos en Tiempo Real para Canales de Venta

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-01: Gestor de Zonas Geográficas y Cotizador de Envíos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-01`, `sdd`, `cotizacion`, `api`, `checkout` |
| **Responsable sugerido** | Valqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Canal de Venta (Marketplace o Chatbot)  
**QUIERO** invocar el endpoint de cotización con el destino y, cuando corresponda, las líneas del pedido (`sku` y `cantidad`) antes de confirmar una orden  
**PARA** ofrecer al cliente la cobertura, el costo de envío exacto y la promesa de entrega en tiempo real.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisito `RF-03`, Criterios `CA-07`, `CA-08`, `CA-09`, `CA-10`).
- **Endpoints asociados:**
  - `POST /api/v1/cotizaciones` (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md), sección 5.1).
- **Autenticación:** token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`; no requiere JWT de usuario humano ni API key adicional. La identidad del consumidor se toma del claim `sub` (por ejemplo, `modulo-chatbot`) y el límite de solicitudes es configurable por `sub` e IP.
- **Cuerpo de la solicitud:**
  - `destino` con `distrito` obligatorio; `direccion` y `codigoPostal` son opcionales.
  - `lineas` opcional: arreglo de al menos un elemento con `sku` obligatorio y `cantidad` mayor que cero.
- **Modalidades según el cuerpo (sección 5.1 del contrato):**

  | Cuerpo | Resultado | `tipoCotizacion` |
  |---|---|---|
  | Solo `destino` | Cobertura, zona y datos del destino | — |
  | `destino` y `lineas` | Cobertura y costo calculado con los datos físicos de los productos | `EXACTA` |
  | Destino sin cobertura | Solo cobertura y datos del destino, sin costo ni plazo | — |

- **Reglas de negocio:**
  - La cobertura se evalúa primero; si el destino no tiene cobertura, se responde sin consultar a Productos y Ofertas ni validar las líneas.
  - Con `lineas`, el sistema agrupa los SKU repetidos, consulta a Productos y Ofertas en lote con su propio token de servicio (scope `productos:fisicos:leer`) y calcula el peso y el volumen totales; el canal nunca envía peso, volumen ni costo.
  - Si el destino se encuentra fuera de todas las zonas activas, se responde `200 OK` con `coberturaDisponible: false`, `nombreZona: null`, sin costo ni plazo y el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura".
  - Sin `lineas`, la respuesta confirma únicamente la cobertura, la zona y los datos del destino, sin costo, sin plazo y sin `tipoCotizacion`.
  - Cada cálculo exacto exitoso se guarda en `cotizaciones` antes de responder, aunque no exista pedido, con vínculos nulos a pedido/despacho. No se guardan cobertura sin productos, resultados sin tarifa ni rechazos.
  - La cotización no crea un pedido ni un despacho ni requiere `Idempotency-Key`: una repetición puede generar otra instantánea del cálculo vigente.
  - El límite de SKU, la integridad del lote, la elegibilidad y los errores se rigen por [contrato externo §§5.1 y 5.2](../../integraciones/api-contract.md#51-solicitar-cotización); la homologación externa sigue pendiente en [§11.1](../../integraciones/api-contract.md#111-respuesta-propuesta-y-plan-de-homologación-física-g2g6) [cite: 1].
  - Rendimiento: tiempo de respuesta menor a 100 ms.
- **Entidades de datos involucradas:** `zonas`, `zonas_distritos`, `zonas_codigos_postales` y `tarifas_zona` (lectura); `cotizaciones` (inserción exacta exitosa, ver [modelo de datos](../../arquitectura/modelo-datos.md)) [cite: 2].

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-07: Cotización exitosa dentro de cobertura**
  - **DADO** un destino en un distrito de la zona "Lima Centro" y las líneas `POL-NEG-M` por 5 y `ZAP-RUN-42` por 1, cuyos datos físicos provienen de Productos y Ofertas.
  - **CUANDO** el canal de venta invoca el endpoint `POST /api/v1/cotizaciones` con su token de servicio.
  - **ENTONCES** el sistema calcula 2.65 kg y 0.021 m³ totales, aplica la tarifa vigente de la zona (10.00 PEN hasta 3 kg, 2.00 PEN por kg adicional, factor volumétrico 1.25) y retorna `tipoCotizacion=EXACTA`, `costoEnvio` de 10.00 PEN, `moneda` `PEN`, `plazoEstimadoDiasHabiles` de 2 y la `fechaEstimadaEntrega`.

- [ ] **CA-08: Cotización con líneas o cantidades inválidas**
  - **DADO** una solicitud con `lineas` vacías o con una línea cuya `cantidad` es menor o igual a cero.
  - **CUANDO** se envía al endpoint de cotización.
  - **ENTONCES** el sistema rechaza la petición con `400 Bad Request` y el código `DESP_ERROR_LINEAS_VACIAS` o `DESP_ERROR_CANTIDAD_INVALIDA`, sin calcular el costo.

- [ ] **CA-09: Cotización con datos físicos inválidos**
  - **DADO** que G6 comunica mediante el error de negocio acordado un SKU sin peso mayor a cero, dimensiones válidas o marca de actualización.
  - **CUANDO** se envía al endpoint de cotización.
  - **ENTONCES** el sistema rechaza la petición con `422 Unprocessable Entity` y el código `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`, identificando el producto, sin devolver costo.

- [ ] **CA-10: Cotización sin cobertura de entrega**
  - **DADO** una solicitud de cotización para un destino fuera de todas las zonas activas, con o sin `lineas`.
  - **CUANDO** se envía al endpoint de cotización.
  - **ENTONCES** el sistema retorna código `200 OK` con `coberturaDisponible: false`, `nombreZona: null`, sin costo de envío ni plazo estimado, y con el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura", sin consultar a Productos y Ofertas.

- [ ] **CA-24 a CA-29: Persistencia e integridad ampliadas**
  - Los escenarios DADO/CUANDO/ENTONCES se mantienen en [F-01 RF-03](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md#rf-03-cotización-en-tiempo-real-para-canales-de-venta) y se concretan en [ES-F01-06 CA-11 a CA-16](../../especificaciones/ES-F01-06-CotizarEnvioConProductos/spec.md#ca-11-instantánea-exacta-exitosa-sin-pedido): instantánea antes de confirmar venta, exclusión de cobertura/rechazos, fallo de escritura, lote inválido, elegibilidad y límite de SKU. Todos pendientes de implementación/verificación; estados de G6 pendientes de homologación [cite: 1].

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Motor de cotización implementado en Spring Boot sobre sus propias tablas de zonas y tarifas, con consulta en lote a Productos y Ofertas usando el token de servicio de `modulo-despacho`.
- [ ] Pruebas unitarias (`JUnit 5 + Mockito`) de cálculo tarifario y validación de cobertura geográfica.
- [ ] Prueba de integración del endpoint `POST /api/v1/cotizaciones` validando las tres modalidades de la sección 5.1 y los códigos `DESP_ERROR_*` según [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Escritor de `cotizaciones` probado con PostgreSQL: correspondencia fila/respuesta, tarifa histórica, vínculos nulos, repetición y rollback; cobertura y rechazos sin filas nuevas.
- [ ] Prueba de seguridad: `401` sin token o con token inválido y `403` con token sin el scope `cotizaciones:calcular`.
- [ ] Verificación automatizada del tiempo de respuesta menor a 100 ms.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.

Referencias: [cite: 1] [contrato externo](../../integraciones/api-contract.md), §§5 y 11.1; [cite: 2] [modelo de datos §3.1](../../arquitectura/modelo-datos.md#31-zonas-y-tarifas-gestión-de-despachos-escribe-f-01), DDL comunicado y escritor pendiente.
