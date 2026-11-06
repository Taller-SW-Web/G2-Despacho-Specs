# Tareas de ES-F06-09: Elegir el tipo de operación de la jornada

**Responsable:** Max Rojas

**Estado:** Pendiente de implementación

**Plan de origen:** [plan.md](./plan.md)

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Migración y tipo en jornada | Backend, I-01 | Ninguna | CA-01 a CA-03 | Pendiente |
| T-02 | Disponibilidad, reserva y transferencia | Backend, I-02 | T-01 | CA-04, CA-05 | Pendiente |
| T-03 | Cierre con recojos pendientes | Backend, I-03 | T-01, ES-F03-09 | CA-06 | Pendiente |
| T-04 | Selector y monitoreo | Frontend, I-04 | T-01 | CUI-01, CUI-02 | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`.

## 2. Detalle de tareas

### T-01. Guardar el tipo

- [ ] Implementada y verificada.
- Verificación: jornadas de ambos tipos, compatibilidad y valor no válido.
- Evidencia: EV-01.

### T-02. Aplicar el tipo a disponibilidad y capacidad

- [ ] Implementada y verificada.
- Verificación: lista filtrada, y reserva y transferencia cruzadas rechazadas sin efectos.
- Evidencia: EV-01.

### T-03. Proteger el cierre

- [ ] Implementada y verificada.
- Verificación: `409` con un recojo pendiente y cierre correcto sin pendientes.
- Evidencia: EV-01.

### T-04. Actualizar el panel

- [ ] Implementada y verificada.
- Verificación: CUI-01 y CUI-02.
- Evidencia: EV-02.

## 3. Cobertura de criterios

| Criterio | Implementan | Verifican | Evidencia |
|---|---|---|---|
| CA-01 a CA-03 | T-01, T-04 | T-01 | EV-01 |
| CA-04, CA-05 | T-02 | T-02 | EV-01 |
| CA-06 | T-03 | T-03 | EV-01 |
| CUI-01, CUI-02 | T-04 | T-04 | EV-02 |

## 4. Cierre

- [ ] Todas las tareas implementadas y verificadas.
- [ ] Simulaciones e integraciones pendientes identificadas.
- [ ] Revisión enlazada.
