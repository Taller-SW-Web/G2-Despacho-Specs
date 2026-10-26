# Evidencia de ES-F02-03: Consultar la cola de despachos pendientes

**Estado:** Backend implementado y verificado localmente; criterios visuales e integración de pantalla pendientes.

**Responsable de coordinación:** Tarqui.

**Última ejecución:** 16/10/2026, America/Lima.

## 1. Versión y entorno verificados

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y Gestión §3.2.
- Backend: rama `feature/f02-implementacion-specs`, base `316767f`, cambios en el árbol de trabajo.
- Java 21.0.12.1, PostgreSQL 18.6 aislado, Flyway y consultas SQL reales; JWT firmados y JWKS de prueba.
- Implementación: `ConsultarColaPendientes`, `ParametrosPendientes`, `ProgramacionPersistencia` y `ControladorProgramacion`.
- [Ejecución y comando reproducible](../../../G2-Despacho-Backend/docs/f02-implementacion-especificaciones.md), §§7–8 [cite: 1].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación ejecutada | Resultado |
|---|---|---|---|
| CA-01 | T-02 a T-05 | Estado pendiente estricto, datos de carga, orden por fecha/creación/id, metadata y paginación SQL. | Backend aprobado. |
| CA-02 | T-02, T-03, T-05 | Filtros por zona, fechas y tipo; reprogramaciones con contadores 0 y 1 se identifican desde el historial, sin incrementarlos. | Backend aprobado. |
| CA-03 | T-03, T-07, T-08 | Fecha civil de Lima, `asignable=false` y fecha de disponibilidad; comando rechaza fecha futura. | Backend aprobado; etiqueta/botón de pantalla pendientes. |
| CA-04 | T-03, T-07 | Cero coincidencias y página posterior al final: contenido vacío y totales coherentes, sin otros estados. | Backend aprobado; estado visual pendiente. |
| CA-05 | T-03, T-07 | Conserva marca `esSimulacion` y permite consultas/asignación de simulados. | Backend aprobado; badge de pantalla pendiente. |
| CA-06 | T-04, T-05 | `403` sin rol y `401` sin token según Común §3.5, sin datos operativos. | Backend aprobado aplicando el contrato canónico. |
| CUI-01 a CUI-06 | T-06 a T-08 | Composición React, filtros/KPI accionables, badges, URL y tableta. | No ejecutado en la pantalla funcional. |

## 3. Registros ejecutados

- **EV-01:** `ProgramacionHttpTests`: filtros combinados, reintentos, KPI calculados antes de filtros/página, validación de parámetros repetidos/desconocidos, fechas inválidas y control de acceso.
- **EV-02:** pendiente; la entrega previa de componentes compartidos no acredita esta pantalla.
- **EV-03:** medición local de backend: **29 ms** para 100 registros sobre 10 000 pendientes, tras calentamiento. No se ejecutó una prueba multiusuario con JMeter/Gatling ni el E2E de navegador previsto.
- Suite completa de Gestión: **69 pruebas aprobadas, 0 fallos, 0 errores y 0 omitidas**, y empaquetado correcto mediante `mvnw verify`.

## 4. Ajustes y límites

Se sigue el patrón JDBC de lectura existente en F-04 con SQL parametrizado y una transacción de lectura consistente. No se implementa el `LIKE` del plan: se comprueba una transición estructurada de F-04, de Fallido a Pendiente, con `nuevaFechaProgramada` registrada. La API no deduce reintentos del número acumulado de fallos.

La ejecución utilizó PostgreSQL externo de pruebas por ausencia de daemon Docker. La composición con F-04 se verifica sembrando su historial contractual; no acredita una reprogramación invocada contra un backend F-04 real ni conexión de la pantalla React.

## 5. Referencias

1. `G2-Despacho-Backend/docs/f02-implementacion-especificaciones.md`: comando, resultados, modelos de presentación y límites de integración.
