# Lineamientos visuales de alta fidelidad: F-01 Gestor de zonas y cotizador

**Módulo:** Despacho y entrega a domicilio
**Responsable:** Valqui
**Usuario y plataforma:** Gestor de Despacho / Administrador · escritorio 1440 × 1024 px
**Fuente obligatoria:** *Guía UX/UI del Marketplace Multicanal* (Inka Athletics) y su [archivo central de Figma](https://www.figma.com/design/rKPdRQHLLUkYk5VdiEErqZ/Sistema-De-Dise%C3%B1o?node-id=57-15)
**Wireframe de referencia:** `f-01.md`

---

## 1. Propósito

Este documento define cómo convertir los wireframes de F-01 en prototipos de alta fidelidad con el sistema de diseño de Inka Athletics: colores, tipografía, layout, componentes, estados e interacciones. No se crean tokens nuevos; las decisiones que la guía no cubre se marcan como **propuesta del módulo** y deben validarse con el responsable de la biblioteca central.

> **Pendiente de alinear:** `arquitectura/stack-frontend.md` define Tailwind CSS y Recharts, mientras que la guía del marketplace establece Mantine 9.6.2. Los tokens de este documento son válidos en ambos casos, pero el equipo debe decidir la librería antes de implementar.

---

## 2. Base visual que aplica

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

### 2.4. Etiquetas de estado

El estado nunca se comunica solo con color: cada badge lleva texto.

| Etiqueta | Variante | Uso |
|---|---|---|
| Activo | success | Zona activa |
| Inactivo | neutral | Zona inactiva |
| Sin tarifa | warning | Zona sin tarifa vigente |
| Distrito | neutral `sm` | Distritos comprendidos en la tabla |

### 2.5. Estructura de layout

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

### 2.6. Reglas de prototipado comunes

- Se usan instancias de la Team Library (Button, TextInput, Select, MultiSelect, Badge, Checkbox) y no copias locales. Los componentes propios del módulo (barra de ocupación, tarjeta de despacho, línea de tiempo) se crean en el archivo del módulo y se proponen a la biblioteca solo si se reutilizan.
- Cada pantalla tiene sus variantes de estado como frames vecinos: normal, carga (skeleton), vacío, error y confirmación.
- El texto sigue el UX Writing de la guía: verbos concretos, primero qué pasó y luego qué hacer, sin códigos HTTP visibles.
- El foco de teclado es un anillo de 2 px en `accent/signal` con desplazamiento de 2 px.

---

## 3. Pantallas y tratamiento visual

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

## 4. Lista de revisión antes de entregar un prototipo

- [ ] Usa instancias de la Team Library y las variables de color de Figma, sin HEX sueltos.
- [ ] Los H1 a H3 van en Oswald mayúsculas; todo lo demás en Inter con los estilos de la escala.
- [ ] La acción principal es naranja con texto `ink`, y hay una sola por pantalla o franja de acciones.
- [ ] No se usa volt; signal solo aparece como foco.
- [ ] Todo estado tiene icono y texto además del color.
- [ ] Los espaciados están en múltiplos de 4 px y los radios son 8, 12, 16 o full.
- [ ] Hay variantes de carga, vacío, error y confirmación junto a cada pantalla.
- [ ] Los textos siguen el UX Writing de la guía, sin códigos HTTP ni mensajes técnicos.
- [ ] El contraste cumple AA, comprobado con un plugin de contraste en Figma.
