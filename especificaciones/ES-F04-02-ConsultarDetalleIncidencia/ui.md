# UI de ES-F04-02: Consultar el detalle de una incidencia

**Responsable:** Gerardo.

**Estado:** Borrador SDD; implementación y verificación pendientes.

**Aplicabilidad:** Página de detalle en la aplicación administrativa.

**Especificación funcional:** [spec.md](./spec.md), CA-01 a CA-11.

## 1. Usuario, contexto y objetivo

- Usuario: Gestor de Despacho autenticado con `GESTOR_DESPACHO`.
- Contexto: centro de despacho, principalmente escritorio; adaptación a tableta y móvil.
- Objetivo: comprender la última incidencia, verificar recepción e historial y abrir únicamente las decisiones permitidas.
- Acceso: `Ver detalle` desde ES-F04-01 o ruta directa `/entregas-fallidas/:idDespacho`. Conservar la consulta de origen en la URL; sin origen, regresar al listado inicial.
- Después de reprogramar o cerrar, la ruta admite consulta histórica con el estado actual y sin acciones de resolución [cite: 1].

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | §§17–18 y 23, P2 y panel de decisión | Disposición, estados, textos, accesibilidad y adaptación. |
| [Diseño F-04](../../disenio/funcionalidades/f-04.md) | Pantalla 2 y navegación a pantallas 3–5 | Bloques de información y destinos. |
| [Componentes React](../../disenio/componentes-react.md) | CR-01/03/05/08/09/18/19; CR-15 al integrar resultados | Acciones, estructura, encabezado, estados, badges, evidencia e historial. |

`PanelDecisionIncidencia`, `ResumenIncidencia` y `RecepcionIncidencia` son composiciones locales propuestas; no crean bibliotecas compartidas nuevas. Los formularios de recepción/reprogramación/cierre pertenecen a ES-F04-03/04/05 y sus propios componentes [cite: 2].

## 3. Pantallas e interacción

### UI-01. Detalle de la incidencia

Composición: estructura administrativa → breadcrumb y H1 con código operativo interno → estado actual y etiquetas → información, recepción e historial a la izquierda; evidencia y decisión a la derecha. Comunicación con Ventas se presenta como bloque de consulta. Una sola acción principal por contexto, según §23 del diseño.

| Bloque | Contenido y comportamiento |
|---|---|
| Identificación | Código, estado actual, última actualización y etiquetas aplicables. Aviso de consulta histórica fuera de `FALLIDO`. |
| Incidencia | Motivo del catálogo, comentario o `Sin comentario`, fecha/hora, repartidor e identificador si falta su nombre. `Intentos consumidos` sobre el máximo vigente. |
| Salida no intentada | `No intentado en esta salida` y explicación de que conserva el acumulado; no se muestra `Intento 0`. |
| Recepción | Pendiente o datos de confirmación de esa incidencia: fecha, usuario, sello Sí/No y observación o `Sin observaciones`. `false` no se interpreta como dato ausente. |
| Historial | CR-19 con todas las operaciones y su orden contractual; distingue recepción sin transición y origen automático. No oculta observaciones necesarias ni recorta entradas silenciosamente. |
| Evidencia | CR-18; solicitud autorizada, carga, visualización y ampliación. Solo la fotografía de la incidencia principal. |
| Decisión | Usa `acciones` del backend y la matriz de `spec.md`, §5.2. Todos los motivos de bloqueo son visibles; recepción ya confirmada y acciones históricas se ocultan según esa matriz. |
| Comunicación con Ventas | Tipo de evento, fecha y estado de envío; sin eventos indica `No hay comunicaciones registradas`. No ofrece reenvío desde esta consulta. |

| Acción | Respuesta de la interfaz | Criterios |
|---|---|---|
| Abrir o cambiar de despacho | Retirar el contenido del recurso anterior, solicitar el actual y distinguir carga de error. | CA-01/04/05/06 |
| Ver o ampliar foto | Solicitar autorización para la referencia actual; mostrar CR-18 y devolver el foco al cerrar. | CA-02/03 |
| Renovar enlace | Solicitar una URL nueva tras validar permisos; descartar una respuesta de otra incidencia. | CA-02/09 |
| Pulsar una decisión | Abrir el formulario propietario con identidad y versión consultadas; no ejecutar una mutación por abrirlo. | CA-07/10/11 |
| Recibir confirmación de recepción | Recargar detalle y actualizar datos, historial y acciones. | CA-10 |
| Reprogramar o cerrar con éxito | Volver al listado, restaurar consulta y recargar filas/indicadores. | CA-10 |
| Regresar o usar el historial del navegador | Conservar filtros, página y tamaño del listado; sin origen, usar su consulta inicial. | CA-10 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Recuperación o acciones | Criterios |
|---|---|---|---|
| Carga inicial | Skeleton y región ocupada; sin datos de otro despacho. | Navegación de regreso; decisiones bloqueadas. | CA-01/04 |
| Datos actuales | Bloques y acciones según respuesta. | Consultar, ampliar foto o abrir formularios permitidos. | CA-01/07 |
| Histórico | Estado actual y última incidencia conservada. | Solo consulta y regreso; sin panel de resolución. | CA-08 |
| `404` | Mensaje distinto para despacho inexistente o sin incidencia, según código. | Volver al listado. | CA-04 |
| Error canónico | Mensaje comprensible sin detalle parcial ni falsa ausencia. | Reintentar. | CA-04/09 |
| Actualización en curso/fallida | Conservar solo contenido autorizado; aviso al fallar y decisiones bloqueadas hasta renovar. | Esperar o reintentar. | CA-10 |
| Nombre/jornada no disponible | Identificador y aviso; atraso desconocido no se presenta como falso ni como cero. | Reintentar sin perder los datos locales. | CA-09 |
| Evidencia ausente | Mensajes distintos para `NO_INTENTADO` y fallo real sin referencia. | Consultar el resto; no buscar foto de una salida anterior. | CA-03 |
| Evidencia expirada/error/sin permiso | Estado de CR-18 específico, sin conservar imagen/URL indebidas. | Renovar o reintentar cuando proceda. | CA-02/05/09 |
| Sin autorización | Retirar detalle, fotografía y URL. | Recuperación de sesión o navegación permitida por la aplicación. | CA-05 |

No aplica un estado vacío de listado ni una confirmación de éxito por este GET. El envío de formularios y sus notificaciones se verifica con las especificaciones propietarias.

## 5. Formularios y mensajes

La página no tiene formulario de modificación propio. Los botones abren los flujos de ES-F04-03/04/05 y conservan la incidencia y versión que esos comandos requieren. Si hay `409`, renovar los datos y pedir revisión antes de otra confirmación; no reenviar automáticamente una decisión sobre una incidencia distinta.

- Los mensajes de bloqueo proceden de códigos contractuales, no de comparar textos de error; máximo y contador se interpolan con valores reales.
- Formatear instantes del servidor en `America/Lima`, diferenciando incidencia, recepción, último cambio de estado y consulta.
- Actualizar la vista activa al menos cada 30 segundos y tras operaciones/conflictos. Si cambia la incidencia, informar y retirar su evidencia previa; las respuestas anteriores no reemplazan la consulta vigente.
- No persistir URLs firmadas ni incluirlas en logs o capturas de pruebas; los modelos HTTP y errores pertenecen a los contratos de [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02) y [Operación §3.4](../../integraciones/api-contract-operacion-reparto.md#34-autorizar-la-lectura-de-evidencia) [cite: 3].

## 6. Accesibilidad y adaptación

- Un H1, secciones identificables y línea de tiempo legible como lista; estados con texto e icono además de color.
- Controles recorribles con teclado, foco visible y razones de bloqueo relacionadas mediante `aria-describedby`.
- Diálogo del visor con título, texto alternativo, cierre con Esc y retorno de foco; imagen ajustada sin recortar evidencia necesaria.
- Anunciar cambios significativos sin repetir la lectura completa en cada actualización. No mover el foco automáticamente por un refresco.
- Dos columnas en escritorio y una en móvil; retirar el comportamiento sticky si dificulta el acceso al contenido. Historial, observaciones y acciones deben permanecer alcanzables [cite: 2].

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterios funcionales |
|---|---|---|---|
| CUI-01 | Abrir fallo real y `NO_INTENTADO`, con cero/un fallo previo y máximo distinto de dos. | Bloques, etiquetas, contador, recepción y fechas correctos; ninguna recepción/foto heredada. | CA-01/03/06/07 |
| CUI-02 | Combinar recepción, anulación y contador menor/igual/mayor al máximo; consultar otro estado. | Acciones y todos sus motivos coinciden con la matriz; histórico sin decisiones. | CA-07/08 |
| CUI-03 | Probar carga, `404`, error canónico y `401/403` después de tener datos. | Estados diferenciados, recuperación y retirada de contenido protegido. | CA-04/05/09 |
| CUI-04 | Abrir/ampliar, vencer/renovar URL y cambiar de despacho/incidencia con respuesta anterior pendiente. | No aparece foto/URL ajena o vencida; cierre y foco funcionan. | CA-02/03/05/06/09 |
| CUI-05 | Mostrar recepción sin transición, orígenes automáticos, fechas empatadas y estados de envío. | Historial completo y estable; comunicaciones separadas; consulta sin efectos. | CA-01/08/11 |
| CUI-06 | Actualizar con temporizador, error, conflicto y formularios; volver a la URL de origen. | Cumple 30 segundos, descarta respuestas obsoletas y restaura/recarga el listado. | CA-10/11 |
| CUI-07 | Simular nombre/jornada y fotografía no disponibles. | Mensajes locales sin inventar datos ni bloquear toda la consulta canónica. | CA-09 |
| CUI-08 | Recorrer con teclado y viewport móvil, incluido visor e historial. | Foco, avisos, textos y acciones utilizables sin desbordar la página. | CA-01/02/07/08/10 |

La implementación visual y sus comprobaciones están pendientes; resultados reales en [evidence.md](./evidence.md). Una prueba con fixtures acredita solo presentación/interacción.

## 8. Referencias

- [cite: 1] [Especificación](./spec.md) y [listado ES-F04-01](../ES-F04-01-ConsultarEntregasFallidas/ui.md).
- [cite: 2] [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md), §23; [componentes React](../../disenio/componentes-react.md), CR-18/19 y §4.5.
- [cite: 3] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §§5.2/5.3; [Operación](../../integraciones/api-contract-operacion-reparto.md), §§3.4/5.4; [plan](./plan.md) y [evidencia](./evidence.md).
