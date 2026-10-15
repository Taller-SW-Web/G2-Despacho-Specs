# Evidencia de ES-F01-04: Configurar la tarifa vigente de una zona

**Estado:** Pendiente; esta plantilla no acredita una implementación.

**Responsable de verificación:** Valqui.

**Última verificación:** Pendiente.

## 1. Versión y entorno verificados

- Especificación y plan utilizados: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión de esta carpeta.
- Repositorios y commits de código: pendientes (frontend y Gestión de Despachos).
- Entorno: pendiente (local / pruebas / nube; versión o despliegue).
- Datos y preparación: pendientes; no incluir datos personales reales ni secretos.
- Dependencias: ninguna utilizada todavía; los componentes y el contrato están pendientes.
- Alcance efectivamente verificado: preparación documental; ningún criterio se declara aprobado por ella.

## 2. Cobertura de criterios

| Criterio | Tarea | Prueba o comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-05, T-06, T-07 | Tarifa válida guardada como vigente y aplicada | Pendiente | Pendiente |
| CA-02 | T-05, T-06, T-07 | Regla inválida o zona inexistente rechazada sin persistir | Pendiente | Pendiente |
| CA-03 | T-05, T-06, T-07 | Sustitución con la anterior conservada como histórico | Pendiente | Pendiente |
| CA-04 | T-05, T-06, T-07 | Zona activa sin tarifa identificada sin costo por defecto | Pendiente | Pendiente |
| CA-05 | T-05, T-06, T-07 | Rechazo sin datos ante rol distinto o sin token | Pendiente | Pendiente |
| CUI-01 | T-03, T-06, T-07 | Guardado válido y confirmación | Pendiente | Pendiente |
| CUI-02 | T-03, T-06, T-07 | Campos inválidos marcados y guardado bloqueado | Pendiente | Pendiente |
| CUI-03 | T-03, T-06, T-07 | Aviso de sustitución y confirmación | Pendiente | Pendiente |
| CUI-04 | T-03, T-06, T-07 | Panel sin tarifa con valores sugeridos | Pendiente | Pendiente |
| CUI-05 | T-03, T-06, T-07 | Zona inactiva con guardado bloqueado | Pendiente | Pendiente |
| CUI-06 | T-03, T-06, T-07 | Ocultar panel tras denegación | Pendiente | Pendiente |
| CUI-07 | T-03, T-06, T-07 | Teclado, foco en primer error y responsive | Pendiente | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles debe identificar su límite y no acredita integración real.

## 3. Registros de verificación

### EV-01. Consulta, guardado y seguridad del backend

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-05/T-07; CA-01 a CA-05.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: `./mvnw.cmd test` desde Gestión de Despachos, con PostgreSQL aislado y Docker para Testcontainers.
- Resultado esperado: consulta y guardado válidos; rechazo de valores inválidos; rechazo de zona inexistente o inactiva; sustitución con histórico; una sola tarifa vigente; rechazo de rol distinto.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: pendiente (reporte de pruebas).
- Dependencias simuladas y límites: ninguna.

### EV-02. Componentes compartidos

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-01/T-02; criterios `CCR-NN-XX` de los CR consumidos en CUI-01 a CUI-07.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: pruebas de interacción de los componentes compartidos, una vez habilitadas las herramientas.
- Resultado esperado: componentes exportados y verificados, sin llamadas HTTP.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: enlace a la evidencia compartida y al commit del frontend.
- Dependencias simuladas y límites: fixtures de presentación.

### EV-03. Panel aislado e interacción

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-03; CUI-01 a CUI-07.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: fixtures de zona con y sin tarifa, con errores de validación y zona inactiva; recorrido con teclado y viewport móvil.
- Resultado esperado: validaciones y estados de UI correctos. No valida la autorización ni las reglas del servidor.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: pendiente (reporte y capturas).
- Dependencias simuladas y límites: API simulada.

### EV-04. Recorrido con servicios reales

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-06/T-07; CA-01 a CA-05 y CUI-01 a CUI-07.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: contrato cerrado, datos sintéticos y servicios identificados; acceso humano por Gateway.
- Resultado esperado: consulta y guardado reales, sustitución correcta y permisos respetados.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: pendiente.
- Dependencias simuladas y límites: ninguna.

Cada registro ejecutado debe indicar versión exacta, preparación reproducible, resultado observado y artefacto. No incluir tokens, credenciales ni datos personales reales.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| Preparación documental de la carpeta SDD | opencode, 15/10/2026 | Especificación previa `12d5041`, plantillas SDD, F-01, contrato, modelo, diseño y componentes | Solicitud de Valqui/Gerardo: migrar ES-F01-04 conservando reglas y criterios CA-01 a CA-05 y completar los documentos. Revisión humana: pendiente. | Pendiente |

Este registro describe asistencia en documentación; no acredita ejecución de T-01 a T-07 ni pruebas aprobadas.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| DT-01: cuerpo de la tarifa y errores pendientes en el contrato. | CA-01 a CA-05 | Bloquea la integración real, no la UI aislada | Revisar el contrato antes de integrar; Valqui con Backend/Frontend |
| DT-02: equivalencia entre campos del contrato y `tarifas_zona`. | CA-01, CA-03 | Mapeo de la regla y su vigencia | Acordar con Arquitectura |
| DT-03: base compartida de JWT, errores, conexión de datos y rutas del Gateway. | CA-01 a CA-05 | Bloquea la ejecución real del backend | Coordinar con Arquitectura y DevOps |
| DT-04: componentes, tema y herramientas de pruebas. | CUI-01 a CUI-07 | Bloquea la composición del panel | Coordinar con los responsables de CR |
| DT-05: definición de «tarifa vigente», índice único parcial y tratamiento del histórico. | CA-03 | Una sola tarifa vigente y conservación del histórico | Acordar con Arquitectura |

Sin hallazgos de implementación porque no se ha ejecutado aún ninguna tarea.

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor y fecha: pendientes.
- Resultado de revisión: pendiente.
- Estado del alcance: Pendiente.
- Integraciones reales pendientes: contrato §9.1 y §14, Gateway y componentes compartidos.

## 7. Referencias

1. [Especificación funcional](./spec.md): comportamiento esperado y criterios CA-01 a CA-05.
2. [Plan](./plan.md) y [tareas](./tasks.md): incrementos y pendientes.
3. [Flujo SDD](../../plantillas/sdd/README.md), [componentes React](../../disenio/componentes-react.md) y [contrato de API](../../integraciones/api-contract.md).
