# Tareas de ES-F04-02: Consultar el detalle de una incidencia

**Responsable de coordinación:** Gerardo.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), misma revisión documental de esta carpeta.

Todas las tareas comienzan pendientes. La preparación de estos documentos no acredita componentes, endpoints ni criterios implementados. Los responsables compartidos son referencias de coordinación según el reparto existente; no se crean issues ni se envían asignaciones externas [cite: 2].

## 1. Orden y dependencias

| ID | Resultado | Área/incremento | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Base y herramientas de verificación disponibles. | Preparación, I-01 | DT-01. | Soporte de CUI-01 a CUI-08. | Pendiente |
| T-02 | Componentes del detalle verificados. | Compartidos, I-01 | T-01 y dependencias de cada CR. | CCR-08-01, CCR-18-01/02, CCR-19-01; soporte de CUI. | Pendiente |
| T-03 | Página aislada con fixtures de todos los estados. | Frontend, I-02 | T-02. | CUI-01 a CUI-08. | Pendiente |
| T-04 | Fuentes locales e historia por incidencia disponibles. | Datos, I-03 | DT-02; coordinación con ES-F04-01 y RT-02/03. | CA-01/04/06/08/11. | Pendiente |
| T-05 | GET canónico autorizado y reglas probadas. | Backend, I-03 | T-04; seguridad/errores existentes verificados. | CA-01/03/04/05/06/07/08/11. | Pendiente |
| T-06 | Enriquecimiento operativo con degradación comprobado. | Integración, I-04 | T-05 y proveedor/credenciales DT-03. | CA-01/06/09/11. | Pendiente |
| T-07 | Lectura temporal de evidencia integrada. | Operación/F-03, I-04 | Contrato de lectura, asociación, almacenamiento y DT-03. | CA-02/03/05/09/11. | Pendiente |
| T-08 | Página conectada, actualizada y protegida ante respuestas obsoletas. | Integración, I-05 | T-03/05/06/07 y Gateway. | CA-01 a CA-11, excepto recorridos de comandos de T-09; CUI-01 a CUI-08. | Pendiente |
| T-09 | Formularios y regreso al listado integrados con sus propietarios. | Integración, I-06 | T-08, ES-F04-01/03/04/05 y DT-04. | CA-07/10/11; CUI-02/06. | Pendiente |
| T-10 | Cobertura, evidencia y revisión final completas. | Calidad, I-07 | T-01 a T-09 verificadas. | Todos los CA y CUI del alcance. | Pendiente |

Estados: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Al iniciar una tarea sin dependencia disponible se registra bloqueo, responsable de coordinación y siguiente acción. Los dobles permiten comprobar incrementos aislados, sin cerrar integración real.

## 2. Detalle de tareas

### T-01. Verificar la base de ejecución y pruebas

- [ ] Implementada y verificada.
- Incremento y responsable: I-01; Gerardo coordina con Max/Rhamses la base existente.
- Alcance y entradas: revisar proveedores, tema, cliente y herramientas en frontend `d2bc27d`; backend `1e7834b`, seguridad y prefijos del Gateway; plan §§1–4 y DT-01.
- Dependencias: disponibilidad del entorno, no reinicializar repositorios ni modificar versiones por rutina.
- Verificación: ejecutar `npm run typecheck` y `npm run build`; habilitar y documentar una prueba de interacción reproducible. Registrar comprobaciones de seguridad/transporte que se reutilizarán.
- Cierre/evidencia: comandos y resultados reales en EV-02; compilar la base no acredita los criterios del detalle.

### T-02. Implementar o reutilizar los componentes del detalle

- [ ] Implementada y verificada.
- Incremento y responsable: I-01; Gerardo para CR-08/18/19, coordinación con sus revisores y responsables de CR-01/03/05/09.
- Alcance y entradas: verificar contratos y exportaciones en `packages/componentes-compartidos`; enlazar trabajo ya realizado en vez de duplicarlo. Usar UI §2 y documento compartido §4.5.
- Dependencias: T-01 y las dependencias documentadas por cada CR; CR-15 se comprueba antes de T-09.
- Verificación: CCR-08-01, renovación/cambio de recurso de CR-18 y recepción sin transición/orden estable de CR-19; teclado y retorno de foco. Los componentes visuales no realizan HTTP ni deciden permisos.
- Cierre/evidencia: pruebas compartidas y commits enlazados en EV-02; integración en la página todavía pendiente.

### T-03. Componer el detalle con fixtures identificados

- [ ] Implementada y verificada.
- Incremento y responsable: I-02; Gerardo, revisión de UI con Max.
- Alcance y entradas: ruta de UI-01, composiciones locales, bloques de historial/comunicación, visor y panel; `ui.md` y fixtures compatibles con los contratos.
- Dependencias: T-02; no necesita que los servicios reales estén desplegados.
- Verificación: CUI-01 a CUI-08 con combinaciones de recepción/anulación/límite, histórico, errores, cambios de recurso, temporizador y URL de origen; llamadas a formularios mediante dobles identificados.
- Cierre/evidencia: EV-04 distingue fixtures de API real; no presentar confirmaciones simuladas como recepciones o decisiones persistidas.

### T-04. Preparar las fuentes canónicas y su historial

- [ ] Implementada y verificada.
- Incremento y responsable: I-03; Gerardo con Arquitectura y responsables de los comandos productores.
- Alcance y entradas: modelo §§3.3–3.5; reutilizar migraciones y fuentes de ES-F04-01, referencia a última incidencia, parámetros, recepción, historial por operación y estado local de outbox.
- Dependencias: DT-02; verificar persistencia real y datos registrados por F-02/F-03/F-04 antes de afirmar historia completa.
- Verificación: dos ciclos con recepciones y evidencias distintas; `NO_INTENTADO`, fechas empatadas, recepción sin transición y consulta posterior al cierre. Añadir/probar solo migraciones necesarias con PostgreSQL aislado.
- Cierre/evidencia: EV-01 documenta esquema, preparación y datos históricos; no rellenar eventos previos con la incidencia actual.

### T-05. Implementar la consulta autorizada y las acciones

- [ ] Implementada y verificada.
- Incremento y responsable: I-03; Gerardo.
- Alcance y entradas: GET de Gestión §5.3, lectura consistente, DTO, matriz de acciones, historial/comunicaciones, `no-store` y errores normalizados; `spec.md`, CA-01/03/04/05/06/07/08/11.
- Dependencias: T-04; verificar la base JWT/errores existente. Operación puede sustituirse por un doble explícito en este incremento.
- Verificación: prueba de integración del endpoint con JWT válido/otro rol/token no aceptado, inexistencia e inconsistencias, máximo variable y todas las restricciones combinadas; comparar datos antes/después de repetir lecturas.
- Cierre/evidencia: EV-01 con reportes y commit backend; el doble no acredita T-06/07.

### T-06. Integrar nombres y jornadas sin perder los datos locales

- [ ] Implementada y verificada.
- Incremento y responsable: I-04; Gerardo coordina proveedor con responsables de F-05/F-06.
- Alcance y entradas: reutilizar Operación §5.4 y su adaptador de Gestión; límite total de enriquecimiento y degradación del plan §4; identidad de la jornada de incidencia.
- Dependencias: T-05, proveedor y credenciales DT-03. No consultar tablas ajenas ni sustituir jornada desconocida por activa.
- Verificación: jornada activa/cerrada/desconocida, nombre ausente, timeout y respuesta incoherente; mantener lectura local y atraso `null` cuando corresponda. Repetir contra proveedor real tras los dobles.
- Cierre/evidencia: EV-03 registra proveedor, autenticación, límites y resultados reales; sin mutaciones de jornada/capacidad.

### T-07. Integrar el acceso temporal a evidencia de F-03

- [ ] Implementada y verificada.
- Incremento y responsable: I-04; Gerardo coordina con Max para F-03 y Rhamses para almacenamiento/configuración.
- Alcance y entradas: implementar o reutilizar Operación §3.4; asociación, propiedad, permisos del Gestor, firma/vencimiento y errores. No ampliar a carga, compresión o retención.
- Dependencias: DT-03 y evidencia asociada real; un Gestor no requiere perfil de repartidor.
- Verificación: evidencia propia/ajena, Gestor sin perfil local, histórico, referencia ausente, no asociada, objeto inaccesible y URL vencida/renovada. Comprobar recursos privados y retirada de URLs en CR-18.
- Cierre/evidencia: EV-03 identifica objeto y dependencias sintéticas sin publicar enlaces firmados; firma real y autorización se distinguen de una URL simulada.

### T-08. Conectar la página y controlar actualización y sesión

- [ ] Implementada y verificada.
- Incremento y responsable: I-05; Gerardo.
- Alcance y entradas: cliente existente hacia Gestión/Operación por Gateway, adaptación a CR, temporizador de 30 segundos, descartes de respuestas antiguas y retirada de datos protegidos; plan §3 y UI §5.
- Dependencias: T-03/05/06/07 y configuración accesible; no exponer credenciales internas en el navegador.
- Verificación: respuestas fuera de orden, cambio de incidencia/estado/anulación, renovación de foto, `401/403`, fallo de actualización y recuperación; CUI-01 a CUI-08 sobre la página conectada.
- Cierre/evidencia: EV-04 indica qué servicios son reales; mantener pendiente el recorrido de formularios hasta T-09.

### T-09. Integrar formularios propietarios y restaurar el listado

- [ ] Implementada y verificada.
- Incremento y responsable: I-06; Gerardo y responsables de los componentes compartidos usados por confirmaciones.
- Alcance y entradas: enlazar ES-F04-03/04/05 con identidad y versión; refrescar tras recibir, regresar tras resolver, restaurar URL y recargar ES-F04-01. No reimplementar sus reglas dentro del GET.
- Dependencias: T-08, implementaciones verificadas de ES-F04-01/03/04/05 y CR-15; DT-04 se mantiene visible mientras falten.
- Verificación: recibir y decidir, petición desactualizada con `409`, reintento exacto sin duplicados y una salida nueva que nunca recibe la decisión anterior automáticamente.
- Cierre/evidencia: EV-04/05 con recorrido real y commits propietarios; los enlaces a destinos inexistentes o confirmaciones ficticias no cierran esta tarea.

### T-10. Verificar cobertura y registrar la revisión

- [ ] Implementada y verificada.
- Incremento y responsable: I-07; Gerardo coordina revisión técnica/funcional con el equipo.
- Alcance y entradas: matriz de §3, plan §6 y `evidence.md`; ejecutar cobertura faltante, teclado/móvil y comprobación de ausencia de efectos de negocio.
- Dependencias: T-01 a T-09 verificadas; servicios reales y configuración disponibles.
- Verificación: comandos frontend, pruebas de Gestión/Operación/Gateway aplicables y recorridos reproducibles; comparar contador, recepción, historial, reservas y outbox antes/después de lecturas.
- Cierre/evidencia: EV-01 a EV-05 con resultados, commits, límites y revisión humana; ningún criterio se aprueba solo por la validación documental EV-06.

## 3. Cobertura de criterios

| Criterio | Tareas que implementan | Comprobación y evidencia prevista |
|---|---|---|
| CA-01 | T-03/04/05/06/08 | T-10; EV-01/03/04. |
| CA-02 | T-02/03/07/08 | T-10; EV-02/03/04. |
| CA-03 | T-03/05/07/08 | T-10; EV-01/03/04. |
| CA-04 | T-03/04/05/08 | T-10; EV-01/04. |
| CA-05 | T-02/03/05/07/08 | T-10; EV-01/02/03/04. |
| CA-06 | T-03/04/05/06/08 | T-10; EV-01/04. |
| CA-07 | T-03/05/08/09 | T-10; EV-01/04. |
| CA-08 | T-02/03/04/05/08 | T-10; EV-01/02/04. |
| CA-09 | T-03/06/07/08 | T-10; EV-03/04. |
| CA-10 | T-03/08/09 | T-10; EV-04/05. |
| CA-11 | T-04/05/06/07/08/09 | T-10; EV-01/03/05. |
| CUI-01 | T-03/08 | T-10; EV-04. |
| CUI-02 | T-03/08/09 | T-10; EV-04. |
| CUI-03 | T-02/03/08 | T-10; EV-02/04. |
| CUI-04 | T-02/03/07/08 | T-10; EV-02/03/04. |
| CUI-05 | T-02/03/08 | T-10; EV-02/04. |
| CUI-06 | T-03/08/09 | T-10; EV-04/05. |
| CUI-07 | T-03/06/07/08 | T-10; EV-03/04. |
| CUI-08 | T-02/03/08 | T-10; EV-02/04. |

Todas las comprobaciones de esta matriz están pendientes; resultados en `evidence.md`. La misma numeración se conserva al implementar [cite: 1, 3].

## 4. Cierre de la especificación

- [ ] T-01 a T-10 completadas con verificación y referencias de evidencia.
- [ ] Todos los CA/CUI cubiertos; fallos y limitaciones documentados.
- [ ] Integraciones reales distinguidas de fixtures y dobles; sin dependencias del alcance ocultas.
- [ ] Documentación e índice coherentes, con revisión del equipo y commits/PR de implementación enlazados.

## 5. Referencias

- [cite: 1] [Especificación](./spec.md), CA-01 a CA-11, y [UI](./ui.md), CUI-01 a CUI-08.
- [cite: 2] [Plan](./plan.md), incrementos/pendientes; [componentes React](../../disenio/componentes-react.md), §4.5.
- [cite: 3] [Evidencia](./evidence.md), registros EV-01 a EV-06; EV-06 es exclusivamente documental.
