# Tareas de ES-F03-06: Registro de entrega fallida

**Responsable:** Max Rojas

**Estado:** Pendiente de implementación

**Plan de origen:** [plan.md](./plan.md)

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Formulario de incidencia con fixtures | Frontend, I-01 | ES-F03-05 T-01, DT-02 | CUI-01 a CUI-05 | Pendiente |
| T-02 | Contrato de incidencia cerrado | Contrato | DT-01, DT-03, DT-04 | CA-01 a CA-06 | Pendiente |
| T-03 | Incidencia, contador e historial en backend | Backend, I-02 | T-02, ES-F03-05 T-03 | CA-01 a CA-06 | Pendiente |
| T-04 | Frontend conectado al backend real | Integración, I-03 | T-01, T-03 | CA-01 a CA-06; CUI-01 a CUI-05 | Pendiente |
| T-05 | Evidencia y revisión completadas | Calidad | T-04 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`.

## 2. Detalle de tareas

### T-01. Construir el formulario con fixtures

- [ ] Implementada y verificada.
- Alcance: UI-01, estados y mensajes de [ui.md](./ui.md).
- Verificación: CUI-01 a CUI-05.
- Evidencia: EV-02.

### T-02. Cerrar el contrato

- [ ] Implementada y verificada.
- Alcance: resolver DT-01, DT-03 y DT-04.
- Verificación: solicitudes y respuestas representativas para CA-01 a CA-06.
- Evidencia: enlace a la revisión del contrato.

### T-03. Implementar la incidencia

- [ ] Implementada y verificada.
- Alcance: RN-01 a RN-09.
- Verificación: incidencia válida, motivo forzado no seleccionable, `NO_INTENTADO` rechazado, `409` por origen, evidencia inválida y reintento sin duplicar contador.
- Evidencia: EV-01.

### T-04. Integrar con servicios reales

- [ ] Implementada y verificada.
- Alcance: reemplazar fixtures por catálogo, almacenamiento y contrato reales.
- Verificación: recorrido completo y despacho visible para F-04.
- Evidencia: EV-03.

### T-05. Verificar y entregar

- [ ] Implementada y verificada.
- Alcance: ejecutar todas las comprobaciones y completar [evidence.md](./evidence.md).
- Evidencia: EV-01 a EV-03.

## 3. Cobertura de criterios

| Criterio | Implementan | Verifican | Evidencia |
|---|---|---|---|
| CA-01 | T-01, T-03, T-04 | T-03, T-05 | EV-01, EV-03 |
| CA-02 | T-01 | T-01, T-05 | EV-02 |
| CA-03 | T-01, T-03 | T-03, T-05 | EV-01, EV-02 |
| CA-04 | T-01 | T-01, T-05 | EV-02 |
| CA-05 | T-03 | T-03, T-05 | EV-01 |
| CA-06 | T-03 | T-03, T-05 | EV-01 |
| CUI-01 a CUI-05 | T-01, T-04 | T-01, T-05 | EV-02, EV-03 |

## 4. Cierre

- [ ] Todas las tareas implementadas y verificadas.
- [ ] Simulaciones e integraciones pendientes identificadas.
- [ ] Revisión enlazada.
