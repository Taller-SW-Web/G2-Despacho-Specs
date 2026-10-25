# Tareas de ES-F04-05: Cerrar un despacho como devuelto a origen

**Responsable de coordinación:** Gerardo.

**Estado:** T-01 a T-06 completadas localmente; T-07/T-08 en curso por integración conjunta y revisión humana.

**Plan de origen:** [plan.md](./plan.md), preparación SDD del 16/10/2026 sobre revisión funcional `c8e6e29`.

## 1. Orden y dependencias

| ID | Resultado verificable | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Controles y herramientas comprobados. | Frontend/calidad | DT-01; base compartida | CA-06/07/14; CUI-01 a CUI-08 | Completada |
| T-02 | Modal de cierre con fixtures. | Frontend | T-01 | CA-04/05/06/08/09/14; CUI-01 a CUI-08 | Completada |
| T-03 | Historial y unicidad de cierre preparados. | Datos | RT-02 base; DT-02 | CA-01/02/10/12/13/15 | Completada |
| T-04 | Cierre autorizado y atómico. | Backend Gestión | T-03; ES-F04-06 T-03 | CA-01/03/04/05/06/07/08/11/12/13/15 | Completada |
| T-05 | Cierre único y recuperación exacta. | Backend/calidad | T-04 | CA-02/09/10/12 | Completada |
| T-06 | Modal conectado y retorno conservado. | Frontend/integración | T-02/T-04/T-05; ES-F04-01/02 | CA-01/02/04/05/06/07/09/14/15; CUI-01 a CUI-08 | Completada |
| T-07 | Cierre integrado con recepción y RT-03. | Integración | T-05/T-06; DT-03 | CA-01/03/05/08/10/11/13/15 | En curso |
| T-08 | Aceptar cobertura y revisión. | Calidad | T-01 a T-07 | CA-01 a CA-15; CUI-01 a CUI-08 | En curso |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar causa y responsable de cada bloqueo. Las tareas de componentes o servicios compartidos se verifican antes de consumirlos; esta carpeta no los da por completados.

## 2. Detalle de tareas

### T-01. Controles y herramientas comprobados

- [x] Implementada y verificada en el entorno local descrito en evidencia.

- Incremento/responsable: I-01; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Verificar tema/proveedores y CR-01/02/08/09/15; reutilizar pruebas y controles preparados para ES-F04-03/04. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-06/07/14; CUI-01 a CUI-08.
- Dependencias: DT-01; base compartida.
- Verificación y condición de cierre: Ejecutar `npm run typecheck`, `npm run build` y el comando de interacción incorporado; verificar mensajes y activación antes del modal.
- Evidencia: [EV-03](./evidence.md#ev-03-modal-recuperación-y-accesibilidad); resultados, pruebas y commits en los registros EV de evidencia; PR y revisión humana pendientes.
- Límites y bloqueos: No crear otro proveedor ni reinicializar la aplicación.

### T-02. Modal de cierre con fixtures

- [x] Implementada y verificada en el entorno local descrito en evidencia.

- Incremento/responsable: I-02; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Implementar UI-01 con motivo de texto, observación, advertencia final, carga, conflictos y recuperación. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-04/05/06/08/09/14; CUI-01 a CUI-08.
- Dependencias: T-01.
- Verificación y condición de cierre: Probar 500/501 puntos de código, doble confirmación, pérdida de respuesta, cierre por distintos motivos y foco/móvil con datos simulados identificados.
- Evidencia: [EV-03](./evidence.md#ev-03-modal-recuperación-y-accesibilidad); resultados, pruebas y commits en los registros EV de evidencia; PR y revisión humana pendientes.
- Límites y bloqueos: No atribuir aceptación real de Ventas a un fixture.

### T-03. Historial y unicidad de cierre preparados

- [x] Implementada y verificada en el entorno local descrito en evidencia.

- Incremento/responsable: I-03; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Reutilizar historial; migrar índice único parcial y compatibilidad de `controlCierre` conforme al modelo, sin otra tabla. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/02/10/12/13/15.
- Dependencias: RT-02 base; DT-02.
- Verificación y condición de cierre: Aplicar en PostgreSQL vacío y base sintética previa; recuperar el cuerpo original inmutable y excluir históricos incoherentes hasta regularizarlos con información real.
- Evidencia: [EV-01](./evidence.md#ev-01-cierre-datos-y-seguridad), [EV-02](./evidence.md#ev-02-concurrencia-y-resultado-original); resultados, pruebas y commits en los registros EV de evidencia; PR y revisión humana pendientes.
- Límites y bloqueos: Coordinar base con ES-F04-06 T-02/T-03; no inventar respuestas para datos previos.

### T-04. Cierre autorizado y atómico

- [x] Implementada y verificada en el entorno local descrito en evidencia.

- Incremento/responsable: I-03; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Implementar Gestión §5.2.3: motivo/observación, contexto, transacción final con historial/resultado/evento real y conservación de recepción. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/03/04/05/06/07/08/11/12/13/15.
- Dependencias: T-03; ES-F04-06 T-03.
- Verificación y condición de cierre: Desde Gestión ejecutar `./mvnw.cmd test` con PostgreSQL; respuestas contractuales, motivo separado del fallo y rollback por cada escritura; simulado sin evento.
- Evidencia: [EV-01](./evidence.md#ev-01-cierre-datos-y-seguridad); resultados, pruebas y commits en los registros EV de evidencia; PR y revisión humana pendientes.
- Límites y bloqueos: No llamar a Operación/Ventas dentro de la transacción.

### T-05. Cierre único y recuperación exacta

- [x] Implementada y verificada en el entorno local descrito en evidencia.

- Incremento/responsable: I-04; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Resolver replay, contenido/ejecutor incompatible y competencia con reprogramación/anulación usando la versión y el resultado durable. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-02/09/10/12.
- Dependencias: T-04.
- Verificación y condición de cierre: Dos transacciones reales, reinicio y reenvío después de 24 horas/cambio de estado de envío: un cierre y un historial, cuerpo idéntico al original.
- Evidencia: [EV-02](./evidence.md#ev-02-concurrencia-y-resultado-original); resultados, pruebas y commits en los registros EV de evidencia; PR y revisión humana pendientes.
- Límites y bloqueos: Una nueva identidad no permite editar un estado final.

### T-06. Modal conectado y retorno conservado

- [x] Implementada y verificada en el entorno local descrito en evidencia.

- Incremento/responsable: I-05; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Conectar cliente/tipos y contexto vigente al Gateway, recuperar el comando original y actualizar listado/detalle/indicadores. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/02/04/05/06/07/09/14/15; CUI-01 a CUI-08.
- Dependencias: T-02/T-04/T-05; ES-F04-01/02.
- Verificación y condición de cierre: Interacción y HTTP real: 200, 400, 409, 500, 503, pérdida de respuesta y refresco fallido; filtros/foco y datos protegidos correctos.
- Evidencia: [EV-03](./evidence.md#ev-03-modal-recuperación-y-accesibilidad); resultados, pruebas y commits en los registros EV de evidencia; PR y revisión humana pendientes.
- Límites y bloqueos: El detalle conserva la consulta histórica y el estado actual del envío.

### T-07. Cierre integrado con recepción y RT-03

- [ ] Implementada y verificada.

- Incremento/responsable: I-06; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Verificar cierre con reserva pendiente, anulado, NO_INTENTADO, límite e intentos disponibles; evento acordado y ninguna vuelta a cola. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/03/05/08/10/11/13/15.
- Dependencias: T-05/T-06; DT-03.
- Verificación y condición de cierre: Con servicios reales mantener liberación pendiente tras cerrar y luego confirmarla; comparar historial, reserva y evento único. Distinguir emisor con doble de entrega contra receptor real de Ventas.
- Evidencia: [EV-04](./evidence.md#ev-04-cierre-logístico-e-integraciones-reales); resultados, pruebas y commits en los registros EV de evidencia; PR y revisión humana pendientes.
- Límites y bloqueos: Se mantiene el acuerdo externo; no se acreditan cambios comerciales no observados.

### T-08. Aceptar cobertura y revisión

- [ ] Implementada y verificada.

- Incremento/responsable: I-06; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Completar la evidencia y revisar coherencia de código, contratos y documentos. Usar [spec.md](./spec.md), [ui.md](./ui.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01 a CA-15; CUI-01 a CUI-08.
- Dependencias: T-01 a T-07.
- Verificación y condición de cierre: Comprobar cada fila CA/CUI, reportes, commits, servicios reales/dobles y revisión humana; cierre solo con resultados reales.
- Evidencia: [EV-01](./evidence.md#ev-01-cierre-datos-y-seguridad), [EV-02](./evidence.md#ev-02-concurrencia-y-resultado-original), [EV-03](./evidence.md#ev-03-modal-recuperación-y-accesibilidad), [EV-04](./evidence.md#ev-04-cierre-logístico-e-integraciones-reales); resultados, pruebas y commits en los registros EV de evidencia; PR y revisión humana pendientes.
- Límites y bloqueos: La implementación y las comprobaciones locales están registradas; falta completar integración conjunta y revisión humana.

## 3. Cobertura de criterios

| Criterio | Tareas que implementan | Comprobación y cierre | Evidencia prevista |
|---|---|---|---|
| CA-01 | T-03/04/06/07 | T-03/04/06/07; revisión T-08 | EV-01/03/04 |
| CA-02 | T-03/05/06 | T-03/05/06; revisión T-08 | EV-02/03 |
| CA-03 | T-04/07 | T-04/07; revisión T-08 | EV-01/04 |
| CA-04 | T-02/04/06 | T-02/04/06; revisión T-08 | EV-01/03 |
| CA-05 | T-02/04/06/07 | T-02/04/06/07; revisión T-08 | EV-01/03/04 |
| CA-06 | T-02/04/06 | T-02/04/06; revisión T-08 | EV-01/03 |
| CA-07 | T-04/06 | T-04/06; revisión T-08 | EV-01/03 |
| CA-08 | T-02/04/07 | T-02/04/07; revisión T-08 | EV-01/03/04 |
| CA-09 | T-05/06 | T-05/06; revisión T-08 | EV-02/03 |
| CA-10 | T-03/05/07 | T-03/05/07; revisión T-08 | EV-02/04 |
| CA-11 | T-04/07 | T-04/07; revisión T-08 | EV-01/04 |
| CA-12 | T-03/04/05 | T-03/04/05; revisión T-08 | EV-01/02 |
| CA-13 | T-03/04/07 | T-03/04/07; revisión T-08 | EV-01/04 |
| CA-14 | T-02/06 | T-02/06; revisión T-08 | EV-03 |
| CA-15 | T-04/06/07 | T-04/06/07; revisión T-08 | EV-01/03/04 |
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

Implementación de T-07 verificada con Gestión/PostgreSQL reales, entrega HTTP de eventos hacia un receptor controlado y liberación con puerto doble. El navegador usa proxy de pruebas. Falta la integración conjunta con los servicios desplegados y la aceptación humana de T-08; no se declara aprobación de Ventas.

- [ ] Todas las tareas del alcance están completadas y verificadas.
- [ ] Cada criterio tiene evidencia; fallos, límites y simulaciones se identifican.
- [ ] Las integraciones reales requeridas están comprobadas.
- [x] Documentos e índice coinciden con el código y los resultados.
- [ ] Commits/PR de implementación y revisión humana están enlazados.

## 5. Referencias

- [cite: 1] [Especificación](./spec.md) y [UI](./ui.md): criterios y límites.
- [cite: 2] [Plan](./plan.md): incrementos, dependencias y comandos de verificación.
- [cite: 3] [Evidencia](./evidence.md): resultados reales y separación de mocks/servicios.
