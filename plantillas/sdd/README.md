# Propuesta de plantillas y flujo SDD

**Estado:** Propuesta para revisión del equipo.

**Alcance:** Plantillas reutilizables para desarrollar cada especificación atómica con trazabilidad desde los requisitos hasta su verificación.

Esta propuesta toma como referencia las diapositivas del curso «SDD y los componentes React» y «SDD: el contrato primero», compartidas por Gerardo. Su secuencia es: especificación funcional, UI y contrato de API como entradas del plan; especificaciones de componentes React compartidos; tareas e implementación incremental con verificación de cada criterio. Los nombres de archivos y la organización de carpetas siguientes son una propuesta del equipo, no una exigencia literal de las diapositivas.

## 1. Organización propuesta

Las seis funcionalidades conservan su alcance general en `funcionalidades/`. Cada comportamiento atómico mantiene su identificador `ES-FXX-NN` y, al adoptar la propuesta, tendrá una carpeta propia:

```text
G2-Despacho-Specs/
├── funcionalidades/                         # Funcionalidades padre e índice
├── integraciones/
│   └── api-contract.md                      # Contrato vigente
├── arquitectura/                            # C4, estados y modelo de datos
├── disenio/
│   ├── SYSTEM-DESIGN.md                     # Referencia visual transversal
│   └── componentes-react.md                 # Documento futuro de componentes compartidos
├── especificaciones/
│   └── ES-FXX-NN-NombreEnPascalCase/         # Carpeta futura de una especificación
│       ├── spec.md                          # Comportamiento y criterios de aceptación
│       ├── ui.md                            # Solo si crea o modifica una interfaz
│       ├── plan.md                          # Diseño técnico y orden de implementación
│       ├── tasks.md                         # Trabajo incremental y verificable
│       └── evidence.md                      # Resultados reales y trazabilidad
└── plantillas/
    └── sdd/                                 # Plantillas de esta propuesta
        ├── README.md
        ├── componentes-react.md
        └── especificacion/
            ├── spec.md
            ├── ui.md
            ├── plan.md
            ├── tasks.md
            └── evidence.md
```

La estructura futura no se ha creado ni se han movido las especificaciones existentes. La sección 3.7 de [AGENTS.md](../../AGENTS.md) conserva la organización vigente de archivos sueltos; su adaptación y la actualización de enlaces e índices formarán parte de una adopción posterior [cite: 1].

## 2. Qué contiene cada archivo

| Archivo | Pregunta que responde | Aplicabilidad |
|---|---|---|
| [spec.md](./especificacion/spec.md) | ¿Qué comportamiento debe cumplirse y cómo se acepta? | Siempre. Un comportamiento atómico, con criterios identificables. |
| [ui.md](./especificacion/ui.md) | ¿Cómo lo utiliza una persona y qué ve en cada estado? | Cuando la especificación crea o modifica una interfaz. |
| [plan.md](./especificacion/plan.md) | ¿Cómo se implementará sobre los contratos y componentes acordados? | Siempre, antes de implementar. |
| [tasks.md](./especificacion/tasks.md) | ¿Qué incremento se implementa y verifica a continuación? | Siempre. Las tareas concretan el plan. |
| [evidence.md](./especificacion/evidence.md) | ¿Qué se implementó, qué se probó y dónde se puede comprobar? | Se inicia como pendiente y se completa con resultados reales. |
| [componentes-react.md](./componentes-react.md) | ¿Qué componentes se reutilizan y cuál es su comportamiento? | Compartido por las especificaciones con frontend. Se completa una vez y evoluciona cuando cambian los componentes. |

`ui.md` no se necesita para una API consumida por otro módulo, un webhook o un proceso interno sin interfaz propia. Registrar «UI: No aplica» y el motivo en `spec.md` y `plan.md`; retirar la copia de `ui.md`. Si una operación backend cambia lo que muestra una pantalla existente, sí se documenta ese impacto visual.

El documento de componentes React complementa [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md): el diseño visual define apariencia y pautas; la especificación de componentes define propósito, propiedades, eventos, estados y accesibilidad [cite: 2]. No necesita repetir todos los estilos ni obligar a compartir componentes exclusivos de una pantalla.

## 3. Contrato de API como referencia

El contrato vigente continúa siendo [integraciones/api-contract.md](../../integraciones/api-contract.md), conforme a la sección 5.3 de las reglas del repositorio [cite: 1, 3]. Esta propuesta no agrega un `api.md` ni otro contrato en cada carpeta.

En `spec.md` y `plan.md`, identificar las operaciones que se consumen o implementan y enlazar la sección exacta del contrato. Los campos, encabezados, scopes, respuestas y errores se definen allí. Antes de implementar una operación nueva o modificar una existente, actualizar y revisar el contrato central; luego ajustar las especificaciones que lo referencian.

Si posteriormente se aprueba separar los contratos por microservicio, habrá que actualizar esa regla y sustituir las referencias. La separación no forma parte de estas plantillas.

## 4. Flujo de trabajo

1. Consultar la funcionalidad padre, el contrato, la arquitectura y el modelo de datos. Resolver o registrar los puntos pendientes que afecten el incremento.
2. Redactar `spec.md`: un comportamiento, sus reglas y criterios `CA-NN`. Conservar los identificadores de criterios existentes si ya están usados en pruebas o tareas.
3. Si hay frontend, redactar `ui.md` y revisar los componentes React compartidos y el diseño visual. Proponer allí los componentes reutilizables que falten antes de implementar las pantallas consumidoras.
4. Revisar el contrato de API aplicable. Con un contrato definido, el frontend puede usar un mock mientras se construye el backend; identificarlo como simulado.
5. Redactar `plan.md` usando la especificación, la UI cuando aplique, el contrato y los componentes compartidos. Definir responsabilidades, persistencia, integraciones y verificación.
6. Descomponer el plan en `tasks.md`. Cada tarea indica criterios cubiertos, dependencias y una comprobación concreta. Implementar primero los componentes compartidos necesarios, luego los incrementos que los usan.
7. Implementar una tarea, verificarla y registrar el resultado en `evidence.md`. Si cambia una decisión funcional o contractual, actualizar sus documentos antes de continuar con el código afectado.
8. Revisar la cobertura de todos los criterios, enlazar commits y PR, y actualizar el índice de funcionalidades cuando corresponda. Completar una tarea no significa automáticamente completar la especificación.

La trazabilidad debe poder recorrerse en ambos sentidos: `CA-NN` → decisión del plan → `T-NN` → código/commit → prueba → `EV-NN`. Un resultado fallido también es evidencia y debe quedar identificado.

## 5. Cómo usar las plantillas

- Copiar los archivos de `especificacion/` a la carpeta de la especificación cuando el equipo adopte la organización. Reutilizar el contenido de la especificación existente como `spec.md`, en lugar de mantener dos versiones activas del mismo comportamiento.
- Reemplazar los marcadores `[por completar]` y adaptar las secciones al alcance. Marcar «No aplica» con una razón cuando corresponda.
- Corregir los enlaces al copiar: desde `especificaciones/ES-FXX-NN-Nombre/` los documentos generales se alcanzan con `../../`; entre sus cinco archivos se usan enlaces como `./spec.md`.
- Copiar la plantilla `componentes-react.md` a `disenio/componentes-react.md` al redactar la especificación compartida; ajustar sus enlaces a la nueva ubicación.
- Mantener identificadores estables de requisitos, criterios, tareas y evidencias. En referencias, combinar enlaces navegables con `[cite: N]` y registrar la revisión o commit cuando se requiera reproducibilidad.
- No marcar tareas como completadas ni pruebas como aprobadas al copiar la plantilla. `evidence.md` nace pendiente, sin capturas o resultados ficticios.
- Si se utiliza IA, proporcionar los documentos y sus revisiones como entrada de la tarea; registrar su uso y la revisión humana. Los prompts por sí solos no demuestran que los criterios se hayan cumplido.

## 6. Lista de revisión

- [ ] La especificación describe un solo comportamiento y enlaza su funcionalidad padre.
- [ ] Los criterios tienen condiciones y resultados observables.
- [ ] La aplicabilidad de UI está justificada; cuando aplica, cubre interacción, estados y accesibilidad.
- [ ] Los componentes reutilizables necesarios están especificados y sus tareas preceden a las pantallas consumidoras.
- [ ] El contrato aplicable está definido y referenciado, sin versiones duplicadas.
- [ ] El plan distingue frontend, backend, servicios propietarios y dependencias.
- [ ] Las tareas cubren todos los criterios y permiten verificación incremental.
- [ ] La evidencia distingue implementado, simulado, fallido y pendiente, con referencias comprobables.
- [ ] La adopción de carpetas actualiza las reglas, los enlaces y la trazabilidad del índice.

## 7. Referencias

1. [AGENTS.md](../../AGENTS.md), secciones 3.7, 4 y 5: organización, trazabilidad y contrato único.
2. [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md): referencia visual compartida.
3. [Contrato de API](../../integraciones/api-contract.md): operaciones y convenciones vigentes.
4. Diapositivas del curso compartidas en la conversación: «SDD y los componentes React» y «SDD: el contrato primero». Pendiente incorporar un enlace estable al material del curso si está disponible.
