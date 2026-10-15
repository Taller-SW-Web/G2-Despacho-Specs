# ES-FXX-NN: [Nombre del comportamiento]

**Funcionalidad padre:** [F-XX, enlace y requisitos de origen].

**Responsable:** [por completar].

**Estado:** Borrador.

**Actor principal:** [persona, módulo o proceso].

**UI:** [Aplica / No aplica, con motivo].

**Servicio propietario:** [Gestión de Despachos / Operación de Reparto y Flota / otro alcance justificado].

> Plantilla de un comportamiento atómico. Al copiarla, completar los marcadores y ajustar los enlaces. Las rutas y los formatos definitivos pertenecen al contrato de API vigente.

## 1. Contexto y objetivo

[Situación que inicia el comportamiento, necesidad que resuelve y resultado observable. Referenciar la funcionalidad padre y sus requisitos sin repetir su alcance completo.] [cite: 1]

## 2. Alcance

- Incluye: [por completar].
- Fuera de alcance: [por completar y, si corresponde, especificación responsable].

## 3. Actor, precondiciones y resultados

- Actor y autorización: [identidad, rol o scope según el contrato; referencia de sección].
- Precondiciones: [estado del recurso, datos y dependencias necesarias].
- Disparador: [acción o evento que inicia el flujo].
- Resultado exitoso: [estado, datos y efectos externos observables].
- Resultado ante rechazo: [qué se informa y qué permanece sin cambios].

## 4. Flujo principal y alternativas

1. [Acción del actor o proceso].
2. [Validación y decisión del sistema].
3. [Resultado y comunicación al actor].

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| [por completar] | [por completar] | [por completar] | CA-02 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | [Regla del comportamiento, sin decisiones de implementación] | [Referencia y requisito] |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| [Método y ruta / evento / proceso interno] | [por completar] | [Enlace, sección y revisión del contrato] |

Indicar validaciones, permisos, efectos sobre datos y reglas de concurrencia o idempotencia solo si aplican. No inventar campos, scopes ni estados que no estén acordados. Los formatos de entrada, salida y error se consultan en el contrato [cite: 2].

## 6. Criterios de aceptación

### CA-01. [Resultado exitoso]

- **DADO** [contexto y datos de prueba].
- **CUANDO** [acción concreta].
- **ENTONCES** [resultado observable y efectos esperados].

### CA-02. [Alternativa o rechazo]

- **DADO** [condición excepcional].
- **CUANDO** [acción concreta].
- **ENTONCES** [respuesta observable y ausencia de efectos indebidos].

Agregar los escenarios aplicables de autorización, datos inválidos, dependencia no disponible, repetición y concurrencia. Mantener los IDs estables y expresar valores concretos cuando el requisito los defina.

## 7. UI, backend y requisitos no funcionales

- UI: [si aplica, detallar interacción en ui.md; si no, explicar por qué].
- Backend: [responsabilidad funcional y servicio propietario, sin anticipar clases].
- Requisitos no funcionales: [seguridad, tiempos, accesibilidad o auditoría exigidos; valor verificable y fuente].
- Pendientes: [pregunta, responsable y criterio afectado; indicar si bloquea el incremento].

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | [unitaria / integración / UI / manual] | [por completar] |
| CA-02 | [por completar] | [por completar] |

- [ ] Todos los criterios aplicables cuentan con resultados comprobables en `evidence.md`.
- [ ] Los documentos, el contrato y el comportamiento implementado son consistentes.
- [ ] Los pendientes que bloquean el alcance están resueltos y la revisión del equipo está registrada.

## 9. Referencias

1. [Funcionalidad padre: completar enlace, requisitos e historias relacionadas].
2. [Contrato de API: completar enlace, secciones y revisión].
3. [Arquitectura, modelo de datos y estados: completar referencias aplicables].
4. Archivos de esta especificación: [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md). Referenciar `ui.md` únicamente cuando aplique.
