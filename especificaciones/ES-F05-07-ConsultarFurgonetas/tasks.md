# Tareas de ES-F05-07: Consultar furgonetas

**Responsable:** Rhamses.

**Estado:** Pendiente de verificación por criterio; existe código de referencia, pero esta migración no certifica su aceptación.

**Plan de origen:** [plan.md](./plan.md), preparado con la fuente documental `f3849d9`.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Conciliar fuentes y verificar dependencias compartidas | Contrato y preparación | Fuentes del plan; responsables de contrato y CR | CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06 | Pendiente |
| T-02 | Verificar y ajustar el comportamiento backend | Backend y datos | T-01 y PostgreSQL de prueba | CA-01, CA-02, CA-03, CA-04, CA-05 | Pendiente |
| T-03 | Verificar la interacción y los componentes frontend | Frontend y UI | T-01; contrato revisado o simulación identificada | CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06 | Pendiente |
| T-04 | Comprobar el recorrido integrado y registrar la aceptación | Integración y calidad | T-02, T-03 y dependencias reales | CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06 | Pendiente |

Los estados son Pendiente, En curso, Bloqueada y Completada. Una tarea de comprobación de código existente sigue pendiente hasta tener un resultado enlazado por criterio; no significa que ese código no exista. Los cambios de CR compartidos se coordinan con sus responsables [cite: 1, 2].

## 2. Detalle de tareas

### T-01. Conciliar fuentes y verificar dependencias compartidas

- [ ] Implementada o contrastada, y verificada.
- Incremento del plan: I-01.
- Responsable: Rhamses en coordinación con Arquitectura y los responsables de CR.
- Objetivo y alcance: Revisar los acuerdos que afectan este comportamiento y comprobar la disponibilidad de los CR antes de aceptar su pantalla.
- Entradas: [spec.md](./spec.md), criterios CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06; [ui.md](./ui.md) cuando corresponda; fuentes del plan §1.
- Dependencias: Fuentes del plan; responsables de contrato y CR.
- Verificación: Contrastar P-01 y DT-01/02 contra el contrato y el modelo; registrar resolución o bloqueo, versión de componentes y responsable.
- Condición de cierre: Revisión registrada y ninguna discrepancia funcional sin tratar para el incremento que se acepte.
- Evidencia: [EV-03](./evidence.md#ev-03-aceptación-por-criterio-pendiente), pendiente; [EV-02](./evidence.md#ev-02-código-y-pruebas-existentes-como-referencia) solo identifica código de referencia.
- Bloqueo potencial: DT-01/02; Rhamses coordina su resolución y registra qué criterios afecta.

### T-02. Verificar y ajustar el comportamiento backend

- [ ] Implementada o contrastada, y verificada.
- Incremento del plan: I-02.
- Responsable: Rhamses.
- Objetivo y alcance: Lectura repetible, orden determinista y filtros parametrizados; no consultar ocupación ni modificar jornadas.
- Entradas: [spec.md](./spec.md), criterios CA-01, CA-02, CA-03, CA-04, CA-05; [ui.md](./ui.md) cuando corresponda; fuentes del plan §1.
- Dependencias: T-01 y PostgreSQL de prueba.
- Verificación: Ejecutar y revisar los casos de la matriz del plan, incluidos permisos y alternativas; identificar los criterios no cubiertos por las pruebas existentes.
- Condición de cierre: Resultado individual por criterio con commit, datos y dependencia identificada; aplicar ajustes de código en el repositorio backend cuando proceda.
- Evidencia: [EV-03](./evidence.md#ev-03-aceptación-por-criterio-pendiente), pendiente; [EV-02](./evidence.md#ev-02-código-y-pruebas-existentes-como-referencia) solo identifica código de referencia.
- Bloqueo potencial: DTO o regla sin conciliar; resolver el acuerdo antes de ajustar el caso afectado.

### T-03. Verificar la interacción y los componentes frontend

- [ ] Implementada o contrastada, y verificada.
- Incremento del plan: I-02.
- Responsable: Rhamses.
- Objetivo y alcance: Combinar estado y búsqueda, limpiar filtros y cambiar de página; conservar separados vacío, error y resultados anteriores sin confirmar.
- Entradas: [spec.md](./spec.md), criterios CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06; [ui.md](./ui.md) cuando corresponda; fuentes del plan §1.
- Dependencias: T-01; contrato revisado o simulación identificada.
- Verificación: Ejecutar pruebas de F-05 y recorrer los CUI de ui.md con teclado y pantalla reducida; diferenciar fixtures de integración real.
- Condición de cierre: Casos CUI con resultado observable, artefacto y revisión visual registrada.
- Evidencia: [EV-03](./evidence.md#ev-03-aceptación-por-criterio-pendiente), pendiente; [EV-02](./evidence.md#ev-02-código-y-pruebas-existentes-como-referencia) solo identifica código de referencia.
- Bloqueo potencial: contrato, componentes o revisión visual pendientes; identificar fixtures y diferencias.

### T-04. Comprobar el recorrido integrado y registrar la aceptación

- [ ] Implementada o contrastada, y verificada.
- Incremento del plan: I-03.
- Responsable: Rhamses con Calidad y los propietarios de dependencias.
- Objetivo y alcance: Comprobar el recorrido con frontend, Gateway, Operación y las dependencias necesarias; conservar evidencia trazable y revisión del equipo.
- Entradas: [spec.md](./spec.md), criterios CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06; [ui.md](./ui.md) cuando corresponda; fuentes del plan §1.
- Dependencias: T-02, T-03 y dependencias reales.
- Verificación: Repetir los criterios en el entorno identificado y revisar sus efectos persistidos; no inferir una aceptación a partir del total de una suite.
- Condición de cierre: Todos los criterios del alcance resueltos, registros EV completos y pendientes externos visibles con responsable.
- Evidencia: [EV-03](./evidence.md#ev-03-aceptación-por-criterio-pendiente), pendiente; [EV-02](./evidence.md#ev-02-código-y-pruebas-existentes-como-referencia) solo identifica código de referencia.
- Bloqueo potencial: DT-01 a DT-04; la disponibilidad de un despliegue no acredita cuentas reales ni acuerdos funcionales.

## 3. Cobertura de criterios

| Criterio | Tareas que lo implementan o contrastan | Comprobación que lo verifica | Evidencia funcional |
|---|---|---|---|
| CA-01 | T-01, T-02, T-03 | T-04; Sembrar furgonetas y revisar filas, capacidades y totales. | Pendiente; EV-03 |
| CA-02 | T-01, T-02, T-03 | T-04; Filtrar por DISPONIBLE y comprobar todas las filas devueltas. | Pendiente; EV-03 |
| CA-03 | T-01, T-02, T-03 | T-04; Buscar ABC y comprobar coincidencias de placa. | Pendiente; EV-03 |
| CA-04 | T-01, T-02, T-03 | T-04; Consultar sin coincidencias y verificar el estado vacío. | Pendiente; EV-03 |
| CA-05 | T-01, T-02, T-03 | T-04; Consultar con otro rol y comprobar rechazo. | Pendiente; EV-03 |
| CUI-01 | T-01, T-03 | T-04; escenario de ui.md §7 | Pendiente; EV-03 |
| CUI-02 | T-01, T-03 | T-04; escenario de ui.md §7 | Pendiente; EV-03 |
| CUI-03 | T-01, T-03 | T-04; escenario de ui.md §7 | Pendiente; EV-03 |
| CUI-04 | T-01, T-03 | T-04; escenario de ui.md §7 | Pendiente; EV-03 |
| CUI-05 | T-01, T-03 | T-04; escenario de ui.md §7 | Pendiente; EV-03 |
| CUI-06 | T-01, T-03 | T-04; escenario de ui.md §7 | Pendiente; EV-03 |

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están verificadas.
- [ ] Los CA y CUI tienen evidencia individual y las diferencias están resueltas.
- [ ] Los dobles, fixtures y servicios reales se identifican expresamente.
- [ ] Los enlaces y el índice de esta migración están verificados en EV-01.
- [ ] Los commits, la revisión humana y la aceptación están registrados.

## 5. Referencias

1. [Especificación funcional](./spec.md) y [UI](./ui.md) [cite: 1].
2. [Plan](./plan.md), incrementos y dependencias [cite: 2].
3. [Evidencia](./evidence.md), resultados y límites [cite: 3].
