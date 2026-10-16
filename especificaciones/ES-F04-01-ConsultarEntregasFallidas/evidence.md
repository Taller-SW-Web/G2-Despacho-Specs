# Evidencia de ES-F04-01: Consultar entregas fallidas

**Estado:** Implementación backend parcial en T-06/T-07; lectores y caso de uso con indicadores/paginación verificados por partes. Endpoint y verificación funcional pendientes.

**Responsable de verificación:** Gerardo.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), incorporados en la misma revisión de esta carpeta.
- Origen de la especificación y fuentes generales: revisión `8586a78` del repositorio de especificaciones.
- Base de código consultada: backend `af13989` y frontend `d2bc27d`; no constituyen una implementación de ES-F04-01.
- Implementación parcial: backend `49d40ff` (consumidor), `df4590a` (lector local) y `a65ed9f67900cec63bd489e8d72098877b24f94d` (caso de uso), rama `feature/f04-consultar-entregas-fallidas` desde `origin/develop` `bad76eb`, activa en el checkout habitual `G2-Despacho-Backend`. Specs: `docs/f04-evidencia-consulta-fallidas`, desde `main`.
- Dependencias de EV-06: HTTP simulado con `MockRestServiceServer`; sin PostgreSQL ni Operación real. Windows, Java Temurin 21.0.12.1, Maven 3.9.11 y Spring Boot 4.1.1 del proyecto.
- Alcance verificado: preparación documental, lectores de T-06 y lógica del caso de uso de T-07. EV-07/08 usan PostgreSQL real con esquema exclusivamente de pruebas; EV-08 comprueba la composición con puertos simulados. Ningún criterio de aceptación completo del endpoint o de UI se declara aprobado.
- Revisión del 15/10/2026: seis decisiones de comportamiento confirmadas por Gerardo; contrato y modelo en `4bad49d`, reglas de consulta en `1f556c0`. Implementación de fuentes, endpoints y componentes pendiente.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-07, T-08, T-09 | Listado autorizado de fallidos con campos e indicadores y paginación. | EV-01, EV-04 | No ejecutado |
| CA-02 | T-07, T-08, T-09 | Combinaciones de filtros, fechas y páginas. | EV-01, EV-04 | No ejecutado |
| CA-03 | T-02, T-04, T-07, T-09 | Vacío, sin coincidencias y recuperación ante error. | EV-01 a EV-04 | No ejecutado |
| CA-04 | T-02, T-04, T-07, T-09 | Rechazo sin datos y retirada de contenido previo. | EV-01 a EV-04 | No ejecutado |
| CA-05 | T-06, T-07, T-08, T-09 | Jornada cerrada/activa y recepción pendiente/confirmada. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-06 | T-06, T-07, T-08, T-09 | Incidencia vigente sin duplicados ni recepción heredada. | EV-01, EV-04 | No ejecutado |
| CA-07 | T-07, T-08, T-09 | Recibidos primero, antigua primero y desempate entre páginas. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-08 | T-06, T-07, T-08, T-09 | Métricas 7/5/2, tarjetas y filtros independientes de página. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-09 | T-07, T-08, T-09 | `NO_INTENTADO` con contador cero/uno sin aumento ni reinicio. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-10 | T-06, T-07, T-08, T-09 | Jornada desconocida, nombre ausente y error al filtrar atrasados. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-11 | T-07, T-08, T-09 | Filtros inválidos y errores diferenciados de vacío. | EV-01, EV-03, EV-04 | No ejecutado |
| CUI-01 | T-04, T-08, T-09 | Composición, campos e indicadores. | EV-03, EV-04 | No ejecutado |
| CUI-02 | T-04, T-08, T-09 | Filtros, URL, paginación y respuestas fuera de orden. | EV-03, EV-04 | No ejecutado |
| CUI-03 | T-02, T-04, T-08, T-09 | Estados de carga, vacío, sin resultados y error. | EV-02 a EV-04 | No ejecutado |
| CUI-04 | T-02, T-04, T-08, T-09 | Ocultar contenido protegido tras denegación. | EV-02 a EV-04 | No ejecutado |
| CUI-05 | T-04, T-08, T-09 | Presentación de retorno atrasado. | EV-03, EV-04 | No ejecutado |
| CUI-06 | T-02, T-04, T-08, T-09 | Teclado, foco, nombres accesibles y responsive. | EV-02 a EV-04 | No ejecutado |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles debe identificar su límite y no acredita integración real [cite: 1, 2].

EV-06 aporta comprobaciones del consumidor para CA-05/10 y T-06; EV-07 del lector para CA-01/02/06/09; EV-08 de la lógica para CA-02/03/05/07/08/09/10/11. Los resultados de aceptación anteriores conservan `No ejecutado`: todavía no existe el endpoint del listado ni su conexión frontend. Las pruebas de cada parte no cierran el recorrido funcional completo.

## 3. Registros de verificación previstos

### EV-01. Consulta y seguridad del backend

- Tareas y criterios: T-06/07/09; CA-01 a CA-11.
- Preparación prevista: PostgreSQL aislado con varios estados, intentos y recepciones; JWT de prueba con roles distintos; fuente de jornada identificada como real o doble.
- Comando previsto: `./mvnw.cmd test` desde Gestión de Despachos, con Docker para Testcontainers.
- Esperado: solo fallidos, filtros y páginas correctos, rechazo sin datos, retorno atrasado según la jornada y ninguna mutación de negocio.
- Fecha, persona, commits, resultado observado y reporte: pendientes. **Resultado: No ejecutado.**

### EV-02. Componente compartido CR-08

- Tareas y criterios: T-01/02; CCR-08-01 y su consumo en CUI-03/04/06.
- Preparación prevista: fixtures identificados y pruebas de interacción, con herramientas habilitadas según T-01.
- Esperado: estados diferenciados, acciones accesibles y ausencia de contenido protegido. Enlazar la evidencia compartida y añadir después la de su consumo.
- Fecha, persona, commit, comando y reporte: pendientes. **Resultado: No ejecutado.**

### EV-03. Página aislada e interacción

- Tareas y criterios: T-03/04; CUI-01 a CUI-06.
- Preparación prevista: fixtures de presentación con las combinaciones de recepción, etiquetas y estados de consulta.
- Esperado: controles y recuperaciones correctos; recorrido con teclado y adaptación a escritorio/móvil. Esta prueba no valida la autorización ni el filtrado del servidor.
- Fecha, persona, commit, pasos y capturas/reportes: pendientes. **Resultado: No ejecutado.**

### EV-04. Recorrido con servicios reales

- Tareas y criterios: T-08/09; CA-01 a CA-11 y CUI-01 a CUI-06.
- Preparación prevista: contrato revisado, datos sintéticos y servicios identificados; acceso humano por Gateway; fuentes de jornada y repartidor disponibles.
- Esperado: consulta real, filtros y permisos correctos, estados recuperables y cifras confirmadas. Registrar por separado los destinos de detalle/recepción disponibles o pendientes.
- Fecha, persona, commits, entorno, comandos y reportes: pendientes. **Resultado: No ejecutado.**

Cada registro ejecutado debe indicar versión exacta, preparación reproducible, resultado observado y artefacto. No incluir tokens, credenciales ni datos personales reales.

### EV-05. Comprobación documental de los acuerdos

- Fecha y herramienta: 15/10/2026, Codex mediante Git y Python del entorno de trabajo.
- Alcance: T-05; definición documental del catálogo/listado/lectura operativa y alineamiento de spec, UI, plan, tareas, historia y diseños. No verifica un endpoint ni una pantalla implementados.
- Comprobaciones: `git diff --check`; lectura y parseo de todos los bloques JSON del contrato; revisión de enlaces locales de los documentos modificados, unicidad de criterios y cobertura CA-01 a CA-11/CUI-01 a CUI-06 en tareas y evidencia; comprobación de consistencia del ejemplo de respuesta con sus totales e indicadores.
- Resultado: comprobación documental aprobada. `git diff --check` sin errores; 43 ejemplos JSON válidos; 170 enlaces locales comprobados sin destinos inexistentes; CA-01 a CA-11 y CUI-01 a CUI-06 únicos y cubiertos por tareas/evidencia. El ejemplo del listado es coherente con su contador, recepción, jornada, métricas y paginación. Los resultados funcionales de EV-01 a EV-04 continúan `No ejecutado`.

### EV-06. Consumidor de datos operativos por lotes

- Fecha: 16/10/2026, America/Lima. Implementación y ejecución por Codex; revisión humana pendiente.
- Tarea: avance parcial de T-06, conforme a Operación §5.4 y Gestión §5.1, sin modificar contratos [cite: 1, 2].
- Código: en Gestión, paquete `incidencias/`, puerto `application/LectorDatosOperativos.java`, modelo `domain/DatosOperativos.java`, adaptador `infrastructure/OperacionIncidenciasHttp.java` y prueba homónima en `src/test/java`. Commit `49d40ff`.
- Preparación: `RestClient` conectado a `MockRestServiceServer`, credencial y nombres exclusivamente de prueba. Identificadores como cadenas opacas, sin convertirlos a UUID. Sin cuentas ni secretos reales.
- Comandos reproducibles desde `G2-Despacho-Backend/servicio-gestion-despachos`:

```powershell
$mavenF04 = 'C:\Users\Gerardo\.m2\wrapper\dists\apache-maven-3.9.11-bin\6mqf5t809d9geo83kj4ttckcbc\apache-maven-3.9.11\bin\mvn.cmd'
& $mavenF04 '-Dtest=OperacionIncidenciasHttpTests' test
& $mavenF04 -B -ntp -o '-Dtest=CalculadoraCotizacionTests,ControladorCotizacionTests,ValidadorTokenDespachoTests' test
```

- Resultado observado: compilación de 72 fuentes y 8 fuentes de prueba; **6 pruebas nuevas aprobadas**, sin fallos, errores ni omitidas. Regresión existente sin contenedores: **13 pruebas aprobadas**, con 6 de cotización HTTP, 3 de cálculo y 4 de validación JWT. Ambas ejecuciones terminan con `BUILD SUCCESS`.
- Reportes Surefire conservados: [consumidor](./evidencia/EV-06-lectura-operativa.txt), [cotización HTTP](./evidencia/EV-06-regresion-cotizacion-api.txt), [cálculo](./evidencia/EV-06-regresion-calculo.txt) y [JWT](./evidencia/EV-06-regresion-jwt.txt).

| Comprobación prioritaria | Resultado observado |
|---|---|
| Entrada vacía o credencial técnica ausente. | No envía solicitudes vacías ni anónimas; conserva identificadores sin inventar nombres o jornadas. |
| 101 repartidores y 205 jornadas, con jornadas duplicadas. | Deduplica y efectúa tres solicitudes; ningún arreglo supera 100 elementos. |
| Respuesta válida. | Envía el Bearer técnico y conserva nombre, jornada activa/cerrada/desconocida, cierre y marca de consulta. |
| Omisiones, identificadores duplicados o ajenos y estado/fecha incoherentes. | Degrada solo los elementos afectados; no incorpora recursos no solicitados. |
| Error de transporte, `401` y `503` después de una lectura válida. | No reutiliza la jornada anterior ni expone errores internos; la información no obtenida queda desconocida. |
| Lote sin `consultadoEn` y lote posterior válido. | No confirma datos del primero; conserva los datos confirmados del segundo. |

Incidencias del entorno: el Wrapper apunta a Maven 3.10.0 e intentó crear su distribución fuera del workspace, sin permisos en el sandbox; se usó Maven instalado sin modificar el Wrapper. El intento offline encontró dependencias ausentes, descargadas después con acceso de red autorizado. La regresión inicial en sandbox se detuvo por el canal local de Mockito (`attach`, pipe Windows con acceso denegado); repetida fuera del sandbox pasó. Docker no está iniciado: no se ejecutan `FlujoF01Tests` ni `ServicioGestionDespachosApplicationTests`, que requieren contenedores.

Corrección de ubicación del 16/10/2026: las pruebas anteriores se ejecutaron inicialmente en un worktree temporal. Por indicación de Gerardo, la misma rama y el mismo commit se activaron en `G2-Despacho-Backend` y se retiró la carpeta temporal. Se respaldaron en Git y verificaron por SHA-256 los 59 archivos locales previos, sin diferencias de contenido. El traslado no modifica el código probado; los reportes anteriores se conservan como evidencia de esa ejecución, sin declarar una repetición de las pruebas.

Límites: no se acredita llamada a Operación real, PostgreSQL, cálculo de indicadores, autorización de un endpoint de F-04 ni pantalla. El adaptador aún no está registrado como bean: falta suministrar URL interna, tiempos de espera acotados y proveedor de credencial vigente al ensamblarlo. La lectura local y `ultima_incidencia_id` requieren la base compartida de F-02/F-03 y Arquitectura. La decisión de `200` degradado o `503` por solo atrasados corresponde al caso de uso pendiente de T-07. T-06 permanece `En curso`.

### EV-07. Lectura local de la incidencia vigente con PostgreSQL

- Fecha: 16/10/2026, America/Lima. Código backend `df4590a`, sobre el incremento `49d40ff`. Implementación y verificación por Codex; revisión humana pendiente.
- Alcance: parte local de T-06, siguiendo modelo §§3.3/3.4 y contrato Gestión §5.1 [cite: 1, 2]. Puerto `LectorIncidenciasLocales`, proyección `IncidenciaListadoLocal`, adaptador `IncidenciasLocalesJdbc` en `incidencias/`.
- Preparación: Docker Desktop iniciado para las pruebas; Docker 29.4.0, Testcontainers 2.0.5, imagen `postgres:17`, Java 21.0.12.1 y Maven 3.9.11. Base temporal sin conexión a los datos del proyecto; esquema mínimo de prueba en `src/test/resources/incidencias/esquema-lectura-fallidos.sql`.
- La selección utiliza una sentencia sobre tablas locales: despacho `FALLIDO`, registro apuntado por `ultima_incidencia_id` del mismo despacho con resultado fallido, catálogo y máximo configurado. No consulta tablas de Operación ni escribe estados, recepciones o eventos. No pagina la base antes de que el caso de uso calcule indicadores.
- Comandos desde `G2-Despacho-Backend/servicio-gestion-despachos`, con `$mavenF04` definido en EV-06:

```powershell
& $mavenF04 -B -ntp '-Dtest=IncidenciasLocalesJdbcTests' test
& $mavenF04 -B -ntp -o '-Dtest=ServicioGestionDespachosApplicationTests,FlujoF01Tests' test
```

- Resultado observado: compilación de 75 fuentes y 9 fuentes de prueba; **4 pruebas nuevas aprobadas**, sin fallos, errores ni omitidas. Regresión: **5 pruebas existentes aprobadas**, cuatro de F-01 y una de arranque, con el lector registrado en Spring. Ambas ejecuciones terminan con `BUILD SUCCESS`; no se añaden pruebas unitarias adicionales.
- Reportes conservados: [lector PostgreSQL](./evidencia/EV-07-lectura-local-postgresql.txt), [regresión F-01](./evidencia/EV-07-regresion-f01.txt) y [arranque](./evidencia/EV-07-arranque-servicio.txt). La regresión conserva la configuración existente `postgres:latest`, que resolvió PostgreSQL 18.6; no modifica esa configuración.

| Prueba prioritaria | Resultado observado |
|---|---|
| Dos incidencias del mismo despacho, última `NO_INTENTADO`, una recepción/evidencia histórica y otros seis estados. | Una sola fila vigente por despacho fallido, sin heredar recepción/evidencia; conserva contador acumulado, versión y referencias de la incidencia. Incluye el motivo histórico inactivo y la anulación. |
| Instantes a ambos lados de medianoche de Lima; rango abierto/cerrado y motivo histórico. | Incluye desde las 05:00 UTC del día y excluye las 05:00 del siguiente, con límites independientes; sin rango no aplica fecha implícita. Rango invertido se rechaza en el lector; validación HTTP aún pendiente. |
| Referencia vigente ausente, de otro despacho o con resultado entregado. | La lectura sin filtros detecta las inconsistencias, sin presentarlas como un listado vacío ni seleccionar otra incidencia por fecha o contador. |
| Política ausente, no numérica, cero o valor válido distinto del inicial. | No inventa un máximo ante configuración inválida; lee el valor vigente cuando es válido. |

Límites: el esquema de prueba no sustituye ni verifica las migraciones de despachos/intentos de F-02/F-03; no se agregan migraciones de producción. No prueba la transacción que escribe `ultima_incidencia_id`, PostgreSQL del proyecto, Operación real, totales, paginación, validación HTTP ni permisos del endpoint. Falta coordinar las migraciones compartidas y ejecutar el lector sobre ellas. T-06 sigue `En curso`; T-07 conserva su estado pendiente.

### EV-08. Caso de uso, filtros tipados, indicadores, orden y paginación

- Fecha: 16/10/2026, America/Lima. Backend `a65ed9f`, sobre `df4590a`. Trabajo asistido por Codex; revisión humana pendiente.
- Alcance: composición independiente de T-07 y subpaso de T-06. Se usan los puertos `LectorIncidenciasLocales`, `LectorDatosOperativos` y `CatalogoMotivosFallo`, con un reloj inyectado. El catálogo se consulta sobre la tabla canónica desde `IncidenciasLocalesJdbc`, sin excluir motivos inactivos; no se crea otra fuente de motivos.
- Código de aplicación: `ConsultarEntregasFallidas`, `FiltrosConsultaFallidos` y `PaginaEntregasFallidas`. Prueba nueva: `ConsultarEntregasFallidasTests`, con lectores simulados, nombres ficticios y reloj fijo `2026-10-16T18:00:00Z`. Ese instante es un dato de prueba, no la hora de ejecución.
- Entorno: Java 21.0.12.1, Maven 3.9.11, Docker 29.4.0 y Spring Boot 4.1.1. La prueba JDBC conserva PostgreSQL 17 y su esquema aislado; las pruebas existentes de arranque/F-01 conservan su configuración original.
- Comandos desde `G2-Despacho-Backend/servicio-gestion-despachos`, con `$mavenF04` definido en EV-06:

```powershell
& $mavenF04 -B -ntp -o '-Dtest=ConsultarEntregasFallidasTests,IncidenciasLocalesJdbcTests' test
& $mavenF04 -B -ntp -o '-Dtest=OperacionIncidenciasHttpTests,ServicioGestionDespachosApplicationTests,FlujoF01Tests,CalculadoraCotizacionTests,ControladorCotizacionTests,ValidadorTokenDespachoTests' test
```

- Resultado observado: compilación de 79 fuentes y 10 fuentes de prueba. Primera ejecución: **10 pruebas aprobadas**, seis nuevas del caso de uso y cuatro del lector JDBC; estas últimas amplían las comprobaciones de catálogo histórico e inexistente sin añadir otra prueba. Segunda ejecución: **24 pruebas existentes aprobadas**. Total: **34 pruebas, sin fallos, errores ni omitidas**; ambas ejecuciones terminan con `BUILD SUCCESS`.
- Reportes Surefire: [seis pruebas del caso de uso](./evidencia/EV-08-caso-uso-fallidos.txt) y [28 pruebas existentes, incluido lector JDBC](./evidencia/EV-08-regresion-backend.txt).

| Comprobación prioritaria | Resultado observado |
|---|---|
| Base 7 pendientes, 5 recibidos y 2 atrasados; página parcial y selección de recibidos. | Conserva 7/5/2 en ambos grupos, calcula el total del grupo antes de paginar y pone recibidos primero aunque haya pendientes más antiguos. Consulta todas las jornadas pendientes y pide nombres solo de la página. |
| Antigüedad, empate de fecha y página máxima entera. | Orden por fecha e identificador; página posterior al final vacía con totales y página conservados, sin desbordar el cálculo de posición. Base vacía tiene cero páginas y no llama a Operación. |
| Jornada desconocida fuera de la página y nombres no disponibles. | El total de atrasados permanece `null`; informa pendientes sin jornada confirmada, conserva el nombre `null`, y un recibido tiene atraso `false`. Un pendiente desconocido tiene atraso `null`. Pedir solo atrasados genera el error de negocio `503` acordado antes de consultar nombres. |
| Filtro de solo atrasados con datos completos y sin pendientes. | Selecciona únicamente pendientes con jornada cerrada. Si todos están recibidos, devuelve cero coincidencias sin depender de Operación para ese filtro. |
| Página/tamaño inválidos, motivo vacío, rango invertido, grupo incompatible y código inexistente. | Genera error de negocio `400` con `DESP_ERROR_FILTROS_INVALIDOS`; no lee incidencias ni datos operativos. El código inexistente se comprueba en el catálogo. |
| Motivo/fechas válidos y una salida `NO_INTENTADO`. | Delega motivo y fechas al lector; mantiene la identidad de incidencia/jornada y el contador acumulado de 1 sobre 2, con `consumeIntento=false`. |

Límites: el caso de uso aún no está registrado como bean de ejecución ni expuesto por controlador. Los estados `400/503` son errores de negocio probados en Java, no respuestas HTTP verificadas de F-04. Siguen pendientes parámetros crudos repetidos/desconocidos o mal formados, JWT/roles antes de cualquier lectura, serialización de respuesta, ensamblaje del cliente técnico, migraciones/escritores compartidos y recorrido real por Gateway. La composición con puertos simulados no acredita la integración conjunta de JDBC y HTTP de Operación. T-06 y T-07 permanecen `En curso`.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción y revisión |
|---|---|---|---|
| Preparación documental de la carpeta SDD | Codex, 15/10/2026 | Especificación previa, plantillas aprobadas en `8586a78`, F-04, contrato, modelo, diseño y componentes; bases de código de §1. | Solicitud de Gerardo: alinear reglas y después preparar únicamente la primera especificación, conservando el contenido existente y completando los documentos. Revisión humana de los nuevos documentos: pendiente. |
| Revisión de reglas de ES-F04-01 | Codex, 15/10/2026 | Seis recomendaciones confirmadas por Gerardo, carpeta SDD, contrato, modelo y diseños relacionados. | Aplicar los acuerdos y alinear documentos; guardar el trabajo en rama y commits separados según CONTRIBUTING. Revisión de comportamiento por Gerardo: confirmada en la conversación. Verificación contra implementación: pendiente. |
| Consumidor backend por lotes de T-06 | Codex, 16/10/2026 | Carpeta SDD, contratos Gestión §5.1 y Operación §5.4, modelo y backend `bad76eb`. | Gerardo autoriza backend por partes, pruebas prioritarias, ramas desde `develop` y Specs desde `main`, sin desarrollar componentes React de compañeros. Solo consumidor, seis pruebas y seguimiento parcial. Revisión humana pendiente. |
| Lectura local JDBC de T-06 | Codex, 16/10/2026 | Mismos documentos y backend `49d40ff`; esquema canónico de Gestión. | Gerardo pide el siguiente incremento dentro del repositorio backend y su rama. Se implementa el lector con cuatro pruebas PostgreSQL y se ejecutan cinco pruebas existentes; migraciones de otros integrantes y endpoint permanecen pendientes. Revisión humana pendiente. |
| Caso de uso y filtros de T-07 | Codex, 16/10/2026 | Carpeta SDD, contratos y backend `df4590a`; lectores ya preparados. | Gerardo pide continuar y guardar los commits correspondientes, manteniendo avances por partes y pruebas prioritarias. Se componen los puertos, se añaden seis pruebas y se ejecuta la regresión; HTTP e integración real permanecen pendientes. Revisión humana pendiente. |

Este registro describe asistencia documental, cierre documental de T-05 y avances técnicos de T-06/T-07 acreditados por EV-06/07/08. No acredita el cierre de esas tareas ni pruebas de aceptación del endpoint del listado o integración real.

## 5. Diferencias y pendientes

| Hallazgo | Criterios afectados | Efecto y siguiente acción |
|---|---|---|
| DT-01: contrato definido en Gestión §4, Gestión §5.1; implementación pendiente. | CA-01 a CA-11 y CUI-02. | Implementar y comprobar consumidores conforme a T-07/08; T-05 solo acredita documentación. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo). |
| DT-02: consumidor por lotes verificado con HTTP simulado en EV-06; proveedor real y ensamblaje pendientes. | CA-01/05/06/08/10 y CUI-01/05. | Coordinar proveedor y credenciales; conectar jornadas/nombres a la consulta y comprobar integración en T-06/07. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias), [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01). |
| DT-03/04: bases de ejecución y componentes aún por verificar/implementar. | Todos. | Coordinar preparación y componentes, ejecutar tareas y registrar resultados. |
| Migraciones de despachos/incidencias ausentes en `bad76eb`; lector preparado con esquema de prueba en EV-07. | CA-01/02/05/06/08/09/10. | Coordinar migraciones/escritores con F-02/F-03 y Arquitectura, y verificar el lector sobre la base compartida real. |
| Caso de uso preparado en EV-08; entrada HTTP, autorización y ensamblaje pendientes. | CA-01 a CA-11 e integración real. | Continuar T-07 con controlador, validación cruda, seguridad y adaptación de los puertos reales, sin dar por completada T-06. |

## 6. Entrega y revisión

- Entrega actual: consumidor backend (EV-06), lector local JDBC (EV-07) y caso de uso/filtros del listado (EV-08), con sus pruebas. Endpoint del listado pendiente.
- Commits backend: `49d40ff`, `df4590a` y `a65ed9f`; PR e integración en `develop` pendientes. Documentación en rama desde `main`; sin publicación remota en estos incrementos.
- Reglas de consulta: confirmadas por Gerardo el 15/10/2026. Revisión técnica y funcional de la implementación: pendientes.
- Estado del alcance funcional: Pendiente.
- Integración real y destinos de otras especificaciones: pendientes según el plan.

## 7. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [plan](./plan.md) y [tareas](./tasks.md).
2. [Flujo SDD](../../plantillas/sdd/README.md), reglas de evidencia y verificación.
3. [Componentes React](../../disenio/componentes-react.md), §4.2 para evidencia compartida.
