# Tareas de ES-F03-09: Recojo de una devolución en el domicilio

**Responsable:** Max Rojas

**Estado:** Pendiente de implementación

**Plan de origen:** [plan.md](./plan.md)

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contratos y decisiones cerrados | Contrato | DT-01 a DT-04 | Todos | Pendiente |
| T-02 | Migraciones de Gestión y Operación | Datos, I-01 | T-01 | CA-03, CA-05, CA-11 | Pendiente |
| T-03 | Estados, historial y eventos del recojo | Backend Gestión, I-02 | T-02 | CA-05, CA-06, CA-09, CA-11 | Pendiente |
| T-04 | Ruta, comandos, evidencia, reserva y cierre | Backend Operación, I-03 | T-03, ES-F06-09 | CA-01 a CA-03, CA-05 a CA-07, CA-09, CA-10, CA-12 | Pendiente |
| T-05 | Pantallas con API simulada | Frontend, I-04 | T-01 | CUI-01 a CUI-07 | Pendiente |
| T-06 | Frontend conectado a servicios reales | Integración, I-05 | T-04, T-05, ES-F02-09, ES-F04-07 | CA-01 a CA-12 | Pendiente |
| T-07 | Evidencia y revisión completadas | Calidad | T-06 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`.

## 2. Detalle de tareas

### T-01. Cerrar contratos y decisiones

- [ ] Implementada y verificada.
- Alcance: revisar los contratos propuestos y resolver DT-01 a DT-04.
- Verificación: solicitudes y respuestas de ejemplo para CA-01 a CA-12.
- Evidencia: enlace a la revisión.

### T-02. Crear las migraciones

- [ ] Implementada y verificada.
- Alcance: tablas y cambios del [modelo §3.6](../../arquitectura/modelo-datos.md#36-recojos-de-devoluciones).
- Verificación: aplicar en una base desechable; los datos actuales no cambian.
- Evidencia: EV-01.

### T-03. Implementar el recojo en Gestión

- [ ] Implementada y verificada.
- Alcance: transiciones, contador, catálogo por ámbito, historial, eventos y copia hacia Operación.
- Verificación: transiciones válidas e inválidas, motivo no permitido y reintento sin duplicados.
- Evidencia: EV-01.

### T-04. Implementar el recojo en Operación

- [ ] Implementada y verificada.
- Alcance: `mi-ruta`, detalle, comandos, evidencia, liberación de reserva, cierre de jornada y resumen.
- Verificación: CA-01 a CA-03, CA-05 a CA-07, CA-09, CA-10 y CA-12; el despacho original sigue `ENTREGADO`.
- Evidencia: EV-01.

### T-05. Construir las pantallas

- [ ] Implementada y verificada.
- Alcance: UI-01 a UI-05, estados y mensajes de [ui.md](./ui.md).
- Verificación: CUI-01 a CUI-07.
- Evidencia: EV-02.

### T-06. Integrar con servicios reales

- [ ] Implementada y verificada.
- Alcance: reemplazar la API simulada por backend y Storage reales.
- Verificación: recorrido asignación → recojo → recepción, y asignación → no recojo → decisión del Gestor.
- Evidencia: EV-03.

### T-07. Verificar y entregar

- [ ] Implementada y verificada.
- Alcance: ejecutar todas las comprobaciones y completar [evidence.md](./evidence.md).
- Evidencia: EV-01 a EV-03.

## 3. Cobertura de criterios

| Criterio | Implementan | Verifican | Evidencia |
|---|---|---|---|
| CA-01 | T-04, T-05 | T-04, T-07 | EV-01, EV-02, EV-03 |
| CA-02 | T-04, T-05 | T-04, T-07 | EV-01, EV-02, EV-03 |
| CA-03 | T-02, T-04, T-05 | T-04, T-07 | EV-01, EV-03 |
| CA-04 | T-05 | T-05, T-07 | EV-02 |
| CA-05 | T-02 a T-05 | T-03, T-04, T-07 | EV-01, EV-03 |
| CA-06 | T-03, T-04, T-05 | T-03, T-05, T-07 | EV-01, EV-02 |
| CA-07 | T-04, T-05 | T-04, T-07 | EV-01, EV-02 |
| CA-08 | T-05 | T-05, T-07 | EV-02 |
| CA-09 | T-03, T-04 | T-03, T-04, T-07 | EV-01 |
| CA-10 | T-04, T-05 | T-04, T-07 | EV-01, EV-02 |
| CA-11 | T-02, T-03 | T-03, T-07 | EV-01 |
| CA-12 | T-04, T-05 | T-04, T-05, T-07 | EV-01, EV-02 |
| CUI-01 a CUI-07 | T-05, T-06 | T-05, T-07 | EV-02, EV-03 |

## 4. Cierre

- [ ] Todas las tareas implementadas y verificadas.
- [ ] Simulaciones e integraciones pendientes identificadas.
- [ ] Revisión enlazada.
