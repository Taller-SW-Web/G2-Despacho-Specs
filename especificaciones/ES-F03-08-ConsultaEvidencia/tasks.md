# Tareas de ES-F03-08: Consulta autorizada de la evidencia

**Responsable:** Max Rojas

**Estado:** Pendiente de implementación

**Plan de origen:** [plan.md](./plan.md)

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Visor con fixtures | Frontend, I-01 | DT-02 | CUI-01 a CUI-04 | Pendiente |
| T-02 | Autorización y firma en backend | Backend, I-02 | DT-01, DT-03, ES-F03-05 T-03 | CA-01 a CA-03 | Pendiente |
| T-03 | Visor conectado al backend y almacenamiento reales | Integración, I-03 | T-01, T-02 | CA-01 a CA-03; CUI-01 a CUI-04 | Pendiente |
| T-04 | Evidencia y revisión completadas | Calidad | T-03 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`.

El contrato ya está definido en Operación §3.4; no requiere tarea de cierre.

## 2. Detalle de tareas

### T-01. Construir el visor con fixtures

- [ ] Implementada y verificada.
- Alcance: UI-01 y estados de [ui.md](./ui.md).
- Verificación: CUI-01 a CUI-04 en móvil y escritorio.
- Evidencia: EV-02.

### T-02. Implementar autorización y firma

- [ ] Implementada y verificada.
- Alcance: RN-01 a RN-04 conforme a §3.4.
- Verificación: URL para propietario y Gestor; `403` para otro repartidor y otro rol; renovación con nueva autorización.
- Evidencia: EV-01.

### T-03. Integrar con servicios reales

- [ ] Implementada y verificada.
- Alcance: reemplazar fixtures por backend y almacenamiento reales.
- Verificación: acceso sin firma, firma alterada y enlace vencido denegados.
- Evidencia: EV-03.

### T-04. Verificar y entregar

- [ ] Implementada y verificada.
- Alcance: ejecutar todas las comprobaciones y completar [evidence.md](./evidence.md).
- Evidencia: EV-01 a EV-03.

## 3. Cobertura de criterios

| Criterio | Implementan | Verifican | Evidencia |
|---|---|---|---|
| CA-01 | T-01, T-02, T-03 | T-02, T-04 | EV-01, EV-03 |
| CA-02 | T-02, T-03 | T-03, T-04 | EV-03 |
| CA-03 | T-01, T-02 | T-02, T-04 | EV-01, EV-02 |
| CUI-01 a CUI-04 | T-01, T-03 | T-01, T-04 | EV-02, EV-03 |

## 4. Cierre

- [ ] Todas las tareas implementadas y verificadas.
- [ ] Simulaciones e integraciones pendientes identificadas.
- [ ] Revisión enlazada.
