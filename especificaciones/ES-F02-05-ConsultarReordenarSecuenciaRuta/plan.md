# Plan de ES-F02-05: Consultar y reordenar la secuencia de ruta

**Responsable:** Tarqui.

**Estado:** Actualizado el 26/10/2026 para la implementación en curso.

## Decisiones vigentes de esta iteración

Prevalece [Gestión §3.2.1](../../integraciones/api-contract-gestion-despachos.md#321-ruta-y-secuencia-administrativa--es-f02-05) sobre las propuestas técnicas históricas de las secciones siguientes:

- `ControladorRutas`, `RutasPersistencia`, `ModelosRuta` y `ValidadorSecuencia`; columna real `secuencia_ruta`, no `posicion_secuencia`.
- Consulta de estado por el puerto existente de Operación §5.4 fuera de transacción local. Desconocida/no disponible: `503`, sin suponer inexistencia.
- `If-Match` obligatorio, identidad de guardado UUID v4 y tabla durable `resultados_secuencia_ruta` (Flyway V5). Recuperación exacta después de perder respuesta.
- Bloqueo de jornada compartido con asignación, filas en orden determinista y comparación de la fotografía completa. Restricción única diferida para intercambiar posiciones en un lote.
- Permutación de espacios vigentes, sin compactar huecos históricos ni mover paradas no `ASIGNADO`.
- Historial y outbox dentro de la misma transacción. Cada parada movida incrementa versión; su proyección reutiliza el mecanismo existente sin reiniciar el hito de asignación.
- `RutasProgramacion` consume monitoreo de F-06 incluyendo saturados; no usa disponibilidad como catálogo de todas las rutas. Reutiliza CR-09/13 y hooks existentes. Arrastre HTML nativo y flechas accesibles, sin añadir biblioteca ni React Query al proyecto.
- Gateway enruta las operaciones específicas a Gestión antes del comodín de jornadas de Operación.
- Verificación: `RutasHttpTests`, pruebas React y recorrido Playwright real con servicios/base desechables en `pruebas/compose.f02.yaml` y `pruebas/verificar_f02_rutas.py` del backend. El emisor es Seguridad temporal, no G7.

## Propuesta histórica (16/10/2026)

**UI:** Aplica; pestaña "Rutas por repartidor" en `/programacion`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-06 | Especificación atómica SDD. |
| UI | [ui.md](./ui.md), UI-01 a UI-04, CUI-01 a CUI-05 | Especificación de interfaz drag & drop. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-06 | Especificación funcional vigente. |
| Contrato de API | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) | Endpoints de ruta y secuencia. |
| Componentes React | [componentes-react.md](../../disenio/componentes-react.md), CR-01, CR-09, CR-13, CR-16 | Componentes Mantine compartidos. |

## 2. Estrategia y responsabilidades

El microservicio `servicio-gestion-despachos` es el propietario de la secuencia de ruta de cada jornada (`posicion_secuencia` en la tabla `despachos`). Expone dos operaciones REST: `GET` para consultar la ruta y `PUT` para reordenar en lote las posiciones. La actualización se ejecuta dentro de una transacción atómica `@Transactional` con bloqueo de fila o bloqueo optimista para prevenir inconsistencias si un repartidor inicia un traslado simultáneamente en F-03.

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| Frontend | Lista drag & drop, botones accesibles, barra fija de cambios (CR-13). | `RutaRepartidorView.tsx`, `ListaParadasDnd.tsx`, `BarraCambiosRuta.tsx`. |
| API / Web | Endpoints `GET` y `PUT` de jornada con autorización JWT. | `RutaJornadaController`, `SecuenciaRutaRequestDTO`. |
| Aplicación | Validación de secuencia 1..N continua y bloqueo de no ASIGNADO. | `ReordenarSecuenciaUseCase`, `ConsultarRutaJornadaUseCase`. |
| Dominio | Reglas de inmutabilidad de paradas iniciadas y permutación matemática. | `SecuenciaValidador`, `Despacho`. |
| Infraestructura | Actualizaciones por lote en PostgreSQL y registro de auditoría. | `DespachoRepository`, `AuditoriaRepository`. |

## 3. Frontend y componentes React

- Biblioteca DND: `@hello-pangea/dnd` para reordenamiento fluido con soporte de accesibilidad y teclado.
- Estado local: `paradasOriginales` y `paradasModificadas`. Cuando difieren, se despliega `BarraAccionesFija` (CR-13).
- Las tarjetas de despacho en `EN_CAMINO`, `ENTREGADO` o `FALLIDO` se renderizan como ítems fijos sin `Draggable`.

## 4. Backend, persistencia e integraciones

- **Endpoints:**
  - `GET /api/v1/jornadas/{idJornada}/ruta`: devuelve despachos ordenados por `posicion_secuencia ASC`.
  - `PUT /api/v1/jornadas/{idJornada}/secuencia`: recibe `{ "despachos": [ { "idDespacho": "...", "posicion": 1 }, ... ] }`.
- **Validaciones en backend:**
  - Obtener todos los despachos de la jornada desde la base de datos con `SELECT ... FOR UPDATE` o comprobación de `@Version`.
  - Comprobar que ningún despacho que no esté en `ASIGNADO` haya cambiado de posición.
  - Verificar que las posiciones recibidas sean exactamente `1, 2, ..., N` sin duplicados.
- **Persistencia:**
  - `UPDATE despachos SET posicion_secuencia = :posicion WHERE id = :idDespacho`.
  - Registro de auditoría `REORDENAMIENTO_RUTA` con lista previa y nueva.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Caso de uso de consulta de ruta y controlador GET. | Repositorio JPA `despachos`. | CA-01. |
| I-02 | Validador de permutación continua y caso de uso PUT con transacción atómica. | I-01. | CA-02, CA-03, CA-04, CA-05. |
| I-03 | Componente React con Drag & Drop, botones de flecha y barra de cambios pendientes. | I-02, Mantine CR-13. | CUI-01 a CUI-05. |

## 6. Estrategia de verificación

- Pruebas unitarias con JUnit 5 de `SecuenciaValidador` probando permutaciones válidas, saltos (1, 3), duplicados (2, 2) y paradas bloqueadas.
- Pruebas de integración con MockMvc verificando respuestas 200, 400 y 409.
- Pruebas de concurrencia: simular cambio simultáneo de estado a `EN_CAMINO` antes de guardar el reordenamiento.
- Pruebas de interacción en React verificando que el botón "Descartar" restaura la lista previa.
