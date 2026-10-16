# Plan de ES-F04-01: Consultar entregas fallidas

**Responsable:** Gerardo.

**Estado:** Listado HTTP y catálogo del Gestor implementados y verificados con dependencias de prueba. Cierre backend pendiente de fuentes compartidas; frontend pendiente.

**UI:** Aplica; página administrativa `/entregas-fallidas`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-11 | CA-01 a CA-05 conservados; revisión acordada en `1f556c0`. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-06 | Misma revisión documental que este plan. |
| Contrato | [API](../../integraciones/api-contract-gestion-despachos.md), Común §3.3, Común §3.5, Gestión §4, Gestión §5.1, Operación §5.4 | `4bad49d`; catálogo, parámetros, respuesta y lectura operativa documentados. Referencia: [Convenciones e integración externa](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio), [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias). |
| Componentes y diseño | [Componentes React](../../disenio/componentes-react.md), §§4.5–4.6; [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md), §23 | Contratos compartidos existentes; listado alineado en esta actualización. |
| Arquitectura y datos | [Contenedores](../../arquitectura/c4-contenedores.md), §3; [modelo de datos](../../arquitectura/modelo-datos.md), §§1, 3.3 y 3.4 | `4bad49d`; referencia a última incidencia y fuente operativa definidas. |
| Base de código | Backend `af13989`; frontend `d2bc27d` | Inicialización de aplicaciones; sin endpoint de consulta ni página funcional de F-04. |

La revisión concreta el comportamiento y el contrato correspondiente de esta consulta. Los avances de implementación se registran en §5 y en la evidencia; las dependencias compartidas y los componentes siguen pendientes. La verificación documental no acredita criterios de comportamiento ni disponibilidad de dependencias [cite: 1, 2].

## 2. Estrategia y responsabilidades

La página consume una consulta autorizada a través del Gateway. Gestión obtiene sus datos locales y la información acordada con Operación, aplica la restricción `FALLIDO`, filtros, orden y paginación, y devuelve únicamente el resumen permitido. El contenedor frontend adapta ese resultado a componentes visuales controlados.

| Área | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Página, filtros, consulta y adaptación del resultado. | `apps/despacho-administrativo/src/features/entregas-fallidas/`; `PaginaEntregasFallidas.tsx` y adaptador de consulta. |
| Componentes compartidos | Presentación e interacción sin HTTP ni acceso a tokens. | `packages/componentes-compartidos/src/`; CR-01/02/03/05/06/07/08/09/10. |
| Cliente de API | Petición y tratamiento del formato de errores vigente. | Paquete existente `packages/cliente-api`; tipos de transporte conforme a Gestión §5.1. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01). |
| Gateway | Enrutamiento de la consulta y propagación de identidad/correlación. | `api-gateway`; configuración base pendiente de habilitar y comprobar. |
| Gestión de Despachos | Autorización, caso de uso y persistencia de consulta. | Funcionalidad propuesta `incidencias/`, bajo el paquete base existente, con `api`, `application`, `domain` e `infrastructure` según necesidad. |
| Operación de Reparto y Flota | Datos propios de repartidor y jornada mediante lectura por lotes. | Adaptador de salida de Gestión para Operación §5.4; implementación pendiente en T-06. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias). |

Los nombres de clases y subpaquetes son decisiones técnicas propuestas. No se crean módulos desplegables nuevos ni se comparten entidades JPA entre servicios.

## 3. Frontend y componentes React

- Verificar primero tema, proveedores, dependencias y herramientas de pruebas según §4.5.1 del documento compartido.
- Gerardo implementará CR-08 EstadoVista como trabajo posterior y lo verificará contra CCR-08-01. Coordinar los demás CR con sus responsables documentados; la preparación de esta carpeta no los declara disponibles.
- CR-12/15 corresponden a confirmaciones y sus resultados; CR-18/19 al detalle. No son prerrequisitos de la consulta aislada.
- El contenedor mantiene filtros, página y estado de consulta, sincroniza la URL y descarta respuestas obsoletas. Los cambios de filtro reinician la página.
- Usar fixtures identificados para los estados de UI, indicadores 7/5/2, múltiples incidencias, `NO_INTENTADO` con cero/un fallo previo y jornada desconocida. Deben ser compatibles con el contrato documentado, sin presentarlos como servicios reales ni pruebas del filtrado del backend.
- Implementar el adaptador de HTTP contra Gestión §5.1 y sustituir los fixtures en el recorrido real. Las tarjetas respetan motivo/fechas e ignoran grupo/página; un valor desconocido se muestra no disponible y la selección de atrasados requiere una consulta completa. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01).
- La navegación al detalle y la apertura de recepción se enlazan con ES-F04-02/03 cuando existan; registrar esa disponibilidad por separado del alcance de consulta.

## 4. Backend, persistencia e integraciones

- Entrada: `GET /api/v1/despachos/fallidos`. Autorizar el JWT humano y exigir `GESTOR_DESPACHO`; el cliente no sustituye esta comprobación.
- Caso de uso: seleccionar una incidencia por despacho `FALLIDO`, sin filtro implícito de fechas; aplicar motivo/fechas, calcular indicadores, filtrar grupo, ordenar y paginar según Gestión §5.1. Recibidos primero y, en cada grupo, incidencia más antigua primero; desempate por identificador. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01).
- Datos locales: despachos, intentos, motivos, recepción, anulación y política de intentos. Usar `ultima_incidencia_id` para no mezclar jornadas, recepciones ni evidencia de distintas salidas. Contadores e identificador de incidencia son independientes.
- Migración: revisar el esquema existente y su forma de gestión con Arquitectura; crear migraciones Flyway solo para cambios necesarios. No asumir que las tablas o migraciones ya están disponibles por aparecer en el modelo.
- Integraciones: implementar la lectura por lotes de Operación §5.4. Consultar las jornadas deduplicadas de todas las incidencias pendientes de la base para que filtro/total de atrasados sean correctos antes de paginar; los nombres se consultan para la página. No acceder a tablas de Operación ni hacer una llamada por fila. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias).
- Degradación: una jornada no confirmada es `DESCONOCIDA`, no activa. En consulta normal, conservar filas y métricas locales y devolver el total de atrasados desconocido; la selección de solo atrasados devuelve el error de dependencia cuando no puede calcularse completa. Un nombre ausente conserva su identificador y no bloquea filas.
- Retorno atrasado: jornada cerrada confirmada y recepción pendiente. No inferirlo solo a partir de la fecha o del reloj del frontend.
- Fechas: instantes UTC y días de filtro inclusivos en `America/Lima`, conforme a Gestión §5.1; se admiten límites abiertos o ausencia de rango. La consulta se basa en la jornada de la incidencia, no en la actual del repartidor. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01).
- Efectos secundarios: la consulta no crea intentos, confirma recepciones, libera capacidad ni emite eventos de negocio. No requiere una clave de idempotencia de comando.
- Errores: aplicar Común §3.5 y los códigos de Gestión §5.1. Separar `200` sin coincidencias, `200` con información operativa desconocida, `503` por lectura local no disponible o atrasados no calculables y `500` por datos canónicos incoherentes. El contrato reutiliza los códigos de §5.3 para la indisponibilidad e inconsistencia, sin exponer SQL ni detalles internos. Referencia: [Convenciones e integración externa](../../integraciones/api-contract.md#35-errores), [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01).

## 5. Orden de implementación

El 16/10/2026 Gerardo prioriza backend y mantiene frontend pendiente cuando dependa de componentes de otros integrantes. Se inicia una parte independiente de I-02/T-06: puerto `LectorDatosOperativos`, modelo de lectura y adaptador `OperacionIncidenciasHttp`, bajo `incidencias/` de Gestión. Base `origin/develop` `bad76eb`; implementación `49d40ff`. El adaptador se verifica con HTTP simulado en EV-06; no se registra todavía como bean de producción ni incorpora credenciales o configuración de red supuestas. Su ensamblaje, persistencia y proveedor real siguen pendientes [cite: 1, 2].

La revisión del esquema encuentra únicamente V1 de F-01. La base de despachos/intentos y sus escritores deben coordinarse con F-02/F-03 y Arquitectura antes de añadir migraciones; este incremento no crea tablas paralelas ni implementa el servicio proveedor de otros integrantes. No cambia contratos ni requisitos de la consulta.

Segundo avance de T-06 del 16/10/2026: backend `df4590a` incorpora `LectorIncidenciasLocales`, `IncidenciaListadoLocal` e `IncidenciasLocalesJdbc`. El lector usa una sola sentencia parametrizada sobre las tablas canónicas de Gestión y lee la política de intentos en esa misma instantánea; conserva toda la base sin aplicar recepción ni paginación. Los límites de día se convierten desde `America/Lima` a instantes; motivo inactivo no se excluye. Se verifica con PostgreSQL 17 y un esquema mínimo únicamente en `src/test/resources/incidencias/`, no como migración de producción. La referencia vigente debe pertenecer al mismo despacho y a un resultado fallido; las incoherencias encontradas o una política inválida fallan explícitamente. Las migraciones/escritores compartidos, el caso de uso y el endpoint siguen pendientes. EV-07 conserva resultados y límites [cite: 1, 2].

Tercer avance del 16/10/2026, backend `a65ed9f`: se inicia la parte de T-07 que puede verificarse independientemente de las fuentes reales pendientes. `ConsultarEntregasFallidas` compone los puertos locales y de Operación con un reloj inyectado. `FiltrosConsultaFallidos` representa filtros ya tipados; `CatalogoMotivosFallo`, implementado sobre el catálogo canónico por el adaptador JDBC existente, valida el código exacto sin excluir inactivos. `PaginaEntregasFallidas` conserva los campos del listado. Se calculan indicadores antes del grupo/página, se deduplican jornadas de toda la base pendiente y se piden nombres solo para la página. La lectura de jornadas pendiente no se sustituye al enriquecer esa página; una ausencia mantiene desconocido el total de atrasados y bloquea solo su selección explícita con el error acordado. EV-08 verifica seis pruebas del caso de uso con dobles y la ampliación del catálogo con PostgreSQL. Siguen pendientes controlador, parámetros HTTP crudos, permisos, ensamblaje de ejecución y fuentes/migraciones reales; el caso de uso no se registra todavía como bean de producción [cite: 1, 2].

Cuarto avance del 16/10/2026, backend `6ffa58c`: `ControladorEntregasFallidas` y `ParametrosConsultaFallidos` exponen la consulta con validación estricta y seguridad previa a cualquier lectura. `ConfiguracionConsultaFallidos` registra los adaptadores y el caso de uso fuera de `integracion-local`, con origen de Operación y JWT técnico suministrados al proceso, conexión de un segundo y lectura de dos segundos, sin redirecciones. La obtención y renovación reales del JWT siguen pendientes. Una excepción específica de datos incoherentes evita que la traducción de excepciones JDBC los confunda con indisponibilidad. EV-09 comprueba cinco pruebas HTTP con PostgreSQL y Operación simulada y una prueba del Gateway con destino simulado; la regresión suma 61 pruebas aprobadas. No se añaden migraciones ni se implementan proveedores de otros integrantes [cite: 1, 2].

Por indicación de Gerardo se completa primero el código de nuestra rama; la integración de los cambios de `develop` del backend y `main` de Specs se deja para el final. La revisión del catálogo detecta además que su ruta actual del Gateway apunta a Operación aunque Gestión §4 lo define como proveedor: coordinar API, autorización de repartidores y ruta antes de la demo, sin crear otro catálogo. El frontend permanece pendiente y se avisará antes de iniciarlo.

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Componentes requeridos disponibles y página aislada con fixtures identificados. | Base frontend y CR de §3; no necesita una API real. | CUI-01 a CUI-06, solo presentación/interacción. |
| I-02 | Fuentes y consulta backend implementadas y probadas contra el contrato definido. | T-05 documental; implementación de DT-01/02 y bases de DT-03. | CA-01 a CA-11. |
| I-03 | Página conectada y verificación del recorrido real. | I-01 e I-02. | CA-01 a CA-11 y CUI-01 a CUI-06. |

La definición contractual y de fuentes puede prepararse mientras se desarrolla I-01. Solo el incremento afectado queda detenido por cada pendiente.

## 6. Estrategia de verificación

Actualización del 16/10/2026, backend `536a0f3`: se completa la API de catálogo para el Gestor, leyendo la tabla canónica, y su ruta del Gateway se mueve a Gestión. EV-10 añade dos pruebas HTTP prioritarias y amplía una del Gateway; ejecuta una selección de 15 pruebas, sin repetir toda la suite, por la prioridad de tiempo indicada por Gerardo. El acceso de repartidores al catálogo conserva su requisito de perfil activo y queda pendiente de su integración de F-03/Operación; no se inventan roles ni consultas a bases ajenas.

Al finalizar el código se consultan los remotos: `origin/develop` continúa en `bad76eb` y no contiene migraciones de despachos/incidencias ni Operación §5.4. Specs `origin/main` `10d6b83` se integra en `83c0b4b`, sin conflictos. La lectura conjunta sobre fuentes reales no puede verificarse todavía; responsables de dependencias: F-02/F-03 y Arquitectura para las migraciones/escritores, Operación para su proveedor y credencial. No se añaden esquemas de producción alternativos a sus cambios en curso.

| Criterio | Comprobación | Nivel y datos |
|---|---|---|
| CA-01 | Excluir otros estados; campos e indicadores correctos; página sin duplicados. | Integración PostgreSQL del backend y recorrido UI; varios estados y más de una página. |
| CA-02 | Combinar filtros, probar límites de fechas, orden estable y cambio de página. | Integración con contrato cerrado; fixtures de UI para interacción. |
| CA-03 | Diferenciar vacío, ausencia de coincidencias y error. | Backend con cero fallidos/coincidencias; UI con fixtures y API real. |
| CA-04 | Rechazar usuario con otro rol sin datos y retirar resultados previos en UI. | Pruebas de seguridad del endpoint y de interacción. |
| CA-05 | Matriz de jornada activa/cerrada y recepción pendiente/confirmada. | Regla backend y adaptador; después fuente real de Operación. |
| CA-06 | Dos fallos del mismo despacho sin duplicados ni recepción heredada. | Integración PostgreSQL con referencia de incidencia vigente. |
| CA-07 | Orden fijo, empate de fechas y varias páginas. | Consulta backend y UI, sin mutaciones concurrentes en el caso de estabilidad. |
| CA-08 | Totales de base 7/5/2, grupo seleccionado y página parcial. | Integración y UI; cambiar motivo/fechas y alternar tarjetas. |
| CA-09 | `NO_INTENTADO` con contador cero y uno. | Consulta e interacción; máximo de dos en los datos de prueba. |
| CA-10 | Jornada desconocida, lote fallido, nombre ausente y petición de solo atrasados. | Dobles identificados y prueba contra Operación; `200` degradado o `503` conforme al contrato. |
| CA-11 | Filtros inválidos y combinaciones incompatibles. | Integración de parámetros y errores normalizados; límites de fechas de Lima. |
| CUI-01 a CUI-06 | Contenido, controles, recuperaciones, foco, nombres accesibles y responsive. | Pruebas de interacción y recorrido manual reproducible. |

Comandos previstos: desde el frontend, `npm run typecheck` y `npm run build`; desde Gestión, `./mvnw.cmd test` en PowerShell. Las herramientas y el comando de pruebas frontend se definirán al habilitarlas; no existe actualmente un script de pruebas. Las pruebas con Testcontainers requieren Docker. Los resultados y la distinción entre dobles y servicios reales se anotarán en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Punto por resolver | Fuente y responsable de coordinación | Bloquea |
|---|---|---|---|
| DT-01 | Listado, validación de códigos y catálogo del Gestor implementados; ruta Gateway a Gestión corregida. Pendiente perfil activo para el consumidor repartidor y migraciones compartidas. | Gerardo con F-03/Operación y Arquitectura. | Verificación real de fuentes y filtros en T-06/07/08; el consumidor de campo se completa con F-03. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo). |
| DT-02 | Consumidor, ensamblaje y degradación verificados con HTTP simulado en EV-06/09. Pendientes proveedor real y obtención/renovación de la credencial técnica. | Gerardo con Operación y Arquitectura; modelo de datos y T-06. | CA-01/05/06/08/10 e integración real de I-02/03. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias), [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01). |
| DT-03 | Esquema/migraciones necesarios y base compartida de JWT, errores, conexión de datos y rutas del Gateway. | Inicialización actual del backend y modelo. Gerardo coordina con Arquitectura y DevOps. | Ejecución real de I-02/03. |
| DT-04 | Disponibilidad y verificación de componentes, tema y herramientas de pruebas. | Componentes React §§4.5–4.6. Gerardo para CR-08; coordinación con los responsables del resto. | Composición y aceptación de I-01 según sus dependencias. |

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas del incremento están revisadas y sus pendientes bloqueantes resueltos.
- [ ] Los componentes requeridos están verificados antes de componer la pantalla consumidora.
- [ ] Las tareas cubren todos los criterios y tienen una comprobación concreta.
- [ ] La consulta respeta el contrato correspondiente y la propiedad de datos de cada servicio.
- [ ] Todos los criterios del alcance cuentan con evidencia, distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md#5-api-de-f-04-entregas-fallidas), [modelo de datos](../../arquitectura/modelo-datos.md) y [arquitectura de contenedores](../../arquitectura/c4-contenedores.md).
3. [Componentes React](../../disenio/componentes-react.md), [sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [flujo SDD](../../plantillas/sdd/README.md).
