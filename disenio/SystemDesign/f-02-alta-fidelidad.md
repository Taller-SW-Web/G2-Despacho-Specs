# Lineamientos visuales de alta fidelidad: F-02 Programación y asignación de despachos

**Módulo:** Despacho y entrega a domicilio
**Responsable:** Tarqui
**Usuario y plataforma:** Gestor de Despacho · escritorio 1440 × 1024 px y tableta 1024 × 768 px
**Fuente obligatoria:** *Guía UX/UI del Marketplace Multicanal* (Inka Athletics) y su [archivo central de Figma](https://www.figma.com/design/rKPdRQHLLUkYk5VdiEErqZ/Sistema-De-Dise%C3%B1o?node-id=57-15)
**Wireframe de referencia:** `f-02.md`

---

## 1. Propósito

Este documento define cómo convertir los wireframes de F-02 en prototipos de alta fidelidad con el sistema de diseño de Inka Athletics: colores, tipografía, layout, componentes, estados e interacciones. No se crean tokens nuevos; las decisiones que la guía no cubre se marcan como **propuesta del módulo** y deben validarse con el responsable de la biblioteca central.

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

### 2.5. Barras de ocupación (F-02 y F-05)

| Nivel | Rango | Color de la barra | Etiqueta |
|---|---|---|---|
| Normal | menos de 70 % | `color/success/default` | Normal |
| Alta | 70–99 % | `color/warning/default` | Alta |
| Llena | 100 % | `color/error/default` | Llena |

- Altura de la barra: 8 px en tablas, 12 px en tarjetas y encabezados; fondo `cloud-subtle` y radio `full`.
- Siempre con texto a la derecha: `usado / límite unidad (porcentaje)`, por ejemplo "320/500 kg (64 %)".
- La proyección de una asignación (F-02) se dibuja como un segundo segmento rayado a 45° del color del nivel *resultante*, con la leyenda "+12 kg si asignas".

### 2.6. Estructura de layout

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

### 2.7. Reglas de prototipado comunes

- Se usan instancias de la Team Library (Button, TextInput, Select, MultiSelect, Badge, Checkbox) y no copias locales. Los componentes propios del módulo (barra de ocupación, tarjeta de despacho, línea de tiempo) se crean en el archivo del módulo y se proponen a la biblioteca solo si se reutilizan.
- Cada pantalla tiene sus variantes de estado como frames vecinos: normal, carga (skeleton), vacío, error y confirmación.
- El texto sigue el UX Writing de la guía: verbos concretos, primero qué pasó y luego qué hacer, sin códigos HTTP visibles.
- El foco de teclado es un anillo de 2 px en `accent/signal` con desplazamiento de 2 px.

---

## 3. Pantallas y tratamiento visual

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

## 4. Lista de revisión antes de entregar un prototipo

- [ ] Usa instancias de la Team Library y las variables de color de Figma, sin HEX sueltos.
- [ ] Los H1 a H3 van en Oswald mayúsculas; todo lo demás en Inter con los estilos de la escala.
- [ ] La acción principal es naranja con texto `ink`, y hay una sola por pantalla o franja de acciones.
- [ ] No se usa volt; signal solo aparece como foco.
- [ ] Todo estado tiene icono y texto además del color.
- [ ] Las barras de ocupación muestran valor, límite, porcentaje y nivel en texto.
- [ ] Los espaciados están en múltiplos de 4 px y los radios son 8, 12, 16 o full.
- [ ] Hay variantes de carga, vacío, error y confirmación junto a cada pantalla.
- [ ] Los textos siguen el UX Writing de la guía, sin códigos HTTP ni mensajes técnicos.
- [ ] El contraste cumple AA, comprobado con un plugin de contraste en Figma.
