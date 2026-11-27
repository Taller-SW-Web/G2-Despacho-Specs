# Evidencia de ES-F02-09

## 1. Alcance

Ramas locales: Docs `docs/f02-adelantar-despachos` desde `main`; backend y frontend `feature/f02-adelantar-despachos` desde `develop`. Sin push, despliegue ni aceptación humana.

- Frontend: commit local `c4f06f4`, basado en `f53c3ff`.
- Backend: commit local `3fc9af6`, basado en `d36faff`.
- Docs: basado en `2bd99a2`; este registro viaja en el commit documental del incremento.

## 2. Resultados

Verificación local del 24/11/2026:

| Comprobación | Resultado | Límite |
|---|---|---|
| Frontend: `npm ci` | Instalación desde lockfile completada | No se modificaron dependencias ni lockfile |
| `NODE_OPTIONS=--no-experimental-webstorage npm run test:administrativo` | 287 pruebas aprobadas en 27 archivos | JSDOM y APIs simuladas; incluye validación de respuesta, recuperación, doble envío e historial |
| `npm run typecheck` y `npm run build` | Ambas aplicaciones aprobadas | Advertencias de chunks mayores de 500 kB y anotaciones de dependencias; no equivalen a despliegue |
| `npm run test:f02:e2e -- pruebas/f02/adelanto.spec.ts` | 2 recorridos Chromium aprobados, 1440 y 390 px | API interceptada; motivo, confirmación, teclado, foco y ausencia de desbordamiento |
| Gestión: `./mvnw -B spotless:apply clean verify` | Ejecución final aprobada: 313 pruebas, cero fallos/errores/omitidas; incluye 31 de `ProgramacionHttpTests` y una de reloj de `AdelantarDespachoTests` | JDK Corretto 21.0.13.1 temporal y PostgreSQL Testcontainers desechable; G7/Operación/Ventas son dobles HTTP |

Las capturas de navegador se generan en `test-results/adelanto/` del frontend (fuera de Git). Se revisó visualmente el modal móvil. El primer intento de frontend detectó dependencias locales incompletas y un uso de autosize incompatible con JSDOM; se instaló desde el lockfile y se dejó un área de texto de filas fijas, sin debilitar pruebas. Una prueba de historial se corrigió para invocar su fábrica de fixtures. El primer Maven se interrumpió durante descarga de dependencias por el límite de ejecución; se amplió el tiempo y la ejecución completa aprobó.

No se utilizaron bases compartidas ni se ejecutaron recorridos contra proveedores publicados. Sin aceptación humana ni auditoría manual con lector de pantalla.

## 3. Cobertura local y pendientes

- CA-01/CA-04: fecha de Lima, estado pendiente, versión, auditoría con fechas, conservación de espera/contador y ausencia de nuevos eventos o reservas durante el adelanto. La asignación posterior publica `DESPACHO_ASIGNADO` y `PROYECCION_DESPACHO` con la fecha actualizada.
- CA-02: rechazo por fecha no futura, estado, versión y cercos de cancelación/asignación pendientes; fallo inyectado de auditoría revierte fecha, versión y respuesta idempotente.
- CA-03: repetición exacta, contenido distinto con igual clave, dos comandos sobre la misma versión y dos repeticiones concurrentes de la misma clave. Se recupera también el resultado después de asignar, sin duplicar auditoría.
- CA-05: pruebas HTTP de identidad ausente, token de servicio sin rol y formato/cabeceras/motivo; controles existentes del gestor reutilizados.
- CA-06: pruebas JSDOM de motivo, doble clic, recarga, permisos, conflicto y recuperación con la misma clave; validación de respuesta e historial. Chromium revisa foco/Escape, ambas anchuras y que solo el POST de adelanto se emita antes de habilitar asignación.
- `git diff --check` en los tres repositorios sin errores. Enlaces Markdown locales revisados sin destinos inexistentes. No se modificó `CHANGELOG.md` ni se crearon tags.
- No se reejecutaron suites de Gateway ni Operación: no se modificó su código, su contrato o su configuración. El recorrido conjunto con proveedores reales, la revisión de pares y aceptación humana permanecen pendientes.

Los comandos Maven se ejecutaron con `JAVA_HOME=/tmp/opencode/corretto21` y su `bin` al inicio de `PATH`. Tras el formateo se retiraron exclusivamente cambios de espacios que el formateador produjo en dos archivos ajenos al incremento; no se cambió su comportamiento. Logs locales de sesión en `/tmp/opencode/adelanto-backend-final.log` y `/tmp/opencode/adelanto-frontend-admin-final.log`; no son artefactos publicados.
