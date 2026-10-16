# Evidencia de ES-F01-03: Activar y desactivar una zona de cobertura

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
| CA-01 | T-05, T-06, T-07 | Activación sin conflicto y cobertura posterior | Pendiente | Pendiente |
| CA-02 | T-05, T-06, T-07 | Conflicto `409` de solapamiento conservando `INACTIVO` | Pendiente | Pendiente |
| CA-03 | T-05, T-06, T-07 | Desactivación con despachos existentes que conservan su zona | Pendiente | Pendiente |
| CA-04 | T-05, T-06, T-07 | Idempotencia por repetición sin auditoría duplicada | Pendiente | Pendiente |
| CA-05 | T-05, T-06, T-07 | Concurrencia: una sola se aplica, la otra `409` | Pendiente | Pendiente |
| CA-06 | T-05, T-06, T-07 | Rechazo sin datos ante rol distinto o sin token | Pendiente | Pendiente |
| CUI-01 | T-03, T-06, T-07 | Desactivación siempre con confirmación | Pendiente | Pendiente |
| CUI-02 | T-03, T-06, T-07 | Activación sin conflicto y fila actualizada | Pendiente | Pendiente |
| CUI-03 | T-03, T-06, T-07 | Conflicto de solapamiento explicado | Pendiente | Pendiente |
| CUI-04 | T-03, T-06, T-07 | Aviso de sin cambio al repetir | Pendiente | Pendiente |
| CUI-05 | T-03, T-06, T-07 | Conflicto de versión concurrente informado | Pendiente | Pendiente |
| CUI-06 | T-03, T-06, T-07 | Cierre y retirada de datos tras `403` | Pendiente | Pendiente |
| CUI-07 | T-03, T-06, T-07 | Teclado, foco contenido y responsive | Pendiente | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles debe identificar su límite y no acredita integración real.

## 3. Registros de verificación

### EV-01. Cambio de estado y seguridad del backend

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-05/T-07; CA-01 a CA-06.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: `./mvnw.cmd test` desde Gestión de Despachos, con PostgreSQL aislado y Docker para Testcontainers.
- Resultado esperado: activación sin conflicto; conflicto de solapamiento; desactivación con despachos existentes; repetición idempotente sin auditoría duplicada; concurrencia resuelta con `409`; rechazo de rol distinto.
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

### EV-03. Confirmación aislada e interacción

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-03; CUI-01 a CUI-07.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: fixtures de activación, desactivación, conflicto, sin cambio y permisos; recorrido con teclado y viewport móvil.
- Resultado esperado: advertencia y estados de UI correctos. No valida la autorización ni las reglas del servidor.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: pendiente (reporte y capturas).
- Dependencias simuladas y límites: API simulada.

### EV-04. Recorrido con servicios reales

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-06/T-07; CA-01 a CA-06 y CUI-01 a CUI-07.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: contrato cerrado, datos sintéticos y servicios identificados; acceso humano por Gateway.
- Resultado esperado: cambios de estado reales, conflictos correctos y permisos respetados, sin despachos alterados.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: pendiente.
- Dependencias simuladas y límites: ninguna.

Cada registro ejecutado debe indicar versión exacta, preparación reproducible, resultado observado y artefacto. No incluir tokens, credenciales ni datos personales reales.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| Preparación documental de la carpeta SDD | opencode, 15/10/2026 | Especificación previa `12d5041`, plantillas SDD, F-01, contrato, modelo, diseño y componentes | Solicitud de Valqui/Gerardo: migrar ES-F01-03 conservando reglas y criterios CA-01 a CA-06 y completar los documentos. Revisión humana: pendiente. | Pendiente |

Este registro describe asistencia en documentación; no acredita ejecución de T-01 a T-07 ni pruebas aprobadas.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| DT-01: formato del `409` (solapamiento y versión) e idempotencia pendientes en el contrato. | CA-01 a CA-06 | Bloquea la integración real, no la UI aislada | Revisar el contrato antes de integrar; Valqui con Backend/Frontend |
| DT-02: `zona_distritos` frente a `zonas_distritos` en el modelo. | CA-02 | Detección de solapamiento | Conciliar con Arquitectura |
| DT-03: base compartida de JWT, errores, conexión de datos y rutas del Gateway. | CA-01 a CA-06 | Bloquea la ejecución real del backend | Coordinar con Arquitectura y DevOps |
| DT-04: componentes, tema y herramientas de pruebas. | CUI-01 a CUI-07 | Bloquea la composición de la confirmación | Coordinar con los responsables de CR |
| DT-05: `zonas` no define columna de versión en el modelo. | CA-05 | Posibles cambios concurrentes sin detección | Acordar control de versión con Arquitectura |
| DT-06: alcance de la conservación de despachos y asignaciones tras la desactivación. | CA-03 | Efecto sobre despachos existentes | Acordar con Arquitectura |

Sin hallazgos de implementación porque no se ha ejecutado aún ninguna tarea.

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor y fecha: pendientes.
- Resultado de revisión: pendiente.
- Estado del alcance: Pendiente.
- Integraciones reales pendientes: contrato de Gestión §3.1 y contrato externo §9, Gateway y componentes compartidos.

## 7. Referencias

1. [Especificación funcional](./spec.md): comportamiento esperado y criterios CA-01 a CA-06.
2. [Plan](./plan.md) y [tareas](./tasks.md): incrementos y pendientes.
3. [Flujo SDD](../../plantillas/sdd/README.md), [componentes React](../../disenio/componentes-react.md), [contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md) y [convenciones compartidas](../../integraciones/api-contract.md#3-convenciones-comunes).
