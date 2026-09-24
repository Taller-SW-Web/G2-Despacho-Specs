# Glosario de Dominio del Módulo de Despacho

Este documento unifica el significado de los términos utilizados en las funcionalidades, el contrato de API, el modelo de datos y los diagramas de arquitectura. No reemplaza las reglas de negocio ni los esquemas definidos en esos documentos.

## 1. Pedidos, despachos y unidades físicas

| Término | Significado dentro del módulo |
|---|---|
| **Pedido** | Compra administrada por Ventas y Postventa. Despacho conserva solamente su identificador y no modifica pagos, importes, productos ni stock. |
| **Despacho** | Entidad operativa propiedad del módulo de Despacho. Representa el proceso de llevar un pedido preparado desde el centro de despacho hasta su destino o devolverlo al centro si no se entrega. |
| **Línea de pedido** | Par formado por `sku` y `cantidad`. Sirve para consultar a Productos y Ofertas los datos físicos necesarios, pero no representa un paquete independiente. |
| **Paquete o bulto físico** | Unidad sellada que ocupa espacio en una furgoneta. Para el alcance inicial, cada pedido genera un despacho con `cantidadPaquetes=1`. |
| **SKU** | Identificador de una presentación concreta de producto, propiedad de Productos y Ofertas. |
| **Centro de despacho** | Único punto operativo desde el que salen los paquetes y al que regresan los no entregados. |

Un pedido puede contener varias líneas y unidades de producto sin dejar de representar un solo paquete dentro del alcance inicial.

## 2. Cobertura, tarifas y cotizaciones

| Término | Significado dentro del módulo |
|---|---|
| **Zona de cobertura** | Agrupación activa de distritos o códigos postales a la que Despacho puede realizar entregas. |
| **Cobertura disponible** | Resultado que indica que un destino pertenece a una zona activa. No implica que ya exista un pedido o despacho. |
| **Tarifa** | Regla de configuración asociada a una zona. Contiene tarifa base, peso incluido, recargo por kilogramo, factor volumétrico, moneda y plazo. |
| **Tarifa base** | Importe mínimo configurado para una zona hasta el peso incluido. Es un dato de configuración, no una cotización ni el precio comercial cobrado al cliente. |
| **Cotización base** | Resultado obtenido enviando solamente el destino. Confirma cobertura y muestra el importe mínimo de la zona como “desde S/ ...”. No considera los productos. |
| **Cotización calculada** | Resultado obtenido enviando destino y líneas de productos. Despacho consulta peso y dimensiones por SKU y calcula el costo logístico con esos datos. En el contrato actual se identifica como `tipoCotizacion=EXACTA`, pero no equivale al precio comercial final. |
| **Costo logístico calculado** | Importe que Despacho comunica como resultado de aplicar sus reglas de cobertura y tarifa. Sirve como insumo para los canales y Ventas. |
| **Importe cobrado al cliente** | Precio comercial decidido por Ventas y Postventa. Puede incorporar promociones, envío gratuito, descuentos o cobro parcial y no pertenece a Despacho. |
| **Plazo estimado** | Cantidad de días hábiles calculada para una zona. Es informativa y no crea por sí misma una fecha comprometida. |

La tarifa base y la cotización base no son sinónimos: la primera es una regla almacenada y la segunda es una respuesta calculada utilizando esa regla. Tampoco debe llamarse “cotización final” a la cotización con productos, porque Ventas conserva la decisión sobre el importe que finalmente cobra.

## 3. Peso, dimensiones y capacidad

| Término | Significado dentro del módulo |
|---|---|
| **Peso del producto** | Peso unitario vigente proporcionado por Productos y Ofertas para un SKU. |
| **Dimensiones del producto** | Largo, ancho y alto unitarios proporcionados por Productos y Ofertas. |
| **Peso total** | Suma de `pesoKg × cantidad` de las líneas del pedido. |
| **Volumen total** | Suma del volumen unitario multiplicado por la cantidad de cada línea. |
| **Peso volumétrico** | Conversión del volumen a un equivalente en kilogramos. La fórmula y el factor definitivos todavía deben cerrarse en F-01. |
| **Peso facturable** | Concepto propuesto para comparar peso real y peso volumétrico al cotizar. Todavía no está definido expresamente en el contrato vigente. |
| **Capacidad de furgoneta** | Límites de peso, volumen y cantidad de paquetes configurados para una furgoneta. |
| **Reserva de capacidad** | Registro creado al asignar un despacho para impedir que dos asignaciones consuman la misma capacidad remanente. |
| **Capacidad remanente** | Diferencia entre los límites de la jornada y las reservas activas de peso, volumen y paquetes. |

## 4. Operación de reparto

| Término | Significado dentro del módulo |
|---|---|
| **Jornada** | Asignación diaria de un repartidor, una furgoneta y una zona de trabajo. |
| **Asignación de despacho** | Operación que reserva capacidad y vincula un despacho pendiente con un repartidor, una jornada y una posición de ruta. |
| **Secuencia de ruta** | Orden operativo en el que el repartidor debe atender sus despachos. No constituye navegación GPS ni optimización automática. |
| **Intento de entrega** | Visita real al destino que termina en entrega o fallo. Un cierre con `NO_INTENTADO` no consume un intento. |
| **Evidencia** | Fotografía obligatoria asociada a una entrega o a un fallo con intento real. |
| **Recepción en centro** | Confirmación de que un paquete `FALLIDO` regresó físicamente. No cambia el estado, pero libera capacidad y habilita la reprogramación o el cierre. |
| **Reprogramación** | Decisión que devuelve un despacho `FALLIDO` recibido en el centro a `PENDIENTE_ASIGNACION` con una nueva fecha programada. |
| **Devolución a origen** | Cierre operativo en `DEVUELTO_A_ORIGEN`; el paquete queda en el centro a disposición de Ventas y Postventa. |

## 5. Integración y trazabilidad

| Término | Significado dentro del módulo |
|---|---|
| **Token de servicio** | Credencial técnica emitida por Seguridad y Usuarios mediante `client_credentials`. Identifica al módulo consumidor y sus scopes. |
| **Idempotencia** | Propiedad que permite repetir una solicitud sin duplicar despachos, reservas, intentos, historial ni eventos. |
| **Webhook** | Petición HTTPS saliente con la que Despacho comunica a Ventas un cambio de estado ya confirmado. |
| **Outbox o bandeja de salida** | Registro transaccional de eventos pendientes que permite enviar y reintentar el webhook sin revertir el cambio de estado. |
| **Proyección de despacho** | Copia mínima y versionada que Operación de Reparto utiliza para mostrar la ruta sin compartir la base de datos de Gestión. |
| **Seguimiento** | Vista resumida del estado y de los hitos del despacho consultada por `idPedido`, sin exponer evidencia, coordenadas ni datos personales. |

## 6. Estados del despacho

Los significados, transiciones, precondiciones y transiciones prohibidas se definen en [Diagrama de estados del despacho](./diagrama-estados-despacho.md).
