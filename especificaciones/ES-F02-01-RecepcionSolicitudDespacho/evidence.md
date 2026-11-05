# Evidencia de ES-F02-01: Recepción de solicitudes de despacho

**Estado:** Recepción y validación estricta de lote implementadas en `feature/f02-cierre-criterios`; regresión local con PostgreSQL aprobada. Homologación bilateral y aceptación pendientes.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

### Incremento del 30/10/2026

- Verificación posterior con Docker iniciado por el usuario: `./mvnw -q clean verify` con Java 21 terminó correctamente en Gestión (**194 pruebas**), Operación (**124**) y Gateway (**28**), sin fallos, errores ni omitidas. Incluye la migración V8 y pruebas de protección del historial. El bloqueo Docker descrito más abajo corresponde al intento anterior y quedó resuelto; no acredita homologación externa ni medición de rendimiento.

- Backend parte de `develop` `e4f8ee1`; se conserva el trabajo de grafo existente. Cambios sin commit/push atribuidos a esta ejecución.
- `ProductosProgramacionHttp` valida clasificación exhaustiva y única, tipos numéricos positivos, estado y fecha. Un lote malformado responde 502 antes de interpretar inexistentes; error técnico o rechazo de credencial saliente, 503. `INACTIVO` válido se admite para pedidos pagados; `BORRADOR` no se habilita mientras no se homologue.
- Recepción agrupa cantidades y rechaza más de 100 SKU únicos antes de consultar. La traducción de errores incompletos usa la propuesta `details.skusAfectados` y conserva afectados en errores públicos; no se atribuye aceptación de ese formato a G6.
- `./mvnw -q -Dtest=ProductosLoteTests test`: **5 pruebas aprobadas**, con HTTP JDK controlado y caso de uso con dobles. `./mvnw clean verify` intentado con Java 21: bloqueado porque no existe `/var/run/docker.sock`. No se deshabilitaron pruebas de persistencia ni se usaron bases compartidas.
- Rendimiento comprometido, homologación con G6, grants G7 y aceptación humana continúan pendientes. La evidencia histórica «No ejecutado» de las matrices siguientes no se convierte en aprobación integral por estos cambios.

- Documentación preparada: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-01, RF-05).
- Contratos asociados: `integraciones/api-contract.md` (§7.1 y §5.2).
- Commits de implementación y entorno de pruebas: pendientes de ejecución en los repositorios de código.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.
- Actualización del 26/10/2026: referencias corregidas a la ruta física canónica y preparación de CA-08 a CA-10, selección de cliente real, matriz de errores y estados según H-G2-01/02/03. No se inspeccionó código backend, ejecutó PostgreSQL ni acreditó aceptación bilateral o grant G7.
- `cotizaciones` se comunica como tabla creada para F-01, cuyo escritor sigue pendiente; esta recepción no exige cotización previa ni utiliza el histórico como fuente física [cite: 1].

### Actualización documental del 03/11/2026

- Se contrastaron la aceptación H-G2-01/02/03 del 02/11 y la respuesta D-G2-01/02 de G2 del 03/11, enlazadas en contrato §11.1. Los pendientes de homologación del antecedente del 26/10 describen esa sesión histórica; H está cerrado.
- Línea base: OpenAPI G6 `0.6.0-rc.3`, SHA `40b566976fb94d924116dcd01d41b3276c2bc9e3`. D-G2-01 está aceptado por G2; campo obligatorio, orden y precedencia D-G2-02 y su revisión normativa requieren confirmación G6.
- El PR backend G6 #162 reporta avances y pruebas de proveedor, sigue en borrador y no acredita el campo adicional solicitado para `SKU_INVALIDO`. Su emisor local no acredita G7 ni E2E con G2 real.
- Se prepararon CA-11 a CA-13, T-09/T-10 y EV-05. No se inspeccionó ni ejecutó el backend G2; no se atribuye resultado funcional a esta actualización documental [cite: 1].

### Comprobación documental local del 03/11/2026

- `git diff --check` y `python3 /tmp/opencode/validar_documentacion_g2_g6.py`: sin errores. El verificador es temporal y externo al repositorio.
- Se comprobaron 18 Markdown versionados y tres documentos personales excluidos por Git: 408 enlaces locales/anclas, jerarquía y 20 ejemplos JSON. Los 13 criterios de esta carpeta y los 19 de ES-F01-06 conservan los IDs anteriores y tienen cobertura de evidencia y referencias a tareas existentes; las tareas nuevas permanecen pendientes.
- Los documentos padre contienen 27 y 32 criterios, respectivamente. Se comprobó que `modelo-datos.md` coincide con `HEAD` y que se conservan los tres contratos. Estas verificaciones son documentales; las matrices funcionales siguientes siguen sin ejecutar.

### Actualización documental del 04/11/2026

- Se verificó la [confirmación final G2 del 04/11](https://github.com/Taller-SW-Web/G2-Despacho-Specs/issues/15#issuecomment-6632557247), posterior a la [aceptación G6 del 03/11](https://github.com/Taller-SW-Web/G2-Despacho-Specs/issues/15#issuecomment-6616780174). D-G2-01/02 están cerrados semánticamente, incluidos afectados, orden, traducción y precedencia. Los registros anteriores conservan el estado histórico de sus sesiones.
- Se comprobó el merge del PR backend G6 #162 del 03/11, `eeaf39ad666d7bc5a11c0b2a80d9c8c4b0016414`, con detalle y precedencia implementados. Sus pruebas son resultados externos reportados por el proveedor, no ejecución del consumidor G2.
- OpenAPI inspeccionado: `0.6.0-rc.3`, última modificación del archivo en `6fcd81f9151649b94ecd736f8976630b39e97dc2`; aún no incorpora las precisiones D en la operación. Publicación normativa y compatibilidad siguen pendientes según DT-08 de ES-F01-06 y [contrato §11.1](../../integraciones/api-contract.md#111-homologación-física-g2g6-y-precisiones-de-seguimiento), donde están las fuentes fijas.
- Se actualizaron las entradas de CA-09 y CA-11 a CA-13, T-09/T-10 y EV-04/EV-05. La implementación G2, la autorización efectiva G7 y el recorrido real requieren evidencia propia; los resultados funcionales siguientes siguen sin ejecutar.

### Comprobación documental local del 04/11/2026

- Se ejecutaron `git diff --check` y `python3 /tmp/opencode/validar_actualizacion_g2_g6.py`, verificador temporal fuera del repositorio. Resultado correcto en los 18 Markdown versionados: 397 enlaces locales/anclas, encabezados, fuentes de citas y 20 ejemplos JSON.
- Se verificaron 13 criterios de esta carpeta, 19 de ES-F01-06 y 27/32 de las funcionalidades padre, cobertura en matrices y referencias a tareas/registros existentes. T-09/T-10 siguen pendientes y los resultados funcionales conservan `No ejecutado`.
- La primera pasada detectó la cita sin marcador de fuente en `spec.md`; se regularizó y la repetición aprobó. También se comprobaron los tres contratos canónicos y el modelo de datos respecto de `HEAD`. La comprobación es documental y no acredita ejecución de G2/G6/G7.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-06, T-07, T-08 | Recepción exitosa con zona activa, datos físicos de Productos, fecha calculada y estado PENDIENTE_ASIGNACION. | EV-01, EV-03 | No ejecutado |
| CA-02 | T-04, T-08 | Solicitud con destino sin zona de cobertura activa rechazada con 422 DESP_ERROR_SIN_COBERTURA. | EV-01, EV-03 | No ejecutado |
| CA-03 | T-01, T-08 | Solicitud con datos incompletos o inválidos rechazada con 400 Bad Request. | EV-01 | No ejecutado |
| CA-04 | T-03, T-08 | Solicitud repetida para el mismo idPedido responde 200 OK de forma idempotente sin duplicar. | EV-01, EV-03 | No ejecutado |
| CA-05 | T-05, T-08 | Inexistencia correctamente clasificada o error físico de negocio traducidos según contrato. | EV-02, EV-03 | No ejecutado |
| CA-06 | T-05, T-08 | Caída o timeout de Productos y Ofertas rechazada con 503 DESP_ERROR_PRODUCTOS_NO_DISPONIBLE. | EV-02, EV-03 | No ejecutado |
| CA-07 | T-02, T-08 | Petición sin token o sin scope despachos:crear rechazada con 401/403. | EV-01 | No ejecutado |
| CA-08 | T-05, T-08 | Lote malformado/incompleto rechazado sin carga ni despacho parciales. | EV-02, EV-03 | No ejecutado |
| CA-09 | T-05, T-08, T-10 | Estado efectivo interpretado sin rechazo automático por `INACTIVO`/`BORRADOR`. | EV-02, EV-04, EV-05 | No ejecutado |
| CA-10 | T-05, T-06, T-08 | Cantidades agrupadas, 100/101 únicos y rechazo previo a G6. | EV-02, EV-03 | No ejecutado |
| CA-11 | T-09, T-10, T-08 | Padres solos/múltiples/mixtos rechazados con afectados exactos; producto simple válido. | EV-05, EV-04 | No ejecutado |
| CA-12 | T-09, T-10 | Detalle obligatorio no conforme produce error de respuesta inválida. | EV-05 | No ejecutado |
| CA-13 | T-09, T-10, T-08 | Precedencia aceptada, mismo código/conjunto de afectados y lista en orden de cada solicitud. | EV-05, EV-04 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Validación de controlador y seguridad
- Tareas asociadas: T-01, T-02, T-03.
- Comando previsto: `./mvnw test -Dtest=CrearDespachoControllerTest`
- Resultado: **No ejecutado**.

### EV-02. Cliente de Productos y manejo de fallos
- Tareas asociadas: T-05.
- Comando previsto: `./mvnw test -Dtest=ProductosClientWireMockTest`
- Resultado: **No ejecutado**.

### EV-03. Prueba de integración E2E con PostgreSQL
- Tareas asociadas: T-04, T-06, T-07, T-08.
- Comando previsto: `./mvnw test -Dtest=CrearDespachoIntegrationTest`
- Resultado: **No ejecutado**.

El comando previsto de EV-03 con proveedor controlado verifica integración local; por sí solo no acredita el recorrido real siguiente ni se ha confirmado que esos nombres de tests existan en el backend.

### EV-04. Homologación y recorrido real G2 → G6

- Tareas asociadas: T-05/T-08/T-09/T-10; CA-01/05/06/08/09/10/11/12/13 y seguridad.
- Preparación prevista: usar aceptación H, SHA rc.3 y cierre semántico D-G2-01/02 enlazados; agregar publicación normativa D, concesión efectiva G7 y commits del consumidor. Comprobar selección HTTP en perfil normal, token propio, audiencia/scope, estados efectivos y errores identificados de F-01/F-02.
- Resultado esperado: recepción con carga íntegra, sin cotización previa, sin escritura en `cotizaciones`, errores diferenciados y ausencia de consultas externas al reconocer una repetición.
- Entorno, comandos, reportes y resultados observados: pendientes.
- Resultado: **No ejecutado**.

### EV-05. Estado efectivo y error identificado D-G2-01/02

- Tareas y criterios: T-09/T-10 y recorrido T-08; CA-09 y CA-11 a CA-13.
- Preparación prevista: revisión normativa D y proveedor controlado identificados; nueve combinaciones padre/variante, simples, padres no físicos solos/múltiples/mixtos y SKU opacos. Probar ausencia/vacío/tipos inválidos/duplicados/SKU ajenos en el error y permutaciones según contrato §5.2.4: mismo código/conjunto de afectados y lista en orden de cada solicitud. Incluir ausencia de bases con perfiles incompletos, `200` con inexistentes y fallos técnicos.
- Resultado esperado: unidades físicas inactivas/borrador pueden continuar; el rechazo por SKU padre conserva los afectados o produce `502` si el error incumple el detalle exigible. Sin despacho, historial ni cotización parciales; el producto simple válido continúa y el reintento idempotente no consulta nuevamente G6.
- Dependencias: publicación normativa D y compatibilidad del consumidor; campo, orden y precedencia ya aceptados. No exigir el campo nuevo a la línea base rc.3 anterior; un doble del acuerdo cerrado no acredita integración real.
- Commits, revisión, entorno, comandos exactos, reportes y resultado observado: pendientes.
- Resultado: **No ejecutado**. La evidencia de proveedor reportada por G6 no sustituye esta comprobación del consumidor.

## 4. Referencias

- [cite: 1] [Contrato externo §§5.2, 7.1 y 11.1](../../integraciones/api-contract.md#111-homologación-física-g2g6-y-precisiones-de-seguimiento) y [evidencia de ES-F01-06](../ES-F01-06-CotizarEnvioConProductos/evidence.md), fuentes bilaterales y límites de esta actualización documental.
