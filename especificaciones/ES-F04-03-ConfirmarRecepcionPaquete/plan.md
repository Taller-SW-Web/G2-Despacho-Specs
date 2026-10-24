# Plan de ES-F04-03: Confirmar la recepción del paquete

**Responsable:** Gerardo.

**Estado:** Recepción en Gestión y frontend implementados y verificados localmente; integración real y revisión humana pendientes. Avance del 24/10/2026 en [evidence.md](./evidence.md).

**UI:** Aplica; modal administrativo desde listado o detalle.

## 1. Entradas y revisiones

| Documento o base | Referencia | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-12 | Revisión funcional de esta conversación sobre la base documental `0734268`; migración SDD del 15/10/2026 incluida en el commit que introduce esta carpeta. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-08 | Misma revisión documental que este plan. |
| Gestión | [§5.2.1](../../integraciones/api-contract-gestion-despachos.md#521-confirmar-recepción-en-centro--es-f04-03) y §5.3 | Transacción, repetición, procesador y consulta de sincronización de esta revisión. |
| Operación | [§5.2](../../integraciones/api-contract-operacion-reparto.md#52-gestión-libera-una-reserva-en-operación); §5.1 para nuevas asignaciones | Consumidor HTTP de Gestión probado con dobles; proveedor y ocupación reales no verificados en este incremento. |
| Diseño y componentes | [Diseño F-04](../../disenio/funcionalidades/f-04.md), Pantalla 3; [componentes](../../disenio/componentes-react.md), CR-01/02/08/09/15 | Tema, controles Mantine y cliente existentes reutilizados; revisión con Max y ampliación al 200 % pendientes. |
| Arquitectura y datos | [Contenedores](../../arquitectura/c4-contenedores.md); [modelo](../../arquitectura/modelo-datos.md), §3.4 | Esquema V1/V2 de Gestión verificado con Flyway en PostgreSQL vacío; no requiere V3. Reconciliación histórica real pendiente. |
| Código implementado | Backend `31e1f6e`; frontend `779f6c4`, documentación `9108caf` | Verificación local del 24/10/2026: 109 pruebas de Gestión y 32 de frontend aprobadas; ver EV-01/03/04. |

La preparación SDD del 15/10/2026 consultó frontend `d2bc27d` y backend `1e7834b`. La implementación posterior parte de `develop`: backend `a9a8f73` y frontend `8a37d13`. Ya existen listado/detalle, pruebas Vitest y el modal conectado al cliente API; Gestión incorpora recepción y procesador durable. La verificación usó PostgreSQL aislado y dobles de proveedores. Por autorización del usuario no se modificó Operación ni su base, Gateway o Seguridad; la integración conjunta sigue pendiente [cite: 1, 2].

## 2. Estrategia y responsabilidades

Gestión confirma el retorno con una transacción local que incluye una solicitud durable; responde sin esperar a Operación. Un procesador independiente libera la reserva original y guarda el resultado. El frontend consulta el estado actual y conserva el éxito de recepción aunque falle la sincronización.

| Capa | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Modal, validación, identidad original, recuperación y actualización de origen. | `apps/despacho-administrativo/src/features/entregas-fallidas/ModalRecepcionPaquete.tsx` y `apiRecepcion.ts`, integrados en listado y detalle. |
| Paquetes frontend | Transporte/tipos y controles visuales sin reglas de negocio propias. | Se reutilizan `packages/cliente-api`, `packages/tipos-compartidos` y `packages/componentes-compartidos`, sin modificarlos en este incremento. |
| Gateway | Propagar identidad/correlación y respuesta `202` sin cachear ni reintentar el POST automáticamente. | Ruta existente `/api/v1/despachos/**`; verificar su seguridad y manejo de errores. |
| Gestión | Recepción, historial, versión, solicitud y procesador de liberaciones. | `incidencias/api`, `incidencias/application` e `incidencias/infrastructure` bajo el paquete base existente. |
| Operación | Liberación idempotente, verificación de pertenencia y ocupación local. | Dependencia de reservas/jornadas y F-02/F-06; sin cambios ni pruebas del proveedor real en esta entrega. |

## 3. Frontend y componentes React

- Reutilizar/verificar CR-01/02/08/09/15 antes del modal; compartir las configuraciones Mantine y el proveedor existente. La tarea de CR de otro integrante conserva su responsable y evidencia.
- Formulario local con sello sin selección inicial y observación opcional; contar puntos de código Unicode tras recortar extremos. UI-01 define interacción y mensajes, sin duplicar el contrato.
- El contenedor conserva despacho, incidencia, versión, actor y cuerpo normalizado de la solicitud enviada mientras recupera su resultado; no sustituye esa identidad con datos de un refresco.
- Obtener contexto actual antes de habilitar envío; cancelar/descartar respuestas antiguas por recurso y generación. El backend sigue siendo autoridad ante cambios posteriores.
- Adaptar respuesta/errores en el cliente; mapear al booleano sin confundir No con ausencia. No configurar reintentos automáticos generales para este POST.
- Ante timeout/`503`, consultar detalle antes de repetir exactamente. Si cambió la incidencia, no usar su recepción para inferir el resultado anterior; recuperar solo la operación original o pedir revisión.
- Tras `202`, invalidar/recargar listado, indicadores y detalle; mantener filtros y foco de origen. Una lectura fallida no borra la confirmación. Leer sincronización con el mecanismo de actualización de ES-F04-02, sin otro temporizador paralelo.
- Fixtures cubren éxito, No sin texto, errores, conflicto, cambio de incidencia y respuesta perdida. Acreditan solo presentación/interacción; se sustituyen por el Gateway real antes del cierre.

## 4. Backend, persistencia e integraciones

- Entrada: validar JWT/rol, formato estricto y normalización según Gestión §5.2.1; autenticar antes de recuperar resultados. Actor y fecha proceden del servidor.
- Identidad: operación + despacho + incidencia + versión presentada según §5.2; comparar contenido normalizado y actor con la operación aceptada antes de comprobar estado/versión actuales.
- Transacción: bloquear/controlar la versión del despacho y revalidar incidencia, estado, recepción e integridad dentro de la misma escritura. Guardar recepción, historial, nueva versión, solicitud y respuesta original juntos.
- Restricciones: una recepción y solicitud por incidencia; reserva original única en la solicitud. Resolver carreras de escritura/unicidad como `409` o repetición exacta, sin exponer excepciones SQL ni producir duplicados.
- Historial: un único `RECEPCION_EN_CENTRO`, `FALLIDO` → `FALLIDO`; no aumentar intentos ni emitir evento a Ventas. Reintentos técnicos actualizan su solicitud, no el historial/versión del despacho.
- Decisión comprobada: V1/V2 de Gestión ya incluyen referencias por salida, `liberaciones_capacidad` e índices/restricciones necesarios; Flyway los crea en PostgreSQL vacío. Se reutilizan sin V3 ni reescritura de migraciones. La clave de asignación de Operación se mantiene como dependencia de T-06; no se modifica su esquema.
- Compatibilidad: revisar datos antes de exigir referencias nuevas. Regularizar reservas/jornadas históricas con información verificable; recepciones ya registradas necesitan reconciliación comprobada para crear su solicitud/estado, sin fabricar una respuesta original ni reenviar a ciegas.
- Si los históricos no permiten reconstrucción segura, registrar y resolver los casos antes de habilitar la lectura/recepción afectada. Una ausencia inconsistente se informa según contrato; no elegir la reserva actual por conjetura.
- Operación §5.2 valida credencial técnica y pertenencia; libera una sola reserva y devuelve la liberación original si ya ocurrió. Su actualización local es atómica y no reabre jornadas cerradas.
- El procesador reclama pendientes con exclusión de 60 s y token, confirma la reclamación y llama fuera de la transacción con límite total de 5 s. Solo el token vigente puede finalizar/reprogramar ese intento.
- Aplicar el calendario configurado y clasificación de errores de Gestión §5.2.1. Persistir siguiente intento y diagnóstico sin secretos; reinicio o pérdida de respuesta conserva la misma reserva. Una respuesta incoherente no confirma liberación.
- Confirmar solo al recibir los IDs esperados y `LIBERADA`; limpiar el aviso de revisión. Con respuesta perdida o fallo al guardar, repetir obtiene la misma liberación sin doble descuento.
- Autorización técnica/secretos y despliegue del procesador son dependencias reales; no inventar scopes ni compartir tablas. GET consulta la solicitud y no ejecuta/reencola envíos.
- Integración: reprogramar/cerrar puede continuar con retorno confirmado; F-02 espera si existe reserva anterior activa. Verificar clave estable por operación, otra clave para otra salida y F-06 sumando reservas activas [cite: 2, 3].

## 5. Orden de implementación

| Incremento | Resultado verificable | Tareas y dependencias | Criterios |
|---|---|---|---|
| I-01 | Base de pruebas y controles necesarios disponibles. | T-01; componentes compartidos coordinados. | CCR aplicables; soporte de CUI. |
| I-02 | Modal aislado con todos sus estados. | T-02, después de I-01. | CUI-01 a CUI-08 con fixtures. |
| I-03 | Recepción atómica y repetible en Gestión. | T-03/04/05; base de datos y productores por salida. | CA-01 a CA-08, CA-10/11; sin acreditar liberación real. |
| I-04 | Liberación correcta y repetible en Operación. | T-06; reservas y credenciales. | CA-01/03/06/07/09. |
| I-05 | Solicitud entregada y recuperada tras fallos. | T-07; I-03/04; dobles controlados durante desarrollo. | CA-01/03/07/08/09. |
| I-06 | Modal conectado y origen actualizado. | T-08; I-02/03 y lecturas de ES-F04-01/02 disponibles. | CA-01 a CA-12 en su alcance de UI. |
| I-07 | Recorrido real y cobertura revisados. | T-09/10; I-04/05/06 y F-02/F-06 disponibles. | Todos los CA/CUI y controles de integración. |

El backend y la UI aislada pueden prepararse por separado; mocks y dobles se identifican. El cierre requiere comprobar la integración real, no solo respuestas simuladas.

## 6. Estrategia de verificación

| Criterio | Comprobación concreta | Nivel y dependencia |
|---|---|---|
| CA-01 | `202`, recepción/historial/versión/solicitud y liberación posterior. | PostgreSQL y después ambos servicios reales. |
| CA-02 | No con observación ausente, vacía y escrita. | Endpoint y UI; booleano `false` persistido. |
| CA-03 | Repetición original antes/después de liberar y resolver. | Persistencia real, mismo actor/cuerpo y respuesta original idéntica. |
| CA-04 | Incidencia/versión obsoletas y estado incompatible. | Endpoint con recursos y versiones controlados. |
| CA-05 | Campos extra, tipos, 500/501 caracteres, espacios y emojis. | Validación contractual y formulario. |
| CA-06 | Sin token, token inválido, otro rol y pérdida de acceso. | Seguridad de Gestión/Operación y retirada de datos en UI. |
| CA-07 | Dos salidas; ejecutar un envío antiguo tras nueva asignación. | Reservas reales; solo la original cambia. |
| CA-08 | Fallo en cada escritura y referencias incompletas. | Transacción PostgreSQL; rollback sin envío huérfano. |
| CA-09 | Caída, `429/5xx/4xx`, respuesta incoherente y reinicio en cada frontera. | Procesador con reloj controlado y después servicios reales. |
| CA-10 | Dos usuarios/contenidos concurrentes sobre la misma versión. | Dos transacciones reales; una recepción y un historial. |
| CA-11 | `NO_INTENTADO`, anulado, máximo, sin foto y jornada activa/cerrada. | Datos combinados sin alterar intentos ni jornada. |
| CA-12; CUI-01 a CUI-08 | Apertura en ambos orígenes, errores, consulta previa a repetición, foco y refresco. | Fixtures identificados y recorrido real con teclado/móvil. |

Comandos ejecutados el 24/10/2026: `./mvnw.cmd clean verify` desde Gestión (109 pruebas, sin fallos, errores ni omisiones, y JAR construido); `npm run test:f04` desde frontend (32 pruebas), `npm run typecheck` (los tres espacios de trabajo) y `npm run build -w @despacho/administrativo` (compilación administrativa aprobada, advertencia de tamaño del bundle). No se ejecutó la construcción de ambas apps en este incremento ni pruebas de Operación/Gateway. Testcontainers utilizó Docker y PostgreSQL/PostGIS desechable; frontend y proveedores remotos usaron dobles. T-09 conserva pendientes las consultas antes/después y reinicios de servicios reales.

## 7. Decisiones y pendientes

| ID | Decisión o pendiente | Responsable y fuente | Bloquea |
|---|---|---|---|
| DT-01 | Herramientas y reutilización necesarias comprobadas localmente; pendientes revisión con Max y ampliación al 200 %. | Gerardo con Max y responsables del catálogo compartido; EV-04. | Cierre visual de I-02/06/07. |
| DT-02 | V1/V2 y reserva original verificados en base nueva y fixtures; faltan inspección/reconciliación de datos históricos reales y productores entre servicios. | Gerardo con Arquitectura y F-02/F-03; EV-01. | Habilitación de históricos afectados e I-07 real. |
| DT-03 | Procesador y consumidor técnico implementados con dobles; falta validar credencial, proveedor y reinicios desplegados. | Gerardo con Operación y DevOps; EV-02/03/05. | I-04/05/07 con servicios reales. |
| DT-04 | Listado/detalle conectados y probados con APIs simuladas; faltan reglas reales de nueva asignación y ocupación. | Gerardo con F-02/F-06; EV-04/05. | Aceptación integrada de I-06/07. |

La tabla durable existente y la ejecución asíncrona están consumidas por Gestión en `31e1f6e`. Esta actualización registra decisiones verificadas y pendientes de integración; no cambia los requisitos ni el contrato y no atribuye cierre a trabajos de otros responsables.

## 8. Condiciones para iniciar y cerrar

- [x] Las entradas, contratos y migraciones del incremento local fueron revisados; históricos reales pendientes según DT-02.
- [x] Componentes y dependencias del incremento local disponibles; los dobles y sus límites están declarados en la evidencia.
- [x] No hay pendientes que impidan el incremento local de Gestión/frontend; DT-01 a DT-04 conservan el trabajo requerido para aceptación integrada.
- [ ] Todas las tareas y criterios cuentan con evidencia real, revisión y commits de implementación al cerrar.

## 9. Referencias

- [cite: 1] [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [flujo SDD](../../plantillas/sdd/README.md).
- [cite: 2] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §§5.2/5.2.1/5.3; [Operación](../../integraciones/api-contract-operacion-reparto.md), §§5.1/5.2; [convenciones](../../integraciones/api-contract.md), §§3/9.
- [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), §3.4; [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), §4.5; [componentes React](../../disenio/componentes-react.md).
- Resultados y límites de la verificación: [evidence.md](./evidence.md).
