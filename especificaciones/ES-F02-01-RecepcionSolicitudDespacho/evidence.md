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
| CA-09 | T-05, T-08 | Estado comercial según homologación, sin exigir cotización previa. | EV-02, EV-04 | No ejecutado |
| CA-10 | T-05, T-06, T-08 | Cantidades agrupadas, 100/101 únicos y rechazo previo a G6. | EV-02, EV-03 | No ejecutado |

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

- Tareas asociadas: T-05/T-08; CA-01/05/06/08/09/10 y seguridad.
- Preparación prevista: enlaces bilaterales H-G2-01/02/03, commit fijo del OpenAPI, concesión efectiva G7 y commits backend. Comprobar selección HTTP en perfil normal, token propio, audiencia/scope y estados homologados en F-01/F-02.
- Resultado esperado: recepción con carga íntegra, sin cotización previa, sin escritura en `cotizaciones`, errores diferenciados y ausencia de consultas externas al reconocer una repetición.
- Entorno, comandos, reportes y resultados observados: pendientes.
- Resultado: **No ejecutado**.

## 4. Referencias

- [cite: 1] [Contrato externo §§5.2, 7.1 y 11.1](../../integraciones/api-contract.md#111-respuesta-propuesta-y-plan-de-homologación-física-g2g6) y [evidencia de ES-F01-06](../ES-F01-06-CotizarEnvioConProductos/evidence.md), antecedentes comunicados y límites de esta actualización documental.
