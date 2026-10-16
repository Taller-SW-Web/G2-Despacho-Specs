# Tareas de ES-F02-05: Consultar y reordenar la secuencia de ruta

**Responsable de coordinación:** Tarqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoints de ruta y secuencia documentado en Gestión §3.2. | Contrato | api-contract-gestion-despachos.md | CA-01, CA-02 | Completada |
| T-02 | Endpoint `GET /api/v1/jornadas/{idJornada}/ruta` implementado con orden por secuencia. | Backend / API | Repositorio `despachos` | CA-01 | Pendiente |
| T-03 | Validador de negocio `SecuenciaValidador` con comprobación de secuencia continua y estados. | Backend / Dominio | T-02 | CA-03, CA-04 | Pendiente |
| T-04 | Caso de uso y endpoint `PUT /api/v1/jornadas/{idJornada}/secuencia` transaccional. | Backend / API | T-03 | CA-02, CA-05, CA-06 | Pendiente |
| T-05 | Pruebas de integración de backend con MockMvc y Testcontainers. | Calidad / Backend | T-04 | CA-01 a CA-06 | Pendiente |
| T-06 | Componente React de lista drag & drop con soporte de teclado y bloqueo de no ASIGNADO. | Frontend / UI | CR-01, CR-09, CR-16 | CUI-01, CUI-02, CUI-04 | Pendiente |
| T-07 | Barra inferior de cambios pendientes (CR-13) con acciones "Guardar" y "Descartar". | Frontend / UI | T-06, CR-13 | CUI-03, CUI-05 | Pendiente |

## 2. Detalle de tareas

### T-01. Validar contrato
- Alcance: confirmar payload `{ despachos: [{ idDespacho, posicion }] }` en [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).
- Comprobación: contrato revisado.

### T-02. Consulta de ruta
- Alcance: `RutaJornadaController.obtenerRuta()` devolviendo lista ordenada de paradas con estados.
- Comprobación: prueba unitaria de controlador.

### T-03. Validador de permutación
- Alcance: verificar que las posiciones recibidas sean una secuencia estricta `1..N` y que despachos en `EN_CAMINO`, `ENTREGADO` o `FALLIDO` no cambien de posición.
- Comprobación: tests unitarios cubriendo casos borde (huecos, números negativos, duplicados).

### T-04. Actualización transaccional
- Alcance: `ReordenarSecuenciaUseCase` con `@Transactional` actualizando `posicion_secuencia` de forma atómica y registrando auditoría.
- Comprobación: tests con MockMvc verificando respuesta 200 y 409 ante concurrencia.

### T-05. Suite de integración backend
- Alcance: suite completa verificando todas las respuestas y transiciones.
- Comprobación: 100% de tests aprobados.

### T-06. Componente Drag & Drop
- Alcance: lista vertical con `@hello-pangea/dnd`, botones subir/bajar y estilos visuales acordes al sistema de diseño.
- Comprobación: tests de interacción con Testing Library.

### T-07. Barra fija de cambios
- Alcance: componente flotante inferior (CR-13) que aparece al mover un ítem y gestiona el guardado o descarte.
- Comprobación: pruebas de componente y E2E.
