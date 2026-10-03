# ES-F01-05: Consultar la cobertura de un destino

**Funcionalidad padre:** F-01 — Gestor de zonas geográficas y cotizador de envíos  
**Responsable:** Valqui  
**Estado:** Borrador  
**Actor principal:** Canal de venta

## 1. Objetivo

Permitir que los canales de venta consulten si un destino está dentro de la cobertura del centro de despacho antes de mostrar un costo de envío. La consulta se realiza sin líneas de producto, por lo que responde únicamente con la disponibilidad de cobertura, la zona que cubre el destino y los datos normalizados del destino. Es la operación que el checkout y el chatbot necesitan para decidir si continúan o guían al usuario.

## 2. Actor y precondiciones

- El actor es un canal de venta que obtuvo un token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`.
- La solicitud identifica el destino con `distrito`; `direccion` y `codigoPostal` son opcionales.
- Las zonas y su cobertura se encuentran persistidas por esta misma funcionalidad.

## 3. Flujo principal

1. El canal envía el destino del cliente, con o sin `lineas`.
2. El backend valida el token de servicio y la presencia de `distrito`.
3. El sistema busca la zona activa que contiene el distrito o el código postal del destino.
4. El sistema responde con la disponibilidad de cobertura, el nombre de la zona y los datos del destino.
5. El canal muestra el resultado al usuario; si no hay cobertura, muestra el mensaje correspondiente.

## 4. Reglas y validaciones

- Si la solicitud incluye `lineas`, se procesa como una cotización completa según ES-F01-06; esta especificación describe el caso en que se omiten.
- Sin `lineas`, la respuesta no incluye costo, plazo, `tipoCotizacion` ni datos de productos.
- La cobertura se evalúa contra zonas en estado `ACTIVO`; una zona `INACTIVO` no cubre ningún destino.
- Un destino sin cobertura se responde `200 OK` con `coberturaDisponible: false`, sin zona y con el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura".
- Un destino cubierto se responde `200 OK` con `coberturaDisponible: true` y el nombre de la zona que lo contiene.
- La ausencia de `distrito` produce `400 Bad Request` con `DESP_ERROR_DESTINO_REQUERIDO`.
- La consulta no requiere `Idempotency-Key`, porque no modifica recursos.
- El canal no puede consultar zonas inactivas, tarifas de otras zonas ni información de configuración mediante esta operación.
- El límite de solicitudes por `sub` del token de servicio e IP se aplica también a esta consulta.

## 5. Entradas, salidas e integraciones

### Entradas

- Token de servicio con scope `cotizaciones:calcular`.
- Destino con `distrito` obligatorio y `direccion` o `codigoPostal` opcionales.

### Salidas

- Disponibilidad de cobertura, nombre de la zona y datos del destino, sin costo ni plazo.
- Mensaje de destino fuera de cobertura cuando no existe zona activa.
- Error normalizado ante token ausente, sin `distrito` o por exceso de límite.

### Integraciones

- La cobertura procede de las tablas propias de zonas de Gestión de Despachos.
- Marketplace y Chatbot son los consumidores previstos; Ventas y Postventa puede consultar la cobertura cuando lo requiere.
- Seguridad y Usuarios emite los tokens de servicio con los scopes concedidos.
- La ruta, los cuerpos, las respuestas y los códigos de error se rigen exclusivamente por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Destino dentro de cobertura

- **DADO** un canal con token de servicio válido y un destino cuyo distrito pertenece a una zona activa.
- **CUANDO** envía la solicitud sin `lineas`.
- **ENTONCES** el sistema responde `200 OK` con `coberturaDisponible: true`, el nombre de la zona y los datos del destino, sin costo ni plazo.

### CA-02. Destino fuera de cobertura

- **DADO** un destino cuyo distrito o código postal no pertenece a ninguna zona activa.
- **CUANDO** el canal envía la solicitud.
- **ENTONCES** el sistema responde `200 OK` con `coberturaDisponible: false`, sin zona y con el mensaje de destino fuera de cobertura.

### CA-03. Destino sin distrito

- **DADO** una solicitud que no informa `distrito`.
- **CUANDO** el canal la envía.
- **ENTONCES** el sistema responde `400 Bad Request` con `DESP_ERROR_DESTINO_REQUERIDO` y no evalúa la cobertura.

### CA-04. Acceso sin token de servicio

- **DADO** una solicitud sin token o con un token sin el scope `cotizaciones:calcular`.
- **CUANDO** llega al backend.
- **ENTONCES** el sistema responde `401 Unauthorized` o `403 Forbidden` y no revela si el destino tiene cobertura.

### CA-05. Exceso de límite de solicitudes

- **DADO** que el mismo `sub` e IP superaron el límite configurado.
- **CUANDO** el canal envía una nueva consulta.
- **ENTONCES** el sistema responde `429 Too Many Requests` con `DESP_ERROR_LIMITE_COTIZACION`.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Calcular costo, plazo o fecha estimada de entrega.
- Consultar datos físicos de productos en Productos y Ofertas.
- Registrar pedidos o despachos.
- Crear, editar o cambiar el estado de zonas desde esta operación.

### Referencias

- [cite: 1] `funcionalidades/F-01-Gestor_ZonasGeograficas.md`, RF-03 y RF-04, CA-02, CA-10, CA-19 y CA-20.
- [cite: 2] `integraciones/api-contract.md`, secciones 3.4, 3.5, 5.1 y 15.1.
- [cite: 3] `arquitectura/modelo-datos.md`, tablas `zonas` y `zona_distritos`.
- [cite: 4] `overview.md`, sección 7 sobre integración con Marketplace, Chatbot y Ventas y Postventa.