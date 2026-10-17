# Especificación compartida de componentes React

**Identificador:** ECR-01.

**Estado:** Borrador especificado; pendiente de revisión del equipo e implementación.

**Fecha:** 14/10/2026.

**Revisión del reparto y de la estructura frontend:** 15/10/2026.

**Responsable de referencia:** Max, Frontend y UI/UX; coordinación técnica con Rhamses.

**Aplicaciones consumidoras:** aplicación administrativa y web responsive del repartidor.

**Fuentes locales revisadas:** repositorio de especificaciones, commit `5b59986`; `SYSTEM-DESIGN.md`, versión 1.0 del 02/10/2026.

**Frontend revisado para esta actualización:** `G2-Despacho-Frontend`, commit `d2bc27d`; monorepositorio con dos aplicaciones y paquetes compartidos. Sus archivos de inicio no acreditan la implementación completa de los CR.

Este documento desarrolla la [plantilla compartida](../plantillas/sdd/componentes-react.md). Define el comportamiento reutilizable que necesitan las pantallas antes de generar su código. Los componentes y comprobaciones siguientes están **por implementar**: su descripción no acredita código, pruebas ni evidencia de ejecución.

## 1. Propósito y fuentes

### 1.1. Alcance y lugar en el flujo SDD

Establecer un catálogo común de controles, composición, propiedades, eventos, estados y criterios de aceptación para que cada integrante construya su funcionalidad con las mismas reglas. La apariencia proviene de [SYSTEM-DESIGN.md](./SYSTEM-DESIGN.md), especialmente §§11–18; este documento concreta el contrato de uso en React [cite: 1].

Las diapositivas compartidas en el curso denominan el enfoque **SDD**. Para una especificación con frontend, las entradas son la especificación funcional, su UI, el contrato de API y esta especificación de componentes. A partir de ellas se elabora el plan, se derivan las tareas y se implementa y verifica un incremento por vez. El contrato de API y los componentes, por sí solos, no describen todos los criterios funcionales [cite: 7].

- Este archivo se mantiene una vez en `disenio/`; las especificaciones consumidoras lo enlazan mediante identificadores `CR-NN` y criterios `CCR-NN-XX`.
- Cada `ui.md` decide cómo compone los componentes, qué datos presenta y cuándo habilita las acciones; cada `plan.md` identifica los componentes que necesita implementar o reutilizar antes de su pantalla.
- La organización SDD por carpetas está aprobada y se adopta progresivamente. Cada especificación nueva o migrada contiene `spec.md`, `plan.md`, `tasks.md`, `evidence.md` y, cuando aplica, `ui.md`. Los archivos sueltos existentes se conservan hasta su migración, actualizando enlaces e índice en ese cambio [cite: 5, 7].
- F-05 corresponde al registro de repartidores y furgonetas; F-06, a jornadas, disponibilidad y monitoreo. El diseño visual todavía agrupa ambas áreas en su guía F-05. En este documento los consumidores se identifican según el índice funcional vigente [cite: 1, 5, 6].

### 1.2. Fuentes y responsabilidades

| Fuente | Qué determina | Uso en esta especificación |
|---|---|---|
| [SYSTEM-DESIGN.md](./SYSTEM-DESIGN.md), §§3–18 | Tokens, identidad, controles, estructuras, accesibilidad y responsive | Referencia visual principal; no copiar el tema en cada componente [cite: 1]. |
| [UI F-01](./funcionalidades/f-01.md), [F-02](./funcionalidades/f-02.md), [F-03](./funcionalidades/f-03.md), [F-04](./funcionalidades/f-04.md), [F-05 y F-06](./funcionalidades/f-05.md) | Interacción y contenido de las pantallas existentes | Consumidores actuales, hasta disponer de `ui.md` por especificación [cite: 2]. |
| [Stack frontend](../arquitectura/stack-frontend.md) | Dependencias propuestas anteriormente | Debe conciliarse con el diseño antes de instalar dependencias; ver DC-01 [cite: 3]. |
| [Convenciones e integraciones externas](../integraciones/api-contract.md), [Gestión](../integraciones/api-contract-gestion-despachos.md) y [Operación](../integraciones/api-contract-operacion-reparto.md) | Comunicación, identidad, permisos, operaciones y errores | Fuente única por operación; las propiedades de este archivo son modelos de presentación, no nuevos payloads [cite: 4]. |
| [Índice funcional](../funcionalidades/funcionalidad.md) y [especificaciones atómicas](../especificaciones/) | Comportamientos y criterios funcionales | Trazabilidad de consumidores; no introducir reglas de negocio desde un componente [cite: 5]. |
| [Estados del despacho](../arquitectura/diagrama-estados-despacho.md) y [F-06](../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md) | Transiciones y ocupación | El backend conserva la autoridad sobre disponibilidad, capacidad e intentos [cite: 6]. |

Si dos fuentes discrepan, registrar la diferencia en §5. Usar el sistema de diseño para la apariencia y el contrato correspondiente para la comunicación y autorización; resolver cualquier contradicción funcional en la especificación propietaria antes de implementar el comportamiento afectado.

### 1.3. Reglas transversales y contratos comunes

- Usar React y TypeScript con Mantine, según `SYSTEM-DESIGN.md` §15. No implementar una segunda biblioteca visual con Tailwind. Las versiones e instalación quedan sujetas a DC-01; aquí no se añade un `package.json` [cite: 1, 3].
- Reutilizar directamente los controles Mantine que cubran la necesidad. Los **patrones de configuración** CR-01 y CR-02 y el adaptador CR-15 no obligan a crear un componente envoltorio. Crear componentes propios para composiciones con responsabilidad compartida [cite: 1].
- El tema y los tokens son únicos para ambas aplicaciones: en el frontend actual se encuentran en `packages/componentes-compartidos/src/index.ts` (exportación `tema`) y `packages/componentes-compartidos/src/tokens.css`. Estas ubicaciones adaptan las rutas orientativas `src/theme/` del diseño al monorepositorio existente. Usar Inter en cuerpo y controles; Oswald 700 en títulos H1–H3; colores, espacios, radios e iconos de §§4–8. No ofrecer colores o radios arbitrarios como propiedades de los componentes de dominio.
- Las propiedades controladas reciben su valor del consumidor; los eventos solicitan cambios y el consumidor devuelve el nuevo valor. Los componentes visuales no consultan APIs, leen tokens, deciden permisos, recalculan capacidad de la flota ni confirman transiciones por su cuenta.
- Los contenedores de cada funcionalidad realizan consultas y mutaciones, adaptan DTO a modelos de presentación y actualizan la vista con la respuesta confirmada. Las cifras mostradas o una acción deshabilitada nunca sustituyen la validación del backend [cite: 4, 6].
- Los límites, catálogos, obligatoriedad y fechas permitidas se toman de la especificación y contrato aplicables. Los ejemplos visuales no añaden nuevos campos, reglas ni operaciones al contrato.
- El contenido y mensajes son en español; no mostrar enums, códigos HTTP, trazas ni respuestas técnicas como texto de operación. Formatear fechas para presentación y conservar el formato contractual al enviar; la zona horaria operativa se acuerda en DC-06. `PEN`, `kg`, `m³` y cifras tabulares siguen §5.5 [cite: 1, 4].
- Objetivo de accesibilidad: el definido en `SYSTEM-DESIGN.md` §17. Controles con nombre accesible, teclado, foco visible, mensajes asociados y estados distinguibles con texto e iconos; movimiento reducido y controles táctiles de al menos 44 × 44 px. Los requisitos de esta sección aplican a todos los `CR-NN` [cite: 1].

Tipos de presentación comunes; sus nombres y campos no describen una respuesta HTTP:

```ts
type EstadoConsulta = 'carga' | 'datos' | 'vacio' | 'sinResultados'
  | 'error' | 'sinPermiso' | 'noEncontrado';
type AccionUi = {
  id: string;
  etiqueta: string;
  disabled?: boolean; // Por defecto false.
  loading?: boolean; // Por defecto false.
  motivoDeshabilitado?: string;
};
type DestinoUi = { id: string; etiqueta: string; ruta: string };
type FiltroActivoUi = { id: string; etiqueta: string };
type OrdenUi = { columna: string; direccion: 'asc' | 'desc' } | null;
type PaginacionUi = { pagina: number; tamanioPagina: number; total: number };
```

`pagina` empieza en 1 en la interfaz. La conversión a parámetros y metadatos HTTP pertenece al adaptador de cada listado, una vez acordados en el contrato (DC-04). Las propiedades `children`, acciones y controles compuestos usan `React.ReactNode` donde se indique; los tipos concretos de librería se importarán de la versión acordada.

### 1.4. Adaptación visual común

| Tamaño según el diseño | Comportamiento obligatorio |
|---|---|
| Base, menos de 576 px | Administración con menú en `Drawer`, filtros apilados y tabla con scroll interno; repartidor con 390 px de referencia. |
| `xs`, desde 576 px | KPI en dos columnas; repartidor centrado con máximo 480 px. |
| `sm`, desde 768 px | Administración con barra lateral de 72 px; tabla F-02 con columnas secundarias accesibles desde el detalle; modales ajustados al viewport. |
| `md`, desde 992 px | Barra lateral colapsada; hasta cuatro KPI por fila. |
| `lg`, desde 1200 px | Barra lateral expandida de 256 px; contenido en grilla del diseño. |
| `xl`, desde 1408 px | Ancho máximo de contenido de 1320 px; referencia administrativa de 1440 × 1024. |

Estas son referencias del documento de diseño, no una configuración de dependencias verificada. F-02 también se revisa a 1024 × 768; F-03 a 390 × 844. Ninguna barra fija debe cubrir el último control ni el foco [cite: 1].

### 1.5. Cómo aplicar estilos sin Tailwind

Gerardo aclara que `SYSTEM-DESIGN.md` recoge el acuerdo visual común entre módulos. Se mantiene su base de Mantine sin Tailwind; la actualización pendiente del stack debe reflejar ese acuerdo, sin cambiar la guía común desde este trabajo.

| Recurso | Responsabilidad | Regla de uso |
|---|---|---|
| Tema exportado desde `packages/componentes-compartidos/src/index.ts` y `MantineProvider` de cada aplicación | Paletas, tipografía, espaciados, radios y valores predeterminados de los controles | Completar la base existente según §§15.2 y 15.4 del diseño. Puede separarse el tema en otro archivo del paquete conservando su exportación pública. |
| Props y componentes de composición Mantine | Aplicar variantes, tamaños y distribución con `Button`, `Stack`, `Group`, `Grid` y otros controles | Usar los nombres y tokens acordados; no reconstruir los controles con estilos distintos por integrante. |
| `packages/componentes-compartidos/src/tokens.css` | Variables y reglas globales del sistema de diseño | Completar los tokens existentes y mantener la correspondencia con el tema y con las variables de Figma, según §15.3. |
| Archivos `*.module.css` | Estilos específicos de una composición, estados visuales y responsive que lo requieran | Referenciar variables `--ia-*` o `--mantine-*` apropiadas. Aplicar con `className` o `classNames` según la Styles API; evitar valores arbitrarios. |

Mantine ya aporta estilos a sus controles. El CSS adicional adapta lo necesario usando los tokens del diseño; «sin Tailwind» no significa «sin CSS». Cambiar un token global requiere actualizar sus representaciones de forma coordinada, no sobreescribirlo de manera independiente en cada pantalla [cite: 1].

## 2. Catálogo y dependencias

El estado de **todos** los elementos del catálogo es `Especificado; implementación y evidencia pendientes`.

| ID | Componente o patrón | Propósito | Consumidores principales | Depende de |
|---|---|---|---|---|
| [CR-01](#cr-01-accionesui) | AccionesUi, patrón Mantine | Jerarquía de botones y acciones con icono | Todas las pantallas con acciones | Tema |
| [CR-02](#cr-02-camposformulario) | CamposFormulario, patrón Mantine | Campos, selecciones y validación visible | F-01 a F-06 con formularios o filtros | Tema |
| [CR-03](#cr-03-shelladministrativo) | ShellAdministrativo | Estructura y navegación de gestión | F-01, F-02, F-04, F-05, F-06 | CR-01 |
| [CR-04](#cr-04-shellrepartidor) | ShellRepartidor y NavegacionInferior | Estructura móvil de campo | ES-F03-02 a ES-F03-07 | CR-01, CR-09, CR-13, CR-14 |
| [CR-05](#cr-05-encabezadopagina) | EncabezadoPagina | Título, contexto, ruta y acciones | Administración | CR-01 |
| [CR-06](#cr-06-barrafiltros) | BarraFiltros | Consulta, limpieza y filtros activos | Listados F-01, F-02, F-04, F-05, F-06 | CR-01, CR-02 |
| [CR-07](#cr-07-tabladatos) | TablaDatos | Listados, orden y paginación | Administración | CR-01, CR-08 |
| [CR-08](#cr-08-estadovista) | EstadoVista: EstadoVacio, EstadoError y AccesoDenegado | Carga, ausencia de datos y recuperación | Ambas aplicaciones | CR-01 |
| [CR-09](#cr-09-badgeestado) | BadgeEstado | Representación única de estados | Ambas aplicaciones | Tema, configuración de estados |
| [CR-10](#cr-10-tarjetakpi) | TarjetaKpi | Indicadores y filtros rápidos | F-02, F-03, F-04, F-06 | Tema |
| [CR-11](#cr-11-barraocupacion) | BarraOcupacion | Ocupación y proyección de carga | ES-F02-04 a ES-F02-06; F-06 | Tema |
| [CR-12](#cr-12-modalconfirmacion) | ModalConfirmacion | Confirmar un efecto con contexto | F-01 a F-06, según su UI | CR-01 |
| [CR-13](#cr-13-barraaccionesfija) | BarraAccionesFija | Acciones persistentes sin ocultar contenido | ES-F01-02; ES-F03-03 a ES-F03-07 | CR-01 |
| [CR-14](#cr-14-franjaestado) | FranjaEstado | Conexión, turno o datos desactualizados | F-03 y F-06 | CR-01 |
| [CR-15](#cr-15-notificacionoperacion) | NotificacionOperacion, adaptador | Resultado consistente de operaciones | Ambas aplicaciones | Proveedor de notificaciones Mantine |
| [CR-16](#cr-16-tarjetadespacho) | TarjetaDespacho | Resumen de una entrega navegable | ES-F03-02, ES-F03-03, ES-F03-07 | CR-09 |
| [CR-17](#cr-17-capturaevidencia) | CapturaEvidencia | Captura y previsualización de foto | ES-F03-05, ES-F03-06 | CR-01, CR-08 |
| [CR-18](#cr-18-visorevidencia) | VisorEvidencia | Lectura de una fotografía autorizada | ES-F03-08, ES-F04-02 | CR-01, CR-08 |
| [CR-19](#cr-19-historialestados) | HistorialEstados | Secuencia de cambios de un despacho | ES-F02-05, ES-F04-02 | CR-08, CR-09 |
| [CR-20](#cr-20-tarjetarepartidor) | TarjetaRepartidor | Selección de candidato para asignación | ES-F02-04, ES-F02-06 | CR-02, CR-09, CR-11 |

`PanelDecision`, editor de tarifas, formularios completos, lista de ruta ordenable y acceso del repartidor permanecen en su funcionalidad. Su comportamiento específico se describe en la UI correspondiente; reutilizan este catálogo. Los patrones exclusivos no se convierten en componentes globales solo por aparecer en un diseño [cite: 1, 2].

## 3. Especificación por componente

### CR-01. AccionesUi

- **Propósito y límites:** patrón para `Button` y `ActionIcon`; el consumidor ejecuta la acción y controla su estado. No requiere un envoltorio de Mantine.
- **Diseño:** `SYSTEM-DESIGN.md` §§11.3 y 12.1. Naranja principal con texto ink; hover con texto inverse; secundarias `outline`, terciarias `subtle`, destructivas rojas; volt no se usa en botones [cite: 1].
- **Consumidores:** acciones de todas las UI; los permisos y motivos de bloqueo llegan del contenedor.

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `children` / `aria-label` | Texto o nodo / texto | Sí: nombre accesible | Sin valor | Botón con verbo concreto; icono aislado siempre con `aria-label`. |
| `variant`, `color` | Props Mantine | No | Principal: `filled`, tema primario | Configurar según la jerarquía de §12.1; como máximo una acción principal por contexto. |
| `size`, `fullWidth` | Props Mantine | No | `md`, `false` | Tabla y filtros: `sm`; repartidor: `lg`, acción principal a ancho completo. |
| `disabled`, `loading` | Booleanos | No | `false` | Ambos impiden activar; `loading` conserva la etiqueta. |
| `type` | `button`, `submit`, `reset` | Sí en formularios | Explicitar | Solo la acción de envío usa `submit`; cancelar y limpiar no envían. |
| `aria-describedby` | Identificador de texto | Si hay bloqueo funcional | Sin valor | Enlaza un motivo visible; no depender solo de tooltip. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `onClick` | Evento de clic React | Activación con puntero o teclado, si está habilitado y sin carga. |

- **Estados y composición:** normal, hover, foco, deshabilitado y carga; icono decorativo opcional. El contenedor bloquea sincrónicamente un segundo envío antes de esperar la mutación; el backend aplica su idempotencia contractual.
- **Accesibilidad y responsive:** semántica nativa; Enter/Espacio, foco signal; área de icono de 44 px en móvil. Cancelar precede a la acción principal; en móvil se apilan con la principal abajo.
- **CCR-01-01:** DADO un envío en curso, CUANDO se repite clic o toque, ENTONCES no se solicita otra mutación y se conserva la etiqueta de la acción.
- **CCR-01-02:** DADA una acción bloqueada por una regla, ENTONCES el motivo es visible y está asociado al control; un botón Cancelar dentro del formulario no lo envía.
- **Pruebas previstas:** interacción con ratón y teclado, doble activación con respuesta demorada y comprobación de tipo de botón en formulario.

### CR-02. CamposFormulario

- **Propósito y límites:** configurar controles Mantine con etiquetas y errores consistentes. Usar `TextInput`, `PasswordInput`, `NumberInput`, `Textarea`, `Checkbox`, `Radio.Group`, `Select`, `MultiSelect`, `TagsInput` y `DatePickerInput` directamente. No crear un formulario universal ni deducir validaciones desde la etiqueta.
- **Diseño:** §§11.4–11.6 y 12.2; `Controller` de React Hook Form cuando haga falta adaptar controles; validación de la funcionalidad con Zod según el stack acordado [cite: 1, 3].
- **Consumidores:** formularios y filtros; `selloIntacto` en F-04 es selección Sí/No sin valor inicial, no un checkbox que confunda «No» con «sin respuesta» [cite: 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `id`, `label` | Texto | Sí | Sin valor | Identidad estable y etiqueta visible. |
| `value` / `checked` | Tipo nativo del control | Sí si controlado | Texto `''`; selección vacía según control | `0` y `false` son respuestas válidas, no valores ausentes. |
| `required`, `disabled`, `readOnly` | Booleanos | No | `false` | Aplicar obligatoriedad y atributos reales; lectura no equivale a campo deshabilitado. |
| `description`, `error` | Nodo compatible con Mantine | No | Sin valor | Ayuda previa y error corregible asociado al campo. |
| `size` | `sm`, `md`, `lg` | No | `md` | `lg` en campo operativo móvil; `sm` en filtros de escritorio. |
| `data`, `searchable`, `clearable` | Props de selección Mantine | Según control | Sin datos; `false`; `false` | Buscar con más de 8 opciones; filtros opcionales pueden limpiarse; mostrar «Sin resultados». |
| `min`, `max`, `maxLength`, restricciones de fecha | Props del control | Según regla | Sin restricción añadida | El consumidor aporta las restricciones acordadas; los ejemplos visuales no fijan límites nuevos. |

| Control o configuración | Valor y evento | Regla específica |
|---|---|---|
| Texto, contraseña, teléfono y comentario | `onChange`: evento del input o textarea; consumidor extrae `currentTarget.value` | Mantener texto introducido al fallar; `Textarea` usa contador si hay límite acordado. |
| `NumberInput`; posible composición `CampoMoneda` | `onChange`: número o texto de edición | Permitir estado vacío; validar antes de convertir. Moneda con `PEN`, dos decimales y no negativos donde lo permita la regla; unidades fuera del valor. |
| `Checkbox` | `onChange`: evento; `currentTarget.checked` | `indeterminate` solo para selección parcial; etiqueta activa el control. |
| `Select`, `MultiSelect`, `TagsInput`, `Radio.Group` | `onChange`: valor nativo del control instalado | Unicidad, listas y formato por funcionalidad; `Radio.Group` exige selección explícita cuando corresponda. |
| `DatePickerInput` | `onChange`: valor nativo de la versión acordada | Presentación `DD/MM/YYYY`, español; adaptador convierte a fecha contractual sin confundir fecha con instante UTC. |

- **Estados y composición:** vacío, con valor, foco, deshabilitado, lectura, cargando opciones y error. Cada control conserva su API nativa; el plan define el adaptador de formulario, sin mezclar firmas de `onChange`.
- **Accesibilidad y responsive:** label visible, `required` real, errores con `aria-describedby`; grupos con leyenda. Campos apilados en móvil, opciones dentro del viewport y controles táctiles suficientes.
- **CCR-02-01:** DADO un campo obligatorio inválido, CUANDO se valida, ENTONCES aparece una instrucción asociada al campo; al corregirlo se elimina ese error sin borrar otros valores.
- **CCR-02-02:** DADO el sello sin respuesta, ENTONCES no se permite confirmar; seleccionar «No» produce el valor `false` y se distingue de no haber seleccionado.
- **CCR-02-03:** DADO un importe vacío o cero, ENTONCES el control conserva esa distinción; no transforma automáticamente vacío en `0` ni envía un texto con `PEN`.
- **Pruebas previstas:** interacción por tipo, etiquetas y errores, selección con teclado, valores vacíos/cero/falso y adaptación de fechas.

### CR-03. ShellAdministrativo

- **Propósito y límites:** alojar navegación, usuario y contenido administrativo. Recibe destinos ya autorizados; no decodifica JWT ni concede permisos.
- **Diseño y consumidores:** §§6.4, 12.5, 13.1 y 18; F-01, F-02, F-04, F-05 y F-06 [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `destinos` | `DestinoUi[]` | Sí | Sin valor | Mantener orden: Programación, Monitoreo, Entregas fallidas, Asignación diaria, Repartidores, Vehículos, Zonas y Tarifas, filtrado por acceso. |
| `destinoActivo` | Identificador o `null` | Sí | Sin valor | Destaca el destino correspondiente a la ruta actual. |
| `usuario` | Objeto con `nombre` y `etiquetaPerfil` | Sí | Sin valor | Presentación de identidad confirmada por la capa de sesión. |
| `contexto`, `children` | `ReactNode` | Contenido sí | Contexto ausente | Contexto en encabezado y página en `main`. |
| `logoUrl`, `rutaInicio` | Texto | Sí | Sin valor | Activo autorizado de marca, variante inversa y enlace al inicio. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alNavegar` | `id` y `ruta` del destino | Se activa un destino disponible. |
| `alCerrarSesion` | Ninguno | La persona selecciona Cerrar sesión. |

- **Estados y composición:** destino activo, menú móvil abierto/cerrado y menú de usuario; `AppShell`, `NavLink`, `Menu`, `Drawer` y contenido. El menú móvil se cierra tras navegar.
- **Accesibilidad y responsive:** enlace para saltar al contenido, navegación etiquetada, destino con `aria-current="page"`, logo con texto alternativo. Barra 256 px desde `lg`, 72 px en `sm`/`md`, `Drawer` en anchos menores; foco contenido y devuelto al abrir/cerrar menú móvil.
- **CCR-03-01:** DADA una ruta administrativa, CUANDO cambia, ENTONCES solo su destino queda activo y se conserva un único `main` con el contenido correspondiente.
- **CCR-03-02:** DADO un viewport móvil, CUANDO se abre, recorre y cierra el menú con teclado, ENTONCES todos los destinos disponibles son alcanzables y el foco vuelve al disparador.
- **Pruebas previstas:** navegación con rutas simuladas, menú móvil y comprobación de landmarks y destino activo.

### CR-04. ShellRepartidor

- **Propósito y límites:** estructura móvil compartida; integra `NavegacionInferior` y recibe estado operativo ya resuelto. La pantalla de acceso usa su composición propia antes de disponer de sesión.
- **Diseño y consumidores:** §§6.5, 12.5, 13.2, 18 y 22; ES-F03-02 a ES-F03-07 [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `titulo`, `children` | Texto / `ReactNode` | Sí | Sin valor | Título visible y contenido operativo. |
| `estadoOperativo` | Valor de estado o `null` | Sí | Sin valor | Usa CR-09; `null` evita afirmar un estado aún desconocido. |
| `destinos`, `destinoActivo` | `DestinoUi[]` / identificador o `null` | En modo navegación | Sin valor | Tres destinos: Mi ruta, Resumen y Cerrar jornada. |
| `modoPie` | `navegacion`, `acciones`, `ninguno` | No | `navegacion` | En detalle y formularios sustituir navegación por CR-13; no superponer ambas. |
| `accionesFijas`, `franjas`, `accionEncabezado` | `ReactNode` | No | Ausentes | Slots para CR-13, CR-14 y actualizar/regresar. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alNavegar` | Destino seleccionado | Se activa una entrada de NavegacionInferior. |
| `alVolver` | Ninguno | Se pulsa el regreso, si la pantalla lo ofrece. |

- **Estados y composición:** navegación activa, detalle con acciones, avisos globales y estado operativo. Encabezado ink de 56 px; pie de 64 px más zona segura; ancho máximo 480 px.
- **Accesibilidad y responsive:** el título de la vista es el único `h1`, aunque use el estilo visual H3; navegación identificada y `aria-current`; no reducir texto operativo por debajo de 16 px. Reservar alturas del encabezado, franjas y pie.
- **CCR-04-01:** DADO el paso de Mi ruta a un formulario, ENTONCES la navegación inferior se sustituye por las acciones y el último campo queda visible al desplazarse, incluso con zona segura.
- **CCR-04-02:** DADO un cambio de destino, ENTONCES la vista y el destino activo coinciden, sin crear una barra lateral en móvil ni en escritorio.
- **Pruebas previstas:** navegación, lectura del título, viewport 390 × 844, aparición conjunta de avisos y barra fija.

### CR-05. EncabezadoPagina

- **Propósito y límites:** presentar título, contexto y acciones; no construir rutas ni decidir qué acción está habilitada.
- **Diseño y consumidores:** §13.3, administración de F-01, F-02, F-04, F-05 y F-06 [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `titulo` | Texto | Sí | Sin valor | Único H1 de la página administrativa. |
| `subtitulo` | Texto | No | Ausente | Contexto con tipografía de cuerpo. |
| `migas` | `DestinoUi[]` | No | `[]` | Último elemento como texto, sin enlace. |
| `acciones`, `pestanias` | `ReactNode` | No | Ausentes | Acciones a la derecha; pestañas bajo el encabezado. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alNavegarMiga` | Destino seleccionado | Se activa una miga anterior; las acciones conservan sus propios eventos. |

- **Estados y composición:** con o sin subtítulo, migas, pestañas y acciones; no hay estado de carga de datos propio.
- **Accesibilidad y responsive:** `Breadcrumbs` dentro de navegación etiquetada; título antes de acciones en el DOM; apilar acciones sin truncar el título en móvil.
- **CCR-05-01:** DADA una página de segundo nivel, ENTONCES la miga actual no navega, las anteriores sí, y se mantiene un solo H1.
- **Pruebas previstas:** roles de encabezado y navegación, activación de migas y ajuste del contenido en ancho móvil.

### CR-06. BarraFiltros

- **Propósito y límites:** componer búsqueda, controles y filtros activos; la pantalla sincroniza URL, consulta y paginación. No fija nombres de parámetros HTTP.
- **Diseño y consumidores:** §§12.2 y 13.4; ES-F01-01, ES-F02-03, ES-F04-01, ES-F05-02, ES-F05-07 y listados de F-06 [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `busqueda` | Texto | Si hay buscador | `''` | Campo controlado y acción Limpiar búsqueda. |
| `etiquetaBusqueda` | Texto | Si hay buscador | Sin valor | Label visible adaptado al listado. |
| `controles` | `ReactNode` | No | Ausente | Selectores y fechas controlados por la pantalla. |
| `activos` | `FiltroActivoUi[]` | No | `[]` | Pills removibles; Limpiar filtros se habilita si hay alguno o búsqueda. |
| `consultando` | Booleano | No | `false` | Indica consulta pendiente sin ocultar controles. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alCambiarBusqueda` | Texto actual | Inmediatamente al editar; la pantalla actualiza el valor controlado. |
| `alConsultarBusqueda` | Último texto | Tras 300 ms sin cambios; cancela la emisión pendiente al cambiar de nuevo o desmontarse. |
| `alQuitarFiltro` / `alLimpiar` | `id` / ninguno | Al retirar una pill o limpiar todo; la limpieza consulta inmediatamente y cancela el debounce anterior. |

- **Estados y composición:** sin filtros, filtros activos y consulta en curso; composición en superficie `cloud-subtle`. Selectores aplican su cambio inmediatamente; sin botón Aplicar.
- **Accesibilidad y responsive:** labels visibles; «Quitar [valor]» en cada pill; controles apilados en móvil, búsqueda primero. El consumidor restaura filtros al volver desde el detalle y vuelve a página 1 al cambiarlos.
- **CCR-06-01:** DADAS varias pulsaciones dentro de 300 ms, ENTONCES se consulta una vez con el texto final; una respuesta de búsqueda anterior no sustituye los resultados actuales.
- **CCR-06-02:** DADOS filtros en la URL, CUANDO se vuelve del detalle o se limpian, ENTONCES controles, URL, página y resultados coinciden; no reaparece una búsqueda pendiente anterior.
- **Pruebas previstas:** temporizadores controlados para debounce, limpieza y desmontaje; integración del contenedor con URL y respuestas fuera de orden.

### CR-07. TablaDatos

- **Propósito y límites:** representar filas y solicitar cambios de orden/página. `Table` de Mantine para presentación; TanStack Table para lógica cuando se necesite. El adaptador determina si la consulta es local o remota, sin paginar dos veces los datos.
- **Diseño y consumidores:** §§12.3 y 13.4; listados administrativos [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `filas`, `obtenerId` | Lista genérica / función a identificador | Sí | Sin valor | Clave estable del registro, nunca índice de fila. |
| `columnas` | Configuración de columnas | Sí | Sin valor | Cada columna declara `id`, encabezado, celda, alineación, si admite orden y prioridad responsive. |
| `tituloAccesible` | Texto | Sí | Sin valor | `caption` de la tabla. |
| `estado`, `actualizando` | `EstadoConsulta` / booleano | Sí / no | Sin valor / `false` | Carga inicial distinta de actualización con datos previos. |
| `orden`, `paginacion` | `OrdenUi`, `PaginacionUi` | Sí cuando aplican | Orden `null`; tamaño UI 20 | El consumidor aporta página y total reales; F-05 aplica su regla de paginar a partir de 50 registros, sin inferir tamaño HTTP. |
| `renderizarAcciones`, `renderizarEstado` | Funciones a `ReactNode` | No | Ausentes | Acciones por fila y CR-08 según contexto. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alCambiarOrden` | Nuevo `OrdenUi` | Se activa la cabecera ordenable con teclado o puntero. |
| `alCambiarPagina` | Página solicitada desde 1 | Se activa paginación válida. |

- **Estados y composición:** carga inicial con cinco filas skeleton; datos; vacío; sin resultados; error; sin permiso. Actualizar conserva filas previas solo mientras el usuario siga autorizado. Nunca mostrar una tabla vacía como sustituto silencioso de un error.
- **Accesibilidad y responsive:** cabeceras con alcance de columna y `aria-sort` cuando aplique, caption, botones de orden y paginación etiquetados. Fila mínima 48 px; números a la derecha con `ia-num`. En móvil, scroll dentro del contenedor; en tableta F-02, datos secundarios accesibles desde Ver detalle. Más de dos acciones: dos visibles y resto en menú.
- **CCR-07-01:** DADO un total conocido y una página válida, ENTONCES el resumen «Mostrando … de …» coincide con las filas; para cero registros no se muestra «1–0» ni se ofrece una página inexistente.
- **CCR-07-02:** DADA una actualización fallida con datos previos autorizados, ENTONCES se conservan con aviso; DADO un rechazo de permisos, ENTONCES se retiran filas y filtros protegidos.
- **Pruebas previstas:** orden y paginación controlados, cero filas, cambio de filtros, error de refresco y lectura de tabla con teclado.

### CR-08. EstadoVista

- **Propósito y límites:** patrón de composición para `EstadoVacio`, `EstadoError` y `AccesoDenegado`, además de skeletons. Puede implementarse mediante componentes pequeños; no obliga a un componente con todas las variantes.
- **Diseño y consumidores:** §§12.7, 13.4 y 13.12; ambas aplicaciones [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `estado` | `EstadoConsulta` | Sí | Sin valor | El contenedor resuelve el resultado, no se infiere desde una lista vacía. |
| `titulo`, `descripcion` | Texto | Según estado | Mensajes comunes de §13.4 si aplican | Mensaje específico comprensible, sin detalle técnico. |
| `accion` | `AccionUi` | No | Ausente | Crear, limpiar, reintentar o volver según el resultado. |
| `esqueleto`, `children` | `ReactNode` | Según estado | Ausentes | Forma de carga propia de tabla, tarjeta o formulario; contenido solo en `datos`. |
| `compacto` | Booleano | No | `false` | Variante dentro de un bloque, salvo denegación de la vista completa. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alAccionar` | `id` de acción | La persona solicita la recuperación ofrecida. |

- **Estados y composición:** vacío inicial con acción de creación si procede; sin resultados con Limpiar filtros; error con Reintentar; no encontrado con Volver; sin permiso sin datos ni filtros del recurso. CR-07 conserva los filtros durante su carga inicial fuera de la región skeleton.
- **Accesibilidad y responsive:** región en carga con `aria-busy`; aviso de resultado sin anuncios repetidos; título respeta jerarquía de la página. Mantener texto completo en móvil y respetar movimiento reducido del skeleton.
- **CCR-08-01:** DADOS cero registros, cero coincidencias, fallo de red y rechazo de acceso, ENTONCES cada caso muestra su mensaje y recuperación propia, sin confundirse entre sí.
- **Pruebas previstas:** matriz de estados, ausencia de contenido protegido y acción de recuperación accesible.

### CR-09. BadgeEstado

- **Propósito y límites:** resolver etiqueta, icono y apariencia desde una configuración única prevista en `packages/componentes-compartidos/src/dominio/estados.ts`. No cambiar estados ni interpretar la disponibilidad del recurso.
- **Diseño y consumidores:** §§11.7 y 16; ambas aplicaciones [cite: 1, 6].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `contexto` | `despacho`, `operacionRepartidor`, `registro`, `zona`, `vehiculo`, `vinculacion`, `recepcion`, `etiqueta` | Sí | Sin valor | Evita confundir valores como `PENDIENTE` de contextos distintos. |
| `valor` | Valor del contexto o desconocido | Sí | Sin valor | Traducción central; no imprimir el enum recibido. |
| `size` | `sm`, `md` | No | `md` | Variante compacta para tabla sin suprimir el texto. |
| `complemento` | Texto | No | Ausente | Fecha o indicación adicional prevista en la UI; no sustituye la etiqueta. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| Ninguno | No aplica | Es informativo; los filtros usan `Chip` o controles separados. |

| Grupo o estado | Etiqueta y variante | Regla |
|---|---|---|
| `PENDIENTE_ASIGNACION`, `ASIGNADO`, `EN_CAMINO` | Pendiente de asignación: neutral; Asignado y En camino: info | Distinguir con texto e icono de §16.1. |
| `ENTREGADO`, `FALLIDO`, `DEVUELTO_A_ORIGEN`, `CANCELADO` | Entregado: success; Fallido: error; Devuelto a origen: warning; Cancelado: neutral | Recepción del paquete no crea un estado nuevo del despacho. |
| `DISPONIBLE`, `EN_RUTA`, `SATURADO`, `FUERA_DE_TURNO` | Disponible: availability; En ruta: info; Saturado: error; Fuera de turno: neutral | Perfil operativo local, distinto del registro activo/inactivo. |
| Registro, zona, vehículo, vinculación, recepción | Configuración de §16.4 | «Vinculado» se representa con texto e icono; estados derivados como «En jornada» los aporta el adaptador. |
| Simulado, Nuevo, Reintento, No intentado y otras etiquetas | Configuración de §16.2 | Nuevo es la variante signal; no usarla para errores o éxito. |
| Valor desconocido | «Estado no disponible», neutral | No inventar una transición ni un permiso; registrar diagnóstico fuera de la UI. |

- **Accesibilidad y responsive:** texto visible, icono decorativo oculto al lector y contraste del tema; sin tooltip obligatorio para leer el estado. No reducir opacidad de filas completas para indicar inactividad; no truncar la etiqueta en móvil.
- **CCR-09-01:** DADO el mismo contexto y estado en dos pantallas, ENTONCES etiqueta, icono y variante coinciden; `FALLIDO` sigue siendo Fallido tras confirmar recepción.
- **CCR-09-02:** DADO un valor no reconocido, ENTONCES se muestra Estado no disponible sin exponer el enum ni provocar un fallo de renderizado.
- **Pruebas previstas:** tabla de correspondencias, contextos con valores iguales, desconocidos y comprobación visual en superficies claras y oscuras.

### CR-10. TarjetaKpi

- **Propósito y límites:** presentar un indicador; opcionalmente solicitar un filtro. Recibe valor confirmado, no calcula agregados de una página paginada.
- **Diseño y consumidores:** §13.5; resumen de F-02, F-03, F-04 y F-06 [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `id`, `etiqueta`, `valor` | Texto, texto, número o texto formateado | Sí | Sin valor | La ausencia de dato no se convierte en cero. |
| `descripcion`, `icono` | Texto / nodo de icono | No | Ausentes | Datos complementarios del indicador. |
| `tono` | `neutral`, `info`, `success`, `warning`, `error`, `availability` | No | `neutral` | Tokens semánticos, sin color arbitrario. |
| `accionable`, `seleccionada`, `cargando` | Booleanos | No | `false` | Solo la variante accionable es botón; selección refleja el filtro real. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alSeleccionar` | `id` del indicador | Activación de una tarjeta accionable habilitada. |

- **Estados y composición:** informativa, accionable, seleccionada y carga; `Card` o `UnstyledButton`. Valor de alto impacto conforme a §13.5; no crear un encabezado semántico por cada número.
- **Accesibilidad y responsive:** nombre con etiqueta y valor, `aria-pressed` en accionables; grilla de una, dos y hasta cuatro columnas según §1.4.
- **CCR-10-01:** DADA una tarjeta accionable, CUANDO se activa con teclado, ENTONCES emite su identificador una vez y su selección coincide con el filtro devuelto por la pantalla.
- **Pruebas previstas:** diferencia entre informativa y botón, carga sin falso cero y selección controlada.

### CR-11. BarraOcupacion

- **Propósito y límites:** visualizar una métrica y su proyección. Recibe ocupación y límites del contenedor; no suma despachos ni autoriza una asignación.
- **Diseño y consumidores:** §§13.6 y 16.6; asignación, reasignación y rutas de F-02; disponibilidad y monitoreo de F-06 [cite: 1, 6].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `metrica` | `peso`, `volumen`, `paquetes` | Sí | Sin valor | Etiqueta y unidad: kg, m³, paquetes. |
| `usado`, `limite` | Números finitos | Sí | Sin valor | Para un porcentaje válido: `usado >= 0` y `limite > 0`. |
| `proyeccion` | Número finito no negativo | No | Ausente | **Total resultante**, no incremento. El segmento adicional representa `max(0, proyeccion - usado)`. |
| `variante` | `completa`, `compacta` | No | `completa` | Barra 8 px con valores; compacta 4 px y porcentaje, conservando acceso al valor completo. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| Ninguno | No aplica | Es visualización, no un control de capacidad. |

- **Cálculo y estados:** porcentaje real `100 × usado / limite`; normal si menor que 70, alta desde 70 y menor que 100, llena desde 100. Clasificar antes de redondear; mostrar decimales si el redondeo ocultaría un umbral. La proyección se expresa también en texto; segmento rayado del nivel resultante. Recortar solo el dibujo a 100 %, no el valor ni el exceso. Un límite inválido muestra «Capacidad no disponible», sin división por cero ni `NaN`.
- **Composición:** `Progress` más etiqueta, relación usado/límite y nivel; exceso con cantidad y unidad. Si falta una proyección válida, no presentar una capacidad supuestamente segura.
- **Accesibilidad y responsive:** progressbar con rango 0–100, `aria-valuenow` recortado al rango y `aria-valuetext` con valores reales, nivel y exceso; texto siempre disponible, incluso en compacta. Apilar etiquetas en móvil.
- **CCR-11-01:** DADOS 69,9 %, 70 %, 99,9 % y 100 %, ENTONCES los niveles son Normal, Alta, Alta y Llena; el redondeo no cambia esa clasificación.
- **CCR-11-02:** DADOS 320/500 kg y proyección total 540 kg, ENTONCES se muestra 64 % actual, 108 % proyectado y «Excede en 40 kg»; la barra no rebasa el contenedor y no confirma ninguna asignación.
- **CCR-11-03:** DADO límite cero o dato no finito, ENTONCES se informa capacidad no disponible sin porcentaje engañoso.
- **Pruebas previstas:** umbrales, proyección, exceso, datos inválidos y nombre/valor accesible.

### CR-12. ModalConfirmacion

- **Propósito y límites:** confirmar una acción con sus efectos y objeto afectado; los formularios complejos componen un `Modal` propio con CR-01/02, sin ampliar este componente a todos los casos.
- **Diseño y consumidores:** §§12.6 y 13.7; activar/desactivar, bajas, recepción simple cuando corresponda, descarte y cierre de jornada [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `abierto` | Booleano | Sí | Sin valor | Apertura controlada. |
| `titulo`, `descripcion`, `etiquetaConfirmar` | Texto | Sí | Sin valor | Pregunta con objeto y verbo concreto; explicar consecuencias. |
| `intencion` | `principal`, `destructiva` | No | `principal` | Icono informativo o advertencia; confirmar en naranja o rojo. |
| `procesando`, `confirmacionDeshabilitada` | Booleanos | No | `false` | Bloquea confirmaciones repetidas y cierre durante el envío. |
| `error`, `children` | Texto / `ReactNode` | No | Ausentes | Error dentro del modal y resumen adicional del objeto. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alConfirmar` | Ninguno | Confirmar habilitado y sin operación en curso. |
| `alCancelar` | Ninguno | Cancelar, Esc o cierre, solo fuera de procesamiento. |

- **Estados y composición:** cerrado, abierto, confirmando y error; un error conserva el modal y su contexto. Clic en fondo no cierra; no hay cierre por éxito hasta que lo ordene el consumidor.
- **Accesibilidad y responsive:** título/descripción asociados, foco contenido y devuelto al disparador. Inicial en Cancelar si destructivo; en el primer control apropiado en otros casos. Modal de referencia 480 px ajustado al viewport; botones apilados en móvil. Hoja inferior para cierre móvil según la UI.
- **CCR-12-01:** DADA una confirmación destructiva, ENTONCES el foco inicial está en Cancelar; Esc cancela fuera de carga y ninguna vía de cierre abandona una operación mientras se está enviando.
- **CCR-12-02:** DADO un fallo de la mutación, ENTONCES se conserva contexto y error dentro del modal y se permite reintentar al finalizar la carga.
- **Pruebas previstas:** foco, retorno, teclado, doble confirmación, error y cierre durante carga.

### CR-13. BarraAccionesFija

- **Propósito y límites:** mantener acciones al pie; el consumidor define etiquetas, disponibilidad y comportamiento.
- **Diseño y consumidores:** §13.9; formulario de zona y detalle, entrega, fallo y cierre del repartidor [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `principal` | `AccionUi` | Sí | Sin valor | Una acción de mayor jerarquía, con bloqueo o carga según CR-01. |
| `secundaria` | `AccionUi` | No | Ausente | Alternativa, regreso o cancelación. |
| `intencionPrincipal` | `principal`, `destructiva` | No | `principal` | Respeta el efecto definido por la UI. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alAccionar` | `id` de la acción | Activación válida del control correspondiente. |

- **Estados y composición:** normal, principal bloqueada y envío en curso; motivos visibles junto a la acción. Superficie blanca y borde superior del tema.
- **Accesibilidad y responsive:** región etiquetada; en móvil principal de 50 px y ancho completo, secundaria encima; padding con zona segura. El shell o contenedor reserva la altura real, incluidos mensajes y botones apilados; no asumir una altura fija insuficiente.
- **CCR-13-01:** DADA una barra con motivo de bloqueo de varias líneas, ENTONCES el último campo y su error pueden desplazarse por encima de ella y siguen siendo operables con teclado.
- **Pruebas previstas:** contenido largo, ambas acciones, carga y viewport móvil con reserva del pie.

### CR-14. FranjaEstado

- **Propósito y límites:** informar conexión, turno o actualización fallida. Recibe el estado; no implementa cola offline, temporizadores de consulta ni habilita transiciones.
- **Diseño y consumidores:** §13.12; F-03 y monitoreo de F-06 [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `tipo` | `sinConexion`, `fueraDeTurno`, `datosDesactualizados` | Sí | Sin valor | Error para conexión; advertencia para turno o refresco. |
| `mensaje` | Texto | No | Texto de §13.12 para el tipo | Explicar situación y siguiente acción; no prometer un reintento automático que el contenedor no programe. |
| `accion` | `AccionUi` | No | Ausente | Actualizar o reintentar manualmente, cuando proceda. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alAccionar` | `id` de acción | Solicitud de recuperación habilitada. |

- **Estados y composición:** visible mientras la causa persista; si coinciden falta de conexión y fuera de turno, mostrar ambas causas en orden conexión/turno. Error de refresco conserva los datos anteriores autorizados y su contexto.
- **Accesibilidad y responsive:** avisar una vez al cambiar la causa, sin anunciar cada refresco; texto e icono. En F-03 debajo del encabezado y dentro de la reserva de altura; en F-06 encima de la tabla.
- **CCR-14-01:** DADO un fallo de actualización del tablero, ENTONCES permanecen los datos previos con aviso y recuperación; al recuperar datos válidos se retira la franja de desactualización.
- **CCR-14-02:** DADO F-03 sin conexión, ENTONCES no se encolan comandos ni se muestra éxito; la franja no oculta la condición de fuera de turno si también existe.
- **Pruebas previstas:** transición de estados, coexistencia de avisos y fallo/recuperación del contenedor con red simulada.

### CR-15. NotificacionOperacion

- **Propósito y límites:** adaptador compartido de `@mantine/notifications`; emitir confirmaciones después del resultado de la operación. No requiere un nuevo componente ni interpreta respuestas HTTP directamente.
- **Diseño y consumidores:** §§12.7 y 17; ambas aplicaciones [cite: 1].

| Entrada del adaptador | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `id` | Texto | Sí | Sin valor | Identifica la notificación para actualizarla o evitar duplicados de la misma operación. |
| `tipo` | `exito`, `efectoPendiente`, `informacion` | Sí | Sin valor | Verde, amarillo persistente o información azul. |
| `mensaje` | Texto | Sí | Sin valor | Resultado concreto; no afirmar éxito mientras la petición esté pendiente. |
| `accion` | `AccionUi` | No | Ausente | Acción contextual prevista en la UI. |

| Evento o salida | Datos entregados | Cuándo se emite |
|---|---|---|
| Resultado de mostrar/actualizar | `id` de notificación | Al registrar la notificación en el proveedor. |
| `alAccionar` | `id` de acción | Se activa la acción contextual, si existe. |

- **Estados y composición:** éxito ordinario con cierre a los 4 s; efecto pendiente sin autocierre; información necesaria para continuar también persistente. Errores que requieren corregir un formulario permanecen en su `Alert` o campo, no solo en una notificación.
- **Accesibilidad y responsive:** región `aria-live="polite"`; evitar anuncios duplicados con el mensaje de página. Posición que no cubra las acciones móviles ni su foco; cierre accesible.
- **CCR-15-01:** DADO un cierre registrado con notificación a Ventas pendiente, ENTONCES se comunica el efecto pendiente sin autocierre y sin presentar la operación registrada como fallida.
- **Pruebas previstas:** temporizadores, persistencia, actualización por `id` y emisión únicamente tras respuesta confirmada.

### CR-16. TarjetaDespacho

- **Propósito y límites:** identificar un despacho de la ruta y abrir su detalle. Recibe posición y presentación; no decide cuál es el siguiente ni incrementa intentos.
- **Diseño y consumidores:** §§13.2 y 22; ES-F03-02, ES-F03-03 y ES-F03-07 [cite: 1, 2].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `idDespacho`, `codigo`, `posicion` | Texto, texto, número | Sí | Sin valor | Identidad opaca y código visible completo. |
| `direccion`, `destinatario`, `estado` | Texto | Sí | Sin valor | Dirección hasta dos líneas; estado con CR-09. |
| `etiquetaIntento` | Texto | Sí | Sin valor | Texto preparado según la regla funcional, por ejemplo «Intento 1 de 2»; no deducirlo solo desde el contador de fallos. |
| `variante` | `normal`, `siguiente`, `resuelto` | No | `normal` | Siguiente con `primary-soft`; resuelto con superficie y texto secundarios, sin opacidad global. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alAbrir` | `idDespacho` | Activación de la tarjeta mediante puntero o teclado. |

- **Estados y composición:** normal, siguiente y resuelto; carga/vacío resueltos por la lista con CR-08. Tarjeta navegable completa, sin botones interactivos anidados.
- **Accesibilidad y responsive:** botón o enlace con nombre que identifique código y destino; foco visible. Ancho completo, texto operativo de 16 px, código sin elipsis; detalle ofrece la dirección completa.
- **CCR-16-01:** DADO un despacho resuelto, ENTONCES la tarjeta mantiene contraste y acceso al detalle; abrirla no inicia traslado ni modifica estado.
- **Pruebas previstas:** activación, variantes, código largo y diferencia entre posición y contador de intentos.

### CR-17. CapturaEvidencia

- **Propósito y límites:** seleccionar o capturar una fotografía y mostrar su estado. El contenedor valida según la política acordada, procesa si corresponde, solicita autorización y sube el archivo; la foto no se envía como Base64 a la API de negocio.
- **Diseño y consumidores:** §13.10 y §22; ES-F03-05 y ES-F03-06; contrato Operación §§3.1–3.3 [cite: 1, 4, 5]. Referencia: [Operación](../integraciones/api-contract-operacion-reparto.md#31-autorizar-la-carga-de-evidencia).

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `archivo` | `File` o `null` | Sí | Sin valor | Selección actual controlada; `null` indica ausencia. |
| `descripcionFoto` | Texto | Sí | Sin valor | Texto alternativo contextual de la previsualización. |
| `fase` | `vacia`, `lista`, `procesando`, `subiendo`, `cargada`, `error` | Sí | Sin valor | Distinguir archivo elegido, carga confirmada y confirmación del despacho. |
| `progreso` | Número de 0 a 100 o `null` | No | `null` | Porcentaje solo si se dispone de medición real; de otro modo carga indeterminada. |
| `politicaArchivo` | Objeto con `tiposPermitidos` y `maximoBytes` | Antes de integración real | Sin valor | Reglas acordadas y trazadas; no inventar formatos o megabytes. Ver DC-03. |
| `error`, `disabled`, `obligatoria` | Texto / booleanos | No | Ausente / `false` / `true` | Mantener archivo al fallar la carga; informar obligatoriedad si falta. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alSeleccionar` | `File` | Cámara o selector devuelve archivo; cancelar el selector conserva la selección previa. |
| `alVolverATomar` | Ninguno | Solicita reemplazo sin borrar anticipadamente la foto actual. |
| `alReintentar` | Ninguno | Solicitud explícita de recuperar una carga fallida. |

- **Estados y composición:** `FileButton` con captura trasera sugerida y filtro acorde a la política, marco 4:3, `Image`, progreso y error. Si el dispositivo no ofrece cámara, usar el selector disponible. Liberar la URL de previsualización local al reemplazar o desmontar; conservarla durante un fallo de carga. No asumir que seleccionar archivo significa evidencia persistida.
- **Accesibilidad y responsive:** área táctil completa con nombre Tomar foto, `alt` contextual y progreso anunciado; sin acciones inaccesibles dentro de una imagen. Marco fluido, controles `lg`; sin almacenamiento de operaciones offline.
- **CCR-17-01:** DADA una entrega sin fotografía, ENTONCES se informa la obligatoriedad, Confirmar entrega permanece bloqueado y no se envía ninguna transición.
- **CCR-17-02:** DADA una foto y carga fallida, ENTONCES la previsualización permanece y puede reintentarse; no se marca `ENTREGADO` ni `FALLIDO` hasta que el comando correspondiente sea confirmado.
- **CCR-17-03:** DADO un archivo que incumple la política acordada, ENTONCES se informa la causa y no se habilita la confirmación; los límites se verifican también en backend.
- **Pruebas previstas:** archivos de ejemplo según política, cancelar/reemplazar selección, fallos de autorización/carga y separación entre carga de foto y transición final.

### CR-18. VisorEvidencia

- **Propósito y límites:** visualizar evidencia autorizada. El contenedor obtiene una URL firmada mediante el contrato Operación §3; el visor no deriva una URL pública ni decide acceso desde un identificador. Referencia: [Operación](../integraciones/api-contract-operacion-reparto.md#3-api-de-f-03-operación-del-repartidor).
- **Diseño y consumidores:** §§12.6, 22 y 23; ES-F03-08 y ES-F04-02 [cite: 1, 4, 5].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `abierto` | Booleano | Sí | Sin valor | Apertura controlada. |
| `estado` | `carga`, `lista`, `sinEvidencia`, `expirada`, `error`, `sinPermiso` | Sí | Sin valor | Distinguir ausencia legítima, vencimiento y fallo de acceso. |
| `urlAutorizada` | Texto o `null` | En estado `lista` | `null` | Referencia temporal obtenida por el contenedor; no persistirla en almacenamiento de navegador, logs ni evidencia de pruebas. |
| `descripcion`, `mensajeSinEvidencia` | Texto | Descripción sí | Mensaje contextual del consumidor | `alt` con despacho y tipo de evidencia; «No intentado — sin foto» solo si ese es el caso confirmado. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alCerrar` | Ninguno | Esc, cierre o regreso del visor. |
| `alSolicitarAcceso` | Ninguno | Volver a cargar o reintentar; el consumidor renueva la autorización. |
| `alFallarImagen` | Ninguno | Falla la carga de `Image`; el contenedor determina si venció o hubo otro error. |

- **Estados y composición:** skeleton 4:3, imagen `fit="contain"`, ausencia, enlace expirado con Volver a cargar y acceso denegado sin imagen. Al cerrar o cambiar de despacho, retirar la URL anterior; no mostrar brevemente la foto del recurso previo.
- **Accesibilidad y responsive:** diálogo con título y retorno de foco; texto alternativo descriptivo, no URL. Modal amplio en administración y hoja inferior en móvil conforme a la UI.
- **CCR-18-01:** DADA una autorización vencida, ENTONCES se ofrece renovar mediante el contenedor; nunca se construye una ruta pública como recuperación.
- **CCR-18-02:** DADO un acceso denegado o cambio de despacho, ENTONCES no queda visible la fotografía anterior ni su URL en el DOM del visor.
- **Pruebas previstas:** apertura/cierre, cambio de recurso, expiración, fallo de imagen y respuesta de acceso denegado con adaptador simulado.

### CR-19. HistorialEstados

- **Propósito y límites:** presentar transiciones registradas por el servidor. No crear eventos por pulsaciones locales ni usar la hora del navegador como fecha de auditoría.
- **Diseño y consumidores:** §23, UI F-02 y F-04; ES-F02-05 y ES-F04-02 [cite: 1, 2, 6].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `entradas` | Lista de entradas de presentación | Sí | Sin valor | Cada una con `id`, `fechaServidor`, `descripcionEvento` y, si existen, `estadoAnterior`, `estadoNuevo`, `ejecutor`, `observacion`. |
| `estado` | `EstadoConsulta` | Sí | Sin valor | Carga, datos, vacío o recuperación según corresponda. |
| `orden` | `ascendente`, `descendente` | No | `ascendente` | Ordenar por tiempo del servidor; conservar orden estable en empates. |
| `titulo` | Texto | No | `Historial de estados` | Encabezado del bloque, no otro H1. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alReintentar` | Ninguno | Recuperación tras fallo de consulta. |

- **Estados y composición:** `Timeline` dentro de tarjeta; estados con CR-09, texto del evento, fecha/hora y datos de autoría disponibles. Una recepción sin transición se representa como evento recibido, conservando Fallido; datos ausentes no se inventan.
- **Accesibilidad y responsive:** lista cronológica legible sin depender de la línea gráfica; elemento `time` con instante original y formato visible acordado. Una columna con texto ajustable, sin truncar observaciones necesarias.
- **CCR-19-01:** DADO un historial con recepción en centro sin cambio de estado, ENTONCES muestra ese evento y su fecha real sin inventar un estado «Recibido» del despacho.
- **Pruebas previstas:** orden estable, entradas sin datos opcionales, fechas del servidor y evento sin transición.

### CR-20. TarjetaRepartidor

- **Propósito y límites:** presentar un candidato seleccionable para asignación o reasignación. Recibe compatibilidad y motivos calculados por el contenedor/backend; no reconstruye disponibilidad solo desde el color de las barras.
- **Diseño y consumidores:** §21, pantallas P2 y P4; ES-F02-04 y ES-F02-06 [cite: 1, 2, 6].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| `idRepartidor`, `nombre`, `placa`, `zona` | Texto | Sí | Sin valor | Identificar candidato, vehículo y jornada operativa. |
| `estadoOperativo` | Valor del contexto operativo | Sí | Sin valor | Usa CR-09. |
| `metricas` | Lista de tres objetos para CR-11 | Sí | Sin valor | Peso, volumen y paquetes con usados, límites y proyección si existe. |
| `seleccionada`, `disabled` | Booleanos | No | `false` | Selección controlada; no permitir candidato bloqueado. |
| `motivoDeshabilitado` | Texto | Si `disabled` por negocio | Sin valor | Causa visible y asociada, por ejemplo capacidad excedida. |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| `alSeleccionar` | `idRepartidor` | Se selecciona una opción habilitada del grupo. |

- **Estados y composición:** normal, seleccionada y bloqueada; `Radio.Card` dentro de `Radio.Group` etiquetado Repartidor, con CR-09 y tres CR-11. Carga y ausencia de candidatos pertenecen al listado. En reasignación, la pantalla excluye al repartidor actual.
- **Accesibilidad y responsive:** selección única con teclado, etiqueta y motivo accesibles; tarjetas apiladas y barras fluidas. Selección no envía la asignación; la confirmación es una acción separada.
- **CCR-20-01:** DADOS candidatos con capacidad suficiente e insuficiente, ENTONCES solo puede seleccionarse uno habilitado; el bloqueado explica el motivo y no se ejecuta una asignación al seleccionarlo.
- **CCR-20-02:** DADO un candidato que deja de ser válido al actualizar, ENTONCES el contenedor invalida la selección y la confirmación, conservando el mensaje del cambio.
- **Pruebas previstas:** radio con teclado, selección controlada, bloqueo por una sola métrica y cambio concurrente de disponibilidad.

## 4. Orden de implementación y evidencia

### 4.1. Incrementos de componentes compartidos

Cada tarea `TCR-NN` es una propuesta de trabajo dentro de esta especificación; no representa un issue creado ni una tarea completada. Se implementa solo el subconjunto requerido por el siguiente incremento funcional, respetando las dependencias. Antes de consumir un componente, su implementación debe haber sido verificada.

| Incremento / tarea | Resultado | Prerrequisitos | Criterios que verifica | Estado y evidencia |
|---|---|---|---|---|
| ICR-01 / TCR-01 | Tema y proveedor; patrones CR-01 y CR-02 | Conciliar dependencias DC-01; entradas funcionales de los campos | CCR-01-01/02, CCR-02-01/02/03; reglas transversales | Pendiente; sin código ni ejecución. |
| ICR-02 / TCR-02 | CR-08, CR-09 y CR-15 | ICR-01; catálogo de estados y errores | CCR-08-01, CCR-09-01/02, CCR-15-01 | Pendiente; sin evidencia. |
| ICR-03 / TCR-03 | CR-03, CR-05, CR-12 y CR-13 | ICR-01 y componentes de feedback que use la página | CCR-03-01/02, CCR-05-01, CCR-12-01/02, CCR-13-01 | Pendiente; sin evidencia. |
| ICR-04 / TCR-04 | CR-06, CR-07 y CR-10 | ICR-01/02; DC-04 para integración de listados | CCR-06-01/02, CCR-07-01/02, CCR-10-01 | Pendiente; fixtures de UI no equivalen a integración. |
| ICR-05 / TCR-05 | CR-11 y CR-20 | ICR-01/02; métricas y disponibilidad acordadas para integración | CCR-11-01/02/03, CCR-20-01/02 | Pendiente; sin evidencia. |
| ICR-06 / TCR-06 | CR-14, CR-04 y CR-16 | ICR-01/02/03; CR-13 disponible | CCR-14-01/02, CCR-04-01/02, CCR-16-01 | Pendiente; sin evidencia. |
| ICR-07 / TCR-07 | CR-17 y CR-18 | ICR-01/02; política DC-03 antes de aceptación real | CCR-17-01/02/03, CCR-18-01/02 | Pendiente; almacenamiento y autorizaciones deben distinguirse de mocks. |
| ICR-08 / TCR-08 | CR-19 | ICR-02; historial y fechas acordados en DC-04/06 para integración | CCR-19-01 | Pendiente; sin evidencia. |

### 4.2. Comprobaciones y registro de evidencia

Verificación prevista con las herramientas de pruebas del frontend una vez creado su proyecto y conciliado el stack. Los casos descritos en §3 se convierten en pruebas de comportamiento con Testing Library y Vitest, complementadas por revisión visual y teclado. No se ejecutan pruebas de componentes desde este repositorio documental [cite: 1, 3].

| Nivel | Qué comprobar | Artefacto esperado al implementar |
|---|---|---|
| Componente | Eventos, estados controlados, datos extremos, carga y recuperación según cada `CCR` | Prueba, comando ejecutado, resultado y commit del frontend. |
| Composición | Filtros/URL/página coherentes; doble envío bloqueado; datos retirados al perder permisos; selección invalidada al cambiar disponibilidad | Prueba del contenedor con adaptador de API simulado, identificada como simulación. |
| Visual y accesibilidad | Tema, contraste previsto, teclado, foco, etiquetas, movimiento reducido, viewport administrativo, tableta y móvil aplicables | Capturas de estados y registro de pasos; herramienta de accesibilidad si se usa, sin sustituir la revisión de teclado. |
| Integración real | Contrato correspondiente, autorización, errores, concurrencia, carga/lectura de foto y cambios confirmados por backend | Registro de entorno, revisiones frontend/backend, datos de prueba y resultados; URLs firmadas y tokens ocultos. |

En la tarea que implemente el componente, registrar `CR-NN` → `CCR-NN-XX` → `TCR-NN` → archivo/commit frontend → prueba → evidencia real. El `evidence.md` de cada especificación consumidora enlaza esa evidencia compartida y añade la comprobación de su integración. Para una especificación todavía sin migrar, usar un registro trazable en el PR o trabajo de implementación; no enlazar rutas de evidencia inexistentes [cite: 7].

### 4.3. Mapa de consumidores y límites

Los enlaces siguientes apuntan a documentos existentes. Que una especificación tenga impacto visual no obliga a que cada operación técnica disponga de una pantalla propia.

| Consumidores | UI actual | Componentes compartidos aplicables |
|---|---|---|
| [ES-F01-01](../especificaciones/ES-F01-01-ConsultarCatalogoZonas/spec.md), [ES-F01-02](../especificaciones/ES-F01-02-RegistrarZonaCobertura/spec.md), [ES-F01-03](../especificaciones/ES-F01-03-ActivarDesactivarZona/spec.md), [ES-F01-04](../especificaciones/ES-F01-04-ConfigurarTarifaZona/spec.md) | [F-01, pantallas 1–4](./funcionalidades/f-01.md) | CR-01/02/03/05/06/07/08/09/12/13/15 según pantalla. Editor de tarifa propio, con campos del contrato vigente; no añadir rangos futuros. |
| [ES-F02-02](../especificaciones/ES-F02-02-GenerarDespachoPrueba.md), [ES-F02-03](../especificaciones/ES-F02-03-ConsultarColaPendientes.md) | [F-02, cola](./funcionalidades/f-02.md) | CR-01/02/03/05/06/07/08/09/10/15; distinguir Simulado de datos reales. |
| [ES-F02-04](../especificaciones/ES-F02-04-AsignarDespachoRepartidor.md), [ES-F02-05](../especificaciones/ES-F02-05-ConsultarReordenarSecuenciaRuta.md), [ES-F02-06](../especificaciones/ES-F02-06-ReasignarDespachoRepartidor.md) | [F-02, asignación y rutas](./funcionalidades/f-02.md) | CR-01/02/03/05/08/09/11/12/15/19/20. Orden de ruta y guardado pertenecen al componente local de F-02. |
| [ES-F03-01](../especificaciones/ES-F03-01-acceso-y-habilitacion.md) | [F-03, acceso](./funcionalidades/f-03.md) | CR-01/02/08/14; sesión y habilitación en el contenedor. No exigir un rol global REPARTIDOR. |
| [ES-F03-02](../especificaciones/ES-F03-02-consulta-de-ruta.md), [ES-F03-03](../especificaciones/ES-F03-03-detalle-de-despacho.md), [ES-F03-04](../especificaciones/ES-F03-04-inicio-de-traslado.md), [ES-F03-07](../especificaciones/ES-F03-07-cierre-de-jornada.md) | [F-03, ruta, detalle y jornada](./funcionalidades/f-03.md) | CR-01/04/08/09/10/12/13/14/15/16 según vista. No añadir cálculo de rutas ni cola offline. |
| [ES-F03-05](../especificaciones/ES-F03-05-entrega-exitosa-con-evidencia.md), [ES-F03-06](../especificaciones/ES-F03-06-entrega-fallida.md), [ES-F03-08](../especificaciones/ES-F03-08-acceso-a-evidencia.md) | [F-03, evidencia](./funcionalidades/f-03.md) | CR-01/02/04/08/13/14/15/17/18; política de archivo pendiente de acuerdo. |
| [ES-F04-01](../especificaciones/ES-F04-01-ConsultarEntregasFallidas/spec.md), [ES-F04-02](../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/spec.md), [ES-F04-03](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/spec.md), [ES-F04-04](../especificaciones/ES-F04-04-ReprogramarDespachoFallido/spec.md), [ES-F04-05](../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen/spec.md) | [F-04, pantallas 1–5](./funcionalidades/f-04.md) | CR-01/02/03/05/06/07/08/09/10/12/15/18/19. `PanelDecision` y formularios de recepción/reprogramación/cierre permanecen locales. |
| [ES-F05-01](../especificaciones/ES-F05-01-RegistrarRepartidor.md), [ES-F05-02](../especificaciones/ES-F05-02-ConsultarRepartidores.md), [ES-F05-03](../especificaciones/ES-F05-03-EditarRepartidor.md), [ES-F05-04](../especificaciones/ES-F05-04-DarDeBajaRepartidor.md), [ES-F05-05](../especificaciones/ES-F05-05-VincularRepartidorConSeguridad.md), [ES-F05-06](../especificaciones/ES-F05-06-RegistrarFurgoneta.md), [ES-F05-07](../especificaciones/ES-F05-07-ConsultarFurgonetas.md), [ES-F05-08](../especificaciones/ES-F05-08-EditarFurgoneta.md), [ES-F05-09](../especificaciones/ES-F05-09-CambiarEstadoFurgoneta.md) | [UI agrupada F-05, repartidores y vehículos](./funcionalidades/f-05.md) | CR-01/02/03/05/06/07/08/09/12/15. Vinculación presenta estado; el formulario y el adaptador usan el contrato Operación §4.1. Referencia: [Operación](../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). |
| [F-06, disponibilidad y capacidad diaria](../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md) | [UI agrupada F-05, monitoreo y asignación diaria](./funcionalidades/f-05.md) | CR-01/02/03/05/06/07/08/09/10/11/12/14/15. Todavía no hay especificaciones atómicas `ES-F06-NN` en la revisión local. |
| [ES-F01-05](../especificaciones/ES-F01-05-ConsultarCoberturaDestino/spec.md), [ES-F01-06](../especificaciones/ES-F01-06-CotizarEnvioConProductos/spec.md), [ES-F01-07](../especificaciones/ES-F01-07-ResolverZonaParaModulo/spec.md), [ES-F01-08](../especificaciones/ES-F01-08-RegistrarTrazabilidadConfiguracion/spec.md), [ES-F02-01](../especificaciones/ES-F02-01-RecepcionSolicitudDespacho.md), [ES-F02-07](../especificaciones/ES-F02-07-CancelarDespachoPorAnulacion.md), [ES-F02-08](../especificaciones/ES-F02-08-RegistrarTrazabilidadOperaciones.md), [ES-F04-06](../especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones/spec.md) | Integración o comportamiento transversal | Sin componente ni pantalla propios por defecto. Las vistas afectadas reutilizan los componentes de su UI; cotización de otros canales permanece en el frontend del canal propietario. |

### 4.4. Uso desde el plan de una especificación

Preparación documental de [ES-F04-03](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/spec.md), con implementación y verificación funcional pendientes:

1. Su [spec.md](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/spec.md) conserva las reglas y los 12 CA; [ui.md](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/ui.md) describe resumen, sello Sí/No, observación opcional y recuperación.
2. Su [plan.md](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/plan.md) referencia esta revisión, CR-01/02/08/09/15 y los criterios aplicables; usa `Modal` Mantine con campos propios. El formulario no se fuerza dentro de CR-12.
3. El plan enlaza Gestión §5.2.1. El contenedor transforma los campos al payload acordado y adapta respuesta y errores; el componente no conoce el endpoint. Referencia: [Gestión](../integraciones/api-contract-gestion-despachos.md#521-confirmar-recepción-en-centro--es-f04-03).
4. [tasks.md](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/tasks.md) prepara/verifica los componentes antes del formulario y separa registro, liberación recuperable y actualización de listado/detalle.
5. [evidence.md](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/evidence.md) reserva los registros para demostrar recepción y liberación reales: el despacho permanece Fallido, el retorno se registra y la capacidad se sincroniza mediante los servicios responsables. Los resultados funcionales siguen sin ejecutar [cite: 4, 6, 7].

### 4.5. Distribución propuesta de responsabilidades

**Estado del reparto:** propuesta preparada a solicitud de Gerardo; trabajo de implementación pendiente. No crea issues, no envía asignaciones a los integrantes ni acredita su aceptación. Los componentes se implementan en el repositorio frontend; este repositorio conserva su especificación y trazabilidad.

El reparto toma como referencia las seis personas y sus funcionalidades, confirmadas por Gerardo, y los roles del [índice funcional](../funcionalidades/funcionalidad.md) y del [equipo](../README.md). Max, Valqui, Rhamses y Luis asumen tres elementos cada uno; Tarqui y Gerardo asumen cuatro. La complejidad varía y la preparación inicial se comparte. Luis es responsable de F-06; Rhamses conserva F-05 y DevOps. Los componentes son del equipo: un responsable mantiene la primera implementación y otra persona la revisa. La revisión funcional se complementa con la revisión visual de Max cuando se modifique la apariencia compartida.

| Responsable propuesto | Componentes o patrones | Relación con su trabajo | Revisor propuesto |
|---|---|---|---|
| Max, F-03 y Frontend/UI | CR-04 ShellRepartidor; CR-16 TarjetaDespacho; CR-17 CapturaEvidencia | Experiencia del repartidor y revisión del tema existente. CR-17 se coordina con Rhamses para almacenamiento y con el contrato para política y autorización, sin trasladar llamadas HTTP al componente visual. | Gerardo; Rhamses participa en evidencia. |
| Valqui, F-01 y Arquitectura | CR-01 AccionesUi; CR-02 CamposFormulario; CR-13 BarraAccionesFija | Controles y composición necesarios para zonas, tarifas y formularios; interfaces de uso comunes. CR-01/02 son configuraciones verificadas de Mantine, no envoltorios obligatorios. | Max. |
| Tarqui, F-02 | CR-05 EncabezadoPagina; CR-06 BarraFiltros; CR-07 TablaDatos; CR-20 TarjetaRepartidor | Listados, búsqueda y selección de candidatos para asignación y reasignación. | Valqui; Luis revisa el consumo de métricas en la selección. |
| Gerardo, F-04 y Calidad | CR-08 EstadoVista; CR-12 ModalConfirmacion; CR-18 VisorEvidencia; CR-19 HistorialEstados | Estados de consulta, confirmaciones, acceso a evidencia y trazabilidad necesarios para entregas fallidas. | Max; Rhamses participa en acceso autorizado a evidencia. |
| Rhamses, F-05 y DevOps | CR-03 ShellAdministrativo; CR-09 BadgeEstado; CR-15 NotificacionOperacion | Estructura administrativa y presentación transversal de estados y resultados; coordinación de herramientas del monorepositorio. CR-15 es un adaptador, no un segundo proveedor. | Max; Gerardo revisa estados de recepción y resultados de F-04. |
| Luis, F-06 | CR-10 TarjetaKpi; CR-11 BarraOcupacion; CR-14 FranjaEstado | Indicadores, ocupación de flota y avisos de datos desactualizados; métricas reutilizadas por F-02 y F-04. | Tarqui; Gerardo revisa indicadores de recepción y retorno. |

#### 4.5.1. Preparación compartida del frontend

| Trabajo previo | Responsable propuesto | Resultado verificable |
|---|---|---|
| Alinear `stack-frontend.md` con la guía común, verificar dependencias y scripts existentes y añadir herramientas de prueba | Rhamses, con revisión de Max | Reutilizar Vite/TypeScript, workspaces y lockfile existentes. Hay scripts `build` y `typecheck`; en la revisión no hay script ni dependencias de pruebas. Verificar la base, sin reinicializarla ni actualizar versiones solo por ser las más recientes. |
| Completar tema, tokens y fuentes existentes, y revisar estilos y proveedores de ambas aplicaciones | Max, con apoyo de Rhamses | Ambas aplicaciones ya importan `tema` y `tokens.css` del paquete y usan `MantineProvider` y `Notifications`. Comparar la base con el diseño y completar diferencias; esto no acredita los CR completos. |
| Incorporar componentes y exportaciones al paquete existente y acordar uso de tipos comunes de §1.3 | Max y Valqui; revisión de Gerardo | Seguir §4.6, mantener la exportación `tema` y coordinar cambios en `src/index.ts` y `package.json`. Declarar en el paquete las dependencias que utilice cada componente, sin depender solo de las instaladas en las apps. |

Esta preparación corresponde al prerrequisito de ICR-01. La base visual ya está definida por la guía común; siguen pendientes su conciliación documental y su comprobación técnica (DC-01).

#### 4.5.2. Orden para integrar el reparto

| Fase | Elementos a implementar y verificar | Dependencia |
|---|---|---|
| 0 | Configuración, tema, tokens, proveedores y herramientas | Preparación de §4.5.1. |
| 1 | CR-01, CR-02, CR-09, CR-10, CR-11 y CR-15 | Fase 0. |
| 2 | CR-03, CR-05, CR-06, CR-08, CR-12, CR-13, CR-14 y CR-20 | Elementos de fase 1 que declara cada componente en el catálogo. |
| 3 | CR-04, CR-07, CR-16, CR-17, CR-18 y CR-19 | Dependencias de las fases anteriores; políticas y contrato aplicables para integración real. |

Las fases complementan los incrementos ICR/TCR de §4.1; no sustituyen sus criterios ni exigen esperar a todos los componentes de una fase para comenzar otro cuyos prerrequisitos ya estén integrados. Cada TCR que involucre varios integrantes se descompone en tareas por `CR-NN`, manteniendo la cobertura de sus criterios. Los datos simulados permiten verificar componentes aislados; los pendientes del contrato siguen bloqueando la integración real afectada.

Para el primer listado de F-04, Gerardo prepara en paralelo sus documentos `spec`, UI, plan y tareas, y coordina la disponibilidad de CR-01/02/03/05/06/07/08/09/10. CR-12/15 intervienen al integrar las confirmaciones y sus resultados; CR-18/19 corresponden al detalle de incidencia. No es necesario terminar los 20 elementos para implementar el listado.

#### 4.5.3. Entrega de cada responsable

- Implementar el `CR-NN` contra las propiedades, eventos, estados y criterios definidos, manteniendo sus identificadores.
- Incluir comprobaciones de sus criterios `CCR-NN-XX`, teclado, errores y responsive aplicables; documentar los límites de cualquier simulación.
- Reutilizar el tema y los controles Mantine. Si falta una propiedad o surge otra responsabilidad compartida, actualizar primero la especificación afectada y revisar consumidores.
- Entregar un PR del frontend con componentes, pruebas y evidencia reproducible; indicar qué CR quedan disponibles y qué dependencias faltan. Los cambios de especificación se enlazan desde un PR del repositorio de documentación.
- El revisor comprueba el resultado y sus consumidores; el responsable actualiza la trazabilidad con los commits y resultados reales. Ninguna asignación de esta tabla cuenta como implementación completada.

### 4.6. Ubicación en el frontend existente

El checkout actualizado usa workspaces npm. Los componentes de este catálogo se implementan en **`G2-Despacho-Frontend/packages/componentes-compartidos/src/`**; las dos aplicaciones los consumen mediante el paquete **`@despacho/componentes-compartidos`**. No crear una biblioteca distinta dentro de cada app ni una tercera aplicación para los componentes.

Estructura de destino propuesta dentro de las carpetas actuales; las subcarpetas de componentes todavía no existen en la revisión `d2bc27d`:

```text
G2-Despacho-Frontend/
├── packages/
│   ├── componentes-compartidos/
│   │   ├── package.json                 # Existe; define el nombre y exportaciones del paquete
│   │   └── src/
│   │       ├── index.ts                 # Existe; exporta tema y exportará componentes/patrones
│   │       ├── tokens.css               # Existe; completar según el diseño
│   │       ├── layout/                  # CR-03, CR-04, CR-05, CR-13
│   │       ├── formularios/             # CR-01, CR-02, CR-06, CR-12, CR-17
│   │       ├── tablas/                  # CR-07
│   │       ├── feedback/                # CR-08, CR-14, CR-15
│   │       └── dominio/                 # CR-09, CR-10, CR-11, CR-16, CR-18, CR-19, CR-20
│   ├── tipos-compartidos/src/index.ts   # Existe; tipos transversales entre capas/apps
│   └── cliente-api/src/index.ts         # Existe; cliente y utilidades de comunicación
└── apps/
    ├── despacho-administrativo/src/
    │   └── features/entregas-fallidas/   # Previsto: páginas, formularios y contenedores propios de F-04
    └── despacho-repartidor/src/         # Existe; páginas y contenedores de F-03
```

- Un componente propio puede tener juntos `NombreComponente.tsx`, `NombreComponente.module.css` si necesita CSS, y sus pruebas al configurar las herramientas. Los patrones CR-01/02 y el adaptador CR-15 no requieren un archivo TSX por obligación.
- `src/index.ts` es la entrada pública existente. Al implementar un componente, agregar su exportación manteniendo `tema`; no crear importaciones desde una app hacia archivos internos de la otra. La exportación de tipos se define según su uso: tipos exclusivos de UI pueden permanecer en este paquete; los transversales entre aplicaciones o capas pueden vivir en `tipos-compartidos`.
- Los contenedores de cada aplicación consultan mediante `cliente-api`, resuelven permisos y transforman datos al modelo de UI. Pasan datos y callbacks a los componentes compartidos, que no dependen de la sesión ni de rutas internas de una app.
- Las llamadas al API, la carga autorizada de imágenes y las decisiones de negocio permanecen en sus adaptadores o contenedores. El paquete compartido aporta la visualización, interacción y eventos definidos en cada CR.
- Ambas apps ya consumen el paquete. Ejemplo de una importación **futura, después de implementar y exportar** CR-12: `import { ModalConfirmacion } from '@despacho/componentes-compartidos'`. Actualmente `src/index.ts` exporta el tema, no los 20 componentes.
- Antes de integrar un cambio compartido, verificar ambas aplicaciones con los scripts existentes `npm run typecheck` y `npm run build`, además de las pruebas del CR cuando estén configuradas. No afirmar que estas comprobaciones se han ejecutado por registrar esta guía.

## 5. Decisiones y evolución

### 5.1. Diferencias detectadas y decisiones pendientes

Los responsables siguientes son los roles de referencia del proyecto, no asignaciones nuevas en un gestor de tareas. Estos puntos no impiden revisar la especificación ni implementar componentes aislados con datos de prueba; los bloqueos indicados corresponden al incremento real afectado.

| ID | Hallazgo o decisión pendiente | Tratamiento de este documento | Responsable de referencia | Bloquea |
|---|---|---|---|---|
| DC-01 | `stack-frontend.md` aún propone React 18, Tailwind y react-hot-toast; el frontend `d2bc27d` ya declara React 19.2 y Mantine 9.6.2, tiene lockfile y contiene un tema y tokens iniciales compartidos. | Mantener el acuerdo común de Mantine sin Tailwind. Actualizar la documentación del stack, verificar la base existente, completar tema/tokens y configurar pruebas; la inicialización no demuestra cumplimiento de los CR ni integración real. | Max y Rhamses, según §4.5.1 | Conciliación documental y verificación de la base para ICR-01; no requiere crear de nuevo el proyecto. |
| DC-02 | Las guías UI agrupan registro, jornadas y monitoreo en F-05; el índice los separa en F-05/F-06. | Mapear consumidores según el índice y conservar enlaces actuales; ajustar nombres de guías y futuras atómicas F-06 al preparar sus trabajos. | Responsables de F-05/F-06 y UI | Trazabilidad definitiva de planes F-06; no bloquea componentes visuales. |
| DC-03 | Formatos, máximo de archivo, compresión y EXIF siguen pendientes en F-03. La lectura temporal está definida en Operación §3.4 y ES-F03-08, con integración real pendiente. | CR-17 recibe política de carga explícita; CR-18 consume §3.4. Completar la política y verificar los servicios, sin tamaños ni procesamiento inventados. | Max, Arquitectura y Backend | Aceptación real de captura, carga y acceso a evidencia; las pruebas simuladas no la cierran. Referencia: [Operación](../integraciones/api-contract-operacion-reparto.md#34-autorizar-la-lectura-de-evidencia). |
| DC-04 | Las tablas de endpoints no detallan todos los parámetros/metadatos de paginación, orden y filtros, ni todos los DTO de historial y métricas necesarias para las tarjetas. | Modelos de presentación controlados; concretar solicitudes y respuestas en el contrato del proveedor antes de integrar. No convertir estos modelos en contratos HTTP implícitos. | Responsables funcionales, Frontend y Backend | Integración de listados, historial, indicadores y selección con capacidad; no sus pruebas aisladas. |
| DC-05 | Algunas atómicas F-03 todavía exigen rol global `REPARTIDOR` o un identificador de repartidor en el token. Contrato Común §3.3, Operación §3: perfil local enlazado al `sub`, activo y propietario. | Shell y controles reciben contexto autorizado; no exigir ese rol global ni tratar `jwt-decode` como autorización. Alinear las atómicas antes de cerrar acceso e integración. | Responsables F-03/F-05 y Backend | Integración de sesión y autorización de campo. Referencia: [Convenciones e integración externa](../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio), [Operación](../integraciones/api-contract-operacion-reparto.md#3-api-de-f-03-operación-del-repartidor). |
| DC-06 | Instantes UTC y fechas civiles requieren reglas por flujo. Reprogramación quedó concretada en ES-F04-04 y Gestión §5.2.2: «hoy» del servidor en `America/Lima`, fecha civil sin conversión a UTC y referencia de UI desde `consultadoEn`. | Aplicar esa decisión a F-04 y comprobar medianoche/zona del navegador; verificar los otros flujos cuando se preparen. La definición documental no acredita su implementación. | Responsables funcionales y Backend/Frontend | Verificación real de fechas y alineación de los flujos restantes; la regla de reprogramación ya está definida. |
| DC-07 | Algunos wireframes/guías de alta fidelidad antiguas difieren de `SYSTEM-DESIGN.md`: opacidad de filas, checkbox para sello, colores de recepción o rangos tarifarios futuros. | Referenciar el sistema de diseño para apariencia y la atómica/contrato para reglas. Sello con respuesta explícita; filas sin opacidad global; no implementar rangos adicionales del documento de pendientes. | Max y responsables funcionales | Revisar la UI de cada incremento antes de aceptarlo; no copiar fragmentos antiguos sin revisión. |

### 5.2. Mantenimiento y condición de aceptación

- Mantener estables `CR-NN` y `CCR-NN-XX`. Si cambia una propiedad, un evento, un valor por defecto o una regla de estado, actualizar este archivo y revisar consumidores, planes, pruebas y evidencia.
- Registrar en cada plan el commit de esta especificación y del diseño utilizados; al actualizar, identificar qué criterios necesitan volverse a comprobar.
- Agregar un componente compartido cuando otra UI requiera la misma responsabilidad; justificar su reutilización y dependencias. Si es específico, mantenerlo en su funcionalidad.
- Antes de declarar implementado un `CR-NN`, verificar sus criterios, reglas transversales y consumidores afectados. La aceptación visual o una captura no sustituyen la integración funcional.
- La revisión de este borrador, la resolución de decisiones y el cierre de tareas quedan pendientes. No se generan aprobaciones ni resultados ficticios.

## 6. Referencias

1. [SYSTEM-DESIGN.md](./SYSTEM-DESIGN.md), versión 1.0: §§4–8 (tokens y fundamentos), §§11–13 (controles y patrones), §§15–18 (base técnica, estados, accesibilidad y responsive), §§20–24 (aplicación por pantalla).
2. UI actuales: [F-01](./funcionalidades/f-01.md), [F-02](./funcionalidades/f-02.md), [F-03](./funcionalidades/f-03.md), [F-04](./funcionalidades/f-04.md), [F-05/F-06](./funcionalidades/f-05.md).
3. [Stack frontend](../arquitectura/stack-frontend.md): propuesta anterior de dependencias; diferencias registradas en DC-01.
4. [Convenciones e integraciones externas](../integraciones/api-contract.md), §§3, 8 y 9: errores, permisos, Seguridad e idempotencia. [Gestión](../integraciones/api-contract-gestion-despachos.md), §§3–6: zonas, programación, catálogo, incidencias y transiciones internas. [Operación](../integraciones/api-contract-operacion-reparto.md), §§3–5: repartidor, evidencia, flota, jornadas y capacidad interna.
5. [Índice de funcionalidades](../funcionalidades/funcionalidad.md), [especificaciones atómicas](../especificaciones/) y [pendientes](../funcionalidades/pendiente.md).
6. [Estados del despacho](../arquitectura/diagrama-estados-despacho.md) y [F-06: disponibilidad y capacidad diaria](../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md).
7. [Plantilla de componentes](../plantillas/sdd/componentes-react.md), [flujo SDD](../plantillas/sdd/README.md), [plantilla UI](../plantillas/sdd/especificacion/ui.md), [plan](../plantillas/sdd/especificacion/plan.md), [tareas](../plantillas/sdd/especificacion/tasks.md), [evidencia](../plantillas/sdd/especificacion/evidence.md) y diapositivas del curso «SDD y los componentes React» / «SDD: el contrato primero», compartidas por Gerardo en la conversación; sin enlace estable al material del curso.
