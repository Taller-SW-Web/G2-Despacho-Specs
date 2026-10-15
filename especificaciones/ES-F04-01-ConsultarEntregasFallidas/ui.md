# UI de ES-F04-01: Consultar entregas fallidas

**Responsable:** Gerardo.

**Estado:** Borrador; pendiente de revisión e implementación.

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
| Indicadores | «Pendientes de retorno», «Recibidos en centro» y «Retornos atrasados». No calcular totales globales desde la página actual ni convertir valores ausentes en cero. Su fuente y relación con los filtros quedan pendientes en DT-01 del plan. |
| Filtros | Motivo, rango de fecha del incidente y recepción: Todos / Pendiente de retorno / Recibido en centro. «Limpiar filtros» restablece la consulta y la primera página. |
| Columnas | Código operativo interno, fecha del incidente, motivo, intento sobre máximo configurado, repartidor, recepción, indicador de evidencia, etiquetas especiales y acciones. |
| Etiquetas | «No intentado», «Pedido anulado» y «Retorno atrasado», solo cuando correspondan. El retorno atrasado destaca la fila y al repartidor según §23.B del diseño. |
| Evidencia | Icono con nombre accesible «Tiene evidencia» o guion; el listado no muestra ni descarga la fotografía. |
| Acciones | «Ver detalle» y, únicamente para recepción pendiente, «Confirmar recepción». La consulta no ejecuta ninguna mutación. |
| Paginación y orden | Usar el total confirmado y el orden del backend. El diseño pide recibidos primero; el orden estable y el desempate se concretan en DT-01 antes de la integración. |

| Acción | Respuesta de la interfaz | Criterio funcional |
|---|---|---|
| Abrir la página | Solicitar la primera página y mostrar la carga inicial. | CA-01 |
| Cambiar filtros | Conservar controles y consultar desde la primera página; una respuesta anterior no reemplaza la consulta vigente. | CA-02 |
| Cambiar de página | Solicitar y presentar la página válida; no volver a paginar localmente una respuesta ya paginada. | CA-01, CA-02 |
| Limpiar filtros | Restablecer filtros, indicadores seleccionados y paginación de manera coherente. | CA-02, CA-03 |
| Recibir un rechazo de permisos | Retirar filas, indicadores y filtros protegidos. | CA-04 |

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

Envío de mutación y confirmación de éxito: no aplican a esta consulta. Las notificaciones posteriores a una recepción pertenecen a ES-F04-03 y a su integración con el listado.

## 5. Formularios y mensajes

Los controles son filtros, no un formulario de modificación. Los códigos del catálogo, nombres de parámetros, límites, errores y DTO definitivos pertenecen al [contrato central](../../integraciones/api-contract.md#11-api-de-f-04-entregas-fallidas). DT-01 del plan debe resolverlos antes de conectarlos por HTTP; no se define un payload alternativo aquí [cite: 3].

La presentación usa fechas de la zona operativa `America/Lima` indicada por el modelo de datos. Los límites del rango y su conversión a los filtros de la API se concretan en DT-01. Un indicador de «Retorno atrasado» se basa en el cierre de jornada confirmado por el servicio responsable, no solo en la hora del navegador.

## 6. Accesibilidad y adaptación

- Recorrer navegación, filtros, tabla, paginación y acciones con teclado; mantener foco visible y etiquetas asociadas.
- Usar encabezados de tabla, caption y nombres accesibles en controles e iconos; anunciar carga y resultados sin repeticiones innecesarias.
- Diferenciar estados mediante texto e iconos además de color. Evitar reducir la opacidad de filas completas.
- Aplicar los breakpoints y tokens de §§6, 17 y 18 del diseño. En móvil, permitir desplazamiento dentro de la tabla, sin desbordar la página ni ocultar las acciones necesarias.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Abrir un listado con los indicadores y casos especiales de prueba. | Columnas, etiquetas y recepción correctas; el indicador de evidencia no muestra la foto. | CA-01 |
| CUI-02 | Combinar filtros, cambiar página, limpiar y volver del detalle disponible. | Controles, URL y resultados coherentes; se reinicia la página al cambiar filtros y no aparecen respuestas anteriores. | CA-02 |
| CUI-03 | Probar carga, cero incidencias, cero coincidencias y fallo de red. | Estados distintos; limpiar y reintentar realizan la recuperación esperada. | CA-03 |
| CUI-04 | Recibir `403` después de mostrar datos. | Se retiran todos los datos e indicadores protegidos, incluidos los filtros. | CA-04 |
| CUI-05 | Mostrar jornadas cerradas/activas con recepción pendiente/confirmada. | «Retorno atrasado» aparece solo para jornada cerrada y recepción pendiente. | CA-05 |
| CUI-06 | Recorrer la pantalla con teclado en escritorio y viewport móvil. | Controles y acciones alcanzables; foco, nombres accesibles, texto y desplazamiento utilizables. | CA-01 a CA-05 |

Los fixtures visuales permiten comprobar presentación e interacción; la integración real queda pendiente hasta cerrar el contrato, las fuentes de datos y los componentes necesarios. Registrar resultados en [evidence.md](./evidence.md).

## 8. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-05.
2. [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md), [guía F-04](../../disenio/funcionalidades/f-04.md) y [componentes React](../../disenio/componentes-react.md).
3. [Contrato de API](../../integraciones/api-contract.md), §§3.3, 3.5 y 11; [modelo de datos](../../arquitectura/modelo-datos.md), §1.
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
