# Evidencia de ES-F01-08: Registrar la trazabilidad de la configuración

**Estado:** Pendiente; la preparación documental no acredita implementación.

**Responsable de verificación:** Valqui.

**Última verificación funcional:** Pendiente.

## 1. Versión y entorno verificados

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), preparación del 16/10/2026 a partir de `91db8f8`.
- Repositorios y commits de código: pendientes, Gestión de Despachos.
- Entorno, despliegue, datos y preparación: pendientes.
- Dependencias: ES-F01-02/03/04 y autenticación no ejecutadas; decisiones de modelo e idempotencia pendientes.
- Alcance efectivamente verificado: ningún criterio funcional ejecutado; solo preparación documental SDD.
- UI: no aplica; captura automática sin interfaz nueva ni `ui.md`.

## 2. Cobertura de criterios

| Criterio | Tarea | Prueba o comprobación | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-03, T-05 | Creación con auditoría, ejecutor y UTC | EV-02, EV-03 | Pendiente |
| CA-02 | T-03, T-05 | Estado anterior/nuevo conservados | EV-03 | Pendiente |
| CA-03 | T-01 a T-05 | Sustitución tarifaria auditable y consultable | EV-01, EV-03, EV-04 | Pendiente |
| CA-04 | T-03, T-05 | Rechazo sin éxito y reversión ante fallo | EV-03 | Pendiente |
| CA-05 | T-04, T-05 | Repetición sin registro adicional | EV-04 | Pendiente |
| CA-06 | T-02, T-04, T-05 | Histórico sin edición ni eliminación | EV-02, EV-04 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. La revisión documental o una prueba aislada no acredita atomicidad de la persistencia real.

## 3. Registros de verificación

### EV-01. Revisión de modelo e identidad

- Tareas y criterios: T-01; soporte de todos, especialmente CA-03/05.
- Preparación y pasos previstos: cerrar DT-01 a DT-04 y revisar ejemplos de sustitución, identidad de operación, acciones y consulta en modelo/contrato de Gestión.
- Resultado esperado: una operación con las dos reglas tarifarias reconstruibles, identidad de reintento y consulta autorizada acordadas.
- Fecha, persona, revisión/commit y entorno: pendientes.
- Resultado observado y artefacto de revisión: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: no utilizadas; la revisión no prueba el backend.

### EV-02. Persistencia e integridad

- Tareas y criterios: T-02/T-05; soporte de CA-01/03 y CA-06.
- Preparación y pasos previstos: PostgreSQL aislado, modelo conciliado y migración si aplica; insertar y leer registros, validar restricciones y ausencia de operaciones de mutación desde la funcionalidad.
- Resultado esperado: valores e identidad íntegros, fechas UTC y registros previos conservados tras migración si corresponde.
- Fecha, persona, commit, entorno y comando exacto de la suite: pendientes.
- Resultado observado y reporte: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: persistencia real requerida; otras dependencias por registrar.

### EV-03. Captura transaccional

- Tareas y criterios: T-03/T-05; CA-01 a CA-04 y edición de zona.
- Preparación y pasos previstos: ejecutar altas, edición, activación/desactivación y sustitución tarifaria con JWT conocido; rechazar configuración inválida e inyectar fallo de auditoría/negocio; intentar aportar usuario u hora desde cliente.
- Resultado esperado: un registro por operación aceptada, valores anterior/nuevo, identidad del JWT y hora del servidor; sin auditoría de éxito ante rechazo ni escritura parcial ante fallo.
- Fecha, persona, commit, entorno y comando/pasos exactos: pendientes.
- Resultado observado y artefacto: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: reloj y fallos controlados previstos; identificar cuáles recorridos usan autenticación real.

### EV-04. Repetición y consulta autorizada

- Tareas y criterios: T-04/T-05; CA-03, CA-05 y CA-06.
- Preparación y pasos previstos: repetir operación aceptada y duplicado concurrente con la identidad acordada; pedir estado ya vigente, consultar histórico y probar acceso sin rol e intentos de mutación.
- Resultado esperado: sin auditoría adicional para reintento/estado sin cambio; nuevas decisiones legítimas distinguibles; histórico íntegro y cronológico, con acceso autorizado.
- Fecha, persona, commit, entorno y comando/pasos exactos: pendientes.
- Resultado observado y artefactos: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: mecanismo de identidad/consulta de DT-03/04 sin implementar; registrar servicios reales al ejecutar.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| Migración y preparación SDD | OpenCode, 16/10/2026 | Original, F-01, contratos, modelo y diseño en `91db8f8`; plantillas SDD y modelo ES-F01-05 | Completar las carpetas ES-F01-06, ES-F01-07 y ES-F01-08 según el modelo existente | Pendiente de revisión humana |

Se trasladaron reglas y criterios y se prepararon plan, tareas y registros pendientes; no acredita ejecución de T-01 a T-05.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| DT-01: sustitución de tarifa afecta dos reglas y el modelo tiene una entidad por registro | CA-03 | Representación de una operación sin duplicación pendiente | Valqui con Arquitectura |
| DT-02: identidad, marcas y acciones por conciliar | CA-01, CA-02, CA-03, CA-06 | Bloquea persistencia final | Valqui con Arquitectura y Seguridad |
| DT-03: identidad concreta de reintento no definida para configuración | CA-05 | Bloquea comprobación de no duplicación | Valqui con Backend |
| DT-04: consulta histórica y desempate de orden no definidos en Gestión | CA-03 y consulta de trazabilidad | Bloquea lectura final | Valqui con Backend y responsables de vistas |

No hay resultados de implementación ejecutados en esta preparación.

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor, fecha y resultado de revisión: pendientes.
- Estado del alcance: Pendiente.
- Integraciones reales pendientes: operaciones de ES-F01-02/03/04 y autenticación con Seguridad.

## 7. Referencias

1. [cite: 1] [Especificación](./spec.md), CA-01 a CA-06.
2. [cite: 2] [Plan](./plan.md) y [tareas](./tasks.md).
3. [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md), [modelo](../../arquitectura/modelo-datos.md) y [flujo SDD](../../plantillas/sdd/README.md).
