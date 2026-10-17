# Evidencia de ES-F05-05: Vincular repartidor con Seguridad y Usuarios

**Estado:** Parcial documental; aceptación funcional pendiente por criterio.

**Responsable de verificación:** Rhamses; revisión humana pendiente.

**Última verificación documental:** 16/10/2026. No se ejecutan nuevas pruebas de producto durante esta migración.

## 1. Versión y entorno verificados

- Fuente documental: `ES-F05-05-VincularRepartidorConSeguridad.md` en `f3849d9`; criterios conservados en [spec.md](./spec.md).
- Plan y UI: borradores de [plan.md](./plan.md) y [ui.md](./ui.md) preparados en esta migración.
- Código de referencia: frontend `9c7a99d`; backend `8f8282a`, referenciados en EV-02.
- Entorno de esta comprobación: archivos Markdown del repositorio de especificaciones; no se conectan bases ni despliegues.
- Datos: documentos y metadatos del código, sin credenciales ni datos reales de personas.
- Alcance efectivo: estructura SDD, conservación de CA, cobertura documental y enlaces. El resultado de esa revisión no acredita la ejecución de los criterios de negocio.

## 2. Cobertura de criterios

| Criterio | Tareas | Prueba o comprobación prevista | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-01 a T-04 | Conciliar el flujo antes de comprobar creación, activación y transición esperadas por el criterio original. | EV-03 | No ejecutado |
| CA-02 | T-01 a T-04 | Definir la simulación de indisponibilidad y el estado contractual esperado. | EV-03 | No ejecutado |
| CA-03 | T-01 a T-04 | Definir el rechazo de Seguridad y verificar el resultado después de conciliarlo. | EV-03 | No ejecutado |
| CA-04 | T-01 a T-04 | Confirmar si el estado de activación pertenece al vínculo local o exclusivamente a Seguridad. | EV-03 | No ejecutado |
| CA-05 | T-01 a T-04 | Conciliar el reintento y comprobar el identificador y estado finales. | EV-03 | No ejecutado |
| CA-06 | T-01 a T-04 | Comprobar fallo del reintento sin pérdida del vínculo ni duplicación una vez acordado el flujo. | EV-03 | No ejecutado |
| CA-07 | T-01 a T-04 | Verificar repetición sobre un vínculo existente y ausencia de duplicados. | EV-03 | No ejecutado |
| CUI-01 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-02 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-03 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-04 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-05 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-06 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |

Los resultados de la matriz corresponden a esta migración. La implementación previa tiene pruebas referenciadas, pero no se asigna aprobación individual a un criterio sin contrastar su escenario y sus dependencias [cite: 1, 2].

## 3. Registros de verificación

### EV-01. Migración documental a SDD

- Fecha y herramienta: 16/10/2026, Codex; revisión humana de Rhamses pendiente.
- Tareas y criterios: soporte documental de T-01 a T-04; no es una prueba de los CA ni de los CUI.
- Revisión de origen: `f3849d9`; la revisión final se identifica en el historial de esta carpeta.
- Preparación: contrastar la plantilla histórica, las plantillas SDD y los ejemplos del repositorio.
- Comprobación: verificar los cinco archivos, sus títulos/secciones, enlaces, IDs y conservación literal del bloque de criterios original; verificar cobertura de CA/CUI en tareas y evidencia.
- Resultado esperado: ninguna especificación duplicada ni referencia activa a la ruta anterior; todos los criterios conservados y trazables.
- Resultado observado: pendiente de registrar tras ejecutar la revisión final de enlaces y estructura.
- Resultado de la comprobación: Pendiente.
- Artefacto: diff y commits de migración de esta carpeta; comprobación documental resumida al cerrar este registro.
- Límite: no se ejecutan pruebas HTTP, UI, rendimiento ni integración desplegada.

### EV-02. Código y pruebas existentes como referencia

- Fuente frontend: [VinculacionRepartidor.tsx](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/apps/despacho-administrativo/src/features/flota/VinculacionRepartidor.tsx), [adaptador API](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/apps/despacho-administrativo/src/features/flota/api.ts) y [pruebas de páginas](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/apps/despacho-administrativo/src/features/flota/PaginasFlota.test.tsx).
- Fuente backend: [GestorFlota](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/8f8282a/servicio-operacion-reparto/src/main/java/com/modulodespacho/operacionreparto/servicio_operacion_reparto/flota/application/GestorFlota.java) y [GestionFlotaHttpTests](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/8f8282a/servicio-operacion-reparto/src/test/java/com/modulodespacho/operacionreparto/servicio_operacion_reparto/GestionFlotaHttpTests.java).
- Registros previos del equipo: [evidencia frontend F-05](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/docs/F-05-GestionRepartidoresFurgonetas.md) y [guía backend F-05](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/8f8282a/docs/gestion-flota.md).
- Resultado observado: existen implementaciones y pruebas de referencia para `vincular`; no se repiten sus ejecuciones ni se trasladan sus totales a una aceptación automática de esta especificación.
- Dependencias: las pruebas de backend identifican el doble JWT; las de frontend pueden usar transporte simulado. No demuestran cuentas reales ni el recorrido publicado completo.
- Resultado por criterio: pendiente de contraste en EV-03.

### EV-03. Aceptación por criterio pendiente

- Responsable: Rhamses con Calidad; participación de los propietarios de dependencias según el plan.
- Tareas y criterios: T-01 a T-04; CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07; CUI-01 a CUI-06.
- Preparación: resolver DT-01/02, identificar commit y entorno, usar datos sintéticos y comprobar permisos.
- Pasos: ejecutar la matriz del plan §6 y los escenarios UI §7; registrar cada caso, salida, efecto persistido y dependencia real o simulada.
- Resultado esperado: el definido por cada CA/CUI, después de revisar las divergencias en sus documentos propietarios.
- Resultado observado: no ejecutado durante la migración documental.
- Resultado de la comprobación: No ejecutado.
- Artefactos funcionales de esta revisión: pendientes.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción | Revisión humana |
|---|---|---|---|---|
| Migración y trazabilidad documental | Codex, 16/10/2026 | Fuente `f3849d9`, AGENTS.md, plantilla histórica, plantillas SDD, contratos, diseño y código de EV-02 | Migrar las nueve ES-F05 a carpetas SDD, conservando criterios y actualizando enlaces, con commits del usuario | Pendiente de Rhamses y del equipo |

La herramienta organiza y contrasta documentos; no se atribuye a una persona una revisión o prueba que no realizó.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterios afectados | Impacto | Acción y responsable |
|---|---|---|---|
| Los siete criterios heredados describen creación automática, activación y reintento; Seguridad §8.4 y Operación §4.1 acuerdan asociar el usuario creado previamente por ADMIN_SISTEMA. No se reemplazan esos criterios durante una migración de estructura: requieren revisión de Rhamses con Seguridad y Arquitectura antes de aceptar el comportamiento. | Criterios indicados en P-01; revisar el alcance completo | Aceptación completa pendiente | Rhamses coordina DT-01 con los propietarios |
| DTO y adaptación no ratificados completamente | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07 según la operación | El código no reemplaza el contrato | Rhamses y Arquitectura, DT-02 |
| Recorrido con dependencias reales pendiente de comprobar | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07; CUI-01 a CUI-06 | Un resultado con dobles no demuestra integración real | Calidad y propietarios externos, DT-03/04 |

## 6. Entrega y revisión

- Código de referencia: commits indicados en EV-02; no se modifica código con esta migración.
- Commits de migración documental: consultar el historial de esta carpeta; no se declara un hash antes de crearlo.
- Revisor humano y fecha: pendientes.
- Estado del alcance: parcial documental; aceptación funcional pendiente.
- Integraciones pendientes: las que exige cada criterio, con Seguridad y F-03/F-06 cuando corresponda; validar configuración y disponibilidad antes del recorrido completo.

## 7. Referencias

1. [Especificación](./spec.md) y [UI](./ui.md), criterios esperados [cite: 1].
2. [Plan](./plan.md) y [tareas](./tasks.md), incrementos y comprobaciones [cite: 2].
3. [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor) [cite: 3].
