# ES-F01-06: Cotizar el envío con datos físicos de productos

**Funcionalidad padre:** F-01 — Gestor de zonas geográficas y cotizador de envíos  
**Responsable:** Valqui  
**Estado:** Borrador  
**Actor principal:** Canal de venta

## 1. Objetivo

Calcular el costo de envío y el plazo estimado de un pedido a partir del destino, de los SKU y cantidades indicados por el canal y de la tarifa vigente de la zona que cubre ese destino. El módulo obtiene los datos físicos de cada producto ante Productos y Ofertas, calcula el peso y el volumen cotizables y devuelve una cotización exacta que los canales comunican al cliente antes de confirmar el pedido.

## 2. Actor y precondiciones

- El actor es un canal de venta que obtuvo un token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`.
- La solicitud identifica el destino con `distrito` y contiene `lineas` con `sku` y `cantidad` mayor que cero.
- El módulo puede obtener de Productos y Ofertas el peso y las dimensiones vigentes de cada SKU.
- La zona que cubre el destino está en estado `ACTIVO` y, para devolver costo, tiene una tarifa vigente.

## 3. Flujo principal

1. El canal envía el destino y las líneas del pedido con su token de servicio.
2. El backend valida el token, el destino y la estructura de las líneas.
3. El sistema evalúa la cobertura del destino y, si existe zona activa, la identifica.
4. El sistema agrupa los SKU repetidos y consulta a Productos y Ofertas en lote con su propio token de servicio.
5. El sistema calcula el peso y el volumen totales, el peso cotizable con el factor volumétrico y el costo con la tarifa vigente de la zona.
6. El sistema responde con `tipoCotizacion=EXACTA`, el desglose calculado, el costo, la moneda, el plazo y la fecha estimada de entrega.

## 4. Reglas y validaciones

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

## 5. Entradas, salidas e integraciones

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
- La ruta, los cuerpos, las respuestas, los códigos de error y las unidades se rigen exclusivamente por `integraciones/api-contract.md` [cite: 2].

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

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Crear el pedido o el despacho, y cualquier comunicación con Ventas y Postventa al cotizar.
- Aplicar promociones, descuentos o envío gratuito.
- Definir o modificar la tarifa de la zona.
- Resolver la zona para F-02 o F-05.
- Persistir la cotización como registro; solo se conserva la auditoría de la configuración.

### Referencias

- [cite: 1] `funcionalidades/F-01-Gestor_ZonasGeograficas.md`, RF-02 y RF-03, CA-07 a CA-11, CA-14 y CA-19 a CA-23.
- [cite: 2] `integraciones/api-contract.md`, secciones 3.4, 3.5, 5.1, 5.2 y 15.1.
- [cite: 3] `arquitectura/modelo-datos.md`, tabla `tarifas_zona`.
- [cite: 4] `overview.md`, sección 7 sobre integración con Productos y Ofertas.
- [cite: 5] `funcionalidades/pendiente.md`, sección F-01 sobre trabajo futuro.