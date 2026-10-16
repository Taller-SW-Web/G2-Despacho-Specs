# Evidencia de ES-F02-01: Recepción de solicitudes de despacho

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-01, RF-05).
- Contratos asociados: `integraciones/api-contract.md` (§7.1 y §5.2).
- Commits de implementación y entorno de pruebas: pendientes de ejecución en los repositorios de código.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-06, T-07, T-08 | Recepción exitosa con zona activa, datos físicos de Productos, fecha calculada y estado PENDIENTE_ASIGNACION. | EV-01, EV-03 | No ejecutado |
| CA-02 | T-04, T-08 | Solicitud con destino sin zona de cobertura activa rechazada con 422 DESP_ERROR_SIN_COBERTURA. | EV-01, EV-03 | No ejecutado |
| CA-03 | T-01, T-08 | Solicitud con datos incompletos o inválidos rechazada con 400 Bad Request. | EV-01 | No ejecutado |
| CA-04 | T-03, T-08 | Solicitud repetida para el mismo idPedido responde 200 OK de forma idempotente sin duplicar. | EV-01, EV-03 | No ejecutado |
| CA-05 | T-05, T-08 | SKU inexistente o con dimensiones nulas rechazado con 422 DESP_ERROR_PRODUCTO_NO_ENCONTRADO / INCOMPLETO. | EV-02, EV-03 | No ejecutado |
| CA-06 | T-05, T-08 | Caída o timeout de Productos y Ofertas rechazada con 503 DESP_ERROR_PRODUCTOS_NO_DISPONIBLE. | EV-02, EV-03 | No ejecutado |
| CA-07 | T-02, T-08 | Petición sin token o sin scope despachos:crear rechazada con 401/403. | EV-01 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Validación de controlador y seguridad
- Tareas asociadas: T-01, T-02, T-03.
- Comando previsto: `./mvnw test -Dtest=CrearDespachoControllerTest`
- Resultado: **No ejecutado**.

### EV-02. Cliente de Productos y manejo de fallos
- Tareas asociadas: T-05.
- Comando previsto: `./mvnw test -Dtest=ProductosClientWireMockTest`
- Resultado: **No ejecutado**.

### EV-03. Prueba de integración E2E con PostgreSQL
- Tareas asociadas: T-04, T-06, T-07, T-08.
- Comando previsto: `./mvnw test -Dtest=CrearDespachoIntegrationTest`
- Resultado: **No ejecutado**.
