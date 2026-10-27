# Tareas de ES-F02-07: Cancelar despacho por anulación del pedido

**Responsable de coordinación:** Tarqui.

**Estado:** Implementada y verificada localmente; no acredita aceptación humana ni Ventas/Seguridad externos reales.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoint de cancelación documentado en api-contract.md §7.2. | Contrato | api-contract.md | CA-01 | Completada |
| T-02 | Reutilizar filtro JWT con identidad `modulo-ventas`, scope y clave estricta. | Seguridad / Backend | Configuración JWT | CA-07 | Completada localmente |
| T-03 | Reglas según estado y marca temporal/versionada de anulación en F-04. | Backend / Dominio | Esquema `despachos` | CA-01, CA-03, CA-04, CA-05 | Completada localmente |
| T-04 | Liberación por reserva con intención/cerco y recuperación hacia adelante. | Backend / Integración | Operación §5.2; Común §7.2.1 | CA-02 | Completada localmente; F-06 real verificado |
| T-05 | Flyway V7, solicitud/resultado durable y confirmación con historial/outbox. | Backend / Datos | Esquema base | CA-06 | Completada localmente |
| T-06 | PostgreSQL, MockMvc, HTTP JDK controlado, React y navegador/API con G2 real. | Calidad / Integración | T-01 a T-05 | CA-01 a CA-07 | Alcance aprobado; dos fallos generales previos registrados en evidence.md |

## 2. Detalle de tareas

### T-01. Validar contrato de API
- Alcance: confirmar operación, tabla de estados y coordinación durable únicamente en [Común §7.2/§7.2.1](../../integraciones/api-contract.md#72-cancelar-por-anulación-del-pedido). Actualizar enlaces a Operación §5.2 sin duplicar el contrato.
- Comprobación: contrato revisado.

### T-02. Seguridad e idempotencia
- Alcance: filtro existente comprueba tipo de servicio, emisor `modulo-ventas` y scope; clave UUID v4 obligatoria. El controlador valida tipos, campos desconocidos, longitudes, pedido y parámetros.
- Comprobación: tests con MockMvc verificando 401 y 403.

### T-03. Máquina de estados de cancelación
- Alcance: `CancelarDespacho` / `CancelacionesPersistencia` implementan las ramas de negocio:
  - `PENDIENTE_ASIGNACION` -> `CANCELADO` (200).
  - `FALLIDO` -> marca temporal `pedido_anulado_en` y versión (202); otra clave no duplica la marca ya registrada.
  - `EN_CAMINO`, `ENTREGADO`, `DEVUELTO_A_ORIGEN`, `CANCELADO` -> conflicto (409), salvo resultado aceptado de la misma clave.
- Comprobación: HTTP/persistencia reales, marca sin transición comercial y decisiones F-04 en ambos órdenes.

### T-04. Liberación de capacidad en Operación
- Alcance: persistir intención/cerco antes de liberar fuera de transacción; confirmar misma reserva/despacho/motivo y luego consolidar `CANCELADO`. No crear otra reserva para compensar. Bloquear traslado, reasignación y movimiento de esa parada mientras sea incierto; recuperar con procesador existente.
- Comprobación: HTTP controlado de éxito, timeout, pérdida de respuesta, referencia/motivo incompatible y rechazo remoto; fallos locales de cada escritura y nueva instancia del coordinador. Recorrido real contra F-06 y consultas F-03.

### T-05. Persistencia idempotente y auditoría
- Alcance: tabla `cancelaciones_despacho`, identidad de servicio/clave/pedido/cuerpo normalizado y resultado original con código HTTP. Auditoría, outbox y resultado en la misma transacción del estado/marca; conservar los huecos históricos de ruta.
- Comprobación: doble petición con la misma clave devuelve el resultado exacto previo.

### T-06. Suite de pruebas de integración
- Alcance: todos los estados y permisos, idempotencia, concurrencia/recuperación, retiro de cola/rutas, capacidad real, marca y cierre F-04. Sin pantalla de cancelación administrativa.
- Comprobación: suites afectadas, tipos, build, navegador y API real en bases desechables; registrar por separado fallos previos de la suite general. No afirmar integración real con Ventas o G7 a partir de dobles locales.
