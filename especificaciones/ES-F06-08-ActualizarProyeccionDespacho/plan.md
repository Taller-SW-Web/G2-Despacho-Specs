# Plan de ES-F06-08: Actualizar la proyección operativa del despacho

**Responsable:** Kevin Rhamses Bohorquez. **Estado:** Preparado antes de implementar.

**UI:** No aplica: operación interna sin controles de usuario.

## 1. Entradas y revisiones

- [spec.md](./spec.md), criterios CA-01, CA-02, CA-03, CA-04; F-06 y contrato de Operación sobre Specs `2b92674` como base.
- [Modelo de datos](../../arquitectura/modelo-datos.md), flota F-05 y plantillas SDD.
- Frontend `9151d1a`; backend `841470a`. La evidencia identificará las revisiones finales.

## 2. Estrategia y responsabilidades

Operación concentra reglas de jornada/capacidad, persistencia JDBC y transacciones. Gestión consume reservas, liberaciones y proyecciones mediante sus clientes existentes. Gateway publica únicamente las rutas administrativas y de campo permitidas.

## 3. Frontend y componentes React

No aplica. Las pruebas de contrato usan el cliente consumidor de Gestión; no se agrega una pantalla para credenciales de servicio.

## 4. Backend, persistencia e integraciones

Recibir la versión canónica confirmada por Gestión; conservar destinatario, destino, jornada y reserva para los consumidores de campo. Versiones antiguas/repetidas no reemplazan datos. Validar que la reserva pertenece al despacho y jornada, sin convertir la proyección en dueño del despacho.

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
| CA-01 | Versión nueva válida; comprobar efectos y ausencia de mutaciones ante rechazo | Unitario, HTTP y PostgreSQL aislado según el caso |
| CA-02 | Versión antigua o repetida; comprobar efectos y ausencia de mutaciones ante rechazo | Unitario, HTTP y PostgreSQL aislado según el caso |
| CA-03 | Referencias incompatibles; comprobar efectos y ausencia de mutaciones ante rechazo | Unitario, HTTP y PostgreSQL aislado según el caso |
| CA-04 | Autorización y datos privados; comprobar efectos y ausencia de mutaciones ante rechazo | Unitario, HTTP y PostgreSQL aislado según el caso |

Frontend: tipos, pruebas de interacción y construcción. Backend: unitarias, HTTP con JWT identificado como doble, pruebas PostgreSQL para atomicidad, idempotencia y concurrencia. Nunca usar Supabase para suites que limpian datos. Docker permanece apagado hasta nueva indicación del usuario.

## 7. Decisiones y pendientes

- DT-01: Seguridad real y concesión de scopes pendientes, propietarios de Seguridad; bloquea aceptación desplegada.
- DT-02: comprobar script sobre copia del esquema Supabase antes de aplicar; responsable Kevin, bloquea despliegue de nuevas estructuras.
- DT-03: rendimiento menor de 200 ms y revisión visual humana pendientes; no inferirlos de pruebas con dobles.

## 8. Condiciones para iniciar y cerrar

- [x] Entradas y contrato definidos para comenzar implementación.
- [ ] Pruebas por criterio ejecutadas y trazadas.
- [ ] Revisión humana y dependencias reales verificadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), Soporte a CA-11 y cierre; F-02/F-03 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#53-gestión-comunica-el-estado-confirmado-a-operación) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Tareas](./tasks.md) y [evidencia](./evidence.md).
