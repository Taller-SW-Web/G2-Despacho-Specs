# Plan de ES-F04-06: Registrar la trazabilidad de las operaciones

**Responsable:** Gerardo.

**Estado:** Preparado documentalmente; implementación y revisión técnica pendientes.

**UI:** No aplica UI nueva ni cambio visual propio; captura interna, consulta ya definida en ES-F04-02. No se crea `ui.md`.

## 1. Entradas y revisiones

| Documento o base | Referencia | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-12 | Revisión funcional `c8e6e29`, migrada sin cambiar criterios en esta entrega SDD del 16/10/2026. |
| UI | No aplica UI propia; consulta/presentación en ES-F04-02. | Misma entrega documental; no acredita interfaz implementada. |
| API del proveedor | [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02); [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02) | Contratos documentales de la base `c8e6e29`; formatos canónicos, sin copiarlos. |
| Transversales y datos | [Overview](../../overview.md), RT-01/02/03; [modelo](../../arquitectura/modelo-datos.md), §3.4 | Misma base documental; persistencia propuesta pendiente de migrar/implementar. |
| Consumidores/productores | [Detalle ES-F04-02](../ES-F04-02-ConsultarDetalleIncidencia/spec.md), [recepción ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/spec.md) y otras carpetas F-04 | Usar sus tareas dependientes; no duplicar el trabajo común. |
| Código inspeccionado | Frontend `d2bc27d`; backend `1e7834b` | Lectura estática local del 16/10/2026, sin compilación ni pruebas funcionales ejecutadas. |

El frontend contiene monorepositorio, tema Mantine y una pantalla F-04 pendiente; el paquete compartido exporta el tema, no los CR completos, y no hay script de interacción. Gestión contiene seguridad y cotización inicial; los comandos y el historial de F-04 siguen pendientes. Los nombres/rutas nuevas de este plan son propuestas, ajustables al iniciar sin cambiar contratos [cite: 1, 2].

## 2. Estrategia y responsabilidades

Reutilizar un escritor de RT-02 dentro de la transacción del comando de origen y una proyección pública del historial. La sexta garantiza los mismos registros de ES-F04-03/04/05; no crea otro endpoint, tabla, procesador o auditoría. La consulta y sus componentes permanecen en ES-F04-02.

| Capa | Responsabilidad | Ubicación prevista |
|---|---|---|
| Gestión | Caso de uso, persistencia y captura común conforme al contrato. | Bajo el paquete base existente; áreas propuestas `incidencias/` y `shared/historial/`. |
| Datos | Reutilizar migraciones base y añadir solo cambios de este alcance. | Migraciones Flyway del servicio Gestión; nombres secuenciales a comprobar al implementar. |
| Frontend/Gateway | Consumir el detalle ya especificado, sin nueva ruta o componente de esta captura. | ES-F04-02 conserva su implementación y controles. |
| Operación y Ventas | Mantener contratos de capacidad/eventos que ya poseen. | APIs/procesadores existentes; sin SQL entre servicios ni nuevas reglas comerciales. |

## 3. Frontend y componentes React

No aplica UI propia ni cambio visual: las entradas cumplen el contrato del detalle existente. No se crea `ui.md`, componente React ni tarea de modal; ES-F04-02 ya define CR-19, autorización, estados y presentación. T-06 verifica ese consumidor sin redefinirlo ni exigir una prueba visual nueva para esta captura interna.

No hay CUI propios. La ausencia de `ui.md` es deliberada: esta captura interna cumple el esquema que ya muestra ES-F04-02, sin añadir campos visibles ni redefinir interacción.

## 4. Backend, persistencia e integraciones

- Datos/migración: Reutilizar o completar la migración base de `historial_estados_despacho` coordinada con F-02/Arquitectura. Conservar incidencia, autoría, estados, datos propios e inmutabilidad. El índice y los metadatos de cierre se integran con ES-F04-05 T-03; el registro durable de reprogramación pertenece a ES-F04-04 T-03. No crear dos migraciones para el mismo cambio.
- Definir una única operación interna de captura con datos del caso de uso; exige una transacción local activa y participa en ella. No usar una transacción independiente que sobreviva al rollback del comando ni registrar después del éxito.
- Obtener usuario/fecha del contexto autenticado y reloj del servidor; la decisión humana conserva origen MANUAL aunque la captura sea automática. Tipos y estados siguen Gestión §5.3 y la tabla funcional.
- Antes de confirmar, los productores guardan historial junto a sus escrituras obligatorias: recepción con solicitud; reprogramación con resultado durable/evento real; cierre con resultado en historial/evento real. El escritor no crea otro evento.
- El incremento común T-03 debe estar disponible antes de ES-F04-04/05 T-04. La integración T-04 de esta carpeta espera esos productores; no exigir la aceptación final de toda la sexta para iniciar cada productor.
- Concurrencia e identidad se resuelven en el comando de origen con versión/unicidad; la captura acepta únicamente la nueva mutación ganadora. Replays y rechazos conservan filas previas sin insertar auditorías aceptadas.
- Proyectar explícitamente campos de presentación y datos propios autorizados; excluir `controlCierre`, huellas y respuestas guardadas. Orden por instante e identificador del contrato, sin reconstruir historia desde la incidencia actual.
- Consultas, reintentos y confirmación técnica de capacidad/envío no invocan otra captura de negocio ni modifican las entradas inmutables. Los procesadores actualizan solo su propia solicitud/evento.

Los contratos son la fuente de encabezados, errores, payload y permisos; no se agregan contratos locales ni scopes inventados [cite: 2, 3].

## 5. Orden de implementación

| Incremento | Resultado verificable | Tareas |
|---|---|---|
| I-01 | Base técnica y controles necesarios comprobados. | T-01 |
| I-02 | Persistencia y escritor común en transacción activa. | T-02/T-03 |
| I-03 | Productores reutilizan el mismo historial. | T-04 |
| I-04 | Repeticiones, concurrencia y rollback comprobados. | T-05 |
| I-05 | Consulta pública autorizada sin metadatos internos. | T-06 |
| I-06 | Recorrido integrado y cobertura revisada. | T-07/T-08 |

Las dependencias concretas y criterios están en [tasks.md](./tasks.md). Las bases de despacho/incidencia/recepción y RT-02 se reutilizan al estar implementadas. La captura común de la sexta habilita los comandos; su integración/aceptación final se comprueba después con los productores. Una dependencia pendiente bloquea solo el incremento real que la necesita.

## 6. Estrategia de verificación

| Criterio | Comprobación concreta | Tareas | Evidencia prevista |
|---|---|---|---|
| CA-01 | Recepción, reserva/sello y transacción conjunta sin evento externo. | T-02/03/04; cierre T-08 | EV-01 |
| CA-02 | Reprogramación con fecha civil y conjunto atómico. | T-02/03/04; cierre T-08 | EV-01 |
| CA-03 | Cierre, motivo separado y resultado durable en historial. | T-02/03/04; cierre T-08 | EV-01 |
| CA-04 | Rechazos conservan historial previo sin auditoría aceptada nueva. | T-03/04/05; cierre T-08 | EV-01/02 |
| CA-05 | Replay tras reinicio/cambio de incidencia conserva la entrada original. | T-02/03/04/05/07; cierre T-08 | EV-01/02/04 |
| CA-06 | Historial completo, varios ciclos y desempate estable en detalle. | T-02/06; cierre T-08 | EV-03 |
| CA-07 | Rollback de historial y cualquier escritura del comando. | T-01/03/05; cierre T-08 | EV-01/02 |
| CA-08 | Concurrencia e identidad incompatible sin doble captura. | T-05; cierre T-08 | EV-02 |
| CA-09 | Inmutabilidad, sub del JWT, hora del servidor y origen MANUAL. | T-01/02/03/04/05/06; cierre T-08 | EV-01/02/03 |
| CA-10 | Reintentos/liberación/envío no modifican historial. | T-07; cierre T-08 | EV-04 |
| CA-11 | Proyección pública sin controlCierre/huellas ni lectura no autorizada. | T-02/06; cierre T-08 | EV-03 |
| CA-12 | Simulado conserva la auditoría aplicable sin evento externo. | T-02/03/04/07; cierre T-08 | EV-01/04 |

Comandos previstos: `./mvnw.cmd test` desde Gestión y, si cambia su código en el recorrido, Operación/Gateway; PostgreSQL/Testcontainers requiere Docker. La comprobación del detalle usa sus pruebas HTTP de contrato/seguridad; no exige crear una pantalla ni otra herramienta frontend. Los pasos de recorrido real y datos antes/después se registrarán en evidencia, sin tokens ni datos personales reales. Estos comandos y recorridos no se ejecutaron al preparar documentos.

## 7. Decisiones y pendientes

| ID | Preparación técnica | Responsable de referencia | Bloquea |
|---|---|---|---|
| DT-01 | Comprobar base PostgreSQL y esquema común RT-02 antes de añadir captura. | Gerardo con Arquitectura y F-02. | I-01/I-02 real. |
| DT-02 | Revisar migraciones base, datos previos y propiedad de cada cambio; regularizar solo desde información verificable. | Gerardo con Arquitectura y productores. | I-03/I-04 real. |
| DT-03 | Disponibilidad de comandos, detalle, procesadores, credenciales y servicios necesarios para el recorrido real. | Gerardo coordina con responsables F-02/F-03/F-06 y DevOps. | I-05/I-06 real. |

Son prerrequisitos de implementación/integración, no preguntas funcionales nuevas. Las revisiones técnicas y visuales se registran al ejecutar; este documento no reasigna trabajo de otros integrantes ni acredita disponibilidad de sus servicios.

## 8. Condiciones para iniciar y cerrar

- [ ] Entradas y bases de código comprobadas en el incremento que se inicia.
- [ ] Tareas y componentes/dependencias necesarios disponibles o simulación explícitamente identificada.
- [ ] No hay bloqueos técnicos para la tarea a ejecutar.
- [ ] Al cerrar, cada criterio tiene evidencia real, revisión y referencias de implementación; los mocks no acreditan integración real.

## 9. Referencias

- [cite: 1] [Especificación](./spec.md), [tareas](./tasks.md) y [guía SDD](../../plantillas/sdd/README.md).
- [cite: 2] [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02), [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02) y [convenciones/eventos](../../integraciones/api-contract.md), §§3/7.3/9.
- [cite: 3] [Modelo](../../arquitectura/modelo-datos.md), [overview](../../overview.md), [componentes](../../disenio/componentes-react.md) y [evidencia](./evidence.md).
