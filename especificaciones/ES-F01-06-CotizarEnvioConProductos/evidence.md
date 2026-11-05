# Evidencia de ES-F01-06: Cotizar el envío con datos físicos de productos

**Estado:** Implementación y automatización local verificadas el 05/11/2026; integración real y aceptación pendientes.

**Responsable de verificación:** Valqui.

**Última verificación funcional:** 05/11/2026, Gestión, 231 pruebas aprobadas; proveedor G6 simulado explícitamente.

## 1. Versión y entorno verificados

### Ejecución local del consumidor — 05/11/2026

- Backend: `G2-Despacho-Backend`, rama `feature/f01-integracion-g6-cotizaciones`, cambios de trabajo sobre `6af187c`. Documentación: `docs/f01-integracion-g6-redondeo`, sobre `637fa8d`. Cambios sin commit de entrega en esta sesión.
- Java Temurin 21.0.9, Maven Wrapper, Docker 29.9.2 y PostgreSQL 17/PostGIS en contenedores desechables. No se aplicaron migraciones a Supabase ni a la base local de trabajo.
- Comando final, ejecutado dentro de `servicio-gestion-despachos`:

```bash
JAVA_TOOL_OPTIONS="-Dspringdotenv.enabled=false -Dpruebas.postgres.externo=false -Dlogging.level.root=ERROR -Dlogging.level.com.modulodespacho=OFF" ./mvnw clean verify
```

- Resultado final: **BUILD SUCCESS**, 231 pruebas, 0 fallos, 0 errores, 0 omitidas; finalizó el 05/11/2026 a las 13:08:46 UTC−05. Artefactos locales: `target/surefire-reports` y JAR verificado de Gestión. Las propiedades fuerzan contenedores, deshabilitan dotenv y reducen logs; no omiten pruebas. La ejecución anterior aprobó 230 pruebas; la última añade validación estricta de tipos sin alterar la precedencia de cobertura.
- Se corrigieron durante el incremento: enlace JDBC de `Instant`, valor opcional postal al deserializar, reloj fijo de pruebas, construcción del manejador en cortes MVC y expectativas de versión final de migración (ahora V10). Se conservaron aserciones de regresión y de datos previos; la primera ejecución completa falló y la repetición final aprobó.
- Pruebas relevantes: `CotizacionG6HttpTests` (12), `ClienteDatosFisicosHttpTests` (7), `RedondeoCotizacionTests` (16), `FlujoF01Tests` (13), `LimiteCotizacionesHttpTests` (2), `CalculadoraCotizacionTests` (3) y `ControladorCotizacionTests` (6). El resto corresponde a regresión de Gestión, incluidas Programación e Incidencias.
- Comprobaciones auxiliares: `docker compose --env-file .env.example config --quiet` y `git diff --check` de ambos repositorios, aprobados. Verificador documental temporal `python3 /tmp/opencode/validar_f01_20261105.py`: 17 Markdown, 433 enlaces locales/anclas, 31 ejemplos JSON y 20 criterios de ES-F01-06, sin errores. La primera pasada del verificador se corrigió para reconocer las anclas HTML explícitas existentes.
- Perfil normal: cliente HTTP real de G2 contra servidor de prueba en loopback, ruta canónica, token propio distinto del canal y ausencia de transacción durante la llamada. El catálogo local requiere `productos-simulados` explícito.
- Persistencia real: correspondencia de respuesta y tarifa capturada, precisión de peso, volumen/costo redondeados, perfiles y cantidades en `detalle`, vínculos nulos, repetición con instantáneas independientes y conservación tras sustituir tarifa. Fallos tanto de inserción como de commit produjeron `500` contractual y cero filas parciales. V8–V10 se aplicaron en contenedores; se verificó también migración desde V2/V3 con datos previos.
- Configuración: reintentos administrativos durables, rechazo de reutilización, cobertura exclusivamente postal y filtro distrital, colisiones concurrentes `409`, conservación de zona en despacho previo, histórico tarifario y rollback si falla auditoría.
- Referencia externa inspeccionada: informe G6 fijado al merge `eeaf39ad666d7bc5a11c0b2a80d9c8c4b0016414`. El intento de consultar el OpenAPI en la rama `main` de su repositorio devolvió `404`; no se acreditó una publicación normativa posterior a la ya enlazada en el contrato.
- Límites: G6 y los JWT entrantes de las pruebas F-01 son dobles; la regresión incluye además criptografía con emisor controlado. No se ejecutaron G6/G7 reales, recorrido con canales/Gateway, UI, matriz padre/variante en el proveedor ni medición de 100 ms. Feriados/horas de corte y consumo remoto de cobertura desde Operación conservan coordinación pendiente.

| Criterios | Evidencia ejecutada | Resultado y límite |
|---|---|---|
| CA-01, CA-03 y CA-10 | Flujo zona/tarifa/cotización, cálculo, líneas y omisión de totales del canal | Aprobado local; proveedor controlado |
| CA-02 y CA-07 | Sin cobertura incluso con líneas inválidas; cobertura sin tarifa | Aprobado local, cero llamadas y filas |
| CA-04 a CA-06 | Inexistentes identificados, error físico contractual y errores técnicos/de credencial saliente | Aprobado local; disponibilidad real pendiente |
| CA-08 y CA-09 | Token técnico/rol, autorización previa al negocio y tasa por consumidor/IP | Aprobado local; grant G7 pendiente |
| CA-11 a CA-13 | Instantáneas, precisión, sustitución, repetición, fallo de inserción y commit | Aprobado con PostgreSQL desechable |
| CA-14 y CA-16 | Integridad, tipos, fechas, estados desconocidos, 100/101 únicos, 150 líneas repetidas y overflow de cantidades | Aprobado local |
| CA-15 | Estado efectivo y rechazo de `INACTIVO`/`BORRADOR` | Aprobado consumidor; nueve combinaciones del proveedor no ejecutadas aquí |
| CA-17 a CA-19 | Afectados, detalle ausente/vacío/duplicado/ajeno/mal ordenado y permutaciones mixtas | Aprobado con doble D; normativa y recorrido real pendientes |
| CA-20 | Ejemplos, límites de medio sol y milésimos, acumulación y costo sobre volumen exacto | Aprobado unitario y PostgreSQL |

### Antecedentes de preparación documental

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), preparación del 16/10/2026 a partir de `91db8f8`.
- Repositorios y commits de código: pendientes, Gestión de Despachos y Gateway.
- Entorno, despliegue, datos y preparación: pendientes.
- Dependencias: Productos, Seguridad y canales no utilizados en esta preparación; simulaciones y servicios reales por identificar al ejecutar.
- Alcance efectivamente verificado: ningún criterio funcional ejecutado; solo preparación documental SDD.
- UI: no aplica; API consumida por canales, sin `ui.md`.

### Antecedentes comunicados y actualización del 26/10/2026

- La persona responsable aportó el DDL de `public.cotizaciones` y `zonas_codigos_postales`, aclaró que la primera solo está creada y la segunda tiene datos, y aceptó persistir únicamente cálculos exactos exitosos al completar F-01, antes de confirmar una venta.
- Se documenta `pedido_id` y `despacho_id` nulos al cotizar, exclusión de cobertura/rechazos y uso histórico del perfil físico y la tarifa. No se habilitan aceptación, vencimiento, cancelación ni asociación automática.
- El DDL comunicado contiene `pedido_id UUID`, estados físicos en minúsculas y escalas de peso/volumen que deben contrastarse con el cálculo. Esas observaciones no son un resultado de inspección de PostgreSQL.
- Se prepararon la matriz de errores, validación integral, límite de 100 SKU únicos y respuestas H-G2-01/02/03 en el [contrato §11.1](../../integraciones/api-contract.md#111-homologación-física-g2g6-y-precisiones-de-seguimiento). En aquella preparación no se publicó un comentario en GitHub ni se acreditó aceptación de G6/G7; las fuentes posteriores se registran en la actualización del 03/11.
- Alcance de esta actualización: documentación. Este workspace no contiene las clases Java reportadas; escritor, selección del cliente HTTP, grant de Seguridad y recorrido real permanecen sin ejecutar. Una tabla creada no acredita T-06 ni los nuevos criterios [cite: 3].

### Comprobación documental local del 26/10/2026

- `git diff --check`: ejecutado desde este repositorio, sin errores de formato del diff.
- Validación local en memoria con Python 3, sin crear archivos auxiliares: 33 Markdown modificados con enlaces locales, anclas y jerarquía de encabezados válidos; sin referencias a la operación física obsoleta en esos documentos.
- Se comprobaron los 16 identificadores de criterios de ES-F01-06 y los 10 de ES-F02-01 contra sus matrices de evidencia, conservando los identificadores anteriores.
- Resultado documental: correcto. No se ejecutaron pruebas funcionales, PostgreSQL ni servicios G2/G6/G7; los resultados de comportamiento de las matrices siguientes permanecen pendientes.

## 2. Cobertura de criterios

### Actualización documental del 03/11/2026

- Se contrastaron la aceptación final H-G2-01/02/03 del 02/11 y la respuesta D-G2-01/02 de G2 ya publicada el 03/11, enlazadas en el [contrato §11.1](../../integraciones/api-contract.md#111-homologación-física-g2g6-y-precisiones-de-seguimiento). El estado pendiente de homologación de los antecedentes del 26/10 corresponde a aquella fecha, no al estado actual.
- Línea base G6: OpenAPI `0.6.0-rc.3`, SHA `40b566976fb94d924116dcd01d41b3276c2bc9e3`, PR documental #108 fusionado. D-G2-01 fue aceptado por G2; campo obligatorio y precedencia D-G2-02 siguen pendientes de G6 y revisión normativa.
- El PR backend G6 #162 reporta implementación y pruebas de proveedor, en borrador y sin el campo nuevo para `SKU_INVALIDO`; es evidencia externa reportada, no ejecución del consumidor ni conformidad con la ampliación solicitada.
- Se prepararon CA-17 a CA-19, T-07/T-08 y EV-07. Ninguna comprobación funcional de esta matriz se ejecutó; la revisión documental no acredita cliente HTTP G2, persistencia, grant G7, despliegue ni E2E.

### Comprobación documental local del 03/11/2026

- Comandos ejecutados: `git diff --check` y `python3 /tmp/opencode/validar_documentacion_g2_g6.py`. El segundo utiliza un verificador temporal fuera del repositorio, preparado para revisar esta actualización.
- Alcance: 18 Markdown versionados y tres documentos personales de `trabajo-jerson/`, excluidos por `.gitignore`. Se comprobaron 408 enlaces locales y sus anclas, jerarquía de encabezados y 20 ejemplos JSON; resultado sin errores.
- Se verificaron los 19 criterios de ES-F01-06 y los 13 de ES-F02-01 contra las matrices de evidencia, la conservación de IDs anteriores, la existencia de tareas/registros referenciados y el estado pendiente de las tareas nuevas. Las funcionalidades padre contienen 32 y 27 criterios, respectivamente.
- Se confirmó la igualdad de `arquitectura/modelo-datos.md` con su versión de `HEAD` y la conservación de los tres contratos. Resultado documental correcto; ningún CA funcional se considera ejecutado o aprobado por estas comprobaciones.

### Actualización documental del 04/11/2026

- Se verificó el [comentario final de G2 del 04/11](https://github.com/Taller-SW-Web/G2-Despacho-Specs/issues/15#issuecomment-6632557247), que acepta la precedencia, el orden de solicitud y la traducción pública. Junto con la [aceptación G6 del 03/11](https://github.com/Taller-SW-Web/G2-Despacho-Specs/issues/15#issuecomment-6616780174), acredita el cierre semántico D-G2-02; D-G2-01 quedó cerrado el 03/11. Las notas anteriores describen el estado de sus respectivas sesiones.
- Se comprobó en GitHub que el PR backend G6 #162 fue fusionado el 03/11, merge `eeaf39ad666d7bc5a11c0b2a80d9c8c4b0016414`. El código y el informe del proveedor incorporan estado efectivo, todas las bases no físicas afectadas en orden de solicitud y precedencia. Las regresiones son evidencia externa reportada por G6; no se ejecutaron aquí.
- Se inspeccionó el OpenAPI publicado, versión `0.6.0-rc.3`, cuya última modificación de archivo está en `6fcd81f9151649b94ecd736f8976630b39e97dc2`. La operación aún deja pendiente el rechazo específico del padre y solo exige afectados para `DATOS_FISICOS_INCOMPLETOS`. DT-08 registra aceptación resuelta y publicación normativa/compatibilidad pendientes; las fuentes fijas están en [contrato §11.1](../../integraciones/api-contract.md#111-homologación-física-g2g6-y-precisiones-de-seguimiento).
- Se alinearon los 18 documentos previstos con el acuerdo. El escritor, la selección HTTP de G2, las regresiones del consumidor, la concesión G7 y el recorrido real conservan su verificación pendiente. Ningún criterio funcional de esta matriz se ejecutó como parte de la actualización.

### Comprobación documental local del 04/11/2026

- Comandos ejecutados: `git diff --check` y `python3 /tmp/opencode/validar_actualizacion_g2_g6.py`. El verificador temporal, externo al repositorio, lee los documentos sin modificarlos.
- Alcance: los 18 Markdown versionados de esta actualización; 397 enlaces locales y sus anclas, jerarquía de encabezados, fuentes de citas y 20 ejemplos JSON válidos. Se verificaron los IDs de 32/27 criterios en las funcionalidades padre y 19/13 en las especificaciones, cobertura en matrices, referencias a tareas/registros existentes y estado pendiente de las tareas nuevas.
- La primera pasada detectó una cita sin marcador de fuente en ES-F02-01; se regularizó y la repetición aprobó todas las comprobaciones. `git diff --check` también aprobó. Se comprobaron los tres contratos canónicos y la igualdad del modelo de datos con `HEAD`.
- Resultado documental: correcto. Las matrices funcionales, la persistencia, la autorización G7 y el E2E no se ejecutaron en esta comprobación.

### Matriz funcional

| Criterio | Tarea | Prueba o comprobación | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02 a T-05, T-06 | Totales, costo, moneda, plazo y fecha esperados; instantánea confirmada | EV-02, EV-03, EV-04, EV-05 | Pendiente |
| CA-02 | T-02, T-03, T-05 | Sin cobertura: sin costo ni llamada a Productos | EV-02, EV-03 | Pendiente |
| CA-03 | T-02, T-03, T-05 | Líneas/cantidades inválidas en destino cubierto | EV-02, EV-03 | Pendiente |
| CA-04 | T-03, T-05 | SKU inexistente identificado sin costo | EV-03 | Pendiente |
| CA-05 | T-03, T-05 | Datos físicos incompletos sin costo | EV-03 | Pendiente |
| CA-06 | T-03, T-05 | Indisponibilidad sin costo estimado | EV-03 | Pendiente |
| CA-07 | T-01, T-03, T-05 | Zona activa sin tarifa: cobertura sin costo ni plazo | EV-01, EV-03 | Pendiente |
| CA-08 | T-03 a T-05, T-06 | Token técnico sin sesión humana ni creación de pedido/despacho; instantánea exacta confirmada | EV-03, EV-04, EV-05 | Pendiente |
| CA-09 | T-04, T-05 | Exceso de límite rechazado sin cálculo | EV-04 | Pendiente |
| CA-10 | T-02, T-03, T-05 | Peso/volumen del cliente no cambian el cálculo | EV-02, EV-03 | Pendiente |
| CA-11 | T-06, T-04, T-05 | Instantánea y respuesta coherentes, vínculos nulos, tarifa histórica y repetición | EV-05, EV-04 | Pendiente |
| CA-12 | T-03, T-06, T-05 | Cobertura y cada rechazo sin filas nuevas | EV-03, EV-05 | Pendiente |
| CA-13 | T-06, T-05 | Fallo en inserción/commit revierte y no devuelve costo exitoso | EV-05 | Pendiente |
| CA-14 | T-02, T-03, T-04, T-05 | Lote malformado/incompleto rechazado íntegramente | EV-02, EV-03, EV-06 | Pendiente |
| CA-15 | T-01, T-02, T-03, T-04, T-05, T-08 | Elegibilidad por estado efectivo sin confundir inexistencia | EV-03, EV-06, EV-07 | Pendiente |
| CA-16 | T-02, T-03, T-05 | Cantidades conservadas y 1/100/101 SKU únicos | EV-02, EV-03 | Pendiente |
| CA-17 | T-07, T-08, T-04, T-05 | Rechazo íntegro con afectados exactos; producto simple válido | EV-07, EV-06 | Pendiente |
| CA-18 | T-07, T-08, T-05 | Detalle obligatorio inválido produce respuesta no conforme | EV-07 | Pendiente |
| CA-19 | T-07, T-08, T-04, T-05 | Precedencia aceptada, mismo código/conjunto de afectados y lista en orden de cada solicitud | EV-07, EV-06 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Un doble no acredita integración con el proveedor real.

## 3. Registros de verificación

### EV-01. Revisión de contrato y datos

- Tareas y criterios: T-01; soporte de todos, en particular CA-01 y CA-07.
- Preparación y pasos previstos: revisar contrato §§5.1/5.2/11.1, modelo, precisión del ejemplo, calendario y decisiones DT-01 a DT-08; utilizar las fuentes H/D cerradas y enlazar publicación normativa y compatibilidad del incremento D.
- Resultado esperado: respuesta sin tarifa y cálculo definidos en documentos canónicos.
- Fecha, persona, revisión/commit y entorno: pendientes.
- Resultado observado y artefacto de revisión: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: no se han utilizado; la revisión documental no verifica el backend.

### EV-02. Motor y validaciones

- Tareas y criterios: T-02/T-05; CA-01 a CA-05, CA-10 y CA-14 a CA-16.
- Preparación y pasos previstos: datos físicos y tarifa del ejemplo, reloj/calendario controlados; ejecutar pruebas de cálculo, recargo, SKU repetidos, líneas inválidas y cobertura previa a validación.
- Resultado esperado: totales/costo según precisión acordada, sin datos físicos autoritativos del cliente ni consulta al proveedor fuera de cobertura.
- Fecha, persona, commit, entorno y comando exacto de la suite: pendientes.
- Resultado observado y reporte: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: doble de Productos previsto; no acredita disponibilidad ni autorización reales.

### EV-03. Endpoint, seguridad e integración

- Tareas y criterios: T-03/T-05; CA-01 a CA-08, CA-10 y CA-14 a CA-16; T-06 confirma las respuestas exactas.
- Preparación y pasos previstos: PostgreSQL aislado, tokens y proveedor controlado; verificar selección real del adaptador HTTP, ruta saliente, respuestas, distrito ausente, seguridad, fallos/timeout y token propio. Comparar ausencia de filas en cobertura/rechazos y conectar el escritor exacto comprobado en EV-05.
- Resultado esperado: lote íntegro con SKU únicos y cantidades conservadas; traducción diferenciada de `422` de negocio, `502` de respuesta inválida y `503` técnico; respuesta exacta solo después de la escritura confirmada.
- Fecha, persona, commit, entorno y comando exacto de la suite: pendientes.
- Resultado observado y reporte: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: proveedor controlado previsto; indicar cuáles casos también se ejecutaron con Productos real.

### EV-04. Tasa, rendimiento y recorrido real

- Tareas y criterios: T-04/T-05, escritor T-06 y regresiones T-07/T-08; recorrido de CA-01 a CA-19, especialmente CA-08/09, persistencia exacta y requisito de latencia.
- Preparación y pasos previstos: Gateway y servicios reales identificados, consumidores técnicos, configuración de tasa/caché y carga acordada; superar límite y medir latencias de solicitudes admitidas.
- Resultado esperado: rechazo por tasa sin cálculo y respuestas conformes; contrastar latencia con menos de 100 ms según F-01 §8.
- Fecha, persona, commits, entorno y comandos/pasos exactos: pendientes.
- Resultado observado, métricas y artefactos: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: por registrar; ninguna simulación sustituye este recorrido real.

### EV-05. Persistencia exacta y rollback

- Tareas y criterios: T-06/T-04/T-05; CA-11 a CA-13 y exclusión transversal de errores.
- Preparación prevista: identificar commit backend y esquema real de `cotizaciones`; ejecutar el escritor sobre PostgreSQL aislado, comparar fila/desglose/respuesta y vínculos nulos. Sustituir tarifa y repetir solicitud; comprobar instantáneas independientes. Inyectar fallo de inserción y commit y comparar ausencia de registros parciales. Consultas de cobertura y todos los rechazos deben dejar el contador de filas sin cambios.
- Resultado esperado: una instantánea completa por ejecución exacta exitosa antes de devolver el costo, con tarifa histórica conservada y error interno al fallar la escritura; sin pedidos/despachos nuevos.
- Fecha, persona, commits, entorno, comando exacto y reporte: pendientes.
- Resultado observado: no ejecutado.
- Resultado de la comprobación: Pendiente.
- Límite: el SQL comunicado no acredita migración aplicada, escritor ni transacción ejecutados desde esta sesión.

### EV-06. Homologación física, seguridad y compatibilidad

- Tareas y criterios: T-01/T-03/T-04/T-05/T-07/T-08; CA-04/05/06/14/15/16/17/18/19 y seguridad.
- Preparación prevista: usar aceptación H, SHA rc.3 y cierre semántico D-G2-01/02 ya enlazados; agregar la publicación normativa D pendiente. Con G7 acreditar concesión y credencial de `modulo-despacho`; ejecutar token ausente, inválido/vencido, audiencia incorrecta, scope ausente/correcto y consulta real desde F-01/F-02, incluidos CA-17 a CA-19 con la revisión exigible.
- Resultado esperado: reglas aceptadas y respuestas contractuales sin aproximaciones; elegibilidad distinta en cotización y pedido pagado, sin confundir estado e inexistencia.
- Enlaces bilaterales y merge proveedor: disponibles en contrato §11.1. Publicación normativa D, grant, commits del consumidor, entorno, comandos y resultados funcionales: pendientes.
- Resultado observado: no ejecutado.
- Resultado de la comprobación: Pendiente.
- Límite: una respuesta propuesta, un código en enum global o un doble HTTP no acreditan homologación, autorización ni E2E.

### EV-07. Estado efectivo y rechazo identificado D-G2-01/02

- Tareas y criterios: T-07/T-08, revisión T-05 y recorrido T-04; CA-15 y CA-17 a CA-19.
- Preparación prevista: fijar revisión normativa D y datos de nueve combinaciones padre/variante, simples y SKU opacos. Probar padres solos/múltiples/mixtos, la lista de afectados y errores con campo ausente/vacío, tipos inválidos, duplicados y SKU ajenos. Permutar lotes según la precedencia aceptada del contrato §5.2.4: mismo código/conjunto de afectados y lista en orden de cada solicitud. Incluir ausencia de bases con perfiles incompletos, `200` con inexistentes y fallos técnicos.
- Resultado esperado: F-01 rechaza estados efectivos no elegibles; conserva los afectados del rechazo de padre o produce `502` si incumple el detalle exigible. Sin costo, cotización nueva ni éxito parcial; simples válidos continúan. La lista corresponde al error seleccionado y no certifica las otras líneas.
- Dependencias: publicación normativa/compatibilidad de DT-08; aceptación semántica resuelta. El campo no se exige a la línea base rc.3 anterior. Dobles del acuerdo identificados como tales; fuente G6 y emisor de token reales/simulados por registrar.
- Revisión, commits, entorno, comandos, reportes y resultados observados: pendientes.
- Resultado: **No ejecutado**. El cierre semántico bilateral y el merge G6 no acreditan implementación ni regresiones del consumidor G2.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| Migración y preparación SDD | OpenCode, 16/10/2026 | Original, F-01, contratos y modelo en `91db8f8`; plantillas SDD y modelo ES-F01-05 | Completar las carpetas ES-F01-06, ES-F01-07 y ES-F01-08 según el modelo existente | Pendiente de revisión humana |

Se trasladaron las reglas y criterios y se prepararon plan, tareas y registros pendientes. OpenCode asistió también a la actualización documental del 26/10/2026 con los antecedentes SQL y la decisión de persistencia comunicados por la persona responsable; revisión humana pendiente. Este uso no acredita ejecución de T-01 a T-06.

OpenCode asistió a la actualización del 03/11/2026 con el contrato, las fuentes bilaterales y la solicitud de identificar SKU causantes. Revisión humana pendiente; T-07/T-08 y todos los resultados funcionales permanecen pendientes.

OpenCode asistió a la actualización del 04/11/2026 a partir del cierre publicado por ambos equipos, el merge G6 y el OpenAPI inspeccionado. La evidencia añadida es documental; los resultados de T-07/T-08 requieren ejecución en el consumidor.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| DT-01: zona sin tarifa sin respuesta contractual completa | CA-07 | Bloquea adaptador de ese caso | Valqui con Backend y canales |
| DT-02: redondeo y calendario pendientes; ejemplo suma `0.02126 m³` antes de redondear | CA-01 | Bloquea aceptación del cálculo y fecha | Valqui con Arquitectura y canales |
| DT-03: modelo de cobertura/tarifa por conciliar | CA-01, CA-02, CA-07 | Lectura local sin concretar | Valqui con Arquitectura |
| DT-04: tasa, timeout, caché y medición pendientes | CA-06, CA-09 y rendimiento | Bloquea verificación operativa | Valqui con DevOps y Productos |
| DT-05: tokens y entorno real sin verificar | CA-01 a CA-10 | Integración real pendiente | Valqui con Seguridad, Productos y canales |
| DT-06: H-G2-01/02/03 cerrados y revisión fija enlazada; consumidor sin contrastar | CA-04/05/14/15/16 | Compatibilidad de implementación pendiente, no homologación H | Valqui con Productos y Calidad |
| DT-07: tabla creada comunicada, pero escritor/backend/esquema sin verificar | CA-11 a CA-13 | Persistencia exacta pendiente | Valqui con Backend y Arquitectura |
| DT-08: aceptación semántica resuelta; publicación normativa D y compatibilidad pendientes | CA-15/17/18/19 | Bloquea cierre integral de las regresiones D; dobles del acuerdo cerrado permiten preparación | Valqui con Productos, Calidad y Tarqui |

No hay resultados de implementación ejecutados en esta preparación.

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor, fecha y resultado de revisión: pendientes.
- Estado del alcance: Pendiente.
- Integraciones reales pendientes: Gateway, Seguridad, Productos y canales.

## 7. Referencias

1. [cite: 1] [Especificación](./spec.md), CA-01 a CA-19.
2. [cite: 2] [Plan](./plan.md) y [tareas](./tasks.md).
3. [cite: 3] [Contrato externo](../../integraciones/api-contract.md), [modelo de datos §§1.2 y 3.1](../../arquitectura/modelo-datos.md#12-persistencia-exacta-y-estado-comunicado-del-esquema) y [flujo SDD](../../plantillas/sdd/README.md). Los antecedentes del DDL proceden de la conversación de trabajo del 26/10/2026 y no de una ejecución de base de datos.
