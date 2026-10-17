# Plan de ES-F06-05: Cerrar una jornada sin despachos en curso

**Responsable:** Kevin Rhamses Bohorquez. **Estado:** Ejecutado localmente; revisión humana pendiente.

**UI:** Aplica, según ui.md.

## 1. Entradas y revisiones

- [spec.md](./spec.md), criterios CA-01, CA-02, CA-03; F-06 y contrato de Operación sobre Specs `2b92674` como base.
- [Modelo de datos](../../arquitectura/modelo-datos.md), flota F-05 y plantillas SDD.
- Frontend `9151d1a`; backend `841470a`. La evidencia identificará las revisiones finales.

## 2. Estrategia y responsabilidades

Operación concentra reglas de jornada/capacidad, persistencia JDBC y transacciones. Gestión consume reservas, liberaciones y proyecciones mediante sus clientes existentes. Gateway publica únicamente las rutas administrativas y de campo permitidas.

## 3. Frontend y componentes React

Reutilizar CR-03/05/06/07/08/09/10/11/12/15 y completar CR-14. Pantalla /jornadas y monitoreo con formularios y detalle; usar cliente autenticado compartido, consultas cancelables y pruebas con transporte simulado explícito. Conservar filtros en URL y bloquear acciones mientras el resultado sea incierto.

## 4. Backend, persistencia e integraciones

Cerrar y auditar atómicamente. No borrar reservas ni proyecciones. Una jornada ya cerrada devuelve el mismo resultado sin otra auditoría. F-03 debe resolver primero ASIGNADO/EN_CAMINO como NO_INTENTADO; F-06 nunca realiza esa conversión por su cuenta.

Implementar paquete `jornadas` con controladores, servicio, modelos y repositorio JDBC. Reutilizar el bloqueo `bloquear_operacion_flota()` para mantener el orden de F-05. No invocar HTTP manteniendo bloqueos de tablas. Auditoría en la misma transacción. Migración aditiva para índices, compatibilidad de proyecciones y respuestas idempotentes; script separado revisable para Supabase heredado con Flyway desactivado. No ejecutar automáticamente sobre producción.

## 5. Orden de implementación

| Incremento | Resultado | Dependencia |
|---|---|---|
| I-01 | Contrato, UI, tareas y componentes revisados | Fuentes de §1 |
| I-02 | Frontend y pruebas aisladas | I-01 y componentes disponibles |
| I-03 | Backend y clientes conectados | I-01; contrato canónico |
| I-04 | Pruebas cruzadas y evidencia | I-02/I-03; PostgreSQL aislado y Seguridad real para aceptación publicada |

## 6. Estrategia de verificación

| Criterio | Comprobación | Entorno |
|---|---|---|
| CA-01 | Cierre seguro e idempotente; comprobar efectos y ausencia de mutaciones ante rechazo | Unitario, HTTP y PostgreSQL aislado según el caso |
| CA-02 | Pendientes de operación; comprobar efectos y ausencia de mutaciones ante rechazo | Unitario, HTTP y PostgreSQL aislado según el caso |
| CA-03 | Propiedad del repartidor; comprobar efectos y ausencia de mutaciones ante rechazo | Unitario, HTTP y PostgreSQL aislado según el caso |

Frontend: tipos, pruebas de interacción y construcción. Backend: unitarias, HTTP con JWT identificado como doble, pruebas PostgreSQL para atomicidad, idempotencia y concurrencia. Nunca usar Supabase para suites que limpian datos. El usuario confirmó Docker disponible para las pruebas PostgreSQL aisladas.

## 7. Decisiones y pendientes

- DT-01: Seguridad real y concesión de scopes pendientes, propietarios de Seguridad; bloquea aceptación desplegada.
- DT-02: comprobar script sobre copia del esquema Supabase antes de aplicar; responsable Kevin, bloquea despliegue de nuevas estructuras.
- DT-03: rendimiento menor de 200 ms y revisión visual humana pendientes; no inferirlos de pruebas con dobles.

## 8. Condiciones para iniciar y cerrar

- [x] Entradas y contrato definidos para comenzar implementación.
- [ ] Pruebas por criterio ejecutadas y trazadas.
- [ ] Revisión humana y dependencias reales verificadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), CA-12 y CA-13 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#42-jornadas-y-monitoreo) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Tareas](./tasks.md) y [evidencia](./evidence.md).
