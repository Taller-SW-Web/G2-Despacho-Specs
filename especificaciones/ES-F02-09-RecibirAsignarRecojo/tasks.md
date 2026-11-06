# Tareas de ES-F02-09: Recibir y asignar un recojo

**Responsable:** Max Rojas

**Estado:** Pendiente de implementación

**Plan de origen:** [plan.md](./plan.md)

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Recojo de prueba y cola | Backend, I-01 | ES-F03-09 T-02 | CA-01 a CA-03 | Pendiente |
| T-02 | Asignación con reserva | Backend, I-02 | T-01, ES-F06-09 | CA-04 a CA-07 | Pendiente |
| T-03 | Cola y modal | Frontend, I-03 | T-01 | CUI-01 a CUI-03 | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`.

## 2. Detalle de tareas

### T-01. Crear y listar recojos

- [ ] Implementada y verificada.
- Verificación: CA-01 a CA-03.
- Evidencia: EV-01.

### T-02. Asignar recojos

- [ ] Implementada y verificada.
- Verificación: CA-04 a CA-07.
- Evidencia: EV-01.

### T-03. Actualizar el panel

- [ ] Implementada y verificada.
- Verificación: CUI-01 a CUI-03.
- Evidencia: EV-02.

## 3. Cobertura de criterios

| Criterio | Implementan | Verifican | Evidencia |
|---|---|---|---|
| CA-01 a CA-03 | T-01 | T-01 | EV-01 |
| CA-04 a CA-07 | T-02 | T-02 | EV-01 |
| CUI-01 a CUI-03 | T-03 | T-03 | EV-02 |

## 4. Cierre

- [ ] Todas las tareas implementadas y verificadas.
- [ ] Simulaciones e integraciones pendientes identificadas.
- [ ] Revisión enlazada.
