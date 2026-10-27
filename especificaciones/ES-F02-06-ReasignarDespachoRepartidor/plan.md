# Plan de ES-F02-06: Reasignar despacho a otro repartidor

**Responsable:** Tarqui.

**Estado:** Coordinación durable y modal implementados; regresión e integración G2 verificadas localmente. Aceptación humana pendiente.

## Corrección de integración — 26/10/2026

Las rutas y el orden de llamadas propuestos abajo son históricos. Prevalece [Operación §5.3.1](../../integraciones/api-contract-operacion-reparto.md#531-transferencia-atómica-de-reserva--primitiva-para-es-f02-06): transferencia local atómica con clave durable, no reserva duplicada y liberación separada. El origen se conserva ante rechazo/fallo; la carga proviene de su reserva.

La coordinación se concreta en [Gestión §3.2.2](../../integraciones/api-contract-gestion-despachos.md#322-reasignación-recuperable--es-f02-06). `ReasignarDespacho` prepara una intención en `ReasignacionesPersistencia` (Flyway V6), consulta F-06 fuera de transacción y confirma localmente con historial/outbox/resultado. El cerco durable impide traslado y cambios de posición del despacho mientras la transferencia sea desconocida. No se compensan reservas transferidas: se recupera hacia adelante con la misma clave técnica. Solo un rechazo remoto definitivo retira el cerco sin cambiar la asignación.

La preparación usa el bloqueo `asignacion:<despacho>` compartido con F-03 y la fila/version original. La confirmación adquiere las jornadas origen/destino en orden determinista, compartido con asignación/reordenamiento, y coloca al final del destino sin renumerar el origen. El mismo procesador de programación recupera pendientes; un arrendamiento técnico vencido permite retomar trabajo, pero nunca retira el cerco por sí solo.

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

La transferencia es atómica dentro de F-06. Gestión conserva intención y resultado durables, usa un cerco frente a F-03/reordenamiento y recupera hacia adelante ante timeout, respuesta inválida, reinicio o rollback local. No mantiene transacciones durante HTTP ni declara atomicidad distribuida.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| Frontend | Modal, motivo, métricas reales, recuperación exacta y recarga de rutas. | `ModalReasignacionDespacho.tsx`, `reasignacionApi.ts`, hooks existentes. |
| API / Web | Operación pública de Gestión §3.2.2 con versión y clave. | `ControladorReasignacion`, `SolicitudesProgramacion`. |
| Aplicación | Orquestación fuera de transacción y recuperación durable. | `ReasignarDespacho`, `AlmacenReasignaciones`, `PuertoTransferencia`. |
| Dominio | Reglas de reasignación y preservación de inmutabilidad en estados posteriores. | `Despacho`, `MotivoReasignacionValidador`. |
| Infraestructura | F-06 §5.3.1, cerco, PostgreSQL/JPA e historial/outbox existentes. | `CapacidadProgramacionHttp`, `ReasignacionesPersistencia`, `GuardiaReasignacion`. |

## 3. Frontend y componentes React

- El modal se renderiza condicionalmente cuando se activa el botón "Reasignar" de una parada `ASIGNADO`.
- Reutiliza la disponibilidad validada de F-06 y los hooks existentes. Excluye el conductor/jornada actual y utiliza límites, ocupación y remanente reales para CR-20/CR-11.
- Exige motivo no vacío tras trim, máximo 500; sin mínimo artificial de cinco caracteres. Tras resultado incierto conserva clave, versión y cuerpo y bloquea el descarte/cambio de destino.

## 4. Backend, persistencia e integraciones

- **Endpoint:** `POST /api/v1/despachos/{idDespacho}/reasignacion`.
- **Solicitud/respuesta, permisos y recuperación:** definición única en Gestión §3.2.2.
- **Validaciones en backend:**
  - Despacho en base de datos debe estar en estado estricto `ASIGNADO`. Si está en `EN_CAMINO`, `ENTREGADO` o `FALLIDO`, responder `409 Conflict`.
  - `idNuevoRepartidor != idRepartidorActual`.
  - `motivo != null && !motivo.trim().isEmpty()`.
- **Interacción con Operación (F-06):**
  - Transferencia atómica y repetible de Operación §5.3.1; la clave técnica es el ID persistido de la intención.
  - No ejecutar una segunda reserva inicial ni una liberación/compensación separada.
- **Persistencia en Gestión:**
  - Referencias reales `repartidor_id_externo`, `asignacion_diaria_id_externa`, `reserva_capacidad_id_externa` y `secuencia_ruta`, con `@Version`.
  - `MAX(secuencia_ruta)+1` serializado por jornada; mantener los espacios históricos del origen.
  - Historial `REASIGNACION` con ambos repartidores/jornadas/reservas, posiciones, motivo, carga, remanente confirmado y UTC; proyección versionada sin evento comercial de cambio de estado.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Caso de uso de transferencia de capacidad con cliente de Operación simulado. | Contrato Operación §5.1. | CA-01, CA-03, CA-05. |
| I-02 | Controlador REST con validaciones de motivo, estado ASIGNADO y concurrencia. | I-01, Spring Security JWT. | CA-02, CA-04, CA-06, CA-07. |
| I-03 | Modal React con selección de candidato, barras proyectadas y validación visual. | I-02, componentes Mantine. | CUI-01 a CUI-05. |

## 6. Estrategia de verificación

- `ReasignacionHttpTests` con PostgreSQL y HTTP de proveedor controlado: estados, idempotencia, cerco, concurrencia, rollback, timeout y recuperación con una instancia nueva del coordinador.
- Pruebas de integración con MockMvc evaluando validaciones de motivo y respuestas 400, 409 y 422.
- Verificación de recuperación hacia adelante tras una transferencia aceptada y fallo local, sin liberar/recrear reservas.
- Pruebas de UI con Testing Library comprobando que el chofer actual no aparece en la lista de candidatos.
