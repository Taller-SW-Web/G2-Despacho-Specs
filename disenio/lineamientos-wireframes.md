# Lineamientos para la creación de wireframes

## 1. Propósito

Este documento establece pautas comunes para que todos los integrantes elaboren las especificaciones de sus funcionalidades y soliciten a una herramienta de inteligencia artificial la generación de wireframes coherentes para el proyecto.

Estos lineamientos corresponden a una etapa temprana de diseño. Su objetivo es validar la estructura, el contenido, la navegación y los flujos de usuario. Los colores, las tipografías y otros detalles visuales definitivos se establecerán posteriormente en el sistema de diseño del proyecto.

## 2. Alcance del wireframe

- Crear wireframes de baja fidelidad.
- Utilizar una presentación neutra, preferentemente en escala de grises.
- Priorizar la distribución, la jerarquía visual, el contenido y la navegación.
- Evitar colores, sombras, imágenes decorativas y acabados propios de un mockup.
- Incluir únicamente componentes que cumplan una función dentro del flujo.
- Mantener consistencia entre pantallas pertenecientes a la misma funcionalidad.

## 3. Información que debe definir cada funcionalidad

Cada integrante debe crear un archivo Markdown a partir de `plantilla-funcionalidad.md` y completar como mínimo:

- Nombre de la funcionalidad.
- Módulo al que pertenece.
- Responsable.
- Rol o tipo de usuario.
- Contexto operativo.
- Plataforma principal: escritorio, tableta o móvil.
- Objetivo general de la funcionalidad.
- Flujo principal del usuario.
- Pantallas necesarias.
- Objetivo de cada pantalla.
- Componentes requeridos en cada pantalla.
- Restricciones y reglas relevantes.
- Estados de la interfaz cuando correspondan.

## 4. Criterios generales de diseño

- Utilizar textos y etiquetas en español.
- Emplear nombres claros, breves y consistentes para pantallas, botones y campos.
- Mantener una jerarquía clara entre títulos, secciones, contenido y acciones.
- Identificar claramente la acción principal y las acciones secundarias.
- No depender únicamente del color para comunicar estados o advertencias.
- Mantener patrones similares para acciones equivalentes entre pantallas.
- Evitar información o controles que no sean necesarios para completar la tarea.
- Indicar cómo se desplaza el usuario de una pantalla a otra.
- Especificar si una pantalla es una vista completa, un modal, un panel lateral u otro tipo de interfaz.

## 5. Estructuras comunes de las pantallas

Para mantener la coherencia entre las funcionalidades, los wireframes deben utilizar una de las dos estructuras descritas a continuación. La estructura depende del usuario y del contexto operativo de la funcionalidad.

### 5.1. Aplicación administrativa de escritorio

Las funcionalidades F-01 Gestor de Zonas Geográficas, F-02 Programación y Asignación de Despachos, F-04 Gestión de Entregas Fallidas y F-05 Monitoreo de Flota y Capacidad deben diseñarse principalmente para una pantalla de escritorio.

Todas sus pantallas deben compartir la siguiente estructura general:

1. **Barra lateral izquierda:** representa la navegación entre los módulos administrativos disponibles para el usuario.
2. **Encabezado superior compacto:** contiene como mínimo el título o contexto de la pantalla y una referencia básica al usuario o sesión activa.
3. **Área principal de contenido:** contiene la información, formularios, tablas, indicadores y acciones específicas de la funcionalidad.

Representación referencial:

```text
┌──────────────────────────────────────────────────────┐
│ Encabezado superior                                  │
├──────────────┬───────────────────────────────────────┤
│ Barra        │                                       │
│ lateral      │        Contenido principal            │
│              │        de la pantalla                 │
│ Navegación   │                                       │
│ general      │                                       │
└──────────────┴───────────────────────────────────────┘
```

La barra lateral y el encabezado son elementos de contexto y no constituyen el objeto principal de cada wireframe. Por ello:

- Deben aparecer de forma sencilla para reservar su espacio y mantener la estructura común.
- No es necesario definir todavía colores, iconos, logotipo, tipografía, medidas exactas ni interacciones avanzadas.
- No es necesario detallar todos los permisos o elementos de navegación de cada rol.
- Se pueden utilizar etiquetas generales o marcadores de posición cuando las opciones definitivas todavía no hayan sido acordadas.
- El esfuerzo de especificación y generación debe concentrarse en el área principal de contenido de cada pantalla.
- El contenido principal sí debe representar con claridad sus componentes, acciones, estados, validaciones y restricciones.

Como tamaño inicial de referencia se recomienda un frame de escritorio de `1440 × 1024 px`. La adaptación a otros anchos podrá definirse posteriormente; no es obligatorio crear una versión móvil de cada pantalla administrativa durante esta etapa, salvo que la entrega lo exija expresamente.

### 5.2. Aplicación móvil del repartidor

La funcionalidad F-03 Web Responsive del Repartidor y Evidencia de Entrega debe diseñarse como una experiencia web `mobile-first`, separada de la navegación administrativa.

Sus pantallas deben utilizar una estructura general compuesta por:

1. **Encabezado móvil compacto:** muestra el nombre o contexto de la vista y, cuando corresponda, una acción de regreso o referencia a la sesión.
2. **Área principal de una sola columna:** contiene la ruta, los detalles del despacho, formularios y acciones operativas.
3. **Navegación inferior sencilla:** puede permitir el acceso a las secciones principales, como `Mi ruta` y `Resumen`, cuando resulte necesaria.

Representación referencial:

```text
┌──────────────────────────┐
│ Encabezado móvil         │
├──────────────────────────┤
│                          │
│ Contenido principal      │
│ en una sola columna      │
│                          │
├──────────────────────────┤
│ Mi ruta       Resumen    │
└──────────────────────────┘
```

En los wireframes móviles se debe:

- Priorizar el uso con una sola mano.
- Utilizar controles táctiles suficientemente grandes.
- Mantener visible y comprensible la acción operativa principal.
- Usar un botón de regreso en los detalles y formularios cuando corresponda.
- Evitar trasladar la barra lateral de la aplicación administrativa al entorno móvil.
- Concentrar el detalle en el contenido y el flujo de trabajo del repartidor.
- Representar los estados de carga, falta de conexión, error, confirmación y ausencia de asignaciones cuando sean aplicables.

Como tamaño inicial de referencia se recomienda un frame móvil de `390 × 844 px`.

### 5.3. Consistencia al generar pantallas con IA

Cada prompt debe indicar expresamente cuál de las dos estructuras utiliza. Aunque las pantallas se generen por separado, todas las que pertenezcan a una misma experiencia deben conservar la posición general de la navegación, el encabezado y el contenido.

Para una pantalla administrativa se puede incluir la instrucción:

> Utilizar la estructura común de la aplicación administrativa: barra lateral izquierda sencilla, encabezado superior compacto y área principal de contenido. Generar un wireframe de escritorio de baja fidelidad. No detallar visualmente la navegación; concentrar el diseño en el contenido específico de la pantalla.

Para una pantalla del repartidor se puede incluir la instrucción:

> Utilizar una estructura web mobile-first: encabezado compacto, contenido de una sola columna, controles táctiles y navegación inferior sencilla cuando corresponda. Generar un wireframe móvil de baja fidelidad y concentrar el diseño en el flujo operativo del repartidor.

## 6. Estados que deben considerarse

Cuando sean aplicables, la especificación de una pantalla debe contemplar:

- Estado inicial o normal.
- Estado de carga.
- Estado sin resultados o sin información.
- Estado de error.
- Validaciones de campos.
- Acciones deshabilitadas.
- Confirmación de una operación exitosa.
- Advertencias antes de acciones importantes o irreversibles.

No es necesario generar una pantalla independiente para todos los estados. Pueden representarse como variantes de la pantalla principal.

## 7. Accesibilidad y usabilidad

- Diseñar controles con etiquetas comprensibles.
- Evitar que el usuario tenga que recordar información de una pantalla anterior.
- Mostrar retroalimentación después de cada acción importante.
- Prevenir errores mediante restricciones y validaciones visibles.
- Permitir cancelar o regresar cuando el flujo lo requiera.
- Mantener un orden lógico de lectura y navegación.
- Considerar un contraste suficiente para la futura etapa de mockups.

## 8. Preparación de los prompts para IA

Cada pantalla descrita en el archivo de la funcionalidad debe poder utilizarse como un prompt independiente. Al solicitar la generación del wireframe, se debe incluir:

1. El tipo de producto y el contexto de la funcionalidad.
2. El rol del usuario.
3. La plataforma y el tamaño de referencia.
4. El objetivo concreto de la pantalla.
5. Los componentes requeridos.
6. Los estados y restricciones específicas.
7. La relación de la pantalla con el resto del flujo.
8. La indicación expresa de generar un wireframe de baja fidelidad.

La IA no debe inventar nuevas reglas de negocio, campos o acciones que no estén definidos en la especificación. Si falta información importante, el responsable debe revisar la funcionalidad antes de generar el wireframe.

## 9. Convenciones de archivos

- Guardar las especificaciones dentro de la carpeta `funcionalidades`.
- Utilizar un archivo Markdown por funcionalidad.
- Nombrar los archivos en minúsculas y separar las palabras con guiones.
- Usar nombres representativos, por ejemplo: `entregas-fallidas.md`.
- Mantener en el Markdown la descripción que se utilizó para generar cada pantalla.
- Registrar los cambios manuales relevantes efectuados después de la generación.

## 10. Revisión del resultado

Antes de aprobar un wireframe, verificar que:

- Cumpla el objetivo de la funcionalidad.
- Represente correctamente el flujo principal.
- Incluya todos los componentes obligatorios.
- Muestre los estados importantes.
- Utilice nombres comprensibles y consistentes.
- Permita identificar con claridad las acciones principales.
- No incorpore decisiones visuales definitivas propias del mockup.

La evaluación heurística de Nielsen se realiza después de generar el wireframe y debe ser completada manualmente por el evaluador indicado.
