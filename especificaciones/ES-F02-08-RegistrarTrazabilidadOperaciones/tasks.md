# Tareas de ES-F02-08: Registrar la trazabilidad de las operaciones

**Responsable de coordinación:** Tarqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Definición de tabla `historial_estados_despacho` y campos de auditoría. | Base de datos | modelo-datos.md §3.1 | CA-01 | Completada |
| T-02 | Entidad JPA `HistorialEstadoDespacho` y repositorio Spring Data de solo inserción. | Backend / Datos | T-01 | CA-01, CA-06 | Pendiente |
| T-03 | Componente transversal `AuditoriaService` con captura de usuario y UTC. | Backend / Aplicación | T-02 | CA-01 a CA-05 | Pendiente |
| T-04 | Integración en casos de uso de F-02 (recepción, asignación, reordenamiento, etc.). | Backend / Dominio | T-03 | CA-01 a CA-05 | Pendiente |
| T-05 | Pruebas de integración de persistencia y atomicidad transaccional. | Calidad / Backend | T-04 | CA-06 | Pendiente |

## 2. Detalle de tareas

### T-01. Esquema de datos
- Alcance: confirmar estructura de tabla `historial_estados_despacho` con columnas de estado, usuario, fecha y metadatos JSONB.
- Comprobación: esquema revisado.

### T-02. Entidad y repositorio JPA
- Alcance: `HistorialEstadoDespacho` y `HistorialEstadoDespachoRepository` con interfaces solo de lectura e inserción.
- Comprobación: tests de repositorio con `DataJpaTest`.

### T-03. Servicio de auditoría
- Alcance: métodos `registrarRecepcion()`, `registrarAsignacion()`, `registrarReordenamiento()`, `registrarReasignacion()` y `registrarCancelacion()`.
- Comprobación: tests unitarios con JUnit 5.

### T-04. Integración en casos de uso
- Alcance: invocación desde `CrearDespachoUseCase`, `AsignarDespachoUseCase`, etc., dentro del bloque `@Transactional`.
- Comprobación: tests de flujo completo.

### T-05. Verificación de atomicidad
- Alcance: tests con inyección de errores verificando rollback completo y ausencia de métodos de actualización.
- Comprobación: 100% de tests aprobados.
