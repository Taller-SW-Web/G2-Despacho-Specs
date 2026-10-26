# Plan de ES-F02-01: Recepción de solicitudes de despacho

**Responsable:** Tarqui.

**Estado:** Plan técnico documental preparado el 16/10/2026; implementación y verificación pendientes.

**Actualización:** 26/10/2026. Preparación de ruta canónica, lotes íntegros, estados comerciales y errores compartidos con F-01; homologación externa pendiente en el contrato §11.1 [cite: 1]. No se inspeccionó ni ejecutó el repositorio backend.

**UI:** No aplica; interfaz externa REST de servicio a servicio.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-10 | Especificación atómica SDD actualizada el 26/10/2026. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-01, RF-05, CA-01, CA-02, CA-11, CA-12 y CA-21 a CA-24 | Especificación funcional vigente. |
| Contrato de API | [api-contract.md §7.1](../../integraciones/api-contract.md#71-crear-un-despacho-para-un-pedido-listo-para-entrega), [§5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas) y [§11.1](../../integraciones/api-contract.md#111-respuesta-propuesta-y-plan-de-homologación-física-g2g6) | Contrato canónico de integración y estado de homologación H-G2-01/02/03. |
| Arquitectura y datos | [C4 Contenedores](../../arquitectura/c4-contenedores.md), §3; [Modelo de datos](../../arquitectura/modelo-datos.md), §§1 y 3.1 | Entidades `despachos` e `historial_estados_despacho`. |

## 2. Estrategia y responsabilidades

El microservicio `servicio-gestion-despachos` recibe la petición en un controlador REST autenticado con Spring Security (Resource Server JWT). La validación sintáctica se delega a Bean Validation (`jakarta.validation`). El servicio de aplicación coordina la consulta de cobertura con F-01 y la llamada HTTP a Productos y Ofertas mediante un cliente WebClient / RestClient con resiliencia y timeouts acotados. La persistencia del despacho y la auditoría se ejecutan en una transacción atómica `@Transactional`.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| API / Web | Validación de headers, JWT scopes y DTO de entrada. | `CrearDespachoController`, `CrearDespachoRequestDTO`, `DespachoResponseDTO`. |
| Aplicación | Orquestación: idempotencia, cálculo de pesos/volúmenes, fecha programada y persistencia. | `CrearDespachoUseCase`, `IdempotenciaService`. |
| Dominio | Reglas de negocio, generación de códigos operativos/rastreo y validación de cobertura. | `Despacho`, `EstadoDespacho`, `CodigoRastreoGenerator`. |
| Infraestructura | Clientes REST hacia Productos (Físicos) y persistencia JPA en PostgreSQL. | `ProductosClient`, `DespachoRepository`, `AuditoriaRepository`. |

## 3. Frontend y componentes React

No aplica. La recepción es un proceso de backend consumido exclusivamente por `modulo-ventas`. El impacto visual en el frontend administrativo se materializa en la cola de pendientes ([ES-F02-03](../ES-F02-03-ConsultarColaPendientes/spec.md)), donde el despacho creado aparece automáticamente en `PENDIENTE_ASIGNACION`.

## 4. Backend, persistencia e integraciones

- **Endpoint:** `POST /api/v1/despachos`.
- **Seguridad:** validar token con `sub=modulo-ventas`, `aud=api-despacho` y scope `despachos:crear`.
- **Idempotencia:** índice único en base de datos sobre `id_pedido`. Comprobación rápida: si ya existe, devolver HTTP `200 OK` con la entidad existente. La tabla de idempotencia almacena `idempotency_key`, `id_despacho`, `hash_payload` y `respuesta_json`.
- **Integración con F-01:** consulta interna a `ZonaService` para validar que el distrito/código postal pertenezca a una zona activa y obtener los días de plazo.
- **Integración con Productos y Ofertas:** utilizar la operación canónica del contrato §5.2, con SKU únicos y cantidades acumuladas conservadas localmente. Máximo 100 únicos; rechazar exceso sin llamar a G6. Token propio `modulo-despacho` con audiencia y scope acordados, sin reutilizar el token de Ventas. Timeout y presupuesto total deben conciliarse con DT-04 de ES-F01-06 y el requisito de recepción de F-02; no fijar un fallback que convierta todos los errores en `503`.
- **Adaptador compartido:** revisar en el backend el cliente seleccionado por `@Qualifier("productosProgramacion")` y la selección de F-01 frente a `CatalogoProductosStub`/`@Primary`. Compartir HTTP y validación del lote, manteniendo elegibilidad por caso de uso. Una prueba de contexto con perfil normal debe demostrar que ambos usan el proveedor HTTP real.
- **Integridad y errores:** validar la correspondencia completa y exclusiva de SKU entre `productos`/`noEncontrados`, esquema físico y marca temporal. Aplicar la matriz del contrato §5.2.2: distinguir datos incompletos de negocio, inexistencia, respuesta no conforme y caída técnica. Un `200` malformado no origina un cálculo parcial.
- **Estado comercial:** la regla prevista H-G2-02 no rechaza pedidos pagados solo por `INACTIVO`; la extensión a `BORRADOR` y el enum explícito requieren aceptación externa. No aplicar a F-02 el rechazo de elegibilidad de F-01.
- **Cálculo físico:** `pesoTotalKg = SUM(pesoKg * cantidad)`, `volumenTotalM3 = SUM(volumenM3 * cantidad)`. Registrar `cantidadPaquetes = 1`.
- **Cálculo de fecha:** `fechaProgramada = hoy + plazoDiasHabiles` considerando fines de semana según calendario de operaciones.
- **Persistencia:** inserción atómica en `despachos` e `historial_estados_despacho` con `estado_nuevo = PENDIENTE_ASIGNACION`.
- **Cotizaciones:** no se exige cotización previa, no se toma su instantánea como perfil vigente y no se escribe `cotizaciones` desde esta recepción. Resolver repeticiones antes de llamar a G6; conservar restricciones de unicidad en el commit concurrente. Las consultas externas se realizan antes de abrir la escritura local.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | DTOs, validaciones jakarta y controlador con seguridad JWT. | Configuración Spring Security base. | CA-03, CA-07. |
| I-02 | Verificación de idempotencia y resolución de zona (F-01). | Esquema base PostgreSQL y servicio F-01. | CA-02, CA-04. |
| I-03 | Cliente físico real, integridad, estados, límite y cálculo de carga/fecha. | Revisión física homologada; dobles primero, G6 real al cierre. | CA-01, CA-05, CA-06, CA-08 a CA-10. |
| I-04 | Persistencia transaccional de despacho y auditoría. | `DespachoRepository`, `AuditoriaService`. | CA-01. |

## 6. Estrategia de verificación

- Pruebas unitarias de controladores con `@WebMvcTest` y validación de DTOs.
- Pruebas unitarias de servicio de dominio con `JUnit 5 + Mockito` para cálculos de peso, volumen y fecha.
- Pruebas de integración con `MockMvc` y `Testcontainers` (PostgreSQL) para verificar unicidad por pedido e idempotencia.
- Proveedor controlado con `WireMock`: error de negocio físico con SKU afectados, inexistencia correctamente clasificada, timeout/caída y `200` malformado. Probar omisiones, duplicados en cada arreglo y entre ambos, inesperados, JSON ilegible, estado desconocido y marca temporal inválida.
- Cantidades originales conservadas; 1/100/101 SKU únicos y más de 100 líneas con pocos SKU. Rechazos sin despacho, historial parcial ni fila en `cotizaciones`; repetición idempotente sin nueva llamada a G6.
- Estados homologados en recepción frente a cotización; `BORRADOR` no acredita conformidad mientras falte aceptación bilateral. Contexto de aplicación con cliente HTTP real y pruebas de token propio, audiencia y scope.
- Recorrido real G2 → G6 con concesión G7 efectiva; registrar comandos, commits, revisión de OpenAPI, entorno, respuestas y limitaciones en [evidence.md](./evidence.md). Los dobles no acreditan ese E2E.

## 7. Dependencias de cierre

- [ ] Repositorio backend y commits de adaptadores/selección de beans identificados.
- [ ] H-G2-01/02/03 publicados y aceptados por ambos equipos, con revisión fija del OpenAPI y esquema de SKU afectados.
- [ ] Credencial concedida y provista por G7 para la audiencia/scope acordados.
- [ ] Tiempo de espera y presupuesto de recepción conciliados con la integración de F-01.
- [ ] CA-01 a CA-10 ejecutados y enlazados con resultados reales.

[cite: 1] [Contrato externo §§5.2 y 11.1](../../integraciones/api-contract.md#111-respuesta-propuesta-y-plan-de-homologación-física-g2g6), [plan de ES-F01-06](../ES-F01-06-CotizarEnvioConProductos/plan.md) y [modelo de datos](../../arquitectura/modelo-datos.md).
