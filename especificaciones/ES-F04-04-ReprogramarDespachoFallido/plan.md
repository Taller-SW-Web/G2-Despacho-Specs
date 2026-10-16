# Plan de ES-F04-04: Reprogramar un despacho fallido

**Responsable:** Gerardo.

**Estado:** Preparado documentalmente; implementación y revisión técnica pendientes.

**UI:** Aplica; modal administrativo desde el detalle de incidencia.

## 1. Entradas y revisiones

| Documento o base | Referencia | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-18 | Revisión funcional `c8e6e29`, migrada sin cambiar criterios en esta entrega SDD del 16/10/2026. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-08 | Misma entrega documental; no acredita interfaz implementada. |
| API del proveedor | [Gestión §5.2.2](../../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04); [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02) | Contratos documentales de la base `c8e6e29`; formatos canónicos, sin copiarlos. |
| Transversales y datos | [Overview](../../overview.md), RT-01/02/03; [modelo](../../arquitectura/modelo-datos.md), §3.4 | Misma base documental; persistencia propuesta pendiente de migrar/implementar. |
| Consumidores/productores | [Detalle ES-F04-02](../ES-F04-02-ConsultarDetalleIncidencia/spec.md), [recepción ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/spec.md) y otras carpetas F-04 | Usar sus tareas dependientes; no duplicar el trabajo común. |
| Código inspeccionado | Frontend `d2bc27d`; backend `1e7834b` | Lectura estática local del 16/10/2026, sin compilación ni pruebas funcionales ejecutadas. |
| Diseño y componentes | [SYSTEM-DESIGN](../../disenio/SYSTEM-DESIGN.md), F-04/P4; [componentes](../../disenio/componentes-react.md), CR-01/02/08/09/15 | Fuentes de UI y límites reutilizables; implementación por comprobar. |

El frontend contiene monorepositorio, tema Mantine y una pantalla F-04 pendiente; el paquete compartido exporta el tema, no los CR completos, y no hay script de interacción. Gestión contiene seguridad y cotización inicial; los comandos y el historial de F-04 siguen pendientes. Los nombres/rutas nuevas de este plan son propuestas, ajustables al iniciar sin cambiar contratos [cite: 1, 2].

## 2. Estrategia y responsabilidades

Gestión acepta la reprogramación con una transacción local, devuelve el mismo despacho a la cola de F-02 inmediatamente y entrega después el evento mediante RT-03. La UI conserva la identidad del comando para recuperar respuestas perdidas. La liberación iniciada por ES-F04-03 sigue por su reserva original.

| Capa | Responsabilidad | Ubicación prevista |
|---|---|---|
| Gestión | Caso de uso, persistencia y captura común conforme al contrato. | Bajo el paquete base existente; áreas propuestas `incidencias/` y `shared/historial/`. |
| Datos | Reutilizar migraciones base y añadir solo cambios de este alcance. | Migraciones Flyway del servicio Gestión; nombres secuenciales a comprobar al implementar. |
| Frontend administrativo | Formulario local, identidad del comando, recuperación y navegación. | `apps/despacho-administrativo/src/features/entregas-fallidas/`, `ModalReprogramacionDespacho.tsx` propuesto. |
| Paquetes frontend | Transporte/tipos, controles y notificaciones existentes. | `packages/cliente-api`, `packages/tipos-compartidos`, `packages/componentes-compartidos`. |
| Gateway | Propagar identidad, correlación y resultado sin cachear o repetir el POST. | Verificar ruta existente `/api/v1/despachos/**`; no crear otro gateway. |
| Operación y Ventas | Mantener contratos de capacidad/eventos que ya poseen. | APIs/procesadores existentes; sin SQL entre servicios ni nuevas reglas comerciales. |

## 3. Frontend y componentes React

Verificar CR-01/02/08/09/15; componer localmente el modal con Mantine y DatePickerInput, sin crear otro catálogo de formularios. Guardar contexto seleccionado y solicitud original. El día de UI se calcula desde `consultadoEn` en Lima; no convertir el valor civil a UTC. Tras éxito actualizar listado, indicadores y detalle; conflicto exige revisión y un refresco fallido no niega el guardado.

Implementar/verificar los controles necesarios antes del modal. Los CR son configuraciones/contratos compartidos, no envoltorios obligatorios ni componentes automáticamente implementados por estar documentados. Las pruebas con fixtures cubren presentación y se sustituyen por integración real antes del cierre.

## 4. Backend, persistencia e integraciones

- Datos/migración: Reutilizar despacho, incidencia, recepción, política, historial y eventos; incorporar el registro durable `reprogramaciones_despacho` ya propuesto en el modelo. La migración añade su unicidad por despacho/incidencia/versión, referencias y respuesta original; no recrea tablas base. Verificar datos previos antes de exigir restricciones y regularizar solo con información comprobable.
- Validar JWT/rol, formato estricto y normalización. Reconocer el comando aceptado antes de comprobar estado/fecha actuales; identidad por despacho, incidencia, operación y versión presentada, comparando ejecutor y contenido normalizado.
- Inyectar un reloj del servidor y utilizar `America/Lima` para la fecha civil. Contrastar futura con el día al validar la solicitud nueva; leer el máximo vigente y tratar la política inválida como inconsistencia, sin reemplazarla por dos.
- Comparar versión dentro de la escritura; guardar estado, fecha, entrada a cola, nueva versión, historial común, resultado original y evento si es real en una sola transacción. Retirar referencias de asignación vigente; conservar instantáneas de incidencia/recepción/liberación.
- Compartir el escritor de RT-02 definido en ES-F04-06: usar su incremento de captura antes de este comando, sin esperar al cierre de toda la sexta. La sexta verifica después este productor; así se evita una dependencia circular.
- RT-03 envía fuera de la transacción con el evento y payload existentes; no llamar a Ventas, Productos u Operación para autorizar la decisión ni liberar capacidad otra vez. F-02 consulta la cola canónica y aplica fecha/reserva anterior para asignar.
- Un reinicio o una salida posterior no pierde el resultado original. Resolver unicidad/concurrencia con replay exacto o conflicto contractual, sin filtrar excepciones SQL ni trasladar decisiones a otra incidencia.

Los contratos son la fuente de encabezados, errores, payload y permisos; no se agregan contratos locales ni scopes inventados [cite: 2, 3].

## 5. Orden de implementación

| Incremento | Resultado verificable | Tareas |
|---|---|---|
| I-01 | Base técnica y controles necesarios comprobados. | T-01 |
| I-02 | Modal completo con fixtures identificados. | T-02 |
| I-03 | Persistencia y comando local atómico. | T-03/T-04 |
| I-04 | Repeticiones, concurrencia y rollback comprobados. | T-05 |
| I-05 | Modal conectado y recuperación contractual. | T-06 |
| I-06 | Recorrido integrado y cobertura revisada. | T-07/T-08 |

Las dependencias concretas y criterios están en [tasks.md](./tasks.md). Las bases de despacho/incidencia/recepción y RT-02 se reutilizan al estar implementadas. La captura común de la sexta habilita los comandos; su integración/aceptación final se comprueba después con los productores. Una dependencia pendiente bloquea solo el incremento real que la necesita.

## 6. Estrategia de verificación

| Criterio | Comprobación concreta | Tareas | Evidencia prevista |
|---|---|---|---|
| CA-01 | Recepción/versión actuales, nueva fecha, contador y transacción. | T-03/04/06/07; cierre T-08 | EV-01/03/04 |
| CA-02 | Hoy/pasado, fecha inexistente y medianoche en Lima. | T-02/04/06; cierre T-08 | EV-01/03 |
| CA-03 | Máximo vigente igual/superado y cambio de configuración. | T-02/04/06; cierre T-08 | EV-01/03 |
| CA-04 | Otra incidencia/versión o estado distinto, sin nueva decisión. | T-04/05/06; cierre T-08 | EV-01/02/03 |
| CA-05 | Recepción vigente pendiente, aunque exista una histórica. | T-04/06; cierre T-08 | EV-01/03 |
| CA-06 | NO_INTENTADO con cero/uno y sin incremento. | T-04/07; cierre T-08 | EV-01/04 |
| CA-07 | Anulación y límite simultáneos; precedencia y bloqueo. | T-04/05/06; cierre T-08 | EV-01/02/03 |
| CA-08 | Replay exacto después de medianoche/reinicio/otra salida. | T-03/05/06; cierre T-08 | EV-02/03 |
| CA-09 | Formato estricto y observación normalizada con Unicode. | T-02/04/06; cierre T-08 | EV-01/03 |
| CA-10 | Misma identidad con otro contenido/ejecutor. | T-05; cierre T-08 | EV-02 |
| CA-11 | Reprogramación contra cierre/anulación en transacciones reales. | T-05/07; cierre T-08 | EV-02/04 |
| CA-12 | Cola visible inmediatamente y asignación por fecha/reserva. | T-06/07; cierre T-08 | EV-03/04 |
| CA-13 | Liberación pendiente conservada y nueva incidencia sin recepción heredada. | T-03/04/07; cierre T-08 | EV-01/04 |
| CA-14 | Rollback local y evento recuperable ante caída de Ventas. | T-04/05/07; cierre T-08 | EV-01/02/04 |
| CA-15 | Autorización y existencia sin revelar datos. | T-04/06; cierre T-08 | EV-01/03 |
| CA-16 | Identidad/zona/carga conservadas y simulado sin evento. | T-04/07; cierre T-08 | EV-01/04 |
| CA-17 | Modal, resultado desconocido y origen actualizado. | T-02/06; cierre T-08 | EV-03 |
| CA-18 | Máximo ausente/no entero/no positivo sin escrituras. | T-04; cierre T-08 | EV-01 |
| CUI-01 a CUI-08 | Interacción, errores, recuperación, teclado, móvil y autorización. | T-01/T-02/T-06; revisión T-08 | EV-03 |

Comandos previstos: `./mvnw.cmd test` desde Gestión y, si cambia su código en el recorrido, Operación/Gateway; PostgreSQL/Testcontainers requiere Docker. Desde frontend, `npm run typecheck`, `npm run build` y el comando de interacción que se incorpore en T-01 (todavía no existe en la base inspeccionada). Los pasos de recorrido real y datos antes/después se registrarán en evidencia, sin tokens ni datos personales reales. Estos comandos y recorridos no se ejecutaron al preparar documentos.

## 7. Decisiones y pendientes

| ID | Preparación técnica | Responsable de referencia | Bloquea |
|---|---|---|---|
| DT-01 | Comprobar controles compartidos/herramienta de interacción; reutilizar lo preparado en trabajos previos. | Gerardo con Max y responsables CR. | I-01/I-02 real. |
| DT-02 | Revisar migraciones base, datos previos y propiedad de cada cambio; regularizar solo desde información verificable. | Gerardo con Arquitectura y productores. | I-03/I-04 real. |
| DT-03 | Disponibilidad de comandos, detalle, procesadores, credenciales y servicios necesarios para el recorrido real. | Gerardo coordina con responsables F-02/F-03/F-06 y DevOps. | I-05/I-06 real. |

Son prerrequisitos de implementación/integración, no preguntas funcionales nuevas. Las revisiones técnicas y visuales se registran al ejecutar; este documento no reasigna trabajo de otros integrantes ni acredita disponibilidad de sus servicios.

## 8. Condiciones para iniciar y cerrar

- [ ] Entradas y bases de código comprobadas en el incremento que se inicia.
- [ ] Tareas y componentes/dependencias necesarios disponibles o simulación explícitamente identificada.
- [ ] No hay bloqueos técnicos para la tarea a ejecutar.
- [ ] Al cerrar, cada criterio tiene evidencia real, revisión y referencias de implementación; los mocks no acreditan integración real.

## 9. Referencias

- [cite: 1] [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [guía SDD](../../plantillas/sdd/README.md).
- [cite: 2] [Gestión §5.2.2](../../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04), [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02) y [convenciones/eventos](../../integraciones/api-contract.md), §§3/7.3/9.
- [cite: 3] [Modelo](../../arquitectura/modelo-datos.md), [overview](../../overview.md), [componentes](../../disenio/componentes-react.md) y [evidencia](./evidence.md).
