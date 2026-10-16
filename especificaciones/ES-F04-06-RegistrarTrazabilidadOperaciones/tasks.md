# Tareas de ES-F04-06: Registrar la trazabilidad de las operaciones

**Responsable de coordinación:** Gerardo.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparación SDD del 16/10/2026 sobre revisión funcional `c8e6e29`.

## 1. Orden y dependencias

| ID | Resultado verificable | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Base de pruebas y límites transaccionales definidos. | Backend/calidad | RT-02; base del servicio Gestión | CA-01/02/03/04/07/09 | Pendiente |
| T-02 | Persistencia común y migraciones coordinadas. | Datos | T-01; DT-01 | CA-01/02/03/05/06/09/11/12 | Pendiente |
| T-03 | Escritor de historial en la transacción de origen. | Backend Gestión | T-02 | CA-01/02/03/04/05/07/09/12 | Pendiente |
| T-04 | Productores de recepción y decisiones integrados. | Backend/integración | T-03; comandos ES-F04-03/04/05 disponibles | CA-01/02/03/04/05/09/12 | Pendiente |
| T-05 | Rollback, identidad y concurrencia comprobados. | Backend/calidad | T-04; protecciones de origen | CA-04/05/07/08/09 | Pendiente |
| T-06 | Consulta pública e inmutabilidad verificadas. | Backend/seguridad | T-03/T-04; ES-F04-02 consulta disponible | CA-06/09/11 | Pendiente |
| T-07 | Procesos técnicos sin doble auditoría. | Integración | T-04; ES-F04-03 T-07 y RT-03 disponibles | CA-05/10/12 | Pendiente |
| T-08 | Cobertura y revisión cerradas. | Calidad | T-01 a T-07 | CA-01 a CA-12 | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar causa y responsable de cada bloqueo. Las tareas de componentes o servicios compartidos se verifican antes de consumirlos; esta carpeta no los da por completados.

## 2. Detalle de tareas

### T-01. Base de pruebas y límites transaccionales definidos

- [ ] Implementada y verificada.

- Incremento/responsable: I-01; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Revisar repositorio y preparar fixtures sintéticos, reloj/contexto autenticado y pruebas PostgreSQL/Testcontainers reutilizables. Usar [spec.md](./spec.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/02/03/04/07/09.
- Dependencias: RT-02; base del servicio Gestión.
- Verificación y condición de cierre: Ejecutar `./mvnw.cmd test` en Gestión y demostrar que los tests de transacción usan base real; registrar configuración sin secretos.
- Evidencia: [EV-01](./evidence.md#ev-01-captura-y-transacciones-de-los-productores); pendiente de resultado, artefacto y commit/PR reales.
- Límites y bloqueos: No ejecutar pruebas contra datos productivos ni asumir resultados por generar esta carpeta.

### T-02. Persistencia común y migraciones coordinadas

- [ ] Implementada y verificada.

- Incremento/responsable: I-02; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Reutilizar/completar historial RT-02 y sus referencias; coordinar índices/metadatos específicos con ES-F04-04/05, sin tablas o migraciones duplicadas. Usar [spec.md](./spec.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/02/03/05/06/09/11/12.
- Dependencias: T-01; DT-01.
- Verificación y condición de cierre: Aplicar en base vacía y sintética previa; comprobar tipos, relación con incidencia e integridad de entradas históricas.
- Evidencia: [EV-01](./evidence.md#ev-01-captura-y-transacciones-de-los-productores); pendiente de resultado, artefacto y commit/PR reales.
- Límites y bloqueos: Arquitectura/F-02 conservan propiedad de su trabajo; no reconstruir resultados ausentes por conjetura.

### T-03. Escritor de historial en la transacción de origen

- [ ] Implementada y verificada.

- Incremento/responsable: I-02; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Implementar la captura común con transacción activa; autoría del contexto, instante UTC, estados y datos propios, sin escritura independiente. Usar [spec.md](./spec.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/02/03/04/05/07/09/12.
- Dependencias: T-02.
- Verificación y condición de cierre: Invocar desde un comando de prueba y forzar rollback después de capturar: no queda fila; aceptar una operación conserva una sola entrada.
- Evidencia: [EV-01](./evidence.md#ev-01-captura-y-transacciones-de-los-productores); pendiente de resultado, artefacto y commit/PR reales.
- Límites y bloqueos: Este incremento habilita productores; no depende de T-04 a T-08 de esta misma carpeta.

### T-04. Productores de recepción y decisiones integrados

- [ ] Implementada y verificada.

- Incremento/responsable: I-03; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Integrar las tres operaciones al mismo escritor sin segunda captura; distinguir simulado y motivo de cierre frente a fallo. Usar [spec.md](./spec.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01/02/03/04/05/09/12.
- Dependencias: T-03; comandos ES-F04-03/04/05 disponibles.
- Verificación y condición de cierre: Ejecutar los comandos con base real; una fila por aceptación, recepción FALLIDO/FALLIDO y decisiones con su transición, sin eventos por recibir/simular.
- Evidencia: [EV-01](./evidence.md#ev-01-captura-y-transacciones-de-los-productores); pendiente de resultado, artefacto y commit/PR reales.
- Límites y bloqueos: ES-F04-04/05 T-04 consumen T-03, y luego esta tarea los verifica: sin dependencia circular.

### T-05. Rollback, identidad y concurrencia comprobados

- [ ] Implementada y verificada.

- Incremento/responsable: I-04; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Cubrir pérdida de respuesta, replay, contenido/actor incompatibles, mutación ganadora y fallo en cada escritura del conjunto. Usar [spec.md](./spec.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-04/05/07/08/09.
- Dependencias: T-04; protecciones de origen.
- Verificación y condición de cierre: Dos transacciones reales y fallos controlados; solo el ganador deja la nueva entrada y una reversión no conserva decisión/historial parciales.
- Evidencia: [EV-02](./evidence.md#ev-02-rechazos-rollback-y-concurrencia); pendiente de resultado, artefacto y commit/PR reales.
- Límites y bloqueos: No sustituir el control de versión de los comandos por otra política de esta sexta.

### T-06. Consulta pública e inmutabilidad verificadas

- [ ] Implementada y verificada.

- Incremento/responsable: I-05; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Verificar proyección explícita, orden estable, varios ciclos y consulta histórica; excluir controles internos y aplicar autorización existente. Usar [spec.md](./spec.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-06/09/11.
- Dependencias: T-03/T-04; ES-F04-02 consulta disponible.
- Verificación y condición de cierre: Consultar con JWT válido, inválido y sin rol; comparar JSON público y persistencia, marcas iguales con desempate y ausencia de mutaciones.
- Evidencia: [EV-03](./evidence.md#ev-03-historial-público-y-autorización); pendiente de resultado, artefacto y commit/PR reales.
- Límites y bloqueos: No crea otro endpoint ni UI; el consumidor visual sigue siendo ES-F04-02.

### T-07. Procesos técnicos sin doble auditoría

- [ ] Implementada y verificada.

- Incremento/responsable: I-06; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Comprobar liberación/envío con reinicios, respuesta perdida y reenvío manual del mismo evento, sin modificar historial original. Usar [spec.md](./spec.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-05/10/12.
- Dependencias: T-04; ES-F04-03 T-07 y RT-03 disponibles.
- Verificación y condición de cierre: Con procesadores reales contrastar conteos, contenido y fechas antes/después; dobles aislados se identifican y no cierran la integración real.
- Evidencia: [EV-04](./evidence.md#ev-04-reintentos-técnicos-y-simulados); pendiente de resultado, artefacto y commit/PR reales.
- Límites y bloqueos: La ausencia de un procesador mantiene pendiente esta comprobación, sin inventar resultado.

### T-08. Cobertura y revisión cerradas

- [ ] Implementada y verificada.

- Incremento/responsable: I-06; Gerardo coordina con los responsables de dependencias sin reasignarlos.
- Alcance y entradas: Revisar resultados de productores/consumidor, documentación y evidencia de todas las garantías comunes. Usar [spec.md](./spec.md), el contrato y las decisiones del [plan](./plan.md). Criterios: CA-01 a CA-12.
- Dependencias: T-01 a T-07.
- Verificación y condición de cierre: Cada criterio tiene reporte, commit y entorno reales; revisar que ningún metadato sensible quede expuesto y que no haya otra auditoría.
- Evidencia: [EV-01](./evidence.md#ev-01-captura-y-transacciones-de-los-productores), [EV-02](./evidence.md#ev-02-rechazos-rollback-y-concurrencia), [EV-03](./evidence.md#ev-03-historial-público-y-autorización), [EV-04](./evidence.md#ev-04-reintentos-técnicos-y-simulados); pendiente de resultado, artefacto y commit/PR reales.
- Límites y bloqueos: La captura no se considera verificada solo por estar descrita en las tres operaciones.

## 3. Cobertura de criterios

| Criterio | Tareas que implementan | Comprobación y cierre | Evidencia prevista |
|---|---|---|---|
| CA-01 | T-02/03/04 | T-02/03/04; revisión T-08 | EV-01 |
| CA-02 | T-02/03/04 | T-02/03/04; revisión T-08 | EV-01 |
| CA-03 | T-02/03/04 | T-02/03/04; revisión T-08 | EV-01 |
| CA-04 | T-03/04/05 | T-03/04/05; revisión T-08 | EV-01/02 |
| CA-05 | T-02/03/04/05/07 | T-02/03/04/05/07; revisión T-08 | EV-01/02/04 |
| CA-06 | T-02/06 | T-02/06; revisión T-08 | EV-03 |
| CA-07 | T-01/03/05 | T-01/03/05; revisión T-08 | EV-01/02 |
| CA-08 | T-05 | T-05; revisión T-08 | EV-02 |
| CA-09 | T-01/02/03/04/05/06 | T-01/02/03/04/05/06; revisión T-08 | EV-01/02/03 |
| CA-10 | T-07 | T-07; revisión T-08 | EV-04 |
| CA-11 | T-02/06 | T-02/06; revisión T-08 | EV-03 |
| CA-12 | T-02/03/04/07 | T-02/03/04/07; revisión T-08 | EV-01/04 |

No hay criterios de UI propios: ES-F04-02 mantiene la presentación y T-06 verifica que la consulta cumple el contrato. La cobertura prevista no equivale a una prueba ejecutada.

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están completadas y verificadas.
- [ ] Cada criterio tiene evidencia; fallos, límites y simulaciones se identifican.
- [ ] Las integraciones reales requeridas están comprobadas.
- [ ] Documentos e índice coinciden con el código y los resultados.
- [ ] Commits/PR de implementación y revisión humana están enlazados.

## 5. Referencias

- [cite: 1] [Especificación](./spec.md): criterios y límites.
- [cite: 2] [Plan](./plan.md): incrementos, dependencias y comandos previstos.
- [cite: 3] [Evidencia](./evidence.md): resultados reales y separación de mocks/servicios.
