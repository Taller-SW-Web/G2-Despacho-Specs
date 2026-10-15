# UI de ES-F04-01: Consultar entregas fallidas

**Responsable:** Gerardo.

**Estado:** Comportamiento del listado acordado el 15/10/2026; implementación y verificación de UI pendientes.

**Aplicabilidad:** Página de consulta en la aplicación administrativa.

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Usuario: Gestor de Despacho con rol `GESTOR_DESPACHO`.
- Contexto: centro de despacho; uso principal en escritorio, con adaptación a tableta y móvil.
- Objetivo: localizar despachos fallidos, distinguir su recepción y reconocer los retornos atrasados.
- Acceso: opción «Entregas fallidas» de la navegación administrativa; ruta prevista `/entregas-fallidas`.
- Salidas: «Ver detalle» conduce a ES-F04-02 y «Confirmar recepción» inicia ES-F04-03. Esta especificación prepara sus puntos de entrada; los flujos consumidores se implementan en sus propios trabajos [cite: 1, 2].

## 2. Referencias visuales y componentes

| Fuente | Secciones | Aplicación |
|---|---|---|
| [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | §§5.5, 12.3, 13.4, 16.2, 16.4, 17, 18 y 23 | Formato, tabla, estados, accesibilidad y pantalla P1. |
| [Diseño F-04](../../disenio/funcionalidades/f-04.md) | Pantalla 1 | Contexto, navegación y contenido del listado. |
| [Componentes React](../../disenio/componentes-react.md) | CR-01/02/03/05/06/07/08/09/10; §4.5 | Contratos de componentes y responsables propuestos. |

El sistema de diseño vigente y la especificación funcional prevalecen sobre fragmentos antiguos del wireframe: usar «código operativo interno»; comunicar la recepción con los estados de §16.4 y conservar el contraste de las filas [cite: 1, 2].

## 3. Pantallas e interacción

### UI-01. Listado de entregas fallidas

Composición: estructura administrativa CR-03 → encabezado CR-05 → tres indicadores CR-10 → filtros CR-06 → tabla CR-07 con CR-08/09 → paginación. La página carece de una acción global de creación.

| Elemento | Contenido y comportamiento |
|---|---|
| Encabezado | Un único H1 «Entregas fallidas». |
| Indicadores | «Pendientes de retorno», «Recibidos en centro» y «Retornos atrasados». Cifras del backend sobre todo el conjunto filtrado por motivo/fechas, independientes de página y grupo. Los atrasados están incluidos en pendientes. El valor desconocido se muestra como «No disponible», nunca cero. |
| Filtros | Motivo del catálogo completo, incluidos `NO_INTENTADO` e inactivos; fechas de la incidencia vigente y recepción: Todos / Pendiente de retorno / Recibido en centro. Al entrar sin URL previa no se limita ninguna fecha. «Limpiar filtros» elimina motivo, fechas y grupo y vuelve a la primera página, conservando el tamaño elegido. |
| Columnas | Código operativo interno, fecha de incidencia, motivo, «Intentos consumidos» sobre el máximo, repartidor, recepción, indicador de evidencia, etiquetas especiales y acciones. Una fila por despacho, con los datos de su incidencia vigente. |
| Etiquetas | «No intentado en esta salida», «Pedido anulado» y «Retorno atrasado», solo cuando correspondan. La primera no reinicia el contador: puede acompañar «0 de 2» o «1 de 2» bajo «Intentos consumidos». El retorno atrasado destaca la fila y al repartidor según §23.B del diseño. |
| Evidencia | Icono con nombre accesible «Tiene evidencia» o guion; el listado no muestra ni descarga la fotografía. |
| Acciones | «Ver detalle» y, únicamente para recepción pendiente, «Confirmar recepción». La consulta no ejecuta ninguna mutación. |
| Paginación y orden | Primera página y 20 filas por defecto; tamaños de UI 20/50/100 dentro del contrato. Recibidos primero, pendientes después y, en cada grupo, incidencia más antigua primero, con desempate del backend. No reordenar ni paginar localmente. Si una actualización deja la página solicitada después de la última, solicitar la última disponible, o la primera cuando no existan resultados. |

| Acción | Respuesta de la interfaz | Criterio funcional |
|---|---|---|
| Abrir la página | Solicitar la primera página y mostrar la carga inicial. | CA-01 |
| Cambiar filtros | Conservar controles y consultar desde la primera página; una respuesta anterior no reemplaza la consulta vigente. | CA-02 |
| Cambiar de página | Solicitar y presentar la página válida; no volver a paginar localmente una respuesta ya paginada. | CA-01, CA-02 |
| Pulsar un indicador | Conservar motivo/fechas, filtrar el grupo y volver a la primera página. Volver a pulsarlo elimina el grupo. Las otras cifras no cambian por esta selección. «Retornos atrasados» activa recepción pendiente y solo atrasados; elegir recepción desde el selector desactiva solo atrasados. | CA-08 |
| Limpiar filtros | Restablecer filtros, indicadores seleccionados y paginación de manera coherente. | CA-02, CA-03 |
| Recibir un rechazo de permisos | Retirar filas, indicadores y filtros protegidos. | CA-04 |
| Volver del detalle o actualizar tras una recepción | Restaurar la consulta de la URL y volver a obtener filas y cifras. Un reprogramado/cerrado ya no aparece; una incidencia nueva no hereda datos visuales de la anterior. | CA-06, CA-07 |

Ejemplo de indicadores: «7 pendientes», «5 recibidos» y «2 atrasados» describen 12 casos. Una ayuda visible en la tarjeta de atrasados indica «Incluidos en pendientes de retorno». La tarjeta seleccionada refleja el filtro real, también al restaurar una URL. El total de la tabla corresponde al grupo seleccionado; puede diferir de la suma de las dos primeras tarjetas.

Las acciones hacia ES-F04-02/03 deben integrarse con sus implementaciones verificadas. Mientras no existan, su ausencia se registra como dependencia; no se enlazan destinos inexistentes ni se presenta una confirmación ficticia.

## 4. Estados de la interfaz

| Estado | Presentación | Recuperación |
|---|---|---|
| Carga inicial | Skeleton de tabla; región ocupada y sin mensaje de vacío. | Esperar la consulta; filtros accesibles fuera de la región de carga según CR-07. |
| Datos | Filas e indicadores confirmados; resumen de paginación correcto. | Filtrar, paginar y usar los destinos disponibles. |
| Vacío inicial | «No hay entregas fallidas por resolver». | Conservar navegación; no ofrecer crear un fallo desde esta pantalla. |
| Sin coincidencias | Mensaje diferenciado de ausencia de incidencias. | «Limpiar filtros». |
| Error inicial | Mensaje comprensible de CR-08, sin detalles técnicos. | «Reintentar» conservando los filtros. |
| Error de actualización | Conservar datos anteriores solo mientras sigan autorizados, con aviso de que no se actualizaron. | Reintentar; no presentarlos como resultado confirmado de filtros nuevos. |
| Sin permisos | Estado de acceso denegado sin datos, indicadores ni filtros protegidos. | Navegación permitida por la aplicación. |
| Jornada no confirmada | En la fila pendiente: «No se pudo confirmar el cierre de jornada». Sin etiqueta de atrasado ni afirmación de retorno a tiempo. | Reintentar la consulta. |
| Indicador de atrasados desconocido | «No disponible», tarjeta deshabilitada y aviso con la cantidad de retornos que no pudieron evaluarse. Filas y cifras locales siguen visibles. | Reintentar; las tarjetas de recepción siguen disponibles. |
| Error al filtrar solo atrasados | Aviso de dependencia, con filtro conservado. No mostrar un subconjunto como completo ni un falso vacío. | «Reintentar» o «Ver todos los grupos», conservando motivo y fechas. |
| Nombre no recuperado | «Nombre del repartidor no disponible» y su identificador. | Reintentar sin bloquear los demás datos. |

Envío de mutación y confirmación de éxito: no aplican a esta consulta. Las notificaciones posteriores a una recepción pertenecen a ES-F04-03 y a su integración con el listado.

## 5. Formularios y mensajes

Los controles son filtros, no un formulario de modificación. Catálogo, parámetros, límites, errores, respuesta y valores desconocidos están definidos en el [contrato central](../../integraciones/api-contract.md), §§10.4, 11.1 y 13.5. No se define un payload alternativo aquí [cite: 3]. Filtros inválidos muestran la validación correspondiente; no se presentan como «sin coincidencias».

La presentación usa `America/Lima`; ambos días seleccionados se incluyen y pueden usarse límites abiertos conforme al contrato. El listado inicial no presupone «Hoy». «Retorno atrasado» se basa en el cierre manual o automático confirmado de la jornada de esa incidencia, no en la hora del navegador ni en la jornada actual del repartidor.

## 6. Accesibilidad y adaptación

- Recorrer navegación, filtros, tabla, paginación y acciones con teclado; mantener foco visible y etiquetas asociadas.
- Usar encabezados de tabla, caption y nombres accesibles en controles e iconos; anunciar carga y resultados sin repeticiones innecesarias.
- Diferenciar estados mediante texto e iconos además de color. Evitar reducir la opacidad de filas completas.
- Aplicar los breakpoints y tokens de §§6, 17 y 18 del diseño. En móvil, permitir desplazamiento dentro de la tabla, sin desbordar la página ni ocultar las acciones necesarias.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Abrir un listado con fallos antiguos/recientes, varias incidencias, `NO_INTENTADO` con cero/un intento previo y más de una página. | Una fila vigente por despacho, columnas y etiquetas correctas, recibidos primero y antigua primero en cada grupo; el indicador de evidencia no muestra la foto. | CA-01, CA-06, CA-07, CA-09 |
| CUI-02 | Combinar filtros, pulsar tarjetas, cambiar página/tamaño, limpiar y volver del detalle. | Controles, URL y resultados coherentes; indicadores independientes de página/grupo, atraso incluido en pendientes y validación de filtros; no aparecen respuestas anteriores. | CA-02, CA-08, CA-11 |
| CUI-03 | Probar carga, cero incidencias, cero coincidencias y fallo de red. | Estados distintos; limpiar y reintentar realizan la recuperación esperada. | CA-03 |
| CUI-04 | Recibir `403` después de mostrar datos. | Se retiran todos los datos e indicadores protegidos, incluidos los filtros. | CA-04 |
| CUI-05 | Mostrar jornadas cerradas/activas/desconocidas, recepción pendiente/confirmada y nombre ausente. | Atraso solo con cierre confirmado y recepción pendiente; avisos, cifra desconocida, tarjeta deshabilitada y recuperación correctos. | CA-05, CA-10 |
| CUI-06 | Recorrer la pantalla con teclado en escritorio y viewport móvil. | Controles, tarjetas y acciones alcanzables; selección y deshabilitados accesibles, foco, texto y desplazamiento utilizables. | CA-01 a CA-11 |

Los fixtures visuales comprueban presentación e interacción. La definición documental del contrato y fuentes ya existe; su implementación, componentes y comprobación real siguen pendientes. Registrar resultados en [evidence.md](./evidence.md).

## 8. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-11.
2. [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md), [guía F-04](../../disenio/funcionalidades/f-04.md) y [componentes React](../../disenio/componentes-react.md).
3. [Contrato de API](../../integraciones/api-contract.md), §§3.3, 3.5 y 11; [modelo de datos](../../arquitectura/modelo-datos.md), §1.
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
