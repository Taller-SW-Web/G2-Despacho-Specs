# Evidencia de ES-F02-05: Consultar y reordenar la secuencia de ruta

**Estado:** Backend y UI implementados; verificación local con servicios G2 reales y Seguridad temporal. Aceptación humana y Seguridad G7 pendientes.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** 26/10/2026, America/Lima.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-06, CA-14).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2).
- Rama `feature/f02-rutas-transferencia-segura` en Docs/Backend/Frontend; cambios sin commit atribuido. Bases de código: Backend `48fe3b6`, Frontend `6520f8f`.
- Java Temurin 21.0.13, Docker 29.9.2, PostgreSQL 17.11/PostGIS desechables, Flyway Gestión V1–V5 y Operación V1–V7. No se usan Supabase ni la base de trabajo.
- `RutasHttpTests` utiliza persistencia y transacciones reales con identidad y lectura de jornada simuladas explícitamente. Playwright utiliza los servicios reales de Gestión/Operación/Gateway y JWT RS256 del emisor temporal G2.
- Contrato precisado en Gestión §3.2.1: permutar posiciones vigentes, conservar huecos históricos, `If-Match` y clave durable; no se promete actualización distribuida instantánea.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación ejecutada | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-05 | Ruta ordenada con estados, ETag y no-store. | EV-01, EV-03 | Aprobado localmente |
| CA-02 | T-03, T-04, T-05 | Intercambio atómico, versión, auditoría y outbox; recuperación exacta sin duplicados. | EV-01, EV-03 | Aprobado localmente |
| CA-03 | T-03, T-05 | Posición fija de no ASIGNADO, rechazo sin escrituras parciales. | EV-01 | Aprobado localmente |
| CA-04 | T-03, T-05 | Duplicados, omisiones, identidades ajenas y espacios no vigentes. | EV-01 | Aprobado localmente |
| CA-05 | T-04, T-05 | Versión cambiada por inicio de traslado y dos guardados simultáneos: uno gana, otro recibe 409. | EV-01, EV-03 | Aprobado con PostgreSQL; además inicio de traslado F-03 real durante edición de navegador |
| CA-06 | T-02, T-04, T-05 | Sin token 401; usuario sin rol y token de servicio 403, sin datos. | EV-01 | Aprobado con identidad de prueba |
| CUI-01 | T-06 | Posiciones persistidas, estados y consulta de jornada. | EV-02, EV-03 | Aprobado localmente |
| CUI-02 | T-06 | Sin controles para paradas fijas; mover conserva sus espacios. | EV-02, EV-03 | Aprobado en React y tras conflicto de traslado real |
| CUI-03 | T-07 | Barra ante cambios; descarte restaura sin escribir. | EV-02, EV-03 | Aprobado localmente |
| CUI-04 | T-06 | Flechas por teclado y anuncio de posición. | EV-02, EV-03 | Aprobado; no equivale a auditoría con lector de pantalla |
| CUI-05 | T-07 | Prevención de doble envío, spinner, éxito, recarga y recuperación con la misma identidad. | EV-02, EV-03 | Aprobado localmente |

## 3. Registros de verificación

### EV-01. Pruebas de integración de la API de ruta y secuencia
- Tareas asociadas: T-02, T-03, T-04, T-05.
- Comando: `./mvnw clean verify` dentro de cada servicio, Java 21 y Docker disponibles.
- Resultado: Gestión **164 pruebas**, Gateway **28**, Operación **123**, sin fallos/errores/omitidas. Incluyen 7 pruebas de `RutasHttpTests`, regresiones de asignación y las pruebas de transferencia F-06. Los resultados de transferencia no acreditan la reasignación canónica de ES-F02-06.
- Se induce fallo de historial: rollback de posición, versión, outbox y resultado. Se conserva la posición histórica al retirar una parada; una jornada cerrada es solo lectura. Gateway prueba enrutamiento específico y preflight con If-Match.

### EV-02. Pruebas de componentes React de Drag & Drop y barra fija
- Tareas asociadas: T-06, T-07.
- Comandos desde frontend: `NODE_OPTIONS=--no-experimental-webstorage npm run test:f02`, `npm run typecheck`, `npm run build`.
- Resultado: **20 pruebas F-02 aprobadas** (13 de cola/asignación y 7 nuevas de rutas). Tipos y construcción correctos. Las 4 pruebas históricas de navegador con APIs simuladas (`npm run test:f02:e2e`) también pasan.
- Suite administrativa completa: **174 aprobadas y 2 fallidas** en `Zonas.test.tsx`; componentes compartidos: **207 aprobadas y 1 fallida** en `ShellAdministrativo.test.tsx`. Se reprodujeron los mismos fallos en un snapshot limpio del HEAD base `6520f8f` sin los cambios de esta rama (167/169 administrativas y 207/208 compartidas). No se deshabilitaron pruebas ni se modificaron esos componentes para ocultarlos.

### EV-03. Pruebas de flujo E2E
- Tareas asociadas: T-05, T-07.
- Comando desde backend: `python3 pruebas/verificar_f02_rutas.py`, que invoca `npm run test:f02:rutas:e2e` del frontend.
- Resultado: recorrido aprobado con navegador, Gateway, Gestión, Operación y consulta de ruta F-03 reales. El emisor es Seguridad temporal de G2; Productos/Ventas/G7 no quedan acreditados. PostgreSQL usa almacenamiento temporal y un proyecto Compose único, eliminado al terminar.
- Se crean dos simulados y se asignan por APIs reales, se abre la ruta administrativa, se mueve con teclado, se descarta y se arrastra otra parada. Se guarda perdiendo la respuesta después de aceptarla y se recupera el mismo comando; se consulta F-03 hasta comprobar el nuevo orden versionado. Luego F-03 inicia traslado mientras el Gestor mantiene otra edición: guardar devuelve conflicto, recarga la ruta y retira los controles de la parada iniciada sin mover su posición.
- Capturas sintéticas: [escritorio](../../../G2-Despacho-Frontend/docs/evidencia/f02-rutas/ruta-1440.png), [tableta](../../../G2-Despacho-Frontend/docs/evidencia/f02-rutas/ruta-1024.png), [móvil](../../../G2-Despacho-Frontend/docs/evidencia/f02-rutas/ruta-390.png). Sin desbordamiento de página tras estabilizar el cambio de layout del Shell.

## 4. Límites y pendientes

- No se implementan reasignación pública, cancelación, optimización de rutas ni una segunda tabla de auditoría.
- La primitiva F-06 es localmente atómica; falta su orquestación durable en Gestión. Ver ES-F02-06 y Operación §5.3.1.
- Se conserva la evidencia histórica del frontend inicial en su guía F-02. Los archivos ES-F02-01 a 04 ya tenían cambios locales del usuario: esta iteración no los sobrescribe. El índice distingue implementación de aceptación pendiente.
- Las proyecciones son eventualmente consistentes. Cada parada movida se entrega por separado; esta iteración no promete una fotografía distribuida atómica entre servicios.
- Aprobación humana, lector de pantalla y validación con Seguridad real siguen pendientes. Las suites generales de frontend no se declaran verdes por los fallos base reproducidos.
