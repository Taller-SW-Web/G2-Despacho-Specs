# Plan de ES-F02-07: Cancelar despacho por anulación del pedido

**Responsable:** Tarqui.

**Estado:** Coordinación durable implementada y verificada localmente; aceptación humana y proveedores externos reales pendientes.

**UI:** No aplica; endpoint externo REST consumido por `modulo-ventas`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-07 | Especificación atómica SDD. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-08, CA-17, CA-18, CA-19 | Especificación funcional vigente. |
| Contrato de API | [api-contract.md §7.2](../../integraciones/api-contract.md#72-cancelar-por-anulación-del-pedido) | Endpoint canónico de cancelación externa. |
| Integración de Capacidad | [Operación §5.2](../../integraciones/api-contract-operacion-reparto.md#52-gestión-libera-una-reserva-en-operación) | Liberación idempotente por reserva en Operación. |
| Arquitectura y datos | [Modelo de datos](../../arquitectura/modelo-datos.md), §1 y §3.1 | Columna `pedido_anulado` y estados terminales. |

## 2. Estrategia y responsabilidades

El filtro existente exige identidad técnica de Ventas y scope de cancelación. `ControladorCancelacion` valida la entrada y delega en `CancelarDespacho`. `CancelacionesPersistencia` serializa identidad de comando y despacho, registra intención/cerco y resuelve casos locales en una transacción. Para `ASIGNADO`, el cliente F-06 libera **fuera de transacción**, y solo después se consolidan cancelación, historial, resultado y outbox. El contrato canónico es [Común §7.2.1](../../integraciones/api-contract.md#721-coordinación-durable-y-recuperación-de-cancelaciones--es-f02-07).

El diseño anterior «liberar y guardar después» queda sustituido: ninguna llamada remota ocurre antes de registrar la intención. Un resultado desconocido o rollback local conserva el cerco y recupera hacia adelante sobre la misma reserva. Nunca se recrea capacidad como compensación; un fallo persistente mantiene bloqueo para revisión.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| API / Web | Operación externa, validación estricta y autorización previa. | `ControladorCancelacion`, `SolicitudesProgramacion`, seguridad existente. |
| Aplicación | Intención/resultado y recuperación sin HTTP transaccional. | `CancelarDespacho`, `AlmacenCancelaciones`, `PuertoLiberacionCancelacion`. |
| Dominio / Datos | Estado canónico y marca temporal de anulación. | `EstadoDespacho`, `pedido_anulado_en`; sin segundo booleano persistido. |
| Infraestructura | Cerco, PostgreSQL, liberación y outbox existentes. | `CancelacionesPersistencia`, `GuardiaCancelacion`, `CapacidadProgramacionHttp`. |

## 3. Frontend y componentes React

No aplica interfaz directa de usuario. El impacto visual en el frontend administrativo se refleja de manera reactiva:
- Si el despacho estaba en la cola de pendientes (`PENDIENTE_ASIGNACION`), desaparece de la tabla y se actualiza el contador KPI.
- En cancelación de `ASIGNADO`, la ruta muestra operación en proceso y bloquea acciones sobre la parada. Tras confirmación, se retira en la siguiente consulta; las capacidades provienen de F-06. No se añade botón para cancelar como gestor.
- Si el despacho estaba en `FALLIDO`, en la pantalla de Entregas Fallidas (F-04) se visualiza la etiqueta o badge "Pedido anulado" y se deshabilitan las opciones de reprogramación, permitiendo únicamente el cierre como devuelto a origen.

## 4. Backend, persistencia e integraciones

- **Endpoint:** `POST /api/v1/despachos/pedidos/{idPedido}/cancelacion`.
- **Entrada/respuestas:** definición única en Común §7.2/§7.2.1; sin encabezado de versión externo nuevo.
- **Persistencia:** Flyway V7 agrega `cancelaciones_despacho`, unicidad por servicio/clave y una intención pendiente por despacho. Solicitud e intención originales inmutables; resultado con código HTTP y cuerpo. Índice de recuperación y lease de 60 segundos; no expira el cerco.
- **Bloqueos:** identidad de comando, bloqueo `asignacion:<id>` compartido con F-03 y fila canónica. Confirmación remota: jornada antes de fila, compatible con reordenamiento/reasignación. Versión y referencias se comprueban al consolidar. Una asignación/compensación/reasignación pendiente impide preparar otra cancelación.
- **F-04:** usar la fila canónica y `pedido_anulado_en`; si reprogramación gana primero, cancelar el pendiente vigente. Si marca gana, rechazar reprogramación con versión vieja o por pedido anulado. El cierre sigue necesitando recepción física.
- **Auditoría:** `CANCELACION_POR_ANULACION` con servicio emisor, motivo, observación, reserva/jornada originales y liberación confirmada; UTC. La marca de `FALLIDO` se audita sin evento comercial nuevo. Los cancelados reales publican `DESPACHO_CANCELADO`, los simulados no.
- **Rutas:** conservar referencia y secuencia históricas, excluir `CANCELADO` de vista operativa y agregar el cerco de cancelación a la huella. Proyecciones versionadas, eventualmente consistentes.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Aclarar contrato de coordinación, recuperación y validación. | Común §7.2.1. | CA-01 a CA-07. |
| I-02 | API e intención/resultado durable; casos locales y seguridad. | Flyway V7, filtro existente. | CA-01, CA-03, CA-04, CA-05, CA-07. |
| I-03 | Liberación recuperable con cerco y confirmación local. | Operación §5.2; I-02. | CA-02, CA-06. |
| I-04 | Retiro de rutas y coherencia con F-04/outbox. | I-03, consumidores existentes. | CA-01 a CA-06. |
| I-05 | Regresión y navegador/API real G2; evidencia e índice. | I-01 a I-04. | CA-01 a CA-07. |

## 6. Estrategia de verificación

- `CancelacionHttpTests`: MockMvc, PostgreSQL/Testcontainers y servidor HTTP JDK controlado, sin dependencia nueva de WireMock. Estados, clave, permisos, errores, timeout, pérdida de respuesta, rollback y recuperación con otra instancia.
- Pruebas F-04 existentes ampliadas con anulación real por API, rechazo de reprogramación, cierre con nueva versión y orden inverso de decisiones.
- React: parada cancelándose fija y sin reasignación. Navegador contra G2 real: cancelación de pendiente/asignado, retiro de vistas y capacidad exacta tras reintento. API real: fallido anulado, recepción física, liberación, rechazo de reprogramación y cierre.
- No acreditar reinicio real de JVM a partir de una instancia nueva; ni Seguridad G7/Ventas reales a partir de sus identidades controladas. Registrar los fallos previos sin deshabilitar pruebas.
