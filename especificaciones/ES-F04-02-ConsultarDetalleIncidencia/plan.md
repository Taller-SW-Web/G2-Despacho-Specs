# Plan de ES-F04-02: Consultar el detalle de una incidencia

**Responsable:** Gerardo.

**Estado:** Consulta implementada en código con verificación local; integración real, revisión humana y comandos propietarios pendientes.

**UI:** Aplica; página administrativa de detalle.

## 1. Entradas y revisiones

| Documento o base | Referencia | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-11 | Archivo existente en `0b32afc`, revisión funcional de esta conversación y migración incluida en este commit. Se conservan los IDs. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-08 | Misma revisión documental que este plan. |
| Contrato de Gestión | [§5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02); §5.2 para destinos | Detalle, acciones, errores y concurrencia definidos en esta revisión. |
| Contrato de Operación | [§3.5](../../integraciones/api-contract-operacion-reparto.md#35-autorizar-la-lectura-de-evidencia) y [§5.4](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias) | Lectura de evidencia y datos operativos; implementación pendiente. |
| Diseño y componentes | [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md), §23; [componentes React](../../disenio/componentes-react.md), CR-01/03/05/08/09/15/18/19 | Contratos compartidos; no equivalen a componentes implementados. |
| Arquitectura y datos | [Contenedores](../../arquitectura/c4-contenedores.md); [modelo](../../arquitectura/modelo-datos.md), §§3.3–3.5 | Última incidencia, historial, outbox y parámetros según esta revisión. |
| Base de código de implementación | Frontend `314537b`; backend `5a5c57b`; specs `0f8f1f1` | Ramas `feature/f04-detalle-incidencia` desde `develop` en código y desde `main` en specs, conforme a la indicación de Gerardo del 16/10/2026. |

La base actual contiene el listado ES-F04-01, los componentes CR-08/18/19 y el lote operativo. Se reutilizan para el detalle y la lectura temporal de evidencia; los resultados reales de las pruebas locales se registran en `evidence.md`. Gerardo solicitó pruebas esenciales (nueve nuevas por frontend y backend), commits incrementales y ninguna ejecución de Docker ni despliegue. Esta indicación acota la verificación de esta entrega; no acredita las integraciones pendientes [cite: 1, 2].

## 2. Estrategia y responsabilidades

Gestión obtiene una lectura local consistente del despacho y su última incidencia, recepción, contador, política, historial y comunicaciones. Enriquece solo nombre y jornada mediante Operación, calcula acciones con datos locales y devuelve el contrato. El contenedor frontend consume ese resultado y obtiene por separado la URL de la fotografía en Operación.

| Área | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Ruta, consulta, adaptación, actualización y navegación. | `apps/despacho-administrativo/src/features/entregas-fallidas/`; página propuesta `PaginaDetalleIncidencia.tsx`. |
| Paquetes frontend existentes | Tipos de transporte, HTTP y componentes visuales sin llamadas de negocio propias. | `packages/cliente-api`, `packages/tipos-compartidos`, `packages/componentes-compartidos`. |
| Gateway | Mantener rutas públicas y propagación de identidad/correlación. | Ya enruta `/api/v1/despachos/**` a Gestión y `/api/v1/evidencias/**` a Operación; verificar transporte, sin crear prefijos nuevos. |
| Gestión | Consulta, autorización, reglas y persistencia local. | Funcionalidad propuesta `incidencias/` bajo el paquete base existente, con capas según los patrones del repositorio. |
| Operación | Proveer nombres/jornadas y autorizar evidencia asociada. | Reutilizar el proveedor de §5.4 y coordinar §3.4 con F-03, sin compartir entidades JPA. |

Los nombres y ubicaciones nuevos son propuestas técnicas; se adaptarán al código disponible al iniciar. Gerardo coordina el incremento; responsables compartidos y revisores se conservan según el documento de componentes.

## 3. Frontend y componentes React

- Verificar tema, proveedores y herramientas de pruebas existentes antes de componer la página; no reinicializar el monorepositorio. En la base consultada hay `build` y `typecheck`, sin script de pruebas.
- Reutilizar CR-01/03/05/08/09 y verificar CR-18 VisorEvidencia y CR-19 HistorialEstados antes de su consumo. CR-15 se requiere al integrar resultados de los formularios, sin crear otro proveedor de notificaciones.
- Implementar localmente resumen, recepción, comunicación y panel de decisión según UI-01; el adaptador recibe el DTO contractual y produce modelos de presentación de los CR.
- Mantener una consulta por despacho y una solicitud de evidencia por referencia. Asociar respuestas a recurso y generación de consulta; cancelar o descartar solicitudes obsoletas y retirar URLs al cerrar/cambiar/perder autorización.
- Programar actualización de la vista activa cada 30 segundos, sin superponer consultas; detener temporizador al desmontar y renovar al retomar la vista. Bloquear acciones durante actualización o después de su error hasta recuperar datos actuales.
- Usar fixtures etiquetados que incluyan varios ciclos del mismo despacho, `NO_INTENTADO`, máximo configurable, restricciones combinadas, histórico, datos desconocidos y permisos rechazados. Un adaptador simulado no acredita servidor ni almacenamiento real.
- Conservar filtros/página/tamaño de origen en la URL. Formularios reciben la identidad y versión consultadas; su ejecución queda en ES-F04-03/04/05. Su disponibilidad se verifica por separado antes de habilitar destinos.

## 4. Backend, persistencia e integraciones

- Entrada: implementar el GET de Gestión §5.3 sobre la base de JWT/errores existente; exigir `GESTOR_DESPACHO` antes de consultar existencia. No confiar en restricciones de la UI.
- Lectura: utilizar `ultima_incidencia_id`; cargar historial completo y comunicaciones locales, sin unir directamente tablas de Operación. Obtener último cambio de estado del historial y mantener campos de recepción de la misma salida.
- Consistencia: completar el DTO local dentro de una lectura transaccional consistente, terminarla y consultar Operación fuera de ella. Las consultas externas no mantienen bloqueos de base; `consultadoEn` no promete atomicidad entre servicios.
- Acciones: calcularlas con estado, recepción, anulación y máximo vigente; devolver todos los bloqueos en el orden contractual. Reutilizar reglas de dominio, sin duplicar una política distinta para cada pantalla.
- Datos/migraciones: en la base inspeccionada no aparecen migraciones SQL de estas tablas. Coordinar/reutilizar las de ES-F04-01 y del historial común; añadir solo cambios necesarios, con pruebas PostgreSQL. No crear un esquema completo duplicado para este GET.
- Historial: los comandos propietarios conservan en `datos` la incidencia y datos de operación; verificar su disponibilidad antes de acreditar historia real. No reconstruir operaciones antiguas con la incidencia actual ni inventar datos faltantes.
- Recepción: leer también su solicitud de `liberaciones_capacidad` según ES-F04-03; retorno y sincronización son independientes. El GET no entrega ni reencola la solicitud y no añade condiciones a la matriz de decisiones por su estado pendiente.
- Operación §5.4: reutilizar lotes de nombres/jornadas, aunque para el detalle sea una sola incidencia. Configurar un límite total de cinco segundos para este enriquecimiento, inferior al timeout de diez segundos del Gateway consultado; una caída produce datos desconocidos, no pérdida de la lectura local.
- Seguridad interna: credenciales de servicio según contratos de proveedor; su aprovisionamiento es DT-03. Sin acceso directo a otra base, credenciales de servicio en frontend ni scopes inventados.
- Evidencia: §3.4 valida JWT, Gestor o propietario local, asociación y objeto; firma HTTPS con parámetro vigente y errores normalizados. Verificar un Gestor sin perfil de repartidor y una evidencia histórica. No añadir compresión, EXIF, carga o retención al alcance.
- Efectos: GET y autorización de lectura no cambian despacho, recepción, contador, historial, reservas ni outbox. No publican ni reenvían eventos; emitir `Cache-Control: no-store` según contratos.
- Concurrencia: transportar identidad/versión a los comandos de Gestión §5.2, que reconocen repeticiones antes de validar una decisión nueva; el GET no requiere clave de idempotencia.

## 5. Orden de implementación

| Incremento | Resultado verificable | Tareas y dependencias | Criterios |
|---|---|---|---|
| I-01 | Base y componentes requeridos disponibles. | T-01/02; trabajos compartidos coordinados. | CCR aplicables; soporte de todos los CUI. |
| I-02 | Detalle aislado con fixtures de UI. | T-03, después de I-01. | CUI-01 a CUI-08, solo presentación/interacción. |
| I-03 | Datos y endpoint canónico autorizados. | T-04/05; migraciones y productores de DT-02. | CA-01/04/05/06/07/08/11. |
| I-04 | Enriquecimiento y evidencia autorizada comprobados. | T-06/07; contratos y credenciales internas. | CA-02/03/05/09/11. |
| I-05 | Página consumiendo APIs reales. | T-08; I-02/03/04 y Gateway disponible. | CA-01 a CA-11 salvo recorridos de comandos aún no disponibles. |
| I-06 | Destinos y regreso integrados con operaciones reales. | T-09; ES-F04-01/03/04/05 implementadas. | CA-07/10/11; CUI-02/06. |
| I-07 | Cobertura y revisión del incremento completas. | T-10; incrementos anteriores verificados. | CA-01 a CA-11 y CUI-01 a CUI-08. |

El frontend aislado y el backend pueden prepararse por separado. La falta de formularios no impide desarrollar la lectura; su recorrido real queda pendiente hasta I-06 y no se simula como completado.

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y dependencia |
|---|---|---|
| CA-01 | DTO completo, estado y comunicaciones del despacho correcto. | Integración PostgreSQL y UI real; nombres/jornada identificados como reales o doble. |
| CA-02 | URL firmada, renovación, permisos y recurso correcto. | Contrato de Operación, objeto privado de prueba y CR-18; doble solo para UI aislada. |
| CA-03 | Ausencia legítima frente a referencia esperada ausente. | Backend y UI con ambos casos; sin buscar otra foto. |
| CA-04 | Despacho inexistente, sin incidencia y referencia inconsistente. | Integración con `404` específicos y `500` contractual sin datos parciales. |
| CA-05 | Token no aceptado, otro rol y pérdida de autorización. | Seguridad de ambos endpoints y retirada de datos/URL en UI; emisor real se registra aparte del temporal local. |
| CA-06 | Dos fallos con recepción/evidencia diferentes. | Persistencia y UI; un ciclo anterior recibido y otro pendiente. |
| CA-07 | Combinaciones de recepción/anulación/contador y máximo variable. | Regla de dominio y UI; contador menor/igual/superior al máximo. |
| CA-08 | Operaciones sin transición, origen automático, orden empatado y consulta posterior. | Integración de historial y CR-19, sin inventar estado Recibido. |
| CA-09 | Timeout de lotes, nombre/jornada desconocidos y fallos de autorización/imagen. | Dobles controlados, luego servicios reales; recuperación por bloque. |
| CA-10 | Temporizador, respuestas fuera de orden, conflicto y regreso con URL. | Pruebas de interacción con reloj controlado y recorrido real de I-06. |
| CA-11 | Comparar datos antes/después de lecturas y renovación, controlando el procesador autónomo de liberaciones para no atribuirle efectos al GET. | Integración de persistencia, reservas e historial/outbox; sin reenvíos disparados por leer. |
| CUI-01 a CUI-08 | Matrices de UI, teclado, foco, móvil y ampliación. | Fixtures identificados y página real conectada. |

Comandos previstos: `npm run typecheck` y `npm run build` desde el frontend; `./mvnw.cmd test` desde Gestión, Operación y Gateway cuando corresponda. Configurar y registrar el comando de pruebas de interacción en T-01; no se afirma que exista actualmente. Testcontainers necesita Docker. Los resultados, commits, preparación y límites se registrarán en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

### Actualización de implementación del 16/10/2026

- Se reutilizan migraciones y persistencia de ES-F04-01/F-02. `V5__consulta_detalle_incidencia.sql` añade únicamente la solicitud durable de liberación leída por el detalle; su comando y procesador quedan en ES-F04-03.
- Operación añade metadatos de evidencia y el parámetro de vigencia en `V3__lectura_evidencias.sql`; no implementa carga ni asociación de F-03. El adaptador de firma usa Supabase Storage privado, conforme a la propuesta C4, con configuración opcional exclusiva del servidor y error de indisponibilidad mientras falte.
- La consulta local usa `REPEATABLE_READ`; el enriquecimiento posterior usa el adaptador existente con un límite total de cinco segundos, sin prolongar la transacción.
- El frontend incorpora ruta, adaptador validado, temporizador de 30 segundos, cancelación de consultas y renovación explícita del visor; no guarda URLs temporales. Los formularios se integrarán mediante callbacks con identidad, versión y resultado.
- Hallazgo heredado: dos migraciones de Gestión usan `V3` (`programacion_despachos` y `zonas_codigos_postales`). Antes de ejecutar PostgreSQL debe revisarse el historial Flyway de cada entorno; no se renumeran migraciones ya aplicadas por conjetura.
- T-09 sigue bloqueada por ES-F04-03/04/05. No se habilitan enlaces a formularios inexistentes ni se ejecutan recepciones/decisiones simuladas.

| ID | Decisión o pendiente | Fuente y coordinación | Bloquea |
|---|---|---|---|
| DT-01 | Disponibilidad y evidencia de CR-08/18/19 y dependencias; herramientas frontend. | Componentes §§4.2/4.5; Gerardo con Max y responsables de base. | I-01/02 y verificación de UI real. |
| DT-02 | Migraciones de despacho/incidencia, historial y outbox; productores que registran datos por salida. | Modelo, ES-F04-01 y RT-02/03; Gerardo con Arquitectura y responsables F-02/F-03. | I-03 e historia real de I-07. |
| DT-03 | Proveedor de lotes, credenciales internas y almacenamiento privado configurado. | Operación §§3.4/5.4; Gerardo con Max, Luis y Rhamses según responsabilidad. | Integración real de I-04/05/07, no fixtures. |
| DT-04 | Listado y formularios implementados; validación de identidad/versión y notificaciones. | ES-F04-01/03/04/05; Gerardo. | I-06 y cierre completo de CA-10. |
| DT-05 | Leer máximos y TTL desde parámetros válidos; uso de `America/Lima`. | Contratos y modelo; valores iniciales documentados, sin fijarlos en UI. | Aceptación de CA-02/07 y fechas locales. |

Los contratos están definidos documentalmente; estos pendientes se refieren a disponibilidad, coordinación y verificación técnica. Al iniciar se actualizan con evidencia, sin ampliar el alcance para implementar otras funcionalidades completas.

## 8. Condiciones para iniciar y cerrar

- [ ] Entradas revisadas y pendientes del incremento que se inicia resueltos.
- [ ] Componentes necesarios verificados antes de componer su pantalla consumidora.
- [ ] Tareas cubren todos los criterios y distinguen dependencias reales de simuladas.
- [ ] APIs, propiedad de datos, errores y ausencia de efectos cumplen sus contratos.
- [ ] CA-01 a CA-11 y CUI-01 a CUI-08 tienen evidencia real; revisión técnica y funcional registrada.

## 9. Referencias

- [cite: 1] [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
- [cite: 2] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §§5.2/5.3; [Operación](../../integraciones/api-contract-operacion-reparto.md), §§3.4/5.4; [convenciones comunes](../../integraciones/api-contract.md), §§3/9.
- [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), [componentes React](../../disenio/componentes-react.md) y [flujo SDD](../../plantillas/sdd/README.md).
