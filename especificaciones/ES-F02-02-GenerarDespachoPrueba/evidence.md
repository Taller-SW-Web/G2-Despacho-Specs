# Evidencia de ES-F02-02: Generación de despachos de prueba para simulación

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-09, CA-20).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2).
- Commits de implementación y entorno de pruebas: pendientes.
- Alcance efectivamente verificado: preparación documental completa; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-03, T-04 | Generación exitosa con payload vacío en zona activa y fecha hoy. | EV-01 | No ejecutado |
| CA-02 | T-02, T-03, T-04 | Generación exitosa respetando zona y valores físicos personalizados. | EV-01 | No ejecutado |
| CA-03 | T-03, T-04 | Rechazo con 400/422 ante parámetros inválidos o zona inexistente. | EV-01 | No ejecutado |
| CA-04 | T-03, T-04 | Acceso sin rol GESTOR_DESPACHO rechazado con 403 Forbidden. | EV-01 | No ejecutado |
| CUI-01 | T-05 | Botón visible en cabecera con foco accesible y nombre semántico. | EV-02 | No ejecutado |
| CUI-02 | T-05 | Control en estado loading deshabilitado durante la petición en vuelo. | EV-02 | No ejecutado |
| CUI-03 | T-05, T-06 | Toast de confirmación emitido y badge "Simulado" visible en la tabla. | EV-02, EV-03 | No ejecutado |
| CUI-04 | T-05 | Notificación de error adecuada ante fallos sin romper la interfaz. | EV-02 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración del simulador backend
- Tareas asociadas: T-02, T-03, T-04.
- Comando previsto: `./mvnw test -Dtest=SimulacionControllerTest`
- Resultado: **No ejecutado**.

### EV-02. Pruebas de componentes React del botón de simulación
- Tareas asociadas: T-05.
- Comando previsto: `npm run test -- BotonGenerarPrueba.test.tsx`
- Resultado: **No ejecutado**.

### EV-03. Verificación de flujo reactivo en navegador (E2E)
- Tareas asociadas: T-06.
- Comando previsto: `npx playwright test tests/e2e/simulacion-despacho.spec.ts`
- Resultado: **No ejecutado**.
