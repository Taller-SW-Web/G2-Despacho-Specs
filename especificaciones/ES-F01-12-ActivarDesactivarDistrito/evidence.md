# Evidencia de ES-F01-12: Activar o desactivar un distrito

## 1. Preparación — 13/11/2026

Contrato y especificación preparados mediante OpenCode por solicitud del usuario. Backend base `65adfd0`; frontend base `feb57e6`; Specs base `c2ea248`. Ramas de funcionalidad desde develop y documental desde main. Revisión humana pendiente.

## 2. Resultados del 13/11/2026

**Estado:** implementación y automatización locales aprobadas; cambios sin commit en las ramas de trabajo. Revisión por pares, PR y aceptación humana pendientes. Verificación asistida con OpenCode por instrucción del usuario. Origen: F-01 CA-36 a CA-38 y regresiones de ES-F01-02/05/06/07/08, ES-F02-01/02 y F-04.

### EV-01. Suites y entorno

Java Temurin 21.0.9, Docker 29.9.3, PostgreSQL 17.11/PostGIS (`postgis/postgis:17-3.6`), Node 20.20.2, npm 10.8.2, Vitest 3.2.7 y Playwright 1.64.1 con Chromium. Las integraciones de Gestión utilizan Testcontainers; las de navegador, un proyecto Compose con PostgreSQL `tmpfs` independiente. No se utilizó Supabase ni la base local de trabajo.

| Ubicación | Comando realmente ejecutado | Resultado |
|---|---|---|
| Gestión | `SPRING_FLYWAY_ENABLED=true ./mvnw clean verify` | 267 pruebas, cero fallos/errores/omisiones; JAR construido |
| Gateway | `./mvnw clean verify` | 34 pruebas, cero fallos/errores/omisiones; JAR construido |
| Frontend | `npm run test:f01` | 24 pruebas aprobadas, incluidas 14 de distritos y 10 de zonas |
| Frontend | `npm run test:administrativo` | 234 pruebas aprobadas en 23 archivos |
| Frontend | `npm run typecheck` | Tres comprobaciones TypeScript aprobadas |
| Frontend | `npm run build` | Administración y repartidor construidos |
| Frontend | `npm run test:distritos:e2e` | Dos pruebas de Chromium aprobadas en 8,9 s |
| Gestión | `./mvnw -q spotless:check` | Aprobado |

La variable de Flyway contrarresta su desactivación en la configuración local únicamente dentro del proceso de pruebas; Testcontainers proporciona la conexión. Los reportes están en `servicio-gestion-despachos/target/surefire-reports/` y `api-gateway/target/surefire-reports/`, fuera de Git. No se deshabilitaron pruebas ni se debilitaron aserciones; las comprobaciones antiguas de versión final se actualizaron de V10 a V11 conservando el resto de sus verificaciones.

### EV-02. Criterios funcionales y de UI

| Criterios | Comprobación ejecutada | Resultado |
|---|---|---|
| CA-01 | `DistritosHttpTests.bajaBloqueaRespaldoPostalConservaHistoricoYOtrosDistritosYRecuperaCalculo`: código ausente, propio y ajeno, cero llamadas a Productos y fila histórica intacta | Aprobado |
| CA-02 | Miraflores de la misma zona conserva cobertura durante la baja de San Borja | Aprobado en HTTP y Chromium |
| CA-03 | Recepción nueva devuelve 422 tras la baja; la misma clave/pedido aceptados recuperan el 201 original sin reconsultar Productos | Aprobado |
| CA-04 | `ReprogramacionDespachoHttpTests.distritoInactivoNoImpideReprogramarDespachoExistente` y regresión completa de F-02/F-04; conserva destino, zona e históricos | Aprobado |
| CA-05 | Cotización completa idéntica antes/después con productos y reloj fijos; Chromium compara costo, moneda, peso, volumen y plazo | Aprobado |
| CA-06 | DELETE/PATCH comparten baja; estado coincidente conserva respuesta, fecha y versión, sin otra auditoría; versión obsoleta rechaza | Aprobado |
| CA-07 | Cobertura exclusivamente postal inactiva, zona inactiva, nueva sin zona, zona sin tarifa y simulador con uno/ningún distrito activo | Aprobado |
| CA-08 | Conservar/retirar asociados inactivos sin convertir cobertura postal en distrital ni añadir inactivos; formulario conserva códigos y modalidad postal | Aprobado en backend/componentes; conservación por Gateway en Chromium |
| CUI-01/02/03 | Confirmación de efectos, baja/reactivación explícitas, filtro actualizado y conflictos sin reenvío automático | Aprobado en componentes y Chromium |
| CUI-04 | `Zonas.test.tsx`: conserva asociación inactiva exclusivamente postal; Chromium guarda zona con San Borja inactivo conservado | Aprobado |
| CUI-05 | Chromium: Cancelar recibe foco destructivo, Escape cancela y formulario móvil navega por teclado sin desbordamiento horizontal | Aprobado local; aceptación humana pendiente |

### EV-03. Recorrido integrado aislado

Proyecto `f01-distritos-qa-20261113`, compuesto con `pruebas/compose.f02.yaml` y `pruebas/compose.f01-distritos.yaml`, usando `--env-file /dev/null`. Solo se iniciaron PostgreSQL, Seguridad temporal, Gestión y Gateway; ambos proveedores alcanzaron salud UP. Frontend en `127.0.0.1:4187`, Gateway en `18080`, Seguridad temporal en `18090`.

Se utilizaron JWT RS256 del emisor temporal (humano gestor y cliente técnico Chatbot), validados por Gateway y Gestión. Productos fue simulado explícitamente mediante `productos-simulados`; no se acredita el proveedor G6 publicado ni G7 real. Las llamadas desde la aplicación fueron reales, sin interceptar sus APIs. El recorrido cubrió alta, edición, duplicado, identidad protegida, baja, respaldo postal propio/ajeno, conservación de zona, reactivación y conflicto concurrente.

Inspección final de la base desechable: Flyway V11, 50 distritos base activos, cinco auditorías distritales, tres cotizaciones exactas y dos asociaciones distritales conservadas. Posteriormente se retiraron los cuatro contenedores y su red; los datos `tmpfs` se descartaron.

Capturas inspeccionadas en el frontend, fuera de Git:

- `test-results/distritos/administracion-administra--1eadc-eal-con-Productos-simulados/distritos-escritorio.png` (1440 × 1024, captura de página completa).
- `test-results/distritos/administracion-mantiene-fo-c68d3-eclado-utilizables-en-móvil/distrito-movil.png` (390 × 844).

Pasos reproducibles en el README del frontend y `docs/pruebas.md` del backend, sección «Administración de distritos: navegador y Gateway aislados». Para repetir se recrea el entorno vacío; las pruebas escriben datos reales en su base desechable. No se registran tokens ni trazas HTTP.

### EV-04. Hallazgos corregidos

- Se detectó diferencia entre la fecha calculada por JPA y la del trigger: el adaptador refresca la entidad antes de producir respuesta y auditoría.
- La prueba de actualización V10 → V11 detectó que marcar catálogo base alteraba fechas históricas: V11 preserva esas fechas durante esa actualización técnica y restaura el trigger en la misma migración transaccional. Se conserva la comparación íntegra de los datos previos en la prueba.
- Una primera ejecución con el nivel raíz de log reducido hizo fallar tres aserciones de diagnóstico existentes. La ejecución final usó la configuración normal y las 267 pruebas pasaron; esas aserciones permanecen intactas.

## 3. Revisión y pendientes

La revisión automatizada local no sustituye revisión por pares ni aceptación humana. Integración por PR a develop en código y a main en Specs, despliegue y aceptación conjunta con G6/G7 quedan pendientes. No se actualizan changelogs ni tags durante esta rama funcional.
