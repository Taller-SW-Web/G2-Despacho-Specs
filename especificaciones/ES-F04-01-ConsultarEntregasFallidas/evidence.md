# Evidencia de ES-F04-01: Consultar entregas fallidas

**Estado:** Implementación backend parcial en T-06; consumidor verificado con HTTP simulado. Verificación funcional pendiente.

**Responsable de verificación:** Gerardo.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), incorporados en la misma revisión de esta carpeta.
- Origen de la especificación y fuentes generales: revisión `8586a78` del repositorio de especificaciones.
- Base de código consultada: backend `af13989` y frontend `d2bc27d`; no constituyen una implementación de ES-F04-01.
- Implementación parcial: backend `49d40ff1507e05e909d859c2792ff5eed8203293`, rama `feature/f04-consultar-entregas-fallidas` desde `origin/develop` `bad76eb`. Worktree `trabajo-f04-backend`, para preservar los cambios locales de F-01 del checkout original. Specs: `docs/f04-evidencia-consulta-fallidas`, desde `main`.
- Dependencias de EV-06: HTTP simulado con `MockRestServiceServer`; sin PostgreSQL ni Operación real. Windows, Java Temurin 21.0.12.1, Maven 3.9.11 y Spring Boot 4.1.1 del proyecto.
- Alcance verificado: preparación documental y consumidor por lotes de T-06. Ningún criterio de aceptación completo del listado o de UI se declara aprobado.
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

EV-06 aporta comprobaciones del consumidor para CA-05/10 y T-06. Los resultados de aceptación anteriores conservan `No ejecutado`: todavía no existe el listado backend ni su conexión frontend.

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
- Comandos desde `trabajo-f04-backend/servicio-gestion-despachos`:

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

Límites: no se acredita llamada a Operación real, PostgreSQL, cálculo de indicadores, autorización de un endpoint de F-04 ni pantalla. El adaptador aún no está registrado como bean: falta suministrar URL interna, tiempos de espera acotados y proveedor de credencial vigente al ensamblarlo. La lectura local y `ultima_incidencia_id` requieren la base compartida de F-02/F-03 y Arquitectura. La decisión de `200` degradado o `503` por solo atrasados corresponde al caso de uso pendiente de T-07. T-06 permanece `En curso`.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción y revisión |
|---|---|---|---|
| Preparación documental de la carpeta SDD | Codex, 15/10/2026 | Especificación previa, plantillas aprobadas en `8586a78`, F-04, contrato, modelo, diseño y componentes; bases de código de §1. | Solicitud de Gerardo: alinear reglas y después preparar únicamente la primera especificación, conservando el contenido existente y completando los documentos. Revisión humana de los nuevos documentos: pendiente. |
| Revisión de reglas de ES-F04-01 | Codex, 15/10/2026 | Seis recomendaciones confirmadas por Gerardo, carpeta SDD, contrato, modelo y diseños relacionados. | Aplicar los acuerdos y alinear documentos; guardar el trabajo en rama y commits separados según CONTRIBUTING. Revisión de comportamiento por Gerardo: confirmada en la conversación. Verificación contra implementación: pendiente. |
| Consumidor backend por lotes de T-06 | Codex, 16/10/2026 | Carpeta SDD, contratos Gestión §5.1 y Operación §5.4, modelo y backend `bad76eb`. | Gerardo autoriza backend por partes, pruebas prioritarias, ramas desde `develop` y Specs desde `main`, sin desarrollar componentes React de compañeros. Solo consumidor, seis pruebas y seguimiento parcial. Revisión humana pendiente. |

Este registro describe asistencia documental, cierre documental de T-05 y avance técnico de T-06 acreditado por EV-06. No acredita el cierre de T-06 ni pruebas de aceptación del listado o integración real.

## 5. Diferencias y pendientes

| Hallazgo | Criterios afectados | Efecto y siguiente acción |
|---|---|---|
| DT-01: contrato definido en Gestión §4, Gestión §5.1; implementación pendiente. | CA-01 a CA-11 y CUI-02. | Implementar y comprobar consumidores conforme a T-07/08; T-05 solo acredita documentación. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo). |
| DT-02: consumidor por lotes verificado con HTTP simulado en EV-06; proveedor real y ensamblaje pendientes. | CA-01/05/06/08/10 y CUI-01/05. | Coordinar proveedor y credenciales; conectar jornadas/nombres a la consulta y comprobar integración en T-06/07. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias), [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01). |
| DT-03/04: bases de ejecución y componentes aún por verificar/implementar. | Todos. | Coordinar preparación y componentes, ejecutar tareas y registrar resultados. |
| Persistencia de despachos/incidencias ausente en `bad76eb`. | CA-01/02/05/06/08/09/10. | Coordinar migraciones y escritores con F-02/F-03 y Arquitectura, sin crear tablas paralelas. |

## 6. Entrega y revisión

- Entrega actual: consumidor backend de T-06 y seis pruebas, EV-06. Listado funcional pendiente.
- Commit backend: `49d40ff`; PR e integración en `develop` pendientes. Documentación en rama desde `main`; sin publicación remota en este incremento.
- Reglas de consulta: confirmadas por Gerardo el 15/10/2026. Revisión técnica y funcional de la implementación: pendientes.
- Estado del alcance funcional: Pendiente.
- Integración real y destinos de otras especificaciones: pendientes según el plan.

## 7. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [plan](./plan.md) y [tareas](./tasks.md).
2. [Flujo SDD](../../plantillas/sdd/README.md), reglas de evidencia y verificación.
3. [Componentes React](../../disenio/componentes-react.md), §4.2 para evidencia compartida.
