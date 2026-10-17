# ES-F01-06: Cotizar el envío con datos físicos de productos

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Canal de venta

**UI:** No aplica. Es una API consumida por Marketplace y Chatbot, responsables de sus propias interfaces; no crea ni modifica pantallas del módulo.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación de la revisión `91db8f8`, migrada al flujo SDD el 16/10/2026; conserva los criterios CA-01 a CA-10.

## 1. Contexto y objetivo

Calcular el costo de envío y el plazo estimado de un pedido a partir del destino, de los SKU y cantidades indicados por el canal y de la tarifa vigente de la zona que cubre ese destino. El módulo obtiene los datos físicos de cada producto ante Productos y Ofertas, calcula el peso y el volumen cotizables y devuelve una cotización exacta que los canales comunican al cliente antes de confirmar el pedido.

## 2. Alcance

- Incluye: cotizar con líneas de productos, consultar sus datos físicos en lote, aplicar la tarifa vigente y calcular costo y estimación de entrega; controlar el acceso técnico y el límite de solicitudes.
- Fuera de alcance: crear el pedido o el despacho y comunicarse con Ventas y Postventa al cotizar; aplicar promociones, descuentos o envío gratuito; definir o modificar tarifas; resolver zona para F-02 o F-05; persistir cotizaciones como registros de negocio. Solo se conserva la auditoría de configuración en ES-F01-08.

## 3. Actor, precondiciones y resultados

- El actor es un canal de venta que obtuvo un token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`.
- La solicitud identifica el destino con `distrito` y contiene `lineas` con `sku` y `cantidad` mayor que cero.
- El módulo puede obtener de Productos y Ofertas el peso y las dimensiones vigentes de cada SKU.
- La zona que cubre el destino está en estado `ACTIVO` y, para devolver costo, tiene una tarifa vigente.
- Disparador: el canal solicita el costo de envío antes de confirmar el pedido.
- Resultado exitoso: cotización exacta con cobertura, zona, totales físicos, costo, moneda, plazo, fecha estimada y marca temporal; sin cobertura se informa esa condición sin costo ni plazo.
- Resultado ante rechazo: error normalizado de autenticación, destino, líneas, productos o límite, sin costo ni creación de recursos [cite: 2].

## 4. Flujo principal y alternativas

1. El canal envía el destino y las líneas del pedido con su token de servicio.
2. El backend valida el token y el destino, y aplica el límite de solicitudes.
3. El sistema evalúa la cobertura del destino y, si existe zona activa, la identifica.
4. Con cobertura, valida las líneas, agrupa los SKU repetidos y consulta a Productos y Ofertas en lote con su propio token de servicio.
5. El sistema calcula el peso y el volumen totales, el peso cotizable con el factor volumétrico y el costo con la tarifa vigente de la zona.
6. El sistema responde con `tipoCotizacion=EXACTA`, el desglose calculado, el costo, la moneda, el plazo y la fecha estimada de entrega.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Sin cobertura | No existe zona activa | Responde sin costo, plazo ni consulta a Productos | CA-02 |
| Líneas inválidas | Lista vacía o cantidad no positiva, con cobertura | Rechaza sin calcular costo | CA-03 |
| Productos inválidos o no disponibles | SKU inexistente, datos incompletos o fallo de consulta | Error normalizado sin estimar costo | CA-04 a CA-06 |
| Sin tarifa | Zona activa sin regla vigente | Confirma cobertura sin costo ni plazo; detalle contractual pendiente | CA-07 |
| Exceso de solicitudes | Se supera el límite por `sub` e IP | Rechaza sin procesar el cálculo | CA-09 |

## 5. Reglas, datos e integraciones

### Reglas y validaciones

- La cobertura se evalúa antes que los productos: si no hay zona activa para el destino, el sistema responde sin consultar a Productos y Ofertas ni validar las líneas.
- El canal envía `sku` y `cantidad`; nunca envía peso, volumen, dimensiones ni costo. El sistema no los acepta como entrada autoritativa.
- Los SKU repetidos se agrupan y se consultan una sola vez por producto dentro de la solicitud en lote.
- El sistema utiliza su propio token de servicio (`modulo-despacho`) con `aud=api-productos` y scope `productos:fisicos:leer`; nunca reenvía a Productos y Ofertas el token del canal.
- El cálculo de los totales por línea y el cálculo del costo son los definidos en la funcionalidad padre:

```text
volumenUnitarioM3 = (largoCm / 100) × (anchoCm / 100) × (altoCm / 100)
pesoLineaKg = pesoKg × cantidad
volumenLineaM3 = volumenUnitarioM3 × cantidad
pesoTotalKg = Σ pesoLineaKg
volumenTotalM3 = Σ volumenLineaM3
pesoCotizableKg = pesoTotalKg + (volumenTotalM3 × factorVolumetrico)
costoEnvio = tarifaBase + (recargoKgAdicional × max(0, pesoCotizableKg − pesoIncluidoKg))
```

- `lineas` vacía produce `400 Bad Request` con `DESP_ERROR_LINEAS_VACIAS`; una `cantidad` menor o igual a cero produce `400 Bad Request` con `DESP_ERROR_CANTIDAD_INVALIDA`.
- Un `sku` no reconocido produce `422 Unprocessable Entity` con `DESP_ERROR_PRODUCTO_NO_ENCONTRADO`; un producto sin peso mayor a cero o sin dimensiones válidas produce `422 Unprocessable Entity` con `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`. En ambos casos no se devuelve costo.
- Si no es posible consultar a Productos y Ofertas, el sistema responde `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE` y no estima un costo.
- Una zona activa sin tarifa vigente no produce costo ni plazo; el sistema no asume una regla implícita y el tratamiento exacto de este caso permanece como acuerdo pendiente en el contrato.
- El sistema calcula el plazo estimado en días hábiles y la fecha estimada de entrega a partir de la tarifa vigente y del calendario operativo.
- La cotización no crea un pedido ni un despacho, no requiere `Idempotency-Key` y no modifica ningún recurso del módulo.
- Ventas y Postventa puede conservar la fecha estimada como referencia, pero no debe enviarla al crear el despacho; las promociones y el envío gratuito pertenecen a Ventas y Postventa y no alteran el costo logístico.
- El límite de solicitudes se aplica por `sub` del token de servicio e IP; al excederlo, la respuesta es `429 Too Many Requests` con `DESP_ERROR_LIMITE_COTIZACION`.
- La cotización no expone la configuración interna de zonas ni de tarifas.

### Entradas

- Token de servicio con scope `cotizaciones:calcular`.
- Destino con `distrito` obligatorio y `direccion` o `codigoPostal` opcionales.
- Líneas con `sku` y `cantidad` mayor que cero.

### Salidas

- `tipoCotizacion=EXACTA`, disponibilidad de cobertura y nombre de la zona.
- Peso total, volumen total, costo, moneda, plazo estimado en días hábiles y fecha estimada de entrega.
- Marca temporal de la cotización.
- Error normalizado ante líneas, cantidades o datos físicos inválidos, producto inexistente, productos no disponible o exceso de límite.

### Integraciones

- Productos y Ofertas provee el peso y las dimensiones vigentes de cada SKU mediante la consulta en lote acordada; los datos siguen siendo de su propiedad.
- Seguridad y Usuarios emite el token del canal y el token propio que el módulo utiliza contra la API de productos.
- Ventas y Postventa incorpora el costo al total del pedido y no envía la fecha estimada al crear el despacho.
- La operación de cotización se define en el [contrato externo §5.1](../../integraciones/api-contract.md#51-solicitar-cotización); la consulta de datos físicos, en [§5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas). Las rutas, cuerpos, respuestas, códigos de error y unidades se rigen exclusivamente por ese contrato [cite: 2].

## 6. Criterios de aceptación

### CA-01. Cotización dentro de cobertura

- **DADO** un destino en un distrito de "Lima Centro" y las líneas `POL-NEG-M` por 5 y `ZAP-RUN-42` por 1, cuyos datos físicos provienen de Productos y Ofertas.
- **CUANDO** un canal de venta solicita la cotización.
- **ENTONCES** el sistema devuelve `tipoCotizacion=EXACTA`, 2.65 kg y 0.021 m³ totales, un costo de 10.00 PEN según la tarifa vigente de la zona (10.00 PEN hasta 3 kg, 2.00 PEN por kg adicional y factor volumétrico 1.25) y un plazo estimado de 2 días hábiles.

### CA-02. Cotización sin cobertura

- **DADO** un destino fuera de todas las zonas activas.
- **CUANDO** el canal envía la solicitud con `lineas`.
- **ENTONCES** el sistema responde `200 OK` con `coberturaDisponible: false`, sin costo ni plazo y con el mensaje de destino fuera de cobertura, sin consultar a Productos y Ofertas.

### CA-03. Líneas o cantidades inválidas

- **DADO** una solicitud con `lineas` vacía o con una `cantidad` menor o igual a cero.
- **CUANDO** el canal envía la cotización.
- **ENTONCES** el sistema responde `400 Bad Request` con `DESP_ERROR_LINEAS_VACIAS` o `DESP_ERROR_CANTIDAD_INVALIDA` y no calcula el costo.

### CA-04. Producto inexistente

- **DADO** una solicitud que incluye un `sku` que Productos y Ofertas no reconoce.
- **CUANDO** el canal envía la cotización.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con `DESP_ERROR_PRODUCTO_NO_ENCONTRADO`, identifica el `sku` y no devuelve costo.

### CA-05. Datos físicos incompletos

- **DADO** una solicitud cuyo producto no tiene peso mayor a cero o dimensiones válidas.
- **CUANDO** el canal envía la cotización.
- **ENTONCES** el sistema responde `422 Unprocessable Entity` con `DESP_ERROR_DATOS_FISICOS_INCOMPLETOS`, identifica el producto y no devuelve costo.

### CA-06. Productos no disponible

- **DADO** que no es posible consultar los datos físicos de los productos.
- **CUANDO** el canal envía la cotización.
- **ENTONCES** el sistema responde `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE` y no devuelve un costo estimado.

### CA-07. Zona activa sin tarifa vigente

- **DADO** un destino cubierto por una zona `ACTIVO` que no tiene tarifa vigente.
- **CUANDO** el canal envía la cotización con `lineas`.
- **ENTONCES** el sistema confirma la cobertura y la zona, no devuelve costo ni plazo y no aplica una regla tarifaria implícita.

### CA-08. Acceso con token de servicio

- **DADO** que un canal obtuvo un token técnico con `cotizaciones:calcular`.
- **CUANDO** envía la solicitud con `Authorization: Bearer <token>`.
- **ENTONCES** el sistema procesa la cotización sin requerir una sesión de usuario humano y sin crear pedido ni despacho.

### CA-09. Exceso de límite de solicitudes

- **DADO** que un mismo `sub` e IP superaron el límite configurado de cotizaciones.
- **CUANDO** el canal envía una nueva solicitud.
- **ENTONCES** el sistema responde `429 Too Many Requests` con `DESP_ERROR_LIMITE_COTIZACION` y sin procesar el cálculo.

### CA-10. Datos de productos no enviados por el canal

- **DADO** una solicitud que incluye peso o volumen en el cuerpo.
- **CUANDO** el canal envía la cotización.
- **ENTONCES** el sistema los ignora y los calcula a partir de los datos de Productos y Ofertas.

## 7. UI, backend y requisitos no funcionales

- UI: no aplica; la presentación del resultado pertenece al canal consumidor. No se incluye `ui.md`.
- Backend: Gestión evalúa cobertura y tarifa, consulta los datos físicos mediante API y calcula la cotización sin modificar recursos.
- Requisitos no funcionales: token técnico y scopes acordados; datos de Productos obtenidos sin compartir persistencia; sin exposición de configuración interna; indisponibilidad explícita sin costo estimado. F-01 §8 exige respuesta en menos de 100 ms; el entorno, carga y medición con la dependencia externa se concretarán en el plan [cite: 1].
- Pendientes: tratamiento contractual de zona sin tarifa, precisión y redondeo, calendario operativo, configuración de tasa/caché y preparación de la integración real; responsables e impacto en [plan.md §7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Unitaria e integración | Productos del ejemplo, tarifa vigente y calendario controlado |
| CA-02 | Integración | Destino sin cobertura, incluso con líneas inválidas; verificar cero llamadas a Productos |
| CA-03 | Integración | Destino cubierto con lista vacía y cantidades cero/negativas |
| CA-04 | Contrato e integración | SKU no reconocido por Productos |
| CA-05 | Contrato e integración | Peso o dimensiones ausentes/no positivos |
| CA-06 | Integración de fallos | Indisponibilidad y timeout del proveedor |
| CA-07 | Integración | Zona activa sin regla vigente; respuesta según acuerdo pendiente |
| CA-08 | Seguridad e integración | Token técnico válido y ausencia de escrituras de pedido/despacho |
| CA-09 | Integración de tasa | Mismo `sub` e IP por encima del límite |
| CA-10 | Integración | Peso y volumen del cliente distintos de los del proveedor |

- [ ] CA-01 a CA-10 cuentan con resultados reproducibles en [evidence.md](./evidence.md).
- [ ] El contrato y los pendientes bloqueantes están resueltos para el alcance implementado.
- [ ] Se verifican agrupación de SKU, ausencia de efectos de negocio, seguridad y rendimiento.
- [ ] Los commits y la revisión funcional y técnica están enlazados.

La ejecución se descompone en [tasks.md](./tasks.md). La migración documental no acredita implementación.

## 9. Referencias

- [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-02 y RF-03, CA-07 a CA-11, CA-14 y CA-19 a CA-23; §8.
- [cite: 2] [Contrato externo](../../integraciones/api-contract.md), §§3.4, 3.5, 5.1, 5.2 y 10.1.
- [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), tabla `tarifas_zona`.
- [cite: 4] [Visión general](../../overview.md), sección 7 sobre integración con Productos y Ofertas.
- [cite: 5] [Pendientes](../../funcionalidades/pendiente.md), sección F-01 sobre trabajo futuro.
- Documentos SDD: [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
