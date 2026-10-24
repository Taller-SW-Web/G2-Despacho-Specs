# Pendientes

Este documento centraliza las posibles ampliaciones y los acuerdos que todavía no forman parte del alcance comprometido del módulo de Despacho y Entrega. Los elementos listados no generan criterios de aceptación ni trabajo de implementación hasta que el equipo los apruebe y los incorpore expresamente en la especificación correspondiente.

## F-01: Zonas y tarifas

### Trabajo futuro

- Dibujo y edición de polígonos mediante Leaflet.
- Detección de solapamientos entre polígonos.
- Almacenamiento y consultas de geometrías complejas mediante PostGIS.
- Integración con servicios geográficos pagados, sujeta a evaluación técnica y presupuestal.
- Rangos de peso por tramos adicionales en la matriz tarifaria; la versión vigente solo define tarifa base, peso incluido y recargo por kilogramo adicional.

## F-02: Programación y asignación

### Decisión pendiente de integración

- Acordar con Ventas y Postventa si en algún momento se permitirá cancelar un despacho que ya está `EN_CAMINO`. En el alcance actual la solicitud se rechaza y Ventas recibe el resultado final mediante los eventos de estado.

### Trabajo futuro

- Simulador formal de despachos para pruebas autónomas.
- Asignación automática inteligente de despachos.
- Actualización en tiempo real mediante WebSockets; la versión inicial actualiza la información mediante nuevas consultas al backend.

## F-03: Operación del repartidor

### Política de fotografía acordada

- Formatos permitidos: `image/jpeg`, `image/png` e `image/webp`; tamaño máximo: 2.097.152 bytes (2 MiB), conforme al esquema y contrato de Operación.
- Decisión del 24/10/2026: la app del repartidor reduce la foto en el navegador antes de subirla (lado mayor 1600 px, JPEG de calidad 0,8 a 0,5 hasta quedar bajo 2 MiB). Una foto de cámara Android pesa de 3 a 8 MB, por lo que sin este paso la mayoría se rechazaría. Al re-codificar se descartan los metadatos EXIF, incluida la ubicación; la app lo indica como «sin datos de ubicación». El backend no comprime y solo valida tipo y tamaño ([Operación §3.2](../integraciones/api-contract-operacion-reparto.md#32-autorizar-la-carga-de-evidencia)).

### Pendientes de F-03

- Configurar el bucket privado con los mismos tipos y límite, y verificar de extremo a extremo la carga firmada, la comprobación previa a la asociación y la lectura con URL firmada ([Operación §3.5](../integraciones/api-contract-operacion-reparto.md#35-autorizar-la-lectura-de-evidencia)). Por decisión del equipo, el entorno local no emula Storage: sin las variables `EVIDENCIAS_*` la entrega y el fallo responden `503`.
- Acceso humano: Seguridad y Usuarios debe confirmar el login propuesto en el [contrato externo §8.6](../integraciones/api-contract.md#86-acceso-humano-de-la-app-del-repartidor-propuesto), entregar cuentas de prueba y definir la renovación del token; hoy un token de 15 minutos obliga a reingresar durante la jornada.
- Corte automático de fin de turno (ES-F03-07 CA-03) y bandeja de regularización de jornadas anteriores.
- Operación sin conexión: la app avisa y exige reintento explícito (RN-08); no guarda operaciones para enviarlas después.

### Trabajo futuro

- Compresión avanzada de imágenes o procesamiento de metadatos más allá de la re-codificación actual.

La aplicación no implementará cálculo de rutas ni navegación propia. El repartidor podrá utilizar Waze, Google Maps u otra aplicación externa.

## F-04: Entregas fallidas

### Decisión pendiente de integración

- **Envío de reemplazo sin recojo:** Ventas y Postventa autoriza el reemplazo y solicita una nueva entrega. El recorrido de salida podría reutilizar F-02 y F-03, pero todavía debe acordarse cómo identificar su origen posventa.
- **Recojo de una devolución:** Despacho recoge en el domicilio un producto ya entregado y lo retorna al centro. Requeriría solicitud autorizada, asignación, evidencia de recojo y confirmación de recepción.
- **Cambio combinado:** el repartidor entrega el reemplazo y recoge el producto anterior en una misma visita. Requeriría reglas para completar o rechazar cada parte de la operación y registrar ambas evidencias.

Los tres escenarios permanecen fuera del alcance actual hasta que Ventas y Postventa confirme cuáles necesita y se acuerden sus contratos de integración.

## F-05: Flota y capacidad

### En discusión


### Trabajo futuro

- Monitoreo GPS de las furgonetas.
- Gestión avanzada de mantenimiento; la versión inicial conserva únicamente el estado básico `EN_MANTENIMIENTO`.
- Registro de combustible, kilometraje y costos operativos.
- Gestión de múltiples turnos sofisticados por repartidor o furgoneta.

## Regla para incorporar un elemento

Antes de trasladar un elemento futuro o pendiente al alcance actual se debe:

1. Confirmar su valor y viabilidad con el responsable de la funcionalidad.
2. Acordar las integraciones afectadas con los otros módulos.
3. Actualizar la especificación funcional y sus criterios de aceptación.
4. Actualizar el contrato de API, el modelo de datos y el diseño cuando corresponda.
5. Crear o actualizar las historias de usuario relacionadas.
