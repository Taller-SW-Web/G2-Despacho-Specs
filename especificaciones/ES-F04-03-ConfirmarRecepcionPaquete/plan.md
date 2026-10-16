# Plan de ES-F04-03: Confirmar la recepción del paquete

**Responsable:** Gerardo.

**Estado:** Borrador documental; implementación y revisión técnica pendientes.

**UI:** Aplica; modal administrativo desde listado o detalle.

## 1. Entradas y revisiones

| Documento o base | Referencia | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-12 | Revisión funcional de esta conversación sobre la base documental `0734268`; migración SDD del 15/10/2026 incluida en el commit que introduce esta carpeta. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-08 | Misma revisión documental que este plan. |
| Gestión | [§5.2.1](../../integraciones/api-contract-gestion-despachos.md#521-confirmar-recepción-en-centro--es-f04-03) y §5.3 | Transacción, repetición, procesador y consulta de sincronización de esta revisión. |
| Operación | [§5.2](../../integraciones/api-contract-operacion-reparto.md#52-gestión-libera-una-reserva-en-operación); §5.1 para nuevas asignaciones | Liberación por reserva e identidad por operación; implementación pendiente. |
| Diseño y componentes | [Diseño F-04](../../disenio/funcionalidades/f-04.md), Pantalla 3; [componentes](../../disenio/componentes-react.md), CR-01/02/08/09/15 | Reutilización documentada; no acredita código implementado. |
| Arquitectura y datos | [Contenedores](../../arquitectura/c4-contenedores.md); [modelo](../../arquitectura/modelo-datos.md), §3.4 | Dos servicios, referencias por salida y tabla propuesta `liberaciones_capacidad`. |
| Código consultado | Frontend `d2bc27d`; backend `1e7834b` | Lectura estática local; sin compilaciones ni pruebas funcionales ejecutadas. |

La base frontend tiene aplicaciones Vite, Mantine, Axios y tema compartido; F-04 sigue como pantalla pendiente y no hay script de pruebas. Backend tiene Gateway/seguridad y cotización inicial, pero no recepción, reservas ni procesador implementados. Las ubicaciones nuevas siguientes son propuestas, ajustables al iniciar sin cambiar contratos [cite: 1, 2].

## 2. Estrategia y responsabilidades

Gestión confirma el retorno con una transacción local que incluye una solicitud durable; responde sin esperar a Operación. Un procesador independiente libera la reserva original y guarda el resultado. El frontend consulta el estado actual y conserva el éxito de recepción aunque falle la sincronización.

| Capa | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Modal, validación, identidad original, recuperación y actualización de origen. | `apps/despacho-administrativo/src/features/entregas-fallidas/`; `ModalRecepcionPaquete.tsx` propuesto. |
| Paquetes frontend | Transporte/tipos y controles visuales sin reglas de negocio propias. | `packages/cliente-api`, `packages/tipos-compartidos`, `packages/componentes-compartidos`. |
| Gateway | Propagar identidad/correlación y respuesta `202` sin cachear ni reintentar el POST automáticamente. | Ruta existente `/api/v1/despachos/**`; verificar su seguridad y manejo de errores. |
| Gestión | Recepción, historial, versión, solicitud y procesador de liberaciones. | Funcionalidad propuesta `incidencias/` y adaptador HTTP bajo el paquete base existente. |
| Operación | Liberación idempotente, verificación de pertenencia y ocupación local. | Funcionalidad de reservas/jornadas; contrato interno y coordinación con F-02/F-06. |

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
- Migración propuesta: referencia de reserva en incidencia, tabla `liberaciones_capacidad`, índices/restricciones y clave de asignación en la reserva de Operación. Reutilizar migraciones de despacho/historial de trabajos previos; no crear otro esquema completo.
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

Comandos previstos: `npm run typecheck` y `npm run build` desde frontend; `./mvnw.cmd test` desde Gestión, Operación y Gateway según el cambio. T-01 concreta el comando de interacción aún inexistente; Testcontainers requiere Docker. T-09 registra además consultas antes/después y reinicios reales. No se han ejecutado estas comprobaciones.

## 7. Decisiones y pendientes

| ID | Decisión o pendiente | Responsable y fuente | Bloquea |
|---|---|---|---|
| DT-01 | Verificar herramientas y CR necesarios; completar lo faltante con sus responsables. | Gerardo con Max y responsables del catálogo compartido. | I-01/02/06 real. |
| DT-02 | Migraciones/productores conservan reserva original; reconciliación histórica si hay datos existentes. | Gerardo con Arquitectura y responsables F-02/F-03; modelo §3.4. | I-03/07 real. |
| DT-03 | Credencial técnica y ejecución del procesador con reclamación recuperable y aviso operativo. | Gerardo con responsables de Operación y DevOps; contratos §§5.2/5.2.1. | I-04/05/07 real. |
| DT-04 | Listado/detalle y reglas de nueva asignación/ocupación integrados. | Gerardo con F-02/F-06; especificaciones relacionadas. | I-06/07 real, no fixtures. |

La tabla durable y la ejecución asíncrona son decisiones de esta revisión, con trabajo de backend explícito. No se implementaron al redactar el modelo. Los pendientes anteriores son de preparación técnica e integración, no reglas funcionales sin definir.

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas, contratos y migraciones del incremento están revisados; las bases de código se vuelven a comprobar al iniciar.
- [ ] Componentes y dependencias necesarios para la tarea están disponibles o su simulación está declarada.
- [ ] No hay pendientes técnicos que bloqueen el incremento a implementar.
- [ ] Todas las tareas y criterios cuentan con evidencia real, revisión y commits de implementación al cerrar.

## 9. Referencias

- [cite: 1] [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [flujo SDD](../../plantillas/sdd/README.md).
- [cite: 2] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §§5.2/5.2.1/5.3; [Operación](../../integraciones/api-contract-operacion-reparto.md), §§5.1/5.2; [convenciones](../../integraciones/api-contract.md), §§3/9.
- [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), §3.4; [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), §4.5; [componentes React](../../disenio/componentes-react.md).
- Resultados y límites de la verificación: [evidence.md](./evidence.md).
