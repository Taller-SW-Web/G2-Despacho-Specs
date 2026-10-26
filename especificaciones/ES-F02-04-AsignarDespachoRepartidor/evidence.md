# Evidencia de ES-F02-04: Asignar despacho a un repartidor

**Estado:** Backend de Gestión implementado y verificado con PostgreSQL real y Operación simulada por HTTP; proveedor F-06 real y pantalla funcional pendientes.

**Responsable de coordinación:** Tarqui.

**Última ejecución:** 16/10/2026, America/Lima.

## 1. Versión y entorno verificados

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md), Gestión §3.2 y Operación §§5.1–5.3.
- Backend: rama `feature/f02-implementacion-specs`, base `316767f`, cambios en el árbol de trabajo.
- Java 21.0.12.1, PostgreSQL 18.6 aislado, Flyway/JPA reales y JWT RS256 firmados con JWKS de prueba.
- Implementación: `AsignarDespacho`, `CapacidadProgramacionHttp`, `Despacho` con `@Version`, intención durable, historial y outbox.
- [Registro del backend](../../../G2-Despacho-Backend/docs/f02-implementacion-especificaciones.md), §§4–8 [cite: 1].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación ejecutada | Resultado |
|---|---|---|---|
| CA-01 | T-02 a T-06 | Reserva con clave propia/carga tridimensional, estado Asignado, versión, última posición, auditoría y comunicaciones durables. | Gestión aprobado con Operación HTTP simulada. |
| CA-02 | T-02, T-06 | Rechazos `422` de peso, volumen y paquetes mantienen el despacho pendiente; respuesta distingue la variable cuando Operación la informa. | Aprobado con rechazos inducidos del proveedor. |
| CA-03 | T-02, T-06 | Rechazo operativo `409`, sin transición ni otra reserva. | Aprobado con Operación simulada. |
| CA-04 | T-03, T-06 | Dos gestores sobre el mismo despacho; cambio de versión después de reservar; posiciones únicas entre despachos concurrentes. | Aprobado con persistencia y concurrencia reales. |
| CA-05 | T-03, T-06 | Fecha futura en Lima se rechaza `409` antes de invocar Operación. | Aprobado localmente. |
| CA-06 | T-02, T-06 | `DESP_ERROR_RESERVA_ANTERIOR_ACTIVA` del proveedor se conserva como `409`, sin asignar. | Aprobado con Operación simulada. |
| CA-07 | T-05, T-06 | `403` sin rol o con token de servicio; `401` sin token según Común §3.5; sin reservar. | Aprobado aplicando el contrato canónico. |
| CUI-01 a CUI-06 | T-07, T-08 | Modal, grupos, barras, confirmación, toast y actualización de cola en la pantalla. | No ejecutado; integración frontend pendiente. |

## 3. Registros ejecutados

- **EV-01:** `ProgramacionHttpTests`: éxito, idempotencia, rechazos y concurrencia; no se mantienen transacciones abiertas durante HTTP.
- Fallo inducido al insertar historial después de reservar: rollback local y compensación. Liberación fallida conserva `COMPENSACION_PENDIENTE`; la recuperación libera la misma reserva sin volver a reservar.
- Respuesta perdida después de reservar: intención y carga originales persistidas, recuperación con la misma clave y una sola reserva.
- `AsignarDespachoTests`: carrera entre confirmación y compensación; no libera una reserva cuya asignación otra recuperación ya confirmó.
- Outbox: misma identidad del evento en seis envíos, agotamiento de cinco reintentos, proyección versionada y exclusión de eventos comerciales para simulados. Redirección de Ventas no se marca como éxito ni revierte la asignación.
- **EV-02 y EV-03:** pendientes para pantalla funcional/E2E entre servicios reales.
- Suite completa de Gestión: **69 pruebas aprobadas, 0 fallos, 0 errores y 0 omitidas**, empaquetado correcto con `mvnw verify`.

## 4. Ajustes respecto del plan y límites

Se aplican reserva y liberación POST canónicas de Operación, no las rutas antiguas ni el DELETE del plan. Una intención durable y una compensación recuperable cubren respuesta perdida y reinicios; los HTTP se realizan fuera de la transacción local. La secuencia se serializa por jornada y conserva las posiciones ya utilizadas, incluida la parte de la ruta que ya salió del estado Asignado.

Operación es la autoridad de habilitación y capacidad. Las pruebas inducen sus respuestas, no demuestran el cálculo de reservas dentro de F-06 real. La auditoría conserva carga y capacidad remanente confirmadas, sin fabricar límites u ocupaciones no devueltos por el contrato. No se ejecutó una asignación desde la pantalla administrativa ni con credenciales de producción.

## 5. Referencias

1. `G2-Despacho-Backend/docs/f02-implementacion-especificaciones.md`: fuentes, algoritmo recuperable, comandos e informes reproducibles.
