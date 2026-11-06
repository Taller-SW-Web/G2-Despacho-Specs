# Plan de ES-F02-04: Asignar despacho a un repartidor

**Responsable:** Tarqui.

**Estado:** Plan técnico documental preparado el 16/10/2026; implementación y verificación pendientes.

**UI:** Aplica; modal interactivo de asignación en `/programacion`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-07 | Especificación atómica SDD. |
| UI | [ui.md](./ui.md), UI-01 a UI-04, CUI-01 a CUI-06 | Especificación de interfaz modal. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-03, RF-06 | Especificación funcional vigente. |
| Contrato de API | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) y [api-contract-operacion-reparto.md §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación) | Endpoints de asignación y reserva de capacidad. |
| Componentes React | [componentes-react.md](../../disenio/componentes-react.md), CR-01, CR-02, CR-11, CR-12, CR-20 | Contratos de Mantine compartidos. |

## 2. Estrategia y responsabilidades

La asignación involucra una transacción distribuida ligera o de dos pasos entre `servicio-gestion-despachos` y `servicio-operacion-reparto`. Primero, Gestión solicita a Operación la reserva de capacidad en la furgoneta mediante una clave de idempotencia única generada para esta asignación; si Operación valida que hay espacio libre en peso, volumen y paquetes, confirma la reserva. Luego, Gestión actualiza el despacho a `ASIGNADO`, asigna la posición secuencial y registra la auditoría. Si la transacción en Gestión falla, se ejecuta una llamada de compensación a Operación para liberar la reserva técnica.

**Conciliación del 05/11/2026:** el backend existente usa `AsignarDespacho`, `ProgramacionPersistencia`, `CapacidadProgramacionHttp` y `RecuperacionProgramacion`. La intención, la confirmación y la compensación son durables; HTTP queda fuera de las transacciones locales. Antes de compensar se consulta una posible confirmación concurrente o respuesta perdida. Las integraciones PostgreSQL siguen bloqueadas por falta de Docker en esta sesión; esta descripción no acredita su resultado.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| Frontend | Modal, proyección de barras, selección de repartidor y mutación. | `ModalAsignacionDespacho.tsx`, `useAsignarDespacho`. |
| API / Web | Endpoint `POST /api/v1/despachos/{idDespacho}/asignacion`. | `AsignacionController`, `AsignarDespachoRequestDTO`. |
| Aplicación | Orquestación transaccional con F-06, control de versión `@Version`. | `AsignarDespachoUseCase`, `CompensacionReservaService`. |
| Dominio | Cálculo de siguiente secuencia, transición a `ASIGNADO`. | `Despacho`, `SecuenciaRuta`. |
| Infraestructura | Cliente HTTP interno hacia Operación §5.1 y persistencia JPA. | `OperacionCapacidadClient`, `DespachoRepository`, `AuditoriaRepository`. |

## 3. Frontend y componentes React

- El modal se abre controlado por estado en `PaginaProgramacion`.
- Consume el endpoint `GET /api/v1/repartidores/disponibles` (provisto por Operación / F-06) para pintar la lista con `TarjetaRepartidor` (CR-20).
- La proyección de carga suma localmente los datos del despacho (`pesoKg`, `volumenM3`, `cantidadPaquetes = 1`) sobre los balances actuales del repartidor y renderiza `BarraOcupacion` (CR-11).
- Si alguna barra supera el 100%, la tarjeta se deshabilita y se muestra advertencia.
- Actualización del hito: `ModalAsignacion.tsx` consume placa, límites y ocupación ya definidos en [Operación §4.2](../../integraciones/api-contract-operacion-reparto.md#42-jornadas-y-monitoreo). La proyección se muestra en el candidato seleccionado y en los candidatos con sobrecarga para explicar su bloqueo; el remanente sigue determinando la compatibilidad visual. No se fabrican totales si falta información ni se utiliza la UI como autoridad de reserva.

## 4. Backend, persistencia e integraciones

- **Endpoint:** `POST /api/v1/despachos/{idDespacho}/asignacion`.
- **Payload:** `{ "idRepartidor": "REP-0012", "idJornada": "JOR-20260923-0012", "observacion": "Texto opcional" }`.
- **Validaciones previas:**
  - Despacho en `PENDIENTE_ASIGNACION`.
  - `fechaProgramada <= LocalDate.now("America/Lima")`.
- **Llamada a Operación (F-06):**
   - Usar la reserva canónica de [Operación §5.1](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación), incluida su cabecera de idempotencia; no mantener un segundo payload en este plan.
- **Cálculo de secuencia:**
   - Usar el máximo histórico de `secuencia_ruta` para `asignacion_diaria_id_externa` y agregar uno; no reutilizar la posición de una parada ya iniciada o cerrada por filtrar solo `ASIGNADO`.
- **Persistencia en Gestión:**
  - Transición a `ASIGNADO`, seteo de repartidor, jornada, secuencia, observaciones y marca temporal.
  - Registro en `historial_estados_despacho` con usuario gestor.
- **Compensación:** usar la liberación canónica de [Operación §5.2](../../integraciones/api-contract-operacion-reparto.md#52-gestión-libera-una-reserva-en-operación) con motivo de compensación, conservando referencia de reserva e intención recuperable. No existe un DELETE alternativo. Reintentar la misma intención sin duplicar reservas y comprobar primero si la asignación ya quedó confirmada.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Cliente interno hacia Operación §5.1 con mock/WireMock. | Contrato de Operación §5.1. | CA-01, CA-02, CA-03. |
| I-02 | Caso de uso de asignación transaccional con bloqueo optimista y secuencia. | I-01, esquema JPA `despachos`. | CA-01, CA-04, CA-05, CA-06. |
| I-03 | Controlador REST y seguridad JWT `GESTOR_DESPACHO`. | I-02. | CA-07. |
| I-04 | Modal React con selección de repartidor y barras de ocupación proyectadas. | I-03, componentes Mantine CR. | CUI-01 a CUI-06. |

## 6. Estrategia de verificación

- Pruebas unitarias con JUnit 5 simulando respuestas de Operación (reserva exitosa, 422 por sobrecarga de paquetes, 409 por saturación).
- Pruebas de concurrencia simulando dos peticiones simultáneas sobre el mismo despacho para verificar rechazo por `@Version` (HTTP 409).
- Verificación de compensación: inyección de fallo de base de datos en Gestión tras la reserva en Operación para constatar la liberación.
- Pruebas de integración de interfaz con React Testing Library verificando cálculo visual de barras proyectadas y bloqueo de botón.
