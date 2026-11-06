# Tareas de ES-F04-07: Recibir en el centro y resolver un recojo

**Responsable:** Max Rojas

**Estado:** Pendiente de implementación

**Plan de origen:** [plan.md](./plan.md)

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Lista y acciones | Backend, I-01 | ES-F03-09 T-03 | CA-01 a CA-05, CA-07 | Pendiente |
| T-02 | Liberación durable | Backend, I-02 | T-01 | CA-02, CA-06 | Pendiente |
| T-03 | Vista y modales | Frontend, I-03 | T-01 | CUI-01 a CUI-03 | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`.

## 2. Detalle de tareas

### T-01. Implementar lista y acciones

- [ ] Implementada y verificada.
- Verificación: CA-01 a CA-05 y CA-07.
- Evidencia: EV-01.

### T-02. Liberar la capacidad

- [ ] Implementada y verificada.
- Verificación: CA-02 y CA-06.
- Evidencia: EV-01.

### T-03. Construir la vista

- [ ] Implementada y verificada.
- Verificación: CUI-01 a CUI-03.
- Evidencia: EV-02.

## 3. Cobertura de criterios

| Criterio | Implementan | Verifican | Evidencia |
|---|---|---|---|
| CA-01, CA-03 a CA-05, CA-07 | T-01 | T-01 | EV-01 |
| CA-02, CA-06 | T-01, T-02 | T-02 | EV-01 |
| CUI-01 a CUI-03 | T-03 | T-03 | EV-02 |

## 4. Cierre

- [ ] Todas las tareas implementadas y verificadas.
- [ ] Simulaciones e integraciones pendientes identificadas.
- [ ] Revisión enlazada.
