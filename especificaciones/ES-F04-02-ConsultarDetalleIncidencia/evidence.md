# Evidencia de ES-F04-02: Consultar el detalle de una incidencia

**Estado:** Código implementado y verificación local aprobada; aceptación integral pendiente.

**Responsable:** Gerardo. Implementación asistida por Codex el 16/10/2026 (America/Lima); revisión humana pendiente.

## 1. Versiones y alcance

- Rama común: `feature/f04-detalle-incidencia`. Frontend parte de `develop` en `314537b`; backend de `develop` en `5a5c57b`; specs de `main` en `0f8f1f1`.
- Frontend: `e8a4f25` implementa la página y `7006761` añade las nueve pruebas esenciales y protege las respuestas de una sesión anterior.
- Backend: `96a0c95` implementa Gestión; `d8116ad`, evidencia de Operación; `cc1421a`, normalización de errores y configuración documentada.
- Código local confirmado mediante commits; no se publicaron ramas ni PR y no se ejecutaron Docker, despliegues, PostgreSQL ni Supabase reales.
- Java 21, Maven local 3.9.16, npm/Vitest existentes y React/Mantine del repositorio. No se cambiaron versiones de dependencias.
- El usuario autorizó código y commits y pidió aplazar Docker/despliegue. Las tareas que requieren integración real no se declaran completadas [cite: 1].

## 2. Resultados locales

| Comprobación | Resultado observado | Alcance real |
|---|---|---|
| Pruebas nuevas de Gestión | 4 aprobadas; 0 fallos/errores | Reglas, composición, filtrado de historial y HTTP con MockMvc; persistencia y proveedor simulados. |
| Pruebas nuevas de Operación | 5 aprobadas; 0 fallos/errores | Permisos, asociación, renovación, firma y objeto eliminado; repositorio y Storage simulados. |
| Pruebas nuevas de frontend | 9 aprobadas; 0 fallos | Página, panel, hooks, URL de origen, permisos y respuestas obsoletas con fixtures. |
| Regresión `npm run test:f04` | 17 aprobadas: 9 de detalle, 7 de listado y 1 de sesión | JSDOM y APIs simuladas; no layout real. |
| `npm run typecheck` | Aprobado | Paquete compartido y ambas aplicaciones, incluidas sus pruebas. |
| `npm run build` | Aprobado | Construcción de ambas aplicaciones; Vite advierte sobre el tamaño del bundle administrativo. |
| Repetición final del detalle y tipos administrativos | 9 aprobadas y typecheck aprobado | Incluye la retirada de datos y el descarte de respuestas de una sesión anterior. |

Los reportes backend se generan en `target/surefire-reports/` de cada servicio. [EV-07: resumen de comandos y reportes](./evidencia/EV-07-pruebas-locales.txt) conserva los resultados mínimos sin tokens ni URLs firmadas reales. La construcción general precede al ajuste final de generación de consultas; ese ajuste quedó cubierto por la repetición de las nueve pruebas y el typecheck administrativo. La distinción final entre ausencia histórica e inconsistencia de la referencia vigente se compiló con Maven; su comprobación PostgreSQL sigue pendiente.

## 3. Registros y trazabilidad

### EV-01. Consulta canónica, datos y seguridad

- T-04/05: implementados `DetalleIncidenciaJdbc`, DTO, política `AccionesIncidencia`, caso de uso y controlador, sin escrituras por leer.
- La selección usa la última incidencia, admite consulta histórica, lee recepción/liberación de la misma salida y ordena historial/comunicaciones en SQL. `REPEATABLE_READ` termina antes de enriquecer por HTTP.
- Pruebas locales aprobadas: restricciones combinadas con máximo tres, contador superior al máximo, consulta histórica, datos operativos desconocidos, whitelist de historial con `false`/`null`, autorización previa y errores 400/404/500.
- **Resultado local: Aprobado.** PostgreSQL con dos ciclos, ausencia de escrituras y migraciones reales: **No ejecutado**.

### EV-02. Base y componentes

- T-01: herramientas existentes, tipos, build y pruebas reproducibles comprobados. Se reutilizan CR-08 `EstadoVista`, CR-18 `VisorEvidencia` y CR-19 `HistorialEstados`, además de encabezado y badges.
- No se duplicaron componentes ni se reimplementaron HTTP/permisos dentro de la biblioteca visual.
- **Resultado local: Aprobado para reutilización y presentación cubierta.** Foco del modal, ampliación y revisión visual con teclado/móvil en navegador: **No ejecutado**; T-02 sigue en curso.

### EV-03. Datos operativos y evidencia

- T-06: se reutiliza el lote existente de Operación con límite total de cinco segundos, incluida la credencial técnica, fuera de la transacción local. Su degradación conserva nombres/jornadas desconocidos.
- T-07: el Gestor consulta evidencia histórica sin perfil local. Un repartidor requiere perfil activo y propiedad local; se valida asociación antes de firmar. La vigencia proviene del parámetro de Operación.
- La firma usa el adaptador de Supabase privado propuesto en arquitectura; la respuesta se comprueba por ruta, HTTPS y vencimiento. Sin configuración devuelve indisponibilidad. No se implementó carga/asociación de F-03 ni se almacenaron URLs temporales.
- Cinco pruebas aprobadas: Gestor y renovación; perfil inactivo/propiedad ajena; referencia ausente/no asociada/política inválida; HTTP humano/no-store/cuerpo inválido; firma privada y objeto eliminado.
- **Resultado con dobles: Aprobado.** Storage, identidades reales y proveedor operativo real del detalle: **No ejecutado**.

### EV-04. Página, actualización y navegación

- T-03/08: ruta desde el listado y acceso directo; resumen, recepción, historial y comunicaciones; consulta histórica; autorización de foto separada y acciones basadas en códigos del backend.
- Se preserva `selloIntacto=false`, se distingue liberación pendiente de retorno confirmado y no se heredan recepción ni foto de otra salida.
- Actualización de 30 segundos en vista activa, sin superponer lecturas; decisiones bloqueadas mientras actualiza o falla. Cancelación y generación de consultas impiden que respuestas anteriores de otro recurso o sesión reemplacen la vigente.
- El visor retira URL al vencer, cerrar, cambiar de incidencia o perder autorización; renueva de forma explícita. Un rechazo de foto permanece en su bloque; un 401 revoca el detalle.
- Nueve pruebas con fixtures aprobadas. Incluyen teclado para regresar y preservación de filtros/página/tamaño en URL, además de descartes y recuperación.
- **Resultado con fixtures: Aprobado.** Recorrido real y revisión responsive en navegador: **No ejecutado**.

### EV-05. Comandos y ausencia de efectos

- `DestinosDetalleIncidencia` transporta identidad de despacho/incidencia y versión a formularios propietarios. Su callback refresca tras recepción/conflicto y regresa al listado tras resolución.
- ES-F04-03/04/05 siguen pendientes; las acciones sin destino integrado se deshabilitan con explicación visible. No se enviaron comandos ficticios.
- Las pruebas de lectura no llaman a mutaciones de negocio; esto no sustituye la comparación de snapshots reales de contador, recepción, reservas, historial y outbox.
- **Resultado integral: No ejecutado.** T-09 bloqueada por los formularios propietarios; Gerardo coordina su implementación posterior.

### EV-06. Preparación documental anterior

- Registro previo del 15/10/2026: carpeta SDD migrada desde `0b32afc`, once CA, ocho CUI, diez tareas y seis registros de evidencia.
- La revisión documental previa registró 380 enlaces/anclas válidos y 24 ejemplos JSON; esos resultados históricos no se atribuyen a esta ejecución ni acreditan comportamiento funcional.
- **Resultado histórico: Aprobado exclusivamente para preparación documental.** Esta actualización conserva criterios y contratos [cite: 1, 2].

### EV-07. Comandos locales de esta implementación

- Gestión: Maven local con `-q -o -Dtest=ConsultarDetalleIncidenciaTests,DetalleIncidenciaJdbcTests,ControladorDetalleIncidenciaTests test`.
- Operación: Maven local con `-q -o -Dtest=AutorizarLecturaEvidenciaTests,FirmadorSupabaseTests,ControladorLecturaEvidenciaTests test`.
- Frontend: `npm run test -w @despacho/administrativo -- src/features/entregas-fallidas/PaginaDetalleIncidencia.test.tsx`, `npm run test:f04`, `npm run typecheck`, `npm run build` y repetición del typecheck administrativo.
- El wrapper de Gestión apuntaba a Maven 3.10.0 sin instalación local; se utilizó la distribución 3.9.16 ya instalada. Se descargó la dependencia de dotenv incorporada en `develop`, sin cambiar el POM. Mockito necesitó ejecutar las pruebas fuera del aislamiento para instrumentar la JVM local.
- Un primer pase detectó un desempaquetado nulo al representar atraso desconocido y un restubbing incorrecto del test HTTP; ambos se corrigieron. La revisión final cubrió también respuestas anteriores a un cambio de sesión. Los resultados finales se registran en §2.

## 4. Cobertura integral pendiente

| Criterios | Código y comprobación local disponibles | Para aceptación integral |
|---|---|---|
| CA-01/04/06/08/11 | GET, snapshot, historial y whitelist; reglas/HTTP con dobles. | PostgreSQL con múltiples ciclos, historial producido por comandos y snapshots sin efectos. |
| CA-02/03/05/09 | Autorización y firma; estados del visor y retirada de datos; degradación operativa. | Identidad, bucket privado y objetos reales; renovación/descarga autorizada real. |
| CA-07/10 | Política combinada, panel, temporizador y regreso con URL; callbacks preparados. | Formularios ES-F04-03/04/05, concurrencia 409 e integración real. |
| CUI-01 a CUI-07 | Nueve pruebas de página/hooks/panel y regresión del listado/sesión. | Recorridos conectados y comandos propietarios. |
| CUI-08 | Controles semánticos, razones asociadas y regreso mediante teclado; layout responsive en código. | Inspección en navegador móvil, foco del modal y ampliación real. |

Todos los criterios integrales permanecen **Pendiente** hasta reunir esas comprobaciones. No se marca una tarea como completada por escribir su código cuando su cierre exige integración real.

## 5. Pendientes concretos

| Hallazgo | Próxima acción |
|---|---|
| Colisión heredada de Gestión: `V3__programacion_despachos.sql` y `V3__zonas_codigos_postales.sql`. | Consultar historial Flyway de cada entorno antes de decidir numeración; no alterar checksums aplicados por conjetura. |
| Migraciones nuevas preparadas: Gestión V5 y Operación V3. | Ejecutar y validar con PostgreSQL después de resolver la colisión; verificar datos por salida y productores de historial. |
| Storage privado sin configuración/objeto real comprobados. | Configurar `EVIDENCIAS_STORAGE_URL`, `EVIDENCIAS_BUCKET` privado y `EVIDENCIAS_CLAVE_SERVICIO` solo en Operación; coordinar asociación de F-03. |
| T-09 sin formularios ES-F04-03/04/05. | Implementar sus comandos y formularios y conectarlos a los destinos preparados; no cambiar reglas dentro de la consulta. |
| Revisión visual y humana pendiente. | Recorrer móvil, foco, ampliación y teclado con Gerardo; luego registrar aceptación de CA/CUI. |

Se comprobaron 224 enlaces locales en los Markdown modificados y `git diff --check` finalizó sin errores. Esta comprobación es documental y no acredita los CA funcionales.

## 6. Uso de IA y entrega

Gerardo pidió implementar ES-F04-02 siguiendo plan/tareas y las reglas de AGENTS/CONTRIBUTING, desde `develop` en código y `main` en specs, con commits Conventional Commits en español y pruebas esenciales. Codex preparó código, pruebas y esta evidencia. La revisión técnica/humana y la publicación de ramas quedan pendientes; no se solicitó desplegar ni publicar.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md), [UI](./ui.md), [plan](./plan.md) y [tareas](./tasks.md).
- [cite: 2] [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02), [Operación §3.5](../../integraciones/api-contract-operacion-reparto.md#35-autorizar-la-lectura-de-evidencia) y [modelo de datos](../../arquitectura/modelo-datos.md).
