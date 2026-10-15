# Tareas de ES-F01-03: Activar y desactivar una zona de cobertura

**Responsable de coordinación:** Valqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), misma revisión documental que esta carpeta.

Esta entrega prepara las tareas; no ejecuta cambios de contrato, componentes ni código. Los responsables de componentes son los del [reparto compartido](../../disenio/componentes-react.md), §4.5; esta lista no crea issues ni acredita su aceptación.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Base frontend y herramientas de pruebas verificadas | Preparación compartida | DT-04 del plan; coordinación con Rhamses/Max | CUI-01 a CUI-07 como soporte | Pendiente |
| T-02 | Componentes de confirmación disponibles y verificados | Componentes compartidos | T-01 y dependencias de cada CR | CUI-01 a CUI-07 | Pendiente |
| T-03 | Confirmación aislada verificable con fixtures | Frontend, I-01 | T-02 | CUI-01 a CUI-07, sin acreditar backend real | Pendiente |
| T-04 | Contrato del cambio de estado concretado en su documento central | Contrato | Revisión posterior DT-01 | CA-01 a CA-06; controles de CUI-03 a CUI-05 | Pendiente |
| T-05 | Caso de uso backend implementado y probado | Backend, I-02 | T-04 y base JWT/errores de DT-03 | CA-01 a CA-06 | Pendiente |
| T-06 | Confirmación conectada a la API real | Integración, I-03 | T-03, T-05 y Gateway accesible | CA-01 a CA-06; CUI-01 a CUI-07 | Pendiente |
| T-07 | Cobertura, evidencia y revisión del alcance completadas | Calidad | T-06 y dependencias reales disponibles | Todos los criterios del alcance | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Al iniciar una tarea cuya dependencia no esté disponible, registrar el bloqueo y su responsable.

## 2. Detalle de tareas

### T-01. Verificar la base compartida del frontend

- [ ] Implementada y verificada.

- Incremento del plan: soporte de I-01.
- Responsable: coordinación de Valqui con Rhamses y Max según el reparto existente.
- Objetivo y alcance: revisar tema, tokens, proveedores, dependencias y scripts existentes; coordinar herramientas de pruebas sin reinicializar el monorepositorio.
- Entradas: componentes React §4.5.1 y DT-04 del plan.
- Dependencias: ninguna.
- Verificación: ambas aplicaciones pasan `npm run typecheck` y `npm run build`.
- Condición de cierre: herramientas, comandos y resultados reales registrados.
- Evidencia: pendiente; completar enlace a EV-02 en evidence.md y commit o PR.
- Bloqueo, si existe: ninguno identificado.

### T-02. Verificar los componentes requeridos

- [ ] Implementada y verificada.

- Incremento del plan: I-01.
- Responsable: Valqui coordina con los responsables de CR según §4.5.
- Objetivo y alcance: confirmar el modal de confirmación, tabla, badges y avisos, sus exportaciones y evidencia; enlazar los trabajos de sus responsables sin duplicar componentes.
- Entradas: componentes React §3 y §4.5.
- Dependencias: T-01.
- Verificación: los componentes se consumen desde el paquete compartido y sus criterios aplicables cuentan con pruebas; ambas aplicaciones siguen compilando.
- Condición de cierre: registrar componentes/revisiones disponibles y pendientes.
- Evidencia: pendiente; completar enlace a EV-02 y EV-03.
- Bloqueo, si existe: dependencias de cada CR.

### T-03. Componer la confirmación con fixtures

- [ ] Implementada y verificada.

- Incremento del plan: I-01.
- Responsable: Valqui.
- Objetivo y alcance: integrar la confirmación en el catálogo; advertencia de desactivación, estados de proceso, éxito, sin cambio y conflicto según UI-01.
- Entradas: [ui.md](./ui.md), componentes verificados y fixtures que distingan activación, desactivación, conflicto y sin cambio.
- Dependencias: T-02.
- Verificación: CUI-01 a CUI-07 con pruebas de interacción y recorrido responsive.
- Condición de cierre: documentar los límites de la simulación y los destinos aún no disponibles.
- Evidencia: pendiente; completar enlace a EV-03.
- Bloqueo, si existe: disponibilidad de componentes.

### T-04. Concretar el contrato central del cambio de estado

- [ ] Implementada y verificada.

- Incremento del plan: habilita I-02/03.
- Responsable: Valqui con Backend/Frontend y Arquitectura.
- Objetivo y alcance: resolver DT-01 en `integraciones/api-contract.md`: parámetro de estado, formato del `409` (solapamiento y versión) e idempotencia; enlazarlo desde los documentos consumidores.
- Entradas: contrato §9.1 y §14 y [spec.md](./spec.md).
- Dependencias: revisión posterior a DT-01.
- Verificación: revisión de solicitudes/respuestas representativas para CA-01 a CA-06, sin crear un segundo contrato.
- Condición de cierre: decisión y revisión enlazadas. Esta tarea no se ejecuta en la preparación documental actual.
- Evidencia: pendiente.
- Bloqueo, si existe: cierre de DT-01.

### T-05. Implementar y probar el cambio de estado backend

- [ ] Implementada y verificada.

- Incremento del plan: I-02.
- Responsable: Valqui con Backend.
- Objetivo y alcance: controlador, caso de uso, puertos y adaptadores mínimos dentro de la funcionalidad `zonas/`; idempotencia por estado, detección de solapamiento en activación y control de versión transaccional.
- Entradas: contrato cerrado, datos de zonas, despachos y distritos, base de seguridad y errores disponible; reglas de [spec.md](./spec.md).
- Dependencias: T-04 y base JWT/errores de DT-03.
- Verificación: `./mvnw.cmd test` desde Gestión; PostgreSQL aislado; activación sin conflicto; conflicto de solapamiento; desactivación con despachos existentes; repetición idempotente sin auditoría duplicada; dos solicitudes concurrentes; autorización con rol distinto.
- Condición de cierre: CA-01 a CA-06 cubiertos en backend; la auditoría se coordina con ES-F01-08.
- Evidencia: pendiente; completar enlace a EV-01.
- Bloqueo, si existe: contrato, control de versión y base pendientes.

### T-06. Conectar el frontend a la API real

- [ ] Implementada y verificada.

- Incremento del plan: I-03.
- Responsable: Valqui.
- Objetivo y alcance: enviar el cambio de estado, refrescar la fila con el resultado y manejar conflicto, sin cambio y permisos; retirar la fuente simulada del recorrido real.
- Entradas: I-01, I-02 y contrato cerrado.
- Dependencias: T-03 y T-05; autenticación humana y Gateway disponibles.
- Verificación: activación y desactivación reales, conflicto explicado, repetición avisada como sin cambio; `npm run typecheck` y `npm run build`.
- Condición de cierre: resultado real por Gateway enlazado.
- Evidencia: pendiente; completar enlace a EV-04.
- Bloqueo, si existe: Gateway y contrato.

### T-07. Verificar y entregar la especificación

- [ ] Implementada y verificada.

- Incremento del plan: cierre.
- Responsable: Valqui con coordinación de Gerardo.
- Objetivo y alcance: ejecutar las comprobaciones de todos los criterios, completar [evidence.md](./evidence.md) y actualizar trazabilidad e índice.
- Entradas: T-05, T-06 y el resto de la carpeta.
- Dependencias: T-06 y dependencias reales disponibles.
- Verificación: registrar commits frontend/backend, entorno y dependencias; revisar teclado, móvil y ausencia de datos de otros módulos.
- Condición de cierre: revisión funcional y técnica registrada; explicar cualquier dependencia pendiente.
- Evidencia: pendiente; completar EV-01 a EV-04.
- Bloqueo, si existe: criterios sin comprobar.

## 3. Cobertura de criterios

| Criterio funcional o de UI | Tareas que lo implementan | Tarea o comprobación que lo verifica | Evidencia |
|---|---|---|---|
| CA-01 | T-02, T-03, T-05, T-06 | T-05 y T-07 | EV-01, EV-04 |
| CA-02 | T-03, T-05, T-06 | T-05 y T-07 | EV-01, EV-04 |
| CA-03 | T-03, T-05, T-06 | T-05 y T-07 | EV-01, EV-04 |
| CA-04 | T-03, T-05, T-06 | T-05 y T-07 | EV-01, EV-04 |
| CA-05 | T-03, T-05, T-06 | T-05 y T-07 | EV-01, EV-04 |
| CA-06 | T-02, T-03, T-05, T-06 | T-05 y T-07 | EV-01 a EV-04 |
| CUI-01 | T-03, T-06 | T-03 y T-07 | EV-03, EV-04 |
| CUI-02 | T-03, T-06 | T-03 y T-07 | EV-03, EV-04 |
| CUI-03 | T-03, T-06 | T-03 y T-07 | EV-03, EV-04 |
| CUI-04 | T-03, T-06 | T-03 y T-07 | EV-03, EV-04 |
| CUI-05 | T-03, T-06 | T-03 y T-07 | EV-03, EV-04 |
| CUI-06 | T-03, T-06 | T-03 y T-07 | EV-02 a EV-04 |
| CUI-07 | T-03, T-06 | T-03 y T-07 | EV-03, EV-04 |

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están implementadas y verificadas.
- [ ] Los criterios tienen evidencia reproducible y las limitaciones están documentadas.
- [ ] Las simulaciones e integraciones pendientes se identifican expresamente.
- [ ] Los documentos y el índice están actualizados y la revisión está enlazada.

## 5. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-06 [cite: 1].
2. [Plan](./plan.md), incrementos I-01 a I-03 y pendientes DT-01 a DT-06 [cite: 2].
3. [UI](./ui.md), criterios CUI-01 a CUI-07, y [evidencia](./evidence.md) [cite: 3].
