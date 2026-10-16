# Tareas de ES-F03-07: Cierre de jornada y resumen del día

**Responsable:** Max Rojas

**Estado:** Pendiente de implementación

**Plan de origen:** [plan.md](./plan.md)

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Diálogo, lista y resumen con fixtures | Frontend, I-01 | ES-F03-02 T-01, DT-03 | CUI-01 a CUI-05 | Pendiente |
| T-02 | Contrato de cierre y resumen cerrado | Contrato | DT-01, DT-02, DT-05 | CA-01 a CA-05 | Pendiente |
| T-03 | Cierre manual y resumen en backend | Backend, I-02 | T-02, ES-F03-04 T-03 | CA-01, CA-02, CA-04, CA-05 | Pendiente |
| T-04 | Corte automático | Backend, I-03 | T-03, DT-04, DT-06 | CA-03, CA-05 | Pendiente |
| T-05 | Frontend conectado al backend real | Integración, I-04 | T-01, T-03 | CA-01, CA-02, CA-04; CUI-01 a CUI-05 | Pendiente |
| T-06 | Evidencia y revisión completadas | Calidad | T-04, T-05 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`.

## 2. Detalle de tareas

### T-01. Construir las vistas con fixtures

- [ ] Implementada y verificada.
- Alcance: UI-01 a UI-03 de [ui.md](./ui.md).
- Verificación: CUI-01 a CUI-05.
- Evidencia: EV-02.

### T-02. Cerrar el contrato

- [ ] Implementada y verificada.
- Alcance: resolver DT-01, DT-02 y DT-05.
- Verificación: solicitudes y respuestas representativas para CA-01 a CA-05.
- Evidencia: enlace a la revisión del contrato.

### T-03. Implementar el cierre manual y el resumen

- [ ] Implementada y verificada.
- Alcance: RN-01 a RN-04 y RN-07 a RN-10.
- Verificación: cierre con y sin pendientes, contador sin cambios, reintento sin duplicados y cifras iguales al historial.
- Evidencia: EV-01.

### T-04. Implementar el corte automático

- [ ] Implementada y verificada.
- Alcance: RN-05 y RN-06 con el mismo caso de uso de T-03.
- Verificación: ejecución a la hora configurada con reloj controlado; reejecución sin transiciones adicionales; origen automático en el historial.
- Evidencia: EV-01.

### T-05. Integrar con servicios reales

- [ ] Implementada y verificada.
- Alcance: reemplazar fixtures por el contrato real y F-05.
- Verificación: recorrido completo y paso a solo lectura.
- Evidencia: EV-03.

### T-06. Verificar y entregar

- [ ] Implementada y verificada.
- Alcance: ejecutar todas las comprobaciones y completar [evidence.md](./evidence.md).
- Evidencia: EV-01 a EV-03.

## 3. Cobertura de criterios

| Criterio | Implementan | Verifican | Evidencia |
|---|---|---|---|
| CA-01 | T-01, T-03, T-05 | T-03, T-06 | EV-01, EV-03 |
| CA-02 | T-01, T-03, T-05 | T-03, T-06 | EV-01, EV-03 |
| CA-03 | T-04 | T-04, T-06 | EV-01 |
| CA-04 | T-01, T-03, T-05 | T-03, T-06 | EV-01, EV-03 |
| CA-05 | T-03, T-04 | T-03, T-04 | EV-01 |
| CUI-01 a CUI-05 | T-01, T-05 | T-01, T-06 | EV-02, EV-03 |

## 4. Cierre

- [ ] Todas las tareas implementadas y verificadas.
- [ ] Simulaciones e integraciones pendientes identificadas.
- [ ] Revisión enlazada.
