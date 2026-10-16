# Evidencia de ES-F02-03: Consultar la cola de despachos pendientes

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-02, RF-06; CA-03, CA-04, CA-05, CA-13).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2).
- Commits de implementación y entorno de pruebas: pendientes.
- Alcance efectivamente verificado: preparación técnica y documental completada; ningún criterio funcional se declara aprobado antes de la ejecución de pruebas reales.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-03, T-04, T-05 | Consulta paginada con columnas obligatorias y orden fecha programada asc. | EV-01 | No ejecutado |
| CA-02 | T-02, T-03, T-05 | Filtro por zona y por tipo de intento (Todos / Primer intento / Reintentos). | EV-01 | No ejecutado |
| CA-03 | T-03, T-07, T-08 | Despachos programados a futuro con etiqueta y botón Asignar bloqueado. | EV-01, EV-02 | No ejecutado |
| CA-04 | T-03, T-07 | Estado vacío amigable cuando no hay despachos pendientes. | EV-01, EV-02 | No ejecutado |
| CA-05 | T-03, T-07 | Despachos simulados destacados con badge punteado "Simulado". | EV-02 | No ejecutado |
| CA-06 | T-04, T-05 | Petición sin rol GESTOR_DESPACHO rechazada con 403 Forbidden. | EV-01 | No ejecutado |
| CUI-01 | T-06, T-08 | Tabla completa con datos de carga y formato adecuado. | EV-02 | No ejecutado |
| CUI-02 | T-06, T-08 | Clic en tarjetas KPI filtra interactivamente la tabla. | EV-02 | No ejecutado |
| CUI-03 | T-07, T-08 | Botón Asignar deshabilitado con tooltip en despachos futuros. | EV-02 | No ejecutado |
| CUI-04 | T-07, T-08 | Visualización correcta del badge "Simulado". | EV-02 | No ejecutado |
| CUI-05 | T-08 | Sincronización bidireccional de parámetros en la URL. | EV-02, EV-03 | No ejecutado |
| CUI-06 | T-06 | Ocultamiento de columnas secundarias en tableta (1024 px). | EV-02 | No ejecutado |

## 3. Registros de verificación previstos

### EV-01. Pruebas de integración de la API de consulta
- Tareas asociadas: T-02, T-03, T-04, T-05.
- Comando previsto: `./mvnw test -Dtest=ColaPendientesControllerTest`
- Resultado: **No ejecutado**.

### EV-02. Pruebas de componentes React de la cola
- Tareas asociadas: T-06, T-07, T-08.
- Comando previsto: `npm run test -- PaginaProgramacion.test.tsx`
- Resultado: **No ejecutado**.

### EV-03. Pruebas de rendimiento y E2E
- Tareas asociadas: T-05, T-08.
- Comando previsto: `npx playwright test tests/e2e/cola-pendientes.spec.ts`
- Resultado: **No ejecutado**.
