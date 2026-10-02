# Sistema de Diseño UX/UI — Módulo de Despacho y Entrega a Domicilio

**Documento:** `SYSTEM-DESIGN.md`  
**Versión:** 1.0  
**Fecha:** 2026-10-02  
**Responsable:** Max (Frontend y UI/UX)  
**Base:** *Guía UX/UI del Marketplace Multicanal — Inka Athletics* (en adelante, **la Guía**)  
**Aplica a:** F-01 Gestor de Zonas Geográficas, F-02 Programación y Asignación de Despachos, F-03 App Móvil del Repartidor, F-04 Gestión de Entregas Fallidas y F-05 Monitoreo de Flota y Capacidad

---

## 1. Propósito y alcance

Este documento es la guía de diseño e implementación UX/UI del módulo de Despacho y Entrega a Domicilio. Reúne todo el contenido de la Guía UX/UI del Marketplace Multicanal, que es común a todos los módulos del marketplace, y explica cómo se aplica en cada funcionalidad del módulo.

Cada módulo del marketplace (Ventas, Tienda, Inventario y otros) es independiente y elabora su propio documento a partir de la misma Guía. Este documento corresponde únicamente a Despacho.

Está organizado en tres partes:

- **Parte I — Sistema de diseño** (§3 a §14): identidad, colores, tipografía, espaciado, radios, iconografía, superficies, UX Writing, componentes, patrones y gobernanza, tal como los define la Guía, con su aplicación en Despacho.
- **Parte II — Implementación** (§15 a §18): configuración técnica del tema, estados del dominio, accesibilidad y comportamiento responsive.
- **Parte III — Guías por funcionalidad** (§19 a §25): cómo se diseña e implementa cada pantalla de F-01 a F-05 y la lista de revisión final.

El contenido, los flujos, los estados y los textos de cada pantalla provienen de las especificaciones de interfaz `disenio/funcionalidades/f-0X.md`. Este documento define cómo se ven y cómo se construyen.

---

## 2. Cómo usar este documento

| Rol | Qué leer | Para qué |
|---|---|---|
| Responsable de una funcionalidad | Parte I y la guía de su funcionalidad en la Parte III | Construir la alta fidelidad en Figma con los componentes y tokens correctos. |
| Desarrollador frontend | Parte II, §11 a §13 y la guía de su funcionalidad | Implementar las pantallas con Mantine usando solo el tema. |
| Revisor | §17 y §25 | Aprobar una pantalla con criterios verificables. |

Reglas básicas, tomadas §2:

- Revisar los fundamentos (§3 a §9) antes de crear una pantalla nueva.
- Usar los componentes publicados en la biblioteca central de Figma en lugar de dibujar copias locales.
- Seleccionar la variante y el estado que correspondan al caso de uso.
- Usar los patrones comunes (§13) cuando una pantalla repita estructuras como tarjetas, navegación, filtros, modales o skeletons.
- Consultar las reglas de UX Writing (§10) antes de escribir botones, alertas o mensajes de error.
- Proponer los cambios desde el canal indicado, sin editar directamente los componentes maestros (§14).

Recursos del proyecto:

- Archivo central de Figma (sistema de diseño): <https://www.figma.com/design/rKPdRQHLLUkYk5VdiEErqZ/Sistema-De-Dise%C3%B1o?node-id=57-15&t=eO6m1Plz1xQ5sFgn-1>
- Logos (PNG y SVG): <https://www.figma.com/design/rKPdRQHLLUkYk5VdiEErqZ/Sistema-De-Dise%C3%B1o?node-id=56-7&t=0TSK36SaklUJeiyS-4>

---

> **PARTE I — SISTEMA DE DISEÑO**

## 3. Identidad de marca

### 3.1. Nombre

La marca es **Inka Athletics**. "Inka" conecta la marca con una identidad peruana contemporánea, comunicada con orgullo y autenticidad, sin representaciones folclóricas superficiales ni recursos que conviertan la identidad peruana en un elemento decorativo. "Athletics" comunica actividad deportiva, movimiento, rendimiento y búsqueda constante de nuevas metas.

### 3.2. Propósito

Inka Athletics existe para impulsar a más personas a vivir el deporte con confianza, encontrando equipamiento, ropa y accesorios adecuados para cada meta. La marca ayuda a tomar decisiones con claridad, seguridad y motivación, sin importar el nivel de experiencia.

En Despacho, ese propósito se traduce en que el pedido llegue: las pantallas operativas priorizan la claridad y la confianza para que gestores y repartidores trabajen sin errores.

### 3.3. Personalidad

Determinada, cercana, contemporánea, confiable, activa y orgullosamente peruana. La marca transmite energía y movimiento, pero también acompañamiento y confianza; no se comporta como una autoridad distante ni como una marca excesivamente agresiva.

### 3.4. Logo y variantes

| Variante | Uso recomendado | Token relacionado |
|---|---|---|
| Logo negro | Fondos claros y aplicaciones generales | `color/surface/ink` |
| Logo volt | Promociones, campañas y piezas de alto impacto visual | `color/accent/volt` |
| Logo signal | Aplicaciones digitales, destacados y composiciones que necesiten un acento secundario | `color/accent/signal` |

La versión blanca o inversa se usa cuando el logo va sobre `color/surface/ink` u otras superficies oscuras. El área de seguridad y el tamaño mínimo se miden a partir del componente maestro de Figma.

No se debe: estirar, comprimir o deformar el logo; rotarlo; cambiar sus colores fuera de las variantes aprobadas; añadir sombras, contornos o efectos; colocarlo sobre fondos con contraste insuficiente; recortar el símbolo o el logotipo; usarlo como sustituto de un icono funcional; ni modificar la separación entre el símbolo y el nombre.

Accesibilidad: cuando el logo cumple una función informativa o de navegación lleva `alt="Inka Athletics"`; cuando es decorativo y el nombre de la marca ya es visible en el mismo contexto, se oculta a las tecnologías de asistencia.

**Aplicación en Despacho:**

| Lugar | Variante | Texto alternativo |
|---|---|---|
| Barra lateral de la aplicación administrativa (fondo ink) | Versión blanca o inversa | `alt="Inka Athletics"` (enlace al inicio) |
| Pantalla de acceso del repartidor (fondo ink) | Versión blanca o inversa | `alt="Inka Athletics"` |
| Encabezado móvil del repartidor (fondo ink) | No se muestra; el espacio se usa para el título de la vista | — |

---

## 4. Paleta de colores

La paleta se organiza en colores de acción, acentos de marca, superficies, texto y colores semánticos de estado. Se basa en la paleta de Mantine 9.6.2 y en colores personalizados del proyecto, para que Figma y React usen el mismo sistema. En Figma todos los colores se registran como **Variables** con nombres semánticos (su función, no su apariencia); en desarrollo se usan los colores equivalentes del tema de Mantine (§15.2).

- **Naranja:** acción principal (CTA, botones principales, elementos interactivos prioritarios).
- **Volt** (verde lima): acento de alto impacto para promociones, disponibilidad, destacados y celebración.
- **Signal** (azul índigo): acento secundario para foco de teclado, confirmación o pago y elementos nuevos.
- **Ink y cloud:** superficies. Cloud es el fondo claro de las pantallas transaccionales; ink se usa en secciones de mayor contraste.
- **Semánticos** (éxito, alerta, error, información): función independiente de los colores de marca. Volt y signal nunca los sustituyen para comunicar un estado del sistema.

### 4.1. Tokens

| Variable de Figma | Función | HEX | RGB | Mantine |
|---|---|---|---|---|
| `color/action/primary` | Acción principal: CTA, botones, enlaces activos | `#F76707` | 247, 103, 7 | `orange.7` |
| `color/action/primary-hover` | Hover de la acción principal | `#C2410C` | 194, 65, 12 | Naranja personalizado (`orange.8` del tema) |
| `color/action/primary-soft` | Fondo suave de la acción principal sobre fondos claros | `#FCE3D0` | 252, 227, 208 | Naranja personalizado |
| `color/accent/volt` | Acento de alto impacto: promociones, disponibilidad, destacados y celebración | `#C3E504` | 195, 229, 4 | `volt` personalizado |
| `color/accent/volt-soft` | Fondo suave del acento volt | `#EEF7B0` | 238, 247, 176 | `volt` (tono claro) |
| `color/accent/signal` | Acento secundario: foco de teclado, confirmación o pago, elementos "nuevo" | `#4361EE` | 67, 97, 238 | `signal` personalizado (≈ `indigo.6`) |
| `color/accent/signal-soft` | Fondo suave del acento signal | `#E1E6FB` | 225, 230, 251 | `signal` (≈ `indigo.0`) |
| `color/surface/ink` | Fondo oscuro para secciones de alto contraste | `#1B1812` | 27, 24, 18 | `ink` personalizado |
| `color/surface/ink-soft` | Superficie elevada sobre ink | `#26221A` | 38, 34, 26 | `ink` (tono claro) |
| `color/surface/cloud` | Fondo claro principal de páginas | `#F7F5F0` | 247, 245, 240 | `cloud` personalizado |
| `color/surface/cloud-subtle` | Fondo secundario sobre cloud | `#EDEAE2` | 237, 234, 226 | `cloud` (tono oscuro) |
| `color/text/primary` | Texto principal sobre fondo claro | `#1B1812` | 27, 24, 18 | — |
| `color/text/inverse` | Texto principal sobre ink | `#F7F5F0` | 247, 245, 240 | — |
| `color/text/secondary` | Texto secundario y descripciones | `#495057` | 73, 80, 87 | `gray.7` |
| `color/text/disabled` | Texto deshabilitado o de baja prioridad | `#868E96` | 134, 142, 150 | `gray.6` |
| `color/border/default` | Bordes sobre fondo claro | `#DEE2E6` | 222, 226, 230 | `gray.3` |
| `color/border/inverse` | Bordes sobre ink | `#3A362C` | 58, 54, 44 | `ink` (tono medio) |
| `color/success/default` | Indicadores de éxito y confirmación | `#2F9E44` | 47, 158, 68 | `green.8` |
| `color/success/background` | Fondo de mensajes de éxito | `#EBFBEE` | 235, 251, 238 | `green.0` |
| `color/warning/default` | Alertas y advertencias | `#F08C00` | 240, 140, 0 | `yellow.8` |
| `color/warning/background` | Fondo de alertas | `#FFF9DB` | 255, 249, 219 | `yellow.0` |
| `color/error/default` | Errores y acciones destructivas | `#E03131` | 224, 49, 49 | `red.8` |
| `color/error/background` | Fondo de mensajes de error | `#FFF5F5` | 255, 245, 245 | `red.0` |
| `color/info/default` | Información y mensajes informativos | `#1971C2` | 25, 113, 194 | `blue.8` |
| `color/info/background` | Fondo de mensajes informativos | `#E7F5FF` | 231, 245, 255 | `blue.0` |

### 4.2. Uso de los colores

| Token | Regla de uso |
|---|---|
| `action/primary` | Acción principal de una pantalla o sección. |
| `action/primary-hover` | Únicamente cuando el cursor está sobre una acción principal; también texto y borde de botones `outline` y `subtle` (§11.3). |
| `action/primary-soft` | Fondo de elementos seleccionados, mensajes informativos o componentes que se relacionan con el color principal sin un fondo intenso. |
| `accent/volt` | Promociones, indicadores de disponibilidad y momentos de energía o celebración. No sustituye a `action/primary` como color de interacción. |
| `accent/signal` | Indicador de foco de teclado en todo el sitio, confirmación o pago cuando se quiere diferenciar de la acción principal y elementos "nuevo". Es color de marca, no semántico: no se confunde con `info/default`. |
| `surface/ink` y `surface/cloud` | Fondos base. Cloud por defecto en pantallas transaccionales; ink en secciones de mayor impacto, siempre con `text/inverse`. No se combinan dentro de un mismo componente o tarjeta. |
| Neutros | `text/primary` es el texto predeterminado; `text/secondary`, información complementaria; `cloud-subtle` separa secciones sin introducir un color nuevo; `border/default` se usa en inputs, tarjetas y divisores. |
| Semánticos | Tienen significado y no se usan con fines decorativos. Un estado nunca se comunica solo con color: va con texto y, cuando corresponde, icono. |

Los colores del logo (ink, volt, signal) pertenecen a la identidad de marca y no sustituyen automáticamente los colores de acciones, alertas o estados. Solo se usan las combinaciones aprobadas en Figma.

### 4.3. Aplicación de los colores en Despacho

| Token | Dónde se usa en Despacho |
|---|---|
| `action/primary` | La única acción principal de cada pantalla, modal o panel: "Nueva zona", "Guardar zona", "Guardar tarifa", "Confirmar asignación", "Guardar orden", "Confirmar recepción", "Abrir jornada", "En camino", "Confirmar entrega", "Registrar fallo", etc. Indicador del ítem activo en la barra lateral, pestaña activa y paginación activa. |
| `action/primary-hover` | Hover de las acciones principales; texto de botones secundarios y terciarios ("Cancelar", "Limpiar filtros", "Editar", "Tarifas", "Ver detalle"). |
| `action/primary-soft` | Elementos seleccionados: tarjeta del repartidor elegido en la asignación, despacho "Siguiente" en Mi Ruta, repartidor activo en Rutas por repartidor. |
| `accent/volt-soft` | Badge de disponibilidad: repartidor y vehículo "Disponible" (§16). |
| `accent/volt` | Borde superior del indicador "Disponible" en el tablero de flota. |
| `accent/signal` | Anillo de foco de teclado y badge "Nuevo" (fila recién creada o pedido de prueba recién generado). |
| `surface/ink` | Barra lateral administrativa, encabezado móvil del repartidor y pantalla de acceso. |
| `surface/ink-soft` | Hover e ítem activo de la barra lateral. |
| `surface/cloud` | Fondo de todas las áreas de contenido. |
| `surface/cloud-subtle` | Barras de filtros, encabezados de tabla, pista de las barras de ocupación, filas atenuadas, franjas de resumen en modales y badge neutral. |
| Semánticos | Estados del despacho, del repartidor y de los vehículos (§16), alertas, validaciones, notificaciones y niveles de ocupación. |

Las superficies `Card`, `Modal`, `Drawer` y `Table` usan fondo blanco sobre cloud para separar planos.

### 4.4. Combinaciones de fondo y texto

Todas las combinaciones cumplen como mínimo WCAG AA para texto normal (4.5:1) y 3:1 para iconos y gráficos.

| Fondo | Texto o elemento | Uso | Contraste |
|---|---|---|---|
| `action/primary` `#F76707` | ink `#1B1812` | Botón principal y CTA | 5.82:1 |
| `action/primary-hover` `#C2410C` | cloud `#F7F5F0` | Hover del botón principal | 4.75:1 |
| ink | cloud | Texto sobre secciones oscuras | 16.25:1 |
| cloud | ink | Texto sobre secciones claras | 16.25:1 |
| `cloud-subtle` `#EDEAE2` | ink | Superficies secundarias | 14.73:1 |
| `accent/volt` `#C3E504` | ink | Promociones, disponibilidad y destacados | 12.25:1 |
| `accent/signal` `#4361EE` | blanco | Confirmación, pago y elementos nuevos | 5.02:1 |
| `success/background` | ink | Mensajes de éxito | 16.50:1 |
| `warning/background` | ink | Mensajes de alerta | 16.72:1 |
| `error/background` | ink | Mensajes de error | 16.55:1 |
| `info/background` | ink | Mensajes informativos | 15.94:1 |

Combinaciones adicionales que usa Despacho:

| Fondo | Texto o elemento | Uso en Despacho | Contraste |
|---|---|---|---|
| cloud | `action/primary-hover` | Texto de botones `outline` y `subtle` | 4.75:1 |
| `action/primary-soft` | ink | Tarjeta o fila seleccionada | 14.37:1 |
| `accent/volt-soft` | ink | Badge "Disponible" | ≥ 15:1 |
| `error/default` | blanco | Botón destructivo | 4.51:1 |
| cloud | `text/secondary` | Texto secundario | 7.50:1 |
| `cloud-subtle` | `text/secondary` | Encabezados de tabla | 6.80:1 |
| `ink-soft` | cloud | Ítem activo de la barra lateral | 14.53:1 |
| cloud | `accent/signal` | Anillo de foco sobre contenido | 4.61:1 |
| ink | `accent/signal` | Anillo de foco en la barra lateral | 3.53:1 |
| cloud | `success/default` | Barra de ocupación "Normal", iconos de éxito | 3.16:1 |
| cloud | `error/default` | Barra de ocupación "Llena", iconos de error | 4.14:1 |
| cloud | `info/default` | Iconos informativos | 4.61:1 |

Reglas §4.4:

- El botón principal **no** usa texto blanco sobre `action/primary`; su texto es `text/primary`.
- En hover, el botón principal cambia a `action/primary-hover` con `text/inverse`.
- Sobre volt siempre se usa `text/primary`; nunca texto blanco.
- Sobre signal se puede usar texto blanco.
- Sobre los fondos semánticos se usa `text/primary` para el contenido y el color semántico para iconos o indicadores.
- Los estados nunca se comunican solo con color.

### 4.5. Instrucciones de implementación para mantener el contraste

Mantine trae comportamientos por defecto que deben configurarse para que las reglas anteriores se cumplan en código. Todas estas instrucciones ya están incluidas en el tema (§15.2 y §15.3).

| Instrucción | Regla que asegura |
|---|---|
| Configurar `luminanceThreshold: 0.2` junto con `autoContrast: true`. Con el umbral por defecto (`0.3`), Mantine pondría texto blanco sobre `#F76707` (luminancia 0.295, contraste 3.04:1). Con `0.2`, elige ink en naranja, volt, verde y amarillo, y blanco en el hover naranja, signal, rojo y azul. | Texto ink en el botón principal. |
| Aplicar `text/inverse` en el hover de los botones `filled` mediante CSS, porque `autoContrast` calcula el texto con el color base y no con el de hover (ink sobre `#C2410C` = 3.42:1). | Texto inverse en el hover del botón principal. |
| Registrar las paletas `volt`, `signal`, `ink` y `cloud` con el valor de marca en el índice 7 (el `primaryShade`) y definir `orange[8] = #C2410C`. | Que `color="volt"`, `color="signal"` y el hover naranja muestren exactamente los HEX de la Guía. |
| Definir `focusClassName` con contorno de 2 px en `accent/signal`. | Foco visible en signal en todo el sitio. |
| Usar siempre `variant="light"` en badges semánticos, con texto `text/primary`. | Contraste ≥ 15:1 en badges; evita texto blanco sobre verde (3.45:1) o amarillo (2.48:1). |
| Acompañar siempre de texto los gráficos e iconos en `warning/default` (2.28:1 sobre cloud) y hacer que los iconos que acompañan una etiqueta hereden `currentColor` (§8). | El estado nunca depende solo del color. |
| En vistas móviles, usar `size="lg"` en botones e inputs (50 px) y `size="xl"` en `ActionIcon` (44 px), porque `md` mide 42 px. | Controles táctiles de tamaño suficiente (§11.6). |

Combinaciones no permitidas: texto blanco sobre `action/primary`, texto ink sobre `action/primary-hover`, texto blanco sobre `accent/volt` y texto blanco sobre `success/default` o `warning/default`.

---

## 5. Tipografía

El sistema usa dos familias con roles distintos:

- **Oswald** para títulos H1, H2 y H3 y elementos de alto impacto. Es condensada, evoca marcadores deportivos y tipografía de camiseta.
- **Inter** para todo el texto de cuerpo, formularios y contenido general, por su legibilidad en interfaces y su variedad de pesos.

La combinación es una decisión de marca y no se extiende: labels de formulario, texto de cuerpo y etiquetas auxiliares usan siempre Inter, nunca Oswald. Los títulos en Oswald se escriben **en mayúsculas y en peso 700**; ese tratamiento es exclusivo de H1, H2 y H3 y no se aplica a subtítulos, labels, badges ni cuerpo.

### 5.1. Familias y carga

| Uso | Familia en desarrollo |
|---|---|
| Cuerpo | `Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` |
| Títulos H1, H2, H3 | `Oswald, "Segoe UI", sans-serif` |

Ambas se cargan desde Google Fonts en el `head` del documento:

```html
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 5.2. Pesos permitidos

| Peso | Nombre | Uso |
|---|---|---|
| 400 | Regular | Texto de cuerpo, descripciones y contenido general |
| 500 | Medium | Elementos que requieren énfasis moderado |
| 600 | SemiBold | Etiquetas, botones y subtítulos |
| 700 | Bold | Títulos y encabezados |

No se usan otros pesos.

### 5.3. Escala tipográfica

| Estilo de Figma | Tamaño | Peso | Interlineado | Uso |
|---|---|---|---|---|
| `Typography/Heading/H1` | 32 px | 700 | 40 px | Título principal de página |
| `Typography/Heading/H2` | 28 px | 700 | 36 px | Secciones principales |
| `Typography/Heading/H3` | 24 px | 700 | 32 px | Subsecciones |
| `Typography/Heading/H4` | 20 px | 700 | 28 px | Tarjetas, modales y bloques |
| `Typography/Subtitle` | 18 px | 600 | 26 px | Subtítulos y encabezados secundarios |
| `Typography/Body` | 16 px | 400 | 24 px | Texto principal de la interfaz |
| `Typography/Body/Small` | 14 px | 400 | 20 px | Información secundaria y contenido compacto |
| `Typography/Label` | 14 px | 600 | 20 px | Labels de formularios y controles |
| `Typography/Auxiliary` | 12 px | 400 | 16 px | Ayuda, metadatos y texto auxiliar |

El espaciado entre letras es 0 en todos los estilos. Cada estilo corresponde a un propósito, no a una preferencia visual. Los títulos de página usan H1; las secciones internas, H2 o H3; H4 se usa en tarjetas, modales y bloques pequeños. El cuerpo es de 16 px; 14 px se reserva para información secundaria y componentes densos; 12 px solo para información auxiliar, nunca para contenido principal o acciones.

**Implementación:** la escala se configura en el tema de Mantine (§15.2). Como `theme.headings.fontFamily` aplica la misma familia a todos los niveles, el CSS global de §15.3 aplica las mayúsculas solo a H1–H3 y devuelve H4–H6 a Inter.

### 5.4. Aplicación de la escala en Despacho

| Estilo (Figma) | Familia | Aplicación administrativa | Web del repartidor |
|---|---|---|---|
| `Typography/Heading/H1` 32/40 | Oswald 700, mayúsculas | Título de página: "ZONAS DE COBERTURA", "PROGRAMACIÓN Y ASIGNACIÓN", "ENTREGAS FALLIDAS", "MONITOREO DE FLOTA". | No se usa (demasiado grande para 390 px). |
| `Typography/Heading/H2` 28/36 | Oswald 700, mayúsculas | Encabezado de secciones grandes ("JORNADAS DE HOY"). | Título "DESPACHO — REPARTIDOR" en la pantalla de acceso. |
| `Typography/Heading/H3` 24/32 | Oswald 700, mayúsculas | Título de modales y del panel lateral de tarifas. | Título de la vista en el encabezado ("MI RUTA", "RESUMEN", "CERRAR JORNADA"). |
| `Typography/Heading/H4` 20/28 | Inter 700 | Títulos de bloques y tarjetas ("Incidencia", "Historial de estados", "Tarifa base"). | Bloques del detalle ("Destino", "Destinatario", "Evidencia"). |
| `Typography/Subtitle` 18/26 | Inter 600 | Subtítulo de página, nombre del repartidor en la ruta. | Saludo y fecha en Mi Ruta; código de rastreo en el encabezado del detalle. |
| `Typography/Body` 16/24 | Inter 400 | Contenido de formularios, textos de modales y alertas. | **Tamaño mínimo para todo contenido operativo** (dirección, destinatario, mensajes). |
| `Typography/Body/Small` 14/20 | Inter 400 | Celdas de tabla, filtros, texto de ayuda de acciones deshabilitadas. | Datos secundarios de la tarjeta (código, "Intento 1 de 2"). |
| `Typography/Label` 14/20 | Inter 600 | Labels de formularios y encabezados de columna. | Labels de formularios y de la navegación inferior. |
| `Typography/Auxiliary` 12/16 | Inter 400 | Metadatos: "Actualizado hace 10 s", contador de caracteres, "Disponible desde [fecha]". | Solo contador de caracteres; nunca información necesaria para operar al sol. |

### 5.5. Formato de datos en Despacho

- **Cifras:** códigos de rastreo, pesos, volúmenes, montos, porcentajes y contadores usan la clase `ia-num` (cifras tabulares) para que las columnas queden alineadas.
- **Códigos de rastreo:** Inter 500, sin transformar mayúsculas ni minúsculas; nunca se cortan con elipsis.
- **Unidades:** separadas del número por un espacio: `500 kg`, `4.0 m³`, `80 paquetes`, `PEN 10.00`, `70 %`.
- **Formato de ocupación:** `usado / límite unidad (porcentaje)`, por ejemplo `320 / 500 kg (64 %)`.
- **Fechas:** `dd/mm/aaaa` en tablas; `Lunes 5 de octubre` en encabezados; horas en formato de 24 h (`14:35`). Se usa `dayjs` con la configuración regional `es`.
- **Direcciones:** máximo dos líneas en tarjetas y una en tablas (`lineClamp`), con la dirección completa visible en el detalle.
- Los valores de enum nunca se muestran crudos: `PENDIENTE_ASIGNACION` se muestra como "Pendiente de asignación" (ver §16).

---

## 6. Espaciado y grilla

### 6.1. Escala de espaciado

Escala basada en 4 px. No se usan valores arbitrarios (7, 13, 19 o 27 px); si una necesidad no cabe en la escala, primero se evalúa ampliar los tokens.

| Token | Valor | Uso | Mantine |
|---|---|---|---|
| `spacing/xs` | 4 px | Separación mínima entre elementos relacionados | `xs` |
| `spacing/sm` | 8 px | Entre icono y texto, controles relacionados | `sm` |
| `spacing/md` | 16 px | Padding y separación estándar (valor por defecto) | `md` |
| `spacing/lg` | 24 px | Entre grupos o bloques | `lg` |
| `spacing/xl` | 32 px | Entre secciones | `xl` |

### 6.2. Grilla responsive

Grilla de 12 columnas en todos los tamaños; cambia cuánto ocupa cada elemento. Los breakpoints son los de Mantine 9.6.2.

| Breakpoint | Ancho de referencia | Columnas | Margen lateral | Gutter | Ancho máximo |
|---|---|---|---|---|---|
| Base | < 576 px | 12 | 16 px | 16 px | Fluido |
| `xs` | ≥ 576 px | 12 | 20 px | 16 px | 540 px |
| `sm` | ≥ 768 px | 12 | 24 px | 20 px | 720 px |
| `md` | ≥ 992 px | 12 | 32 px | 24 px | 960 px |
| `lg` | ≥ 1200 px | 12 | 32 px | 24 px | 1140 px |
| `xl` | ≥ 1408 px | 12 | 40 px | 24 px | 1320 px |

```tsx
<Grid gutter={{ base: 16, sm: 20, md: 24 }}>
  <Grid.Col span={{ base: 12, sm: 6, lg: 3 }}>…</Grid.Col>
</Grid>
```

En Figma se muestra al menos una versión móvil y una de escritorio de los componentes o patrones cuyo comportamiento cambie de forma relevante (§18).

### 6.3. Uso de la escala en Despacho

| Relación | Token |
|---|---|
| Icono y texto dentro de un control | `sm` (8 px) |
| Campos dentro de un formulario, controles de una barra de filtros | `md` (16 px) |
| Padding interno de tarjetas, barra de filtros y barras de acciones | `md` (16 px) |
| Padding interno de modales y panel lateral | `lg` (24 px) |
| Entre encabezado de página, indicadores, filtros y tabla | `lg` (24 px) |
| Entre secciones de un formulario largo | `xl` (32 px) |

### 6.4. Layout de la aplicación administrativa (`AppShell` de Mantine)

| Elemento | Medida | Token |
|---|---|---|
| Barra lateral expandida | 256 px | — |
| Barra lateral colapsada (`md` a `lg`) | 72 px, solo iconos con `aria-label` y tooltip | — |
| Encabezado superior | 64 px de alto | — |
| Margen lateral del contenido | Según §6.2: 16 px (`base`), 20 px (`xs`), 24 px (`sm`), 32 px (`md` y `lg`), 40 px (`xl`) | Grilla de la Guía |
| Separación entre encabezado de página, indicadores, filtros y tabla | 24 px | `lg` |
| Gutter entre columnas | Según §6.2: 16 px (`base`, `xs`), 20 px (`sm`), 24 px (`md` en adelante) | Grilla de la Guía |
| Padding interno de tarjetas y modales | 16 px y 24 px | `md`, `lg` |
| Ancho del contenido | Grilla de 12 columnas con el ancho máximo §6.2 (hasta 1320 px en `xl`); formularios de página completa en 8 columnas centradas desde `md` (12 en anchos menores) | Grilla de la Guía |
| Modal estándar / amplio | 480 px / 880 px | `size="md"` / `size={880}` |
| Panel lateral (`Drawer`) | 560 px | — |

En tableta (`sm`, 768–991 px), usada por F-02, la barra lateral pasa a modo colapsado y la tabla oculta las columnas de menor prioridad (definidas en la Parte III para cada pantalla) detrás de una acción "Ver detalle".

### 6.5. Layout de la web del repartidor

| Elemento | Medida |
|---|---|
| Encabezado móvil | 56 px de alto, fondo ink |
| Padding lateral del contenido | 16 px (`md`) |
| Separación entre tarjetas de despacho | 16 px (`md`) |
| Barra de acciones fija | 16 px de padding + `env(safe-area-inset-bottom)` |
| Navegación inferior | 64 px de alto + `env(safe-area-inset-bottom)`, tres destinos |
| Área táctil mínima | 44 × 44 px; acciones principales a 50 px de alto (`size="lg"`) y ancho completo (`fullWidth`) |
| Ancho máximo | 480 px centrado (si se abre en una pantalla más grande) |

---

## 7. Radios de borde

| Token | Valor | Uso | Mantine |
|---|---|---|---|
| `radius/xs` | 4 px | Elementos pequeños y controles compactos | `xs` |
| `radius/sm` | 8 px | Botones, inputs, dropdowns y controles (valor por defecto) | `sm` |
| `radius/md` | 12 px | Tarjetas y contenedores | `md` |
| `radius/lg` | 16 px | Modales y superficies destacadas | `lg` |
| `radius/full` | 999 px | Badges, tags y elementos tipo pill | `xl` |

No se usan valores intermedios (5, 10 o 14 px). En Figma el token se llama `radius/full`; en el tema de Mantine se registra con la clave `xl`, por lo que en código se escribe `radius="xl"`.

**Aplicación en Despacho:**

| Elemento de Despacho | Token | Mantine |
|---|---|---|
| Botones, inputs, selects, segmentos, filas seleccionables del catálogo de repartidores | `radius/sm` 8 px | `sm` (por defecto) |
| Tarjetas de indicadores, tarjetas de despacho, bloques del detalle, tabla contenedora | `radius/md` 12 px | `md` |
| Modales, panel lateral, área de captura de foto | `radius/lg` 16 px | `lg` |
| Badges de estado, etiquetas especiales, `Pill` de distritos | `radius/full` 999 px | `xl`  |
| Barras de ocupación | `radius/xs` 4 px | `xs` |

---

## 8. Iconografía

Set único: **Tabler Icons** (`@tabler/icons-react`), lienzo de 24 × 24 px y trazo de 2 px.

| Tamaño | Uso |
|---|---|
| 16 × 16 px | Controles pequeños, badges (14–16 px) y elementos compactos |
| 20 × 20 px | Botones, inputs y controles estándar (tamaño estándar en botones e inputs) |
| 24 × 24 px | Iconos independientes, navegación y acciones destacadas |

- Separación entre icono y texto: 8 px.
- Color: `currentColor`, para heredar el color del elemento que lo contiene. No se usan colores distintos para iconos de un mismo control salvo significado semántico definido.
- Iconos decorativos (acompañan un texto): no reciben foco ni se anuncian por separado.
- Iconos interactivos (representan solos una acción): siempre dentro de `Button` o `ActionIcon`, con nombre accesible (`aria-label`). No se usan iconos sueltos con `onClick`.
- Los nombres en Figma corresponden, siempre que sea posible, al nombre en `@tabler/icons-react`.

```tsx
<Button leftSection={<IconShoppingCart size={20} />}>Agregar al carrito</Button>
<ActionIcon aria-label="Agregar a favoritos" variant="subtle"><IconHeart size={20} /></ActionIcon>
```

**Catálogo de iconos de Despacho:**

Tamaños: 16 px en badges y celdas, 20 px en botones e inputs, 24 px en navegación y encabezados. Trazo de 2 px y `currentColor`. Los iconos sin texto van dentro de `ActionIcon` con `aria-label`.

| Concepto | Icono | Concepto | Icono |
|---|---|---|---|
| Zonas y Tarifas | `IconMapPin` | Repartidores | `IconUsers` |
| Programación | `IconCalendarTime` | Vehículos | `IconTruck` |
| Entregas fallidas | `IconPackageOff` | Asignación diaria | `IconCalendarCheck` |
| Monitoreo de flota | `IconGauge` | Cerrar sesión | `IconLogout` |
| Mi Ruta | `IconRoute` | Resumen | `IconChartBar` |
| Cerrar jornada | `IconDoorExit` | Actualizar / Reintentar | `IconRefresh` |
| Buscar | `IconSearch` | Limpiar filtros | `IconFilterOff` |
| Editar | `IconPencil` | Tarifas | `IconCash` |
| Abrir en mapas | `IconMap2` | Llamar | `IconPhone` |
| Tomar foto / evidencia | `IconCamera` | Ver foto | `IconPhoto` |
| Arrastrar para ordenar | `IconGripVertical` | Subir / Bajar | `IconChevronUp` / `IconChevronDown` |
| Reasignar | `IconArrowsExchange` | Reprogramar | `IconCalendarRepeat` |
| Confirmar recepción | `IconPackageImport` | Cerrar como devuelto | `IconArrowBackUp` |
| Simulado | `IconFlask` | Reintento | `IconRepeat` |
| Tiempo de espera elevado | `IconClockExclamation` | Sin conexión | `IconWifiOff` |
| Acceso denegado | `IconLock` | Advertencia | `IconAlertTriangle` |
| Error | `IconAlertCircle` | Éxito | `IconCircleCheck` |
| Información | `IconInfoCircle` | Vinculación pendiente | `IconLinkOff` |
| Mantenimiento | `IconTool` | Historial | `IconHistory` |

Antes de publicar el componente en Figma, se verifica que cada nombre exista en la versión instalada de `@tabler/icons-react`.

---

## 9. Superficies, alternancia y motivo gráfico

El sitio alterna dos fondos base, `surface/cloud` y `surface/ink`, para crear ritmo visual y evitar que el naranja sea el único elemento con contraste.

- Las pantallas transaccionales (catálogos, formularios y, en Despacho, todas las pantallas de trabajo) usan cloud por defecto, priorizando legibilidad y foco en la tarea.
- Las secciones de mayor impacto (heroes, banners, footer) pueden usar ink, siempre con `text/inverse`.
- No se alternan fondos dentro de un mismo componente o tarjeta.

**Motivo gráfico — líneas de velocidad:** líneas diagonales delgadas (≈ 110°–120°) en tonos de `action/primary`, `accent/volt` y `accent/signal`, como recurso decorativo de fondo en heroes o divisores. Es puramente decorativo: no comunica estado, jerarquía ni información.

**Aplicación en Despacho:**

| Superficie | Fondo | Contenido |
|---|---|---|
| Barra lateral administrativa | `surface/ink` | Texto `text/inverse`, bordes `border/inverse`, ítem activo en `ink-soft` |
| Encabezado superior administrativo y área de contenido | `surface/cloud` | Tarjetas, tablas y modales en blanco |
| Encabezado móvil del repartidor | `surface/ink` | Título y acciones en `text/inverse` |
| Contenido móvil del repartidor | `surface/cloud` | Tarjetas blancas |
| Navegación inferior y barras de acciones fijas | Blanco con borde superior `border/default` | — |
| Pantalla de acceso del repartidor | `surface/ink` con líneas de velocidad | Único lugar de Despacho donde se usa el motivo gráfico (funciona como hero de entrada) |

---

## 10. UX Writing

### 10.1. Tono de voz

Inka Athletics comunica de forma directa, motivadora y humana. Habla con energía, pero no grita ni exagera; acompaña al usuario en lugar de presionarlo. Su personalidad es determinada, cercana, contemporánea, confiable, activa y orgullosamente peruana, sin clichés folclóricos.

| Debe sonar | Ejemplo |
|---|---|
| Claro | "Encuentra tu talla y entrena cómodo." |
| Motivador | "Compra tu próxima meta hoy." |
| Cercano | "Todo listo para seguir avanzando." |
| Seguro | "Compra productos verificados y recibe seguimiento de tu pedido." |
| Deportivo | "Equípate para dar tu mejor paso." |

Debe evitar: exceso de palabras en inglés; frases agresivas ("sé el mejor", "no pares nunca"); expresiones juveniles, forzadas o informales; referencias folclóricas superficiales; promesas exageradas o absolutas; mensajes que presionen o culpabilicen.

**En Despacho** el tono es directo y operativo: se conserva la cercanía y la confianza de la marca, y los mensajes motivacionales quedan fuera de las pantallas de trabajo. Ejemplo de cierre de jornada sin pendientes: "No tienes despachos pendientes. Puedes cerrar tu jornada."

### 10.2. Reglas generales de redacción

- Escribir acciones con verbos concretos: Comprar, Guardar, Aplicar, Continuar o Volver.
- Mantener el mismo término para una misma acción en todas las pantallas.
- Explicar primero qué ocurrió y después qué puede hacer el usuario.
- Evitar mensajes técnicos, códigos internos, culpas y signos de exclamación innecesarios.
- No depender solo del color para comunicar éxito, alerta o error.
- Usar mayúscula inicial en frases y no escribir botones completos en mayúsculas.

### 10.3. Botones y llamados a la acción

| Situación | Hacer | No hacer |
|---|---|---|
| Compra | Comprar ahora | Haz clic aquí |
| Filtros | Aplicar filtros | Aceptar |
| Pago | Continuar al pago | Siguiente |
| Disponibilidad | Ver disponibilidad | Consultar |
| Guardar | Guardar cambios | Enviar |
| *Despacho:* crear | Nueva zona, Nuevo repartidor, Nuevo vehículo | Agregar, Crear |
| *Despacho:* guardar | Guardar zona, Guardar tarifa, Guardar orden | Enviar, OK |
| *Despacho:* confirmar en un modal | Confirmar asignación, Confirmar recepción, Desactivar zona | Aceptar, Sí |
| *Despacho:* operación del repartidor | En camino, Confirmar entrega, Registrar fallo | Siguiente, Listo |

La acción de confirmación de un modal repite el verbo de su título ("¿Desactivar la zona Lima Norte?" → "Desactivar zona").

### 10.4. Mensajes de error

| Caso | Hacer | No hacer |
|---|---|---|
| Stock agotado | Este producto está agotado. Prueba otra talla o revisa productos similares. | Error de stock. |
| Tarjeta rechazada | No pudimos procesar la tarjeta. Revisa los datos o utiliza otro método de pago. | Pago fallido. |
| Campo obligatorio | Ingresa tu correo electrónico. | Campo inválido. |
| Problema de conexión | No pudimos cargar la información. Inténtalo nuevamente. | Error 500. |
| *Despacho:* duplicidad de zona | El distrito San Isidro ya pertenece a la zona activa Lima Centro. | Error 409. |
| *Despacho:* capacidad | Capacidad de carga del repartidor excedida: peso. | Error 422. |
| *Despacho:* foto | No se pudo subir la foto. La entrega no se registró. | Upload failed. |
| *Despacho:* campo numérico | La tarifa no puede ser negativa. | Valor inválido. |

### 10.5. Alertas y confirmaciones

| Tipo | Ejemplo de la Guía | Ejemplos de Despacho |
|---|---|---|
| Información | Tu pedido está siendo preparado. | La regla se aplicará a las cotizaciones siguientes para esta zona. / Este intento contará como Intento 1 de 2. |
| Alerta | Quedan pocas unidades disponibles. | 3 despachos quedarán como No intentado. / Tu turno no está activo. Solo puedes consultar tu ruta. |
| Éxito | Producto agregado al carrito. | Zona registrada correctamente. / Entrega registrada. / Despacho DSP-000123 asignado a Juan Pérez. |
| Confirmación | ¿Quieres eliminar este producto del carrito? | ¿Desactivar la zona Lima Norte? / ¿Cerrar tu jornada? Esta acción no se puede deshacer. |

### 10.6. Vocabulario de Despacho

Un concepto, un término, en todas las pantallas:

| Usar | No usar |
|---|---|
| Despacho | Envío, orden, pedido (el pedido pertenece a Ventas) |
| Código de rastreo | Tracking, ID, código de seguimiento |
| Repartidor | Conductor, chofer, motorizado, operador |
| Vehículo (tipo: Moto, Auto, Furgoneta) | Unidad |
| Gestor de Despacho | Administrador, operador |
| Jornada | Turno (salvo en "Turno habitual" y "Cerrar turno", definidos en F-05) |
| Centro de despacho | Almacén, base |
| Zona de cobertura | Área, sector |
| Reprogramar | Reagendar (el "reintento" es la etiqueta, no la acción) |
| Devuelto a origen | Devuelto al almacén, retornado |
| Evidencia | Prueba, comprobante |

### 10.7. Reglas adicionales de Despacho

- Tuteo en la aplicación administrativa y en la web del repartidor, igual que los ejemplos de la Guía.
- Notificaciones de éxito en pasado y con el objeto afectado: "Zona registrada correctamente".
- Nunca se muestran códigos HTTP ni valores de enum: `PENDIENTE_ASIGNACION` se muestra como "Pendiente de asignación".
- Los textos de cada pantalla provienen de su especificación `f-0X.md`; si se ajustan en alta fidelidad, se actualiza también la especificación.

---

## 11. Componentes reutilizables (UI Kit)

### 11.1. Base de implementación

El UI Kit se implementa con **Mantine 9.6.2 sobre React y TypeScript**, configurado mediante `MantineProvider` y el objeto de tema en `src/theme/theme.ts` (§15). Los componentes de Figma representan las mismas propiedades, tamaños, variantes y estados que la implementación.

Siempre que Mantine tenga un componente que cubra la necesidad, se usa ese componente. Solo se crean componentes propios cuando existe un patrón reutilizable específico del proyecto, cuando el comportamiento no puede representarse con Mantine o cuando hay que combinar varios componentes básicos. La personalización se hace con el tema y la Styles API, sin modificar la implementación interna de la librería.

Configuración inicial: tema claro; acción principal `orange.7` (`#F76707`) con hover `#C2410C`; volt `#C3E504`; signal `#4361EE`; ink `#1B1812`; cloud `#F7F5F0`; cuerpo en Inter; títulos H1–H3 en Oswald; radio predeterminado 8 px; contraste automático habilitado. Los semánticos usan las familias `green`, `yellow`, `red` y `blue` de Mantine y no se sustituyen por volt o signal.

### 11.2. Reglas comunes de los componentes

- Cada componente de Figma es un componente principal con *Component Properties* para variantes y estados, con nombres equivalentes a las props de código.
- Solo se usan los tokens de §4 a §7; nada de colores, radios o espacios arbitrarios.
- `action/primary` para acciones principales; `accent/volt` para promociones, disponibilidad y destacados; `accent/signal` para foco, confirmación o pago diferenciado y elementos nuevos; semánticos solo para estados.
- Estados aplicables a componentes interactivos: default, hover, focus, disabled, loading, selected, open y error (no todos aplican a todos; por ejemplo, error es propio de campos y loading de acciones que esperan una operación).
- Foco visible en `accent/signal` al usar teclado.
- Error, alerta y éxito no dependen solo del color.
- Controles sin texto visible con nombre accesible (`aria-label`).
- `loading` impide acciones repetidas cuando la operación no puede ejecutarse varias veces.
- Cada componente documenta su comportamiento responsive.
- No se duplica un componente solo para cambiar una propiedad visual; los cambios que afectan a varios módulos se hacen desde el tema o el componente reutilizable.

Nomenclatura de propiedades, equivalente a Mantine: `variant`, `size`, `color`, `radius`, `disabled`, `loading`, `error`, `checked`, `searchable`, `clearable`.

### 11.3. Botones

Los botones comunican acciones; su etiqueta empieza con un verbo concreto y debe existir una jerarquía visual clara entre la acción principal y las alternativas.

| Uso | Mantine | Color | Texto | Cuándo |
|---|---|---|---|---|
| Acción principal | `variant="filled"` | `action/primary` | `text/primary` (hover: `primary-hover` + `text/inverse`) | Acción de mayor importancia |
| Acción secundaria | `variant="outline"` | `action/primary-hover` | `action/primary-hover` | Alternativa a la principal |
| Acción terciaria | `variant="subtle"` | `action/primary-hover` | `action/primary-hover` | Acción de menor jerarquía |
| Confirmación o pago | `variant="filled" color="signal"` | `accent/signal` | Blanco | Cuando debe diferenciarse de la principal |
| Acción destructiva | `variant="filled" color="red"` | `error/default` | Blanco | Eliminar, cancelar o anular |

Volt no se usa como botón.

| Propiedad | Valores | Regla |
|---|---|---|
| `size` | `sm` (tablas, filtros, espacios compactos), `md` (predeterminado), `lg` (acciones destacadas o pantallas de conversión) | No se usan `xs` ni `xl`. |
| Icono | `none`, `left`, `right` | 16 px en `sm`, 20 px en `md` y `lg`; 8 px de separación; `currentColor`. |
| Ancho | Según contenido; mínimo visual ≈ 96 px | En móvil, las acciones principales de formularios y procesos lineales pueden usar `fullWidth`. |
| Estados en Figma | default, hover, focus, disabled, loading | Focus con `accent/signal`. Error no es estado del botón: se usa `intent=destructive` o un mensaje asociado. Loading conserva el contexto e impide repetir. |

Propiedades en Figma: `variant = filled | outline | subtle`, `intent = primary | confirmation | destructive`, `size = sm | md | lg`, `state = default | hover | focus | disabled | loading`, `icon = none | left | right`, `fullWidth = true | false`. Correspondencia de `intent`: `primary` → `action/primary`; `confirmation` → `accent/signal`; `destructive` → `error/default`.

### 11.4. Campos de texto y búsqueda

| Necesidad | Componente |
|---|---|
| Texto general | `TextInput` |
| Contraseña | `PasswordInput` |
| Números | `NumberInput` |
| Varias líneas | `Textarea` |
| Búsqueda | `TextInput` con `IconSearch` a la izquierda |

- Tamaños: `sm` (compacto, filtros), `md` (predeterminado), `lg` (casos de mayor énfasis).
- **Label visible siempre**; el placeholder solo complementa.
- Obligatorios: `required` (atributo HTML + indicador) en lugar de solo `withAsterisk`.
- Texto auxiliar (`description`) para explicar una restricción antes del error.
- Errores con la propiedad `error`, diciendo qué ocurrió y cómo corregirlo ("Ingresa un correo electrónico válido", nunca "Campo inválido").
- Longitudes iniciales: nombre o título hasta 100 caracteres; búsqueda hasta 120; correo hasta 254; texto descriptivo corto hasta 250.
- Búsqueda: acción para limpiar cuando hay texto, loader a la derecha durante la consulta y mensaje claro sin coincidencias ("No encontramos resultados para esta búsqueda").
- Estados en Figma: default, hover, focus, filled, disabled, loading y error. Propiedades: `size`, `state`, `required`, `description`, `leftIcon`, `rightAction = none | clear | loading`.

### 11.5. Checkboxes

Para activar o desactivar una opción independiente o seleccionar varias de un conjunto; para una única alternativa excluyente se usa `Radio`.

- Tamaños `sm` y `md` (predeterminado); 8 px entre control y etiqueta; toda la etiqueta activa el control.
- Selección: unchecked, checked e indeterminate (grupo parcialmente seleccionado). Lo seleccionado se reconoce por el símbolo, no solo por el color.
- Estados en Figma: default, hover, focus, disabled y error, combinados con los tres estados de selección.
- Error con instrucción clara: "Debes aceptar los términos para continuar", no "Campo obligatorio".
- Propiedades: `checked = false | true | indeterminate`, `size`, `state`, `label`, `description`.

### 11.6. Dropdowns

| Necesidad | Componente |
|---|---|
| Selección única | `Select` |
| Selección múltiple | `MultiSelect` |
| Texto libre con sugerencias | `Autocomplete` |
| Comportamientos avanzados | `Combobox` |

- Tamaños `sm`, `md` (predeterminado) y `lg`.
- `searchable` en listas de más de ~8 opciones; `clearable` en dropdowns opcionales o usados como filtros.
- Sin coincidencias: `nothingFoundMessage="Sin resultados"`.
- Listas grandes: `limit` para no renderizar miles de opciones.
- Móvil: ancho del contenedor, lista dentro del viewport con desplazamiento vertical y opciones de tamaño cómodo.
- Estados en Figma: default, hover, focus, open, selected, disabled, loading (opciones asíncronas) y error. Propiedades: `size`, `state`, `searchable`, `clearable` y, en `Select`, `required`.

### 11.7. Badges y tags

| Tipo | Componente | Uso |
|---|---|---|
| Badge informativo | `Badge` | Estado o categoría (no interactivo) |
| Tag seleccionable | `Chip` | Filtro que se activa o desactiva |
| Tag removible | `Pill` (`withRemoveButton`) | Filtro o valor seleccionado que puede quitarse |
| Entrada de varios tags | `PillsInput` / `TagsInput` | Ingreso de etiquetas |

Variantes de badge:

| Variante | Fondo / color | Texto | Ejemplo de la Guía | Ejemplo en Despacho |
|---|---|---|---|---|
| `neutral` | `cloud-subtle` | `text/primary` | Running | Pendiente de asignación |
| `info` | `info/background` + `info/default` | `text/primary` | En preparación | Asignado, En camino |
| `success` | `success/background` + `success/default` | `text/primary` | Pago aprobado | Entregado |
| `warning` | `warning/background` + `warning/default` | `text/primary` | Poco stock | Reintento |
| `error` | `error/background` + `error/default` | `text/primary` | Agotado | Fallido |
| `promotion` | `accent/volt` | `text/primary` | -20 % | No se usa en Despacho |
| `availability` | `accent/volt-soft` | `text/primary` | Disponible | Repartidor o vehículo disponible |
| `new` | `accent/signal` | Blanco | Nuevo | Pedido de prueba recién generado |

- Info, éxito, alerta y error son semánticos; volt y signal no los sustituyen.
- Badges informativos con fondos suaves (`variant="light"`).
- Tamaños `sm` (tarjetas, tablas, contextos compactos) y `md` (mayor visibilidad).
- Icono de 14–16 px solo si aporta significado; texto de máximo ~24 caracteres.
- El badge informativo no parece botón y solo tiene estado default. `Chip`: default, hover, focus, selected, disabled. `Pill`: default, hover, focus, disabled, con botón de quitar accesible (no una "X" sin contexto). Loading y error solo aplican a entradas de tags asíncronas.
- Propiedades en Figma: `Badge` (`semantic`, `size`, `icon = none | left`), `Chip` (`size`, `state`, `icon`), `Pill` (`size`, `removable`, `state`). Focus en `accent/signal`.

```tsx
<Badge color="green" variant="light">Pago aprobado</Badge>
<Badge color="volt">Disponible</Badge>
<Badge color="signal">Nuevo</Badge>
```

La aplicación de estos componentes a cada necesidad de Despacho se detalla en §12, y la asignación de cada estado del dominio a una variante de badge, en §16.

---

## 12. Aplicación de los componentes en Despacho

Esta sección indica qué componente del UI Kit (§11) y qué configuración usa cada necesidad de las pantallas de Despacho.

### 12.1. Botones

**Regla de jerarquía:** una sola acción `primary` por pantalla, modal o panel. Las acciones repetidas en cada fila de una tabla nunca son `primary`, aunque inicien el flujo principal: una columna de botones naranjas competiría con la acción del encabezado y saturaría la tabla. Las demás acciones son `outline` (alternativa directa) o `subtle` (acción de fila o de menor peso). **`intent=confirmation` (signal):** la Guía lo reserva para confirmación o pago cuando se necesita diferenciarlo de la acción principal. Despacho no tiene flujos de pago, y sus confirmaciones son la acción principal de cada modal, por lo que usan `primary`; signal se usa en Despacho para el foco y el badge "Nuevo".

| Intent / variante | Mantine | Acciones de Despacho |
|---|---|---|
| `primary` / `filled` | `<Button>` | Nueva zona, Guardar zona, Guardar tarifa, Confirmar asignación, Confirmar reasignación, Guardar orden, Confirmar recepción, Confirmar reprogramación, Nuevo repartidor, Guardar, Nuevo vehículo, Abrir jornada, Ingresar, En camino, Confirmar entrega, Registrar fallo, Cerrar jornada (pantalla), Volver a mi ruta. |
| secundaria / `outline` | `<Button variant="outline">` | **Acciones de fila que inician el flujo principal** ("Asignar" en F-02, "Confirmar recepción" en F-04), Cancelar (en modales y formularios), Generar pedido de prueba, Reintentar, Actualizar cola, **Marcar como fallido** (F-03), Ver resumen. |
| terciaria / `subtle` | `<Button variant="subtle">` | Limpiar filtros, Editar, Tarifas, Ver detalle, Reasignar, Descartar, Volver a tomar, Agregar rango, Ver foto, Reintentar vinculación (fila), Configurar tarifas (enlace en notificación). |
| `destructive` / `filled` | `<Button color="red">` | Desactivar zona, Cerrar despacho (devuelto a origen), Dar de baja, Sí, cerrar (jornada), Cerrar turno (confirmación). |
| `destructive` / `subtle` | `<Button variant="subtle" color="red">` | Acción "Desactivar" y "Dar de baja" en la fila de una tabla (abre el modal; no ejecuta). |

Reglas adicionales:

- **Tamaño:** `md` en la aplicación administrativa, `sm` dentro de tablas y barras de filtros, `lg` + `fullWidth` en la web del repartidor (§4.5).
- **Orden en pies de modal y formulario:** alineados a la derecha, `Cancelar` a la izquierda de la acción principal. En móvil, la acción principal va abajo a ancho completo y la secundaria encima.
- **Loading:** toda acción que cambia un estado usa `loading` (bloquea el doble clic o doble toque, requisito de F-03 y de idempotencia del backend). El texto del botón se conserva.
- **Deshabilitado con explicación:** cuando una acción está deshabilitada por una regla de negocio, se muestra el motivo como texto visible debajo o al lado (`Typography/Body/Small`, `text/secondary`), no solo en un tooltip. Ejemplos: "Disponible desde 08/10/2026", "Primero confirma la recepción del paquete", "Se alcanzó el máximo de intentos (2 de 2)".
- **Acciones solo con icono** (subir, bajar, cerrar panel, ver foto en tabla): `ActionIcon variant="subtle"` con `aria-label`; tamaño `lg` (34 px) en escritorio y `xl` (44 px) en móvil.

### 12.2. Campos de formulario

| Necesidad de Despacho | Componente Mantine | Configuración |
|---|---|---|
| Nombre de zona, nombres, apellidos, correo, brevete, placa | `TextInput` | Label visible, `required` cuando aplica, error con instrucción ("Ingresa el nombre de la zona"). Placa con `maxLength` y texto en mayúsculas al escribir. |
| DNI | `TextInput` | `inputMode="numeric"`, `maxLength={8}`, error "Ingresa un DNI de 8 dígitos". En edición: `readOnly` con `description` "El DNI no se puede modificar". |
| Teléfono | `TextInput` | `type="tel"`, `inputMode="tel"`. |
| Contraseña (acceso del repartidor) | `PasswordInput` | `size="lg"`. |
| Tarifa base, recargos | `NumberInput` | `leftSection="PEN"` (texto, ancho 48 px), `decimalScale={2}`, `fixedDecimalScale`, `min={0}`, `allowNegative={false}`. |
| Peso, volumen, máximo de paquetes, factor volumétrico | `NumberInput` | `rightSection` con la unidad (`kg`, `m³`, `paq.`), `min={0}` y validación "> 0" donde aplique. |
| Búsqueda (zona, repartidor, DNI, placa) | `TextInput` + `IconSearch` | `leftSection`, limpiar con `ActionIcon` (`aria-label="Limpiar búsqueda"`), búsqueda con *debounce* de 300 ms. |
| Distritos de la zona | `MultiSelect` | `searchable`, `clearable`, `hidePickedOptions`, `limit={50}` (§11.6). |
| Códigos postales | `TagsInput` | `description` "Escribe un código y presiona Enter", validación de formato por tag. |
| Estado, turno, tipo de vehículo, zona, motivo (filtro) | `Select` | `clearable` en filtros; `searchable` si tiene más de 8 opciones. |
| Estado inicial de la zona, sello intacto (Sí / No) | `SegmentedControl` (escritorio) / `Radio.Group` | En F-04 el sello usa `Radio.Group` obligatorio sin valor por defecto. |
| Motivo de entrega fallida (F-03) | `Radio.Group` con tarjetas (`Radio.Card`) | Cada opción ocupa el ancho completo y mide al menos 56 px de alto. |
| Fecha programada, rango del incidente, fecha de reprogramación | `DatePickerInput` (`@mantine/dates`) | `locale="es"`, `valueFormat="DD/MM/YYYY"`; en reprogramación `minDate` = mañana. Rango con `type="range"`. |
| Comentario, observaciones, motivo de cierre o reasignación | `Textarea` | `autosize`, `minRows={3}`, contador "0/250" en `Typography/Auxiliary`. |
| Repartidor, vehículo y zona en Asignación diaria | `Select` con `renderOption` | La opción muestra datos clave: placa y límites del vehículo; zona activa. |

Estados de campo que deben existir en Figma y código (§11.4): default, hover, focus (anillo signal), filled, disabled, loading (búsqueda y selects asíncronos) y error (borde y mensaje `error/default` con `IconAlertCircle`).

### 12.3. Tablas

- Componente `Table` de Mantine dentro de una `Card` blanca con `radius="md"` y borde `gray.3`; lógica de orden, filtro y paginación con `@tanstack/react-table`.
- Encabezado: fondo `cloud-subtle`, `Typography/Label` en `text/secondary`, `Table.Thead` con posición *sticky* cuando la tabla tiene scroll vertical.
- Filas: 48 px de alto mínimo, `highlightOnHover`, texto `Body/Small`.
- Columnas numéricas alineadas a la derecha con `ia-num`; códigos, estados y acciones a la izquierda; acciones agrupadas en la última columna.
- Más de dos acciones por fila: las dos más frecuentes visibles y el resto en un `Menu` con `ActionIcon` `IconDots` (`aria-label="Más acciones"`).
- Paginación inferior con `Pagination` (tamaño `sm`) y el texto "Mostrando 1–20 de 134" a la izquierda. Tamaño de página por defecto: 20; F-05 pagina a partir de 50 registros según su especificación.

### 12.4. Badges, chips y pills

Se aplica §11.7 sin cambios. `Badge` para estados (§16), `Pill` con `withRemoveButton` para distritos seleccionados y filtros activos (botón con `aria-label` "Quitar [valor]") y `Chip` para filtros rápidos de la cola (Todos / Primer intento / Reintentos) cuando se use una variante de filtros compacta.

### 12.5. Navegación y estructura

| Necesidad | Componente |
|---|---|
| Estructura administrativa | `AppShell` con `navbar` (256 px) y `header` (64 px) |
| Ítems de la barra lateral | `NavLink` con icono 24 px, texto inverse; activo con fondo `ink-soft`, borde izquierdo de 4 px `action/primary` y peso 600 |
| Pestañas de F-02 | `Tabs` (`variant="default"`), indicador en `action/primary` |
| Ruta de navegación | `Breadcrumbs` en `Body/Small`, último elemento en `text/primary` sin enlace |
| Navegación inferior de F-03 | Componente propio `NavegacionInferior` con tres `UnstyledButton` de 64 px de alto, icono 24 px y `Typography/Label`; activo en `action/primary-hover` con indicador superior de 4 px |

### 12.6. Superposiciones

| Tipo | Componente | Uso en el módulo |
|---|---|---|
| Modal estándar (480 px) | `Modal size="md"` | Desactivar o activar zona, confirmar recepción, reprogramación, cierre como devuelto a origen, dar de baja, enviar a mantenimiento, cerrar turno, descartar cambios. |
| Modal amplio (880 px) | `Modal size={880}` | Asignación y reasignación (F-02), formulario de repartidor y de vehículo (F-05). |
| Panel lateral (560 px) | `Drawer position="right"` | Tarifas de la zona (F-01). |
| Hoja inferior móvil | `Drawer position="bottom"` con esquinas superiores `radius/lg` | Confirmación de cierre de jornada y visor de foto en F-03 (alcance del pulgar). |
| Visor de foto | `Modal size="xl"` con `Image fit="contain"` | Evidencia en F-03 y F-04. |

Reglas: el foco entra al primer control del modal y vuelve al botón que lo abrió; `Esc` y el botón de cierre funcionan salvo durante `loading`; el clic en el fondo **no** cierra modales con formularios para no perder datos.

### 12.7. Retroalimentación

| Situación | Componente | Color |
|---|---|---|
| Operación exitosa (crear, guardar, asignar, registrar) | `notifications.show` | `green`, `IconCircleCheck`, cierre automático a los 4 s |
| Operación registrada con efecto pendiente (notificación a Ventas pendiente, vinculación pendiente) | `notifications.show` | `yellow`, `IconAlertTriangle`, sin cierre automático |
| Error dentro de un formulario o modal (`409`, `422`, red) | `Alert` dentro del contenedor, encima de los campos | `red` o `yellow` según §13.12 |
| Advertencia previa a una acción (capacidad excedida, pendientes al cerrar jornada) | `Alert` | `yellow` |
| Texto informativo fijo ("La regla se aplicará a las cotizaciones siguientes") | `Alert variant="light"` | `blue` |
| Carga de una vista | `Skeleton` con la forma del contenido final | `cloud-subtle` |
| Carga de una acción | `Button loading` | — |
| Subida de foto | `Progress` con porcentaje visible | `orange` |

---

## 13. Organismos y patrones comunes

La Guía define cinco patrones comunes: tarjeta de producto, barra de navegación, filtros de catálogo, modales y pantallas de carga con skeletons.

- **Tarjeta de producto:** reúne imagen con texto alternativo, nombre y datos que lo diferencian, precio y promoción, disponibilidad o stock, y acciones autorizadas, con estructura consistente en catálogo, búsqueda y recomendaciones. Despacho no muestra productos; su equivalente es la tarjeta de despacho de la web del repartidor (§13.2), que sigue la misma lógica: datos para reconocer el elemento, estado y acción.
- **Barra de navegación:** identifica la marca, da acceso a las áreas principales y conserva la prioridad de las acciones entre escritorio y móvil. En Despacho se concreta en los shells de §13.1 y §13.2.
- **Filtros:** reducen el listado, muestran qué opciones están activas y permiten aplicarlas, limpiarlas o retirarlas sin perder el contexto de los resultados. En Despacho: §13.4.
- **Modales:** se reservan para acciones que requieren atención antes de continuar; incluyen título, contenido, acción principal, alternativa o cancelación y una forma clara de cerrarlos. En Despacho: §12.6 y §13.7.
- **Skeletons:** representan la estructura que aparecerá al terminar la carga y se aproximan al tamaño del contenido final. En Despacho: §12.7 y §13.4.

A continuación se define cada patrón tal como se usa en Despacho.

### 13.1. Shell administrativo (F-01, F-02, F-04, F-05)

```text
┌──────────────┬─────────────────────────────────────────────────────┐
│ LOGO inverso │ Encabezado 64 px · cloud                             │
│              │ [Contexto de la pantalla]          [Usuario ▾]       │
│ ink · 256 px ├─────────────────────────────────────────────────────┤
│              │ Contenido · cloud · grilla de la Guía (márgenes 32 px)│
│ ▌Zonas y     │  H1 TÍTULO DE PÁGINA            [Acción principal]   │
│  Tarifas     │  Subtítulo (text/secondary)                          │
│  Programación│  ── 24 px ──                                         │
│  Entregas    │  [KPI] [KPI] [KPI] [KPI]                             │
│  fallidas    │  ── 24 px ──                                         │
│  Monitoreo   │  Filtros (cloud-subtle)                              │
│  Repartidores│  ── 16 px ──                                         │
│  Vehículos   │  Tabla (Card blanca)                                 │
│  Asignación  │                                                      │
│  diaria      │                                                      │
│ ──────────── │                                                      │
│  Cerrar      │                                                      │
│  sesión      │                                                      │
└──────────────┴─────────────────────────────────────────────────────┘
```

- **Logo:** sobre ink se usa la versión inversa (blanca), como indica §3.4. No se sustituye por la variante volt, reservada para promociones y campañas. `alt="Inka Athletics"` porque funciona como enlace al inicio. Debajo, en `Typography/Auxiliary` inverse: "Despacho".
- **Orden de la barra lateral** (por frecuencia de uso en la jornada): Programación, Monitoreo de flota, Entregas fallidas, Asignación diaria, Repartidores, Vehículos, Zonas y Tarifas.
- **Encabezado:** a la izquierda el contexto (por ejemplo, fecha de jornada en F-02 y F-05); a la derecha `Menu` del usuario con nombre, rol ("Gestor de Despacho") y "Cerrar sesión".

### 13.2. Shell del repartidor (F-03)

```text
┌──────────────────────────────┐
│ ← MI RUTA        [En ruta]   │  Encabezado 56 px · ink
├──────────────────────────────┤
│ Hola, Juan · Lunes 5 oct.    │  Subtitle
│ 4 de 12 despachos resueltos  │
│ ████████░░░░░░░░░░░░░░░░░░   │  Progress (orange)
│                              │
│ ┌──────────────────────────┐ │
│ │ ① SIGUIENTE              │ │  Tarjeta · primary-soft
│ │ DSP-000123   [Asignado]  │ │
│ │ Av. Arequipa 1234, Lince │ │
│ │ María Torres · Int. 1/2  │ │
│ └──────────────────────────┘ │
│ ┌──────────────────────────┐ │
│ │ ②  DSP-000124  [...]     │ │  Tarjeta · blanca
│ └──────────────────────────┘ │
├──────────────────────────────┤
│  Mi Ruta   Resumen   Cerrar  │  Navegación 64 px · blanca
└──────────────────────────────┘
```

- Sin barra lateral (requisito de los lineamientos §5.2).
- En pantallas de detalle y formularios, la navegación inferior se reemplaza por la **barra de acciones fija** (§13.9).
- Franjas de estado globales (fuera de turno, sin conexión) se ubican debajo del encabezado, fijas, a ancho completo (§13.12).

### 13.3. Encabezado de página

- `Title order={1}` + subtítulo `Body` en `text/secondary` a la izquierda; acción principal a la derecha (`Group justify="space-between"`).
- Si la página tiene pestañas (F-02), van debajo del encabezado y antes de los indicadores.
- Si la página es de segundo nivel (formulario de zona, detalle de incidencia), arriba aparece `Breadcrumbs`.

### 13.4. Barra de filtros + tabla

- Contenedor `cloud-subtle`, `radius/md`, padding 16 px; controles en `size="sm"` en una fila (`Group gap="md"`), con salto de línea en anchos menores.
- Orden: búsqueda (más ancha) → selectores → fechas → "Limpiar filtros" (`subtle`, solo habilitado si hay filtros activos).
- Los filtros se aplican al cambiar (sin botón "Aplicar"), porque son consultas rápidas sobre un listado.
- Los filtros activos se reflejan en la URL (`?zona=lima-centro&estado=activo`) para conservar el contexto al volver desde un detalle.

Estados de la tabla (todos obligatorios donde la especificación los pide):

| Estado | Presentación |
|---|---|
| Carga | 5 filas `Skeleton` de 48 px con las mismas columnas; los filtros siguen visibles. |
| Vacío (sin registros) | Componente `EstadoVacio`: icono 48 px en `text/secondary`, título H4, texto `Body` y acción principal de la pantalla. |
| Sin resultados (filtros) | `EstadoVacio` con icono `IconFilterOff`, texto "No encontramos resultados con estos filtros" y botón `subtle` "Limpiar filtros". |
| Error de red | `EstadoError`: `Alert` rojo "No pudimos cargar la información. Inténtalo nuevamente." con botón `outline` "Reintentar". |
| Acceso denegado (`403`) | `AccesoDenegado`: reemplaza todo el contenido (sin tabla ni filtros), icono `IconLock`, mensaje de la especificación. |

### 13.5. Tarjetas de indicadores (KPI)

- `Card` blanca, `radius/md`, padding 16 px, en una grilla con los gutters §6.2: `SimpleGrid cols={{ base: 1, xs: 2, md: 4 }} spacing={{ base: 16, sm: 20, md: 24 }}` (3 columnas cuando son tres indicadores).
- Contenido: etiqueta `Typography/Label` en `text/secondary` + icono 20 px a la derecha; valor con el estilo `Typography/Heading/H2` (Oswald 700, 28/36; §5 admite Oswald en "elementos de alto impacto") y `ia-num`; descripción opcional en `Auxiliary`.
- El color solo aparece en el icono y en un borde superior de 4 px cuando el indicador representa un estado (por ejemplo, "Retornos atrasados" en `error/default`, "Saturado" en `error/default`, "Disponible" en `accent/volt`).
- Si el indicador es accionable (filtra la tabla al hacer clic), la tarjeta es un `UnstyledButton` con foco visible y `aria-pressed` cuando el filtro está activo.

### 13.6. Componente `BarraOcupacion`

Componente único para F-02 (lista de repartidores, modal de asignación y reasignación, encabezado de ruta) y F-05 (tablero).

```text
Peso        320 / 500 kg (64 %)                Normal
████████████████████░░░░░░░░░░░
Volumen     3.2 / 4.0 m³ (80 %)                ⚠ Alta
████████████████████████░░░░░░░
Paquetes    50 / 50 paq. (100 %)               ⓘ Llena
███████████████████████████████
```

| Propiedad | Valores | Descripción |
|---|---|---|
| `metrica` | `peso` \| `volumen` \| `paquetes` | Define etiqueta y unidad. |
| `usado`, `limite` | número | El porcentaje se calcula en el componente. |
| `proyeccion` | número (opcional) | Ocupación resultante si se asigna el despacho seleccionado. |
| `variante` | `completa` \| `compacta` | `completa`: etiqueta, valores y nivel en una fila sobre la barra de 8 px. `compacta`: barra de 4 px con porcentaje a la derecha (lista lateral de F-02). |

- Implementación con `Progress.Root` de Mantine (tamaño 8 px, `radius/xs`, pista `cloud-subtle`) y un segundo `Progress.Section` para la proyección con relleno a rayas diagonales (`striped`) del color del **nivel resultante**.
- Si la proyección supera el 100 %, la sección se recorta en el 100 % y aparece debajo el texto `error/default` "Excede en 40 kg".
- El color depende del nivel (§16.6). En F-05, cuando el repartidor está saturado, la barra que llegó al 100 % se resalta con la etiqueta "Llena" en peso 600.
- Accesibilidad: `role="progressbar"`, `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"` y `aria-label="Peso: 320 de 500 kg, 64 %, nivel normal"`.

### 13.7. Modal de confirmación

```text
┌─────────────────────────────────────────┐
│ ⚠  ¿DESACTIVAR LA ZONA LIMA NORTE?   ✕  │  H3 + icono 24 px
│                                         │
│ Texto explicativo de efectos (Body)     │
│                                         │
│ [Alert de error si la operación falla]  │
│                                         │
│                 [Cancelar] [Desactivar  │
│                             zona]       │
└─────────────────────────────────────────┘
```

- Título en forma de pregunta con el nombre del objeto afectado.
- El texto explica primero el efecto y después lo que se conserva (§10.2).
- La acción de confirmación repite el verbo del título ("Desactivar zona", no "Aceptar").
- Acciones irreversibles o de cierre usan `intent=destructive` e icono `IconAlertTriangle` en `warning/default` junto al título. Las confirmaciones no destructivas (activar zona, confirmar recepción) usan `IconInfoCircle` en `info/default` y botón `primary`.
- El foco inicial va a "Cancelar" en los modales destructivos.

### 13.8. Panel lateral (tarifas de F-01)

- `Drawer` de 560 px a la derecha, encabezado con H3 + badge de estado de la zona + botón de cierre; cuerpo desplazable con secciones separadas por `Divider` y H4; pie fijo con "Cancelar" y "Guardar tarifa".
- La tabla editable de rangos usa `Table` con `NumberInput size="sm"` en cada celda, `ActionIcon` `IconTrash` (`aria-label="Eliminar rango"`) y la fila inconsistente con fondo `error/background` y mensaje debajo.

### 13.9. Barra de acciones fija

- **Escritorio** (formulario de zona): barra blanca al pie del área de contenido, borde superior `gray.3`, padding 16 px, botones alineados a la derecha.
- **Móvil** (detalle, entrega, fallo, cierre): barra blanca fija en la parte inferior con padding 16 px + zona segura; acción principal `lg` a ancho completo; si hay acción secundaria, va encima (`Stack gap="sm"`). El contenido de la página reserva un margen inferior igual a la altura de la barra para que nada quede oculto.

### 13.10. Captura de evidencia fotográfica (F-03)

```text
┌────────────────────────────┐
│                            │
│        [ IconCamera ]      │  Área 4:3 · borde discontinuo border/default
│        Tomar foto          │  radius/lg · fondo blanco
│ Foto obligatoria del       │
│ paquete entregado          │
└────────────────────────────┘
```

- `FileButton` con `accept="image/*"` y `capture="environment"` para abrir la cámara trasera; toda el área es táctil.
- Con foto: previsualización `Image fit="cover"` en el mismo marco + botón `subtle` "Volver a tomar".
- Procesamiento: texto "Optimizando imagen…" con `Loader size="sm"`; envío: `Progress` con porcentaje.
- Error: `Alert` rojo con el mensaje de la especificación y "Reintentar"; **la foto se conserva** en pantalla.
- Validación: si el usuario intenta confirmar sin foto, el marco cambia a borde `error/default` y aparece el mensaje "Debes tomar una foto como evidencia".

### 13.11. Lista reordenable de ruta (F-02, Pantalla 3)

- Cada despacho en `ASIGNADO` es una fila con número de posición (`Typography/Subtitle`, `ia-num`), `IconGripVertical` como asa de arrastre y `ActionIcon` "Subir" y "Bajar" como alternativa accesible por teclado.
- Despachos que ya iniciaron o cerraron su ciclo se agrupan debajo de un `Divider` con la etiqueta "En curso o finalizados", en filas atenuadas (§16.5) y sin controles de orden.
- Mientras haya cambios sin guardar, aparece una barra `warning/background` fija sobre la lista con el texto de la especificación, "Descartar" (`subtle`) y "Guardar orden" (`primary`). Al intentar salir de la pestaña con cambios, se muestra el modal "¿Descartar los cambios?".
- Al mover un elemento con teclado, se anuncia la nueva posición con una región `aria-live="polite"` ("DSP-000123 movido a la posición 3 de 8").

### 13.12. Respuestas del sistema y su presentación

| Respuesta | Presentación | Ejemplo de texto |
|---|---|---|
| Validación de cliente | Error bajo el campo; acción principal deshabilitada mientras falten obligatorios | "Ingresa el nombre de la zona" |
| `400` | Errores bajo cada campo indicado por el backend + `Alert` rojo resumen si el campo no es visible | "Revisa los rangos de peso marcados" |
| `401` | Redirección al acceso con `Alert` informativo | "Tu sesión expiró. Ingresa nuevamente." |
| `403` | `AccesoDenegado` a pantalla completa | "No tienes permisos para ver la configuración de zonas" |
| `404` | `EstadoVacio` con "Volver al listado" | "No encontramos este despacho" |
| `409` | `Alert` amarillo en el contenedor + recarga de los datos + acción "Actualizar" | "El despacho cambió de estado. Se actualizó la información." |
| `422` | `Alert` rojo con el límite o regla incumplida; la acción no se aplica | "Capacidad de carga del repartidor excedida: peso" |
| Error de red o tiempo de espera | `Alert` rojo con "Reintentar"; los datos ingresados se conservan | "No pudimos guardar los cambios. Inténtalo nuevamente." |
| Sin conexión (F-03) | Franja fija `error/background` bajo el encabezado con `IconWifiOff` | "Sin conexión. Revisa tu señal." |
| Fuera de turno (F-03) | Franja fija `warning/background` bajo el encabezado; acciones deshabilitadas | "Tu turno no está activo. Solo puedes consultar tu ruta." |
| Error al refrescar datos (F-05) | Franja `warning/background` sobre la tabla, **sin borrar** los últimos datos | "No se pudo actualizar la información" |

Nunca se muestran códigos HTTP, nombres de enums ni mensajes técnicos al usuario (§10.2).

---

## 14. Gobernanza y trabajo en Figma

### 14.1. Biblioteca central y reglas de trabajo

- El archivo central se publica como Team Library de Figma y contiene foundations, componentes y patrones compartidos. Cada módulo mantiene sus pantallas y flujos en su propio archivo y consume los componentes publicados, sin crear versiones maestras propias.
- Las instancias se actualizan desde la biblioteca cuando se publica una nueva versión. Los componentes específicos de un módulo permanecen locales hasta demostrar que son reutilizables.
- La biblioteca tiene una sola persona responsable de editar, aprobar y publicar. Los demás usan la biblioteca y envían propuestas; no modifican los componentes maestros.

**Propuesta de un componente nuevo:** (1) comprobar que no exista un componente o variante que cubra la necesidad; (2) describir el problema, las pantallas afectadas y por qué es reutilizable; (3) adjuntar la propuesta visual en el archivo del módulo; (4) incluir variantes, estados, responsive, contenido de ejemplo y accesibilidad; (5) enviarla por el canal acordado; (6) tras la aprobación, incorporarla a la biblioteca, documentarla y publicar.

**Criterios de aceptación de una propuesta:** resuelve una necesidad real; es reutilizable o extiende un componente sin duplicarlo; respeta foundations, UX Writing y patrones; incluye estados y responsive; se usa con teclado y comunica sus estados de forma comprensible; tiene equivalencia clara entre Figma e implementación.

**Actualización de un componente existente:** explicar qué resuelve y qué módulos afecta; no eliminar propiedades o variantes en uso sin revisar sus instancias; probar el cambio en una pantalla representativa; registrar qué cambió y qué debe revisar cada módulo; comunicar la publicación.

**Revisión antes de publicar:** nombre según la convención; propiedades y variantes ordenadas y comprensibles; estados representados; estilos o variables de foundations; contenido de ejemplo según UX Writing; responsive documentado; probado en una pantalla real; actualización comunicada.

### 14.2. Organización del archivo de Despacho

El módulo consume la Team Library central de la Guía y mantiene sus pantallas en un archivo propio (§14.1):

```text
Despacho — UX/UI
├── 00 Portada y registro de cambios
├── 01 Componentes del módulo (locales)   ← BadgeEstado, BarraOcupacion, TarjetaKpi,
│                                            TarjetaDespacho, EstadoVacio, CapturaEvidencia
├── 02 Shells                              ← Shell administrativo y shell del repartidor
├── 10 F-01 Zonas y Tarifas
├── 20 F-02 Programación y Asignación
├── 30 F-03 Repartidor
├── 40 F-04 Entregas Fallidas
├── 50 F-05 Flota y Capacidad
└── 90 Wireframes (baja fidelidad, archivo histórico)
```

Dentro de cada página de funcionalidad: una sección por pantalla, con el frame principal a la izquierda y sus estados (carga, vacío, error, `403`, `409`, confirmación) a la derecha, nombrados igual que en la especificación.

### 14.3. Convención de nombres

Despacho usa la estructura de nombres indicada en la Guía: `categoría / componente / variante`, alineada con los nombres de código:

| Elemento | Ejemplo en Figma | Ejemplo en código |
|---|---|---|
| Componente del módulo | `Dominio / BadgeEstado / EnCamino` | `<BadgeEstado valor="EN_CAMINO" />` |
| Componente del módulo | `Dominio / BarraOcupacion / Completa` | `<BarraOcupacion variante="completa" />` |
| Patrón | `Feedback / EstadoVacio / SinResultados` | `<EstadoVacio tipo="sinResultados" />` |
| Frame de pantalla | `F-02 / P2 Modal de asignación / Capacidad excedida` | `features/programacion/ModalAsignacion.tsx` |

Las propiedades de componente usan los mismos nombres que las props de código (`variante`, `metrica`, `estado`, `size`, `disabled`).

### 14.4. Paso de wireframe a alta fidelidad

1. Completar en cada `f-0X.md` la sección "Registro del wireframe generado".
2. Realizar y registrar la evaluación heurística de Nielsen por un compañero distinto al responsable.
3. Corregir los hallazgos en el wireframe.
4. Construir la alta fidelidad usando **solo** componentes de la Team Library y del archivo del módulo, y tokens de §4.
5. Revisar con la lista de §25 y registrar el enlace al frame de alta fidelidad en la especificación.

### 14.5. Componentes candidatos a la biblioteca central

`BarraOcupacion`, `TarjetaKpi`, `EstadoVacio` y el patrón de respuestas del sistema (§13.12) son propios de Despacho. Según §14.1, permanecen locales hasta demostrar reutilización y luego se proponen §14.1.

---

> **PARTE II — IMPLEMENTACIÓN**

## 15. Base técnica

### 15.1. Stack de la interfaz

El frontend de Despacho se implementa con el stack que define la Guía: **Mantine 9.6.2 sobre React y TypeScript**. Mantine 9 requiere React 19.2 o superior. El tema de Mantine es el único origen de estilos: no se usan Tailwind CSS ni hojas de estilo con valores sueltos.

| Paquete | Versión | Uso |
|---|---|---|
| `react`, `react-dom` | `^19.2.0` | Base requerida por Mantine 9 |
| `@mantine/core`, `@mantine/hooks` | `9.6.2` | UI Kit (§11) |
| `@mantine/dates` + `dayjs` | `9.6.2` + `^1.11` | Selectores de fecha y formato en español |
| `@mantine/notifications` | `9.6.2` | Notificaciones del sistema |
| `@tabler/icons-react` | `3.x` | Iconografía (§8) |
| `postcss-preset-mantine`, `postcss-simple-vars` | última | Breakpoints y utilidades CSS de Mantine |
| `@testing-library/react` | `^16` | Pruebas de componentes con React 19 |

Se integran con Mantine las librerías sin estilos propios: `react-router-dom` (rutas), `axios` (API), `@tanstack/react-table` (lógica de tablas renderizada con `Table` de Mantine), `react-hook-form` + `zod` (validación conectada a los inputs con `Controller`) y `zustand` (estado global). El proyecto se crea con la plantilla `react-ts` de Vite.

### 15.2. Tema de Mantine (`src/theme/theme.ts`)

Las paletas personalizadas tienen 10 tonos. El valor de marca se ubica en el **índice 7** para que `variant="filled"` lo use directamente (§4.5). La paleta `orange` reemplaza el índice 8 por `#C2410C` para que el hover nativo de Mantine coincida con `color/action/primary-hover`.

```ts
import { createTheme, type MantineColorsTuple } from '@mantine/core';

const orange: MantineColorsTuple = [
  '#FFF4E6', '#FCE3D0', '#FFD8A8', '#FFC078', '#FFA94D',
  '#FF922B', '#FD7E14', '#F76707', '#C2410C', '#9A3412',
];
const volt: MantineColorsTuple = [
  '#FBFEE0', '#F5FCC2', '#EEF7B0', '#E4F48A', '#D9EF5E',
  '#CFEA33', '#C8E81A', '#C3E504', '#9DB803', '#5C6B00',
];
const signal: MantineColorsTuple = [
  '#EEF0FE', '#E1E6FB', '#C3CDF8', '#A2B1F4', '#8297F2',
  '#6A82F0', '#5670EF', '#4361EE', '#3550D4', '#1B2A99',
];
const ink: MantineColorsTuple = [
  '#F5F4F2', '#E4E2DD', '#C9C5BC', '#A39E92', '#7D776A',
  '#5A5447', '#46402F', '#3A362C', '#26221A', '#1B1812',
];
const cloud: MantineColorsTuple = [
  '#FFFFFF', '#F7F5F0', '#EDEAE2', '#E2DED3', '#D6D2C4',
  '#BDB8A8', '#A39E8D', '#888372', '#6D6858', '#524E40',
];

export const theme = createTheme({
  primaryColor: 'orange',
  primaryShade: 7,
  autoContrast: true,
  luminanceThreshold: 0.2, // §4.5: evita texto blanco sobre #F76707
  black: '#1B1812',        // color/text/primary
  white: '#FFFFFF',
  colors: { orange, volt, signal, ink, cloud },

  fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  headings: {
    fontFamily: 'Oswald, "Segoe UI", sans-serif',
    fontWeight: '700',
    sizes: {
      h1: { fontSize: '2rem', lineHeight: '2.5rem' },
      h2: { fontSize: '1.75rem', lineHeight: '2.25rem' },
      h3: { fontSize: '1.5rem', lineHeight: '2rem' },
      h4: { fontSize: '1.25rem', lineHeight: '1.75rem' },
    },
  },
  fontSizes: { xs: '0.75rem', sm: '0.875rem', md: '1rem', lg: '1.125rem', xl: '1.25rem' },
  lineHeights: { xs: '1rem', sm: '1.25rem', md: '1.5rem', lg: '1.625rem', xl: '1.75rem' },

  spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '2rem' },
  radius: { xs: '0.25rem', sm: '0.5rem', md: '0.75rem', lg: '1rem', xl: '999px' },
  defaultRadius: 'sm',

  focusClassName: 'ia-focus', // anillo de foco en signal (ver tokens.css)

  components: {
    Button: { defaultProps: { size: 'md', radius: 'sm' } },
    Badge: { defaultProps: { size: 'sm', radius: 'xl', variant: 'light' } },
    Card: { defaultProps: { radius: 'md', padding: 'md', withBorder: true } },
    Modal: { defaultProps: { radius: 'lg', centered: true, overlayProps: { backgroundOpacity: 0.55 } } },
    Drawer: { defaultProps: { position: 'right', size: 560 } },
    TextInput: { defaultProps: { size: 'md' } },
    Select: { defaultProps: { size: 'md', nothingFoundMessage: 'Sin resultados' } },
    MultiSelect: { defaultProps: { size: 'md', nothingFoundMessage: 'Sin resultados' } },
    Table: { defaultProps: { verticalSpacing: 'sm', horizontalSpacing: 'md', highlightOnHover: true } },
    Notification: { defaultProps: { radius: 'md', withBorder: true } },
  },
});
```

### 15.3. Tokens y reglas globales (`src/theme/tokens.css`)

Los tokens de la Guía se exponen también como variables CSS con el mismo nombre que en Figma (prefijo `--ia-`, de Inka Athletics), para usarlos en CSS Modules sin escribir valores HEX.

```css
:root {
  --ia-color-action-primary: #F76707;
  --ia-color-action-primary-hover: #C2410C;
  --ia-color-action-primary-soft: #FCE3D0;
  --ia-color-accent-volt: #C3E504;
  --ia-color-accent-volt-soft: #EEF7B0;
  --ia-color-accent-signal: #4361EE;
  --ia-color-accent-signal-soft: #E1E6FB;
  --ia-color-surface-ink: #1B1812;
  --ia-color-surface-ink-soft: #26221A;
  --ia-color-surface-cloud: #F7F5F0;
  --ia-color-surface-cloud-subtle: #EDEAE2;
  --ia-color-text-primary: #1B1812;
  --ia-color-text-inverse: #F7F5F0;
  --ia-color-text-secondary: #495057;
  --ia-color-text-disabled: #868E96;
  --ia-color-border-default: #DEE2E6;
  --ia-color-border-inverse: #3A362C;
  --ia-color-success-default: #2F9E44;
  --ia-color-success-background: #EBFBEE;
  --ia-color-warning-default: #F08C00;
  --ia-color-warning-background: #FFF9DB;
  --ia-color-error-default: #E03131;
  --ia-color-error-background: #FFF5F5;
  --ia-color-info-default: #1971C2;
  --ia-color-info-background: #E7F5FF;
}

body {
  background: var(--ia-color-surface-cloud);
  color: var(--ia-color-text-primary);
}

/* mayúsculas solo en H1–H3; H4–H6 vuelven a Inter */
.mantine-Title-root:is(h1, h2, h3) { text-transform: uppercase; }
.mantine-Title-root:is(h4, h5, h6) { font-family: var(--mantine-font-family); }

/* anillo de foco global en signal (§11.2) */
.ia-focus:focus-visible {
  outline: 2px solid var(--ia-color-accent-signal);
  outline-offset: 2px;
}

/* texto inverse en el hover del botón principal */
.mantine-Button-root[data-variant='filled']:not([data-disabled]):hover {
  --button-color: var(--ia-color-text-inverse);
}
/* También es válido para destructive (hover red.9) y signal (hover signal.8):
   ambos fondos de hover son oscuros y mantienen contraste AA con texto inverse.
   Volt nunca se usa como botón (§11.3). */

/* Cifras alineadas en tablas, KPI y capacidades */
.ia-num { font-variant-numeric: tabular-nums; }
```

### 15.4. Configuración de `MantineProvider`

```tsx
import '@mantine/core/styles.css';
import '@mantine/dates/styles.css';
import '@mantine/notifications/styles.css';
import './theme/tokens.css';
import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { theme } from './theme/theme';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <MantineProvider theme={theme} defaultColorScheme="light">
      <Notifications position="top-right" limit={3} autoClose={4000} />
      {children}
    </MantineProvider>
  );
}
```

En la web del repartidor, `Notifications` usa `position="top-center"` para no tapar la barra de acciones inferior.

Las fuentes se cargan en `index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 15.5. Estructura de carpetas de UI

```text
src/
├── theme/
│   ├── theme.ts           # createTheme (§15.2)
│   └── tokens.css         # variables --ia-* y reglas globales (§15.3)
├── components/
│   ├── layout/            # ShellAdministrativo, ShellRepartidor, EncabezadoPagina
│   ├── feedback/          # EstadoVacio, EstadoError, AccesoDenegado, FranjaConexion
│   ├── dominio/           # BadgeEstadoDespacho, BarraOcupacion, TarjetaKpi, TarjetaDespacho
│   └── formularios/       # CampoMoneda, CapturaEvidencia, BarraAccionesFija
└── features/
    ├── zonas/             # F-01
    ├── programacion/      # F-02
    ├── repartidor/        # F-03
    ├── entregas-fallidas/ # F-04
    └── flota/             # F-05
```

Los nombres de componentes y archivos siguen la regla de idioma de `AGENTS.md` §2: en español, salvo términos técnicos de las librerías.

---

## 16. Representación visual de los estados del dominio

### 16.0. Regla de asignación

Cada estado del dominio de Despacho se asigna a **una** de las variantes de badge de §11.7 (`neutral`, `info`, `success`, `warning`, `error`, `availability`, `new`) con este criterio:

| Si el estado significa… | Variante | Tokens |
|---|---|---|
| Punto de partida, espera o cierre sin carga emocional | `neutral` | `surface/cloud-subtle` + `text/primary` |
| Avance normal, proceso en curso o información | `info` | `info/background` + `info/default` |
| Resultado exitoso | `success` | `success/background` + `success/default` |
| Requiere atención pero no bloquea | `warning` | `warning/background` + `warning/default` |
| Fallo, bloqueo o resultado negativo | `error` | `error/background` + `error/default` |
| Recurso disponible para usarse (repartidor, vehículo) | `availability` | `accent/volt-soft` + `text/primary` |
| Elemento recién creado | `new` | `accent/signal` + blanco |

Cuando dos estados de una misma pantalla comparten variante, se distinguen por su texto y su icono.

Todo estado se comunica con **texto + icono + color** (§4.2). Los badges usan `variant="light"` con texto `color/text/primary` sobre el fondo indicado, salvo cuando se especifica otra cosa. El componente `BadgeEstado` recibe el valor del enum y resuelve etiqueta, icono y color desde una única tabla de configuración en `src/components/dominio/estados.ts`, para que todas las pantallas muestren el mismo estado del mismo modo.

### 16.1. Estados del despacho

| Enum | Etiqueta visible | Fondo / color | Icono | Nota |
|---|---|---|---|---|
| `PENDIENTE_ASIGNACION` | Pendiente de asignación | `cloud-subtle` + ink | `IconClockHour4` | Neutral: es el punto de partida. |
| `ASIGNADO` | Asignado | `info` | `IconUserCheck` | Avance del proceso. |
| `EN_CAMINO` | En camino | `info` | `IconTruckDelivery` | Avance del proceso; se distingue de "Asignado" por texto e icono. |
| `ENTREGADO` | Entregado | `success/background` + `success/default` | `IconCircleCheck` | Final. |
| `FALLIDO` | Fallido | `error/background` + `error/default` | `IconAlertCircle` | En F-03 se acompaña del texto "No entregado, regresa al centro de despacho". |
| `DEVUELTO_A_ORIGEN` | Devuelto a origen | `warning/background` + ink | `IconArrowBackUp` | Final no exitoso que requiere gestión de Ventas y Postventa. |
| `CANCELADO` | Cancelado | `cloud-subtle` + `text/secondary` | `IconBan` | Final. |

### 16.2. Etiquetas especiales de fila

| Etiqueta | Dónde aparece | Fondo / color | Icono |
|---|---|---|---|
| Simulado | F-02, cola de pendientes | `neutral`: `cloud-subtle` + ink | `IconFlask` |
| Nuevo | Fila recién creada o generada (5 s) | `accent/signal` + blanco (`variant="filled"`) | — |
| Programado para [fecha] | F-02 | `info/background` + ink | `IconCalendarTime` |
| Reintento | F-02 | `warning/background` + ink | `IconRepeat` |
| Tiempo de espera elevado | F-02 | Solo icono en `text/primary` (§4.5) con `aria-label` "Tiempo de espera elevado" y tooltip | `IconClockExclamation` |
| No intentado | F-04 | `cloud-subtle` + ink | `IconClockPause` |
| Pedido anulado | F-04 | `error/background` + ink | `IconBan` |
| Retorno atrasado | F-04 | `error/background` + ink; la fila completa lleva borde izquierdo de 4 px `error/default` y fondo `error/background` | `IconAlertTriangle` |
| Sin tarifa configurada | F-01 | `warning/background` + ink | `IconAlertTriangle` |
| Siguiente | F-03, tarjeta del próximo despacho | `neutral` (la tarjeta completa lleva fondo `action/primary-soft` como elemento seleccionado) | `IconArrowRight` |

### 16.3. Estado operativo del repartidor

| Enum | Etiqueta | Fondo / color | Icono |
|---|---|---|---|
| `DISPONIBLE` | Disponible | `accent/volt-soft` + ink (variante `availability` §11.7) | `IconCircleCheck` |
| `EN_RUTA` | En ruta | `info` | `IconTruckDelivery` |
| `SATURADO` | Saturado | `error/background` + `error/default` | `IconGauge` |
| `FUERA_DE_TURNO` | Fuera de turno | `cloud-subtle` + `text/secondary` | `IconMoon` |

En F-03 el estado del repartidor se muestra en el encabezado ink con el mismo `BadgeEstado` y su variante de esta tabla: todos los fondos de badge son claros y mantienen texto `text/primary`, por lo que no se crea una variante para fondo oscuro.

### 16.4. Registro, vinculación, zonas, vehículos y recepción

| Contexto | Valor | Etiqueta | Fondo / color | Icono |
|---|---|---|---|---|
| Registro de repartidor y zona | `ACTIVO` | Activo | `success/background` | `IconCircleCheck` |
| Registro de repartidor y zona | `INACTIVO` | Inactivo | `cloud-subtle` + `text/secondary`; fila atenuada | `IconCircleOff` |
| Vinculación con Seguridad y Usuarios | `VINCULADO` | Vinculado | Sin badge: solo texto `text/secondary` | `IconLink` |
| Vinculación con Seguridad y Usuarios | `PENDIENTE` | Vinculación pendiente · No puede recibir jornada | `warning/background` + ink | `IconLinkOff` |
| Vehículo | `DISPONIBLE` | Disponible | `accent/volt-soft` + ink (`availability`) | `IconCircleCheck` |
| Vehículo | En jornada | En jornada | `info` | `IconTruck` |
| Vehículo | `EN_MANTENIMIENTO` | En mantenimiento | `warning/background` + ink | `IconTool` |
| Vehículo | `INACTIVO` | Inactivo | `cloud-subtle` + `text/secondary` | `IconCircleOff` |
| Recepción en centro (F-04) | Pendiente | Pendiente de retorno | `warning/background` + ink | `IconHourglass` |
| Recepción en centro (F-04) | Recibido | Recibido en centro | `success/background` | `IconPackageImport` |

### 16.5. Filas atenuadas

Zonas inactivas, repartidores inactivos y despachos resueltos en la ruta se muestran con fondo `cloud-subtle` y texto `text/secondary`. **No se reduce la opacidad** de la fila completa, porque bajaría el contraste del texto por debajo de AA. Las acciones que siguen disponibles en esas filas ("Editar", "Activar") mantienen su color normal.

### 16.6. Niveles de ocupación (F-02 y F-05)

| Nivel | Rango | Color de la barra | Etiqueta | Icono |
|---|---|---|---|---|
| Normal | menos de 70 % | `success/default` | Normal | — |
| Alta | 70 % a 99 % | `warning/default` | Alta | `IconAlertTriangle` heredando `currentColor` de la etiqueta (`text/primary`) |
| Llena | 100 % | `error/default` | Llena | `IconAlertCircle` |

La etiqueta de nivel y el valor `usado / límite (porcentaje)` siempre son visibles, de modo que el color nunca es el único medio de lectura (§4.2). Esto resuelve también el bajo contraste del amarillo como gráfico (§4.5): la barra no es el único portador de la información.

---

## 17. Accesibilidad

Objetivo: **WCAG 2.1 nivel AA** en todo el módulo.

- **Contraste:** solo combinaciones de §4.4. Ninguna combinación nueva sin verificar.
- **Color:** ningún estado depende solo del color (badges con texto e icono, barras con valor y nivel).
- **Teclado:** todo es operable con teclado; orden de tabulación igual al orden visual; anillo de foco signal de 2 px siempre visible (§15.3); la lista reordenable tiene alternativa con botones.
- **Lectores de pantalla:** un único `h1` por página; tablas con `<caption>` visualmente oculta ("Listado de zonas de cobertura"); `aria-label` en todos los `ActionIcon`; regiones `aria-live="polite"` para notificaciones, cambios de orden y la actualización automática del tablero de F-05 (anunciando solo cambios de estado relevantes, no cada refresco).
- **Formularios:** label visible siempre; errores asociados al campo con `aria-describedby` (Mantine lo resuelve con la propiedad `error`); `required` real además del asterisco.
- **Imágenes:** la foto de evidencia lleva `alt` descriptivo ("Evidencia de entrega del despacho DSP-000123"); iconos decorativos con `aria-hidden`.
- **Movimiento:** animaciones de máximo 200 ms; respetar `prefers-reduced-motion` (sin skeleton animado ni icono girando).
- **Táctil (F-03):** áreas de 44 × 44 px mínimo y 8 px de separación entre controles táctiles.
- **Tiempo:** las notificaciones con información necesaria para continuar (vinculación pendiente, notificación a Ventas pendiente) no se cierran solas.

---

## 18. Comportamiento responsive

| Breakpoint (Mantine) | Aplicación administrativa | Web del repartidor |
|---|---|---|
| `base` < 576 px | Barra lateral oculta y accesible con `Burger` (`aria-label="Abrir menú"`) en un `Drawer`; todo en 12 columnas; filtros apilados; tablas con scroll horizontal dentro de `Table.ScrollContainer` | Diseño principal (390 px de referencia) |
| `xs` ≥ 576 px | Igual a `base`; KPI en 2 columnas | Contenido centrado, máximo 480 px |
| `sm` ≥ 768 px | Tableta (F-02): barra lateral colapsada a 72 px, columnas secundarias ocultas, modales a 100 % del ancho menos 32 px | Igual a `xs` |
| `md` ≥ 992 px | Barra lateral colapsada; KPI en 4 columnas | Igual a `xs` |
| `lg` ≥ 1200 px | Barra lateral expandida (256 px); diseño de referencia a partir de 1440 px | Igual a `xs` |
| `xl` ≥ 1408 px | Igual a `lg`; las tablas aprovechan el ancho | Igual a `xs` |

El §6.2 pide mostrar en Figma una versión móvil y una de escritorio de los componentes y patrones cuyo comportamiento cambie de forma relevante: por eso el shell administrativo, la barra de filtros y la tabla (§13.1 y §13.4) se documentan también en móvil. Para las pantallas se entregan, como mínimo, los frames de referencia de los lineamientos: `1440 × 1024` para F-01, F-02, F-04 y F-05, `1024 × 768` adicional para F-02 y `390 × 844` para F-03.

---

> **PARTE III — GUÍAS POR FUNCIONALIDAD**

## 19. Formato de las guías por funcionalidad

Cada funcionalidad de Despacho tiene una guía con la misma estructura, para que diseño y desarrollo encuentren la información en el mismo lugar:

| Bloque | Contenido |
|---|---|
| A. Ficha | Usuario, plataforma, estructura común, frame de referencia, prioridad UX, especificación y carpeta de código |
| B. Tokens y estilos clave | Elemento de la interfaz → color, tipografía, espaciado y radio |
| C. Mapa de pantallas | Pantalla → tipo → ruta → endpoint → archivo |
| D. Pantallas | Layout, tabla de elementos (componente, props, estilo, texto), tabla de estados e interacción |
| E. Componentes de dominio | Componentes propios de Despacho que usa |
| F. Fragmento de referencia | Código que muestra el uso correcto de tokens y componentes |
| G. Criterios de aceptación | Lista verificable para aprobar la funcionalidad |

Convenciones comunes:

- Las rutas son del frontend (`react-router-dom`); los endpoints son los de `integraciones/api-contract.md`.
- Los textos provienen de la especificación de interfaz de cada funcionalidad, ajustados a §10.
- Las pantallas administrativas usan el shell de §13.1 y las del repartidor el de §13.2; aquí solo se describe el área de contenido.
- Los estados genéricos de tabla (carga, vacío, sin resultados, error de red y `403`) siguen §13.4 y solo se repiten cuando tienen un texto propio.
- F-03 agrega un bloque de reglas de la experiencia móvil (§22.B).

---

## 20. Guía F-01 — Gestor de Zonas Geográficas y Cotizador

### 20.A. Ficha

| Campo | Valor |
|---|---|
| Funcionalidad | F-01 Gestor de Zonas Geográficas y Cotizador de Envíos |
| Usuario | Gestor de Despacho (`GESTOR_DESPACHO`) |
| Plataforma y estructura | Escritorio, aplicación administrativa |
| Frame de referencia | 1440 × 1024 px |
| Prioridad UX | Prevención de errores sobre velocidad: cada cambio afecta de inmediato las cotizaciones del Marketplace y el Chatbot. |
| Especificación de interfaz | `disenio/funcionalidades/f-01.md` |
| Carpeta de código | `src/features/zonas/` |
| Nota | La cotización por token de servicio no tiene interfaz; la consumen los canales de venta por API. |

### 20.B. Tokens y estilos clave

| Elemento | Color | Tipografía | Espaciado / radio |
|---|---|---|---|
| Título de página | `text/primary` | `Heading/H1` (Oswald, mayúsculas) | 24 px hasta el siguiente bloque |
| Filtros | Fondo `cloud-subtle` | `Label` | Padding 16 px, `radius/md` |
| Tabla | Fondo blanco, borde `border/default` | `Body/Small`; tarifa con `ia-num` | Filas de 48 px, `radius/md` |
| Distritos en tabla | Badge `neutral` | `Body/Small` | `radius/full` |
| Formulario de zona | `Card` blanca | Secciones con `Heading/H4` | Máximo 720 px, padding 24 px, `radius/md` |
| Panel de tarifas | `Drawer` blanco | Título `Heading/H3` | 560 px, padding 24 px, `radius/lg` |
| Prefijo de moneda | `text/secondary` | `Label` | — |
| Confirmación de desactivación | Botón `error/default` | Título `Heading/H3` | Modal 480 px, `radius/lg` |

### 20.C. Mapa de pantallas

| Pantalla | Tipo | Ruta | Endpoint principal | Archivo |
|---|---|---|---|---|
| P1 Panel de gestión de zonas | Página | `/zonas` | `GET /api/v1/zonas` | `PaginaZonas.tsx` |
| P2 Formulario de zona | Página | `/zonas/nueva`, `/zonas/:idZona/editar` | `POST` / `PUT /api/v1/zonas` | `FormularioZona.tsx` |
| P3 Tarifas de la zona | Panel lateral | `/zonas?tarifas=:idZona` | `GET` / `PUT /api/v1/zonas/{idZona}/tarifa` | `PanelTarifas.tsx` |
| P4 Activar / desactivar zona | Modal | Sobre `/zonas` | `PATCH /api/v1/zonas/{idZona}/estado` | `ModalEstadoZona.tsx` |

### 20.D. Pantallas

#### P1 Panel de gestión de zonas

**Layout:** encabezado de página (§13.3) → barra de filtros → tabla a todo el ancho → paginación.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Título y subtítulo | `Title order={1}` + `Text c="dimmed"` | H1 + `Body` `text/secondary` | "Zonas de cobertura" / "Define dónde entregamos y cuánto cuesta el envío" |
| Acción principal | `Button leftSection={<IconPlus size={20} />}` | `primary`, `md` | "Nueva zona" |
| Búsqueda | `TextInput size="sm" leftSection={<IconSearch size={16} />}` | — | Label "Buscar zona", placeholder "Nombre de la zona" |
| Filtro distrito | `Select size="sm" searchable clearable` | — | "Distrito" |
| Filtro estado | `Select size="sm"` con Todos / Activo / Inactivo | — | "Estado" |
| Limpiar filtros | `Button variant="subtle" size="sm" leftSection={<IconFilterOff />}` | `primary-hover` | "Limpiar filtros" |
| Columna distritos | Hasta 3 `Badge` neutrales + `Badge` "+n" con `Tooltip` | `neutral` | — |
| Columna tarifa | `Text className="ia-num" ta="right"` o `BadgeEstado` "Sin tarifa configurada" | `warning` | "PEN 10.00" |
| Columna estado | `BadgeEstado` | Activo `success` / Inactivo `neutral` | — |
| Acciones de fila | `Button variant="subtle" size="sm"`: "Editar", "Tarifas"; "Desactivar" con `color="red"` o "Activar" | — | — |

| Estado | Presentación |
|---|---|
| Vacío | `EstadoVacio` con `IconMapPin`: "Aún no hay zonas de cobertura registradas" + "Nueva zona" |
| Zona activa sin tarifa | Badge `warning` "Sin tarifa configurada" en la columna de tarifa |
| Zona inactiva | Fila atenuada (§16.5) con "Editar" y "Activar" |
| `403` | `AccesoDenegado`: "No tienes permisos para ver la configuración de zonas" |
| Éxito | Notificación verde: "Zona registrada correctamente", "Zona desactivada", etc. |

**Interacción:** "Desactivar" nunca ejecuta: abre P4. Los filtros se reflejan en la URL.

#### P2 Formulario de zona

**Layout:** `Breadcrumbs` → `Card` de máximo 720 px centrada con tres secciones → barra de acciones fija (§13.9).

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Ruta de navegación | `Breadcrumbs` | `Body/Small` | "Zonas de cobertura / Nueva zona" o "/ Editar [nombre]" |
| Sección identificación | `Title order={4}` + `TextInput required maxLength={100}` | H4 | "Nombre de la zona" |
| Distritos | `MultiSelect searchable clearable hidePickedOptions limit={50}` | Pills `radius/full` | "Distritos" |
| Códigos postales | `TagsInput` con `description` | — | "Códigos postales (opcional)" / "Escribe un código y presiona Enter" |
| Estado inicial | `SegmentedControl data={['Activo','Inactivo']}` | Indicador `primary` | "Estado inicial" |
| Resumen de cobertura | `Alert color="blue" variant="light" icon={<IconInfoCircle />}` | `info` | "3 distritos y 2 códigos postales seleccionados" |
| Acciones | `Button variant="outline"` + `Button loading={guardando}` | — | "Cancelar" / "Guardar zona" |

| Estado | Presentación |
|---|---|
| Validación | Error bajo el campo: "Ingresa el nombre de la zona", "Selecciona al menos un distrito o código postal" |
| Guardando | "Guardar zona" con `loading`; campos con `disabled` |
| Duplicidad `409` | `Alert` amarillo arriba del formulario: "El distrito San Isidro ya pertenece a la zona activa Lima Centro" |
| Error de red | `Alert` rojo con "Reintentar"; datos conservados |
| Cancelar con cambios | Modal "¿Descartar los cambios?" con "Seguir editando" (`outline`) y "Descartar" (`primary`) |
| Éxito | Regreso a P1 con notificación "Zona registrada correctamente" y enlace `subtle` "Configurar tarifas" |

**Interacción:** "Guardar zona" deshabilitado sin nombre o sin cobertura, con el motivo visible bajo el botón.

#### P3 Tarifas de la zona

**Layout:** `Drawer` derecho de 560 px: encabezado fijo → cuerpo desplazable con cuatro secciones separadas por `Divider` → pie fijo.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Encabezado | `Title order={3}` + `BadgeEstado` + cierre | H3 | "Tarifas de Lima Norte" |
| Tarifa base | `NumberInput leftSection="PEN" decimalScale={2} fixedDecimalScale min={0} allowNegative={false} required` | — | "Tarifa base" |
| Peso incluido | `NumberInput rightSection="kg" min={0}` | — | "Peso incluido hasta" |
| Recargo por kg | `NumberInput leftSection="PEN"` | — | "Recargo por kg adicional" |
| Rangos de peso | `Table` con `NumberInput size="sm"` y `ActionIcon` `IconTrash` (`aria-label="Eliminar rango"`) | Fila inválida en `error/background` | Columnas "Desde (kg)", "Hasta (kg)", "Recargo (PEN)" |
| Agregar rango | `Button variant="subtle" leftSection={<IconPlus />}` | — | "Agregar rango" |
| Factor volumétrico | `NumberInput` con `description` | — | "Factor volumétrico" |
| Plazo estimado | `TextInput` | — | "Plazo estimado de entrega" |
| Aviso | `Alert color="blue" variant="light"` | `info` | "La regla se aplicará a las cotizaciones siguientes para esta zona" |
| Pie | "Cancelar" (`outline`) + "Guardar tarifa" (`primary`) | — | — |

| Estado | Presentación |
|---|---|
| Sin tarifa | `Alert` amarillo "Esta zona aún no tiene tarifa"; campos vacíos |
| Tarifa vigente | Campos precargados |
| Validación `400` | Errores por campo: "La tarifa no puede ser negativa", "El valor Desde debe ser menor que Hasta", "Los rangos no pueden superponerse" |
| Éxito | Panel cerrado, tabla actualizada, notificación "Tarifa guardada" |

#### P4 Activar / desactivar zona

Patrón §13.7. Desactivar: icono `IconAlertTriangle`, botón `destructive` "Desactivar zona", foco inicial en "Cancelar". Activar: icono `IconInfoCircle`, botón `primary` "Activar zona". El `409` por solapamiento se muestra como `Alert` amarillo dentro del modal con la zona en conflicto.

### 20.E. Componentes de dominio

`BadgeEstado` (zona y tarifa), `EstadoVacio`, `EstadoError`, `AccesoDenegado`, `BarraAccionesFija`, `CampoMoneda` (envoltorio de `NumberInput` con prefijo "PEN" y dos decimales).

### 20.F. Fragmento de referencia

```tsx
<Drawer opened={abierto} onClose={cerrar} position="right" size={560}
  title={<Group gap="sm"><Title order={3}>Tarifas de {zona.nombre}</Title><BadgeEstado valor={zona.estado} /></Group>}>
  <Stack gap="lg">
    <Stack gap="md">
      <Title order={4}>Tarifa base</Title>
      <CampoMoneda label="Tarifa base" required {...form.register('tarifaBase')} />
      <NumberInput label="Peso incluido hasta" rightSection="kg" min={0} allowNegative={false} />
    </Stack>
    <Alert color="blue" variant="light" icon={<IconInfoCircle size={20} />}>
      La regla se aplicará a las cotizaciones siguientes para esta zona
    </Alert>
  </Stack>
  <BarraAccionesFija>
    <Button variant="outline" onClick={cerrar}>Cancelar</Button>
    <Button loading={guardando} disabled={!esValido}>Guardar tarifa</Button>
  </BarraAccionesFija>
</Drawer>
```

### 20.G. Criterios de aceptación de diseño

- [ ] Una sola acción `primary` en P1 ("Nueva zona"); acciones de fila en `subtle`.
- [ ] "Desactivar" siempre abre el modal destructivo; el foco inicial está en "Cancelar".
- [ ] Ningún campo numérico acepta negativos; los montos muestran "PEN" y dos decimales.
- [ ] El `409` de duplicidad nombra la zona y el distrito o código en conflicto.
- [ ] Las zonas inactivas son legibles (sin opacidad) y conservan "Editar" y "Activar".
- [ ] Los datos del formulario se conservan ante un error de red.

---

## 21. Guía F-02 — Programación y Asignación de Despachos

### 21.A. Ficha

| Campo | Valor |
|---|---|
| Funcionalidad | F-02 Programación y Asignación de Despachos |
| Usuario | Gestor de Despacho (`GESTOR_DESPACHO`) |
| Plataforma y estructura | Escritorio con adaptación a tableta, aplicación administrativa |
| Frame de referencia | 1440 × 1024 px y 1024 × 768 px |
| Prioridad UX | Lectura de un vistazo y asignación en pocos clics, con alto volumen y presión de tiempo. |
| Especificación de interfaz | `disenio/funcionalidades/f-02.md` |
| Carpeta de código | `src/features/programacion/` |
| Nota | La recepción de solicitudes y la cancelación llegan de Ventas por API; solo se reflejan en la cola y en las rutas. |

### 21.B. Tokens y estilos clave

| Elemento | Color | Tipografía | Espaciado / radio |
|---|---|---|---|
| Pestañas | Indicador `action/primary` | `Label` | Debajo del encabezado, 24 px |
| KPI | Fondo blanco; icono semántico | Valor `Heading/H2` `ia-num` | Grilla de 3 columnas con gutters §6.2, `radius/md` |
| Código de rastreo | `text/primary` | Inter 500 `Body/Small` `ia-num` | Sin elipsis |
| Etiquetas especiales | Según §16.2 | `Body/Small` | `radius/full` |
| Tarjeta de repartidor (modal) | Blanca; seleccionada `primary-soft` con borde 2 px `action/primary`; excedida con borde `error/default` | Nombre `Subtitle` | Padding 16 px, `radius/sm` |
| Barras de ocupación | Según §16.6 | `Body/Small` y `Auxiliary` | 8 px de alto, `radius/xs` |
| Barra de cambios sin guardar | `warning/background` | `Body` | Padding 16 px, `radius/md` |

### 21.C. Mapa de pantallas

| Pantalla | Tipo | Ruta | Endpoint principal | Archivo |
|---|---|---|---|---|
| P1 Cola de pendientes | Página (pestaña 1) | `/programacion` | `GET /api/v1/despachos/pendientes`, `POST /api/v1/despachos/simulaciones` | `PaginaProgramacion.tsx`, `TablaCola.tsx` |
| P2 Modal de asignación | Modal 880 px | Sobre `/programacion` | `GET /api/v1/repartidores/disponibles`, `POST /api/v1/despachos/{id}/asignacion` | `ModalAsignacion.tsx` |
| P3 Rutas por repartidor | Página (pestaña 2) | `/programacion/rutas/:idJornada?` | `GET /api/v1/jornadas/{id}/ruta`, `PUT /api/v1/jornadas/{id}/secuencia` | `RutasRepartidor.tsx` |
| P4 Modal de reasignación | Modal 880 px | Sobre `/programacion/rutas` | `POST /api/v1/despachos/{id}/reasignacion` | `ModalReasignacion.tsx` |

### 21.D. Pantallas

#### P1 Cola de pendientes

**Layout:** encabezado con `Tabs` → `SimpleGrid` de 3 KPI → filtros → tabla ordenada por fecha programada ascendente → paginación.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Título | `Title order={1}` | H1 | "Programación y asignación" |
| Acción secundaria | `Button variant="outline" leftSection={<IconFlask />}` | `outline` | "Generar pedido de prueba" |
| Pestañas | `Tabs` con `Tabs.Tab` | — | "Cola de pendientes", "Rutas por repartidor" |
| KPI | `TarjetaKpi` (clic filtra la tabla) | Iconos: `IconCalendarTime` neutral, `IconCalendarEvent` info, `IconRepeat` warning | "Pendientes para hoy", "Programados a futuro", "Reintentos" |
| Filtros | `DatePickerInput type="range" size="sm"`, `Select size="sm"` zona, `Chip.Group` intento | — | "Fecha programada", "Zona", "Todos / Primer intento / Reintentos" |
| Columnas | Código, pedido, zona, dirección (`lineClamp={1}`), peso, volumen, fecha, intento, tiempo en espera, acción | Numéricas a la derecha con `ia-num` | — |
| Etiquetas de fila | `BadgeEstado` "Simulado", "Programado para [fecha]", "Reintento", "Nuevo" | §16.2 | — |
| Espera elevada | `IconClockExclamation` en `text/primary` (§4.5) dentro de `Tooltip` | `aria-label="Tiempo de espera elevado"` | — |
| Acción de fila | `Button variant="outline" size="sm"` | `outline` | "Asignar" |

| Estado | Presentación |
|---|---|
| Vacío | `EstadoVacio` `IconCalendarTime`: "No hay despachos pendientes de asignación" + "Generar pedido de prueba" |
| Programado a futuro | "Asignar" deshabilitado y, debajo, `Auxiliary` "Disponible desde 08/10/2026" |
| Pedido de prueba generado | Notificación "Pedido de prueba generado: DSP-000245"; fila con badge "Nuevo" durante 5 s |
| Asignación exitosa | Notificación "Despacho DSP-000123 asignado a Juan Pérez"; la fila sale de la cola |
| Tableta | Se ocultan "Pedido", "Volumen" y "Tiempo en espera"; quedan accesibles desde el modal |

#### P2 Modal de asignación

**Layout:** franja de resumen (`cloud-subtle`, `SimpleGrid cols={4}`) → buscador → dos grupos de repartidores (`ScrollArea` con altura máxima 480 px) → pie con acciones.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Título | `Modal title` | H3 | "Asignar despacho DSP-000123" |
| Resumen | Pares `Label` + valor | `Label` + `Body/Small` `ia-num` | Código, pedido, zona, dirección, peso, volumen, fecha, intento |
| Buscador | `TextInput leftSection={<IconSearch />}` | — | "Buscar repartidor" |
| Grupos | `Title order={4}` | H4 | "En la zona Lima Centro" / "Otras zonas" |
| Repartidor | `Radio.Card` con nombre, placa, zona, `BadgeEstado`, despachos en ruta y 3 `BarraOcupacion variante="completa" proyeccion={...}` | Seleccionado `primary-soft` + borde `action/primary` | — |
| Alerta de capacidad | `Alert color="red" variant="light" icon={<IconAlertCircle />}` dentro de la tarjeta | `error` | "Capacidad de carga del repartidor excedida: peso" |
| Acciones | "Cancelar" (`outline`), "Confirmar asignación" (`primary`, `loading`) | — | — |

| Estado | Presentación |
|---|---|
| Carga | 3 `Skeleton` con la forma de la tarjeta |
| Sin repartidores | `EstadoVacio`: "No hay repartidores disponibles en este momento" + enlace "Ir a Monitoreo de flota" |
| Capacidad excedida | Tarjeta con borde `error/default`, alerta y botón principal deshabilitado con motivo visible |
| `422` | `Alert` rojo arriba del pie con el límite excedido; el despacho sigue en la cola |
| `409` | `Alert` amarillo "El despacho ya fue procesado" o "El repartidor ya no está habilitado" + "Actualizar cola" (`outline`) |

**Accesibilidad:** el grupo de repartidores es un `Radio.Group` con label "Repartidor"; cada barra expone su valor con `aria-label` (§13.6).

#### P3 Rutas por repartidor

**Layout:** `Grid` con `Grid.Col span={{ base: 12, lg: 4 }}` (lista de repartidores) y `span={{ base: 12, lg: 8 }}` (ruta). En tableta, la lista se reemplaza por un `Select` "Repartidor" sobre la ruta.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Lista de repartidores | `UnstyledButton` por repartidor con nombre, placa, zona, `BadgeEstado`, n.º de despachos y `BarraOcupacion variante="compacta"` | Activo con `primary-soft` | — |
| Encabezado de ruta | Nombre (`Subtitle`), vehículo y zona + 3 barras completas | — | — |
| Lista ordenable | Patrón §13.11 | Posición `Subtitle` `ia-num` | — |
| Acciones de fila | `ActionIcon` subir y bajar (`aria-label`), `Button variant="subtle"` | — | "Reasignar" |
| Cambios sin guardar | Barra `warning/background` con "Descartar" (`subtle`) y "Guardar orden" (`primary`) | — | "Tienes cambios sin guardar en el orden" |

| Estado | Presentación |
|---|---|
| Sin repartidores en jornada | `EstadoVacio`: "No hay repartidores en turno hoy" |
| Repartidor sin despachos | `EstadoVacio`: "Este repartidor aún no tiene despachos asignados" |
| Guardado | Notificación "Orden de ruta actualizado" |
| `409` al guardar | `Alert` amarillo "Un despacho cambió de estado mientras ordenabas. Se actualizó la ruta." y recarga |

#### P4 Modal de reasignación

Igual que P2, excluyendo al repartidor actual, con "Repartidor actual: [nombre]" en el resumen, `Textarea required` "Motivo de la reasignación" y `Alert` azul "El despacho se ubicará al final de la ruta del nuevo repartidor". Acción principal "Confirmar reasignación", deshabilitada sin destino, sin motivo o con capacidad excedida. `409`: "El despacho ya inició su traslado y no puede reasignarse".

### 21.E. Componentes de dominio

`BadgeEstado`, `TarjetaKpi`, `BarraOcupacion` (completa, compacta y con proyección), `TarjetaRepartidor` (compartida por P2 y P4), `ListaRutaOrdenable`.

### 21.F. Fragmento de referencia

```tsx
<Radio.Group value={idSeleccionado} onChange={setIdSeleccionado} label="Repartidor">
  <Stack gap="sm">
    {repartidores.map((r) => {
      const excede = superaCapacidad(r, despacho);
      return (
        <Radio.Card key={r.id} value={r.id} radius="sm" p="md"
          className={excede ? classes.excedida : undefined}>
          <Group justify="space-between">
            <Text fw={600} size="lg">{r.nombre}</Text>
            <BadgeEstado valor={r.estadoOperativo} />
          </Group>
          <Text size="sm" c="dimmed">{r.placa} · {r.zona} · {r.despachosEnRuta} despachos en ruta</Text>
          <Stack gap="xs" mt="sm">
            <BarraOcupacion metrica="peso" usado={r.pesoUsado} limite={r.pesoLimite} proyeccion={despacho.peso} />
            <BarraOcupacion metrica="volumen" usado={r.volumenUsado} limite={r.volumenLimite} proyeccion={despacho.volumen} />
            <BarraOcupacion metrica="paquetes" usado={r.paquetes} limite={r.paquetesLimite} proyeccion={1} />
          </Stack>
        </Radio.Card>
      );
    })}
  </Stack>
</Radio.Group>
```

### 21.G. Criterios de aceptación de diseño

- [ ] La cola no tiene `primary` en el encabezado; "Asignar" es `outline` en cada fila.
- [ ] Los despachos simulados, reintentos y programados a futuro se distinguen por texto e icono, no solo por color.
- [ ] El modal muestra primero los repartidores de la zona del despacho.
- [ ] La proyección de capacidad es visible antes de confirmar y bloquea la confirmación si excede cualquier límite.
- [ ] La ruta puede reordenarse solo con teclado y anuncia la nueva posición.
- [ ] Solo los despachos `ASIGNADO` muestran controles de orden y "Reasignar".
- [ ] En 1024 × 768 px la tabla no tiene scroll horizontal.

---

## 22. Guía F-03 — App Móvil del Repartidor y Evidencia de Entrega

### 22.A. Ficha

| Campo | Valor |
|---|---|
| Funcionalidad | F-03 Web Responsive del Repartidor y Evidencia de Entrega |
| Usuario | Repartidor (`REPARTIDOR` vinculado a un repartidor activo) |
| Plataforma y estructura | Móvil (*mobile-first*), estructura móvil operativa |
| Frame de referencia | 390 × 844 px |
| Prioridad UX | Uso con una mano, de pie, al sol y con prisa. Cero ambigüedad sobre qué hacer después. |
| Especificación de interfaz | `disenio/funcionalidades/f-03.md` |
| Carpeta de código | `src/features/repartidor/` |
| Nota | Sin modo sin conexión, sin GPS ni mapa propio; "Abrir en mapas" delega en una aplicación externa. |

### 22.B. Reglas específicas de la experiencia móvil

| Regla | Valor |
|---|---|
| Tamaño de acciones | `Button size="lg"` (50 px) y `fullWidth`; `ActionIcon size="xl"` (44 px) (§4.5) |
| Inputs | `size="lg"` |
| Texto operativo | Mínimo `Body` 16 px; `Body/Small` 14 px solo para datos secundarios; `Auxiliary` 12 px solo para contadores |
| Ubicación de la acción principal | Barra de acciones fija inferior (§13.9), en la zona del pulgar |
| Acciones principales por pantalla | Una; "Marcar como fallido" siempre `outline` |
| Contraste | Contenido en ink sobre blanco o cloud (≥ 16:1); nada por debajo de `text/secondary` |
| Notificaciones | `position="top-center"` para no tapar la barra inferior |
| Separación entre controles táctiles | Mínimo 8 px (`spacing/sm`) |
| Datos personales | Teléfono y dirección solo en `ASIGNADO` y `EN_CAMINO`; sin copiar ni exportar |

### 22.C. Tokens y estilos clave

| Elemento | Color | Tipografía | Espaciado / radio |
|---|---|---|---|
| Encabezado | Fondo `surface/ink`, texto `text/inverse` | Título `Heading/H3` | 56 px de alto, padding 16 px |
| Badge de estado del repartidor en el encabezado | Variante de §16.3 (fondo claro, texto `text/primary`) | `Body/Small` | `radius/full` |
| Progreso de jornada | `Progress color="orange"` sobre `cloud-subtle` | `Body/Small` | 8 px, `radius/xs` |
| Tarjeta de despacho | Blanca, borde `border/default` | Dirección `Body`; código `Body/Small` `ia-num` | Padding 16 px, gap 16 px, `radius/md` |
| Tarjeta "Siguiente" | `action/primary-soft`, borde 2 px `action/primary` | Igual | Igual |
| Número de posición | Círculo `cloud-subtle` con texto ink | `Subtitle` `ia-num` | 32 px |
| Bloques del detalle | `Card` blanca | Título `Heading/H4` | Padding 16 px, `radius/md` |
| Área de foto | Blanca, borde discontinuo `border/default`; error `error/default` | `Body` | Proporción 4:3, `radius/lg` |
| Navegación inferior | Blanca, borde superior `border/default`; activo `action/primary-hover` | `Label` | 64 px + zona segura |

### 22.D. Mapa de pantallas

| Pantalla | Tipo | Ruta | Endpoint principal | Archivo |
|---|---|---|---|---|
| P1 Acceso | Página | `/repartidor/acceso` | Autenticación de Seguridad y Usuarios | `AccesoRepartidor.tsx` |
| P2 Mi Ruta | Página + navegación inferior | `/repartidor/ruta` | `GET /api/v1/repartidor/mi-ruta` | `MiRuta.tsx` |
| P3 Detalle del despacho | Página + acciones fijas | `/repartidor/despachos/:id` | `GET /api/v1/repartidor/despachos/{id}`, `POST .../inicio-traslado` | `DetalleDespacho.tsx` |
| P4 Entrega con evidencia | Página + acción fija | `/repartidor/despachos/:id/entrega` | `POST /api/v1/repartidor/evidencias/autorizaciones`, `POST .../entrega` | `FormularioEntrega.tsx` |
| P5 Entrega fallida | Página + acción fija | `/repartidor/despachos/:id/fallo` | `GET /api/v1/catalogos/motivos-fallo`, `POST .../fallo` | `FormularioFallo.tsx` |
| P6 Cierre de jornada | Página + hoja inferior | `/repartidor/cierre` | `POST /api/v1/repartidor/jornada/cierre` | `CierreJornada.tsx` |
| P7 Resumen de jornada | Página + navegación inferior | `/repartidor/resumen` | `GET /api/v1/repartidor/jornada/resumen` | `ResumenJornada.tsx` |

### 22.E. Pantallas

#### P1 Acceso

**Layout:** fondo `surface/ink` a pantalla completa con líneas de velocidad (§9, único uso en Despacho) → logo inverso centrado → título → `Card` blanca con el formulario.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Logo | `Image` del logo inverso, `alt="Inka Athletics"` | Versión inversa (§3.4) | — |
| Título | `Title order={2} c="var(--ia-color-text-inverse)"` | H2 Oswald | "Despacho — Repartidor" |
| Usuario | `TextInput size="lg" autoComplete="username"` | — | "Usuario o correo" |
| Contraseña | `PasswordInput size="lg" autoComplete="current-password"` | — | "Contraseña" |
| Acción | `Button size="lg" fullWidth loading` | `primary` | "Ingresar" |

| Estado | Presentación (`Alert` dentro de la tarjeta) |
|---|---|
| Credenciales | Rojo: "Usuario o contraseña incorrectos" |
| `403` | Amarillo: "Tu usuario no está habilitado como repartidor. Comunícate con el Gestor de Despacho." |
| `401` | Azul: "Tu sesión expiró. Ingresa nuevamente." |
| Sin conexión | Rojo con `IconWifiOff`: "Sin conexión a internet. Revisa tu señal e inténtalo de nuevo." |

#### P2 Mi Ruta

**Layout:** encabezado → franja de estado (si aplica) → saludo y progreso → lista de tarjetas → navegación inferior.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Encabezado | `ShellRepartidor titulo="Mi ruta"` + `BadgeEstado` + `ActionIcon size="xl"` `IconRefresh` | ink | `aria-label="Actualizar ruta"` |
| Saludo | `Text size="lg" fw={600}` + fecha | `Subtitle` | "Hola, Juan · Lunes 5 de octubre" |
| Progreso | `Progress value={...} size={8}` + texto | `primary` | "4 de 12 despachos resueltos" |
| Tarjeta de despacho | `TarjetaDespacho` como `UnstyledButton` a ancho completo | §22.C | Posición, código, dirección, destinatario, estado, "Intento 1 de 2" |
| Siguiente | Variante `siguiente` + `BadgeEstado` "Siguiente" | `primary-soft` | — |
| Resueltas | Al final, atenuadas (§16.5) | `cloud-subtle` | — |
| Regularización | `Button variant="subtle" fullWidth` | — | "Pendientes de regularización (2)" |
| Navegación inferior | `NavegacionInferior` | §12.5 | "Mi ruta", "Resumen", "Cerrar jornada" |

| Estado | Presentación |
|---|---|
| Carga | 4 `Skeleton` con la forma de la tarjeta (altura 112 px, `radius/md`) |
| Ruta vacía | `EstadoVacio` `IconRoute`: "No tienes despachos asignados para hoy" |
| Fuera de turno | Franja fija `warning/background`: "Tu turno no está activo. Solo puedes consultar tu ruta." |
| Sin conexión | Franja fija `error/background` con `IconWifiOff`: "Sin conexión" |
| Ruta actualizada | Notificación azul "La ruta se actualizó" |

#### P3 Detalle del despacho

**Layout:** encabezado con flecha de regreso → `Stack gap="md"` de bloques → barra de acciones fija.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Encabezado | `ActionIcon size="xl"` `IconArrowLeft` (`aria-label="Volver a mi ruta"`) + código + `BadgeEstado` | ink | — |
| Destino | `Card` + dirección `Body` + referencia + `Button variant="outline" size="lg" fullWidth leftSection={<IconMap2 />}` | — | "Abrir en mapas" |
| Destinatario | `Card` + nombre + `Button component="a" href="tel:..." variant="outline" size="lg" fullWidth leftSection={<IconPhone />}` | — | "Llamar" |
| Despacho | `Card` con pares etiqueta/valor | `Label` + `Body` | Posición, "Intento 1 de 2", fecha, estado |
| Evidencia (cerrados) | `Card` + `Button variant="subtle" leftSection={<IconPhoto />}` | — | "Ver foto" |
| Acciones en `ASIGNADO` | `Button size="lg" fullWidth loading` | `primary` | "En camino" |
| Acciones en `EN_CAMINO` | `Button variant="outline" size="lg" fullWidth` encima de `Button size="lg" fullWidth` | `outline` + `primary` | "Marcar como fallido" / "Confirmar entrega" |

| Estado | Presentación |
|---|---|
| Iniciando traslado | "En camino" con `loading`; al confirmar, el badge cambia sin recargar la pantalla |
| Cerrado | Solo lectura; sin bloques de destino ni destinatario; bloque "Evidencia" visible |
| `409` | `Alert` amarillo: "Este despacho fue actualizado por el centro de despacho" |
| Cancelado con paquete | `Alert` rojo destacado: "Pedido cancelado. Devuelve el paquete al centro de despacho." |
| Fuera de turno | Acciones deshabilitadas con el motivo visible encima |
| Visor de foto | `Drawer position="bottom"` con `Image`; enlace expirado: "El enlace expiró, vuelve a abrir la foto" |

#### P4 Entrega con evidencia

**Layout:** encabezado "Confirmar entrega" → resumen (código y dirección) → `CapturaEvidencia` (§13.10) → campo opcional → barra de acción fija.

| Elemento | Componente y props | Texto |
|---|---|---|
| Captura | `CapturaEvidencia` con `FileButton accept="image/*" capture="environment"` | "Tomar foto" / "Foto obligatoria del paquete entregado" |
| Recepción | `TextInput size="lg"` | "Nombre de quien recibe (opcional)" |
| Acción | `Button size="lg" fullWidth loading disabled={!foto}` | "Confirmar entrega" |

| Estado | Presentación |
|---|---|
| Sin foto | Botón deshabilitado y mensaje visible: "Debes tomar una foto como evidencia" |
| Procesando | `Loader size="sm"` + "Optimizando imagen…" |
| Enviando | `Progress` con porcentaje; botón bloqueado |
| Error de carga | `Alert` rojo: "No se pudo subir la foto. La entrega no se registró." + "Reintentar"; foto conservada |
| Archivo inválido `400` | `Alert` rojo: "La imagen no es válida. Toma la foto nuevamente." |
| Éxito | Regreso a Mi Ruta y notificación verde "Entrega registrada" |

#### P5 Entrega fallida

| Elemento | Componente y props | Texto |
|---|---|---|
| Motivo | `Radio.Group required` con `Radio.Card` de ancho completo y 56 px de alto mínimo | Seis motivos del catálogo (`GET /catalogos/motivos-fallo`) |
| Foto | `CapturaEvidencia` | "Foto obligatoria del domicilio" |
| Comentario | `Textarea autosize minRows={3} maxLength={250}` + contador | "Comentario (opcional)" |
| Aviso de intento | `Alert color="blue" variant="light"` | "Este intento contará como Intento 1 de 2" |
| Acción | `Button size="lg" fullWidth loading` | "Registrar fallo" |

| Estado | Presentación |
|---|---|
| Sin motivo | El grupo muestra borde y mensaje `error/default`: "Selecciona el motivo" |
| Errores de carga y red | Igual que P4 |
| Éxito | Pantalla de resultado: icono `IconPackageOff` 48 px, `Title order={3}` "Fallo registrado", texto destacado en `Body` 600 "Devuelve el paquete al centro de despacho." y botón `primary` "Volver a mi ruta" |

#### P6 Cierre de jornada

| Elemento | Componente y props | Texto |
|---|---|---|
| Advertencia | `Alert color="yellow" variant="light" icon={<IconAlertTriangle />}` | "3 despachos quedarán como No intentado. No consumen intento y deberás devolver sus paquetes al centro de despacho." |
| Pendientes | Tarjetas compactas con código y dirección | — |
| Acción | `Button size="lg" fullWidth` | "Cerrar jornada" |
| Confirmación | `Drawer position="bottom"` con `Title order={3}`, texto y botones `outline` "Cancelar" y `color="red"` "Sí, cerrar" | "¿Cerrar tu jornada? Esta acción no se puede deshacer." |
| Resultado | Lista "Paquetes a devolver al centro" con `BadgeEstado` y `Button size="lg" fullWidth` | "Ver resumen" |

Estados adicionales: sin pendientes ("No tienes despachos pendientes. Puedes cerrar tu jornada."), error ("La jornada no se cerró" + "Reintentar") y ya cerrada ("Tu jornada ya está cerrada").

#### P7 Resumen de jornada

`SimpleGrid cols={2} spacing={16}` (gutter `base` §6.2) de `TarjetaKpi` (Total asignado, Entregados, Fallidos, No intentados, Pendientes) con borde superior del color del estado (§16.1) y `Accordion` agrupado por estado con código y dirección. Las cifras deben coincidir con Mi Ruta.

### 22.F. Componentes de dominio

`ShellRepartidor`, `NavegacionInferior`, `FranjaEstado` (fuera de turno, sin conexión), `TarjetaDespacho`, `BadgeEstado`, `CapturaEvidencia`, `BarraAccionesFija`, `TarjetaKpi`.

### 22.G. Fragmento de referencia

```tsx
<ShellRepartidor titulo="Confirmar entrega" onVolver={volver}>
  <Stack gap="md" pb={120}>
    <Text size="sm" c="dimmed" className="ia-num">{despacho.codigo}</Text>
    <Text size="md" lineClamp={2}>{despacho.direccion}</Text>
    <CapturaEvidencia foto={foto} onCambiar={setFoto} error={intentoSinFoto}
      texto="Foto obligatoria del paquete entregado" />
    <TextInput size="lg" label="Nombre de quien recibe (opcional)" />
    {errorCarga && (
      <Alert color="red" variant="light" icon={<IconAlertCircle size={20} />}>
        No se pudo subir la foto. La entrega no se registró.
      </Alert>
    )}
  </Stack>
  <BarraAccionesFija movil>
    <Button size="lg" fullWidth loading={enviando} disabled={!foto}>Confirmar entrega</Button>
  </BarraAccionesFija>
</ShellRepartidor>
```

### 22.H. Criterios de aceptación de diseño

- [ ] Todas las áreas táctiles miden al menos 44 × 44 px y las acciones principales 50 px.
- [ ] La acción principal está siempre en la barra inferior; nunca hay dos `primary`.
- [ ] Ninguna acción que cambia el estado admite doble toque (`loading`).
- [ ] La foto se conserva ante cualquier error de carga o de red.
- [ ] Las franjas de fuera de turno y sin conexión son visibles en todas las pantallas afectadas.
- [ ] Teléfono y dirección no aparecen en despachos cerrados.
- [ ] Se verificó la lectura en un teléfono real a pleno sol (prueba de campo).

---

## 23. Guía F-04 — Gestión de Entregas Fallidas

### 23.A. Ficha

| Campo | Valor |
|---|---|
| Funcionalidad | F-04 Gestión de Entregas Fallidas y Reprogramaciones |
| Usuario | Gestor de Despacho (`GESTOR_DESPACHO`) |
| Plataforma y estructura | Escritorio, aplicación administrativa |
| Frame de referencia | 1440 × 1024 px |
| Prioridad UX | Decidir con la evidencia y el historial a la vista; nunca ofrecer una acción que el backend rechazaría. |
| Especificación de interfaz | `disenio/funcionalidades/f-04.md` |
| Carpeta de código | `src/features/entregas-fallidas/` |

### 23.B. Tokens y estilos clave

| Elemento | Color | Tipografía | Espaciado / radio |
|---|---|---|---|
| KPI | Borde superior: `warning/default` (pendientes de retorno), `success/default` (recibidos), `error/default` (atrasados) | Valor `Heading/H2` `ia-num` | 3 columnas, gutters §6.2 |
| Fila "Retorno atrasado" | Fondo `error/background`, borde izquierdo 4 px `error/default` | Repartidor en peso 600 | — |
| Columnas del detalle | Tarjetas blancas | Títulos `Heading/H4` | `Grid` 7 + 5, gap 24 px, `radius/md` |
| Historial | Puntos del `Timeline` con el color del estado (§16.1) | `Body/Small`; fecha en `Auxiliary` | — |
| Panel de decisión | `Card` blanca *sticky* (`top: 24px`) | Ayuda de deshabilitados en `Body/Small` `text/secondary` | Botones apilados, gap 8 px |
| Aviso de pedido anulado | `Alert` rojo | `Body` 600 | Encima del panel |

### 23.C. Mapa de pantallas

| Pantalla | Tipo | Ruta | Endpoint principal | Archivo |
|---|---|---|---|---|
| P1 Listado de entregas fallidas | Página | `/entregas-fallidas` | `GET /api/v1/despachos/fallidos` | `PaginaEntregasFallidas.tsx` |
| P2 Detalle de la incidencia | Página | `/entregas-fallidas/:idDespacho` | `GET /api/v1/despachos/{id}/incidencia`, `POST /api/v1/evidencias/{id}/acceso` | `DetalleIncidencia.tsx` |
| P3 Confirmación de recepción | Modal 480 px | Sobre P1 o P2 | `POST /api/v1/despachos/{id}/recepcion-centro` | `ModalRecepcion.tsx` |
| P4 Reprogramación | Modal 480 px | Sobre P2 | `POST /api/v1/despachos/{id}/reprogramacion` | `ModalReprogramacion.tsx` |
| P5 Cierre como devuelto a origen | Modal 480 px | Sobre P2 | `POST /api/v1/despachos/{id}/devolucion-origen` | `ModalDevolucionOrigen.tsx` |

### 23.D. Pantallas

#### P1 Listado de entregas fallidas

**Layout:** encabezado (sin `primary`) → 3 KPI → filtros → tabla → paginación.

| Elemento | Componente y props | Estilo | Texto |
|---|---|---|---|
| Título | `Title order={1}` | H1 | "Entregas fallidas" |
| KPI | `TarjetaKpi` (clic filtra) | §23.B | "Pendientes de retorno", "Recibidos en centro", "Retornos atrasados" |
| Filtros | `Select size="sm"` motivo, `DatePickerInput type="range" size="sm"`, `Select size="sm"` recepción | — | "Motivo", "Fecha del incidente", "Recepción" |
| Columnas | Código, fecha del incidente, motivo, intento ("1 de 2", `ia-num`), repartidor, recepción (`BadgeEstado`), evidencia (`IconCamera` con `aria-label="Tiene evidencia"` o "—"), etiquetas especiales, acciones | — | — |
| Acciones de fila | `Button variant="outline" size="sm"` (solo pendiente de retorno) + `Button variant="subtle" size="sm"` | — | "Confirmar recepción" / "Ver detalle" |

| Estado | Presentación |
|---|---|
| Vacío | `EstadoVacio` `IconPackageOff`: "No hay entregas fallidas por resolver" |
| Orden por defecto | Filas "Recibido en centro" primero (esperan decisión) |
| Retorno atrasado | Fila destacada (§23.B) con badge "Retorno atrasado" y nombre del repartidor |
| Éxito | Notificación verde tras confirmar recepción o decidir |

#### P2 Detalle de la incidencia

**Layout:** `Breadcrumbs` → encabezado con código (H1), `BadgeEstado` "Fallido" y etiquetas → `Grid` con `Grid.Col span={{ base: 12, lg: 7 }}` (información) y `span={{ base: 12, lg: 5 }}` (evidencia y decisión).

| Elemento | Componente y props | Texto |
|---|---|---|
| Incidencia | `Card` con pares etiqueta/valor | Motivo, comentario, fecha y hora, repartidor, "Intento 1 de 2" |
| Recepción en centro | `Card`; si está pendiente, `BadgeEstado` "Pendiente de retorno"; si no, fecha, usuario, "Sello intacto: Sí/No" y observaciones | — |
| Historial de estados | `Card` + `Timeline bulletSize={20}` | Estado, fecha, ejecutor, observación |
| Evidencia | `Card` + `Image radius="md"` 4:3 clicable → `Modal size="xl"` | `alt="Evidencia de la incidencia del despacho DSP-000123"` |
| Panel de decisión | `Card` *sticky* con tres `Button fullWidth` según §23.D.1 | — |

| Estado | Presentación |
|---|---|
| Evidencia cargando | `Skeleton` 4:3 |
| Sin evidencia | `EstadoVacio` compacto: "No intentado — sin foto" |
| Enlace expirado | `Alert` amarillo + `Button variant="subtle"` "Volver a cargar" |
| No intentado | `Alert` azul: "Este despacho no consumió intento" |
| `409` | `Alert` amarillo: "El despacho cambió de estado. Se actualizó la información." |
| `404` | `EstadoVacio` "No encontramos este despacho" + "Volver al listado" |

##### 23.D.1. Panel de decisión

| Situación | Confirmar recepción | Reprogramar | Cerrar como devuelto a origen |
|---|---|---|---|
| Pendiente de retorno | `primary` | Deshabilitado + "Primero confirma la recepción del paquete" | Deshabilitado + mismo motivo |
| Recibido y reprogramable | Oculto | `primary` | `variant="outline" color="red"` |
| Máximo de intentos | Oculto | Deshabilitado + "Se alcanzó el máximo de intentos (2 de 2)" | `color="red"` (`filled`, pasa a ser la acción principal) |
| Pedido anulado | Oculto | Deshabilitado + "El pedido fue anulado por Ventas y Postventa" | `color="red"` (`filled`) |

El motivo de cada botón deshabilitado se muestra como texto visible debajo del botón y se asocia con `aria-describedby`.

#### P3 Confirmación de recepción

| Elemento | Componente y props | Texto |
|---|---|---|
| Resumen | Franja `cloud-subtle` | Código, repartidor, motivo, fecha del incidente |
| Sello | `Radio.Group required` con "Sí" y "No", sin valor por defecto | "¿El sello del paquete está intacto?" |
| Observaciones | `Textarea autosize`; si sello = "No", `description` "Describe el estado del paquete" y `withAsterisk` | "Observaciones" |
| Nota | `Alert color="blue" variant="light"` | "El despacho seguirá en Fallido; después podrás reprogramarlo o cerrarlo." |
| Acciones | "Cancelar" (`outline`) + "Confirmar recepción" (`primary`, deshabilitado sin sello) | — |

Estados: ya registrada ("La recepción ya fue confirmada", `Alert` azul), error con "Reintentar" y éxito con notificación y fila actualizada a "Recibido en centro".

#### P4 Reprogramación

| Elemento | Componente y props | Texto |
|---|---|---|
| Resumen | Franja `cloud-subtle` | Código, motivo, "Intento 1 de 2" |
| Fecha | `DatePickerInput required minDate={mañana} locale="es" valueFormat="DD/MM/YYYY"` | "Nueva fecha de entrega" |
| Información | `Alert color="blue" variant="light"` | "El despacho volverá a la cola de programación para la fecha elegida. El contador de intentos se mantiene en 1." |
| Acciones | "Cancelar" + "Confirmar reprogramación" | — |

Estados: fecha inválida `400` bajo el selector ("Elige una fecha posterior a hoy"); `422` o `409` como `Alert` en el modal con "Volver al detalle"; éxito con notificación "Despacho reprogramado para 08/10/2026" y regreso a P1.

#### P5 Cierre como devuelto a origen

Patrón §13.7 destructivo: `Alert` amarillo con "El despacho no tendrá más intentos de entrega. El paquete quedará en el centro de despacho y se notificará a Ventas y Postventa.", resumen, `Textarea required` "Motivo del cierre", "Cancelar" y "Cerrar despacho" (`color="red"`). Si la notificación a Ventas queda pendiente: notificación amarilla sin cierre automático "Cierre registrado. La notificación a Ventas y Postventa se reintentará automáticamente."

### 23.E. Componentes de dominio

`BadgeEstado`, `TarjetaKpi`, `PanelDecision`, `HistorialEstados` (envoltorio de `Timeline`), `VisorEvidencia`, `EstadoVacio`.

### 23.F. Fragmento de referencia

```tsx
function AccionDeshabilitada({ motivo, children, ...props }: AccionProps) {
  const id = useId();
  return (
    <Stack gap={4}>
      <Button fullWidth disabled={!!motivo} aria-describedby={motivo ? id : undefined} {...props}>
        {children}
      </Button>
      {motivo && <Text id={id} size="sm" c="dimmed">{motivo}</Text>}
    </Stack>
  );
}

<Card withBorder radius="md" p="md" pos="sticky" top={24}>
  <Title order={4} mb="md">Decisión</Title>
  <Stack gap="sm">
    <AccionDeshabilitada motivo={motivoReprogramar} leftSection={<IconCalendarRepeat size={20} />}>
      Reprogramar
    </AccionDeshabilitada>
    <AccionDeshabilitada motivo={motivoCerrar} color="red" variant={soloCierre ? 'filled' : 'outline'}
      leftSection={<IconArrowBackUp size={20} />}>
      Cerrar como devuelto a origen
    </AccionDeshabilitada>
  </Stack>
</Card>
```

### 23.G. Criterios de aceptación de diseño

- [ ] Ninguna decisión está habilitada antes de confirmar la recepción.
- [ ] Todo botón deshabilitado muestra su motivo como texto visible.
- [ ] Hay una sola acción `filled` en el panel de decisión en cada situación.
- [ ] La evidencia y el historial son visibles sin desplazarse en 1440 × 1024 px.
- [ ] El selector de fecha no permite hoy ni fechas pasadas.
- [ ] Los retornos atrasados se identifican por texto, borde y nombre del repartidor, no solo por color.

---

## 24. Guía F-05 — Monitoreo de Flota y Capacidad

### 24.A. Ficha

| Campo | Valor |
|---|---|
| Funcionalidad | F-05 Monitoreo de Flota y Capacidad |
| Usuario | Gestor de Despacho (`GESTOR_DESPACHO`) |
| Plataforma y estructura | Escritorio, aplicación administrativa |
| Frame de referencia | 1440 × 1024 px |
| Prioridad UX | Supervisión en tiempo real sin perder contexto; configuración sin errores de registro. |
| Especificación de interfaz | `disenio/funcionalidades/f-05.md` |
| Carpeta de código | `src/features/flota/` |
| Nota | La ocupación nunca se edita a mano; se calcula desde los despachos. La API nombra los vehículos como `furgonetas`; la interfaz usa "Vehículos" porque el tipo admite Moto, Auto y Furgoneta. |

### 24.B. Tokens y estilos clave

| Elemento | Color | Tipografía | Espaciado / radio |
|---|---|---|---|
| KPI por estado | Borde superior: `accent/volt` (Disponible), `info/default` (En ruta), `error/default` (Saturado), `border/default` (Fuera de turno) | Valor `Heading/H2` `ia-num` | 4 columnas, gutters §6.2 |
| Indicador de actualización | `text/secondary` | `Auxiliary` | Junto al título |
| Barras de ocupación en tabla | Según §16.6 | `Body/Small` | Columna de 200 px mínimo por métrica |
| Badge de vinculación pendiente | `warning` | `Body/Small` | `radius/full` |
| Formulario de asignación diaria | `Card` blanca | `Label` | `Grid` de 4 columnas, gap 16 px |
| Vista previa de jornada | `Alert` azul | `Body` | — |

### 24.C. Mapa de pantallas

| Pantalla | Tipo | Ruta | Endpoint principal | Archivo |
|---|---|---|---|---|
| P1 Tablero de monitoreo | Página | `/flota` | `GET /api/v1/flota/monitoreo` | `TableroFlota.tsx` |
| P2 Panel de repartidores | Página | `/flota/repartidores` | `GET /api/v1/repartidores`, `PATCH .../estado`, `POST .../vinculacion/reintento` | `PaginaRepartidores.tsx` |
| P3 Formulario de repartidor | Modal 880 px | Sobre P2 | `POST` / `PUT /api/v1/repartidores` | `ModalRepartidor.tsx` |
| P4 Vehículos | Página + modal 880 px | `/flota/vehiculos` | `GET` / `POST` / `PUT /api/v1/furgonetas`, `PATCH .../estado` | `PaginaVehiculos.tsx`, `ModalVehiculo.tsx` |
| P5 Asignación diaria | Página | `/flota/asignacion-diaria` | `POST /api/v1/jornadas`, `POST /api/v1/jornadas/{id}/cierre` | `AsignacionDiaria.tsx` |

### 24.D. Pantallas

#### P1 Tablero de monitoreo

**Layout:** encabezado con título, fecha e indicador de actualización → 4 KPI → filtros → tabla.

| Elemento | Componente y props | Texto |
|---|---|---|
| Título | `Title order={1}` + fecha (`Subtitle`) + `Text size="xs" c="dimmed"` | "Monitoreo de flota" / "Actualizado hace 10 s" |
| Acción | `Button variant="outline" leftSection={<IconCalendarCheck />}` | "Asignación diaria" |
| KPI | `TarjetaKpi` × 4 (clic filtra) | "Disponible", "En ruta", "Saturado", "Fuera de turno" |
| Filtros | `Select size="sm"` estado operativo y zona; `TextInput size="sm"` placa | — |
| Tabla | Repartidor, vehículo, zona, `BadgeEstado`, 3 columnas `BarraOcupacion variante="completa"` | "50 / 50 paq. (100 %)" |

| Estado | Presentación |
|---|---|
| Saturado por un límite | `BadgeEstado` "Saturado"; la barra en 100 % con nivel "Llena" en peso 600 |
| Sin jornadas | `EstadoVacio` `IconCalendarCheck`: "No hay repartidores en jornada hoy" + "Ir a Asignación diaria" |
| Error de actualización | Franja `warning/background` sobre la tabla: "No se pudo actualizar la información"; los datos anteriores se mantienen |

**Actualización automática:** consulta periódica sin recargar la página; no reordena filas ni mueve el scroll mientras el usuario interactúa; el icono de actualización solo gira si no está activo `prefers-reduced-motion`; solo los cambios de estado operativo se anuncian por `aria-live`.

#### P2 Panel de repartidores

| Elemento | Componente y props | Texto |
|---|---|---|
| Título y acción | `Title order={1}` + `Button leftSection={<IconPlus />}` | "Repartidores" / "Nuevo repartidor" |
| Filtros | Registro, estado operativo, turno, vinculación (`Select size="sm"`) y búsqueda | "Buscar por nombre o DNI" |
| Columnas | Nombre, DNI (`ia-num`), teléfono, brevete, turno, registro, estado operativo, vinculación, acciones | — |
| Vinculación pendiente | `BadgeEstado` + `Button variant="subtle" size="sm" loading` | "Vinculación pendiente · No puede recibir jornada" / "Reintentar vinculación" |
| Acciones | "Editar" (`subtle`), "Dar de baja" (`subtle` rojo) | — |

Estados: vacío ("Aún no hay repartidores registrados" + "Nuevo repartidor"), inactivos atenuados sin "Dar de baja", reintento exitoso (notificación verde) o fallido (notificación amarilla). "Dar de baja" abre el modal destructivo (§13.7) "¿Dar de baja a [nombre]?" con "El historial se conserva y no podrá recibir nuevas asignaciones."; el `409` por despachos en curso aparece como `Alert` amarillo en el modal.

#### P3 Formulario de repartidor

`Modal size={880}` con `SimpleGrid cols={2}`: sección "Datos personales" (nombres, apellidos, DNI, teléfono, correo) y "Datos operativos" (brevete, turno habitual). DNI de solo lectura en edición. `Alert` azul "Al registrar, se creará el usuario del repartidor en Seguridad y Usuarios." Errores: "Ingresa un DNI de 8 dígitos", "Ingresa un correo electrónico válido", DNI duplicado bajo el campo. Éxitos: "Repartidor registrado y vinculado" (verde) o "Repartidor registrado. La vinculación quedó pendiente; podrás reintentarla desde el listado." (amarilla, sin cierre automático).

#### P4 Vehículos

| Elemento | Componente y props | Texto |
|---|---|---|
| Título y acción | `Title order={1}` + `Button leftSection={<IconPlus />}` | "Vehículos" / "Nuevo vehículo" |
| Filtros | Tipo, estado, placa | — |
| Columnas | Placa, tipo, peso (kg), volumen (m³), máx. paquetes (todas `ia-num`, a la derecha), estado, repartidor en jornada, acciones | — |
| Acciones | "Editar" (`subtle`), "Enviar a mantenimiento" / "Habilitar" (`subtle`) | — |
| Formulario | `Modal size={880}`: `Select` tipo, `TextInput` placa, `Select` estado, `NumberInput` × 3 con unidad y `min` > 0 | "Límite de peso", "Límite de volumen", "Máximo de paquetes" |
| Mantenimiento | Modal de confirmación con botón `primary` (acción reversible) | "El vehículo quedará excluido de nuevas jornadas. Si está en una jornada sin despachos en curso, esta se cerrará." |

Estados: placa duplicada bajo el campo; límites ≤ 0 ("Ingresa un valor mayor que 0"); rechazo `409` de mantenimiento como `Alert` amarillo: "El repartidor tiene despachos en curso. Deben reasignarse o cerrarse primero."

#### P5 Asignación diaria

**Layout:** `Card` con el formulario en una fila (`Grid` de 4 columnas) → vista previa → tabla "Jornadas de hoy".

| Elemento | Componente y props | Texto |
|---|---|---|
| Fecha | `TextInput readOnly` | "Fecha de la jornada" |
| Repartidor | `Select searchable` (solo activos, vinculados y sin jornada) | "Repartidor" |
| Vehículo | `Select` con `renderOption` que muestra placa y límites | "Vehículo" |
| Zona | `Select` (solo zonas activas de F-01) | "Zona" |
| Vista previa | `Alert color="blue" variant="light"`, visible con los tres campos | "Juan Pérez quedará Disponible con 500 kg, 4.0 m³ y 80 paquetes en Lima Centro" |
| Acción | `Button loading`, habilitado con los tres campos | "Abrir jornada" |
| Tabla de jornadas | Repartidor, vehículo, zona, hora de inicio, `BadgeEstado`, despachos en curso, acción | — |
| Cerrar turno | `Button variant="subtle" color="red" size="sm"`; deshabilitado con motivo si hay despachos en curso | "Cerrar turno" |

Estados: selectores sin opciones ("No hay repartidores habilitados sin jornada", "No hay vehículos disponibles"), jornada duplicada `409`, éxito "Jornada abierta", cierre exitoso y cierre rechazado: "El repartidor tiene despachos Asignados o En camino. El cierre con pendientes se realiza desde la web del repartidor."

### 24.E. Componentes de dominio

`TarjetaKpi`, `BarraOcupacion`, `BadgeEstado`, `IndicadorActualizacion`, `EstadoVacio`, `AccionDeshabilitada` (compartido con F-04).

### 24.F. Fragmento de referencia

```tsx
<SimpleGrid cols={{ base: 1, xs: 2, md: 4 }} spacing={{ base: 16, sm: 20, md: 24 }}>
  {(['DISPONIBLE', 'EN_RUTA', 'SATURADO', 'FUERA_DE_TURNO'] as const).map((estado) => (
    <TarjetaKpi
      key={estado}
      etiqueta={ESTADOS_REPARTIDOR[estado].etiqueta}
      icono={ESTADOS_REPARTIDOR[estado].icono}
      valor={resumen[estado]}
      acento={ESTADOS_REPARTIDOR[estado].acento}   // token de §16.3, nunca un HEX
      activo={filtroEstado === estado}
      onClick={() => alternarFiltro(estado)}
    />
  ))}
</SimpleGrid>
```

### 24.G. Criterios de aceptación de diseño

- [ ] Un repartidor saturado por un solo límite muestra "Saturado" y la barra afectada en "Llena".
- [ ] Toda barra muestra `usado / límite (porcentaje)` y la etiqueta de nivel.
- [ ] La actualización automática no borra datos ante un error ni mueve el scroll.
- [ ] La terminología es "Vehículos" en barra lateral, título y botones.
- [ ] Las acciones bloqueadas por despachos en curso explican el motivo antes de intentarlo.
- [ ] "Abrir jornada" solo se habilita con repartidor, vehículo y zona elegidos, y muestra la vista previa.

---

## 25. Lista de revisión para aprobar una pantalla

- [ ] Usa la estructura común que le corresponde (aplicación administrativa o web del repartidor).
- [ ] Tiene una sola acción `primary`; las acciones de fila no son `primary`; las destructivas usan `color="red"` y confirmación.
- [ ] Todos los colores, espacios, radios y estilos tipográficos son tokens de §4 a §7; no hay valores HEX ni medidas sueltas en el código.
- [ ] Ninguna combinación de color está fuera de §4.4 y ninguna prohibida aparece.
- [ ] Los estados del dominio usan `BadgeEstado` configurado con la regla de §16.0.
- [ ] Están diseñados e implementados todos los estados de la especificación: carga, vacío, sin resultados, error, `403` y los `409` / `422` aplicables.
- [ ] Las acciones deshabilitadas explican su motivo con texto visible.
- [ ] Los textos siguen §10, y coinciden con la especificación.
- [ ] El foco es visible en signal y todo se opera con teclado.
- [ ] En vistas móviles: áreas táctiles de 44 px, acciones `lg` en la zona inferior y texto operativo de 16 px como mínimo.
- [ ] Se cumplen los criterios de aceptación de la guía de implementación de la funcionalidad.
- [ ] El frame de Figma y el componente de código tienen nombres y propiedades equivalentes.
- [ ] La evaluación heurística de Nielsen está registrada.