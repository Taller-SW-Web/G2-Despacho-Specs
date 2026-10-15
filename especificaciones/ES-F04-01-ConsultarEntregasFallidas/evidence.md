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
- Revisión del 15/10/2026: seis decisiones de comportamiento confirmadas por Gerardo; contrato y modelo en `4bad49d`, reglas de consulta en `1f556c0`. Implementación de fuentes, endpoints y componentes pendiente.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-07, T-08, T-09 | Listado autorizado de fallidos con campos e indicadores y paginación. | EV-01, EV-04 | No ejecutado |
| CA-02 | T-07, T-08, T-09 | Combinaciones de filtros, fechas y páginas. | EV-01, EV-04 | No ejecutado |
| CA-03 | T-02, T-04, T-07, T-09 | Vacío, sin coincidencias y recuperación ante error. | EV-01 a EV-04 | No ejecutado |
| CA-04 | T-02, T-04, T-07, T-09 | Rechazo sin datos y retirada de contenido previo. | EV-01 a EV-04 | No ejecutado |
| CA-05 | T-06, T-07, T-08, T-09 | Jornada cerrada/activa y recepción pendiente/confirmada. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-06 | T-06, T-07, T-08, T-09 | Incidencia vigente sin duplicados ni recepción heredada. | EV-01, EV-04 | No ejecutado |
| CA-07 | T-07, T-08, T-09 | Recibidos primero, antigua primero y desempate entre páginas. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-08 | T-06, T-07, T-08, T-09 | Métricas 7/5/2, tarjetas y filtros independientes de página. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-09 | T-07, T-08, T-09 | `NO_INTENTADO` con contador cero/uno sin aumento ni reinicio. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-10 | T-06, T-07, T-08, T-09 | Jornada desconocida, nombre ausente y error al filtrar atrasados. | EV-01, EV-03, EV-04 | No ejecutado |
| CA-11 | T-07, T-08, T-09 | Filtros inválidos y errores diferenciados de vacío. | EV-01, EV-03, EV-04 | No ejecutado |
| CUI-01 | T-04, T-08, T-09 | Composición, campos e indicadores. | EV-03, EV-04 | No ejecutado |
| CUI-02 | T-04, T-08, T-09 | Filtros, URL, paginación y respuestas fuera de orden. | EV-03, EV-04 | No ejecutado |
| CUI-03 | T-02, T-04, T-08, T-09 | Estados de carga, vacío, sin resultados y error. | EV-02 a EV-04 | No ejecutado |
| CUI-04 | T-02, T-04, T-08, T-09 | Ocultar contenido protegido tras denegación. | EV-02 a EV-04 | No ejecutado |
| CUI-05 | T-04, T-08, T-09 | Presentación de retorno atrasado. | EV-03, EV-04 | No ejecutado |
| CUI-06 | T-02, T-04, T-08, T-09 | Teclado, foco, nombres accesibles y responsive. | EV-02 a EV-04 | No ejecutado |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles debe identificar su límite y no acredita integración real [cite: 1, 2].

## 3. Registros de verificación previstos

### EV-01. Consulta y seguridad del backend

- Tareas y criterios: T-06/07/09; CA-01 a CA-11.
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

- Tareas y criterios: T-08/09; CA-01 a CA-11 y CUI-01 a CUI-06.
- Preparación prevista: contrato revisado, datos sintéticos y servicios identificados; acceso humano por Gateway; fuentes de jornada y repartidor disponibles.
- Esperado: consulta real, filtros y permisos correctos, estados recuperables y cifras confirmadas. Registrar por separado los destinos de detalle/recepción disponibles o pendientes.
- Fecha, persona, commits, entorno, comandos y reportes: pendientes. **Resultado: No ejecutado.**

Cada registro ejecutado debe indicar versión exacta, preparación reproducible, resultado observado y artefacto. No incluir tokens, credenciales ni datos personales reales.

### EV-05. Comprobación documental de los acuerdos

- Fecha y herramienta: 15/10/2026, Codex mediante Git y Python del entorno de trabajo.
- Alcance: T-05; definición documental del catálogo/listado/lectura operativa y alineamiento de spec, UI, plan, tareas, historia y diseños. No verifica un endpoint ni una pantalla implementados.
- Comprobaciones: `git diff --check`; lectura y parseo de todos los bloques JSON del contrato; revisión de enlaces locales de los documentos modificados, unicidad de criterios y cobertura CA-01 a CA-11/CUI-01 a CUI-06 en tareas y evidencia; comprobación de consistencia del ejemplo de respuesta con sus totales e indicadores.
- Resultado: comprobación documental aprobada. `git diff --check` sin errores; 43 ejemplos JSON válidos; 170 enlaces locales comprobados sin destinos inexistentes; CA-01 a CA-11 y CUI-01 a CUI-06 únicos y cubiertos por tareas/evidencia. El ejemplo del listado es coherente con su contador, recepción, jornada, métricas y paginación. Los resultados funcionales de EV-01 a EV-04 continúan `No ejecutado`.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción y revisión |
|---|---|---|---|
| Preparación documental de la carpeta SDD | Codex, 15/10/2026 | Especificación previa, plantillas aprobadas en `8586a78`, F-04, contrato, modelo, diseño y componentes; bases de código de §1. | Solicitud de Gerardo: alinear reglas y después preparar únicamente la primera especificación, conservando el contenido existente y completando los documentos. Revisión humana de los nuevos documentos: pendiente. |
| Revisión de reglas de ES-F04-01 | Codex, 15/10/2026 | Seis recomendaciones confirmadas por Gerardo, carpeta SDD, contrato, modelo y diseños relacionados. | Aplicar los acuerdos y alinear documentos; guardar el trabajo en rama y commits separados según CONTRIBUTING. Revisión de comportamiento por Gerardo: confirmada en la conversación. Verificación contra implementación: pendiente. |

Este registro describe asistencia en documentación y el cierre documental de T-05; no acredita implementación ni pruebas funcionales aprobadas de T-01 a T-04 o T-06 a T-09.

## 5. Diferencias y pendientes

| Hallazgo | Criterios afectados | Efecto y siguiente acción |
|---|---|---|
| DT-01: contrato definido en Gestión §4, Gestión §5.1; implementación pendiente. | CA-01 a CA-11 y CUI-02. | Implementar y comprobar consumidores conforme a T-07/08; T-05 solo acredita documentación. Referencia: [Gestión](../../integraciones/api-contract-gestion-despachos.md#4-catálogo-único-de-motivos-de-fallo). |
| DT-02: fuente y degradación definidas en Operación §5.4 y Gestión §5.1; proveedor/adaptador pendientes. | CA-01/05/06/08/10 y CUI-01/05. | Implementar lectura por lotes, referencia de incidencia y pruebas contra Operación en T-06/07. Referencia: [Operación](../../integraciones/api-contract-operacion-reparto.md#54-gestión-consulta-repartidores-y-jornadas-de-incidencias), [Gestión](../../integraciones/api-contract-gestion-despachos.md#51-consultar-entregas-fallidas--es-f04-01). |
| DT-03/04: bases de ejecución y componentes aún por verificar/implementar. | Todos. | Coordinar preparación y componentes, ejecutar tareas y registrar resultados. |

## 6. Entrega y revisión

- Entrega actual: documentos SDD; implementación funcional pendiente.
- Commits y PR de implementación: pendientes.
- Reglas de consulta: confirmadas por Gerardo el 15/10/2026. Revisión técnica y funcional de la implementación: pendientes.
- Estado del alcance funcional: Pendiente.
- Integración real y destinos de otras especificaciones: pendientes según el plan.

## 7. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [plan](./plan.md) y [tareas](./tasks.md).
2. [Flujo SDD](../../plantillas/sdd/README.md), reglas de evidencia y verificación.
3. [Componentes React](../../disenio/componentes-react.md), §4.2 para evidencia compartida.
