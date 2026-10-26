# Tareas de ES-F02-05: Consultar y reordenar la secuencia de ruta

**Responsable de coordinación:** Tarqui.

**Estado:** Backend, UI y recorrido integrado verificados localmente con Seguridad temporal; aceptación humana pendiente.

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoints de ruta y secuencia documentado en Gestión §3.2. | Contrato | api-contract-gestion-despachos.md | CA-01, CA-02 | Completada |
| T-02 | Consulta de ruta ordenada mediante `ControladorRutas` y `RutasPersistencia`. | Backend / API | Repositorio `despachos` | CA-01 | Completada localmente |
| T-03 | `ValidadorSecuencia`: permutación de posiciones vigentes y paradas fijas. | Backend / Dominio | T-02 | CA-03, CA-04 | Completada localmente |
| T-04 | PUT transaccional con fotografía, resultado durable, auditoría y outbox. | Backend / API | T-03 | CA-02, CA-05, CA-06 | Completada localmente |
| T-05 | `RutasHttpTests`, MockMvc y PostgreSQL desechable. | Calidad / Backend | T-04 | CA-01 a CA-06 | 7 pruebas aprobadas |
| T-06 | `RutasProgramacion`, arrastre nativo, flechas y bloqueo de posiciones fijas. | Frontend / UI | CR-01, CR-09 | CUI-01, CUI-02, CUI-04 | Completada localmente: React y navegador real |
| T-07 | CR-13, descarte, guardado y recuperación de respuesta perdida. | Frontend / UI | T-06, CR-13 | CUI-03, CUI-05 | Completada localmente: incluye pérdida de respuesta y conflicto con F-03 real |

## 2. Detalle de tareas

### T-01. Validar contrato
- Alcance: confirmar payload `{ despachos: [{ idDespacho, posicion }] }` en [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).
- Comprobación: contrato revisado.

### T-02. Consulta de ruta
- Alcance: `ControladorRutas` devuelve la lista ordenada de paradas con estados y ETag; jornadas consultadas mediante el puerto existente de Operación.
- Comprobación: prueba unitaria de controlador.

### T-03. Validador de permutación
- Alcance: verificar permutación exacta de las posiciones vigentes (`1..N` en rutas nuevas), conservar huecos históricos y posiciones de no `ASIGNADO`.
- Comprobación: tests unitarios cubriendo casos borde (huecos, números negativos, duplicados).

### T-04. Actualización transaccional
- Alcance: `RutasPersistencia` actualiza `secuencia_ruta` atómicamente con comparación de fotografía, historial, outbox y resultado durable. Gateway y CORS publican la operación correcta.
- Comprobación: tests con MockMvc verificando respuesta 200 y 409 ante concurrencia.

### T-05. Suite de integración backend
- Alcance: suite completa verificando todas las respuestas y transiciones.
- Comprobación: 100% de tests aprobados.

### T-06. Componente Drag & Drop
- Alcance: lista con arrastre HTML nativo y botones subir/bajar por teclado, sin nueva dependencia; estilos de componentes y tema compartidos.
- Comprobación: tests de interacción con Testing Library.

### T-07. Barra fija de cambios
- Alcance: componente flotante inferior (CR-13) que aparece al mover un ítem y gestiona el guardado o descarte.
- Comprobación: pruebas de componente y E2E.
