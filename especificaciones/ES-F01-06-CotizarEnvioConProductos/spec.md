# ES-F01-06: Cotizar el envío con datos físicos de productos

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Canal de venta

**UI:** No aplica. Es una API consumida por Marketplace y Chatbot, responsables de sus propias interfaces; no crea ni modifica pantallas del módulo.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación de la revisión `91db8f8`, migrada al flujo SDD el 16/10/2026; conserva los criterios CA-01 a CA-10.

**Actualización 26/10/2026:** persistencia exacta acordada con la persona responsable y preparación de H-G2-01 a H-G2-03. Se conservan CA-01 a CA-10 y se agregan CA-11 a CA-16. El escritor y la homologación externa continúan pendientes [cite: 2, 3].

## 1. Contexto y objetivo

Calcular el costo de envío y el plazo estimado de un pedido a partir del destino, de los SKU y cantidades indicados por el canal y de la tarifa vigente de la zona que cubre ese destino. El módulo obtiene los datos físicos de cada producto ante Productos y Ofertas, calcula el peso y el volumen cotizables y devuelve una cotización exacta que los canales comunican al cliente antes de confirmar el pedido.

## 2. Alcance

- Incluye: cotizar con líneas de productos, consultar y validar sus datos físicos en lote, aplicar la tarifa vigente, calcular costo y estimación de entrega y guardar la instantánea exacta exitosa antes de responder; controlar acceso técnico y límites de solicitudes y SKU.
- Fuera de alcance: crear el pedido o el despacho y comunicarse con Ventas y Postventa al cotizar; aplicar promociones, descuentos o envío gratuito; definir o modificar tarifas; resolver zona para F-02 o F-05; aceptar, cancelar, vencer o exponer consultas de cotizaciones; vincularlas automáticamente a pedidos. La auditoría de configuración sigue en ES-F01-08.

## 3. Actor, precondiciones y resultados

- El actor es un canal de venta que obtuvo un token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`.
- La solicitud identifica el destino con `distrito` y contiene `lineas` con `sku` y `cantidad` mayor que cero.
- El módulo puede obtener de Productos y Ofertas el peso y las dimensiones vigentes de cada SKU.
- La zona que cubre el destino está en estado `ACTIVO` y, para devolver costo, tiene una tarifa vigente.
- Disparador: el canal solicita el costo de envío antes de confirmar el pedido.
- Resultado exitoso: cotización exacta con cobertura, zona, totales físicos, costo, moneda, plazo, fecha estimada y marca temporal, cuya instantánea se confirma en Gestión antes de responder. Sin cobertura se informa esa condición sin costo, plazo ni nueva cotización.
- Resultado ante rechazo: error normalizado de autenticación, destino, líneas, productos o límite, sin costo ni creación de recursos [cite: 2].

## 4. Flujo principal y alternativas

1. El canal envía el destino y las líneas del pedido con su token de servicio.
2. El backend valida el token y el destino, y aplica el límite de solicitudes.
3. El sistema evalúa la cobertura del destino y, si existe zona activa, la identifica.
4. Con cobertura, valida las líneas, agrupa los SKU repetidos conservando sus cantidades y verifica el límite de 100 SKU únicos antes de consultar a Productos con su propio token.
5. Valida la estructura e integridad de todo el lote, la existencia, el perfil físico y la elegibilidad comercial de cada SKU conforme al contrato y su homologación pendiente.
6. Calcula los totales, el peso cotizable y el costo con la tarifa capturada de la zona, y obtiene plazo y fecha estimada.
7. Confirma en `cotizaciones` la instantánea completa del cálculo, con vínculos nulos a pedido y despacho; no mantiene una transacción de escritura abierta durante la llamada a G6.
8. Responde con `tipoCotizacion=EXACTA` y los valores del mismo cálculo confirmado.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Sin cobertura | No existe zona activa | Responde sin costo, plazo ni consulta a Productos | CA-02 |
| Líneas inválidas | Lista vacía o cantidad no positiva, con cobertura | Rechaza sin calcular costo | CA-03 |
| Productos inválidos o no disponibles | SKU inexistente, datos incompletos o fallo de consulta | Error normalizado sin estimar costo | CA-04 a CA-06 |
| Sin tarifa | Zona activa sin regla vigente | Confirma cobertura sin costo ni plazo; detalle contractual pendiente | CA-07 |
| Exceso de solicitudes | Se supera el límite por `sub` e IP | Rechaza sin procesar el cálculo | CA-09 |
| Persistencia | Cálculo exacto válido, aunque no exista pedido | Confirma la instantánea antes de responder | CA-11 |
| Cobertura o rechazo | Sin productos, sin cobertura, sin tarifa o cualquier error | No inserta cotizaciones | CA-12 |
| Fallo de escritura | Falla la inserción o el commit local | Error interno sin costo ni fila parcial | CA-13 |
| Lote no conforme | SKU omitidos/duplicados/inesperados o perfil malformado | Rechaza todo el resultado | CA-14 |
| Estado no elegible | Estado comercial no habilitado por H-G2-02 | Rechaza sin confundirlo con inexistencia | CA-15 |
| Exceso de SKU | Más de 100 SKU únicos con cobertura | Rechaza antes de llamar a G6 | CA-16 |

## 5. Reglas, datos e integraciones

### Reglas y validaciones

- La cobertura se evalúa antes que los productos: si no hay zona activa para el destino, el sistema responde sin consultar a Productos y Ofertas ni validar las líneas.
- El canal envía `sku` y `cantidad`; nunca envía peso, volumen, dimensiones ni costo. El sistema no los acepta como entrada autoritativa.
- Los SKU repetidos se agrupan y se consultan una sola vez por producto dentro de la solicitud en lote.
- La agrupación conserva la suma de cantidades y la identidad opaca de cada SKU; no cambia mayúsculas ni ceros iniciales. El límite y la partición completa de la respuesta se rigen por el contrato externo §5.2.1.
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
- Un `sku` correctamente clasificado como inexistente y un error de negocio de datos físicos incompletos se traducen según el contrato externo §5.2.2. Una respuesta `200` que incumple el esquema o el lote se trata como respuesta inválida, no como inexistencia ni como un cálculo parcial.
- Si no es posible consultar a Productos y Ofertas, el sistema responde `503 Service Unavailable` con `DESP_ERROR_PRODUCTOS_NO_DISPONIBLE` y no estima un costo.
- Una zona activa sin tarifa vigente no produce costo ni plazo; el sistema no asume una regla implícita y el tratamiento exacto de este caso permanece como acuerdo pendiente en el contrato.
- El sistema calcula el plazo estimado en días hábiles y la fecha estimada de entrega a partir de la tarifa vigente y del calendario operativo.
- La cotización no crea un pedido ni un despacho y no requiere `Idempotency-Key`: cada ejecución exacta exitosa conserva una instantánea independiente. Repetir puede recalcular y guardar otra fila; no se garantiza deduplicación por contenido ni una tarifa anterior.
- Solo se inserta una fila cuando el resultado completo es exacto y exitoso. La respuesta y la persistencia proceden del mismo cálculo y tarifa capturada; los rechazos y la cobertura sin costo no crean filas.
- `pedido_id` y `despacho_id` quedan nulos. La persistencia sucede antes de una venta confirmada, no porque Ventas invoque esta API. F-02 sigue consultando a Productos y no depende del registro histórico.
- La correspondencia de columnas, el valor físico inicial de estado y el contenido de `detalle` se definen en el modelo de datos §3.1. No se habilitan transiciones de cotización por la mera existencia de columnas [cite: 3].
- La propuesta comercial H-G2-02 y los campos del error G6 siguen pendientes de aceptación bilateral; no se consideran implementados por aparecer en esta especificación [cite: 2].
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

- **DADO** que G6 comunica mediante el error de negocio acordado un SKU sin peso mayor a cero, dimensiones válidas o marca de actualización.
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

### CA-11. Instantánea exacta exitosa sin pedido

- **DADO** un cálculo exacto válido solicitado por un canal antes de confirmar la venta.
- **CUANDO** Gestión completa el cálculo.
- **ENTONCES** confirma una fila coherente con la respuesta, la tarifa capturada y su desglose, con vínculos nulos a pedido/despacho, antes de devolver el costo. Una modificación posterior de tarifa no cambia el registro; repetir la solicitud puede generar otra instantánea.

### CA-12. Exclusión de cobertura y rechazos

- **DADO** una consulta sin líneas, sin cobertura, sin tarifa o rechazada por validación, seguridad, límites o Productos.
- **CUANDO** se procesa la operación compartida.
- **ENTONCES** no aumenta el número de filas de `cotizaciones` ni se insertan totales ficticios.

### CA-13. Fallo al confirmar la instantánea

- **DADO** un cálculo válido cuya inserción o commit local falla.
- **CUANDO** Gestión intenta guardar la cotización.
- **ENTONCES** aplica el error interno de persistencia del contrato, sin costo exitoso ni fila parcial; no lo presenta como caída de G6.

### CA-14. Integridad de la respuesta física

- **DADO** una respuesta `200` con SKU omitidos, duplicados, inesperados o perfil físico malformado.
- **CUANDO** Gestión valida el lote completo.
- **ENTONCES** aplica el error contractual de respuesta inválida sin inventar datos, calcular costos parciales ni guardar cotización.

### CA-15. Estado comercial no elegible

- **DADO** un SKU existente con perfil válido pero estado no elegible conforme a H-G2-02.
- **CUANDO** F-01 valida la cotización.
- **ENTONCES** rechaza por elegibilidad sin presentarlo como inexistente, sin costo ni registro. El escenario de `BORRADOR` está pendiente de homologación externa.

### CA-16. Límite y cantidades del lote

- **DADO** líneas repetidas y destino cubierto.
- **CUANDO** F-01 agrupa los SKU.
- **ENTONCES** conserva la suma de unidades, consulta una sola vez cada SKU hasta 100 únicos y rechaza 101 o más antes de llamar a G6 o insertar una fila. El límite no se aplica a las unidades de un mismo SKU.

## 7. UI, backend y requisitos no funcionales

- UI: no aplica; la presentación del resultado pertenece al canal consumidor. No se incluye `ui.md`.
- Backend: Gestión evalúa cobertura y tarifa, consulta y valida los datos físicos mediante API, calcula y confirma la instantánea exacta en su propia persistencia antes de responder.
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
| CA-11 | Integración PostgreSQL | Fila y respuesta coherentes, vínculos nulos, sustitución de tarifa y repetición |
| CA-12 | Integración PostgreSQL | Comparación de filas antes/después de cobertura y de cada rechazo |
| CA-13 | Integración de fallos | Error en inserción y en commit; rollback y respuesta interna sin costo |
| CA-14 | Contrato e integración | Duplicados en cada arreglo y entre ambos, omisiones, inesperados, JSON/perfil inválido |
| CA-15 | Contrato e integración | Estados homologados, con escenario `BORRADOR` pendiente de aceptación |
| CA-16 | Unitaria e integración | 1, 100 y 101 SKU únicos; más de 100 líneas con pocos SKU y cantidades conservadas |

- [ ] CA-01 a CA-16 cuentan con resultados reproducibles en [evidence.md](./evidence.md).
- [ ] El contrato y los pendientes bloqueantes están resueltos para el alcance implementado.
- [ ] Se verifican agrupación, integridad de SKU, persistencia solo exacta, rollback, ausencia de pedidos/despachos/cobros, seguridad y rendimiento.
- [ ] Los commits y la revisión funcional y técnica están enlazados.

La ejecución se descompone en [tasks.md](./tasks.md). La migración documental no acredita implementación.

## 9. Referencias

- [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-02 y RF-03, CA-07 a CA-11, CA-14 y CA-19 a CA-29; §8.
- [cite: 2] [Contrato externo](../../integraciones/api-contract.md), §§3.4, 3.5, 5.1, 5.2, 10.1 y 11.1.
- [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), §§1.2 y 3.1, tablas `tarifas_zona`, `zonas_codigos_postales` y `cotizaciones`.
- [cite: 4] [Visión general](../../overview.md), sección 7 sobre integración con Productos y Ofertas.
- [cite: 5] [Pendientes](../../funcionalidades/pendiente.md), sección F-01 sobre trabajo futuro.
- Documentos SDD: [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
