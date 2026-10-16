# Plan de ES-F04-05: Cerrar un despacho como devuelto a origen

**Responsable:** Gerardo.

**Estado:** Preparado documentalmente; implementación y revisión técnica pendientes.

**UI:** Aplica; modal administrativo desde el detalle de incidencia.

## 1. Entradas y revisiones

| Documento o base | Referencia | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-15 | Revisión funcional `c8e6e29`, migrada sin cambiar criterios en esta entrega SDD del 16/10/2026. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-08 | Misma entrega documental; no acredita interfaz implementada. |
| API del proveedor | [Gestión §5.2.3](../../integraciones/api-contract-gestion-despachos.md#523-cerrar-como-devuelto-a-origen--es-f04-05); [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02) | Contratos documentales de la base `c8e6e29`; formatos canónicos, sin copiarlos. |
| Transversales y datos | [Overview](../../overview.md), RT-01/02/03; [modelo](../../arquitectura/modelo-datos.md), §3.4 | Misma base documental; persistencia propuesta pendiente de migrar/implementar. |
| Consumidores/productores | [Detalle ES-F04-02](../ES-F04-02-ConsultarDetalleIncidencia/spec.md), [recepción ES-F04-03](../ES-F04-03-ConfirmarRecepcionPaquete/spec.md) y otras carpetas F-04 | Usar sus tareas dependientes; no duplicar el trabajo común. |
| Código inspeccionado | Frontend `d2bc27d`; backend `1e7834b` | Lectura estática local del 16/10/2026, sin compilación ni pruebas funcionales ejecutadas. |
| Diseño y componentes | [SYSTEM-DESIGN](../../disenio/SYSTEM-DESIGN.md), F-04/P5; [componentes](../../disenio/componentes-react.md), CR-01/02/08/09/15 | Fuentes de UI y límites reutilizables; implementación por comprobar. |

El frontend contiene monorepositorio, tema Mantine y una pantalla F-04 pendiente; el paquete compartido exporta el tema, no los CR completos, y no hay script de interacción. Gestión contiene seguridad y cotización inicial; los comandos y el historial de F-04 siguen pendientes. Los nombres/rutas nuevas de este plan son propuestas, ajustables al iniciar sin cambiar contratos [cite: 1, 2].

## 2. Estrategia y responsabilidades

Gestión confirma un estado final con motivo obligatorio, guarda el resultado original dentro del historial existente y entrega el evento por RT-03. El modal informa el cierre local y recupera el resultado sin repetir la decisión ni atribuirle una entrega a Ventas o una liberación de capacidad.

| Capa | Responsabilidad | Ubicación prevista |
|---|---|---|
| Gestión | Caso de uso, persistencia y captura común conforme al contrato. | Bajo el paquete base existente; áreas propuestas `incidencias/` y `shared/historial/`. |
| Datos | Reutilizar migraciones base y añadir solo cambios de este alcance. | Migraciones Flyway del servicio Gestión; nombres secuenciales a comprobar al implementar. |
| Frontend administrativo | Formulario local, identidad del comando, recuperación y navegación. | `apps/despacho-administrativo/src/features/entregas-fallidas/`, `ModalCierreDespacho.tsx` propuesto. |
| Paquetes frontend | Transporte/tipos, controles y notificaciones existentes. | `packages/cliente-api`, `packages/tipos-compartidos`, `packages/componentes-compartidos`. |
| Gateway | Propagar identidad, correlación y resultado sin cachear o repetir el POST. | Verificar ruta existente `/api/v1/despachos/**`; no crear otro gateway. |
| Operación y Ventas | Mantener contratos de capacidad/eventos que ya poseen. | APIs/procesadores existentes; sin SQL entre servicios ni nuevas reglas comerciales. |

## 3. Frontend y componentes React

Verificar CR-01/02/08/09/15. Componer el modal local con Mantine, advertencia, motivo obligatorio y observación opcional; no es el selector genérico CR-12 ni un catálogo nuevo. Conservar contexto y solicitud original. Después de 200 volver al listado con filtros/página; pérdida de respuesta exige consulta y un refresco fallido no se presenta como rechazo del cierre.

Implementar/verificar los controles necesarios antes del modal. Los CR son configuraciones/contratos compartidos, no envoltorios obligatorios ni componentes automáticamente implementados por estar documentados. Las pruebas con fixtures cubren presentación y se sustituyen por integración real antes del cierre.

## 4. Backend, persistencia e integraciones

- Datos/migración: Reutilizar `historial_estados_despacho`; no añadir tabla de cierres. Incorporar el índice único parcial del cierre y los metadatos `controlCierre` ya definidos en el modelo. La migración se coordina con la base RT-02, verifica datos previos y no fabrica resultados originales ausentes.
- Validar JWT humano/rol antes de existencia/resultados, formato y normalización de motivo/observación. Motivo es texto libre, no enum ni catálogo de fallos; usuario y fecha proceden del contexto/servidor.
- Reconocer primero el resultado aceptado del mismo ejecutor/contenido. Para una decisión nueva validar incidencia/versión, FALLIDO, recepción e integridad local sin exigir máximo agotado, sello intacto, foto, jornada cerrada o liberación confirmada.
- Comparar versión dentro de la escritura; confirmar estado final, versión, historial con resultado original y evento si es real en una transacción local. `motivo_codigo` queda null; motivo de cierre y control interno siguen el modelo.
- Consumir el escritor común de ES-F04-06 T-03 antes del comando, sin esperar la aceptación completa de la sexta. Mantener la relación de la recepción y su solicitud para que el procesador continúe después del cierre.
- El mismo evento acordado comunica cierre logístico, incluido NO_INTENTADO o anulación registrada. No consultar/imponer el estado comercial, generar otra cancelación ni redefinir el contrato de Ventas; entrega y reintentos pertenecen a RT-03.
- Usar una proyección pública del historial: `controlCierre`, huellas y respuesta almacenada no salen en el detalle. Cambios técnicos de comunicación/liberación no editan el registro final.

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
| CA-01 | Cierre local, versión, historial/resultado y evento real atómicos. | T-03/04/06/07; cierre T-08 | EV-01/03/04 |
| CA-02 | Replay exacto después de reinicio o cambios técnicos. | T-03/05/06; cierre T-08 | EV-02/03 |
| CA-03 | Caída de Ventas conserva cierre y agota reintentos RT-03. | T-04/07; cierre T-08 | EV-01/04 |
| CA-04 | Recepción de esta incidencia pendiente, incluso con una histórica recibida. | T-02/04/06; cierre T-08 | EV-01/03 |
| CA-05 | Anulación permite cierre; no genera otra cancelación. | T-02/04/06/07; cierre T-08 | EV-01/03/04 |
| CA-06 | Motivo/formato y normalización Unicode de ambos textos. | T-02/04/06; cierre T-08 | EV-01/03 |
| CA-07 | 401/403/404 y retirada de datos protegidos. | T-04/06; cierre T-08 | EV-01/03 |
| CA-08 | Límite, intentos disponibles y NO_INTENTADO sin cierre automático. | T-02/04/07; cierre T-08 | EV-01/03/04 |
| CA-09 | Estado/versión/incidencia obsoletos sin editar decisiones. | T-05/06; cierre T-08 | EV-02/03 |
| CA-10 | Dos cierres, cierre/reprogramación/anulación y contenido incompatible. | T-03/05/07; cierre T-08 | EV-02/04 |
| CA-11 | Solicitud original continúa al cerrar con liberación pendiente. | T-04/07; cierre T-08 | EV-01/04 |
| CA-12 | Inconsistencia local y rollback de cada escritura. | T-03/04/05; cierre T-08 | EV-01/02 |
| CA-13 | Datos conservados y simulado sin evento externo. | T-03/04/07; cierre T-08 | EV-01/04 |
| CA-14 | Envío, resultado desconocido y recuperación del origen. | T-02/06; cierre T-08 | EV-03 |
| CA-15 | Fuera de fallidos/cola, detalle final autorizado y sin metadatos. | T-04/06/07; cierre T-08 | EV-01/03/04 |
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
- [cite: 2] [Gestión §5.2.3](../../integraciones/api-contract-gestion-despachos.md#523-cerrar-como-devuelto-a-origen--es-f04-05), [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02) y [convenciones/eventos](../../integraciones/api-contract.md), §§3/7.3/9.
- [cite: 3] [Modelo](../../arquitectura/modelo-datos.md), [overview](../../overview.md), [componentes](../../disenio/componentes-react.md) y [evidencia](./evidence.md).
