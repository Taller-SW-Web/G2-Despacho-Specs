# Pendientes

Este documento centraliza las posibles ampliaciones y los acuerdos que todavía no forman parte del alcance comprometido del módulo de Despacho y Entrega. Los elementos listados no generan criterios de aceptación ni trabajo de implementación hasta que el equipo los apruebe y los incorpore expresamente en la especificación correspondiente.

## F-01: Zonas y tarifas

### Trabajo futuro

- Dibujo y edición de polígonos mediante Leaflet.
- Detección de solapamientos entre polígonos.
- Almacenamiento y consultas de geometrías complejas mediante PostGIS.
- Integración con servicios geográficos pagados, sujeta a evaluación técnica y presupuestal.

## F-02: Programación y asignación

### Decisión pendiente de integración

- Acordar con Ventas y Postventa si en algún momento se permitirá cancelar un despacho que ya está `EN_CAMINO`. En el alcance actual la solicitud se rechaza y Ventas recibe el resultado final mediante los eventos de estado.

### Trabajo futuro

- Simulador formal de despachos para pruebas autónomas.
- Asignación automática inteligente de despachos.
- Actualización en tiempo real mediante WebSockets; la versión inicial actualiza la información mediante nuevas consultas al backend.

## F-03: Operación del repartidor

### Decisión pendiente sobre fotografías

- Definir si se aplicará compresión básica en el navegador.
- Definir si se eliminarán metadatos EXIF y en qué componente se realizará.
- Acordar formatos permitidos y tamaño máximo de archivo.
- Elegir el mecanismo de almacenamiento y acceso autorizado a las evidencias.

### Trabajo futuro sujeto a la decisión anterior

- Compresión avanzada de imágenes en el navegador.
- Procesamiento sofisticado de metadatos de las fotografías.

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
