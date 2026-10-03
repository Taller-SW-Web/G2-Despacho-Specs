# ES-F01-04: Configurar la tarifa vigente de una zona

**Funcionalidad padre:** F-01 — Gestor de zonas geográficas y cotizador de envíos  
**Responsable:** Valqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho defina la regla de cobro de una zona mediante tarifa base, peso incluido, recargo por kilogramo adicional, factor volumétrico, moneda y plazo estimado en días hábiles. La regla vigente es la que aplica el motor de cotización a los destinos de esa zona, por lo que su consistencia determina el costo que los canales muestran al cliente.

## 2. Actor y precondiciones

- El actor está autenticado con un JWT que incluye el rol `GESTOR_DESPACHO`.
- La zona existe y se encuentra en estado `ACTIVO`.
- La operación se ejecuta contra la tabla propia de tarifas de Gestión de Despachos.

## 3. Flujo principal

1. El Gestor abre el panel de tarifas desde el catálogo o desde la notificación de una zona recién creada.
2. Ingresa la tarifa base, el peso incluido, el recargo por kilogramo adicional, el factor volumétrico y el plazo estimado.
3. El frontend valida los campos y deshabilita el guardado mientras falte un dato obligatorio o exista un rango inconsistente.
4. El backend valida el rol y la consistencia de la regla.
5. El sistema deja la nueva regla como única tarifa vigente de la zona, conserva la anterior como histórico y confirma la operación.

## 4. Reglas y validaciones

- La regla se asocia a una zona existente y en estado `ACTIVO`; una zona inexistente o inactiva produce `404 Not Found` o `400 Bad Request` según corresponda.
- La tarifa base y el recargo por kilogramo adicional no pueden ser negativos; el peso incluido debe ser mayor que cero y el factor volumétrico, si se informa, también.
- La moneda se expresa en `PEN` y el plazo estimado se informa en días hábiles enteros.
- Una regla inválida produce `400 Bad Request` con el detalle de los campos afectados y no persiste nada.
- Una zona tiene como máximo una tarifa vigente; al guardar una nueva, la anterior queda inactiva y se conserva como histórico.
- La nueva tarifa se aplica a las cotizaciones posteriores; no altera cotizaciones ya emitidas ni los costos ya comunicados a los canales.
- Una zona activa sin tarifa vigente es un estado válido y visible, pero no puede producir costo de envío.
- El historial de tarifas no se edita ni se elimina desde esta interfaz.
- Un usuario sin el rol `GESTOR_DESPACHO` obtiene `403 Forbidden` y no expone información de configuración.

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador de la zona.
- Tarifa base y moneda.
- Peso incluido en kilogramos.
- Recargo por kilogramo adicional.
- Factor volumétrico, en kilogramos equivalentes por metro cúbico.
- Plazo estimado en días hábiles.
- Identidad y roles obtenidos del JWT.

### Salidas

- Tarifa vigente de la zona y su identificador.
- Registro de la tarifa anterior conservado como histórico.
- Confirmación de la operación y actualización del catálogo.
- Error normalizado ante regla inválida, zona inexistente o falta de permisos.

### Integraciones

- El motor de cotización de esta misma funcionalidad consume la tarifa vigente; esta especificación no calcula costos.
- Seguridad y Usuarios emite el JWT que habilita el acceso administrativo.
- La ruta, el cuerpo de la tarifa, la respuesta y los códigos de error se rigen exclusivamente por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Configuración de una tarifa válida

- **DADO** que se configura para "Lima Norte" una tarifa base de 10.00 PEN hasta 3 kg y un recargo de 2.00 PEN por kilogramo adicional.
- **CUANDO** el Gestor guarda la regla.
- **ENTONCES** el sistema la asocia a la zona como tarifa vigente y la aplica a las cotizaciones siguientes de esa zona.

### CA-02. Rechazo de una regla inválida

- **DADO** una regla con tarifa base negativa, peso incluido no positivo, factor volumétrico no positivo o zona inexistente.
- **CUANDO** el Gestor intenta guardarla.
- **ENTONCES** el sistema responde `400 Bad Request`, detalla los campos inválidos y no persiste la regla.

### CA-03. Sustitución de la tarifa vigente

- **DADO** que una zona tiene una tarifa vigente y el Gestor guarda una nueva regla para ella.
- **CUANDO** el sistema confirma la operación.
- **ENTONCES** la nueva regla queda como única tarifa vigente, la anterior queda inactiva y se conserva como histórico.

### CA-04. Zona sin tarifa vigente

- **DADO** una zona en `ACTIVO` que no tiene ninguna regla vigente.
- **CUANDO** el Gestor consulta el catálogo.
- **ENTONCES** la zona se identifica con la advertencia de zona sin tarifa y el sistema no asume un costo por defecto.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar o guardar la tarifa de una zona.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone información de configuración.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Calcular el costo de un envío con la tarifa configurada.
- Definir rangos de peso por tramos o tarifas planas por zona.
- Aplicar promociones, descuentos o envío gratuito.
- Eliminar o editar tarifas históricas.

### Referencias

- [cite: 1] `funcionalidades/F-01-Gestor_ZonasGeograficas.md`, RF-02, CA-05, CA-06 y CA-18.
- [cite: 2] `integraciones/api-contract.md`, secciones 3.3, 3.5 y 9.1.
- [cite: 3] `disenio/funcionalidades/f-01.md`, Pantalla 3: Formulario de Tarifas de la Zona.
- [cite: 4] `disenio/SystemDesign/f-01-alta-fidelidad.md`, panel de tarifas.
- [cite: 5] `arquitectura/modelo-datos.md`, tabla `tarifas_zona` y su índice único parcial.
- [cite: 6] `funcionalidades/pendiente.md`, sección F-01 sobre trabajo futuro.