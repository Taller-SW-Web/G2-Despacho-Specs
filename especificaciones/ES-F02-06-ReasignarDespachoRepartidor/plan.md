# Plan de ES-F02-06: Reasignar despacho a otro repartidor

**Responsable:** Tarqui.

**Estado:** Plan técnico documental preparado el 16/10/2026; implementación y verificación pendientes.

**UI:** Aplica; modal interactivo de reasignación en `/programacion`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-07 | Especificación atómica SDD. |
| UI | [ui.md](./ui.md), UI-01 a UI-04, CUI-01 a CUI-05 | Especificación de interfaz modal. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-07, CA-15, CA-16 | Especificación funcional vigente. |
| Contrato de API | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) y [api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación) | Endpoints de reasignación y gestión de capacidad. |
| Componentes React | [componentes-react.md](../../disenio/componentes-react.md), CR-01, CR-02, CR-11, CR-12, CR-15, CR-20 | Componentes Mantine compartidos. |

## 2. Estrategia y responsabilidades

La reasignación requiere orquestar con Operación (F-06) la transferencia de la reserva de capacidad vehicular: liberar la reserva en la furgoneta saliente y registrar una nueva reserva en la furgoneta entrante. Para evitar inconsistencias ante fallos intermedios, se utiliza el patrón de reserva previa con clave técnica y posterior confirmación o compensación. En Gestión, la mutación actualiza el repartidor y ubica el despacho al final de la ruta del nuevo conductor de forma atómica bajo bloqueo optimista.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| Frontend | Modal de reasignación, validación de motivo y llamada React Query. | `ModalReasignacionDespacho.tsx`, `useReasignarDespacho`. |
| API / Web | Endpoint `POST /api/v1/despachos/{idDespacho}/reasignacion`. | `ReasignacionController`, `ReasignarDespachoRequestDTO`. |
| Aplicación | Coordinación con F-06, validación de estado `ASIGNADO` y recálculo de secuencia. | `ReasignarDespachoUseCase`. |
| Dominio | Reglas de reasignación y preservación de inmutabilidad en estados posteriores. | `Despacho`, `MotivoReasignacionValidador`. |
| Infraestructura | Cliente interno hacia Operación §5.1 y persistencia JPA en PostgreSQL. | `OperacionCapacidadClient`, `DespachoRepository`, `AuditoriaRepository`. |

## 3. Frontend y componentes React

- El modal se renderiza condicionalmente cuando se activa el botón "Reasignar" de una parada `ASIGNADO`.
- Consume la lista de repartidores en turno mediante el hook `useRepartidoresDisponibles`, filtrando localmente para excluir al conductor actual.
- Valida en tiempo real que el campo `motivo` contenga al menos 5 caracteres no vacíos antes de habilitar el botón primario.

## 4. Backend, persistencia e integraciones

- **Endpoint:** `POST /api/v1/despachos/{idDespacho}/reasignacion`.
- **Payload:** `{ "idNuevoRepartidor": "REP-0018", "idNuevaJornada": "JOR-20260923-0018", "motivo": "Falla de la furgoneta" }`.
- **Validaciones en backend:**
  - Despacho en base de datos debe estar en estado estricto `ASIGNADO`. Si está en `EN_CAMINO`, `ENTREGADO` o `FALLIDO`, responder `409 Conflict`.
  - `idNuevoRepartidor != idRepartidorActual`.
  - `motivo != null && !motivo.trim().isEmpty()`.
- **Interacción con Operación (F-06):**
  - Reserva nueva: `POST /internal/v1/operacion/capacidad/reserva` (evalúa espacio libre tridimensional).
  - Liberación anterior: `POST /internal/v1/operacion/capacidad/liberacion` con la clave de reserva del conductor saliente.
- **Persistencia en Gestión:**
  - Actualizar `id_repartidor = :idNuevoRepartidor`, `id_jornada = :idNuevaJornada`.
  - Posición en secuencia: `SELECT COALESCE(MAX(posicion_secuencia), 0) + 1 FROM despachos WHERE id_jornada = :idNuevaJornada`.
  - Registro de auditoría `REASIGNACION_DESPACHO` con `repartidor_anterior`, `nuevo_repartidor` y `motivo`.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Caso de uso de transferencia de capacidad con cliente de Operación simulado. | Contrato Operación §5.1. | CA-01, CA-03, CA-05. |
| I-02 | Controlador REST con validaciones de motivo, estado ASIGNADO y concurrencia. | I-01, Spring Security JWT. | CA-02, CA-04, CA-06, CA-07. |
| I-03 | Modal React con selección de candidato, barras proyectadas y validación visual. | I-02, componentes Mantine. | CUI-01 a CUI-05. |

## 6. Estrategia de verificación

- Pruebas unitarias de `ReasignarDespachoUseCase` verificando transiciones válidas y rechazos ante despachos `EN_CAMINO`.
- Pruebas de integración con MockMvc evaluando validaciones de motivo y respuestas 400, 409 y 422.
- Verificación de compensación ante error en la liberación o en el guardado de base de datos.
- Pruebas de UI con Testing Library comprobando que el chofer actual no aparece en la lista de candidatos.
