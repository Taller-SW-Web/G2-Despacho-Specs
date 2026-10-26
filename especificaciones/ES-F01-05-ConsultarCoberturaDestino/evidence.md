# Evidencia de ES-F01-05: Consultar la cobertura de un destino

**Estado:** Pendiente; esta plantilla no acredita una implementación.

**Responsable de verificación:** Valqui.

**Última verificación:** Pendiente.

## 1. Versión y entorno verificados

- Especificación y plan utilizados: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión de esta carpeta.
- Repositorios y commits de código: pendientes (Gestión de Despachos).
- Entorno: pendiente (local / pruebas / nube; versión o despliegue).
- Datos y preparación: pendientes; no incluir datos personales reales ni secretos.
- Dependencias: ninguna utilizada todavía; el contrato y la base de tokens están pendientes.
- Alcance efectivamente verificado: preparación documental; ningún criterio se declara aprobado por ella.
- UI: no aplica; no se incluye `ui.md`.
- Actualización documental del 26/10/2026: la persona responsable comunica datos existentes en `zonas_codigos_postales`; se alinea la fuente postal y se excluye esta consulta de la persistencia exacta. No se inspeccionaron tablas ni se ejecutaron pruebas del lector.

## 2. Cobertura de criterios

| Criterio | Tarea | Prueba o comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-07 | Destino cubierto responde disponibilidad y zona sin costo | Pendiente | Pendiente |
| CA-02 | T-03, T-07 | Destino fuera de cobertura responde `200` con `false` | Pendiente | Pendiente |
| CA-03 | T-03, T-07 | Falta de `distrito` produce `DESP_ERROR_DESTINO_REQUERIDO` | Pendiente | Pendiente |
| CA-04 | T-04, T-07 | Token ausente o sin scope rechazado sin revelar cobertura | Pendiente | Pendiente |
| CA-05 | T-05, T-07 | Exceso de límite produce `429` con `DESP_ERROR_LIMITE_COTIZACION` | Pendiente | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con dobles debe identificar su límite y no acredita integración real.

## 3. Registros de verificación

### EV-01. Casos de uso, autorización y seguridad del backend

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-03/T-04/T-07; CA-01 a CA-04.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: `./mvnw.cmd test` desde Gestión de Despachos, con PostgreSQL aislado y Docker para Testcontainers.
- Resultado esperado: destino cubierto y no cubierto correctos; ausencia de `distrito` rechazada; token ausente o sin scope rechazado sin revelar cobertura; sin modificar recursos.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: pendiente (reporte de pruebas).
- Dependencias simuladas y límites: ninguna.

### EV-02. Base compartida del backend

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-02; soporte de CA-01 a CA-05.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: compilación y arranque del servicio con esquema, errores, conexión y rutas configuradas.
- Resultado esperado: servicio operativo con la configuración acordada.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: enlace a commit y configuración.
- Dependencias simuladas y límites: ninguna.

### EV-03. Límite de tasa

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-05; CA-05.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: superar el límite por el mismo `sub` e IP con `LIMITE_COTIZACIONES_POR_MINUTO`.
- Resultado esperado: la consulta sin líneas también recibe `429` con `DESP_ERROR_LIMITE_COTIZACION`.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: pendiente.
- Dependencias simuladas y límites: mecanismo del límite definido en DT-05.

### EV-04. Recorrido con los canales por Gateway

- Fecha y persona que verificó: pendiente.
- Tareas y criterios: T-06/T-07; CA-01 a CA-04.
- Commit y entorno exactos: pendientes.
- Preparación y pasos o comando: contrato cerrado, canal simulado y servicios identificados; acceso con token de servicio por Gateway.
- Resultado esperado: consumo conforme al contrato, sin costo ni datos de configuración.
- Resultado observado: pendiente.
- Resultado de la comprobación: Pendiente.
- Artefacto: pendiente.
- Dependencias simuladas y límites: ninguna.

Cada registro ejecutado debe indicar versión exacta, preparación reproducible, resultado observado y artefacto. No incluir tokens, credenciales ni datos personales reales.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| Preparación documental de la carpeta SDD | opencode, 15/10/2026 | Especificación previa `12d5041`, plantillas SDD, F-01, contrato, modelo y arquitectura | Solicitud de Valqui/Gerardo: migrar ES-F01-05 conservando reglas y criterios CA-01 a CA-05 y completar los documentos. Revisión humana: pendiente. | Pendiente |

Este registro describe asistencia en documentación; no acredita ejecución de T-01 a T-07 ni pruebas aprobadas.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| DT-01: DTO y errores de cobertura pendientes en el contrato. | CA-01 a CA-05 | Bloquea la implementación del adaptador | Revisar el contrato; Valqui con Backend y Arquitectura |
| DT-02: fuente postal `zonas_codigos_postales` documentada; lector y precedencia todavía sin verificar. | CA-01/02 | Evaluación compartida de cobertura, sin nuevas cotizaciones | Contrastar esquema, consultas y casos de conflicto con Arquitectura/Backend |
| DT-03: base compartida, tokens de servicio y rutas del Gateway. | CA-01 a CA-05 | Bloquea la ejecución real | Coordinar con Arquitectura, DevOps y Seguridad |
| DT-04: verificación del consumo de Marketplace y Chatbot. | CA-01 a CA-04 | Aceptación de la integración | Acordar con los responsables de los canales |
| DT-05: mecanismo del límite de tasa y valor del parámetro. | CA-05 | Control de tasa | Acordar con Arquitectura y DevOps |

Sin hallazgos de implementación porque no se ha ejecutado aún ninguna tarea.

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor y fecha: pendientes.
- Resultado de revisión: pendiente.
- Estado del alcance: Pendiente.
- Integraciones reales pendientes: contrato §5.1, Gateway, Seguridad y canales.

## 7. Referencias

1. [Especificación funcional](./spec.md): comportamiento esperado y criterios CA-01 a CA-05.
2. [Plan](./plan.md) y [tareas](./tasks.md): incrementos y pendientes.
3. [Flujo SDD](../../plantillas/sdd/README.md) y [contrato de API](../../integraciones/api-contract.md).
