# Evidencia de ES-F01-09: Consultar distritos

## 1. Preparación — 13/11/2026

Contrato y especificación preparados mediante OpenCode por solicitud del usuario. Backend base `65adfd0`; frontend base `feb57e6`; Specs base `c2ea248`. Ramas de funcionalidad desde develop y documental desde main. Revisión humana pendiente.

## 2. Resultados

Verificación local del 13/11/2026 mediante OpenCode: aprobada; cambios en las ramas de trabajo, todavía sin commit ni revisión humana. F-01 CA-33.

| Criterios | Comprobación ejecutada | Resultado |
|---|---|---|
| CA-01/02 | `DistritosHttpTests.migracionConservaCatalogoBaseYFiltrosCompatibles`: 50 base, baja, activos por defecto, inactivos/todos y búsqueda sin distinguir mayúsculas | Aprobado |
| CA-03 | Detalle con versión/identidad editable y UUID inexistente con 404 | Aprobado |
| CA-04 | `todasLasOperacionesRequierenGestorHumano`: seis operaciones sin token, con otro rol y con token técnico que intenta incluir el rol | Aprobado |
| CUI-01/02 | `Distritos.test.tsx`: filtros, datos reales del contrato, error/reintento, permiso denegado y respuesta antigua ignorada | Aprobado con API simulada |
| CUI-03/04 | Chromium: lista y acciones por Gateway real local; captura de escritorio y formulario móvil/teclado | Aprobado local; revisión humana pendiente |

Comandos, entorno, suites y límites compartidos en [ES-F01-12, resultados](../ES-F01-12-ActivarDesactivarDistrito/evidence.md#2-resultados-del-13112026). La automatización local no acredita aceptación humana ni el despliegue G6/G7.
