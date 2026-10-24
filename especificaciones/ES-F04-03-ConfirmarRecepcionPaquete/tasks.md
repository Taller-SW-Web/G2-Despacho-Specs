# Tareas de ES-F04-03: Confirmar la recepción del paquete

**Responsable de coordinación:** Gerardo.

**Estado:** Implementación local de Gestión y frontend disponible; integración real y cierre pendientes. Actualizado el 24/10/2026 con los commits y resultados de [evidence.md](./evidence.md).

**Plan de origen:** [plan.md](./plan.md), preparación SDD del 15/10/2026 sobre la revisión funcional de esta conversación.

## 1. Orden y dependencias

| ID | Resultado verificable | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Base y controles compartidos necesarios comprobados. | Frontend/calidad | DT-01 | CCR aplicables; soporte de CUI | Completada |
| T-02 | Modal completo con fixtures identificados. | Frontend | T-01 | CUI-01 a CUI-08 | En curso |
| T-03 | Persistencia preparada y referencia original preservada. | Datos | DT-02; base de despachos/incidencias | CA-01/03/07/08/11 | En curso |
| T-04 | Recepción autorizada y atómica. | Backend Gestión | T-03 | CA-01/02/04/05/06/08/11 | Completada |
| T-05 | Repeticiones y concurrencia protegidas. | Backend Gestión | T-04 | CA-03/04/07/10 | Completada |
| T-06 | Reserva liberada una vez en Operación. | Backend Operación | Reservas y DT-03 | CA-01/03/06/07/09 | Pendiente |
| T-07 | Procesador recuperable con diagnóstico y calendario. | Backend Gestión | T-04/05/06; DT-03 | CA-01/03/07/08/09 | En curso |
| T-08 | Modal conectado, recuperación y origen actualizados. | Frontend/integración | T-02/04/05; lecturas ES-F04-01/02 | CA-01 a CA-12; todos los CUI | En curso |
| T-09 | Recorrido real Gestión–Operación–F02/F06. | Integración | T-06/07/08; DT-04 | CA-01/03/07/09/11/12 | Pendiente |
| T-10 | Cobertura, documentos y revisión cerrados. | Calidad | T-01 a T-09 | Todos los CA/CUI | En curso |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar causa/responsable cuando se bloquee. Los pendientes del plan se resuelven antes del incremento afectado; crear estos documentos no completa ninguna tarea.

T-01/04/05 se completan dentro de su alcance local comprobado; no equivalen a aceptación de todos los CA ni a habilitación de históricos reales. T-06 pertenece a Operación, fuera de los cambios autorizados; su proveedor real no se modificó ni se verificó en esta entrega. Los límites abiertos de T-02/03/07/08/09/10 se detallan a continuación.

## 2. Detalle de tareas

### T-01. Preparar herramientas y controles necesarios

- [x] Implementada y verificada para las dependencias consumidas por este flujo.
- Incremento/responsable: I-01; Gerardo coordina con responsables compartidos, sin reasignarlos.
- Alcance/entradas: comprobar repositorios actuales, scripts, tema/proveedores y CR-01/02/08/09/15 del [catálogo](../../disenio/componentes-react.md); habilitar herramientas de interacción si faltan.
- Dependencias/bloqueo: DT-01; revisar evidencia de controles antes de consumirlos. No reinicializar el monorepositorio.
- Verificación ejecutada: `npm run typecheck`, `npm run build -w @despacho/administrativo` y `npm run test:f04`; doble activación, etiquetas, errores, `false` y aviso de efecto pendiente cubiertos. No se modificaron bibliotecas compartidas ni se declara completitud global de los CR.
- Evidencia: [EV-04](./evidence.md#ev-04-modal-estados-y-accesibilidad), frontend `779f6c4` y registro `9108caf`.

### T-02. Componer el modal y sus estados

- [ ] Implementada y verificada.
- Incremento/responsable: I-02; Gerardo, revisión visual propuesta con Max.
- Alcance/entradas: UI-01, CUI-01 a CUI-08; resumen, selección sin valor inicial, observación opcional/contador y estados de envío, rechazo y resultado desconocido.
- Dependencias/bloqueo: T-01; usar fixtures de los contratos expresamente identificados, sin atribuirles integración real.
- Verificación/cierre: interacción con teclado, clic repetido, No sin texto, espacios/emojis, conflicto, autorización, foco, móvil y ampliación; cada estado de UI reproducible.
- Avance: modal y estados implementados en `779f6c4`; 10 pruebas propias y revisión manual de teclado, foco y móvil aprobadas con datos simulados. Quedan ampliación al 200 % y revisión con Max.
- Evidencia: [EV-04](./evidence.md#ev-04-modal-estados-y-accesibilidad), límites y captura en `9108caf`. Se conserva la casilla abierta por las verificaciones pendientes.

### T-03. Preparar datos y migraciones de recepción

- [ ] Implementada y verificada.
- Incremento/responsable: I-03; Gerardo coordina con Arquitectura y productores F-02/F-03.
- Alcance/entradas: modelo §3.4 y plan §4; instantánea de reserva en incidencia, solicitud durable e índices/restricciones. Coordinar clave de asignación de Operación con T-06.
- Dependencias/bloqueo: DT-02 y migraciones base; inspeccionar datos existentes y reconciliar solo con información verificable, sin adivinar reserva ni respuesta histórica.
- Verificación/cierre: migración en PostgreSQL vacío y base sintética previa; dos salidas conservan referencias distintas y unicidad por incidencia/reserva. Casos históricos incompletos resueltos o explícitamente bloqueados antes de habilitarlos.
- Avance: Flyway aplica V1/V2 en PostgreSQL vacío; esquema, unicidad y referencias por salida utilizados en `31e1f6e`, sin nueva migración V3. Los casos inconsistentes se rechazan sin inventar referencias ni respuestas originales.
- Evidencia: [EV-01](./evidence.md#ev-01-persistencia-recepción-y-seguridad). Pendientes inspección/reconciliación histórica real y prueba de actualización desde una base previa; T-04/05 se verifican con datos aislados válidos sin habilitar esos históricos.

### T-04. Registrar una recepción atómica y autorizada

- [x] Implementada y verificada en Gestión con PostgreSQL aislado.
- Incremento/responsable: I-03; Gerardo.
- Alcance/entradas: Gestión §5.2.1 y CA-01/02/04/05/06/08/11; validar formato/rol/contexto y guardar recepción, historial, versión, solicitud y respuesta original en una transacción.
- Dependencias/bloqueo: T-03; la reserva/jornada/repartidor local debe ser consistente. La caída de Operación no impide este registro.
- Verificación ejecutada: `./mvnw.cmd clean verify` en Gestión con PostgreSQL/Testcontainers; `202`, `false`, Unicode, autorización, errores y casos especiales. Fallos inyectados en las cuatro escrituras comprueban rollback íntegro, sin intentos extra ni eventos a Ventas.
- Evidencia: [EV-01](./evidence.md#ev-01-persistencia-recepción-y-seguridad), backend `31e1f6e`; 109 pruebas del servicio aprobadas, incluidas las de recepción.

### T-05. Proteger repeticiones y confirmaciones concurrentes

- [x] Implementada y verificada mediante transacciones concurrentes en PostgreSQL aislado.
- Incremento/responsable: I-03; Gerardo.
- Alcance/entradas: identidad/repetición de Gestión §5.2 y CA-03/04/07/10; recuperar respuesta aceptada antes de validar estado actual, comparando actor y cuerpo normalizado.
- Dependencias/bloqueo: T-04; control de versión/unicidad dentro de transacciones reales, no solo una comprobación previa al guardado.
- Verificación/cierre: dos transacciones concurrentes; mismo actor/cuerpo, actor diferente y contenido diferente; repetir después de resolver y con otra salida actual. Una recepción/historial/solicitud, original inmutable y `409` cuando corresponde.
- Evidencia: [EV-01](./evidence.md#ev-01-persistencia-recepción-y-seguridad), `31e1f6e`: carreras de repetición exacta, otro actor y otro contenido; respuesta original conservada tras liberar, resolver y cambiar de salida. Se comprueban unicidad y conteos finales.

### T-06. Liberar la reserva original en Operación

- [ ] Implementada y verificada.
- Incremento/responsable: I-04; Gerardo coordina con responsables de Operación y F-02/F-06.
- Alcance/entradas: Operación §§5.1/5.2, CA-01/03/06/07/09; autenticación técnica, pertenencia, liberación atómica y respuesta original al repetir. Conservar clave por operación de asignación.
- Dependencias/bloqueo: reservas implementadas, DT-03 y parte de migración coordinada en T-03; no crear otra reserva como sustitución.
- Verificación/cierre: `./mvnw.cmd test` en Operación; repetición sin doble descuento, reserva ajena/inexistente, jornada cerrada y dos salidas. Otra asignación con reserva anterior activa recibe conflicto; una clave repetida conserva su resultado.
- Evidencia: [EV-02](./evidence.md#ev-02-liberación-y-reservas-de-operación), no ejecutada para el proveedor real. Fuera del alcance autorizado de cambios de este incremento; requiere coordinación con Operación/F-02/F-06. Los dobles de Gestión no cierran esta tarea.

### T-07. Procesar liberaciones pendientes de forma recuperable

- [ ] Implementada y verificada.
- Incremento/responsable: I-05; Gerardo con coordinación de despliegue/credenciales por DT-03.
- Alcance/entradas: plan §4, Gestión §5.2.1 y CA-01/03/07/08/09; reclamación temporal, HTTP fuera de transacción, calendario persistido, revisión operativa y confirmación solo con respuesta válida.
- Dependencias/bloqueo: T-04/05/06. Se pueden usar dobles durante desarrollo; el resultado contra Operación real se verifica en T-09.
- Verificación/cierre: reloj controlado y reinicios tras guardar, reclamar, liberar remotamente y antes de confirmar localmente; dos procesadores, token vencido, `429/4xx/5xx`, respuesta incoherente y pérdida de respuesta. Sin solicitudes perdidas ni doble descuento.
- Avance: procesador y adaptador HTTP implementados en `31e1f6e`; reclamación, token vencido, calendario, errores, respuesta incoherente y recuperación probados con PostgreSQL y receptor controlado. No se modificó Operación.
- Evidencia: [EV-03](./evidence.md#ev-03-procesador-caídas-y-recuperación). Pendientes reinicios de procesos desplegados, credencial y proveedor reales en T-09; la recreación de un objeto en pruebas no acredita esos reinicios.

### T-08. Conectar el modal y recuperar el resultado

- [ ] Implementada y verificada.
- Incremento/responsable: I-06; Gerardo.
- Alcance/entradas: UI-01, CUI-01 a CUI-08 y Gestión §§5.2.1/5.3; cliente, contexto vigente, identidad original, recuperación y refresco de ambos orígenes.
- Dependencias/bloqueo: T-02/04/05 y consultas ES-F04-01/02; T-07 para observar sincronización real. No habilitar confirmación usando solo una fila obsoleta.
- Verificación/cierre: `npm run typecheck`, `npm run build` y pruebas de interacción; respuesta perdida exige consulta antes de repetición, `409` no traslada datos a otra incidencia y refresco fallido tras `202` conserva éxito. Filtros/foco y pendientes/confirmados/revisión visibles.
- Avance: `779f6c4` conecta listado/detalle al cliente API; consulta contexto actual, preserva la solicitud original, exige consulta antes de repetir y conserva éxito ante refresco fallido. Las 32 pruebas F-04/sesión pasan; incluyen una integración de componentes nueva por pantalla con APIs simuladas.
- Evidencia: [EV-04](./evidence.md#ev-04-modal-estados-y-accesibilidad), aprobada en su alcance local; [EV-05](./evidence.md#ev-05-recorrido-real-y-coherencia-del-módulo), pendiente con Gateway/servicios reales.

### T-09. Comprobar el recorrido real y las integraciones

- [ ] Implementada y verificada.
- Incremento/responsable: I-07; Gerardo con responsables F-02/F-06 y DevOps.
- Alcance/entradas: contratos reales y CA-01/03/07/09/11/12; recibir, reprogramar/cerrar mientras hay pendiente, liberar la reserva y permitir otra salida sin afectar su reserva nueva.
- Dependencias/bloqueo: T-06/07/08, DT-04 y servicios/lecturas reales disponibles; falta de integración queda pendiente, no acreditada con mocks.
- Verificación/cierre: recorrido desde listado y detalle; detener/reiniciar Operación/procesador, perder una respuesta y contrastar recepción, historial, ocupación y nuevas asignaciones. Jornada cerrada permanece cerrada y GET no dispara envíos.
- Evidencia: [EV-05](./evidence.md#ev-05-recorrido-real-y-coherencia-del-módulo), pendiente de commits/entorno, pasos reproducibles y resultados.

### T-10. Revisar cobertura y cerrar el incremento

- [ ] Implementada y verificada.
- Incremento/responsable: I-07; Gerardo, revisión técnica/humana pendiente.
- Alcance/entradas: T-01 a T-09, CA-01 a CA-12 y CUI-01 a CUI-08; completar registros con código, reportes, dependencias reales/simuladas y limitaciones.
- Dependencias/bloqueo: tareas previas verificadas; resolver fallos y pendientes que impidan cumplir el alcance. La validación documental no cierra esta tarea.
- Verificación/cierre: ejecutar las comprobaciones apropiadas del plan y revisar trazabilidad en ambos sentidos; contratos/índices coinciden y cada criterio tiene evidencia real aceptable.
- Avance: commits, comandos, resultados, cobertura y límites locales registrados el 24/10/2026; documentos e índice actualizados sin cambiar requisitos/contratos.
- Evidencia: [EV-01 a EV-05](./evidence.md#3-registros-de-verificación), con verificación local y pendientes separados. Faltan EV-02/05 reales, comprobaciones visuales pendientes y revisión humana; no hay PR de esta entrega registrado.

## 3. Cobertura de criterios

| Criterio | Tareas que implementan | Verificación/cierre | Evidencia prevista |
|---|---|---|---|
| CA-01 | T-03/04/06/07/08 | T-09/10 | EV-01/02/03/04/05 |
| CA-02 | T-02/04/08 | T-10 | EV-01/04 |
| CA-03 | T-03/05/06/07/08 | T-09/10 | EV-01/02/03/04/05 |
| CA-04 | T-02/04/05/08 | T-10 | EV-01/04 |
| CA-05 | T-02/04/08 | T-10 | EV-01/04 |
| CA-06 | T-02/04/06/08 | T-10 | EV-01/02/04 |
| CA-07 | T-03/05/06/07/08 | T-09/10 | EV-01/02/03/04/05 |
| CA-08 | T-03/04/07/08 | T-10 | EV-01/03/04 |
| CA-09 | T-06/07/08 | T-09/10 | EV-02/03/04/05 |
| CA-10 | T-02/05/08 | T-10 | EV-01/04 |
| CA-11 | T-03/04/08 | T-09/10 | EV-01/04/05 |
| CA-12 | T-02/08 | T-09/10 | EV-04/05 |
| CUI-01 a CUI-08 | T-01/02/08 | T-09/10 | EV-04/05 |

La última fila cubre cada CUI de [ui.md](./ui.md); el desglose individual, resultados locales y pendientes figuran en la evidencia. La reutilización necesaria está comprobada en T-01; no se declaran todos los CR completados.

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están completadas y verificadas.
- [ ] Cada CA/CUI tiene evidencia; fallos, simulaciones y límites quedan visibles.
- [ ] Recepción y liberación recuperable se verificaron con servicios reales.
- [ ] Documentos/índice reflejan la implementación y revisión del equipo.
- [ ] Commits/PR de implementación y revisión humana están enlazados.

## 5. Referencias

- [cite: 1] [Especificación](./spec.md) y [UI](./ui.md): criterios estables y comportamiento.
- [cite: 2] [Plan](./plan.md): incrementos, fuentes y pendientes DT-01 a DT-04.
- [cite: 3] [Evidencia](./evidence.md): registros reales y separación de preparación documental.
