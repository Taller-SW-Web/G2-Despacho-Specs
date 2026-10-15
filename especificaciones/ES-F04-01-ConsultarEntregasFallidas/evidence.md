# Evidencia de ES-F04-01: Consultar entregas fallidas

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Gerardo.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), incorporados en la misma revisión de esta carpeta.
- Origen de la especificación y fuentes generales: revisión `8586a78` del repositorio de especificaciones.
- Base de código consultada: backend `af13989` y frontend `d2bc27d`; no constituyen una implementación de ES-F04-01.
- Commits de implementación, entorno funcional y datos ejecutados: pendientes.
- Dependencias reales o simuladas: aún no utilizadas en pruebas de comportamiento de esta especificación.
- Alcance efectivamente verificado: preparación documental; ningún criterio funcional o de UI se declara aprobado por ella.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-07, T-08, T-09 | Listado autorizado de fallidos con campos e indicadores y paginación. | EV-01, EV-04 | No ejecutado |
| CA-02 | T-07, T-08, T-09 | Combinaciones de filtros, fechas y páginas. | EV-01, EV-04 | No ejecutado |
| CA-03 | T-02, T-04, T-07, T-09 | Vacío, sin coincidencias y recuperación ante error. | EV-01 a EV-04 | No ejecutado |
| CA-04 | T-02, T-04, T-07, T-09 | Rechazo sin datos y retirada de contenido previo. | EV-01 a EV-04 | No ejecutado |
| CA-05 | T-06, T-07, T-08, T-09 | Jornada cerrada/activa y recepción pendiente/confirmada. | EV-01, EV-03, EV-04 | No ejecutado |
| CUI-01 | T-04, T-08, T-09 | Composición, campos e indicadores. | EV-03, EV-04 | No ejecutado |
| CUI-02 | T-04, T-08, T-09 | Filtros, URL, paginación y respuestas fuera de orden. | EV-03, EV-04 | No ejecutado |
| CUI-03 | T-02, T-04, T-08, T-09 | Estados de carga, vacío, sin resultados y error. | EV-02 a EV-04 | No ejecutado |
| CUI-04 | T-02, T-04, T-08, T-09 | Ocultar contenido protegido tras denegación. | EV-02 a EV-04 | No ejecutado |
| CUI-05 | T-04, T-08, T-09 | Presentación de retorno atrasado. | EV-03, EV-04 | No ejecutado |
| CUI-06 | T-02, T-04, T-08, T-09 | Teclado, foco, nombres accesibles y responsive. | EV-02 a EV-04 | No ejecutado |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles debe identificar su límite y no acredita integración real [cite: 1, 2].

## 3. Registros de verificación previstos

### EV-01. Consulta y seguridad del backend

- Tareas y criterios: T-06/07/09; CA-01 a CA-05.
- Preparación prevista: PostgreSQL aislado con varios estados, intentos y recepciones; JWT de prueba con roles distintos; fuente de jornada identificada como real o doble.
- Comando previsto: `./mvnw.cmd test` desde Gestión de Despachos, con Docker para Testcontainers.
- Esperado: solo fallidos, filtros y páginas correctos, rechazo sin datos, retorno atrasado según la jornada y ninguna mutación de negocio.
- Fecha, persona, commits, resultado observado y reporte: pendientes. **Resultado: No ejecutado.**

### EV-02. Componente compartido CR-08

- Tareas y criterios: T-01/02; CCR-08-01 y su consumo en CUI-03/04/06.
- Preparación prevista: fixtures identificados y pruebas de interacción, con herramientas habilitadas según T-01.
- Esperado: estados diferenciados, acciones accesibles y ausencia de contenido protegido. Enlazar la evidencia compartida y añadir después la de su consumo.
- Fecha, persona, commit, comando y reporte: pendientes. **Resultado: No ejecutado.**

### EV-03. Página aislada e interacción

- Tareas y criterios: T-03/04; CUI-01 a CUI-06.
- Preparación prevista: fixtures de presentación con las combinaciones de recepción, etiquetas y estados de consulta.
- Esperado: controles y recuperaciones correctos; recorrido con teclado y adaptación a escritorio/móvil. Esta prueba no valida la autorización ni el filtrado del servidor.
- Fecha, persona, commit, pasos y capturas/reportes: pendientes. **Resultado: No ejecutado.**

### EV-04. Recorrido con servicios reales

- Tareas y criterios: T-08/09; CA-01 a CA-05 y CUI-01 a CUI-06.
- Preparación prevista: contrato revisado, datos sintéticos y servicios identificados; acceso humano por Gateway; fuentes de jornada y repartidor disponibles.
- Esperado: consulta real, filtros y permisos correctos, estados recuperables y cifras confirmadas. Registrar por separado los destinos de detalle/recepción disponibles o pendientes.
- Fecha, persona, commits, entorno, comandos y reportes: pendientes. **Resultado: No ejecutado.**

Cada registro ejecutado debe indicar versión exacta, preparación reproducible, resultado observado y artefacto. No incluir tokens, credenciales ni datos personales reales.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción y revisión |
|---|---|---|---|
| Preparación documental de la carpeta SDD | Codex, 15/10/2026 | Especificación previa, plantillas aprobadas en `8586a78`, F-04, contrato, modelo, diseño y componentes; bases de código de §1. | Solicitud de Gerardo: alinear reglas y después preparar únicamente la primera especificación, conservando el contenido existente y completando los documentos. Revisión humana de los nuevos documentos: pendiente. |

Este registro describe asistencia en documentación; no acredita ejecución de T-01 a T-09 ni pruebas aprobadas.

## 5. Diferencias y pendientes

| Hallazgo | Criterios afectados | Efecto y siguiente acción |
|---|---|---|
| DT-01: detalle contractual del listado pendiente. | CA-01 a CA-05 y CUI-02. | Revisar el contrato central posteriormente, antes de integrar el transporte HTTP. |
| DT-02: fuentes de repartidor y cierre de jornada pendientes de concretar. | CA-01/05 y CUI-01/05. | Acordar mecanismo y tratamiento de indisponibilidad con Operación. |
| DT-03/04: bases de ejecución y componentes aún por verificar/implementar. | Todos. | Coordinar preparación y componentes, ejecutar tareas y registrar resultados. |

## 6. Entrega y revisión

- Entrega actual: documentos SDD; implementación funcional pendiente.
- Commits y PR de implementación: pendientes.
- Revisor, fecha y resultado de revisión funcional/técnica: pendientes.
- Estado del alcance funcional: Pendiente.
- Integración real y destinos de otras especificaciones: pendientes según el plan.

## 7. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [plan](./plan.md) y [tareas](./tasks.md).
2. [Flujo SDD](../../plantillas/sdd/README.md), reglas de evidencia y verificación.
3. [Componentes React](../../disenio/componentes-react.md), §4.2 para evidencia compartida.
