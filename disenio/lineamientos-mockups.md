# Lineamientos para la creación de mockups

## 1. Propósito

Este documento establece una guía común para generar en Stitch los mockups de alta fidelidad del módulo de Despacho y Entrega a Domicilio.

Para trabajar en Stitch se deben adjuntar juntos este archivo y la especificación de interfaz de la funcionalidad, ubicada en `disenio/funcionalidades/f-0X.md`. La especificación aporta el contenido, los flujos, las pantallas y los estados; este lineamiento resume las reglas visuales de `SYSTEM-DESIGN.md` necesarias para generar los mockups [cite: 1] [cite: 2].

El objetivo es que las pantallas generadas por distintos integrantes mantengan la misma identidad, jerarquía y estructura, sin tener que copiar todo el sistema de diseño dentro de cada prompt.

## 2. Alcance del mockup

- Generar mockups de alta fidelidad con colores, tipografías, componentes, espaciado e iconografía definidos.
- Representar con claridad el contenido y los estados indicados en la funcionalidad correspondiente.
- Mantener consistencia entre las pantallas administrativas y, por separado, entre las pantallas del repartidor.
- Usar datos de ejemplo realistas en español para mostrar correctamente tablas, formularios, tarjetas y mensajes.
- Conservar las decisiones de estructura validadas en los wireframes cuando estos ya existan.
- No redefinir reglas de negocio, agregar campos, crear acciones ni modificar flujos que no estén documentados.
- No crear una identidad visual alternativa ni introducir colores, tipografías, iconos o componentes ajenos al sistema de diseño.

El mockup debe comunicar una herramienta operativa clara, confiable y eficiente. No necesita verse promocional: la prioridad es facilitar el trabajo del Gestor de Despacho o del repartidor.

## 3. Fuentes que deben usarse

Para generar una pantalla se utilizan estas fuentes:

1. **Archivo común que se adjunta a Stitch:** `disenio/lineamientos-mockups.md`.
2. **Archivo de la funcionalidad que se adjunta a Stitch:** `disenio/funcionalidades/f-0X.md`, con el objetivo, componentes, estados, restricciones y navegación [cite: 2].
3. **Referencia opcional:** wireframe aprobado de la pantalla, si existe, para conservar la distribución y jerarquía ya validadas.
4. **Fuente de consulta del equipo:** `SYSTEM-DESIGN.md`, cuando exista una duda que este lineamiento resumido no resuelva [cite: 1].

Si falta información, no se debe pedir a Stitch que complete la regla de negocio por su cuenta. El responsable debe resolver la omisión en la especificación antes de aprobar el mockup.

No es necesario crear un documento adicional de “alta fidelidad” por cada funcionalidad si solo repite propósito, tipografía, espaciado, estados o layout ya definidos aquí. Una decisión exclusiva de una funcionalidad debe incorporarse en su `f-0X.md`; una regla compartida debe incorporarse en este lineamiento.

### 3.1. Relación con el wireframe

El mockup debe parecerse al wireframe en su arquitectura de información: conserva el orden del contenido, los componentes obligatorios, la jerarquía, la navegación y el flujo que ya fueron validados. No necesita copiarlo píxel por píxel ni conservar su apariencia en escala de grises.

La alta fidelidad aplica la identidad visual, los componentes y los estados definitivos sobre esa estructura. Si hay una diferencia, prevalece `f-0X.md` para el comportamiento funcional y este lineamiento, derivado de `SYSTEM-DESIGN.md`, para la presentación visual.

## 4. Información que debe definir cada pantalla

Para que Stitch pueda generar una pantalla de manera independiente, el archivo `f-0X.md` debe definir como mínimo:

- Funcionalidad y nombre de la pantalla.
- Rol del usuario y contexto operativo.
- Tipo de experiencia: administrativa de escritorio o web móvil del repartidor.
- Tamaño del frame de referencia.
- Objetivo de la pantalla.
- Tipo de interfaz: página completa, modal, panel lateral, formulario o variante de estado.
- Componentes y datos que deben aparecer.
- Acción principal, acciones secundarias y acciones destructivas.
- Estados que se deben representar.
- Restricciones o reglas visibles para el usuario.
- Origen y destino dentro del flujo.

La descripción de estos puntos debe provenir del archivo `f-0X.md`; este lineamiento solo aporta las reglas visuales comunes.

## 5. Criterios visuales generales

### 5.1. Color y superficies

- Fondo principal de las pantallas de trabajo: cloud `#F7F5F0`.
- Barra lateral administrativa, encabezado móvil y acceso del repartidor: ink `#1B1812`.
- Tarjetas, tablas, modales y paneles: fondo blanco con borde suave `#DEE2E6`.
- Acción principal: naranja `#F76707` con texto ink; hover `#C2410C` con texto claro.
- Foco de teclado y elementos nuevos: signal `#4361EE`.
- Volt `#C3E504` se reserva para disponibilidad o acentos aprobados; no se usa como botón.
- Éxito, advertencia, error e información usan los colores semánticos definidos en el sistema de diseño.
- Ningún estado se comunica solo mediante color: debe incluir texto y, cuando corresponda, icono.
- Las líneas de velocidad son decorativas y solo se usan en la pantalla de acceso del repartidor.

### 5.2. Tipografía

- Usar **Oswald 700**, en mayúsculas, únicamente para títulos H1, H2 y H3.
- Usar **Inter** para cuerpo, botones, formularios, tablas, badges, subtítulos y textos auxiliares.
- Referencias principales: H1 `32/40 px`, H2 `28/36 px`, H3 `24/32 px`, H4 `20/28 px`, cuerpo `16/24 px`, texto compacto `14/20 px` y auxiliar `12/16 px`.
- En la experiencia móvil no usar H1; el contenido operativo debe medir al menos `16 px`.
- Los códigos, cifras, montos, pesos, volúmenes y porcentajes deben alinearse y ser fáciles de comparar.

### 5.3. Espaciado, radios e iconos

- Usar la escala de espaciado de `4`, `8`, `16`, `24` y `32 px`.
- Usar radio de `8 px` en controles, `12 px` en tarjetas, `16 px` en modales y radio completo en badges.
- Usar únicamente Tabler Icons: `16 px` en badges o celdas, `20 px` en botones e inputs y `24 px` en navegación.
- Mantener `8 px` entre un icono y su texto.
- Evitar sombras intensas, efectos decorativos innecesarios y valores visuales arbitrarios.

### 5.4. Jerarquía de acciones

- Debe existir una sola acción principal naranja por pantalla, modal o panel.
- Las acciones alternativas usan estilo `outline`; las acciones menores o de fila usan estilo `subtle`.
- Las acciones repetidas en una tabla no deben mostrarse como botones principales.
- Las acciones destructivas usan rojo y requieren confirmación.
- Un botón deshabilitado por una regla de negocio debe mostrar el motivo mediante texto visible.
- Los botones deben empezar con un verbo concreto, por ejemplo: “Guardar zona”, “Confirmar asignación” o “Registrar fallo”.

## 6. Estructuras comunes de pantalla

### 6.1. Aplicación administrativa

Aplica a F-01, F-02, F-04 y F-05.

- Frame principal: `1440 × 1024 px`.
- F-02 debe comprobarse además en tableta de `1024 × 768 px`.
- Barra lateral ink de `256 px`, con logo inverso, nombre del módulo y navegación.
- Encabezado superior cloud de `64 px`, con contexto de la vista y usuario activo.
- Contenido principal sobre cloud, organizado con una grilla de 12 columnas.
- Márgenes de `32 px` en escritorio y separación habitual de `24 px` entre bloques principales.
- Tarjetas, filtros, tablas y formularios se presentan sobre superficies blancas o cloud-subtle según el patrón.

Esqueleto visual de referencia:

```text
┌────────────────┬──────────────────────────────────────────────┐
│ Logo           │ Encabezado superior · contexto · usuario    │
│ Despacho       ├──────────────────────────────────────────────┤
│                │ TÍTULO                         [Acción]       │
│ Navegación     │ Subtítulo                                    │
│ administrativa│                                              │
│                │ [KPI] [KPI] [KPI]                            │
│                │                                              │
│                │ [Filtros]                                    │
│                │                                              │
│                │ [Tabla, formulario o contenido operativo]   │
│                │                                  [Paginación]│
└────────────────┴──────────────────────────────────────────────┘
```

Orden general recomendado:

1. Encabezado de página con título, subtítulo y acción principal.
2. Pestañas, si corresponden.
3. Indicadores o KPI, si corresponden.
4. Barra de filtros.
5. Tabla, formulario o contenido operativo principal.
6. Paginación, retroalimentación o barra de acciones.

En tableta la barra lateral se reduce a `72 px`, los filtros pueden saltar de línea y las tablas ocultan las columnas de menor prioridad.

### 6.2. Web móvil del repartidor

Aplica a F-03.

- Frame principal: `390 × 844 px` y ancho máximo de contenido de `480 px`.
- Encabezado ink de `56 px`.
- Contenido de una sola columna con padding lateral de `16 px`.
- Navegación inferior blanca de `64 px` cuando corresponda.
- En detalles y formularios, reemplazar la navegación inferior por una barra de acciones fija.
- Botones principales de `50 px` de alto y ancho completo.
- Áreas táctiles mínimas de `44 × 44 px`, con al menos `8 px` entre controles.
- Reservar espacio inferior para que la barra fija no cubra contenido.

Esqueleto visual de referencia:

```text
┌──────────────────────────────┐
│ ← TÍTULO            [Estado] │
├──────────────────────────────┤
│                              │
│ Contenido principal          │
│ en una sola columna          │
│                              │
│ [Tarjetas, detalle o campos] │
│                              │
├──────────────────────────────┤
│ [Acción principal fija]      │
│ o navegación inferior        │
└──────────────────────────────┘
```

La experiencia móvil no debe heredar la barra lateral administrativa.

## 7. Patrones y componentes comunes

| Necesidad | Tratamiento esperado |
| :--- | :--- |
| Encabezado de página | Título a la izquierda y única acción principal a la derecha; breadcrumb en pantallas de segundo nivel. |
| KPI | Tarjeta blanca, radio de 12 px, etiqueta, valor destacado e icono; el color semántico es un apoyo, no la única información. |
| Filtros | Contenedor cloud-subtle, padding de 16 px, búsqueda primero, luego selectores y fechas, y “Limpiar filtros” al final. |
| Tabla | Card blanca con borde, encabezado cloud-subtle, filas de al menos 48 px, acciones en la última columna y paginación inferior. |
| Formulario | Labels siempre visibles, ayuda antes del error, unidades visibles y mensajes que expliquen cómo corregir el dato. |
| Modal | Título claro, contenido enfocado y pie con “Cancelar” antes de la acción principal; estándar de 480 px o amplio de 880 px. |
| Panel lateral | Drawer de 560 px, cuerpo desplazable y pie fijo con acciones. |
| Badges | Forma pill, texto e icono coherentes con el estado; nunca mostrar enums como `PENDIENTE_ASIGNACION`. |
| Retroalimentación | Skeleton para carga, alerta dentro del contenedor para errores y notificación breve para operaciones exitosas. |
| Ocupación | Mostrar nombre de métrica, valor usado/límite, porcentaje, nivel y barra; nunca solo la barra de color. |

Se deben reutilizar visualmente los mismos componentes para la misma necesidad en todas las funcionalidades.

## 8. Estados que deben representarse

Cada pantalla debe incluir el estado normal y las variantes que su especificación solicite. Cuando correspondan, considerar:

- Carga con skeleton de la forma del contenido final.
- Vacío sin registros, con explicación y una acción útil.
- Sin resultados por filtros, con opción para limpiarlos.
- Error de red, conservando los datos ingresados y ofreciendo “Reintentar”.
- Acceso denegado, sin mostrar información operativa.
- Validaciones de campos con instrucciones específicas.
- Acciones deshabilitadas con motivo visible.
- Envío en curso para evitar acciones repetidas.
- Confirmación exitosa mediante notificación.
- Advertencias y confirmaciones antes de acciones importantes o irreversibles.
- Conflictos o reglas incumplidas con mensajes comprensibles, sin mostrar códigos HTTP.

No es obligatorio crear un frame separado para cada estado menor. Los estados complejos que cambian el contenido completo sí deben generarse como variantes identificables.

## 9. Accesibilidad, redacción y contenido

- Mantener contraste WCAG 2.1 AA y usar únicamente las combinaciones aprobadas en `SYSTEM-DESIGN.md` [cite: 1].
- Mostrar un único H1 por página y conservar un orden lógico de lectura.
- Representar foco visible signal en controles interactivos.
- Incluir label visible en todos los campos e identificación accesible en acciones solo con icono.
- Escribir en español, con tono directo, cercano y operativo.
- Utilizar siempre el mismo término para el mismo concepto: “Despacho”, “Código de rastreo”, “Repartidor”, “Vehículo”, “Jornada” y “Zona de cobertura”.
- No mostrar nombres de enum, códigos HTTP ni mensajes técnicos al usuario.
- Formatear fechas como `dd/mm/aaaa`, horas en formato de 24 h y unidades con espacio, por ejemplo `320 / 500 kg (64 %)`.
- Usar direcciones completas en el detalle; en tablas, truncarlas a una línea sin ocultar los códigos de rastreo.

## 10. Generación pantalla por pantalla en Stitch

1. Abrir un nuevo chat de Stitch para la funcionalidad.
2. Adjuntar `lineamientos-mockups.md` y el archivo `f-0X.md` correspondiente.
3. Pedir únicamente la primera pantalla en su estado normal.
4. Revisar el resultado antes de solicitar la siguiente pantalla.
5. Pedir las demás pantallas una por una dentro del mismo chat para conservar el shell, la paleta, la tipografía y los componentes.
6. Generar después las variantes relevantes de carga, vacío, error, validación u otros estados descritos.

Prompt inicial recomendado:

```text
Lee los dos archivos adjuntos y úsalos como fuentes obligatorias. Genera únicamente el mockup de alta fidelidad de la Pantalla 1 de la funcionalidad, en su estado normal. Respeta su contenido y flujo, aplica el sistema visual común y no inventes campos, acciones ni reglas. No generes todavía las demás pantallas.
```

Prompt para continuar:

```text
Ahora genera únicamente la Pantalla [número y nombre] descrita en la funcionalidad. Mantén exactamente el mismo shell, sistema visual y componentes de la pantalla anterior. Representa el estado [normal o variante solicitada] y no modifiques las reglas documentadas.
```

Para corregir un resultado, se debe indicar qué cambia y qué se conserva. Ejemplo: “Mantén sin cambios el shell, la paleta, la tipografía y los componentes; corrige únicamente la jerarquía de acciones y agrega el estado vacío descrito”.

## 11. Convenciones para los resultados

- Organizar los mockups por funcionalidad: F-01, F-02, F-03, F-04 y F-05.
- Nombrar cada frame como `F-0X / PX Nombre de pantalla / Estado`.
- Mantener el frame principal a la izquierda y sus variantes de estado a la derecha.
- Registrar la herramienta, fecha, enlace, versión elegida y cambios manuales en el archivo `f-0X.md` correspondiente.
- Si se cambia un texto, componente o comportamiento durante el mockup, actualizar también la especificación para conservar la trazabilidad.

## 12. Revisión del resultado

Antes de aprobar un mockup, verificar que:

- [ ] Corresponde al objetivo, contenido y flujo definidos en `f-0X.md`.
- [ ] Usa la estructura administrativa o móvil que le corresponde.
- [ ] Respeta la paleta, tipografías, espacios, radios e iconos del sistema de diseño.
- [ ] Presenta una sola acción principal y diferencia las acciones secundarias y destructivas.
- [ ] Incluye los estados importantes indicados en la especificación.
- [ ] Los estados utilizan texto e icono además del color.
- [ ] Las acciones deshabilitadas explican su motivo.
- [ ] Los textos están en español, son operativos y usan el vocabulario acordado.
- [ ] Mantiene contraste, foco visible, labels y tamaños táctiles accesibles.
- [ ] No incorpora reglas, campos, pantallas ni elementos decorativos no documentados.
- [ ] Mantiene consistencia con los demás mockups de la funcionalidad.

La evaluación heurística de Nielsen registrada durante la etapa de wireframes continúa siendo una referencia obligatoria para la revisión final [cite: 2].

## Referencias

1. `disenio/SYSTEM-DESIGN.md` — Sistema de diseño UX/UI del módulo de Despacho y Entrega a Domicilio.
2. `disenio/funcionalidades/f-01.md` a `f-05.md` — Especificaciones de interfaz, flujos, pantallas y estados por funcionalidad.
