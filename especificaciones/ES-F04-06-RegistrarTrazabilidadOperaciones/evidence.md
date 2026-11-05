# Evidencia de ES-F04-06: Registrar la trazabilidad de las operaciones

**Estado:** Verificación local aprobada en Gestión. Aceptación conjunta y revisión humana pendientes.

**Responsable de verificación:** Gerardo. Ejecución y registro asistidos por Codex.

**Última ejecución:** 04/11/2026, America/Lima.

## 1. Versión y entorno verificados

- Backend: rama `feature/f04-es06-trazabilidad-operaciones`, base `6af187c`, commit de pruebas `cb2872b`. Los tres productores ya comparten `HistorialIncidenciasJdbc` en la base revisada.
- Specs: rama `docs/f04-es06-trazabilidad-operaciones`, base `1356151`. Se conservan CA-01 a CA-12 de [spec.md](./spec.md).
- Windows, Java 21, Docker 29.4.0 y PostgreSQL 17.11/PostGIS desechable de Testcontainers. Flyway aplica V1 a V7 en las bases de prueba. Fixtures y credenciales sintéticos.
- Comando desde `servicio-gestion-despachos`: `./mvnw.cmd -B -ntp -Dpruebas.postgres.externo=false clean verify`. Resultado `BUILD SUCCESS`, 189 pruebas, cero fallos, errores u omitidas.
- Informes locales de la ejecución en `servicio-gestion-despachos/target/surefire-reports/TEST-*.xml`. Las suites HTTP de recepción, reprogramación y cierre ejecutaron 14, 21 y 18 pruebas respectivamente, todas aprobadas.

## 2. Cobertura de criterios

| Criterio | Qué quedó comprobado | Registro | Resultado |
|---|---|---|---|
| CA-01 | Recepción con sello y reserva original, un historial y solicitud de liberación sin evento a Ventas. | EV-01 | Aprobado local |
| CA-02 | Reprogramación con fecha civil y conjunto transaccional de historial, resultado y evento. | EV-01 | Aprobado local |
| CA-03 | Cierre con motivo propio y resultado durable, separado del catálogo de fallos. | EV-01 | Aprobado local |
| CA-04 | Solicitudes inválidas, no autorizadas o incompatibles sin otra decisión aceptada. | EV-02 | Aprobado local |
| CA-05 | Recuperación del resultado original tras repetir y recrear el servicio o cambiar la incidencia. | EV-02, EV-04 | Aprobado local |
| CA-06 | Consulta después del cierre con entradas de F-02, F-03 y F-04 de dos ciclos, con desempate por ID y sin escrituras. | EV-03 | Aprobado local |
| CA-07 | Fallo inyectado en las escrituras requeridas y reversión de la operación completa. | EV-02 | Aprobado local |
| CA-08 | Duplicados concurrentes, contenido o actor incompatible y competencia sobre la versión vigente. | EV-02 | Aprobado local |
| CA-09 | Autoría del JWT de prueba y fecha del servidor, origen MANUAL e historial anterior preservado. | EV-01, EV-02, EV-03 | Aprobado local |
| CA-10 | Liberación y envío con contrapartes controladas, comparando todas las filas antes y después. | EV-04 | Aprobado local; integración real pendiente |
| CA-11 | Lectura con autorización, rechazo 401/403 y proyección sin metadatos internos. | EV-03 | Aprobado local |
| CA-12 | Los casos simulados conservan su historial aplicable y omiten eventos externos. | EV-01, EV-04 | Aprobado local |

## 3. Registros de verificación

### EV-01. Captura y transacciones de los productores

- **Resultado observado:** `RecepcionCentroHttpTests`, `ReprogramacionDespachoHttpTests` y `CierreDespachoHttpTests` ejecutaron los comandos de Gestión con Flyway y PostgreSQL real. Verificaron las filas de historial, estado, versión y escrituras relacionadas. Las suites de reprogramación y cierre también verificaron migraciones con datos históricos sintéticos.
- **Alcance:** T-01 a T-04. La infraestructura y el escritor existentes cubren la captura común. La prueba HTTP usa identidades de prueba.
- **Resultado:** Aprobado local.

### EV-02. Rechazos, rollback y concurrencia

- **Resultado observado:** Las suites HTTP de los tres comandos inyectaron fallos en escrituras de PostgreSQL, probaron repeticiones exactas y confrontaron decisiones con otro actor, contenido o versión. En reprogramación, `historialComunExigeTransaccionYParticipaEnSuRollback` comprueba el rechazo fuera de una transacción y la reversión dentro de ella.
- **Alcance:** T-05. Transacciones reales de Gestión sobre datos desechables.
- **Resultado:** Aprobado local.

### EV-03. Historial público y autorización

- **Resultado observado:** La prueba `consultaCiclosAnterioresConDesempateEstableSinAlterarElHistorial` de `CierreDespachoHttpTests` consultó el detalle tras cerrar el segundo ciclo. El GET devolvió las seis entradas, aplicó el desempate por identificador en dos marcas iguales y conservó los datos de cada incidencia. Las llamadas sin sesión o sin rol recibieron 401 y 403 sin historial. Dos lecturas autorizadas dejaron intactos el historial, la versión y los conteos de escrituras relacionadas. La proyección excluyó `controlCierre`; la prueba de cierre existente también comprueba que se excluyen huellas y respuestas internas.
- **Alcance:** T-06. Endpoint HTTP existente de ES-F04-02, JWT controlados y PostgreSQL real de Gestión.
- **Resultado:** Aprobado local.

### EV-04. Reintentos técnicos y simulados

- **Resultado observado:** `liberacionPendienteContinuaDespuesDelCierreSinCambiarSuVersion` confirmó la liberación mediante el procesador real de Gestión y un puerto controlado. `eventoReintentaPorHttpConElMismoPayloadSinRevertirLaDecision` usó el emisor real de Gestión contra un receptor HTTP local controlado. Tras seis respuestas 503 y un reenvío controlado con 204, el payload y el historial persistido completo se conservaron. Las pruebas existentes cubren también recuperación de una respuesta de liberación perdida y simulados sin envío externo.
- **Alcance:** T-07 local. El puerto de liberación es un doble y el receptor de Ventas es un servidor local de prueba. El reenvío se provoca en la prueba sobre el mismo evento.
- **Resultado:** Aprobado local. Falta comprobar la liberación contra Operación y el envío y reenvío contra Ventas con credenciales y servicios autorizados, comparando las mismas filas antes y después.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción conservada | Revisión humana |
|---|---|---|---|---|
| Preparación documental SDD | Codex, 16/10/2026 | Revisión funcional `c8e6e29`, plantillas SDD, contratos y modelo | Completar carpetas SDD y conservar criterios. | Pendiente |
| Verificación y cobertura de ES-F04-06 | Codex, 04/11/2026 | Carpeta SDD, Gestión §5.2/§5.3 y repositorios actualizados | Completar la especificación conforme al contrato en ramas descriptivas. Reutilizar el historial existente y registrar resultados reales. | Pendiente |

## 5. Diferencias y pendientes

| Pendiente | Criterios afectados | Acción |
|---|---|---|
| Aceptación conjunta de la liberación y la comunicación con Ventas. | CA-10; T-07. | Gerardo coordina con Operación, Ventas y DevOps la prueba autorizada con un despacho sintético y guarda el historial antes y después. |
| Revisión humana y cierre de cobertura. | T-08. | Revisar los commits y actualizar la evidencia al completar EV-04 en el entorno integrado. |

## 6. Entrega y revisión

- Commit de backend `cb2872b`. Suites y entorno identificados en EV-01 a EV-04.
- T-01 a T-06 verificadas en Gestión. T-07 y T-08 en curso.
- El alcance conserva el contrato, las migraciones y el consumidor frontend existentes.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md), [plan](./plan.md) y [tareas](./tasks.md).
- [cite: 2] [Gestión §5.2 y §5.3](../../integraciones/api-contract-gestion-despachos.md#52-comandos-de-recepción-reprogramación-y-cierre), [modelo](../../arquitectura/modelo-datos.md) y [guía SDD](../../plantillas/sdd/README.md).
