# Evidencia de ES-F04-03: Confirmar la recepción del paquete

**Estado:** Recepción en Gestión y frontend implementados y verificados localmente; integración real y aceptación pendientes.

**Responsable de verificación:** Gerardo; implementación y registro asistidos por Codex. Revisión humana pendiente.

**Última verificación de implementación:** 24/10/2026, America/Lima. Esta actualización documental consulta los commits y registros existentes; no vuelve a ejecutar las suites ni acredita un despliegue.

## 1. Versión y entorno verificados

| Repositorio | Rama y base | Commits del incremento |
|---|---|---|
| Backend | `feature/f04-confirmar-recepcion-paquete`, desde `develop` en `a9a8f73` | `31e1f6eb9b39b991d3ecee08f02a1a7ea3a50034`: recepción, procesador, pruebas y registro backend. |
| Frontend | `feature/f04-recepcion-paquete-frontend`, desde `develop` en `8a37d13` | `779f6c41ffa644770019dbb277afb3352731848a`: modal, integración en ambas pantallas y pruebas; `9108cafb36880d4fc9496105e1969e24086f6977`: documentación y captura. |
| Especificaciones | `docs/f04-evidencia-recepcion-paquete`, desde `main` en `21bb18f` | Actualización documental del 24/10/2026 que registra el avance en los cinco documentos SDD y la fila ES-F04-03 del índice. |

- Preparación histórica: migración SDD del 15/10/2026 sobre `0734268`, con lectura estática de frontend `d2bc27d` y backend `1e7834b`. No se atribuyen las pruebas posteriores a esa preparación.
- Backend: Java 21, Maven Wrapper, Docker Desktop y PostgreSQL/PostGIS 17.11 desechable mediante Testcontainers. Flyway aplica V1/V2 originales en base vacía; no se agregó V3 ni se utilizaron Supabase o bases compartidas.
- Frontend: React 19.2, Mantine 9.6.2, TypeScript, Vite, Vitest/Testing Library y JSDOM existentes; revisión manual de la app con APIs y datos simulados identificados. Sin cambios de dependencias ni componentes compartidos.
- Los proveedores JWT y Operación del backend son dobles controlados. No se modificó ni se ejecutó para aceptación el microservicio de Operación, su base de datos, Gateway o Seguridad. El frontend no se probó conjuntamente contra los servicios reales.
- Commits comprobados en los checkouts locales. No se registra push, PR, aprobación o despliegue de este incremento; las rutas a repositorios hermanos siguientes requieren esos checkouts, no constituyen enlaces de publicación.

Registros de origen: [verificación backend](../../../G2-Despacho-Backend/servicio-gestion-despachos/docs/ES-F04-03-verificacion.md) en `31e1f6e` y [verificación frontend](../../../G2-Despacho-Frontend/docs/ES-F04-03-ConfirmarRecepcionPaquete.md) en `9108caf`. Esta evidencia consolida su trazabilidad sin redefinir los contratos [cite: 1, 2, 3].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación efectuada y límite | Registros | Resultado |
|---|---|---|---|---|
| CA-01 | T-03/04/06/07/08/09/10 | Recepción/historial/versión/solicitud atómicos y UI actualizada; reducción real de ocupación sin verificar. | EV-01/03/04/05 | Aprobado local; pendiente integral |
| CA-02 | T-02/04/08/10 | No sin observación y normalización probados en endpoint y UI por separado. | EV-01/04 | Aprobado local |
| CA-03 | T-03/05/06/07/08/09/10 | Respuesta original tras liberar/resolver/nueva salida; recuperación exacta del frontend. Liberación real pendiente. | EV-01/03/04/05 | Aprobado local; pendiente integral |
| CA-04 | T-02/04/05/08/10 | Estado, incidencia, versión incompatibles y conflicto sin traslado de decisión. | EV-01/04 | Aprobado local |
| CA-05 | T-02/04/08/10 | Tipos/campos estrictos, 500/501 puntos de código, espacios y emojis. | EV-01/04 | Aprobado local |
| CA-06 | T-02/04/06/08/10 | Seguridad de Gestión y retirada de datos de UI con identidades de prueba; acceso real a Operación sin verificar. | EV-01/02/04 | Aprobado local; pendiente integral |
| CA-07 | T-03/05/06/07/08/09/10 | Referencia original con otra salida actual y cliente HTTP controlado; reservas reales entre servicios pendientes. | EV-01/03/04/05 | Aprobado local; pendiente integral |
| CA-08 | T-03/04/07/08/10 | Fallos en cuatro escrituras, rollback íntegro y referencias/respuestas originales inconsistentes rechazadas. | EV-01/03/04 | Aprobado local |
| CA-09 | T-06/07/08/09/10 | Calendario, exclusión, token vencido, errores y respuesta perdida con dobles; reinicios desplegados pendientes. | EV-02/03/04/05 | Aprobado local; pendiente integral |
| CA-10 | T-02/05/08/10 | Carreras de dos transacciones PostgreSQL y doble activación de UI; primera recepción inmutable. | EV-01/04 | Aprobado local |
| CA-11 | T-03/04/08/09/10 | NO_INTENTADO/anulación/máximo/sin foto sin alterar intentos; estado de jornada real pendiente. | EV-01/04/05 | Aprobado local; pendiente integral |
| CA-12 | T-02/08/09/10 | Contexto vigente, recuperación antes de repetir, origen/filtros y éxito conservado con refresco fallido; APIs simuladas. | EV-04/05 | Aprobado local; pendiente integral |
| CUI-01 | T-01/02/08/09/10 | Apertura desde listado/detalle, fecha Lima y origen conservado con datos simulados. | EV-04/05 | Aprobado local |
| CUI-02 | T-01/02/08/10 | Selección explícita, No sin texto y contador Unicode. | EV-04 | Aprobado local |
| CUI-03 | T-01/02/08/10 | Doble activación y envío demorado sin editar/cancelar ni duplicar POST. | EV-04 | Aprobado local |
| CUI-04 | T-01/02/08/10 | Valores conservados con 400/500; 503 exige consulta y repetición original incluso tras reapertura. | EV-04/05 | Aprobado local |
| CUI-05 | T-01/02/08/09/10 | 409/cambio de incidencia y recepción consultada sin sustituir la operación original. | EV-04/05 | Aprobado local |
| CUI-06 | T-01/02/08/09/10 | 202 conserva aviso de éxito con refresco fallido y distingue liberación pendiente; Operación real caída no probada. | EV-04/05 | Aprobado local; pendiente integral |
| CUI-07 | T-01/02/08/10 | Revocación de permiso durante confirmación retira datos protegidos. | EV-04 | Aprobado local |
| CUI-08 | T-01/02/08/10 | Teclado/foco y móvil comprobados; ampliación al 200 % y revisión con Max pendientes. | EV-04 | Pendiente; alcance local parcial aprobado |

`Aprobado local` acredita solo las comprobaciones descritas con su entorno; no equivale a aceptación integrada. Los pendientes de EV-02/05, históricos reales y revisión humana impiden cerrar la especificación. No se declara fallida una integración que no se ejecutó.

## 3. Registros de verificación

### EV-01. Persistencia, recepción y seguridad

- Tareas/criterios: T-03/04/05/10; CA-01 a CA-08, CA-10/11 en el alcance de Gestión.
- Código: backend `31e1f6e`; `RecepcionCentroJdbc`, `ControladorRecepcionCentro`, validación de `SolicitudesRecepcion` y esquema original V1/V2. Sin migración nueva ni cambios en tablas de Operación.
- Ejecución final de implementación: 24/10/2026, 01:28:56 (America/Lima), `./mvnw.cmd clean verify` desde `servicio-gestion-despachos`; **BUILD SUCCESS**, 2 min 47 s, **109 pruebas, cero fallos, errores y omisiones**, JAR construido. Incluye 25 pruebas nuevas: 14 de recepción HTTP con PostgreSQL, 3 de validación, 4 del procesador y 4 del adaptador HTTP; las demás son regresiones de Gestión.
- `RecepcionCentroHttpTests` prueba aceptación, lectura posterior, roles/tipos, incidencias/versiones, NO_INTENTADO/anulación/máximo/sin foto, fallos inyectados en las cuatro escrituras y tres carreras con dos transacciones. Comprueba una recepción/historial/solicitud, contador y estado conservados y ausencia de eventos a Ventas.
- `respuestaOriginalSobreviveLiberacionResolucionYNuevaSalida` y `rechazaReutilizacionPorOtroActorOCuerpoPeroNormalizaEspacios` comprueban la respuesta durable y el reconocimiento previo a las precondiciones actuales. `SolicitudesRecepcionTests` incluye espacios Unicode y 500/501 caracteres suplementarios.
- Artefactos reproducibles: `servicio-gestion-despachos/target/surefire-reports/TEST-*.xml` y `*.txt`; salida de entrega `target/verificacion-f04.log`, generados y sin versionar. La actualización documental releyó los 24 informes XML existentes: suman 109 pruebas sin fallos, errores u omisiones; no los volvió a ejecutar.
- **Resultado: Aprobado para Gestión y persistencia aislada.** T-04/05 completadas; T-03 sigue en curso por inspección/reconciliación histórica real y actualización desde una base previa no ejecutadas. Los fixtures inconsistentes se rechazan; no se fabrican reservas ni respuestas históricas.

### EV-02. Liberación y reservas de Operación

- Tareas/criterios: T-06/10; CA-01/03/06/07/09.
- **Resultado: No ejecutado para el proveedor real.** Operación y su base quedaron fuera de los cambios autorizados. Las pruebas del consumidor de Gestión no acreditan liberación atómica, idempotencia u ocupación del proveedor.
- Pendiente: credencial técnica real, reservas activas/liberadas/ajenas, dos salidas, jornada cerrada, repetición sin doble descuento y nueva asignación bloqueada por reserva anterior activa. Coordinar con responsables de Operación y F-02/F-06 antes de cerrar T-06/09.
- Al ejecutarlo, registrar commit, entorno, comandos y estados antes/después sin secretos; no reutilizar resultados de otros incrementos sin comprobarlos.

### EV-03. Procesador, caídas y recuperación

- Tareas/criterios: T-07/10; CA-01/03/07/08/09 en Gestión.
- Código: `ProcesadorLiberaciones`, `LiberacionesCapacidadJdbc`, `LiberadorCapacidadHttp` y configuración en `31e1f6e`. Reclamación SQL atómica con exclusión de 60 s y token, HTTP fuera de transacción y límite total de cinco segundos, calendario y revisión persistidos.
- Verificación incluida en el `clean verify` de EV-01: cuatro `ProcesadorLiberacionesTests`, cuatro `LiberadorCapacidadHttpTests` y escenarios JDBC/HTTP de recepción. Reloj y receptor controlados comprueban reclamación/exclusión, token vencido, errores HTTP, respuesta incoherente/perdida, referencia original y recuperación de solicitudes persistidas. Solo una confirmación válida completa el envío; los GET no lo ejecutan ni reencolan.
- Operación se representa mediante servidor HTTP local o MockRestServiceServer; la identidad técnica utiliza proveedores de prueba. La recreación del procesador en pruebas no equivale a reiniciar procesos desplegados.
- **Resultado: Aprobado para procesador y consumidor aislados.** T-07 sigue en curso: faltan credencial/proveedor reales y reinicios en las fronteras de persistencia/liberación de EV-05. No se acredita reducción real de ocupación ni ausencia de doble descuento en la base de Operación.

### EV-04. Modal, estados y accesibilidad

- Tareas/criterios: T-01/02/08/10; CA-01 a CA-12 en su alcance de interfaz y CUI-01 a CUI-08.
- Código: frontend `779f6c4`, registro y captura `9108caf`. `ModalRecepcionPaquete.tsx` y `apiRecepcion.ts`, integrados en `PaginaEntregasFallidas` y `PaginaDetalleIncidencia`. Reutiliza tema, cliente y controles existentes sin modificar bibliotecas compartidas ni añadir dependencias.
- El 24/10/2026 se ejecutaron desde la raíz del frontend: `npm run test:f04` (**32 aprobadas**: 10 del modal, 11 de detalle, 8 de listado y 3 de sesión); `npm run typecheck` (tres espacios de trabajo, aprobado); `npm run build -w @despacho/administrativo` (aprobado). Vite advierte sobre bundle administrativo mayor de 500 kB; no impide compilar. No se atribuye una construcción de ambas aplicaciones a este incremento.
- Son **12 pruebas nuevas**: 10 en `ModalRecepcionPaquete.test.tsx` y una integración de componentes nueva en cada archivo de pruebas de página. El total de 32 incluye regresiones, no 32 pruebas nuevas de recepción.
- Comprobado con JSDOM/APIs simuladas: contexto actualizado antes de habilitar, No sin texto, contador Unicode, identidad/versiones, doble envío, 400/500/503, 409, revocación 403, consulta antes de repetir, cuerpo original tras cerrar/reabrir y cambio de incidencia. Una incidencia nueva recibida no acredita la recepción original ni sustituye sus datos.
- La prueba integrada del listado usa la versión vigente del detalle, refresca indicadores y conserva filtros. La del detalle mantiene el éxito con refresco posterior 503 y comprueba el foco de retorno cuando la acción queda bloqueada.
- Revisión manual de la app con datos simulados: apertura desde ambos orígenes, No sin observación, 202, actualización del detalle/KPI, filtro de pendientes conservado y retirada de fila; foco inicial, Tab, Escape, reapertura limpia y retorno al disparador o encabezado si aquel desaparece. A 390 × 844 píxeles CSS el modal mide 351 píxeles, sin desbordamiento horizontal, y Confirmar queda debajo de Cancelar; se restableció el tamaño del navegador.
- Artefacto versionado en frontend `9108caf`: [captura del modal con datos simulados](../../../G2-Despacho-Frontend/docs/evidencia/f04-modal-recepcion.png); reproducibilidad y límites en el registro frontend de §1. El servidor temporal de revisión no forma parte del producto ni acredita una integración con Gestión desplegada.
- **Resultado: Aprobado para pruebas locales y recorrido manual descrito.** T-01 completada para dependencias consumidas, sin cerrar todos los CR. T-02/08 siguen en curso: ampliación al 200 %, revisión visual con Max y recorrido real EV-05 pendientes. Las pruebas simuladas no acreditan el historial/capacidad entre servicios reales.

### EV-05. Recorrido real y coherencia del módulo

- Tareas/criterios: T-08/09/10; CA-01/03/07/09/11/12 y CUI-01/04/05/06.
- **Resultado: No ejecutado.** No se registra una ejecución conjunta de frontend, Gateway, Gestión, Seguridad y Operación con F-02/F-06. T-09 permanece pendiente; no se considera cubierta por las suites aisladas.
- Preparación pendiente: servicios reales e identidad técnica autorizada, datos sintéticos trazables y responsables de Operación/F-02/F-06 disponibles. No modificar servicios de otros responsables ni bases compartidas para simular el cierre.
- Recorrido por registrar: recibir desde ambos orígenes, interrumpir/reanudar Operación y el procesador, perder una respuesta, contrastar historial y ocupación, consultar sin efectos y repetir la operación original tras otra salida. Reprogramación/cierre y nueva asignación requieren sus implementaciones ES-F04-04/05 y F-02; no se incorporaron como parte de ES-F04-03.
- Esperado: recepción independiente de sincronización, capacidad conservadora hasta liberar, asignación posterior segura y jornada cerrada sin reapertura; una repetición antigua no libera otra reserva. Registrar commits, comandos, estados antes/después y limitaciones al ejecutarlo.

### EV-06. Preparación y validación documental

- Registro histórico: preparación SDD del 15/10/2026 sobre `0734268`, incluida en el commit que introdujo la carpeta. Sus comprobaciones registraron 463 enlaces/anclas y 24 ejemplos JSON válidos en 24 documentos; 12 CA, 8 CUI, 10 tareas y 6 registros. Acreditó documentación, sin implementar ni ejecutar EV-01 a EV-05 en aquella fecha.
- Actualización del 24/10/2026: revisión de los commits y registros backend/frontend y de los informes XML existentes; actualizados estados, decisiones verificadas, tareas, cobertura y pendientes de esta carpeta y únicamente la fila ES-F04-03 del índice.
- Comprobación documental de esta actualización: `git diff --check` y validación local con Node aprobados; seis Markdown con H1 único y jerarquía correcta, 282 enlaces locales y 19 anclas válidos, 12 CA, 8 CUI, 10 tareas y 6 registros conservados. Se contrastaron casillas/estados, cobertura y ausencia de cambios en requisitos, reglas de UI u otras filas del índice. No se ejecutaron pruebas de código ni se modificaron backend/frontend durante este cambio.
- **Resultado: Aprobado para la preparación histórica y esta actualización documental.** La aceptación humana permanece pendiente; EV-06 no sustituye EV-02/05.

## 4. Uso de IA

| Trabajo | Herramienta/fecha | Entradas | Instrucción y revisión humana |
|---|---|---|---|
| Preparación SDD | Codex, 15/10/2026 | Revisión funcional, plantillas, contratos, modelo y bases iniciales. | Gerardo solicitó preparar los Markdown. Su preparación no acreditó implementación. |
| Backend y frontend ES-F04-03 | Codex, 24/10/2026 | Los cinco documentos SDD, AGENTS/CONTRIBUTING y contratos/diseño vigentes; bases `a9a8f73` y `8a37d13`. | Implementar y guardar commits; limitar backend a Gestión sin tocar Operación ni su base. Frontend autorizado en el incremento siguiente. Pruebas locales descritas en EV-01/03/04; revisión humana pendiente. |
| Actualización de seguimiento SDD | Codex, 24/10/2026 | Commits, registros de implementación, informes XML existentes y conversación. | Gerardo pidió actualizar solo lo necesario del repositorio de especificaciones. No cambia requisitos/contratos ni vuelve a ejecutar las pruebas; no atribuye aceptación al registro documental. |

## 5. Diferencias, fallos y pendientes

| Hallazgo o pendiente | Criterios afectados | Impacto y siguiente acción |
|---|---|---|
| DT-01: herramientas y reutilización comprobadas; faltan ampliación al 200 % y revisión con Max. | CUI-08 y cierre visual. | T-02/10 siguen en curso; coordinar revisión sin cambiar reglas funcionales. |
| DT-02: V1/V2 suficientes, sin V3; históricos y actualización de base previa no verificados. | CA-01/03/07/08/11. | T-03 sigue en curso; inspección/reconciliación verificable con Arquitectura y F-02/F-03 antes de habilitar datos afectados. |
| DT-03: procesador/cliente aprobados con dobles; liberación y credencial reales sin probar. | CA-01/03/06/07/09. | T-06/07/09; coordinación con Operación/DevOps, sin modificar su servicio en este incremento. |
| DT-04: origen actualizado con APIs simuladas; nueva asignación, ocupación e historial conjuntos sin probar. | CA-01/07/09/11/12. | EV-05 y T-08/09/10 pendientes de integración con F-02/F-06 y servicios reales. |
| Bundle administrativo mayor de 500 kB, advertencia de Vite. | Calidad de compilación. | Build aprobado; no se añade una optimización ajena al alcance de recepción. |

## 6. Entrega y revisión

- Código y pruebas locales: backend `31e1f6e`; frontend `779f6c4` y documentación/captura `9108caf`. Registros de origen y límites en §1 y EV-01/03/04.
- Estado de tareas: T-01/04/05 completadas en su alcance local; T-02/03/07/08/10 en curso; T-06/09 pendientes. Ninguna simulación cierra tareas de Operación o aceptación conjunta.
- Cambios documentales de este incremento limitados a ES-F04-03 y su fila del índice. No se alteran los CA/CUI, contratos, otras especificaciones ni repositorios de código.
- PR, aprobación por pares, revisión con Max y aceptación humana: pendientes. La publicación de los commits no se da por realizada.
- No se declara cerrada ES-F04-03: siguen integración real, históricos, ampliación al 200 % y revisión según el plan/tareas.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md) y [UI](./ui.md): comportamiento y criterios conservados.
- [cite: 2] [Plan](./plan.md), [tareas](./tasks.md) y [flujo SDD](../../plantillas/sdd/README.md): incrementos y estados verificables.
- [cite: 3] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §§5.2.1/5.3; [Operación](../../integraciones/api-contract-operacion-reparto.md), §§5.1/5.2; [modelo de datos](../../arquitectura/modelo-datos.md), §3.4: definiciones canónicas, sin duplicarlas aquí.
