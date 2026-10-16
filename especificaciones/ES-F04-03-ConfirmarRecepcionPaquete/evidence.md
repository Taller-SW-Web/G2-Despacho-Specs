# Evidencia de ES-F04-03: Confirmar la recepción del paquete

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Gerardo.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), migración SDD del 15/10/2026.
- Origen: archivo suelto ES-F04-03 sobre la base documental `0734268`, corregido en esta conversación antes de migrarlo. Se conservan CA-01 a CA-12 de esa revisión.
- Base de código consultada: frontend `d2bc27d` y backend `1e7834b`; lectura estática local, sin compilaciones ni pruebas funcionales.
- Commits de implementación, despliegue funcional, datos ejecutados y dependencias efectivamente probadas: pendientes.
- Alcance de esta entrega: preparación documental; la tabla, el procesador, el modal y los endpoints descritos siguen por implementar/verificar [cite: 1, 2].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-03/04/06/07/08/09/10 | Recepción atómica y liberación posterior. | EV-01/02/03/04/05 | No ejecutado |
| CA-02 | T-02/04/08/10 | Sello No sin observación y texto normalizado. | EV-01/04 | No ejecutado |
| CA-03 | T-03/05/06/07/08/09/10 | Original idéntico después de liberar/resolver, sin duplicados. | EV-01/02/03/04/05 | No ejecutado |
| CA-04 | T-02/04/05/08/10 | Estado, incidencia y versión incompatibles. | EV-01/04 | No ejecutado |
| CA-05 | T-02/04/08/10 | Campos/tipos, límites Unicode, espacios y emojis. | EV-01/04 | No ejecutado |
| CA-06 | T-02/04/06/08/10 | Permisos humanos/técnicos y retirada de datos. | EV-01/02/04 | No ejecutado |
| CA-07 | T-03/05/06/07/08/09/10 | Dos salidas y repetición contra la reserva original. | EV-01/02/03/04/05 | No ejecutado |
| CA-08 | T-03/04/07/08/10 | Fallos de persistencia y referencias inconsistentes. | EV-01/03/04 | No ejecutado |
| CA-09 | T-06/07/08/09/10 | Caída/reinicio, respuesta perdida y errores de integración. | EV-02/03/04/05 | No ejecutado |
| CA-10 | T-02/05/08/10 | Dos usuarios/contenidos concurrentes; primera recepción inmutable. | EV-01/04 | No ejecutado |
| CA-11 | T-03/04/08/09/10 | Casos especiales sin alterar intentos/jornada. | EV-01/04/05 | No ejecutado |
| CA-12 | T-02/08/09/10 | Resultado desconocido, recuperación exacta y origen actualizado. | EV-04/05 | No ejecutado |
| CUI-01 | T-01/02/08/09/10 | Contexto y navegación desde ambos orígenes. | EV-04/05 | No ejecutado |
| CUI-02 | T-01/02/08/10 | Selección explícita, opcionalidad y contador. | EV-04 | No ejecutado |
| CUI-03 | T-01/02/08/10 | Doble activación y envío demorado. | EV-04 | No ejecutado |
| CUI-04 | T-01/02/08/10 | Valores conservados y recuperación contractual. | EV-04/05 | No ejecutado |
| CUI-05 | T-01/02/08/09/10 | Conflicto/cambio de incidencia sin trasladar decisión. | EV-04/05 | No ejecutado |
| CUI-06 | T-01/02/08/09/10 | Recepción aceptada con liberación/refresco pendientes. | EV-04/05 | No ejecutado |
| CUI-07 | T-01/02/08/10 | Pérdida de autorización sin datos protegidos. | EV-04 | No ejecutado |
| CUI-08 | T-01/02/08/10 | Teclado, foco, móvil y ampliación. | EV-04 | No ejecutado |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Los fixtures/dobles acreditan únicamente los escenarios comprobados; no sustituyen la integración real.

## 3. Registros de verificación

### EV-01. Persistencia, recepción y seguridad

- Tareas/criterios: T-03/04/05/10; CA-01 a CA-08, CA-10/11.
- Preparación prevista: PostgreSQL aislado, dos salidas/reservas del mismo despacho, jornadas activa/cerrada, pedidos anulados, máximo y JWT de usuarios/roles diferentes; Docker para Testcontainers.
- Comando previsto: `./mvnw.cmd test` desde Gestión. Verificar migración vacía/histórica, rollback por fallo de escritura y carreras de dos transacciones.
- Esperado: `202`/errores contractuales, una recepción/historial/solicitud, respuesta original durable y referencias correctas; sin alterar intentos ni publicar a Ventas.
- Fecha, persona, commit/entorno, datos/fixtures exactos, salida observada y reporte: pendientes. **Resultado: No ejecutado.**

### EV-02. Liberación y reservas de Operación

- Tareas/criterios: T-06/10; CA-01/03/06/07/09.
- Preparación prevista: reservas activas/liberadas, despacho ajeno, segunda salida y jornada cerrada; credencial técnica configurada y casos de acceso no permitido.
- Comando previsto: `./mvnw.cmd test` desde Operación; registrar aparte las llamadas entre servicios reales.
- Esperado: una liberación, respuesta repetible sin doble descuento, errores de pertenencia/autorización y clave estable por asignación; reserva anterior activa impide otra asignación.
- Fecha, persona, commit/entorno, dependencias reales/dobles, salida observada y reporte: pendientes. **Resultado: No ejecutado.**

### EV-03. Procesador, caídas y recuperación

- Tareas/criterios: T-07/10; CA-01/03/07/08/09.
- Preparación prevista: solicitudes persistidas, reloj controlado, dos procesadores, respuestas demoradas/perdidas, `429/4xx/5xx` e identificadores incoherentes. Reiniciar en cada frontera del plan §6.
- Comandos previstos: pruebas de Gestión y recorrido de reinicio contra Operación; registrar los comandos/configuración reales al ejecutarlos, sin secretos.
- Esperado: próximo intento conservado, reclamación recuperable, revisión operativa y confirmación solo de la reserva esperada; ningún GET envía ni reencola y ningún reintento duplica historial/descuento.
- Fecha, persona, commits/entorno, calendario observado, consultas antes/después y artefactos: pendientes. **Resultado: No ejecutado.**

### EV-04. Modal, estados y accesibilidad

- Tareas/criterios: T-01/02/08/10; CA-01 a CA-12 en su alcance de interfaz y CUI-01 a CUI-08.
- Preparación prevista: herramientas/CR verificados en T-01, fixtures identificados de todos los estados y después Gateway real. Registrar evidencia de controles compartidos sin declararlos completos por esta preparación.
- Comandos previstos: `npm run typecheck`, `npm run build` y comando de interacción que se configure en T-01; recorrido manual de teclado/foco, móvil y ampliación al 200 %.
- Esperado: No sin observación aceptado, límites Unicode correctos, un envío, recuperación sin sustituir identidad y acceso protegido. Tras `202` conserva éxito aunque falle el refresco.
- Fecha, persona, commit/entorno, escenarios reales/simulados, salidas, capturas y reportes: pendientes. **Resultado: No ejecutado.**

### EV-05. Recorrido real y coherencia del módulo

- Tareas/criterios: T-08/09/10; CA-01/03/07/09/11/12 y CUI-01/04/05/06.
- Preparación prevista: Gateway, Gestión, Operación, identidad técnica y consultas de listado/detalle disponibles; datos sintéticos trazables y reglas F-02/F-06 implementadas.
- Pasos previstos: recibir desde ambos orígenes, interrumpir/reanudar Operación, consultar sin efectos, reprogramar/cerrar con liberación pendiente, intentar asignar y repetir el envío original después de una salida nueva.
- Esperado: retorno independiente de sincronización, capacidad conservadora hasta liberar, asignación posterior segura y jornada cerrada sin reapertura; ninguna reserva nueva se libera por un reintento antiguo.
- Fecha, persona, commits/despliegue, pasos exactos, resultados antes/después y artefactos: pendientes. **Resultado: No ejecutado.**

### EV-06. Preparación y validación documental

- Alcance: cinco documentos SDD, una versión activa, enlaces/índice e IDs conservados; no acredita implementación de T-01 a T-10.
- Preparación: migración del archivo revisado y lectura de plantillas, contratos, modelo, diseño/componentes y código local de §1.
- Fecha y herramienta: 15/10/2026, Codex mediante Git y PowerShell; revisión documental sobre `0734268`, incluida en el commit que introduce esta carpeta.
- Comprobaciones ejecutadas: `git diff --check`, enlaces/anclas locales, ejemplos JSON, cinco documentos con H1 único, IDs/cobertura, ausencia de la ruta anterior, marcadores y casillas de implementación completadas.
- Resultado observado: 463 enlaces/anclas locales y 24 ejemplos JSON válidos en 24 documentos nuevos/modificados; 12 CA, 8 CUI, 10 tareas y 6 registros. `spec.md` tiene 168 líneas sin bloques de código; los otros archivos tienen entre 113 y 150 líneas.
- **Resultado: Aprobado exclusivamente para preparación documental.** EV-01 a EV-05 siguen sin ejecutar; T-01 a T-10 y la revisión humana permanecen pendientes.

Al ejecutar EV-01 a EV-05, conservar commit/entorno, preparación reproducible y artefactos; ocultar tokens, credenciales y datos personales. EV-06 solo acredita documentación.

## 4. Uso de IA

| Trabajo | Herramienta/fecha | Entradas | Instrucción y revisión humana |
|---|---|---|---|
| Preparación SDD de ES-F04-03 | Codex, 15/10/2026 | Revisión funcional de esta conversación, plantillas SDD, contratos, modelo, componentes y bases de código de §1. | Gerardo solicitó crear los Markdown siguiendo la plantilla. Revisión humana pendiente; la conversación registra el proceso, no el cumplimiento de criterios. |

## 5. Diferencias, fallos y pendientes

| Hallazgo o pendiente | Criterios afectados | Impacto y siguiente acción |
|---|---|---|
| DT-01: componentes y herramientas aún sin comprobar para este flujo. | Todos los CUI. | T-01/02; coordinación de Gerardo con responsables compartidos. |
| DT-02: migraciones, referencias por salida e históricos por verificar. | CA-01/03/07/08/11. | T-03/04/05; Arquitectura y F-02/F-03 antes de habilitar datos afectados. |
| DT-03: liberación y procesador todavía sin integración real. | CA-01/03/06/07/09. | T-06/07/09; credenciales/despliegue con Operación y DevOps. |
| DT-04: orígenes, nueva asignación y ocupación por integrar. | CA-01/07/09/11/12. | T-08/09; comprobar F-02/F-06 y ES-F04-01/02 reales. |

## 6. Entrega y revisión

- Entrega actual: documentación SDD, referencias e índice; commit documental que introduce esta carpeta.
- Commits/PR de implementación, revisor, fecha y resultado de revisión: pendientes.
- Estado del alcance funcional: Pendiente; EV-01 a EV-05 no ejecutados.
- Integraciones reales pendientes: recepción/consulta de Gestión, liberación/reservas de Operación, procesador, Gateway, identidad y recorridos F-02/F-06.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md) y [UI](./ui.md): comportamiento y criterios.
- [cite: 2] [Plan](./plan.md), [tareas](./tasks.md) y [flujo SDD](../../plantillas/sdd/README.md): implementación incremental y evidencia.
- [cite: 3] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §§5.2.1/5.3; [Operación](../../integraciones/api-contract-operacion-reparto.md), §§5.1/5.2; [modelo de datos](../../arquitectura/modelo-datos.md), §3.4.
