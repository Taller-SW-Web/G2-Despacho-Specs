# Tareas de ES-F02-01: Recepción de solicitudes de despacho

**Responsable de coordinación:** Tarqui.

**Estado:** Implementación local con validación estricta incorporada; homologación y regresión PostgreSQL pendientes.

**Avance 30/10/2026:** `ProductosProgramacionHttp` y recepción cubren validación del lote, clasificación, fechas/estado y límite de SKU. Cinco pruebas específicas aprobadas con HTTP controlado/dobles; la tabla histórica inferior no equivale a tareas inexistentes ni a aceptación final. CA-09 mantiene BORRADOR bloqueado hasta homologación. Detalle y bloqueo Docker en [evidence.md](./evidence.md).

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

Actualización del 26/10/2026: se mantienen T-01 a T-08 y se amplía su alcance a CA-08 a CA-10. Homologación externa, revisión del backend y recorrido real continúan pendientes [cite: 1].

Actualización del 03/11/2026: H-G2-01/02/03 cerrados y respuesta D publicada; la frase anterior describe el antecedente del 26/10. Se agregan T-09/T-10 para CA-11 a CA-13 y el estado efectivo de CA-09. Implementación, ampliación D-G2-02 y verificación funcional pendientes [cite: 1].

Actualización del 04/11/2026: D-G2-01/02 cerrados semánticamente y proveedor G6 fusionado. Campo, afectados, orden y precedencia aceptados; sincronización normativa y verificación del consumidor pendientes. El cierre del acuerdo no completa las tareas de backend.

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
| T-09 | Traducción pública del SKU padre con afectados validados. | Backend / Integración, I-05 | T-05 y revisión exigible D-G2-02; aceptación resuelta | CA-11 a CA-13 | Pendiente |
| T-10 | Regresiones de estado efectivo, detalle y precedencia bilateral. | Calidad / Integración, I-05 | T-06, T-07, T-09 y revisión D acordada | CA-09, CA-11 a CA-13 | Pendiente |
| T-08 | Pruebas controladas y recorrido real G2 → G6, identificados por separado. | Calidad | T-01 a T-07, T-09/T-10, revisión D y grant G7 | CA-01 a CA-13 | Pendiente |

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
- Dependencia: contrastar el consumidor con H-G2-01/02/03 ya cerrados y el OpenAPI rc.3 fijo; enlazar publicación normativa D-G2-01/02 ya acordados semánticamente. El detalle de SKU padre se implementa en T-09 con su revisión exigible; un doble no acredita integración real.
- Comprobación: contexto de aplicación y WireMock con llamada real a la ruta exacta; `200` íntegro, inexistencia, `422` de negocio, `503` técnico y `502` por respuesta inválida. Casos de omisión, duplicación, inesperados, perfil/marca temporal malformados, 1/100/101 únicos, cantidades agrupadas y estados homologados. No aplicar la elegibilidad de cotización al pedido pagado.

### T-06. Desarrollar caso de uso CrearDespachoUseCase
- Alcance: orquestar cálculos de peso, volumen, paquetes fijado en 1 y cálculo de fecha programada según calendario. Generar códigos `DSP-` y `TRK-`.
- Comprobación: pruebas unitarias con JUnit 5.

### T-07. Persistencia transaccional y auditoría
- Alcance: `@Transactional` guardando en `despachos` e invocando `AuditoriaService.registrarCreacion()`.
- Comprobación: verificación de rollback si la persistencia falla.
- No escribir `cotizaciones` ni exigir un registro previo; G6 se consulta antes de la transacción local. Comparar ausencia de filas parciales en despacho/historial y ausencia de cambios en cotizaciones ante todos los rechazos.

### T-08. Pruebas de integración E2E

- Alcance: verificar CA-01 a CA-13 con PostgreSQL y proveedor controlado; luego recorrer recepción y cotización contra G6 real con revisión H/D acordada y credencial G7 efectiva. Verificar token ausente, inválido/vencido, audiencia incorrecta, scope ausente/correcto y token propio saliente.
- Comprobación: registrar comandos exactos, commits, entorno, reportes y respuesta observada en [evidence.md](./evidence.md); ninguna prueba controlada se informa como E2E real. F-02 no genera una cotización ni reutiliza el perfil histórico de F-01.

### T-09. Traducir el rechazo identificado de SKU padre

- [ ] Implementada y verificada.
- Responsable: Tarqui con Backend y Valqui para el adaptador compartido. Incremento: I-05.
- Alcance: incorporar contrato §5.2.4 con D-G2-02 cerrado semánticamente; reconocer el caso acordado y preservar todos y únicamente los causantes en el error público, literalmente, sin duplicados y en orden de solicitud. Compartir deserialización/validación con F-01, manteniendo la política comercial de F-02. Traducir el error prioritario seleccionado por G6 según la precedencia aceptada.
- Dependencias: T-05 y revisión normativa publicada por G6 que exige el campo para ese caso, seguida en DT-08 de ES-F01-06. Preparar un doble del acuerdo cerrado no completa la tarea.
- Comprobación/cierre: CA-11/12 con padre solo/múltiple/mixto y producto simple válido; lista ausente/vacía, tipos incorrectos, duplicados o SKU ajenos producen el error contractual de respuesta inválida. Sin inferir identificadores desde texto ni desde todo el lote. Sin despacho, historial ni cotización parciales.
- Evidencia prevista: EV-05. Pendiente: publicación de revisión normativa y compatibilidad del consumidor; Tarqui coordina con Valqui y G6.

### T-10. Verificar las regresiones D-G2-01/02

- [ ] Implementada y verificada.
- Responsable: Tarqui con Calidad, Valqui y Productos. Incremento: I-05.
- Alcance: CA-09 y CA-11 a CA-13; contrastar nueve combinaciones padre/variante y productos simples del proveedor. F-02 utiliza el estado recibido y continúa para `INACTIVO`/`BORRADOR` si el perfil es válido; el SKU padre no físico sigue siendo rechazado.
- Dependencias: T-06/T-07/T-09 y publicación normativa D-G2-01/02; precedencia aceptada el 04/11. Permutar lotes con errores de distintas clases: mismo código/conjunto de afectados y lista en orden de cada solicitud. Incluir lotes sin bases con perfiles incompletos, `200` con inexistentes y fallos técnicos conforme al contrato §5.2.4.
- Comprobación/cierre: proveedor controlado identificado, comparación de escrituras y regresión de idempotencia sin nueva consulta G6 al reconocer un despacho. Registrar revisión, commits, comandos y resultados; el recorrido real se acredita en T-08 por separado.
- Evidencia prevista: EV-05 y EV-04. Bloqueos externos y responsables quedan registrados al iniciar.

## 3. Cobertura y cierre

Los criterios CA-01 a CA-10 mantienen su cobertura en la matriz de [evidence.md](./evidence.md); CA-09 amplía su verificación con T-10. CA-11 se implementa en T-09 y verifica en T-10/T-08; CA-12 en T-09/T-10; CA-13 en T-09 con verificación T-10/T-08. EV-05 cubre las regresiones controladas y EV-04 el recorrido real. La especificación se cierra cuando todos los criterios tienen resultados reproducibles, revisión y dependencias reales verificadas, con el acuerdo D-G2-02 y su revisión normativa enlazados.

[cite: 1] [Contrato externo §11.1](../../integraciones/api-contract.md#111-homologación-física-g2g6-y-precisiones-de-seguimiento) y [plan](./plan.md), dependencias de cierre. Las tareas de backend permanecen pendientes.
