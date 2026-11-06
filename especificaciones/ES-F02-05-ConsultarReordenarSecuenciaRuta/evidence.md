# Evidencia de ES-F02-05: Consultar y reordenar la secuencia de ruta

**Estado:** Consulta y subconjunto seguro de reordenamiento verificados localmente con API simulada; integración real y aclaración de huecos pendientes.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** 05/11/2026, consumidor con API simulada y Chromium; integración persistente pendiente.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-06, CA-14).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2).
- Commits de implementación y entorno de pruebas: pendientes.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-05 | Consulta exitosa de la ruta completa ordenada por posición con estados. | EV-01 | No ejecutado |
| CA-02 | T-03, T-04, T-05 | Reordenamiento exitoso de paradas ASIGNADO sin huecos ni duplicados. | EV-01, EV-03 | No ejecutado |
| CA-03 | T-03, T-05 | Rechazo con 409 al intentar cambiar posición de despachos en camino o cerrados. | EV-01 | No ejecutado |
| CA-04 | T-03, T-05 | Rechazo con 400 Bad Request ante secuencia discontinua o duplicada. | EV-01 | No ejecutado |
| CA-05 | T-04, T-05 | Rechazo con 409 si un despacho pasa a EN_CAMINO en F-03 concurrentemente. | EV-01 | No ejecutado |
| CA-06 | T-02, T-04, T-05 | Petición sin rol GESTOR_DESPACHO rechazada con 403 Forbidden. | EV-01 | No ejecutado |
| CUI-01 | T-06 | Presentación ordenada y numerada de las paradas de la jornada. | EV-04 | Verificado localmente; huecos históricos conservados, aceptación integral pendiente |
| CUI-02 | T-06 | Bloqueo visual de manijas de arrastre en paradas en camino o cerradas. | EV-04 | Verificado con API simulada |
| CUI-03 | T-07 | Aparición de barra fija ante cambios y descarte exitoso restaurando orden. | EV-04 | Verificado con API simulada para rutas continuas |
| CUI-04 | T-06 | Operación de subir/bajar ejecutable mediante teclado de forma accesible. | EV-04 | Verificado con API simulada para rutas continuas |
| CUI-05 | T-07 | Guardado con spinner, toast de éxito y consolidación de la nueva ruta. | EV-04 | Verificado con API simulada; persistencia real pendiente |

## 3. Registros de verificación

### EV-01. Pruebas de integración de la API de ruta y secuencia
- Tareas asociadas: T-02, T-03, T-04, T-05.
- Comando previsto: `./mvnw test -Dtest=RutaJornadaControllerTest`
- Resultado: **No ejecutado**.

### EV-04. Incremento seguro de rutas del Hito 4 · 05/11/2026

- Rama `feature/f02-ejecucion-hito4` sobre frontend `5c42d46`, backend `e2d10b7` y documentación `637fa8d`, conservando los cambios locales anteriores. Sin nuevo commit aprobado, PR ni despliegue.
- `RutasProgramacion.tsx` habilita la pestaña, selector de jornadas desde monitoreo paginado (incluidas saturadas), consulta de ruta desde Gestión, estados y marcas temporales. Las lecturas cancelan/descartan respuestas obsoletas y se renuevan cada 30 segundos/foco sin edición activa.
- Reordenamiento por arrastre nativo o botones de teclado, conservando fijas las paradas no `ASIGNADO`. CR-13 permite guardar/descartar, bloquea cambio de pestaña/jornada mientras hay cambios y conserva el comando exacto ante resultado incierto. `If-Match` usa la versión de **ruta**, no la versión numérica de una parada.
- **Límite explícito:** no se renumeran huecos históricos. Rutas no continuas siguen consultables pero no editables desde esta UI; también bloquean edición la jornada cerrada y los comandos pendientes. No se declara satisfecho el criterio integral de continuidad frente a cancelaciones/reasignaciones hasta resolver la aclaración. Los CA y antecedentes de EV-01/02/03 se conservan; no se atribuye su ejecución a clases o comandos previstos que no existen.
- `RutasProgramacion.test.tsx` verifica consulta pública, estados fijos, teclado, descarte sin PUT, guardado único, versiones/UUID, arrastre, huecos, cierre, cercos, conflictos, recuperación exacta, permisos, cambio de sesión y validación de respuestas. `rutasModelo.test.tsx` verifica siete casos de permutación y validación del proveedor. El `scrollIntoView` ausente de JSDOM se sustituye únicamente en la prueba; el desplazamiento real se comprueba en Chromium.
- `pruebas/f02/rutas.spec.ts` ejecuta en Chromium los flujos de consulta, edición y reasignación recuperable en 1440×1024, 1024×768 y 390×844, con APIs **interceptadas**. Verifica ausencia de desbordamiento, conservación del estado/posición iniciados, versión actualizada tras guardar, recuperación de la misma transferencia y consulta del destino sin caché. Capturas sintéticas en `docs/evidencia/f02/hito4/ruta-{1440,1024,390}.png` y `reasignacion-{1440,1024,390}.png` del frontend, aún locales.
- Comandos ejecutados: `NODE_OPTIONS=--no-experimental-webstorage npm run test:administrativo` (**209 pruebas**, 21 archivos), `npm run typecheck`, `npm run build` y `npm run test:f02:e2e` (**7 recorridos**, de ellos 3 de rutas). Resultado correcto con Node 26.13.0 y dependencias existentes, sin actualizar lockfile. La compilación conserva la advertencia de tamaño de chunks. La selección de jornada en JSDOM se comprueba por teclado; Chromium comprueba la selección con puntero. Se añadió regresión del retorno al orden original y su renovación posterior, sin conservar un borrador que oculte paradas nuevas.
- Backend: se corrigió el perfil `render` del Gateway, cuya lista reemplazaba la ruta específica de Gestión. `RutasProgramacionRenderTests` comprueba destino correcto, ETag, CORS, cabeceras/cuerpo de secuencia y reasignación, denegación anónima y aislamiento de rutas internas. `clean verify` de Gateway con Corretto 21.0.13: **29 pruebas aprobadas**; son proveedores e identidad de prueba, no servicios publicados.
- Se precisó el transporte canónico en [Gestión §3.2.1](../../integraciones/api-contract-gestion-despachos.md#321-consulta-de-ruta-y-transporte-de-secuencia) sin modificar la regla de huecos. Se mantienen pendientes Docker para persistencia, identidad interna, G7 y aceptación humana del hito.

### EV-02. Pruebas de componentes React de Drag & Drop y barra fija
- Tareas asociadas: T-06, T-07.
- Comando previsto: `npm run test -- ListaParadasDnd.test.tsx`
- Resultado: **No ejecutado**.

### EV-03. Pruebas de flujo E2E
- Tareas asociadas: T-05, T-07.
- Comando previsto: `npx playwright test tests/e2e/secuencia-ruta.spec.ts`
- Resultado: **No ejecutado**.
