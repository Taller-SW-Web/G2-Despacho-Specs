# Tareas de ES-F03-01: Acceso y habilitación operativa del repartidor

**Responsable:** Max Rojas

**Estado:** Pendiente de implementación

**Plan de origen:** [plan.md](./plan.md)

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Pantalla de acceso y modos de «Mi Ruta» con fixtures | Frontend, I-01 | DT-04 | CUI-01 a CUI-05 | Pendiente |
| T-02 | Contrato de contexto y errores cerrado | Contrato | DT-01, DT-02 | CA-01 a CA-04 | Pendiente |
| T-03 | Autorización, contexto y rechazo `409` en backend | Backend, I-02 | T-02, DT-03, DT-05 | CA-01 a CA-04 | Pendiente |
| T-04 | Frontend conectado al backend real | Integración, I-03 | T-01, T-03 | CA-01 a CA-04; CUI-01 a CUI-05 | Pendiente |
| T-05 | Evidencia y revisión completadas | Calidad | T-04 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`.

## 2. Detalle de tareas

### T-01. Construir acceso y modos con fixtures

- [ ] Implementada y verificada.
- Alcance: pantalla de acceso, guardia de ruta, modo operativo, modo de solo lectura y mensajes de [ui.md](./ui.md).
- Verificación: CUI-01 a CUI-05 en viewport móvil.
- Evidencia: EV-02.

### T-02. Cerrar el contrato

- [ ] Implementada y verificada.
- Alcance: resolver DT-01 y DT-02 en el contrato de operación de reparto; sin crear un contrato paralelo.
- Verificación: solicitudes y respuestas representativas para CA-01 a CA-04.
- Evidencia: enlace a la revisión del contrato.

### T-03. Implementar la autorización en backend

- [ ] Implementada y verificada.
- Alcance: validación del JWT, resolución en F-05, cálculo de habilitación (RN-04) y rechazo `409` (RN-05).
- Verificación: pruebas de seguridad e integración para `401`, `403`, `409` y acceso en turno; identificadores del cliente ignorados.
- Evidencia: EV-01.

### T-04. Integrar con servicios reales

- [ ] Implementada y verificada.
- Alcance: reemplazar fixtures por el contrato real y retirar la fuente simulada.
- Verificación: recorrido completo con datos sintéticos de F-05.
- Evidencia: EV-03.

### T-05. Verificar y entregar

- [ ] Implementada y verificada.
- Alcance: ejecutar todas las comprobaciones y completar [evidence.md](./evidence.md).
- Verificación: commits, entorno y dependencias registrados.
- Evidencia: EV-01 a EV-03.

## 3. Cobertura de criterios

| Criterio | Implementan | Verifican | Evidencia |
|---|---|---|---|
| CA-01 | T-01, T-03, T-04 | T-03, T-05 | EV-01, EV-03 |
| CA-02 | T-01, T-03, T-04 | T-03, T-05 | EV-01, EV-03 |
| CA-03 | T-01, T-03, T-04 | T-03, T-05 | EV-01, EV-03 |
| CA-04 | T-01, T-03, T-04 | T-03, T-05 | EV-01, EV-03 |
| CUI-01 a CUI-05 | T-01, T-04 | T-01, T-05 | EV-02, EV-03 |

## 4. Cierre

- [ ] Todas las tareas implementadas y verificadas.
- [ ] Simulaciones e integraciones pendientes identificadas.
- [ ] Revisión enlazada.
