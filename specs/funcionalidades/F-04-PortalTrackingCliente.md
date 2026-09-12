# Especificación: F-04 - Portal Web de Tracking de Envíos (Cliente)

## 1. Contexto
En la experiencia de compra de comercio electrónico, los clientes demandan visibilidad y certidumbre sobre el paradero y fecha estimada de entrega de sus pedidos. Para evitar la saturación de canales de soporte al cliente (call centers o mensajería) y mejorar la confianza en el servicio, se requiere un portal web público de seguimiento en tiempo real.

Este portal opera como un módulo de consulta directa en solo lectura sobre el estado de los despachos, garantizando total independencia funcional al no requerir iniciar sesión ni emitir comandos de escritura o modificación sobre la base de datos operativa.

## 2. Propósito
Proveer al cliente final de una interfaz web pública, intuitiva y accesible desde cualquier navegador, donde pueda consultar el estado actualizado de su envío mediante un código de rastreo único, visualizando una línea de tiempo (*timeline*) cronológica con los hitos de entrega y un mapa interactivo con la zona o destino del despacho.

## 3. Alcance
Incluye:
- Buscador público de despachos por código de rastreo (`codigoRastreo` o identificador de pedido).
- Línea de tiempo visual interactiva (*timeline*) que muestra los estados históricos y el estado actual:
  - `REGISTRADO` / `PENDIENTE_ASIGNACION` (Solicitud de envío recibida)
  - `ASIGNADO` (Preparado y asignado a repartidor)
  - `EN_CAMINO` (Repartidor en ruta hacia el domicilio)
  - `ENTREGADO` (Paquete entregado con éxito) o `FALLIDO` / `REPROGRAMADO` (Incidencia en camino y reprogramación programada)
- Visualización de mapa informativo que delimita la zona de entrega y la dirección de destino.
- Datos no sensibles de la entrega: fecha estimada de llegada, franja horaria y estado actual en lenguaje comprensible para el consumidor final.
- Protección y privacidad: anonimización de datos personales sensibles (ej. enmascaramiento parcial de nombres y teléfonos).

## 4. Requisitos

### Requisito 1: Búsqueda y Consulta Pública por Código de Rastreo
El sistema DEBE permitir a cualquier usuario consultar el estado de un despacho ingresando un código de rastreo válido sin requerir registro ni credenciales de acceso.

#### Escenario: Consulta exitosa de despacho activo
- DADO que existe un despacho en tránsito con código de rastreo `TRK-78901`.
- CUANDO el cliente ingresa `TRK-78901` en el portal de tracking y presiona "Rastrear Pedido".
- ENTONCES el sistema consulta el backend y despliega la pantalla de seguimiento con el estado actual del paquete, fecha estimada y línea de tiempo de hitos cumplidos.

#### Escenario: Código de rastreo inexistente o inválido
- DADO que un usuario ingresa un código que no existe en la base de datos (ej. `TRK-00000`).
- CUANDO presiona "Rastrear Pedido".
- ENTONCES el sistema retorna un código `404 Not Found` y muestra una notificación amigable en pantalla: "No encontramos información asociada a este código de rastreo. Por favor, verifica el código ingresado".

### Requisito 2: Visualización de Línea de Tiempo (*Timeline*) de Estados
El sistema DEBE graficar una secuencia temporal clara de los eventos del despacho, indicando fecha, hora y descripción de cada hito alcanzado.

#### Escenario: Visualización de hitos en despacho entregado
- DADO un despacho cuyo estado final es `ENTREGADO`.
- CUANDO el cliente visualiza el detalle del seguimiento.
- ENTONCES la línea de tiempo muestra con indicadores verdes los hitos: "Pedido recibido en centro logístico", "Asignado a transporte", "En camino hacia tu dirección" y "Entregado satisfactoriamente", con sus respectivas marcas de tiempo.

#### Escenario: Visualización de evento de entrega fallida o reprogramada
- DADO un despacho que sufrió una incidencia en ruta y pasó a estado `FALLIDO` o fue reprogramado.
- CUANDO el cliente visualiza el seguimiento.
- ENTONCES el portal muestra un aviso informativo destacado: "No pudimos completar la entrega por ausencia del receptor. Tu paquete será reprogramado para el siguiente día hábil".

### Requisito 3: Visualización de Mapa de Zona de Entrega
El sistema DEBE mostrar un mapa referencial con la ubicación de destino del despacho, garantizando la privacidad de los involucrados.

#### Escenario: Carga de mapa con coordenadas de entrega
- DADO un despacho con coordenadas geográficas válidas de destino.
- CUANDO se renderiza la página de tracking.
- ENTONCES se visualiza un mapa interactivo centrado en el distrito/zona de entrega con un marcador sobre la dirección referencial.

## 5. Requisitos no funcionales
- **Seguridad y Privacidad:** Acceso público de solo lectura sin necesidad de login. Se deben anonimizar los datos del cliente (ej. `C*** M*****`, teléfono `***-**-321`) para cumplir con normativas de protección de datos personales.
- **Rendimiento y Disponibilidad:** El endpoint de tracking debe soportar alto tráfico concurrente y responder en menos de 150 ms, utilizando mecanismos de caché HTTP si el estado no ha cambiado.
- **Responsividad:** Diseño adaptable (*responsive design*) que proporcione una experiencia visual óptima tanto en computadoras de escritorio como en smartphones y tablets.

## 6. Fuera de alcance
- **Seguimiento GPS en vivo del vehículo:** Por razones de seguridad del operador y consumo de recursos, no se transmite la ubicación satelital en tiempo real del repartidor; se muestra la etapa operativa y la zona destino.
- **Modificación o cancelación del despacho por parte del cliente:** Cualquier cambio de dirección o cancelación debe tramitarse a través del canal oficial de Postventa o Atención al Cliente.
- **Gestión operativa interna:** No expone datos de transportistas, placas vehiculares ni costos internos de despacho.

## Criterio de completitud
La capacidad se considera correctamente implementada cuando:
- La consulta pública responde de forma precisa a códigos de rastreo existentes.
- La línea de tiempo refleja fielmente los estados del despacho (`PENDIENTE_ASIGNACION`, `ASIGNADO`, `EN_CAMINO`, `ENTREGADO`, `FALLIDO`).
- Los datos personales sensibles se presentan debidamente enmascarados.
- No se permiten modificaciones ni escrituras desde este portal público.
