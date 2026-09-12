# Especificación: F-01 - Gestor de Zonas Geográficas y Cotizador de Envíos

## 1. Contexto
La determinación precisa de las tarifas y la cobertura de entrega es el primer paso en el ciclo de despacho comercial. Antes de que una orden sea pagada y enviada a programación, las aplicaciones de venta (tienda web, marketplace, chatbot o carrito de compras) necesitan conocer si la dirección del cliente se encuentra dentro del rango de cobertura y cuál es el costo exacto del flete logístico.

El Gestor de Zonas Geográficas y Cotizador de Envíos opera como un servicio autónomo dentro del módulo de Despacho. Trabaja sobre sus propias tablas maestras de polígonos/distritos y matrices de tarifas, garantizando total independencia operativa al no requerir información de clientes ni depender del estado de las órdenes en curso para realizar sus cálculos.

## 2. Propósito
Permitir la configuración administrativa de las zonas de cobertura logística y la matriz tarifaria de envíos, y exponer un endpoint público y ágil de cotización para calcular el costo de entrega en función del destino, peso, volumen o distancia, proveyendo esta información en tiempo real a los canales de venta.

## 3. Alcance
Incluye:
- Administración de Zonas Geográficas: registro, delimitación y activación/desactivación de distritos, sectores o códigos postales de cobertura.
- Matriz de Tarifas: configuración de reglas de precio basadas en peso (kg), volumen (m³), distancia kilométrica o tarifa plana por zona.
- Endpoint de Cotización de Envíos (`POST /api/v1/zonas/cotizar`): servicio consultado por el carrito de compras o módulos comerciales para obtener el costo de envío y el tiempo estimado de entrega.
- Validación de Cobertura: verificación inmediata de si una dirección o coordenadas geográficas se encuentran dentro de las zonas activas de despacho.

## 4. Requisitos

### Requisito 1: Configuración de Zonas de Cobertura
El sistema DEBE permitir al administrador registrar y delimitar zonas geográficas de atención logística asociadas a distritos o polígonos de servicio.

#### Escenario: Creación exitosa de una zona de cobertura
- DADO que un usuario administrador ingresa el nombre de la zona (ej. "Lima Centro"), distritos comprendidos (Miraflores, San Isidro, Lince) y estado "Activo".
- CUANDO confirma la creación de la zona en el sistema.
- ENTONCES el backend valida que no existan solapamientos conflictivos y registra la zona con identificador único y estado `ACTIVO`.

#### Escenario: Consulta de cobertura para dirección fuera de rango
- DADO que se consulta la cobertura para un distrito no registrado en ninguna zona activa (ej. provincia no cubierta).
- CUANDO el cotizador evalúa la dirección.
- ENTONCES el sistema retorna código `200 OK` con bandera `coberturaDisponible: false` y un mensaje: "La dirección se encuentra fuera de nuestra zona de cobertura".

### Requisito 2: Matriz Tarifaria y Reglas de Cobro
El sistema DEBE permitir parametrizar las reglas de tarificación por zona, soportando esquemas de costo base, recargo por kilogramo adicional y factor de cubicaje volumétrico.

#### Escenario: Configuración de tarifa mixta por peso y zona
- DADO que se configura para la zona "Lima Norte" una tarifa base de 10.00 PEN hasta 3 kg, más 2.00 PEN por cada kg adicional.
- CUANDO se guarda la regla tarifaria.
- ENTONCES el sistema asocia la regla a la zona y la aplica a todas las cotizaciones futuras para ese sector.

### Requisito 3: Cotización en Tiempo Real para Canales de Venta
El sistema DEBE calcular y retornar el costo de envío estimado y los días hábiles de entrega a partir del destino, peso y dimensiones del paquete.

#### Escenario: Cotización exitosa dentro de cobertura
- DADO un paquete de 5 kg con destino a un distrito dentro de la zona "Lima Centro".
- CUANDO el carrito de compras invoca el endpoint `POST /api/v1/zonas/cotizar`.
- ENTONCES el sistema calcula el flete conforme a la matriz tarifaria activa y retorna el monto total calculado junto con la promesa de entrega (ej. "Entrega estimada en 24 a 48 horas").

#### Escenario: Cotización con parámetros de peso inválidos
- DADO una solicitud de cotización con peso negativo o cero.
- CUANDO se envía al endpoint de cotización.
- ENTONCES el sistema rechaza la petición con código `400 Bad Request` indicando "El peso del paquete debe ser mayor a cero".

## 5. Requisitos no funcionales
- **Rendimiento:** El endpoint de cotización debe procesar la solicitud en menos de 100 ms para no perjudicar la experiencia de usuario en el checkout de ventas.
- **Alta Disponibilidad e Independencia:** El motor de cálculo debe operar sobre sus propias tablas maestras de tarifas en memoria caché o base de datos local sin acoplamientos externos.
- **Seguridad:** Los endpoints de administración y configuración de zonas requieren token JWT con rol `ADMIN` o `GESTOR_DESPACHO`. El endpoint de cotización para clientes es de acceso público o protegido por API Key de aplicación.

## 6. Fuera de alcance
- **Procesamiento de pagos:** El cobro efectivo del costo de envío cotizado corresponde a la pasarela de pagos del módulo de Ventas.
- **Generación de despachos:** La creación de la orden de envío formal se produce tras el pago y corresponde a la funcionalidad F-02.
- **Ruteo y asignación:** La asignación de choferes para la zona corresponde a F-02 y F-06.

## Criterio de completitud
La capacidad se considera correctamente implementada cuando:
- El registro de zonas y tarifas funciona sin inconsistencias.
- El endpoint de cotización devuelve tarifas correctas conforme a las reglas configuradas.
- Se valida adecuadamente la cobertura geográfica.
- No se incorporan alcances no especificados.