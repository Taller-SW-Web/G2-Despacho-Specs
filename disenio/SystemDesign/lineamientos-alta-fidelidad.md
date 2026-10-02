# Lineamientos visuales para prototipos de alta fidelidad: Módulo de Despacho

**Módulo:** Despacho y entrega a domicilio
**Fuente obligatoria:** *Guía UX/UI del Marketplace Multicanal* (Inka Athletics) y su [archivo central de Figma](https://www.figma.com/design/rKPdRQHLLUkYk5VdiEErqZ/Sistema-De-Dise%C3%B1o?node-id=57-15)
**Etapa previa:** `lineamientos-wireframes.md` y `funcionalidades/f-0X.md` (baja fidelidad)

---

## 1. Propósito

Este documento traduce el sistema de diseño de Inka Athletics a las pantallas del módulo de Despacho. Los wireframes ya validaron estructura, contenido y flujo; aquí se definen los colores, la tipografía, el layout, los componentes y los estados visuales que deben aplicarse al convertirlos en prototipos.

No se crean tokens nuevos. Cuando el módulo necesita una decisión que la guía no cubre (por ejemplo, el color de cada estado del despacho), se indica como **propuesta del módulo** y debe validarse con el responsable de la biblioteca central.

> **Pendiente de alinear:** `arquitectura/stack-frontend.md` define Tailwind CSS y Recharts, mientras que la guía del marketplace establece Mantine 9.6.2. Los tokens de este documento son válidos en ambos casos, pero el equipo debe decidir la librería antes de implementar.

---

## 2. Base común del módulo

### 2.1. Paleta aplicada

| Token | HEX | Uso en Despacho |
|---|---|---|
| `color/surface/cloud` | `#F7F5F0` | Fondo de todas las pantallas operativas |
| `color/surface/cloud-subtle` | `#EDEAE2` | Fila de indicadores, cabecera de tablas, bloques secundarios |
| `color/surface/ink` | `#1B1812` | Barra lateral administrativa y encabezado móvil |
| `color/surface/ink-soft` | `#26221A` | Hover de ítems en la barra lateral |
| `color/action/primary` | `#F76707` | Acción principal de cada pantalla (texto siempre `ink`) |
| `color/action/primary-hover` | `#C2410C` | Hover del botón principal (texto `cloud`), botones outline y subtle |
| `color/action/primary-soft` | `#FCE3D0` | Fila o tarjeta seleccionada, marca "Siguiente" |
| `color/accent/signal` | `#4361EE` | Solo el indicador de foco de teclado |
| `color/text/primary` | `#1B1812` | Texto principal |
| `color/text/secondary` | `#495057` | Metadatos: códigos, fechas, placas |
| `color/text/disabled` | `#868E96` | Filas atenuadas y acciones no disponibles |
| `color/border/default` | `#DEE2E6` | Bordes de tarjetas, inputs, tablas y divisores |
| Semánticos `success`, `warning`, `error`, `info` | Ver guía | Estados del despacho, ocupación y alertas |

`color/accent/volt` **no se usa** en el módulo: está reservado para promociones y disponibilidad comercial, que no existen en una herramienta operativa. El motivo gráfico de líneas de velocidad tampoco se aplica a pantallas transaccionales; solo podría usarse en la pantalla de acceso de F-03.

**Propuesta del módulo:** las tarjetas, tablas, modales y paneles usan fondo blanco (`cloud.0`, `#FFFFFF`) con `color/border/default`, para separarse del fondo `cloud` sin introducir sombras fuertes.

### 2.2. Tipografía

| Estilo | Fuente | Uso en Despacho |
|---|---|---|
| H1 · 32/40 · 700 | Oswald, mayúsculas | Título de página ("ZONAS Y TARIFAS", "MI RUTA") |
| H2 · 28/36 · 700 | Oswald, mayúsculas | Secciones grandes (poco frecuente en admin) |
| H3 · 24/32 · 700 | Oswald, mayúsculas | Títulos de bloque en detalle (F-04) y valores grandes de tarjetas de resumen |
| H4 · 20/28 · 700 | Inter | Título de modal, panel lateral y tarjeta |
| Subtitle · 18/26 · 600 | Inter | Encabezado de la ruta, nombre del repartidor en detalle |
| Body · 16/24 · 400 | Inter | Texto general, formularios, contenido móvil |
| Body/Small · 14/20 · 400 | Inter | **Celdas de tabla** y contenido denso |
| Label · 14/20 · 600 | Inter | Labels, encabezados de columna, botones |
| Auxiliary · 12/16 · 400 | Inter | Ayudas, "hace 12 min", contador "+2" |

Los códigos (`TRK-78901`, `PED-2026-00891`, placas) usan Inter con `font-variant-numeric: tabular-nums` para que las columnas queden alineadas. No se usa Oswald en labels, badges ni celdas.

### 2.3. Espaciado, radios e iconos

- **Espaciado:** escala de 4 px (`xs` 4, `sm` 8, `md` 16, `lg` 24, `xl` 32). Padding interno de tarjetas y modales: 16 px en móvil y 24 px en escritorio.
- **Radios:** botones, inputs y selects `radius/sm` (8 px); tarjetas y tablas `radius/md` (12 px); modales y paneles laterales `radius/lg` (16 px); badges `radius/full`.
- **Iconos:** Tabler Icons con trazo de 2 px, en 20 px dentro de botones e inputs y 24 px en navegación, con 8 px de separación del texto y color `currentColor`.

| Concepto | Icono Tabler |
|---|---|
| Zonas y tarifas | `IconMapPin` |
| Programación | `IconCalendarTime` |
| Entregas fallidas | `IconPackageOff` |
| Flota | `IconTruck` |
| Repartidor | `IconUser` |
| En camino | `IconTruckDelivery` |
| Evidencia / cámara | `IconCamera` |
| Arrastrar fila | `IconGripVertical` |
| Abrir en mapas | `IconExternalLink` |
| Sin conexión | `IconWifiOff` |

### 2.4. Estados del despacho como badges (propuesta del módulo)

El estado nunca se comunica solo con color: cada badge lleva icono y texto.

| Estado | Variante | Icono | Texto visible |
|---|---|---|---|
| `PENDIENTE_ASIGNACION` | neutral | `IconClock` | Pendiente |
| `ASIGNADO` | info | `IconUserCheck` | Asignado |
| `EN_CAMINO` | info | `IconTruckDelivery` | En camino |
| `ENTREGADO` | success | `IconCircleCheck` | Entregado |
| `FALLIDO` | error | `IconAlertTriangle` | Fallido |
| `DEVUELTO_A_ORIGEN` | warning | `IconArrowBackUp` | Devuelto a origen |
| `CANCELADO` | neutral + texto `disabled` | `IconBan` | Cancelado |

Etiquetas especiales (badge `sm`):

| Etiqueta | Variante | Dónde aparece |
|---|---|---|
| Simulado | neutral con borde punteado | F-02 |
| Programado para [fecha] | info | F-02 |
| Reintento / Intento 2 de 2 | warning | F-02, F-03, F-04 |
| No intentado | neutral | F-04 |
| Pedido anulado | error | F-04 |
| Retorno atrasado | warning | F-04 |
| Activo / Inactivo (zona, repartidor, furgoneta) | success / neutral | F-01, F-05 |

### 2.5. Barras de ocupación (F-02 y F-05)

| Nivel | Rango | Color de la barra | Etiqueta |
|---|---|---|---|
| Normal | menos de 70 % | `color/success/default` | Normal |
| Alta | 70–99 % | `color/warning/default` | Alta |
| Llena | 100 % | `color/error/default` | Llena |

- Altura de la barra: 8 px en tablas, 12 px en tarjetas y encabezados; fondo `cloud-subtle` y radio `full`.
- Siempre con texto a la derecha: `usado / límite unidad (porcentaje)`, por ejemplo "320/500 kg (64 %)".
- La proyección de una asignación (F-02) se dibuja como un segundo segmento rayado a 45° del color del nivel *resultante*, con la leyenda "+12 kg si asignas".

### 2.6. Estructuras de layout

**Aplicación administrativa (F-01, F-02, F-04, F-05).** Frame de 1440 × 1024 px, grilla de 12 columnas, margen de 40 px y gutter de 24 px.

```text
┌────────────┬─────────────────────────────────────────────┐
│            │ Encabezado 64 px (cloud, borde inferior)    │
│  Barra     ├─────────────────────────────────────────────┤
│  lateral   │ H1 + acción principal a la derecha          │
│  256 px    │ Indicadores (opcional)                      │
│  (ink)     │ Filtros                                     │
│            │ Tabla / contenido (fondo blanco, radio 12)  │
└────────────┴─────────────────────────────────────────────┘
```

- La barra lateral tiene fondo `ink` y texto `inverse`, con el logo blanco arriba. El ítem activo lleva fondo `ink-soft`, un indicador izquierdo de 4 px en `action/primary` e icono y texto en `cloud`.
- El encabezado muestra el breadcrumb en Body/Small `secondary` y el usuario a la derecha (avatar de 32 px y nombre).
- Paneles laterales derechos de 560 px y modales `md` (560 px) o `lg` (880 px), todos con `radius/lg`.
- Las notificaciones aparecen arriba a la derecha y se cierran solas a los 4 s; las de error permanecen hasta cerrarse.

**Aplicación del repartidor (F-03).** Frame de 390 × 844 px, margen de 16 px y una sola columna.

```text
┌──────────────────────────┐
│ Encabezado 56 px (ink)   │
├──────────────────────────┤
│ Contenido en cloud       │
│ Tarjetas blancas 16 px   │
│                          │
├──────────────────────────┤
│ Barra de acción fija o   │
│ navegación inferior 64 px│
└──────────────────────────┘
```

- Las áreas táctiles miden como mínimo 48 × 48 px y los botones de acción son `lg`, `fullWidth` y están fijos al pie.
- Por el uso bajo luz solar, todo texto operativo va en `text/primary` sobre blanco o `cloud`; el gris `secondary` queda solo para metadatos.

### 2.7. Reglas de prototipado comunes

- Se usan instancias de la Team Library (Button, TextInput, Select, MultiSelect, Badge, Checkbox) y no copias locales. Los componentes propios del módulo (barra de ocupación, tarjeta de despacho, línea de tiempo) se crean en el archivo del módulo y se proponen a la biblioteca solo si se reutilizan.
- Cada pantalla tiene sus variantes de estado como frames vecinos: normal, carga (skeleton), vacío, error y confirmación.
- El texto sigue el UX Writing de la guía: verbos concretos, primero qué pasó y luego qué hacer, sin códigos HTTP visibles.
- El foco de teclado es un anillo de 2 px en `accent/signal` con desplazamiento de 2 px.

---

## 3. F-01: Gestor de zonas y cotizador (escritorio)

**Layout**

- Panel de zonas: H1 "ZONAS Y TARIFAS" con el botón principal "Nueva zona" (`IconPlus`) a la derecha. Debajo, una barra de filtros en una fila (búsqueda de 4 columnas, distrito de 3, estado de 3 y "Limpiar filtros" subtle) y la tabla en 12 columnas.
- Formulario de zona: formulario en 5 columnas y mapa en 7 (aproximadamente 40/60), con una barra de acciones fija al pie, fondo blanco y borde superior.
- Tarifas: panel lateral derecho de 560 px sobre el listado, con overlay `ink` al 40 %.

**Componentes y tratamiento visual**

- **Tabla de zonas:** los distritos se muestran como hasta tres badges neutral `sm` más "+n" en Auxiliary. La tarifa vigente va en "S/ 10.00" con tabular-nums, o "Sin tarifa" en un badge warning. El estado usa el badge Activo o Inactivo, y las acciones son botones `subtle` con iconos `IconEdit`, `IconCurrencySol`, `IconPower`.
- **Distritos y códigos postales:** MultiSelect `searchable` con Pills removibles.
- **Mapa** (si se mantienen los polígonos; ver la decisión pendiente sobre coordenadas): la zona actual va con relleno `action/primary-soft` al 60 % y borde de 2 px en `action/primary-hover`; las zonas existentes con relleno `cloud-subtle` y borde `border/default`; un solapamiento, con relleno `error/background` y borde discontinuo `error/default`. La barra de herramientas del mapa usa botones de icono de 40 px con `aria-label`.
- **Tabla editable de rangos:** NumberInput `sm` dentro de las celdas, el prefijo "S/" o el sufijo "kg" en `secondary` y el botón "Agregar rango" outline.
- **Modal de desactivación** (`md`): icono `IconAlertTriangle` en `warning`, la cantidad de despachos activos destacada en Subtitle y el botón "Desactivar zona" destructivo (rojo, texto blanco) junto a "Cancelar" outline.

**Estados**

- Carga: 6 filas skeleton.
- Vacío: `IconMapPinOff` de 48 px en `disabled` con el CTA "Nueva zona".
- 403: alerta neutral sin tabla.
- 409 por solapamiento: alerta `error/background` arriba del formulario que nombra la zona y el distrito en conflicto.
- 400: error inline bajo cada campo.

**Interacciones a prototipar:** abrir y cerrar el panel de tarifas con deslizamiento de 200 ms, dibujar un polígono (simulado con dos frames), guardar con notificación de éxito y el flujo de desactivación con su modal.

---

## 4. F-02: Programación y asignación de despachos (escritorio y tableta)

**Layout**

- Las pestañas "Cola de pendientes" y "Rutas por repartidor" (Tabs con subrayado de 2 px en `action/primary`) van bajo el H1 "PROGRAMACIÓN". La acción "Generar pedido de prueba" es outline y queda a la derecha.
- La fila de indicadores tiene 4 tarjetas de 3 columnas cada una, con fondo `cloud-subtle`, el valor en H3 Oswald y la etiqueta en Label.
- En Rutas por repartidor, la lista de repartidores ocupa 4 columnas y la ruta seleccionada 8.
- En tableta de 1024 × 768 px, la barra lateral se colapsa a 72 px (solo iconos) y la tabla oculta las columnas de volumen y tiempo en espera.

**Componentes y tratamiento visual**

- **Tabla de cola:** el código de rastreo va en Label y el pedido en Auxiliary `secondary` debajo. La dirección se trunca a una línea con tooltip. Peso y volumen van alineados a la derecha. El "Tiempo en espera" pasa a texto `warning/default` con `IconClock` cuando supera el umbral acordado. Las etiquetas especiales van junto al código. La acción "Asignar" es un botón principal `sm`.
- **Modal de asignación** (880 px): arriba, un resumen del despacho en una franja `cloud-subtle` (código, zona, peso, volumen). Debajo, una lista de tarjetas de repartidor (Radio card): la seleccionada lleva borde de 2 px en `action/primary` y fondo `primary-soft`, y las que no tienen capacidad suficiente se muestran atenuadas con el motivo en texto ("Excede 12 kg"). Cada tarjeta tiene tres barras de ocupación con proyección rayada. El separador "Otras zonas" es un divider con Label.
- **Ruta del repartidor:** filas con posición en un círculo de 32 px (`ink` con número `cloud`), `IconGripVertical` como asa y los botones de icono "Subir" y "Bajar". Las filas no reordenables (no `ASIGNADO`) van con opacidad del 60 % y sin asa.
- **Barra de cambios sin guardar:** franja fija inferior con fondo `ink`, texto `inverse`, "Descartar" subtle (texto `cloud`) y "Guardar orden" principal.

**Estados**

- Carga: skeleton de tabla y de tarjetas en el modal.
- Cola vacía: "No hay despachos pendientes", con `IconChecks`.
- Fila recién generada: fondo `info/background` que se desvanece en 2 s.
- 409 al guardar el orden: alerta error con el botón "Recargar ruta".

**Interacciones a prototipar:** seleccionar un repartidor y ver cómo cambia la proyección de las barras, arrastrar una fila con su sombra de elevación y el placeholder punteado en la posición destino, guardar el orden y el flujo de reasignación.

---

## 5. F-03: Web del repartidor y evidencia de entrega (móvil)

**Layout**

- El encabezado `ink` de 56 px lleva el título en Subtitle Inter `inverse`, la flecha de regreso de 24 px a la izquierda en las vistas de detalle y el badge de estado operativo a la derecha.
- El progreso de la jornada va bajo el encabezado: texto "4 de 12 despachos resueltos" en Label y una barra de 8 px en `action/primary`. Es progreso, no ocupación, así que no lleva colores semánticos.
- La navegación inferior blanca mide 64 px y tiene borde superior: tres ítems con icono de 24 px y Auxiliary. El ítem activo va en `action/primary-hover` con un indicador superior de 2 px.
- Los formularios tienen el botón de confirmación fijo al pie dentro de una franja blanca con padding de 16 px.

**Componentes y tratamiento visual**

- **Pantalla de acceso:** fondo `ink` con el logo blanco centrado y, opcionalmente, líneas de velocidad sutiles. El formulario va en una tarjeta blanca con `radius/lg` y el botón "Ingresar" es principal `lg` `fullWidth`.
- **Tarjeta de despacho:** la posición va en un círculo de 40 px (`ink` y número `cloud` en Label). Debajo, el código en Body/Small `secondary`, la dirección en Body 600 con un máximo de dos líneas, el destinatario en Body y una fila inferior con el badge de estado y el badge "Intento 1 de 2". La tarjeta "Siguiente" lleva borde de 2 px en `action/primary` y el badge "Siguiente" con fondo `primary-soft`. Toda la tarjeta es tocable, con un mínimo de 96 px de alto.
- **Detalle:** bloques en tarjetas separadas por 16 px (Destinatario, Destino, Despacho). El teléfono es un enlace con `IconPhone` y un área táctil de 48 px. "Abrir en mapas" es un botón outline `fullWidth` con `IconExternalLink`. La barra inferior muestra una sola acción principal según el estado ("Iniciar traslado" o "Confirmar entrega") y "Marcar como fallido" como botón outline rojo (borde y texto `error/default`), para no competir con la principal.
- **Área de fotografía:** contenedor de 240 px de alto con borde discontinuo de 2 px en `border/default` y `radius/md`, `IconCamera` de 48 px y el texto "Toma la foto del paquete entregado". Con foto, se muestra la previsualización a todo el ancho y el botón "Volver a tomar" subtle encima.
- **Motivos de fallo:** Radio cards de 56 px de alto a todo el ancho; la seleccionada lleva borde en `action/primary`.
- **Resumen de jornada:** grilla de 2 × 3 tarjetas con el número en H3 Oswald y la etiqueta en Label; entregados y fallidos llevan un icono semántico.

**Estados**

- Carga: tres tarjetas skeleton.
- Ruta vacía: `IconRoute` de 48 px con "No tienes despachos asignados para hoy".
- Sin conexión: franja fija bajo el encabezado con `warning/background`, `IconWifiOff` y el texto.
- Fuera de turno: franja `info/background` y acciones con estilo `disabled`.
- Subida de foto: barra de progreso en el propio botón (loading) y el texto "Subiendo foto…".
- Error de subida: alerta `error/background` con "Reintentar", conservando la foto.
- Confirmación de fallo: pantalla con `IconArrowBackUp` y el recordatorio de devolver el paquete en Subtitle.

**Interacciones a prototipar:** Mi ruta → detalle → iniciar traslado (el badge cambia a En camino) → confirmar entrega con foto → regreso con notificación; el flujo de fallo, y el cierre de jornada con su diálogo. Conviene probar el prototipo en un celular real con la pantalla al brillo máximo.

---

## 6. F-04: Entregas fallidas y reprogramaciones (escritorio)

**Layout**

- Listado: H1 "ENTREGAS FALLIDAS", fila de 3 indicadores (Recibidos en centro, Pendientes de retorno y Retorno atrasado, este último con borde izquierdo de 4 px en `warning/default`), filtros y tabla.
- Detalle: breadcrumb y encabezado con código en H3 Oswald, badge Fallido y etiquetas especiales. Debajo, dos columnas de 7 y 5 (aproximadamente 60/40); la columna derecha queda fija (sticky) con la evidencia y el panel de decisión.

**Componentes y tratamiento visual**

- **Tabla:** la columna de recepción usa un badge info ("Recibido en centro") o neutral ("Pendiente de retorno"). La de evidencia muestra `IconCamera` en `text/primary` o un guion en `disabled`. Las filas "Recibido en centro" llevan un indicador izquierdo de 4 px en `action/primary` porque esperan una decisión.
- **Línea de tiempo del historial:** puntos de 12 px del color semántico de cada estado, línea de 2 px en `border/default`, estado en Label, fecha y ejecutor en Auxiliary `secondary` y observación en Body/Small.
- **Evidencia:** imagen en proporción 4:3 con `radius/md` y el botón "Ampliar" (`IconZoomIn`), que abre un modal a pantalla completa con fondo `ink`.
- **Panel de decisión:** tarjeta blanca con H4 "Decisión". "Reprogramar" es principal `fullWidth` y "Cerrar como devuelto a origen" es outline. Si el paquete aún no se recibió, ambos botones aparecen deshabilitados con la ayuda "Confirma primero la recepción en centro" y "Confirmar recepción" pasa a ser la acción principal.
- **Modales** (`md`): el de recepción usa un Checkbox de sello y Textarea; si el sello está marcado como "No", las observaciones se resaltan con borde `warning/default` y texto de ayuda. La reprogramación usa DatePickerInput con fechas pasadas deshabilitadas. El cierre usa Select de motivo y un botón destructivo.

**Estados**

- Evidencia cargando: skeleton 4:3.
- Sin evidencia: tarjeta `cloud-subtle` con "No intentado — sin foto".
- Enlace expirado: alerta info con "Volver a cargar".
- Pedido anulado: alerta error arriba del detalle que explica que solo queda cerrar.

**Interacciones a prototipar:** listado → detalle → confirmar recepción (se habilitan las decisiones) → reprogramar con fecha, y el cierre como devuelto a origen con su confirmación.

---

## 7. F-05: Monitoreo de flota y capacidad (escritorio)

**Layout**

- Tablero: H1 "FLOTA" con un indicador de actualización a la derecha ("Actualizado hace 10 s" en Auxiliary con un punto `success` de 8 px). Debajo, 4 tarjetas de resumen de 3 columnas cada una, filtros y la tabla de repartidores en jornada.
- Repartidores y Vehículos: páginas de listado con el patrón de F-01 (H1, acción principal, filtros, tabla). El formulario de repartidor va en un panel lateral de 560 px y el de vehículo en un modal `md`.
- Asignación diaria: formulario en una fila de 3 Selects (repartidor, furgoneta, zona) con el botón principal "Abrir jornada" alineado al final. Debajo, la tabla de jornadas del día.

**Componentes y tratamiento visual**

- **Tarjetas de resumen:** número en H3 Oswald y etiqueta en Label, con un icono de 24 px por estado: Disponible `IconCircleCheck` en `success`, En ruta `IconTruckDelivery` en `info`, Saturado `IconAlertOctagon` en `error` y Fuera de turno `IconMoon` en `disabled`. La tarjeta funciona como filtro rápido: al hacer clic aplica ese estado a la tabla y queda seleccionada con borde `action/primary`.
- **Estado operativo:** badges Disponible (success), En ruta (info), Saturado (error) y Fuera de turno (neutral).
- **Tabla de ocupación:** tres columnas de barra con el patrón de la sección 2.5. La fila con algún límite al 100 % lleva fondo `error/background` y el badge Saturado.
- **Formularios:** NumberInput con sufijos "kg", "m³" y "paquetes". La placa va en mayúsculas automáticas con formato `ABC-123` en la ayuda. La baja lógica se hace con un Switch "Activo" y una confirmación cuando hay historial.

**Estados**

- Carga: skeleton de tarjetas y tabla.
- Sin jornadas abiertas: CTA "Abrir jornada" que lleva a Asignación diaria.
- Error de actualización automática: franja `warning/background` con "No pudimos actualizar el tablero. Reintentaremos en 30 s" y "Actualizar ahora".
- Conflicto al abrir jornada (furgoneta o repartidor ya asignado): error inline en el Select correspondiente.

**Interacciones a prototipar:** el clic en una tarjeta de resumen filtra la tabla, un cambio de ocupación animado (la barra crece y cambia de nivel), el registro de repartidor y vehículo y la apertura de jornada.

---

## 8. Lista de revisión antes de entregar un prototipo

- [ ] Usa instancias de la Team Library y las variables de color de Figma, sin HEX sueltos.
- [ ] Los H1 a H3 van en Oswald mayúsculas; todo lo demás en Inter con los estilos de la escala.
- [ ] La acción principal es naranja con texto `ink`, y hay una sola por pantalla o franja de acciones.
- [ ] No se usa volt; signal solo aparece como foco.
- [ ] Todo estado tiene icono y texto además del color.
- [ ] Las barras de ocupación muestran valor, límite, porcentaje y nivel en texto.
- [ ] Los espaciados están en múltiplos de 4 px y los radios son 8, 12, 16 o full.
- [ ] Hay variantes de carga, vacío, error y confirmación junto a cada pantalla.
- [ ] En F-03, las áreas táctiles miden al menos 48 px y la acción principal queda fija al pie.
- [ ] Los textos siguen el UX Writing de la guía, sin códigos HTTP ni mensajes técnicos.
- [ ] El contraste cumple AA, comprobado con un plugin de contraste en Figma.
