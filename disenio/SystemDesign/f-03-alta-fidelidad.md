# Lineamientos visuales de alta fidelidad: F-03 Web del repartidor y evidencia de entrega

**Módulo:** Despacho y entrega a domicilio
**Responsable:** Max Rojas
**Usuario y plataforma:** Repartidor · móvil 390 × 844 px
**Fuente obligatoria:** *Guía UX/UI del Marketplace Multicanal* (Inka Athletics) y su [archivo central de Figma](https://www.figma.com/design/rKPdRQHLLUkYk5VdiEErqZ/Sistema-De-Dise%C3%B1o?node-id=57-15)
**Wireframe de referencia:** `f-03.md`

---

## 1. Propósito

Este documento define cómo convertir los wireframes de F-03 en prototipos de alta fidelidad con el sistema de diseño de Inka Athletics: colores, tipografía, layout, componentes, estados e interacciones. No se crean tokens nuevos; las decisiones que la guía no cubre se marcan como **propuesta del módulo** y deben validarse con el responsable de la biblioteca central.

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

### 2.6. Reglas de prototipado comunes

- Se usan instancias de la Team Library (Button, TextInput, Select, MultiSelect, Badge, Checkbox) y no copias locales. Los componentes propios del módulo (barra de ocupación, tarjeta de despacho, línea de tiempo) se crean en el archivo del módulo y se proponen a la biblioteca solo si se reutilizan.
- Cada pantalla tiene sus variantes de estado como frames vecinos: normal, carga (skeleton), vacío, error y confirmación.
- El texto sigue el UX Writing de la guía: verbos concretos, primero qué pasó y luego qué hacer, sin códigos HTTP visibles.
- El foco de teclado es un anillo de 2 px en `accent/signal` con desplazamiento de 2 px.

---

## 3. Pantallas y tratamiento visual

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

## 4. Lista de revisión antes de entregar un prototipo

- [ ] Usa instancias de la Team Library y las variables de color de Figma, sin HEX sueltos.
- [ ] Los H1 a H3 van en Oswald mayúsculas; todo lo demás en Inter con los estilos de la escala.
- [ ] La acción principal es naranja con texto `ink`, y hay una sola por pantalla o franja de acciones.
- [ ] No se usa volt; signal solo aparece como foco.
- [ ] Todo estado tiene icono y texto además del color.
- [ ] Los espaciados están en múltiplos de 4 px y los radios son 8, 12, 16 o full.
- [ ] Hay variantes de carga, vacío, error y confirmación junto a cada pantalla.
- [ ] Las áreas táctiles miden al menos 48 px y la acción principal queda fija al pie.
- [ ] Los textos siguen el UX Writing de la guía, sin códigos HTTP ni mensajes técnicos.
- [ ] El contraste cumple AA, comprobado con un plugin de contraste en Figma.
