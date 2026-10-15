# ES-F01-05: Consultar la cobertura de un destino

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Canal de venta

**UI:** No aplica. Es una operación de API consumida por Marketplace y Chatbot; no posee interfaz propia en la aplicación administrativa ni en el módulo. La justificación se amplía en [plan.md, sección 1](./plan.md#1-entradas-y-revisiones).

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación existente en la revisión `12d5041`; migrada al flujo SDD el 15/10/2026, conservando las reglas y los criterios CA-01 a CA-05.

## 1. Contexto y objetivo

La consulta de cobertura permite que los canales de venta sepan si un destino está dentro de la cobertura del centro de despacho antes de mostrar un costo de envío. La consulta se realiza sin líneas de producto, por lo que responde únicamente con la disponibilidad de cobertura, la zona que cubre el destino y los datos normalizados del destino. Es la operación que el checkout y el chatbot necesitan para decidir si continúan o guían al usuario. Esta especificación concreta RF-03 y RF-04 de la funcionalidad padre y no repite su alcance general [cite: 1].

## 2. Alcance

- Incluye: evaluar la cobertura de un destino sin líneas de producto; devolver disponibilidad, zona y datos normalizados del destino; aplicar el límite de solicitudes por `sub` e IP.
- Fuera de alcance: calcular costo, plazo o fecha estimada (ES-F01-06); consultar datos físicos de productos; registrar pedidos o despachos; crear, editar o cambiar el estado de zonas; resolver la zona para módulos internos (ES-F01-07).

## 3. Actor, precondiciones y resultados

- Actor y autorización: un canal de venta con un token de servicio (`tipo=servicio`) y scope `cotizaciones:calcular`, conforme a la sección 3.4 del contrato [cite: 2]. Marketplace y Chatbot son los únicos consumidores previstos; Ventas y Postventa no invoca esta operación.
- Precondiciones: la solicitud identifica el destino con `distrito`; `direccion` y `codigoPostal` son opcionales; las zonas y su cobertura están persistidas por esta misma funcionalidad.
- Disparador: el canal envía el destino del cliente, con o sin `lineas`.
- Resultado exitoso: `200 OK` con `coberturaDisponible`, el nombre de la zona y los datos del destino, sin costo ni plazo.
- Resultado ante rechazo: `400 Bad Request` con `DESP_ERROR_DESTINO_REQUERIDO` si falta `distrito`; `401 Unauthorized` o `403 Forbidden` sin el scope requerido; `429 Too Many Requests` con `DESP_ERROR_LIMITE_COTIZACION` al exceder el límite.

## 4. Flujo principal y alternativas

1. El canal envía el destino del cliente, con o sin `lineas`.
2. El backend valida el token de servicio y la presencia de `distrito`.
3. El sistema busca la zona activa que contiene el distrito o el código postal del destino.
4. El sistema responde con la disponibilidad de cobertura, el nombre de la zona y los datos del destino.
5. El canal muestra el resultado al usuario; si no hay cobertura, muestra el mensaje correspondiente.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Destino fuera de cobertura | El distrito o código postal no pertenece a ninguna zona activa | `200 OK` con `coberturaDisponible: false` y el mensaje de destino fuera de cobertura | CA-02 |
| Destino sin distrito | La solicitud no informa `distrito` | `400 Bad Request` con `DESP_ERROR_DESTINO_REQUERIDO`; no evalúa la cobertura | CA-03 |
| Token ausente o sin scope | Sin token o con un token sin `cotizaciones:calcular` | `401` o `403`; no revela si el destino tiene cobertura | CA-04 |
| Exceso de límite | El mismo `sub` e IP superaron el límite configurado | `429 Too Many Requests` con `DESP_ERROR_LIMITE_COTIZACION` | CA-05 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Si la solicitud incluye `lineas`, se procesa como una cotización completa según ES-F01-06; esta especificación describe el caso en que se omiten. | F-01 CA-10 |
| RN-02 | Sin `lineas`, la respuesta no incluye costo, plazo, `tipoCotizacion` ni datos de productos. | F-01 CA-02, CA-19 |
| RN-03 | La cobertura se evalúa contra zonas `ACTIVO`; una zona `INACTIVO` no cubre ningún destino. | F-01 CA-13 |
| RN-04 | Un destino sin cobertura se responde `200 OK` con `coberturaDisponible: false`, sin zona y con el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura". | F-01 CA-19 |
| RN-05 | Un destino cubierto se responde `200 OK` con `coberturaDisponible: true` y el nombre de la zona que lo contiene. | F-01 CA-19 |
| RN-06 | La ausencia de `distrito` produce `400 Bad Request` con `DESP_ERROR_DESTINO_REQUERIDO`. | F-01 CA-20 |
| RN-07 | La consulta no requiere `Idempotency-Key`, porque no modifica recursos. | F-01 CA-20 |
| RN-08 | El canal no puede consultar zonas inactivas, tarifas de otras zonas ni información de configuración mediante esta operación. | F-01 CA-20 |
| RN-09 | El límite de solicitudes por `sub` del token de servicio e IP se aplica también a esta consulta. | F-01 CA-14 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `POST /api/v1/cotizaciones` (sin `lineas`) | Evaluar cobertura y devolver disponibilidad | [Contrato §5.1](../../integraciones/api-contract.md#51-cotizaciones) |
| Seguridad y Usuarios | Emite los tokens de servicio con los scopes concedidos | Contrato §§3.4 y 8 |
| Tablas `zonas` y `zona_distritos` | Fuente de la cobertura | [Modelo de datos](../../arquitectura/modelo-datos.md), §3.1 |
| Límite `LIMITE_COTIZACIONES_POR_MINUTO` | Control de tasa por `sub` e IP | [Modelo de datos](../../arquitectura/modelo-datos.md), parámetros globales |

Los errores `DESP_ERROR_*` y el formato de respuesta se rigen por el contrato central [cite: 2].

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

## 7. UI, backend y requisitos no funcionales

- UI: no aplica. Es una operación de API de servicio; la consumen Marketplace y Chatbot, que son responsables de su propia interfaz. No se crea `ui.md`.
- Backend: operación de solo lectura autorizada por token de servicio; evalúa la cobertura contra zonas `ACTIVO`; no modifica recursos ni publica eventos.
- Requisitos no funcionales: la operación requiere token de servicio con `cotizaciones:calcular`; aplica el límite de tasa por `sub` e IP; no expone configuración interna; las fechas se presentan en `America/Lima` si aplican.
- Pendientes: el tratamiento de un destino cubierto por una zona `ACTIVO` sin tarifa vigente no corresponde a esta operación (es propia de ES-F01-06) y el detalle del DTO de respuesta se registra en [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración | Destino en un distrito de una zona activa; token válido; sin `lineas`. |
| CA-02 | Integración | Destino fuera de toda zona activa. |
| CA-03 | Integración | Solicitud sin `distrito`. |
| CA-04 | Seguridad e integración | Solicitud sin token y con token sin scope. |
| CA-05 | Integración y límite | Mismo `sub` e IP por encima del límite configurado. |

- [ ] Los criterios CA-01 a CA-05 cuentan con resultados comprobables en [evidence.md](./evidence.md).
- [ ] El DTO de respuesta y los errores del contrato están definidos y verificados.
- [ ] La revisión del alcance y los commits de implementación están enlazados.

La descomposición está en [tasks.md](./tasks.md) y los resultados se registrarán en [evidence.md](./evidence.md); todas las comprobaciones de comportamiento están pendientes.

## 9. Referencias

1. [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-03 y RF-04, CA-02, CA-10, CA-19 y CA-20.
2. [cite: 2] [Contrato de API](../../integraciones/api-contract.md), secciones 3.4, 3.5, 5.1 y 15.1.
3. [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), tablas `zonas` y `zona_distritos`; parámetro `LIMITE_COTIZACIONES_POR_MINUTO`.
4. Archivos de esta especificación: [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
