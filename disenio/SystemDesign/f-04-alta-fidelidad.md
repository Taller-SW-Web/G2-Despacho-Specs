# Lineamientos visuales de alta fidelidad: F-04 Entregas fallidas y reprogramaciones

**Módulo:** Despacho y entrega a domicilio
**Responsable:** Gerardo
**Usuario y plataforma:** Gestor de Despacho · escritorio 1440 × 1024 px
**Fuente obligatoria:** *Guía UX/UI del Marketplace Multicanal* (Inka Athletics) y su [archivo central de Figma](https://www.figma.com/design/rKPdRQHLLUkYk5VdiEErqZ/Sistema-De-Dise%C3%B1o?node-id=57-15)
**Wireframe de referencia:** `f-04.md`

---

## 1. Propósito

Este documento define cómo convertir los wireframes de F-04 en prototipos de alta fidelidad con el sistema de diseño de Inka Athletics: colores, tipografía, layout, componentes, estados e interacciones. No se crean tokens nuevos; las decisiones que la guía no cubre se marcan como **propuesta del módulo** y deben validarse con el responsable de la biblioteca central.

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
