# Plan de ES-F02-08: Registrar la trazabilidad de las operaciones

**Responsable:** Tarqui.

**Estado:** Plan técnico documental preparado el 16/10/2026; implementación y verificación pendientes.

**UI:** No aplica; captura interna transaccional y exposición en detalle de despacho.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-06 | Especificación atómica SDD. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-04, CA-10 | Especificación funcional vigente. |
| Requisito transversal | [overview.md §6](../../overview.md) | RT-02: Trazabilidad y auditoría. |
| Modelo de datos | [modelo-datos.md §3.1](../../arquitectura/modelo-datos.md#31-entidad-despachos) | Esquema de la tabla `historial_estados_despacho`. |

## 2. Estrategia y responsabilidades

Se implementa el servicio de dominio transversal `AuditoriaService` desacoplado, invocado directamente desde cada caso de uso de F-02 dentro de su demarcación `@Transactional`. No se crean tablas duplicadas ni se ejecutan procesos asíncronos para la auditoría esencial: la inserción en `historial_estados_despacho` comparte la conexión y la transacción de base de datos de la entidad `despachos`.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| Dominio | Entidad inmutable `HistorialEstadoDespacho` con métodos factoría. | `HistorialEstadoDespacho`, `TipoOperacionDespacho`. |
| Aplicación | Servicio de auditoría invocado por los casos de uso de F-02. | `AuditoriaService`. |
| Infraestructura | Repositorio Spring Data JPA de solo lectura e inserción (`save` y `findByDespachoIdOrderByFechaAsc`). | `HistorialEstadoDespachoRepository`. |

## 3. Frontend y componentes React

No aplica interfaz nueva ni formulario independiente. La visualización de la trazabilidad capturada por esta especificación se integra en el componente `HistorialEstados` (CR-19) dentro de la vista de detalle del despacho ([api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación)), donde se muestra la línea de tiempo cronológica con fechas, ejecutores y estados.

## 4. Backend, persistencia e integraciones

- **Entidad JPA:** `HistorialEstadoDespacho` mapeada a la tabla `historial_estados_despacho`.
- **Campos:**
  - `id`: UUID (Primary Key).
  - `idDespacho`: UUID / String (Foreign Key a `despachos`).
  - `estadoAnterior`: String nullable.
  - `estadoNuevo`: String obligatorio (`PENDIENTE_ASIGNACION`, `ASIGNADO`, `CANCELADO`, etc.).
  - `idRepartidor`: String nullable (en asignaciones/reasignaciones).
  - `idJornada`: String nullable.
  - `posicionSecuencia`: Entero nullable.
  - `usuarioEjecutor`: String obligatorio (extraído de `SecurityContextHolder`).
  - `tipoEjecutor`: Enum (`USUARIO_GESTOR`, `SISTEMA_VENTAS`, `SISTEMA_OPERACION`).
  - `fechaHoraUtc`: `Instant` obligatorio generado con `Instant.now()`.
  - `observaciones`: String nullable.
  - `metadatosJson`: JSONB para balances de ocupación (kg, m³, paquetes) o secuencias de ruta.
- **Inmutabilidad:** no se implementan métodos `update` ni `delete` en el repositorio JPA ni en servicios.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Entidad JPA y repositorio Spring Data de solo inserción. | Esquema PostgreSQL `historial_estados_despacho`. | CA-01, CA-06. |
| I-02 | Servicio `AuditoriaService` con métodos de registro por tipo de operación de F-02. | I-01, Spring Security context. | CA-01 a CA-05. |
| I-03 | Integración transaccional con casos de uso de F-02 y verificación de rollback. | I-02, casos de uso ES-F02-01 a 07. | CA-06. |

## 6. Estrategia de verificación

- Pruebas unitarias de `AuditoriaService` validando captura de usuario y marcas temporales UTC.
- Pruebas de integración con `DataJpaTest` verificando inserción correcta de registros y consulta cronológica.
- Prueba de atomicidad: inyectar fallo de base de datos en la auditoría y comprobar que el despacho no cambia de estado.
