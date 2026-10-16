# Tareas de ES-F02-01: Recepción de solicitudes de despacho

**Responsable de coordinación:** Tarqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de API y DTOs de recepción documentados y validados sintácticamente. | Contrato / API | [api-contract.md §7.1](../../integraciones/api-contract.md#71-crear-un-despacho-para-un-pedido-listo-para-entrega) | CA-03 | Completada |
| T-02 | Filtro de seguridad JWT con verificación de scope `despachos:crear`. | Seguridad / Backend | Configuración base JWT | CA-07 | Pendiente |
| T-03 | Mecanismo de idempotencia por `idPedido` y por `Idempotency-Key`. | Backend / Datos | Esquema base PostgreSQL | CA-04 | Pendiente |
| T-04 | Adaptador de resolución de zona activa y cálculo de plazo con F-01. | Integración interna | Servicio de F-01 | CA-02 | Pendiente |
| T-05 | Cliente REST de Productos y Ofertas para obtención de datos físicos en lote. | Integración externa | WireMock / Cliente HTTP | CA-05, CA-06 | Pendiente |
| T-06 | Caso de uso `CrearDespachoUseCase` con cálculos físicos y fecha programada. | Backend / Dominio | T-03, T-04, T-05 | CA-01 | Pendiente |
| T-07 | Persistencia transaccional del despacho y registro de auditoría (RT-02). | Backend / Persistencia | T-06 | CA-01 | Pendiente |
| T-08 | Pruebas de integración extremo a extremo con Testcontainers y WireMock. | Calidad | T-01 a T-07 | CA-01 a CA-07 | Pendiente |

## 2. Detalle de tareas

### T-01. Validar DTOs y contrato de API
- Alcance: crear `CrearDespachoRequestDTO` con validaciones `@NotNull`, `@NotBlank`, `@Valid`, `@Positive` y DTO de respuesta.
- Comprobación: pruebas de deserialización JSON y Bean Validation.

### T-02. Configurar seguridad del endpoint
- Alcance: mapear endpoint `POST /api/v1/despachos` a regla de autorización `@PreAuthorize("hasAuthority('SCOPE_despachos:crear')")`.
- Comprobación: peticiones sin token responden 401; tokens sin scope responden 403.

### T-03. Implementar control de idempotencia
- Alcance: comprobación en tabla `despachos` por `id_pedido` antes de procesar y registro en tabla de claves de idempotencia.
- Comprobación: llamadas duplicadas devuelven el despacho existente con 200 OK sin crear nuevos registros.

### T-04. Integrar resolución de zona con F-01
- Alcance: invocar `ZonaService.resolverZonaPorUbicacion(distrito, codigoPostal)`. Si la zona está inactiva o no existe, lanzar excepción de negocio `SinCoberturaException`.
- Comprobación: destino sin zona activa responde 422 con código `DESP_ERROR_SIN_COBERTURA`.

### T-05. Implementar cliente hacia Productos y Ofertas
- Alcance: llamada en lote `POST /api/v1/productos/lote-datos-fisicos`. Manejo de 422 (SKU no encontrado / datos incompletos) y 503 (servicio no disponible).
- Comprobación: WireMock simulando respuestas 200, 422 y 503.

### T-06. Desarrollar caso de uso CrearDespachoUseCase
- Alcance: orquestar cálculos de peso, volumen, paquetes fijado en 1 y cálculo de fecha programada según calendario. Generar códigos `DSP-` y `TRK-`.
- Comprobación: pruebas unitarias con JUnit 5.

### T-07. Persistencia transaccional y auditoría
- Alcance: `@Transactional` guardando en `despachos` e invocando `AuditoriaService.registrarCreacion()`.
- Comprobación: verificación de rollback si la persistencia falla.

### T-08. Pruebas de integración E2E
- Alcance: suite completa con Testcontainers verificando todos los escenarios de CA-01 a CA-07.
- Comprobación: todos los tests pasan en verde.
