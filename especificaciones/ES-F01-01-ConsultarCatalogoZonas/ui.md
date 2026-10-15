# UI de ES-F01-01: Consultar el catálogo de zonas de cobertura

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión e implementación.

**Aplicabilidad:** Panel de Gestión de Zonas (Pantalla 1) en la aplicación administrativa.

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Usuario y permisos: Gestor de Despacho con rol `GESTOR_DESPACHO`; sin ese rol se muestra acceso denegado sin datos de configuración.
- Contexto de uso: centro de despacho; uso principal en escritorio, con adaptación responsive.
- Objetivo visible: consultar y filtrar las zonas de cobertura y acceder a su edición, a su tarifa y a su activación o desactivación.
- Acceso y navegación: opción «Zonas y Tarifas» de la barra lateral; ruta frontend propuesta `/zonas`.
- Salidas: «Nueva zona» conduce a ES-F01-02; «Editar» a ES-F01-02; «Tarifas» a ES-F01-04; «Activar» / «Desactivar» a ES-F01-03. Esta especificación prepara sus puntos de entrada; cada flujo se implementa en su propio trabajo [cite: 1, 2].

## 2. Referencias visuales y componentes

| Fuente | Secciones | Aplicación |
|---|---|---|
| [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | Layout administrativo, tablas, filtros y estados | Estructura, tokens y pautas de la pantalla. |
| [Diseño F-01](../../disenio/funcionalidades/f-01.md) | Pantalla 1: Panel de Gestión de Zonas | Contexto, navegación y contenido del listado. |
| [Alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md) | §§2 y 3 | Tabla de zonas, badges de estado y tratamiento visual. |
| [Componentes React](../../disenio/componentes-react.md) | CR-01/02/03/05/06/07/08/09/10/12/15; §4.5 | Contratos de componentes y responsables propuestos. |

El sistema de diseño vigente y la especificación funcional prevalecen sobre fragmentos antiguos del wireframe o de la guía de alta fidelidad: la cobertura se delimita con distritos y códigos postales, sin mapa, sin polígonos y sin rangos de peso por tramos [cite: 1, 2].

## 3. Pantallas e interacción

### UI-01. Panel de Gestión de Zonas

Composición: estructura administrativa CR-03 → encabezado CR-05 → filtros CR-06 → tabla CR-07 con CR-08/09 → paginación. La acción principal es «Nueva zona»; no hay acciones globales de destrucción.

| Elemento | Contenido y comportamiento |
|---|---|
| Encabezado | Un único H1 «Zonas de cobertura», subtítulo breve y botón principal «Nueva zona». |
| Filtros | Búsqueda por nombre, selector de distrito y selector de estado (Todos / Activo / Inactivo) con «Limpiar filtros». |
| Columnas | Nombre de la zona, distritos (hasta tres visibles y un indicador «+n»), códigos postales, tarifa vigente (tarifa base o «Sin tarifa»), estado (Activo / Inactivo), última modificación y acciones. |
| Acciones por fila | «Editar», «Tarifas» y «Activar» / «Desactivar». «Tarifas» permanece deshabilitada en zonas inactivas con el motivo visible «Activa la zona para configurar su tarifa». |
| Advertencia en fila | «Sin tarifa configurada» cuando la zona está activa y no tiene regla vigente. |
| Zonas inactivas | Apariencia atenuada; conservan «Editar» y «Activar». |
| Paginación | Paginación inferior con total de registros. |

| Paso | Acción de la persona | Respuesta de la interfaz | Criterio funcional |
|---|---|---|---|
| 1 | Abrir «Zonas y Tarifas» | Solicitar la primera página y mostrar la carga inicial | CA-01 |
| 2 | Escribir o elegir filtros | Consultar desde la primera página; conservar controles | CA-01, CA-02 |
| 3 | Cambiar de página | Solicitar y presentar la página válida | CA-01 |
| 4 | Elegir «Editar», «Tarifas» o «Activar» / «Desactivar» | Abrir el destino correspondiente | RN-04 |
| 5 | Recibir un rechazo de permisos | Retirar tabla, filtros y datos protegidos | CA-04 |

La desactivación nunca se ejecuta directamente desde la tabla: abre siempre la confirmación de ES-F01-03.

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones disponibles | Criterio |
|---|---|---|---|
| Carga inicial | Filas skeleton en la tabla; sin mensaje de vacío | Esperar la consulta | CA-01 |
| Con datos | Tabla y paginación confirmadas | Filtrar, paginar y abrir destinos | CA-01 |
| Vacío inicial | «Aún no hay zonas de cobertura registradas» | «Nueva zona» | CA-02 |
| Sin resultados | Mensaje diferenciado con enlaces | «Limpiar filtros» | CA-02 |
| Zona sin tarifa | Fila con advertencia «Sin tarifa configurada» | «Tarifas» habilitada solo si la zona está activa | CA-03 |
| Error de red | Mensaje comprensible sin detalle técnico | «Reintentar» conservando filtros | CA-01 |
| Sin permisos | «No tienes permisos para ver la configuración de zonas», sin tabla | Navegación permitida por la aplicación | CA-04 |

Envío de mutación y confirmación de éxito no aplican a esta consulta.

## 5. Formularios y mensajes

Los controles son filtros, no un formulario de modificación. Los nombres de parámetros, límites y DTO definitivos pertenecen al [contrato central](../../integraciones/api-contract.md#91-zonas-y-tarifas); se registran en los pendientes del plan y no se redefine aquí un payload alternativo [cite: 3].

| Control | Obligatorio | Validación y momento | Mensaje visible | Fuente contractual |
|---|---|---|---|---|
| Búsqueda por nombre | No | Texto libre con debounce; consulta al pausar | «Limpiar búsqueda» | Contrato §9.1 (pendiente de detalle) |
| Selector de distrito | No | Selección única | «Todos» por defecto | Contrato §9.1 (pendiente de detalle) |
| Selector de estado | No | Todos / Activo / Inactivo | Sin resultado informado | Contrato §9.1 (pendiente de detalle) |

| Resultado o error de API | Mensaje y comportamiento de UI | Recuperación |
|---|---|---|
| `401` / `403` | Acceso denegado sin datos de configuración | Navegación permitida por la aplicación |
| Error de red o `5xx` | Mensaje comprensible con reintento | «Reintentar» conservando filtros |

La presentación usa fechas de la zona operativa `America/Lima` indicada por el modelo de datos. Los límites del rango y su conversión a los filtros se concretan en los pendientes del plan.

## 6. Accesibilidad y adaptación

- Teclado y foco: recorrer navegación, filtros, tabla, paginación y acciones con teclado; mantener foco visible.
- Etiquetas y avisos: encabezados de tabla, caption y nombres accesibles en controles e iconos; anunciar carga y resultados sin repeticiones innecesarias.
- Percepción: diferenciar estados mediante texto e iconos además de color; no reducir la opacidad de filas completas para indicar inactividad.
- Responsive: aplicar los breakpoints y tokens del diseño; en móvil, permitir desplazamiento dentro de la tabla sin desbordar la página.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Abrir el listado con zonas activas e inactivas y casos especiales | Columnas, badges y advertencia «Sin tarifa» correctos | CA-01, CA-03 |
| CUI-02 | Combinar filtros, cambiar de página y limpiar | Controles, URL y resultados coherentes; la página se reinicia al cambiar filtros | CA-01, CA-02 |
| CUI-03 | Probar carga, cero zonas, cero coincidencias y fallo de red | Estados distintos; limpiar y reintentar realizan la recuperación esperada | CA-01, CA-02 |
| CUI-04 | Recibir `403` después de mostrar datos | Se retiran tabla, filtros y datos protegidos | CA-04 |
| CUI-05 | Recorrer la pantalla con teclado en escritorio y viewport móvil | Controles y acciones alcanzables; foco, nombres accesibles y desplazamiento utilizables | CA-01 a CA-04 |

- Pendientes de diseño: nombres de parámetros, límites y DTO del listado (DT-01 del plan).
- Evidencia prevista: pruebas de interacción, revisión con teclado y capturas de los estados aplicables.

## 8. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-04.
2. [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md), [guía F-01](../../disenio/funcionalidades/f-01.md) y [componentes React](../../disenio/componentes-react.md).
3. [Contrato de API](../../integraciones/api-contract.md), §§3.3, 3.5 y 9.1; [modelo de datos](../../arquitectura/modelo-datos.md), §3.1.
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
