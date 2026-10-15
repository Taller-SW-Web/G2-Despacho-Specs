# Tareas de ES-F04-01: Consultar entregas fallidas

**Responsable de coordinación:** Gerardo.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), misma revisión documental que esta carpeta.

Esta entrega prepara las tareas; no ejecuta cambios de contrato, componentes ni código. Los responsables de componentes son los del [reparto compartido](../../disenio/componentes-react.md), §4.5; esta lista no crea issues ni acredita su aceptación.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Base frontend y herramientas de pruebas verificadas. | Preparación compartida | DT-04; coordinación con Max/Rhamses. | CUI-01 a CUI-06 como soporte. | Pendiente |
| T-02 | CR-08 EstadoVista implementado y verificado. | Componente compartido | T-01 y patrones CR-01 necesarios. | CCR-08-01; soporte de CA-03/04 y CUI-03/04. | Pendiente |
| T-03 | Resto de componentes del listado disponibles y verificados. | Componentes compartidos | T-01 y dependencias de cada CR; CR-07 depende de T-02. | CUI-01/02/05/06. | Pendiente |
| T-04 | Página de consulta verificable con fixtures de presentación. | Frontend, I-01 | T-02 y T-03. | CUI-01 a CUI-06, sin acreditar backend real. | Pendiente |
| T-05 | Contrato del listado concretado en su documento central. | Contrato | Revisión posterior DT-01. | CA-01 a CA-05; controles de CUI-02. | Pendiente |
| T-06 | Persistencia y fuentes operativas de la consulta preparadas. | Datos e integración | T-05 y decisiones DT-02/03. | CA-01/02/05. | Pendiente |
| T-07 | Endpoint de consulta autorizado y probado. | Backend, I-02 | T-05, T-06 y base JWT/errores/rutas de DT-03. | CA-01 a CA-05. | Pendiente |
| T-08 | Página conectada a la consulta real. | Integración, I-03 | T-04, T-07 y Gateway accesible. | CA-01 a CA-05; CUI-01 a CUI-06. | Pendiente |
| T-09 | Cobertura, evidencia y revisión del alcance completadas. | Calidad | T-08 y dependencias reales disponibles. | Todos los criterios del alcance. | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Al iniciar una tarea cuya dependencia no esté disponible, registrar el bloqueo y su responsable. T-05 puede prepararse en paralelo con I-01; su ejecución queda para la revisión del contrato acordada con Gerardo.

## 2. Detalle de tareas

### T-01. Verificar la base compartida del frontend

- [ ] Implementada y verificada.

- Alcance: revisar tema, tokens, proveedores, dependencias y scripts existentes; coordinar herramientas de pruebas sin reinicializar el monorepositorio.
- Entradas: componentes React §4.5.1 y DT-04 del plan.
- Responsable: coordinación de Gerardo con Max y Rhamses según el reparto existente.
- Comprobación: ambas apps pasan `npm run typecheck` y `npm run build`; una prueba de interacción puede ejecutarse con el comando que se configure y documente.
- Cierre y evidencia: registrar herramientas, comandos y resultados reales; no acreditar componentes por la compilación de la base.

### T-02. Implementar CR-08 EstadoVista

- [ ] Implementada y verificada.

- Alcance: componentes de vacío, sin resultados, error, falta de permiso y carga según el contrato de CR-08; añadir sus exportaciones manteniendo `tema`.
- Ubicación: `packages/componentes-compartidos/src/feedback/` del frontend.
- Responsable: Gerardo; revisión propuesta de Max.
- Comprobación: CCR-08-01, acciones de recuperación con teclado, carga diferenciada de vacío y ausencia de datos protegidos. Usar fixtures identificados.
- Cierre y evidencia: enlazar commit/pruebas compartidas desde EV-02; no realizar llamadas HTTP dentro del componente.

### T-03. Coordinar y verificar los otros componentes requeridos

- [ ] Implementada y verificada.

- Alcance: confirmar CR-01/02/03/05/06/07/09/10 y sus dependencias, exportaciones y evidencia; enlazar los trabajos de sus responsables sin duplicar componentes.
- Responsable: Gerardo coordina con Valqui, Rhamses, Tarqui y Luis según §4.5 del documento compartido.
- Comprobación: los componentes se consumen desde el paquete compartido y sus criterios aplicables cuentan con pruebas; ambas aplicaciones siguen compilando.
- Cierre y evidencia: registrar componentes/revisiones disponibles y pendientes. CR-12/15/18/19 se reservan para sus flujos consumidores.

### T-04. Componer la página con fixtures

- [ ] Implementada y verificada.

- Alcance: crear la página en la funcionalidad de entregas fallidas; tabla, controles, indicadores, paginación y estados definidos en UI-01.
- Entradas: [ui.md](./ui.md), componentes verificados y fixtures de presentación que distingan todos los casos, incluido `NO_INTENTADO`.
- Comprobación: CUI-01 a CUI-06 con pruebas de interacción y recorrido responsive. Los filtros locales de demostración y los indicadores de prueba se identifican como simulados.
- Cierre y evidencia: documentar los límites de la simulación y los destinos ES-F04-02/03 aún no disponibles. No crear un contrato HTTP implícito a partir del fixture.

### T-05. Concretar el contrato central del listado

- [ ] Implementada y verificada.

- Alcance: resolver DT-01 en `integraciones/api-contract.md`: filtros y límites, paginación, respuesta, indicadores, orden estable y errores; enlazarlo desde los documentos consumidores.
- Responsable: Gerardo con Backend/Frontend y Arquitectura.
- Comprobación: revisión de solicitudes/respuestas representativas para CA-01 a CA-05; verificar que los datos necesarios estén descritos sin crear un segundo contrato.
- Cierre y evidencia: decisión y revisión enlazadas; los pendientes restantes identifican qué integración impiden. Esta tarea no se ejecuta en la preparación documental actual.

### T-06. Preparar persistencia y fuentes de datos

- [ ] Implementada y verificada.

- Alcance: revisar el esquema real y las migraciones requeridas; disponer de datos locales y del mecanismo acordado para nombre del repartidor y cierre de jornada, resolviendo DT-02/03.
- Responsable: Gerardo con Arquitectura y responsables de Operación; coordinar la base compartida con DevOps.
- Comprobación: preparar datos sintéticos de varios estados e intentos; verificar que no se cruzan bases de servicios y que la fuente distingue jornada activa/cerrada. Si hay migraciones nuevas, comprobar su aplicación en una base aislada.
- Cierre y evidencia: registrar revisiones y decisiones de integración, disponibilidad de las dependencias y cualquier doble de prueba utilizado.

### T-07. Implementar y probar la consulta backend

- [ ] Implementada y verificada.

- Alcance: controlador, caso de uso, puertos y adaptadores mínimos dentro de la funcionalidad de incidencias de Gestión; ruta pública a través del Gateway.
- Entradas: contrato cerrado, datos de T-06, base de seguridad y errores disponible; reglas y verificaciones de [spec.md](./spec.md).
- Comprobación: `./mvnw.cmd test` desde Gestión; PostgreSQL aislado para consulta y paginación; autorización de usuario con rol diferente; matriz de retorno atrasado, ausencia de duplicados y exclusión de datos del detalle. Probar también token ausente/inválido conforme al contrato de seguridad.
- Cierre y evidencia: CA-01 a CA-05 cubiertos en backend, con límites de dobles externos explícitos. La lectura no cambia datos de negocio ni genera eventos.

### T-08. Conectar el frontend a la API real

- [ ] Implementada y verificada.

- Alcance: adaptar la respuesta contractual desde el cliente de API, conectar filtros/URL/paginación y gestionar errores y respuestas fuera de orden; retirar la fuente simulada del recorrido real.
- Dependencias: I-01 e I-02; autenticación humana y Gateway disponibles. Coordinar los destinos de detalle/recepción cuando estén implementados.
- Comprobación: filtros combinados y límites, paginación con más de una página, reintentos y `403` después de cargar datos; `npm run typecheck` y `npm run build` en ambas apps.
- Cierre y evidencia: resultado real por Gateway enlazado; indicadores procedentes de la fuente acordada, sin totales fabricados desde una página parcial.

### T-09. Verificar y entregar la especificación

- [ ] Implementada y verificada.

- Alcance: ejecutar las comprobaciones de todos los criterios, completar [evidence.md](./evidence.md) y actualizar trazabilidad e índice cuando corresponda.
- Comprobación: registrar commits frontend/backend, entorno y dependencias; revisar teclado, móvil y ausencia de fotografías/comentarios en listado. La simulación aislada no sustituye la prueba real.
- Cierre: revisión funcional y técnica registrada; explicar cualquier destino o integración pendiente. Si queda un criterio obligatorio sin comprobar, el alcance permanece parcial.

## 3. Cobertura de criterios

| Criterio | Implementación | Verificación | Registro previsto |
|---|---|---|---|
| CA-01 | T-04, T-06, T-07, T-08 | T-07 y T-09 | EV-01, EV-04 |
| CA-02 | T-04 a T-08 según dependencias | T-07 y T-09 | EV-01, EV-04 |
| CA-03 | T-02, T-04, T-07, T-08 | T-07 y T-09 | EV-01 a EV-04 |
| CA-04 | T-02, T-04, T-07, T-08 | T-07 y T-09 | EV-01 a EV-04 |
| CA-05 | T-04, T-06, T-07, T-08 | T-07 y T-09 | EV-01, EV-03, EV-04 |
| CUI-01 | T-03, T-04, T-08 | T-04 y T-09 | EV-03, EV-04 |
| CUI-02 | T-03, T-04, T-08 | T-04 y T-09 | EV-03, EV-04 |
| CUI-03 | T-02, T-04, T-08 | T-04 y T-09 | EV-02 a EV-04 |
| CUI-04 | T-02, T-04, T-08 | T-04 y T-09 | EV-02 a EV-04 |
| CUI-05 | T-03, T-04, T-08 | T-04 y T-09 | EV-03, EV-04 |
| CUI-06 | T-02, T-03, T-04, T-08 | T-04 y T-09 | EV-02 a EV-04 |

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están implementadas y verificadas.
- [ ] Los criterios tienen evidencia reproducible y las limitaciones están registradas.
- [ ] Los contratos, fuentes de datos y dependencias necesarios están resueltos.
- [ ] Los documentos e índice están actualizados y la revisión está enlazada.

## 5. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-05 [cite: 1].
2. [Plan](./plan.md), incrementos I-01 a I-03 y pendientes DT-01 a DT-04 [cite: 2].
3. [UI](./ui.md), criterios CUI-01 a CUI-06, y [evidencia](./evidence.md) [cite: 3].
