# ES-F01-04: Configurar la tarifa vigente de una zona

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Gestor de Despacho

**UI:** Aplica; formulario de tarifas de la zona (Pantalla 3) de la aplicación administrativa.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación existente en la revisión `12d5041`; migrada al flujo SDD el 15/10/2026, conservando las reglas y los criterios CA-01 a CA-05.

## 1. Contexto y objetivo

La tarifa vigente es la regla de cobro que el motor de cotización aplica a los destinos de una zona. El Gestor la define mediante tarifa base, peso incluido, recargo por kilogramo adicional, factor volumétrico, moneda y plazo estimado en días hábiles. Su consistencia determina el costo que los canales muestran al cliente. Esta especificación concreta RF-02 de la funcionalidad padre y no repite su alcance general [cite: 1].

## 2. Alcance

- Incluye: consultar y guardar la tarifa vigente de una zona; validar la consistencia de la regla; sustituir la tarifa vigente conservando la anterior como histórico.
- Fuera de alcance: calcular el costo de un envío (ES-F01-06); definir rangos de peso por tramos o tarifas planas; aplicar promociones, descuentos o envío gratuito; eliminar o editar tarifas históricas.

## 3. Actor, precondiciones y resultados

- Actor y autorización: el Gestor de Despacho autenticado con un JWT humano de rol `GESTOR_DESPACHO`, conforme a la sección 3.3 del contrato [cite: 2].
- Precondiciones: la zona existe y se encuentra en estado `ACTIVO`; las operaciones se ejecutan contra la tabla propia de tarifas de Gestión de Despachos.
- Disparador: el Gestor abre el panel de tarifas desde el catálogo o desde la notificación de una zona recién creada.
- Resultado exitoso: la nueva regla queda como única tarifa vigente de la zona, la anterior conserva su registro como histórico, y el catálogo se actualiza.
- Resultado ante rechazo: `400 Bad Request` con el detalle de los campos inválidos, `404 Not Found` si la zona no existe, o `403 Forbidden`; no se persiste ninguna regla inválida.

## 4. Flujo principal y alternativas

1. El Gestor abre el panel de tarifas desde el catálogo o desde la notificación de una zona recién creada.
2. Ingresa la tarifa base, el peso incluido, el recargo por kilogramo adicional, el factor volumétrico y el plazo estimado.
3. El frontend valida los campos y deshabilita el guardado mientras falte un dato obligatorio o exista un rango inconsistente.
4. El backend valida el rol y la consistencia de la regla.
5. El sistema deja la nueva regla como única tarifa vigente de la zona, conserva la anterior como histórico y confirma la operación.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Regla inválida | Tarifa base negativa, peso incluido no positivo, factor no positivo o zona inexistente | `400 Bad Request` o `404 Not Found` con el detalle; no persiste | CA-02 |
| Sustitución | Ya existe una tarifa vigente y se guarda una nueva | La nueva queda vigente; la anterior queda inactiva y se conserva | CA-03 |
| Zona sin tarifa | La zona activa no tiene regla vigente | La zona se identifica con la advertencia y no se asume costo por defecto | CA-04 |
| Acceso sin permisos | Usuario sin rol `GESTOR_DESPACHO` | `403 Forbidden` sin información de configuración | CA-05 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | La regla se asocia a una zona existente y en `ACTIVO`; una zona inexistente o inactiva produce `404 Not Found` o `400 Bad Request` según corresponda. | F-01 CA-05, CA-18 |
| RN-02 | La tarifa base y el recargo por kilogramo adicional no pueden ser negativos; el peso incluido debe ser mayor que cero y el factor volumétrico, si se informa, también. | F-01 CA-06 |
| RN-03 | La moneda se expresa en `PEN` y el plazo estimado se informa en días hábiles enteros. | F-01 CA-05 |
| RN-04 | Una regla inválida produce `400 Bad Request` con el detalle de los campos afectados y no persiste nada. | F-01 CA-06 |
| RN-05 | Una zona tiene como máximo una tarifa vigente; al guardar una nueva, la anterior queda inactiva y se conserva como histórico. | F-01 CA-18 |
| RN-06 | La nueva tarifa se aplica a las cotizaciones posteriores; no altera cotizaciones ya emitidas ni los costos ya comunicados a los canales. | F-01 CA-18 |
| RN-07 | Una zona activa sin tarifa vigente es un estado válido y visible, pero no puede producir costo de envío. | F-01 CA-23 |
| RN-08 | El historial de tarifas no se edita ni se elimina desde esta interfaz. | F-01 CA-18 |
| RN-09 | Un usuario sin el rol `GESTOR_DESPACHO` obtiene `403 Forbidden` y no se expone información de configuración. | F-01 CA-04 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `GET /api/v1/zonas/{idZona}/tarifa` | Consultar la tarifa vigente de la zona | [Gestión §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas) |
| `PUT /api/v1/zonas/{idZona}/tarifa` | Guardar la tarifa vigente de la zona | [Gestión §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas) |
| Seguridad y Usuarios | Emite el JWT que habilita el acceso administrativo | Contrato externo §§3.3 y 8 |
| Tabla `tarifas_zona` | Tabla propia de tarifas, con su índice único parcial | [Modelo de datos](../../arquitectura/modelo-datos.md), §3.1 |

El motor de cotización de esta misma funcionalidad consume la tarifa vigente; esta especificación no calcula costos. Los cuerpos y códigos de error se rigen por el contrato de Gestión y sus convenciones compartidas [cite: 2].

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

## 7. UI, backend y requisitos no funcionales

- UI: aplica. La interacción, los estados, la accesibilidad y los criterios de UI se detallan en [ui.md](./ui.md).
- Backend: consulta y alta autorizadas sobre la tabla propia de tarifas; valida la consistencia antes de persistir y garantiza una sola tarifa vigente por zona; no publica eventos.
- Requisitos no funcionales: las operaciones administrativas requieren JWT de rol `GESTOR_DESPACHO`; la identidad y la marca temporal proceden del servidor; las marcas se persisten en UTC y se presentan en `America/Lima`.
- Pendientes: la conciliación entre los campos del contrato y la tabla `tarifas_zona` (peso incluido, plazo estimado, vigencia) se registra en [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración y UI | Zona activa sin tarifa previa; guardado de regla válida. |
| CA-02 | Integración y UI | Reglas con valores negativos o no positivos; zona inexistente. |
| CA-03 | Integración y UI | Zona con tarifa vigente; guardado de una nueva regla. |
| CA-04 | Integración y UI | Zona `ACTIVO` sin regla vigente consultada desde el catálogo. |
| CA-05 | Seguridad e integración | Usuario con otro rol y solicitud sin token. |

- [ ] Los criterios CA-01 a CA-05 y los criterios de UI cuentan con resultados comprobables en [evidence.md](./evidence.md).
- [ ] La equivalencia entre los campos contractuales y la tabla `tarifas_zona` está definida y verificada.
- [ ] La revisión del alcance y los commits de implementación están enlazados.

La descomposición está en [tasks.md](./tasks.md) y los resultados se registrarán en [evidence.md](./evidence.md); todas las comprobaciones de comportamiento están pendientes.

## 9. Referencias

1. [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-02, CA-05, CA-06 y CA-18.
2. [cite: 2] [Contrato de Gestión, sección 3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas); [convenciones compartidas](../../integraciones/api-contract.md#3-convenciones-comunes), secciones 3.3 y 3.5.
3. [cite: 3] [Diseño de F-01](../../disenio/funcionalidades/f-01.md), Pantalla 3; [alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md), panel de tarifas.
4. [cite: 4] [Modelo de datos](../../arquitectura/modelo-datos.md), tabla `tarifas_zona` y su índice único parcial.
5. Archivos de esta especificación: [ui.md](./ui.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
