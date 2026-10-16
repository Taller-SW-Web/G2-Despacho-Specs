# Plan de ES-F02-01: Recepción de solicitudes de despacho

**Responsable:** Tarqui.

**Estado:** Plan técnico documental preparado el 16/10/2026; implementación y verificación pendientes.

**UI:** No aplica; interfaz externa REST de servicio a servicio.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-07 | Especificación atómica SDD de ES-F02-01. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-01, RF-05, CA-01, CA-02, CA-11, CA-12, CA-21 | Especificación funcional vigente. |
| Contrato de API | [api-contract.md §7.1](../../integraciones/api-contract.md#71-crear-un-despacho-para-un-pedido-listo-para-entrega) y [§5.2](../../integraciones/api-contract.md#52-obtener-datos-físicos-vigentes-de-productos) | Contrato canónico de integración con Ventas y Productos. |
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
- **Integración con Productos y Ofertas:** llamada POST a `/api/v1/productos/lote-datos-fisicos` enviando lista de SKU deduplicados. Timeout: 1500 ms con fallback que responda `503 Service Unavailable`.
- **Cálculo físico:** `pesoTotalKg = SUM(pesoKg * cantidad)`, `volumenTotalM3 = SUM(volumenM3 * cantidad)`. Registrar `cantidadPaquetes = 1`.
- **Cálculo de fecha:** `fechaProgramada = hoy + plazoDiasHabiles` considerando fines de semana según calendario de operaciones.
- **Persistencia:** inserción atómica en `despachos` e `historial_estados_despacho` con `estado_nuevo = PENDIENTE_ASIGNACION`.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | DTOs, validaciones jakarta y controlador con seguridad JWT. | Configuración Spring Security base. | CA-03, CA-07. |
| I-02 | Verificación de idempotencia y resolución de zona (F-01). | Esquema base PostgreSQL y servicio F-01. | CA-02, CA-04. |
| I-03 | Cliente de Productos y cálculo de carga física y fecha. | Cliente REST con mock/wiremock. | CA-01, CA-05, CA-06. |
| I-04 | Persistencia transaccional de despacho y auditoría. | `DespachoRepository`, `AuditoriaService`. | CA-01. |

## 6. Estrategia de verificación

- Pruebas unitarias de controladores con `@WebMvcTest` y validación de DTOs.
- Pruebas unitarias de servicio de dominio con `JUnit 5 + Mockito` para cálculos de peso, volumen y fecha.
- Pruebas de integración con `MockMvc` y `Testcontainers` (PostgreSQL) para verificar unicidad por pedido e idempotencia.
- Mock de Productos y Ofertas con `WireMock` simulando respuestas exitosas, datos faltantes (422) y timeouts (503).
