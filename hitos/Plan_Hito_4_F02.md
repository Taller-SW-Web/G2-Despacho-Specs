# Plan de F-02 para el Hito 4 · Programación y asignación

**Responsable:** Tarqui.

**Fecha de preparación:** 05/11/2026.

**Estado:** Ejecución local parcial iniciada el 05/11; integración publicada y aceptación pendientes.
**Entrega objetivo:** 07/11/2026, según el README documental. Confirmar el alcance con el profesor conforme al plan general [cite: 1].

## 1. Objetivo y límites

Preparar en los tres repositorios un caso reproducible en nube: consultar la cola, asignar un despacho a una jornada activa con capacidad y comprobar que aparece en la ruta real del repartidor. Continuar con el mismo despacho en F-03/F-04 y verificar por separado recepción, liberación y reprogramación. F-02 no implementa la sesión, la entrega fallida ni la administración de flota: coordina esas dependencias con sus responsables [cite: 1, 2].

Este documento coordina la entrega, no sustituye la funcionalidad padre, los ocho planes SDD ni los tres contratos. Los IDs `H4-F02-*` identifican trabajo del hito; los `CA-*`, `CUI-*`, `T-*` y `EV-*` de cada atómica conservan su significado y numeración [cite: 2, 3].

### 1.1. Prioridades

- **P0 — Demo principal:** sesión real del gestor, zona y jornada preparadas, cola, asignación, reserva tridimensional y ruta propia en F-03; evidencia del recorrido publicado y enlace con F-04.
- **P1 — Consolidación de lo existente:** contrastar rutas, secuencia, reasignación, cancelación y auditoría del backend con contratos y pruebas. No confundir código presente con operación aceptada.
- **P2 — Ampliaciones condicionadas:** interfaz administrativa de rutas/reasignación y barras de ocupación absoluta, tras acordar los datos del proveedor. No bloquean el recorrido mínimo por sí mismas, pero siguen pendientes para completar sus criterios de F-02.
- **Integración externa independiente:** recepción desde Ventas y datos físicos de G6. Si entra en la demo, pasa a P0 y requiere contrato compatible y credenciales reales; una simulación etiquetada no acredita ese recorrido.

La prioridad no reduce los criterios de completitud de F-02: aprobar el tramo del hito no significa aprobar los CA-01 a CA-27 de la funcionalidad [cite: 2].

## 2. Línea base inspeccionada

Revisión local de código y documentos, sin ejecución funcional ni consulta nueva de PR remotos. Bases antes de estos cambios: backend `develop` en `e2d10b7`, frontend `develop` en `5c42d46` y documentación `main` en `637fa8d`.

| Área | Hallazgo verificable en el checkout | Consecuencia para el plan |
|---|---|---|
| Backend: programación | Existen `ControladorProgramacion`, `AsignarDespacho`, persistencia e intenciones recuperables bajo `servicio-gestion-despachos/src/main/java/.../programacion/`. | Reutilizar y verificar; no rehacer la asignación desde cero ni reemplazar la recuperación durable por una compensación solo en memoria. |
| Backend: rutas y cambios | Existen `ControladorRutas`, `ReasignarDespacho`, `CancelarDespacho` y `RecuperacionProgramacion`. | Contrastar los comandos realmente integrados, su exposición por Gateway y el procesador en nube. |
| Contratos administrativos | Gestión §3.2 enumera operaciones y cuerpos, pero no detalla allí las cabeceras `If-Match`/`Idempotency-Key` exigidas por el controlador de secuencia inspeccionado. | Valqui y Tarqui deben resolver y documentar el contrato antes de ampliar el consumidor; no copiar requisitos de cabecera a ciegas. |
| Frontend F-02 | `features/programacion/api.ts` consume cola, zonas, disponibles, simulación y asignación; `PaginaProgramacion.tsx` mantiene deshabilitada la pestaña de rutas. | Verificar lo existente con servicios reales; planificar rutas/reasignación como incremento, no como capacidad ya entregada. |
| Evidencia frontend | `docs/F-02-ProgramacionAsignacion.md` registra pruebas históricas con APIs simuladas y pendiente de ocupación absoluta. | Llevar referencias y SHA a la evidencia canónica; no convertir resultados de octubre en pruebas de la versión del hito. |
| Evidencia SDD | Las ocho carpetas F-02 mantienen verificación funcional pendiente. Algunos comandos previstos nombran pruebas distintas de las presentes. | Conciliar tareas y evidencia con el código y con resultados nuevos, sin marcar completado por inspección. |
| Productos | `ProductosProgramacionHttp` no muestra manejo del rechazo identificado de SKU padre y detalle D-G2-02 requerido por la documentación del 04/11. | Mantener abierta la compatibilidad de recepción; contrastar el proveedor y ajustar el consumidor con pruebas específicas. |
| CI | Backend ya verifica los tres componentes; frontend incluye suite administrativa, repartidor, tipos/build y E2E F-02 interceptado. | Conservar regresiones; acordar con Kevin/Gerardo el despliegue y la verificación posterior, que no quedan acreditados por esos jobs. |

Graphify se utilizó para localizar componentes; sus referencias pueden estar desactualizadas y se contrastaron con archivos actuales. Ninguno de los tres repositorios tiene resultados de Graphify versionados al preparar este plan.

## 3. Trabajo por repositorio y orden de ejecución

Todas las tareas siguientes comienzan pendientes. Tarqui coordina F-02; las colaboraciones no cambian los dueños definidos en el plan general [cite: 1].

| ID | Prioridad / repositorio | Trabajo y responsable | Depende de | Cierre verificable |
|---|---|---|---|---|
| H4-F02-01 | P0 / documentación | Tarqui acuerda alcance, origen del despacho (real o simulado), IDs del caso y criterios con Max, Kevin y Gerardo. | Confirmación de alcance del hito. | Guion acordado; entorno, cuentas, fecha y responsable de cada transición registrados sin secretos. |
| H4-F02-02 | P0 / documentación + backend | Tarqui y Valqui contrastan Gestión §3.2, Operación §§4.2/5.1 y convenciones externas con controladores, Swagger y respuestas reales. Resolver paginación/KPI, versiones, cabeceras, errores y recuperación de resultados. | Línea base de los servicios identificada. | Diferencias resueltas en el contrato canónico antes de modificar consumidores; inventario enlazado y pruebas de contrato asociadas. |
| H4-F02-03 | P0 / backend, dependencia transversal | Kevin y Valqui definen emisión, audiencia e identidad autorizada de Gestión/Operación. Tarqui verifica reserva/compensación de asignación con esa credencial. | Decisión de autenticación interna y ambiente. | Servicio autorizado puede reservar; token humano u otro servicio se rechazan. No solicitar los seis scopes internos a G7 ni quitarlos sin mecanismo sustituto acordado. |
| H4-F02-04 | P0 / backend + frontend | Tarqui verifica simulación si se autoriza, cola y asignación ya existentes; corrige únicamente brechas reproducidas. Kevin prepara jornada, vehículo y vínculo de repartidor; Valqui prepara zona activa. | H4-F02-01/02/03; sesión de Max. | Un despacho pasa de `PENDIENTE_ASIGNACION` a `ASIGNADO`, sale de cola y conserva jornada, secuencia, reserva y auditoría; ocupación antes/después en kg, m³ y paquetes. |
| H4-F02-05 | P0 / ambas apps + backend | Tarqui y Max comprueban la asignación en la ruta propia de F-03 a través del Gateway, sin fixtures ni demo en memoria. | H4-F02-04; sesión y F-03 reales. | Mismo ID visible en la app del repartidor; orden y jornada coinciden; el segundo repartidor no accede al despacho ajeno. |
| H4-F02-06 | P0 / integración F-04 | Gerardo ejecuta recepción/reprogramación; Kevin comprueba liberación y Tarqui verifica la vuelta a cola. | Fallo con evidencia de Max y H4-F02-05. | `202` de recepción, confirmación de liberación y reprogramación se registran por separado. Fecha futura bloquea asignación; reserva anterior activa produce rechazo. Una nueva asignación exitosa se prueba solo al llegar la fecha y tras liberar capacidad. |
| H4-F02-07 | P1 / backend | Tarqui verifica consulta/reordenamiento de ruta y reasignación ya presentes, con revisión de Max y Kevin en sus límites de integración. | H4-F02-02/03; dos jornadas aptas para reasignar. | Secuencia continua, estados no movibles preservados, versiones y repetición exacta; transferencia sin doble reserva y ruta actualizada en F-03. Fallos intermedios recuperables sin duplicar historial. |
| H4-F02-08 | P1 / backend + documentación | Tarqui verifica cancelación en cada estado, idempotencia y auditoría; Gerardo revisa la rama `FALLIDO` y Kevin la liberación. | H4-F02-02/03; credencial externa de Ventas si se prueba realmente. | Cancelación previa al traslado retira cola/ruta y libera una sola vez; `FALLIDO` registra anulación con `202`; estados incompatibles rechazan. Repetición exacta no duplica efectos. |
| H4-F02-09 | Condicional / backend + documentación | Tarqui y Valqui concilian recepción con G6: línea base normativa, selección del cliente real, traducción de errores, lotes completos, cantidades, 100/101 SKU y D-G2-01/02. | Publicación normativa compatible de G6 y autorización externa de G7. | Pruebas del consumidor cubren CA-21 a CA-27 de F-02 y criterios propios de ES-F02-01; rechazo sin despacho/historial/cotización parciales. E2E real separado del proveedor controlado. |
| H4-F02-10 | P2 / frontend | Tarqui implementa con revisión de Max la pestaña administrativa de rutas, reordenamiento accesible y reasignación reutilizando cliente/componentes existentes. | H4-F02-02/07; `spec.md`, `ui.md`, `plan.md` de ES-F02-05/06 y diseño vigentes. | Guardar/descartar, teclado, foco, estados bloqueados, concurrencia y resultado incierto cubiertos; ambas rutas se renuevan tras reasignación. Sin nueva biblioteca sin justificación. |
| H4-F02-11 | P2 / Operación + frontend | Kevin y Valqui confirman si el proveedor publicará totales, ocupación y vehículo; Tarqui adapta las barras solo tras el acuerdo. | Contrato de disponibilidad revisado y datos reales. | Proyección tridimensional calculada desde datos publicados y validada. Si solo hay remanente, mostrar unidades sin inventar porcentajes; CUI-03 de ES-F02-04 sigue pendiente. |
| H4-F02-12 | P0 / tres repositorios | Tarqui consolida evidencia SDD; Gerardo revisa resultados y Kevin identifica la revisión publicada y pipeline. | Pruebas del tramo entregado y comprobaciones posteriores al despliegue. | Evidencia con SHA por repositorio, revisión/imagen, URLs, IDs, comandos, respuestas saneadas, capturas y aprobación humana explícita. Pendientes P1/P2 y externos conservan responsable. |

### 3.1. Secuencia propuesta hasta la entrega

1. **05/11 — Preparar y desbloquear:** H4-F02-01/02/03; revisar credenciales, zona, jornada y sesión. En paralelo, conciliar pruebas existentes y preparar datos negativos en ambiente aislado.
2. **06/11 — Integrar y verificar:** H4-F02-04/05/06; ejecutar regresiones y revisar H4-F02-07/08. Atender H4-F02-09 si se acordó recepción real como parte de la demo. No comenzar P2 a costa de dejar P0 sin evidencia.
3. **07/11 — Ensayar y cerrar:** repetir el recorrido publicado sobre la revisión candidata, registrar H4-F02-12 y validar funcionalmente con el equipo. No promover si fallan reserva, ruta propia o seguridad. Ajustar fechas con el equipo; no representan compromisos ya aceptados.

## 4. Matriz de verificación

Los criterios siguientes pertenecen a la **funcionalidad padre**. Cada resultado se registra además con los IDs locales de su atómica; no asumir que el mismo número significa lo mismo en ambos documentos [cite: 2, 3].

| Caso | Criterios padre / atómicas | Resultado a comprobar |
|---|---|---|
| Cola, filtros y simulación autorizada | CA-03/04/05/13/20; ES-F02-02/03 | Paginación, KPI y fecha del servidor coherentes; simulación identificada; futuro solo lectura; errores sin contenido operativo residual. |
| Asignación y ruta propia | CA-06/10; ES-F02-04/05/08 + F-03 | Reserva única en las tres dimensiones, despacho retirado de cola, jornada/secuencia visibles desde el repartidor y auditoría con actor/UTC. |
| Rechazos de asignación | CA-05/07/08/09/13; ES-F02-04 | `401` sin token, `403` sin permiso; `422` por cada dimensión; `409` ante inhabilitación, fecha futura, concurrencia o reserva anterior activa, sin efectos parciales. |
| Secuencia y reasignación | CA-14/15/16; ES-F02-05/06/08 | Reordenar solo `ASIGNADO`; rechazar secuencia inválida o versión obsoleta; traslado concurrente no se sobrescribe; transferencia recuperable y sin duplicados. |
| Cancelación | CA-17/18/19; ES-F02-07/08 | Éxito/`409`/`202` según estado y contrato; repetición exacta conserva respuesta y libera solo una vez. Usar un despacho adicional para no destruir el caso principal. |
| Recepción externa | CA-01/02/11/12/21 a CA-27; ES-F02-01/08 | Idempotencia por pedido/clave, zona activa, carga física íntegra, errores D identificados y ausencia de persistencia parcial. No depende de cotización previa. |
| Continuidad F-04 → F-02 | CA-13; ES-F02-03/04 + F-04/F-06 | Reprogramación visible sin esperar a la fecha, contador conservado, reserva anterior liberada antes de nueva salida. No adelantar fecha en una base compartida para forzar el caso. |
| Recuperación y seguridad interna | ES-F02-04/06/07/08 + contratos internos | Reinicio/respuesta perdida no duplica reserva, transferencia, liberación ni auditoría; identidad de servicio autorizada y rechazo de identidades ajenas. |

### 4.1. Comandos previstos, no ejecutados en esta planificación

Backend: desde cada servicio afectado (`servicio-gestion-despachos`, `servicio-operacion-reparto` y `api-gateway` si cambia enrutamiento/seguridad), usar Java 21 y Docker/Testcontainers:

```bash
./mvnw clean verify
```

Pruebas existentes localizadas en Gestión: `ProgramacionHttpTests`, `RutasHttpTests`, `ReasignacionHttpTests`, `CancelacionHttpTests` y `ContratoCapacidadF06Tests`. Antes de sustituir los comandos previstos de `evidence.md`, confirmar cobertura por criterio; el nombre de una clase no garantiza cobertura completa. No ejecutar contra Supabase ni bases de trabajo.

Frontend: desde la raíz, con la versión de Node acordada (CI actual: Node 22) y dependencias del lockfile:

```bash
npm ci
npm run test:f02
npm run test:administrativo
npm test
npm run test -w @despacho/repartidor
npm run typecheck
npm run build
npm run test:f02:e2e
```

Preparar Chromium conforme al README antes del E2E. `test:f02:e2e` intercepta APIs: acredita regresión del consumidor, **no** integración en nube. Registrar aparte el ensayo en navegador con APIs reales y cuentas G7. No lanzar E2E que escriba en servicios reales sin un entorno de prueba autorizado.

## 5. Evidencia y criterio de salida

- [ ] Registrar en cada `evidence.md` afectado: entorno, fecha, SHA de los tres repositorios, revisión desplegada, comprobación exacta, resultado y limitaciones. Diferenciar inspección, prueba con doble, integración local, nube y aceptación humana.
- [ ] Conciliar `tasks.md`/`plan.md` con nombres y mecanismos reales solo después de revisar cada atómica. Conservar IDs y antecedentes; no cerrar tareas pendientes solo porque existan clases similares.
- [ ] Guardar ID de despacho/pedido, repartidor, jornada y reserva; peticiones/respuestas sin JWT, credenciales ni datos personales reales. Capturar cola antes/después, capacidad y ruta propia con el mismo caso.
- [ ] Enlazar pipeline → SHA → revisión publicada → prueba posterior al despliegue. Gerardo/Kevin mantienen la prueba de humo común de Gateway/F-04; F-02 añade su evidencia funcional sin sustituirla.
- [ ] Tarqui valida el recorrido y otro integrante revisa los cambios; registrar por separado qué quedó aceptado y qué continúa bloqueado. Si solo se logró un recorrido simulado, declararlo y no dar por entregada la integración real.

La evidencia canónica permanece en las ocho carpetas [SDD de F-02](../funcionalidades/funcionalidad.md#especificaciones-atómicas-de-f-02). No crear copias de contratos o nuevas especificaciones para el mismo comportamiento. Código por ramas desde `develop` y PR a `develop`; documentación desde `main` y PR a `main`. Changelog y tag se preparan únicamente al publicar una línea base aprobada [cite: 3, 4].

## 6. Higiene de Graphify

Añadir `graphify-out/` sin anclar a la raíz en los seis `.gitignore` mantenidos de estos tres repositorios, incluidos los tres componentes Java. Así se excluyen resultados, cachés y exportaciones dentro del directorio de salida también en subcarpetas. Las exportaciones deliberadas a rutas personalizadas requieren revisar su exclusión específica.

Comprobar con `git check-ignore` rutas de muestra en raíz y subcarpetas, y con `git ls-files` que no haya resultados ya versionados. No borrar grafos locales ni desversionar trabajo ajeno automáticamente. Esta tarea de mantenimiento no implica regenerar grafos ni ejecutar pruebas funcionales.

## 7. Registro de ejecución del 05/11/2026

Rama nueva en los tres repositorios: `feature/f02-ejecucion-hito4`, sobre los SHA de §2. Se conservaron los cambios documentales y de `.gitignore` de la planificación, aún sin commit al iniciar esta sesión. No se realizaron commits, PR, despliegues ni cambios de datos compartidos.

### 7.1. Incremento implementado y estado de tareas

| Tareas | Avance real de esta sesión | Pendiente de cierre |
|---|---|---|
| H4-F02-01 | Preparación del caso y herramienta de verificación de solo lectura. | Acuerdo del equipo, alcance del profesor, ambiente e IDs de ensayo. |
| H4-F02-02 | Contraste estático de controladores y contratos; disponibilidad vigente sí incluye placa, límites y ocupación. Se corrigieron referencias obsoletas de reserva/compensación y seguridad en ES-F02-04. | Respuestas/Swagger del despliegue e inventario validado con Valqui. |
| H4-F02-03 | No se modificaron scopes, audiencia ni credenciales internas. | Emisión/identidad autorizada acordada por Kevin y Valqui, y comprobación en nube. |
| H4-F02-04/05 | Regresión del consumidor con APIs simuladas; nuevo `pruebas/verificar_f02_publicado.py` para comprobar una asignación ya preparada por Gateway con GET. Se reparó `verificar_f02_rutas.py`: invocaba un script npm inexistente; ahora comprueba APIs sin afirmar evidencia de navegador. | Ejecutar el entorno aislado con Docker y repetir con G7/servicios publicados. El verificador de solo lectura no crea la asignación ni prueba el balance antes/después. |
| H4-F02-06 | No se ejecutó el recorrido integrado F-04. | Fallo con evidencia, recepción, liberación y reprogramación reales. |
| H4-F02-07/08 | Suites completas intentadas con JDK 21; integración PostgreSQL bloqueada por Docker. | Reordenamiento, transferencia, cancelación y auditoría persistente verificadas; resolver discrepancia de secuencia descrita debajo. |
| H4-F02-09 | No se cambió el cliente G6 ni se declaró compatible. | Línea base normativa, credenciales y pruebas del consumidor D-G2-01/02. |
| H4-F02-10 | Sin implementación de rutas administrativas o reasignación en esta sesión. | Acordar semántica de secuencia y completar contrato antes de habilitar escrituras. |
| H4-F02-11 | Integradas placa, búsqueda por placa, ocupación absoluta y proyección tridimensional desde los datos que el contrato ya publica. Reutiliza CR-11/CR-20; rechaza respuesta incompleta o capacidad incoherente. | Verificar proveedor publicado, aceptación humana y revisión de Max/Valqui/Kevin. No se cierra el criterio como integración real. |
| H4-F02-12 | Resultados locales registrados en este plan y en EV-04 de ES-F02-04. | SHA del incremento aprobado, pipeline remoto, revisión publicada y aceptación humana. |

**Discrepancia abierta de secuencia:** ES-F02-05 exige `1..N` sin huecos y conservar posiciones de paradas iniciadas. El backend `ValidadorSecuencia` permuta los espacios vigentes, y `RutasHttpTests.conservaHuecosHistoricosYJornadaCerradaEsSoloLectura` acepta conservar huecos históricos. `ControladorRutas` exige además `If-Match` e `Idempotency-Key`, aún sin detalle equivalente en Gestión §3.2. Tarqui y Valqui deben acordar el tratamiento de una cancelación/reasignación que deja huecos antes de cambiar contrato, pruebas o consumidor. Esta sesión no modifica criterios para hacer coincidir las pruebas con el código.

### 7.2. Verificaciones realizadas y limitaciones

- Frontend: pruebas administrativas, componentes compartidos, repartidor, TypeScript, construcción y cuatro recorridos Chromium con API interceptada; resultados detallados en [EV-04 de ES-F02-04](../especificaciones/ES-F02-04-AsignarDespachoRepartidor/evidence.md#ev-04-incremento-local-del-hito-4--05112026). Capturas nuevas separadas de las históricas en `docs/evidencia/f02/hito4/` del frontend.
- Backend: el primer intento con JDK 27 falló al compilar por Lombok (`EndPosTable`). Se descargó Corretto 21.0.13 al directorio temporal externo `/tmp/opencode/jdk21`, se comprobó su SHA-256 contra el proveedor y se repitió sin cambiar dependencias del proyecto.
- Gateway: `clean verify` con JDK 21 aprobado, **28 pruebas**, sin errores ni omisiones. Usa proveedores/identidades de prueba; no es el ambiente publicado.
- Gestión: `clean verify` con JDK 21 compila; **184 pruebas contabilizadas, 129 errores de integración**, sin fallos de aserción ni omisiones. La suite no aprueba: Testcontainers no encuentra `/var/run/docker.sock`.
- Operación: `clean verify` con JDK 21 compila; **131 pruebas contabilizadas, 47 errores de integración**, sin fallos de aserción ni omisiones. Mismo bloqueo de Docker; no acredita PostgreSQL ni reserva real.
- Verificador Python: **7 pruebas aprobadas** con dobles explícitos, incluida protección contra redirección de Bearer; job añadido al workflow backend. Su ejecución contra un despliegue sigue pendiente por falta de origen, IDs y sesiones suministradas para el ensayo. No se imprimieron ni guardaron JWT.
- No se usó Supabase, no se iniciaron migraciones compartidas, no se alteraron cuentas G7 y no se activó un modo sin autenticación para hacer pasar la demo. Se preservó la validación del backend.

Comandos realmente ejecutados desde cada raíz/servicio correspondiente:

```bash
# Backend: en cada uno de los tres componentes; JAVA_HOME temporal apunta a Corretto 21.
./mvnw --batch-mode --no-transfer-progress -Dpruebas.postgres.externo=false clean verify
# Verificador: desde la raíz del backend; prueba la herramienta, no el despliegue.
python3 -B -m unittest discover -s pruebas -p 'test_verificar_f02_publicado.py' -v
# Frontend: dependencias existentes; no se regeneró el lockfile.
NODE_OPTIONS=--no-experimental-webstorage npm run test:administrativo
NODE_OPTIONS=--no-experimental-webstorage npm test
NODE_OPTIONS=--no-experimental-webstorage npm run test -w @despacho/repartidor
npm run typecheck
npm run build
npm run test:f02:e2e
```

El Gateway se verificó sin el parámetro de PostgreSQL, que no necesita. Los reportes Maven permanecen en `target/surefire-reports/`; registros locales de esta ejecución en `/tmp/opencode/f02-*.log`, no versionados. Ningún resultado local cierra por sí solo las tareas del hito que exigen nube, revisión o aceptación humana.

### 7.3. Reanudación

1. Disponer de Docker con permiso de uso y repetir `clean verify` de Gestión/Operación. No sustituir Testcontainers por una base compartida ni omitir pruebas para obtener aprobación.
2. Con los tres JAR aprobados, ejecutar el recorrido aislado `python3 -B pruebas/verificar_f02_rutas.py`; usa Compose de pruebas y Seguridad temporal. La reparación de su invocación se inspeccionó, pero el recorrido no se ejecutó por Docker. No se presenta como prueba de navegador ni G7.
3. Acordar identidad interna y diferencias contractuales con los responsables. Mantener G6 y rutas administrativas pendientes hasta resolver sus condiciones.
4. Para la versión publicada, preparar el despacho y las cuentas por el flujo real; aportar al verificador origen, tres sesiones distintas, IDs y SHA mediante variables de entorno privadas según el README backend. Ejecutarlo antes del traslado y guardar el JSON saneado junto al balance antes/después y las capturas de ambas apps.
5. Completar con Max/Gerardo/Kevin el fallo, la recepción, la liberación y la reprogramación. Registrar aprobación solo después de comprobar cada resultado.

## 8. Continuación: rutas y reasignación seguras

Continuación local del 05/11/2026 en la misma rama, sin descartar los cambios anteriores. Este registro actualiza el alcance del consumidor descrito en §7; no declara resueltos los pendientes externos.

- **H4-F02-02:** se precisó en los contratos canónicos el transporte ya exigido por los controladores de ruta/secuencia y reasignación. `If-Match` de ruta y versión numérica de parada no se intercambian; ambas operaciones conservan clave y contenido para recuperar respuestas. La transferencia interna ya existente se registra en Operación §5.5, sin pedir permisos nuevos a G7.
- **H4-F02-07/10:** consulta de rutas y reordenamiento del subconjunto compatible implementados en Administración. Botones de teclado y arrastre, guardar/descartar, paradas iniciadas fijas y recuperación del comando exacto. Una ruta con huecos, jornada cerrada o comandos pendientes no admite reordenamiento desde la UI. No se compactan huecos ni se cambian los CA controvertidos.
- **H4-F02-10:** modal de reasignación implementado: origen excluido, motivo, validación tridimensional, versiones y doble envío. Un `503` o `409 DESP_ERROR_REASIGNACION_EN_PROCESO` conserva el comando para recuperación explícita, sin otra transferencia. Tras éxito se consulta el origen y se renueva el catálogo; el destino se consulta al seleccionarlo, sin caché antigua.
- **Backend publicado:** el perfil `render` del Gateway omitía la ruta específica de programación al reemplazar la lista de rutas local. Se corrigió su precedencia hacia Gestión y se añadió una prueba que distingue Gestión/Operación y comprueba ETag, CORS, cabeceras/cuerpo, autorización y aislamiento de API interna. No se cambió la seguridad de Gestión/Operación ni la transferencia de capacidad.
- **Verificación local:** Gateway `clean verify` con Corretto 21.0.13: **29 pruebas aprobadas**. Frontend: **209 pruebas administrativas**, tipos y build de ambas apps correctos y **7 recorridos Chromium** con API interceptada, incluidos los tres tamaños de rutas/reasignación. Siete pruebas Python del verificador vuelven a aprobar. Capturas sintéticas y evidencia canónica en [ES-F02-05 EV-04](../especificaciones/ES-F02-05-ConsultarReordenarSecuenciaRuta/evidence.md#ev-04-incremento-seguro-de-rutas-del-hito-4--05112026) y [ES-F02-06 EV-04](../especificaciones/ES-F02-06-ReasignarDespachoRepartidor/evidence.md#ev-04-reasignación-desde-administración--05112026).
- **Conservados pendientes:** G6/D-G2-01/02, emisión/audiencia de identidad interna, aclaración de huecos, Docker para pruebas PostgreSQL, ensayo con G7 y aceptación humana. Docker sigue sin daemon disponible. No se repitieron suites persistentes sobre una base alternativa, no se publicaron ramas ni se desplegó este incremento. No hay un SHA aprobado nuevo que atribuirle.

## 9. Referencias

- [cite: 1] [Plan general del Hito 4](./Plan_Hito_4_Despacho.md), reparto, dependencias de Seguridad y demo integrada; [README](../README.md), fecha objetivo comunicada.
- [cite: 2] [F-02: programación y asignación](../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), alcance y criterios; [Gestión §3.2](../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación), [Operación](../integraciones/api-contract-operacion-reparto.md) y [contrato externo](../integraciones/api-contract.md), únicas fuentes contractuales.
- [cite: 3] [Índice de atómicas F-02](../funcionalidades/funcionalidad.md#especificaciones-atómicas-de-f-02) y [guía SDD](../plantillas/sdd/README.md); sus planes, tareas y evidencias conservan el seguimiento por criterio.
- [cite: 4] [Flujo de contribución](../CONTRIBUTING.md), ramas, revisión y versiones.
