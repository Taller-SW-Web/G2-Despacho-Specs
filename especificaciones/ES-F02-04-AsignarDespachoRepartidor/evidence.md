# Evidencia de ES-F02-04: Asignar despacho a un repartidor

**Estado:** Modal y barras verificados localmente con API simulada; integración real, persistencia y aceptación pendientes.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** 05/11/2026, consumidor con APIs simuladas y navegador Chromium; servicios reales no verificados.

## 1. Versión y entorno verificados

### Incremento del 30/10/2026

- Frontend `feature/f02-cierre-criterios` desde `develop` `6520f8f`. Se exigieron placa, límites positivos y ocupación de F-06; sin esos campos la consulta falla, no se fabrican porcentajes. Se mantienen selección por zona, rechazo tridimensional y verificación final del backend.
- Pruebas F-02: 13 aprobadas. Chromium: 4 recorridos con APIs simuladas aprobados. Tipos y build correctos. La prueba de asignación comprueba tres barras por candidato, placa y búsqueda por placa antes de confirmar.
- Suite administrativa serial: 167 aprobadas y dos fallos previos de `Zonas.test.tsx`, sin modificar sus aserciones. No equivale a suite general verde.
- No se pudo actualizar frontend desde GitHub (autenticación SSH rechazada). El checkout local no incluye todavía las rutas/reasignación de la rama funcional. El backend sí parte del develop integrado `e4f8ee1`. La verificación conjunta requiere actualizar ese checkout y Docker disponible; no se repitió el runner G2 real.
- La evidencia histórica siguiente conserva su alcance; no se declaran aprobados los criterios de integración real por las pruebas con fixtures.

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-03, RF-06; CA-06 a CA-09).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2) y `integraciones/api-contract-operacion-reparto.md` (§5.1).
- Commits de implementación y entorno de pruebas: pendientes.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-03, T-05, T-06 | Asignación exitosa con reserva tridimensional en F-06 y estado ASIGNADO con secuencia. | EV-01, EV-03 | No ejecutado |
| CA-02 | T-02, T-06 | Rechazo con 422 ante capacidad excedida en peso, volumen o paquetes. | EV-01 | No ejecutado |
| CA-03 | T-02, T-06 | Rechazo con 409 ante repartidor no habilitado (fuera de turno o saturado). | EV-01 | No ejecutado |
| CA-04 | T-03, T-06 | Rechazo con 409 por colisión de versión optimista ante asignación concurrente. | EV-01 | No ejecutado |
| CA-05 | T-03, T-06 | Rechazo con 409 al intentar asignar despacho con fecha programada futura. | EV-01 | No ejecutado |
| CA-06 | T-02, T-06 | Rechazo con 409 si la reserva previa de un reprogramado no se ha liberado. | EV-01 | No ejecutado |
| CA-07 | T-05, T-06 | Petición sin rol GESTOR_DESPACHO rechazada con 403 Forbidden. | EV-01 | No ejecutado |
| CUI-01 | T-07 | Modal muestra datos de carga completos del despacho al abrirse. | EV-04 | Aprobado localmente con API simulada; nube pendiente |
| CUI-02 | T-07 | Repartidores agrupados priorizando los de la zona de destino. | EV-04 | Aprobado localmente con API simulada; nube pendiente |
| CUI-03 | T-07 | Proyección sombreada en barras de capacidad al seleccionar repartidor. | EV-04 | Aprobado localmente con API simulada; proveedor real pendiente |
| CUI-04 | T-07 | Bloqueo visual de tarjeta y botón de confirmación ante sobrecarga. | EV-04 | Aprobado localmente con API simulada; backend pendiente |
| CUI-05 | T-07 | Spinner en botón "Confirmar" impidiendo dobles clics. | EV-04 | Aprobado localmente con API simulada; backend pendiente |
| CUI-06 | T-08 | Cierre de modal, toast emitido y retiro de la cola tras asignación exitosa. | EV-04 | Aprobado localmente con API simulada; integración real pendiente |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración del caso de uso de asignación
- Tareas asociadas: T-02, T-03, T-04, T-05, T-06.
- Comando previsto: `./mvnw test -Dtest=AsignarDespachoIntegrationTest`
- Resultado: **No ejecutado**.

### EV-02. Pruebas de componentes React del modal de asignación
- Tareas asociadas: T-07, T-08.
- Comando previsto: `npm run test -- ModalAsignacionDespacho.test.tsx`
- Resultado: **No ejecutado**.

### EV-03. Pruebas de flujo E2E
- Tareas asociadas: T-06, T-08.
- Comando previsto: `npx playwright test tests/e2e/asignacion-despacho.spec.ts`
- Resultado: **No ejecutado**.

### EV-04. Incremento local del Hito 4 · 05/11/2026

- Base: frontend `5c42d46`, backend `e2d10b7`, documentación `637fa8d`, rama `feature/f02-ejecucion-hito4` en los tres repositorios. Incremento aún sin commit, revisión de pares ni despliegue; no existe un SHA aprobado nuevo que atribuirle.
- Alcance implementado: `ModalAsignacion.tsx` consume placa, límites y ocupación ya publicados por Operación §4.2. Búsqueda por placa, tres barras CR-11/CR-20 y proyección de ocupación más carga en el candidato seleccionado y en los candidatos sobrecargados, donde explica el exceso sin permitir seleccionarlos. `modelo.ts` rechaza campos omitidos, límites no positivos, identidades repetidas y remanentes incoherentes. El backend mantiene la autoridad para reservar.
- Fuentes contrastadas: contrato canónico de [Operación §4.2](../../integraciones/api-contract-operacion-reparto.md#42-jornadas-y-monitoreo) y captura sintética backend `servicio-gestion-despachos/src/test/resources/contratos/f06-respuestas-backend.json`. No se consultó un proveedor publicado; no se modificó su contrato para obtener las barras.
- Entorno: Linux; Node 26.13.0, Vitest y Chromium de las dependencias existentes. Se reutilizó `node_modules`; no se ejecutó `npm ci` ni se cambió el lockfile. Vitest se lanzó con `NODE_OPTIONS=--no-experimental-webstorage` para utilizar el almacenamiento de JSDOM.

| Comprobación desde la raíz frontend | Resultado observado | Límite |
|---|---|---|
| `NODE_OPTIONS=--no-experimental-webstorage npm run test:administrativo` | 186 pruebas aprobadas en 19 archivos; incluye 15 de `PaginaProgramacion.test.tsx` y 10 de `modelo.test.tsx`. | APIs simuladas; no prueba PostgreSQL ni G7. |
| `NODE_OPTIONS=--no-experimental-webstorage npm test` | 208 pruebas compartidas aprobadas. | Regresión de componentes, no integración entre servicios. |
| `NODE_OPTIONS=--no-experimental-webstorage npm run test -w @despacho/repartidor` | 13 pruebas aprobadas. | Consumidor de F-03 con dobles; no acredita ruta propia publicada. |
| `npm run typecheck` y `npm run build` | Tipos y construcción de ambas apps aprobados; advertencia Vite de chunks mayores de 500 kB. | No equivale a despliegue. |
| `npm run test:f02:e2e` | 4 recorridos Chromium aprobados: escritorio, tableta, móvil y generación/asignación. Se añadió comprobación accesible de proyección y placa. | Vite con API interceptada, sin cuentas reales. |

Los casos de esta atómica se cubren con `PaginaProgramacion.test.tsx`: resumen, zona prioritaria, bloqueo tridimensional, doble envío, respuestas antiguas, permisos, `409`/`422`, resultado incierto y renovación de capacidad; se añadieron búsqueda por placa y bloqueo ante respuesta incoherente. `modelo.test.tsx` añade diez comprobaciones de integridad del proveedor. El primer ensayo de búsqueda falló por contar radios de filtros fuera del modal; se acotó la consulta al diálogo y la suite completa volvió a pasar. Una prueba de renovación actualizó también la ocupación de su fixture al variar el remanente, para no simular una respuesta físicamente incoherente.

Capturas nuevas, con datos exclusivamente sintéticos, en el frontend:

- [Asignación escritorio](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/feature/f02-ejecucion-hito4/docs/evidencia/f02/hito4/asignacion-1440.png).
- [Asignación tableta](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/feature/f02-ejecucion-hito4/docs/evidencia/f02/hito4/asignacion-1024.png).
- [Asignación móvil](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/feature/f02-ejecucion-hito4/docs/evidencia/f02/hito4/asignacion-390.png).

Los enlaces remotos anteriores son destinos previstos: la rama y las capturas están únicamente locales hasta publicar el PR. Se preservaron las capturas históricas del 17/10 en su ubicación anterior. La comprobación en navegador cubre overflow, navegación por flechas, selección, foco y cierre; no se afirma una auditoría manual con lector de pantalla.

Backend: los tres `clean verify` se repitieron con Corretto 21.0.13 temporal, tras un fallo de compilación con el JDK 27 instalado. Gateway aprueba 28 pruebas. Gestión compila pero su suite no aprueba (184 contabilizadas, 129 errores de contexto); Operación compila pero tampoco aprueba (131 contabilizadas, 47 errores). Testcontainers no encuentra el daemon Docker, sin usar una base compartida como sustituto ni omitir los tests. CA-01 a CA-07 de esta atómica siguen sin aceptación de integración.

Se añadió al backend `pruebas/verificar_f02_publicado.py` para comprobar por GET una asignación ya preparada y su coincidencia en F-03, sin tokens en el reporte. Sus siete pruebas con dobles pasan y se incorporan a CI; **el verificador contra nube no se ejecutó**. Requiere origen, IDs, sesiones de gestor y dos repartidores, y revisión publicada. Tampoco prueba por sí solo la reserva antes/después, MFA, fallo con evidencia o recepción/reprogramación. Continuar según el [registro del Hito 4](../../hitos/Plan_Hito_4_F02.md#7-registro-de-ejecución-del-05112026).
