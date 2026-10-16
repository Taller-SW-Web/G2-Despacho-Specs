# Evidencia de ES-F02-05: Consultar y reordenar la secuencia de ruta

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

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
| CUI-01 | T-06 | Presentación ordenada y numerada de las paradas de la jornada. | EV-02 | No ejecutado |
| CUI-02 | T-06 | Bloqueo visual de manijas de arrastre en paradas en camino o cerradas. | EV-02 | No ejecutado |
| CUI-03 | T-07 | Aparición de barra fija ante cambios y descarte exitoso restaurando orden. | EV-02 | No ejecutado |
| CUI-04 | T-06 | Operación de subir/bajar ejecutable mediante teclado de forma accesible. | EV-02 | No ejecutado |
| CUI-05 | T-07 | Guardado con spinner, toast de éxito y consolidación de la nueva ruta. | EV-02, EV-03 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración de la API de ruta y secuencia
- Tareas asociadas: T-02, T-03, T-04, T-05.
- Comando previsto: `./mvnw test -Dtest=RutaJornadaControllerTest`
- Resultado: **No ejecutado**.

### EV-02. Pruebas de componentes React de Drag & Drop y barra fija
- Tareas asociadas: T-06, T-07.
- Comando previsto: `npm run test -- ListaParadasDnd.test.tsx`
- Resultado: **No ejecutado**.

### EV-03. Pruebas de flujo E2E
- Tareas asociadas: T-05, T-07.
- Comando previsto: `npx playwright test tests/e2e/secuencia-ruta.spec.ts`
- Resultado: **No ejecutado**.
