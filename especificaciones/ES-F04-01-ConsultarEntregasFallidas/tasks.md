# Tareas de ES-F04-01: Consultar entregas fallidas

**Responsable de coordinación:** Gerardo.

**Estado:** Implementación backend parcial; T-06 y T-07 en curso.

**Plan de origen:** [plan.md](./plan.md), misma revisión documental que esta carpeta.

La revisión del 15/10/2026 concreta el contrato y actualiza las tareas de implementación. Solo T-05 se completa documentalmente; los componentes, endpoints y criterios funcionales siguen pendientes. Los responsables compartidos son los de [componentes React](../../disenio/componentes-react.md), §4.5; esta lista no crea issues ni acredita implementación.

El 16/10/2026 se inicia backend por indicación de Gerardo, mientras se preparan los componentes de otros integrantes. El primer avance de T-06 implementa y prueba únicamente el consumidor de Operación; no completa persistencia, proveedor, ensamblaje de ejecución ni endpoint. Ver EV-06 de [evidence.md](./evidence.md).

El segundo avance de T-06 implementa la lectura local JDBC y la comprueba con cuatro pruebas sobre PostgreSQL aislado y esquema exclusivo de pruebas. No sustituye las migraciones compartidas de producción ni completa el listado. Ver EV-07 de [evidence.md](./evidence.md).

El tercer avance inicia la parte independiente de T-07: caso de uso, filtros tipados, indicadores, orden y paginación, con lectores simulados y catálogo JDBC. No requiere componentes React. Las dependencias reales de T-06 y la entrada HTTP permanecen pendientes; EV-08 de [evidence.md](./evidence.md) distingue sus límites.

El cuarto avance, backend `6ffa58c`, expone el listado HTTP con autorización y validación estricta, registra los adaptadores en Spring y verifica cinco pruebas HTTP y una del Gateway. EV-09 distingue PostgreSQL temporal, esquema de prueba, decodificador JWT simulado y proveedor HTTP simulado. Gerardo acuerda completar primero el código de nuestra rama y traer después los cambios compartidos de `develop` del backend y `main` de Specs; este avance no integra esas ramas ni inicia frontend.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Base frontend y herramientas de pruebas verificadas. | Preparación compartida | DT-04; coordinación con Max/Rhamses. | CUI-01 a CUI-06 como soporte. | Pendiente |
| T-02 | CR-08 EstadoVista implementado y verificado. | Componente compartido | T-01 y patrones CR-01 necesarios. | CCR-08-01; soporte de CA-03/04 y CUI-03/04. | Pendiente |
| T-03 | Resto de componentes del listado disponibles y verificados. | Componentes compartidos | T-01 y dependencias de cada CR; CR-07 depende de T-02. | CUI-01/02/05/06. | Pendiente |
| T-04 | Página de consulta verificable con fixtures de presentación. | Frontend, I-01 | T-02 y T-03. | CUI-01 a CUI-06, sin acreditar backend real. | Pendiente |
| T-05 | Contrato documentado y comprobado, sin acreditar implementación. | Contrato | DT-01/02 definidos en API Gestión §4, Gestión §5.1, Operación §5.4. | CA-01 a CA-11; soporte de CUI-02/05. | Completada. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo), [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias). |
| T-06 | Persistencia y lectura operativa por lotes implementadas. | Datos e integración | T-05 y bases de DT-03. | CA-01/02/05/06/08/10. | En curso; lectores y ensamblaje verificados en EV-06 a EV-09; migraciones, catálogo y proveedor reales pendientes. |
| T-07 | Endpoint de consulta autorizado y probado. | Backend, I-02 | T-05, T-06 y base JWT/errores/rutas de DT-03. | CA-01 a CA-11. | En curso; caso de uso en EV-08 y entrada HTTP/ruta Gateway en EV-09; recorrido con dependencias reales pendiente. |
| T-08 | Página conectada a la consulta real. | Integración, I-03 | T-04, T-07 y Gateway accesible. | CA-01 a CA-11; CUI-01 a CUI-06. | Pendiente |
| T-09 | Cobertura, evidencia y revisión del alcance completadas. | Calidad | T-08 y dependencias reales disponibles. | Todos los criterios del alcance. | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Al iniciar una tarea cuya dependencia no esté disponible, registrar el bloqueo y su responsable. T-05 acredita únicamente definición documental y sus comprobaciones; T-06/07/08 verifican la implementación y comunicación reales.

## 2. Detalle de tareas

### T-01. Verificar la base compartida del frontend

- [ ] Implementada y verificada.

- Alcance: revisar tema, tokens, proveedores, dependencias y scripts existentes; coordinar herramientas de pruebas sin reinicializar el monorepositorio.
- Entradas: componentes React §4.5.1 y DT-04 del plan.
- Responsable: coordinación de Gerardo con Max y Rhamses según el reparto existente.
- Comprobación: ambas apps pasan `npm run typecheck` y `npm run build`; una prueba de interacción puede ejecutarse con el comando que se configure y documente.
- Cierre y evidencia: registrar herramientas, comandos y resultados reales; no acreditar componentes por la compilación de la base.

### T-02. Implementar CR-08 EstadoVista

- [ ] Implementada y verificada.

- Alcance: componentes de vacío, sin resultados, error, falta de permiso y carga según el contrato de CR-08; añadir sus exportaciones manteniendo `tema`.
- Ubicación: `packages/componentes-compartidos/src/feedback/` del frontend.
- Responsable: Gerardo; revisión propuesta de Max.
- Comprobación: CCR-08-01, acciones de recuperación con teclado, carga diferenciada de vacío y ausencia de datos protegidos. Usar fixtures identificados.
- Cierre y evidencia: enlazar commit/pruebas compartidas desde EV-02; no realizar llamadas HTTP dentro del componente.

### T-03. Coordinar y verificar los otros componentes requeridos

- [ ] Implementada y verificada.

- Alcance: confirmar CR-01/02/03/05/06/07/09/10 y sus dependencias, exportaciones y evidencia; enlazar los trabajos de sus responsables sin duplicar componentes.
- Responsable: Gerardo coordina con Valqui, Rhamses, Tarqui y Luis según §4.5 del documento compartido.
- Comprobación: los componentes se consumen desde el paquete compartido y sus criterios aplicables cuentan con pruebas; ambas aplicaciones siguen compilando.
- Cierre y evidencia: registrar componentes/revisiones disponibles y pendientes. CR-12/15/18/19 se reservan para sus flujos consumidores.

### T-04. Componer la página con fixtures

- [ ] Implementada y verificada.

- Alcance: crear la página en la funcionalidad de entregas fallidas; tabla, controles, indicadores, paginación y estados definidos en UI-01.
- Entradas: [ui.md](./ui.md), componentes verificados y fixtures de presentación que distingan todos los casos, incluido `NO_INTENTADO`.
- Comprobación: CUI-01 a CUI-06 con pruebas de interacción y recorrido responsive. Los filtros locales de demostración y los indicadores de prueba se identifican como simulados.
- Cierre y evidencia: documentar los límites de la simulación y los destinos ES-F04-02/03 aún no disponibles. No crear un contrato HTTP implícito a partir del fixture.

### T-05. Concretar el contrato correspondiente del listado

- [x] Definición documental completada y comprobada el 15/10/2026; implementación no acreditada.

- Alcance: API Gestión §4, Gestión §5.1, Operación §5.4: catálogo, filtros/límites, respuesta, paginación, métricas, orden, lectura operativa por lotes y errores; fuente inequívoca de la incidencia en el modelo. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo), [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias).
- Responsable: Gerardo con Backend/Frontend y Arquitectura.
- Comprobación: seis acuerdos del listado reflejados en criterios, contrato y UI; ejemplos JSON válidos, referencias locales y trazabilidad completas, sin contratos duplicados. No sustituye pruebas HTTP.
- Cierre y evidencia: contratos en `4bad49d`, reglas en `1f556c0` y comprobación documental EV-05 de [evidence.md](./evidence.md). Implementación y pruebas reales permanecen en T-06 a T-09.

### T-06. Preparar persistencia y fuentes de datos

- [ ] Implementada y verificada.

Avance parcial del 16/10/2026, backend `49d40ff`:

- [x] Revisar el esquema de `origin/develop` (`bad76eb`): existe V1 de F-01, aún no hay tablas de despachos/incidencias ni proveedor de Operación §5.4.
- [x] Implementar puerto y consumidor HTTP de Operación §5.4 con deduplicación, lotes de hasta 100 por arreglo y credencial técnica suministrada por el ensamblaje.
- [x] Verificar el consumidor con seis pruebas prioritarias: sin llamadas vacías/anónimas, lotes, respuesta válida, omisiones/incoherencias, fallos de comunicación y aislamiento entre lotes. Evidencia EV-06.
- [x] Implementar el puerto `LectorIncidenciasLocales`, la proyección `IncidenciaListadoLocal` y `IncidenciasLocalesJdbc`: una lectura de la base completa `FALLIDO`, incidencia por referencia/propiedad, motivo y límites inclusivos de fecha en Lima; backend `df4590a`.
- [x] Verificar el lector con cuatro pruebas PostgreSQL de prioridad: incidencia vigente sin herencia de recepción/evidencia, límites de Lima y motivos históricos, referencias inconsistentes y política configurable. Evidencia EV-07, con esquema exclusivo de pruebas.
- [ ] Coordinar con F-02/F-03 y Arquitectura las migraciones de despachos, motivos, incidencias y `ultima_incidencia_id`; verificar el lector sobre esas migraciones reales y sus escritores.
- [x] Ensamblar el cliente con URL interna configurable, conexión de un segundo, lectura de dos segundos y credencial técnica suministrada al proceso; verificar su uso con HTTP simulado en EV-09, backend `6ffa58c`.
- [ ] Comprobar el proveedor real de Operación y el suministro/renovación de credenciales vigentes con sus responsables. La variable de entorno no implementa esa obtención ni acredita permisos reales.
- [ ] Coordinar la API compartida del catálogo de Gestión §4 y su ruta: el Gateway actual aún dirige esa consulta a Operación. El lector de códigos no sustituye esa API ni su autorización de repartidores.
- [x] Componer los puertos en el caso de uso y verificar con dobles las jornadas de toda la base pendiente, nombres por página, indicadores y error de solo atrasados. EV-08; backend `a65ed9f`.
- [ ] Ensamblar esa composición con la persistencia compartida y Operación real, y verificar el recorrido por el Gateway en T-07/T-08.

- Alcance: revisar esquema/migraciones y crear la referencia `ultima_incidencia_id`; implementar la lectura por lotes de Operación (Operación §5.4) y su adaptador en Gestión, con jornadas históricas y nombres de repartidor, conforme a DT-02/03. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias).
- Responsable: Gerardo con Arquitectura y responsables de Operación; coordinar la base compartida con DevOps.
- Comprobación: varios estados y varias incidencias por despacho; jornadas activas/cerradas/desconocidas y nombres ausentes; lotes de más de 100 jornadas divididos sin llamadas por fila, totales antes de paginar y ninguna consulta cruzada de bases. Comprobar migraciones en una base aislada.
- Cierre y evidencia: registrar revisiones y decisiones de integración, disponibilidad de las dependencias y cualquier doble de prueba utilizado. EV-06 acredita el consumidor, EV-07 el lector con esquema de prueba y EV-09 su ensamblaje conjunto con HTTP simulado; T-06 conserva su casilla general pendiente.

### T-07. Implementar y probar la consulta backend

- [ ] Implementada y verificada.

Avance parcial del 16/10/2026, backend `a65ed9f`, evidencia EV-08:

- [x] Implementar `ConsultarEntregasFallidas` y `PaginaEntregasFallidas`: indicadores anteriores a grupo/página, recibidos primero, fecha e identificador como desempate, y páginas fuera de rango sin perder totales.
- [x] Implementar `FiltrosConsultaFallidos` y validar existencia de motivo en el catálogo canónico, incluidos inactivos. Sin modificar los contratos.
- [x] Verificar seis pruebas prioritarias del caso de uso con puertos simulados y ampliar la comprobación PostgreSQL del catálogo; regresión existente aprobada.
- [x] Implementar entrada HTTP, validación estricta de parámetros crudos, rechazo de parámetros repetidos/desconocidos y autorización humana previa a cualquier lectura. Cinco pruebas HTTP prioritarias en EV-09, backend `6ffa58c`.
- [x] Registrar el caso de uso y el cliente interno en Spring fuera de `integracion-local`, con URL y credencial técnica externas y tiempos de espera acotados. EV-09 verifica el Bearer técnico de prueba; su emisión/renovación real sigue en T-06.
- [x] Verificar el ensamblaje HTTP/JDBC, respuestas `200/400/401/403/500/503`, privacidad, nulabilidad y degradación con PostgreSQL temporal y proveedor HTTP simulado. EV-09; el esquema exclusivo de pruebas no acredita migraciones reales.
- [x] Comprobar la ruta existente del listado en Gateway, propagación de parámetros/Bearer, rechazo anónimo y bloqueo de rutas internas, contra un destino HTTP simulado. EV-09.
- [ ] Verificar el recorrido conjunto con Seguridad, Gateway, Gestión, Operación y migraciones/escritores acordados. Los dobles no completan este punto.

- Alcance: controlador, caso de uso, puertos y adaptadores mínimos dentro de la funcionalidad de incidencias de Gestión; ruta pública a través del Gateway.
- Entradas: contrato cerrado, datos de T-06, base de seguridad y errores disponible; reglas y verificaciones de [spec.md](./spec.md).
- Comprobación: `./mvnw.cmd test` desde Gestión; verificar CA-01 a CA-11 con PostgreSQL aislado, filtros inválidos, orden/empates, métricas 7/5/2, incidencia vigente, `NO_INTENTADO`, matriz de jornada desconocida y degradación. Probar rol diferente y token ausente/inválido.
- Cierre y evidencia: CA-01 a CA-11 cubiertos en backend, con límites de dobles explícitos y pruebas de contrato de Operación §5.4. La lectura no cambia datos de negocio ni genera eventos. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias).

### T-08. Conectar el frontend a la API real

- [ ] Implementada y verificada.

- Alcance: adaptar la respuesta contractual desde el cliente de API, conectar filtros/URL/paginación y gestionar errores y respuestas fuera de orden; retirar la fuente simulada del recorrido real.
- Dependencias: I-01 e I-02; autenticación humana y Gateway disponibles. Coordinar los destinos de detalle/recepción cuando estén implementados.
- Comprobación: filtros, tarjetas y URL coherentes; totales fuera de la página, orden estable, retorno del detalle, jornada desconocida, error de solo atrasados y permisos revocados; `npm run typecheck` y `npm run build` en ambas apps. No convertir `null` en cero.
- Cierre y evidencia: resultado real por Gateway enlazado; indicadores procedentes de la fuente acordada, sin totales fabricados desde una página parcial.

### T-09. Verificar y entregar la especificación

- [ ] Implementada y verificada.

- Alcance: ejecutar las comprobaciones de todos los criterios, completar [evidence.md](./evidence.md) y actualizar trazabilidad e índice cuando corresponda.
- Comprobación: registrar commits frontend/backend, entorno y dependencias; revisar teclado, móvil y ausencia de fotografías/comentarios en listado. La simulación aislada no sustituye la prueba real.
- Cierre: revisión funcional y técnica registrada; explicar cualquier destino o integración pendiente. Si queda un criterio obligatorio sin comprobar, el alcance permanece parcial.

## 3. Cobertura de criterios

| Criterio | Implementación | Verificación | Registro previsto |
|---|---|---|---|
| CA-01 | T-04, T-06, T-07, T-08 | T-07 y T-09 | EV-01, EV-04 |
| CA-02 | T-04 a T-08 según dependencias | T-07 y T-09 | EV-01, EV-04 |
| CA-03 | T-02, T-04, T-07, T-08 | T-07 y T-09 | EV-01 a EV-04 |
| CA-04 | T-02, T-04, T-07, T-08 | T-07 y T-09 | EV-01 a EV-04 |
| CA-05 | T-04, T-06, T-07, T-08 | T-07 y T-09 | EV-01, EV-03, EV-04 |
| CA-06 | T-04, T-06, T-07, T-08 | T-07 y T-09 | EV-01, EV-04 |
| CA-07 | T-04, T-07, T-08 | T-07 y T-09 | EV-01, EV-03, EV-04 |
| CA-08 | T-04, T-06, T-07, T-08 | T-07 y T-09 | EV-01, EV-03, EV-04 |
| CA-09 | T-04, T-07, T-08 | T-07 y T-09 | EV-01, EV-03, EV-04 |
| CA-10 | T-04, T-06, T-07, T-08 | T-07 y T-09 | EV-01, EV-03, EV-04 |
| CA-11 | T-04, T-07, T-08 | T-07 y T-09 | EV-01, EV-03, EV-04 |
| CUI-01 | T-03, T-04, T-08 | T-04 y T-09 | EV-03, EV-04 |
| CUI-02 | T-03, T-04, T-08 | T-04 y T-09 | EV-03, EV-04 |
| CUI-03 | T-02, T-04, T-08 | T-04 y T-09 | EV-02 a EV-04 |
| CUI-04 | T-02, T-04, T-08 | T-04 y T-09 | EV-02 a EV-04 |
| CUI-05 | T-03, T-04, T-08 | T-04 y T-09 | EV-03, EV-04 |
| CUI-06 | T-02, T-03, T-04, T-08 | T-04 y T-09 | EV-02 a EV-04 |

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están implementadas y verificadas.
- [ ] Los criterios tienen evidencia reproducible y las limitaciones están registradas.
- [ ] Los contratos, fuentes de datos y dependencias necesarios están resueltos.
- [ ] Los documentos e índice están actualizados y la revisión está enlazada.

## 5. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-11 [cite: 1].
2. [Plan](./plan.md), incrementos I-01 a I-03 y pendientes DT-01 a DT-04 [cite: 2].
3. [UI](./ui.md), criterios CUI-01 a CUI-06, y [evidencia](./evidence.md) [cite: 3].
