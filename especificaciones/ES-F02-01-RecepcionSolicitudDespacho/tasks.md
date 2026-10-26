# Tareas de ES-F02-01: Recepción de solicitudes de despacho

**Responsable de coordinación:** Tarqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

Actualización del 26/10/2026: se mantienen T-01 a T-08 y se amplía su alcance a CA-08 a CA-10. Homologación externa, revisión del backend y recorrido real continúan pendientes [cite: 1].

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de API y DTOs de recepción documentados y validados sintácticamente. | Contrato / API | [api-contract.md §7.1](../../integraciones/api-contract.md#71-crear-un-despacho-para-un-pedido-listo-para-entrega) | CA-03 | Completada |
| T-02 | Filtro de seguridad JWT con verificación de scope `despachos:crear`. | Seguridad / Backend | Configuración base JWT | CA-07 | Pendiente |
| T-03 | Mecanismo de idempotencia por `idPedido` y por `Idempotency-Key`. | Backend / Datos | Esquema base PostgreSQL | CA-04 | Pendiente |
| T-04 | Adaptador de resolución de zona activa y cálculo de plazo con F-01. | Integración interna | Servicio de F-01 | CA-02 | Pendiente |
| T-05 | Cliente HTTP físico con integridad, estados y traducción diferenciada. | Integración externa | Contrato homologado, selección de adaptador y WireMock | CA-05, CA-06, CA-08 a CA-10 | Pendiente |
| T-06 | Caso de uso `CrearDespachoUseCase` con cálculos físicos y fecha programada. | Backend / Dominio | T-03, T-04, T-05 | CA-01 | Pendiente |
| T-07 | Persistencia transaccional del despacho y registro de auditoría (RT-02). | Backend / Persistencia | T-06 | CA-01 | Pendiente |
| T-08 | Pruebas controladas y recorrido real G2 → G6, identificados por separado. | Calidad | T-01 a T-07, homologación y grant G7 | CA-01 a CA-10 | Pendiente |

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
- Comprobar que una repetición reconocida no vuelve a consultar G6, aunque el producto haya cambiado después; mantener la unicidad frente a recepciones concurrentes nuevas.

### T-04. Integrar resolución de zona con F-01
- Alcance: invocar `ZonaService.resolverZonaPorUbicacion(distrito, codigoPostal)`. Si la zona está inactiva o no existe, lanzar excepción de negocio `SinCoberturaException`.
- Comprobación: destino sin zona activa responde 422 con código `DESP_ERROR_SIN_COBERTURA`.

### T-05. Implementar cliente hacia Productos y Ofertas

- Alcance: usar la operación canónica de [contrato §5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas), conservar cantidades y rechazar más de 100 únicos. Compartir transporte/validador con F-01; revisar `productosProgramacion`, `CatalogoProductosStub`, `@Primary` y perfiles en el backend. Obtener token propio y aplicar la matriz de errores por código/HTTP.
- Dependencia: publicar y homologar H-G2-01/02/03, incluidos `BORRADOR` y el campo de SKU afectados; fijar revisión del OpenAPI. La prueba con doble puede prepararse antes, registrando el límite.
- Comprobación: contexto de aplicación y WireMock con llamada real a la ruta exacta; `200` íntegro, inexistencia, `422` de negocio, `503` técnico y `502` por respuesta inválida. Casos de omisión, duplicación, inesperados, perfil/marca temporal malformados, 1/100/101 únicos, cantidades agrupadas y estados homologados. No aplicar la elegibilidad de cotización al pedido pagado.

### T-06. Desarrollar caso de uso CrearDespachoUseCase
- Alcance: orquestar cálculos de peso, volumen, paquetes fijado en 1 y cálculo de fecha programada según calendario. Generar códigos `DSP-` y `TRK-`.
- Comprobación: pruebas unitarias con JUnit 5.

### T-07. Persistencia transaccional y auditoría
- Alcance: `@Transactional` guardando en `despachos` e invocando `AuditoriaService.registrarCreacion()`.
- Comprobación: verificación de rollback si la persistencia falla.
- No escribir `cotizaciones` ni exigir un registro previo; G6 se consulta antes de la transacción local. Comparar ausencia de filas parciales en despacho/historial y ausencia de cambios en cotizaciones ante todos los rechazos.

### T-08. Pruebas de integración E2E

- Alcance: verificar CA-01 a CA-10 con PostgreSQL y proveedor controlado; luego recorrer recepción y cotización contra G6 real con revisión homologada y credencial G7 efectiva. Verificar token ausente, inválido/vencido, audiencia incorrecta, scope ausente/correcto y token propio saliente.
- Comprobación: registrar comandos exactos, commits, entorno, reportes y respuesta observada en [evidence.md](./evidence.md); ninguna prueba controlada se informa como E2E real. F-02 no genera una cotización ni reutiliza el perfil histórico de F-01.

[cite: 1] [Contrato externo §11.1](../../integraciones/api-contract.md#111-respuesta-propuesta-y-plan-de-homologación-física-g2g6) y [plan](./plan.md), dependencias de cierre. Las tareas de backend permanecen pendientes.
