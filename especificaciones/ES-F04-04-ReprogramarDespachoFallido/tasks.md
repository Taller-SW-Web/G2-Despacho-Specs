# Tareas de ES-F04-04: Reprogramar un despacho fallido

**Responsable de coordinación:** Gerardo.

**Estado:** Implementación local verificada el 24/10/2026. T-01 a T-05 completadas; T-06/07/08 en curso por integración conjunta y revisión humana. Resultados y límites en [evidence.md](./evidence.md).

**Plan de origen:** [plan.md](./plan.md), preparación SDD del 16/10/2026 sobre revisión funcional `c8e6e29`.

## 1. Orden y dependencias

| ID | Resultado verificable | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Base de pruebas y controles disponibles. | Frontend/calidad | DT-01; controles compartidos | CA-02/09/15/17; CUI-01 a CUI-08 | Completada |
| T-02 | Modal y recuperación con fixtures. | Frontend | T-01 | CA-02/03/04/05/07/09/17; CUI-01 a CUI-08 | Completada |
| T-03 | Persistencia durable preparada. | Datos | Base canónica; DT-02; historial RT-02 | CA-01/08/10/12/13/14/16 | Completada |
| T-04 | Comando de reprogramación atómico. | Backend Gestión | T-03; ES-F04-06 T-03 | CA-01/02/03/04/05/06/07/09/13/14/15/16/18 | Completada |
| T-05 | Concurrencia y repetición verificadas. | Backend/calidad | T-04 | CA-04/07/08/10/11/14 | Completada |
| T-06 | Formulario conectado al contrato. | Frontend/integración | T-02/T-04/T-05; ES-F04-01/02 | CA-01/02/03/04/05/07/08/09/12/15/17; CUI-01 a CUI-08 | En curso |
| T-07 | Recorrido entre funcionalidades y eventos. | Integración | T-05/T-06; DT-03 | CA-01/06/11/12/13/14/16 | En curso |
| T-08 | Cobertura y revisión de aceptación. | Calidad | T-01 a T-07 | CA-01 a CA-18; CUI-01 a CUI-08 | En curso |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar causa y responsable de cada bloqueo. Las tareas de componentes o servicios compartidos se verifican antes de consumirlos; esta carpeta no los da por completados.

Se reutilizó la base de ES-F04-03. T-03 incorpora V3 y captura común RT-02 dentro de la transacción; T-05 acredita carreras PostgreSQL y dobles SQL de cierre/anulación, cuya integración por APIs queda en T-07. T-06 verifica navegador → proxy de pruebas → Gestión real; Gateway/Seguridad desplegados siguen pendientes. T-07 conserva liberación/asignación/nueva salida y proveedores reales como pendientes. T-08 requiere esas verificaciones y revisión humana. La regresión compartida detectó un fallo heredado de CR-03, documentado en EV-03; no se modificó ese componente.

## 2. Detalle de tareas

### T-01. Base de pruebas y controles disponibles

- [x] Implementada y verificada en el alcance local de esta tarea.

- Incremento/responsable: I-01; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Comprobar el tema, proveedores y CR-01/02/08/09/15; reutilizar la base de ES-F04-03 y añadir la herramienta de interacción que aún falta. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-02/09/15/17; CUI-01 a CUI-08.
- Dependencias: DT-01; controles compartidos.
- Verificación y condición de cierre: Desde frontend ejecutar `npm run typecheck`, `npm run build` y el comando de interacción incorporado; verificar controles antes de consumirlos.
- Evidencia: [EV-03](./evidence.md#ev-03-modal-contrato-y-accesibilidad); resultados, artefactos, commits y límites registrados el 24/10/2026.
- Límites y bloqueos: No reinicializar el monorepositorio ni dar por implementados los CR por estar especificados.

### T-02. Modal y recuperación con fixtures

- [x] Implementada y verificada en el alcance local de esta tarea.

- Incremento/responsable: I-02; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Implementar UI-01, fecha vacía, contador dinámico, observación, bloqueo y recuperación; fixtures explícitamente simulados. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-02/03/04/05/07/09/17; CUI-01 a CUI-08.
- Dependencias: T-01.
- Verificación y condición de cierre: Probar reloj UTC/Lima/navegador, cambio de día, emojis, doble envío, conflictos, pérdida de respuesta y teclado/móvil.
- Evidencia: [EV-03](./evidence.md#ev-03-modal-contrato-y-accesibilidad); resultados, artefactos, commits y límites registrados el 24/10/2026.
- Límites y bloqueos: Los fixtures no acreditan el endpoint ni F-02.

### T-03. Persistencia durable preparada

- [x] Implementada y verificada en el alcance local de esta tarea.

- Incremento/responsable: I-03; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Añadir la migración de `reprogramaciones_despacho` del modelo; conservar historial, última incidencia y solicitud original al retirar asignación vigente. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/08/10/12/13/14/16.
- Dependencias: Base canónica; DT-02; historial RT-02.
- Verificación y condición de cierre: Aplicar en PostgreSQL vacío y con datos sintéticos previos; probar unicidad y replay tras reinicio sin fabricar respuestas históricas.
- Evidencia: [EV-01](./evidence.md#ev-01-persistencia-fecha-y-seguridad), [EV-02](./evidence.md#ev-02-concurrencia-y-recuperación-durable); resultados, artefactos, commits y límites registrados el 24/10/2026.
- Límites y bloqueos: Coordinar tablas base y escritor con ES-F04-06 T-02/T-03; no duplicarlos.

### T-04. Comando de reprogramación atómico

- [x] Implementada y verificada en el alcance local de esta tarea.

- Incremento/responsable: I-03; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Implementar Gestión §5.2.2, reloj/política, permisos y transacción con historial/resultado/evento; preservar contador y zona. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/02/03/04/05/06/07/09/13/14/15/16/18.
- Dependencias: T-03; ES-F04-06 T-03.
- Verificación y condición de cierre: Desde Gestión ejecutar `./mvnw.cmd test` con PostgreSQL; cubrir reglas, límites, 200/400/401/403/404/409/422/500/503 y rollback de cada escritura.
- Evidencia: [EV-01](./evidence.md#ev-01-persistencia-fecha-y-seguridad); resultados, artefactos, commits y límites registrados el 24/10/2026.
- Límites y bloqueos: Backend y fixtures pueden avanzar separados; esta tarea requiere base y captura común disponibles.

### T-05. Concurrencia y repetición verificadas

- [x] Implementada y verificada en el alcance local de esta tarea.

- Incremento/responsable: I-04; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Recuperar el resultado original antes de validar estado/fecha, rechazar otra identidad/contenido/actor y competir con cierre/anulación. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-04/07/08/10/11/14.
- Dependencias: T-04.
- Verificación y condición de cierre: Dos transacciones reales; duplicado exacto, dos decisiones distintas, cambio de día y replay tras asignación/nueva incidencia: una transición, un historial y un evento.
- Evidencia: [EV-02](./evidence.md#ev-02-concurrencia-y-recuperación-durable); resultados, artefactos, commits y límites registrados el 24/10/2026.
- Límites y bloqueos: Coordinar cierre y anulación con sus propietarios; comprobar el conflicto, no redefinir sus contratos.

### T-06. Formulario conectado al contrato

- [ ] Integración y aceptación final pendientes; implementación local comprobada.

- Incremento/responsable: I-05; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Conectar cliente/tipos al Gateway; contexto vigente, consulta previa al replay y regreso con filtros/página. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/02/03/04/05/07/08/09/12/15/17; CUI-01 a CUI-08.
- Dependencias: T-02/T-04/T-05; ES-F04-01/02.
- Verificación y condición de cierre: Pruebas de interacción y recorrido HTTP real; 200 conserva éxito ante refresco fallido, 409 no sustituye IDs y 401/403 retiran datos.
- Evidencia: [EV-03](./evidence.md#ev-03-modal-contrato-y-accesibilidad); resultados, artefactos, commits y límites registrados el 24/10/2026.
- Límites y bloqueos: Mantener el detalle como dueño de su actualización; sin temporizador paralelo del modal.

### T-07. Recorrido entre funcionalidades y eventos

- [ ] Integración y aceptación final pendientes; implementación local comprobada.

- Incremento/responsable: I-06; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Verificar cola inmediata, asignación por fecha/reserva, recepción por nueva salida y evento RT-03 en reales/simulados. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/06/11/12/13/14/16.
- Dependencias: T-05/T-06; DT-03.
- Verificación y condición de cierre: Con F-02/F-03/F-06 y ES-F04-03 reales comprobar reserva anterior pendiente, otra reserva al asignar y evento único. Caída de Ventas conserva decisión; registrar entrega real aparte de los dobles.
- Evidencia: [EV-04](./evidence.md#ev-04-recorrido-real-de-reprogramación); resultados, artefactos, commits y límites registrados el 24/10/2026.
- Límites y bloqueos: Una dependencia no implementada mantiene pendiente su integración; no se acredita con un mock.

### T-08. Cobertura y revisión de aceptación

- [ ] Integración y aceptación final pendientes; implementación local comprobada.

- Incremento/responsable: I-06; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Revisar todas las filas de cobertura y completar evidencia con código, comandos, resultados y revisión humana. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01 a CA-18; CUI-01 a CUI-08.
- Dependencias: T-01 a T-07.
- Verificación y condición de cierre: Contrastar CA/CUI contra reportes reales, commits y límites; cerrar solo con integración y criterios acreditados.
- Evidencia: [EV-01](./evidence.md#ev-01-persistencia-fecha-y-seguridad), [EV-02](./evidence.md#ev-02-concurrencia-y-recuperación-durable), [EV-03](./evidence.md#ev-03-modal-contrato-y-accesibilidad), [EV-04](./evidence.md#ev-04-recorrido-real-de-reprogramación); resultados, artefactos, commits y límites registrados el 24/10/2026.
- Límites y bloqueos: La preparación documental no completa esta tarea.

## 3. Cobertura de criterios

| Criterio | Tareas que implementan | Comprobación y cierre | Evidencia prevista |
|---|---|---|---|
| CA-01 | T-03/04/06/07 | T-03/04/06/07; revisión T-08 | EV-01/03/04 |
| CA-02 | T-02/04/06 | T-02/04/06; revisión T-08 | EV-01/03 |
| CA-03 | T-02/04/06 | T-02/04/06; revisión T-08 | EV-01/03 |
| CA-04 | T-04/05/06 | T-04/05/06; revisión T-08 | EV-01/02/03 |
| CA-05 | T-04/06 | T-04/06; revisión T-08 | EV-01/03 |
| CA-06 | T-04/07 | T-04/07; revisión T-08 | EV-01/04 |
| CA-07 | T-04/05/06 | T-04/05/06; revisión T-08 | EV-01/02/03 |
| CA-08 | T-03/05/06 | T-03/05/06; revisión T-08 | EV-02/03 |
| CA-09 | T-02/04/06 | T-02/04/06; revisión T-08 | EV-01/03 |
| CA-10 | T-05 | T-05; revisión T-08 | EV-02 |
| CA-11 | T-05/07 | T-05/07; revisión T-08 | EV-02/04 |
| CA-12 | T-06/07 | T-06/07; revisión T-08 | EV-03/04 |
| CA-13 | T-03/04/07 | T-03/04/07; revisión T-08 | EV-01/04 |
| CA-14 | T-04/05/07 | T-04/05/07; revisión T-08 | EV-01/02/04 |
| CA-15 | T-04/06 | T-04/06; revisión T-08 | EV-01/03 |
| CA-16 | T-04/07 | T-04/07; revisión T-08 | EV-01/04 |
| CA-17 | T-02/06 | T-02/06; revisión T-08 | EV-03 |
| CA-18 | T-04 | T-04; revisión T-08 | EV-01 |
| CUI-01 | T-01/T-02/T-06 | T-06; revisión T-08 | EV-03 |
| CUI-02 | T-01/T-02/T-06 | T-06; revisión T-08 | EV-03 |
| CUI-03 | T-01/T-02/T-06 | T-06; revisión T-08 | EV-03 |
| CUI-04 | T-01/T-02/T-06 | T-06; revisión T-08 | EV-03 |
| CUI-05 | T-01/T-02/T-06 | T-06; revisión T-08 | EV-03 |
| CUI-06 | T-01/T-02/T-06 | T-06; revisión T-08 | EV-03 |
| CUI-07 | T-01/T-02/T-06 | T-06; revisión T-08 | EV-03 |
| CUI-08 | T-01/T-02/T-06 | T-06; revisión T-08 | EV-03 |

Cada CUI de [ui.md](./ui.md) tiene una fila propia; los controles se comprueban antes del modal. La cobertura prevista no equivale a una prueba ejecutada.

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están completadas y verificadas.
- [ ] Cada criterio tiene evidencia; fallos, límites y simulaciones se identifican.
- [ ] Las integraciones reales requeridas están comprobadas.
- [x] Documentos e índice coinciden con el código y los resultados locales, incluyendo pendientes.
- [ ] Commits/PR de implementación y revisión humana están enlazados.

## 5. Referencias

- [cite: 1] [Especificación](./spec.md) y [UI](./ui.md): criterios y límites.
- [cite: 2] [Plan](./plan.md): incrementos, dependencias y comandos previstos.
- [cite: 3] [Evidencia](./evidence.md): resultados reales y separación de mocks/servicios.
