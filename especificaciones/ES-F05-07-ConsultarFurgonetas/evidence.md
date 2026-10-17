# Evidencia de ES-F05-07: Consultar furgonetas

**Estado:** Parcial documental; aceptación funcional pendiente por criterio.

**Responsable de verificación:** Rhamses; revisión humana pendiente.

**Identificación de la verificación:** commits de Git y registros EV.

## 1. Versión y entorno verificados

- Fuente documental: `ES-F05-07-ConsultarFurgonetas.md` en `f3849d9`; IDs conservados; cambios funcionales posteriores en EV-04 y [spec.md](./spec.md).
- Plan y UI: borradores de [plan.md](./plan.md) y [ui.md](./ui.md) preparados en esta migración.
- Código de referencia: frontend `9c7a99d`; backend `8f8282a`, referenciados en EV-02.
- Entorno de esta comprobación: archivos Markdown del repositorio de especificaciones; no se conectan bases ni despliegues.
- Datos: documentos y metadatos del código, sin credenciales ni datos reales de personas.
- Alcance efectivo: estructura SDD, conservación de CA, cobertura documental y enlaces. El resultado de esa revisión no acredita la ejecución de los criterios de negocio.

## 2. Cobertura de criterios

| Criterio | Tareas | Prueba o comprobación prevista | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-01 a T-04 | Listado con furgonetas; contrastar el escenario de spec.md y sus efectos persistidos. | EV-03 | No ejecutado |
| CA-02 | T-01 a T-04 | Filtro por estado; contrastar el escenario de spec.md y sus efectos persistidos. | EV-03 | No ejecutado |
| CA-03 | T-01 a T-04 | Búsqueda por placa; contrastar el escenario de spec.md y sus efectos persistidos. | EV-03 | No ejecutado |
| CA-04 | T-01 a T-04 | Listado vacío; contrastar el escenario de spec.md y sus efectos persistidos. | EV-03 | No ejecutado |
| CA-05 | T-01 a T-04 | Acceso sin permisos; contrastar el escenario de spec.md y sus efectos persistidos. | EV-03 | No ejecutado |
| CUI-01 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-02 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-03 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-04 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-05 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |
| CUI-06 | T-01, T-03, T-04 | Escenario de ui.md §7 | EV-03 | No ejecutado |

Los resultados de la matriz corresponden a esta migración. La implementación previa tiene pruebas referenciadas, pero no se asigna aprobación individual a un criterio sin contrastar su escenario y sus dependencias [cite: 1, 2].

## 3. Registros de verificación

### EV-01. Migración documental a SDD

- Fecha y herramienta: revisión documental de F-05, Codex; revisión humana de Rhamses pendiente.
- Tareas y criterios: soporte documental de T-01 a T-04; no es una prueba de los CA ni de los CUI.
- Revisión de origen: `f3849d9`; la revisión final se identifica en el historial de esta carpeta.
- Preparación: contrastar la plantilla histórica, las plantillas SDD y los ejemplos del repositorio.
- Comprobación: verificar los cinco archivos, sus títulos/secciones, enlaces, IDs y conservación literal del bloque de criterios original; verificar cobertura de CA/CUI en tareas y evidencia.
- Resultado esperado: ninguna especificación duplicada ni referencia activa a la ruta anterior; todos los criterios conservados y trazables.
- Resultado observado: revisión documental aprobada para las nueve carpetas: 45 archivos SDD, 47 criterios CA originales conservados literalmente, 54 criterios CUI con trazabilidad y 871 enlaces locales revisados, sin errores.
- Resultado de la comprobación: Aprobado, exclusivamente para la migración documental.
- Artefacto: [commit de migración 15f726a](https://github.com/Taller-SW-Web/G2-Despacho-Specs/commit/15f726a) y diff frente a `f3849d9`. La revisión comparó bloques CA, secciones de plantilla, tablas de cobertura y destinos/anclas de enlaces locales.
- Límite: no se ejecutan pruebas HTTP, UI, rendimiento ni integración desplegada.

### EV-02. Código y pruebas existentes como referencia

- Fuente frontend: [PaginaFurgonetas.tsx](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/apps/despacho-administrativo/src/features/flota/PaginaFurgonetas.tsx), [adaptador API](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/apps/despacho-administrativo/src/features/flota/api.ts) y [pruebas de páginas](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/apps/despacho-administrativo/src/features/flota/PaginasFlota.test.tsx).
- Fuente backend: [GestorFlota](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/8f8282a/servicio-operacion-reparto/src/main/java/com/modulodespacho/operacionreparto/servicio_operacion_reparto/flota/application/GestorFlota.java) y [GestionFlotaHttpTests](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/8f8282a/servicio-operacion-reparto/src/test/java/com/modulodespacho/operacionreparto/servicio_operacion_reparto/GestionFlotaHttpTests.java).
- Registros previos del equipo: [evidencia frontend F-05](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/docs/F-05-GestionRepartidoresFurgonetas.md) y [guía backend F-05](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/8f8282a/docs/gestion-flota.md).
- Resultado observado: existen implementaciones y pruebas de referencia para `listarFurgonetas`; no se repiten sus ejecuciones ni se trasladan sus totales a una aceptación automática de esta especificación.
- Dependencias: las pruebas de backend identifican el doble JWT; las de frontend pueden usar transporte simulado. No demuestran cuentas reales ni el recorrido publicado completo.
- Resultado por criterio: pendiente de contraste en EV-03.

### EV-03. Aceptación por criterio pendiente

- Responsable: Rhamses con Calidad; participación de los propietarios de dependencias según el plan.
- Tareas y criterios: T-01 a T-04; CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06.
- Preparación: revisar DT-01/02, identificar commit y entorno, usar datos sintéticos y comprobar permisos.
- Pasos: ejecutar la matriz del plan §6 y los escenarios UI §7; registrar cada caso, salida, efecto persistido y dependencia real o simulada.
- Resultado esperado: el definido por cada CA/CUI, después de revisar las divergencias en sus documentos propietarios.
- Resultado observado: no ejecutado durante la migración documental.
- Resultado de la comprobación: No ejecutado.
- Artefactos funcionales de esta revisión: pendientes.

### EV-04. Alineación con frontend y backend

- Alcance: revisión de las nueve ES-F05 y Operación §4.1 frente al código de flota. La revisión final queda identificada por los commits de esta entrega.
- Versiones de esta entrega: [frontend `1d688a5`](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/commit/1d688a5) y [backend `cecda68`](https://github.com/Taller-SW-Web/G2-Despacho-Backend/commit/cecda68).
- Comprobación documental: 45 archivos SDD, 47 IDs CA, 54 CUI y 896 enlaces locales revisados sin errores. Se conservan los IDs; la redacción modificada se documenta a continuación.
- Cambio de requisitos: se mantienen los 47 IDs CA; ES-F05-01/05 sustituyen la provisión automática heredada por registro local y asociación manual acordada con Seguridad §8.4. ES-F05-02 usa los estados locales vigentes y ES-F05-09 aclara la rehabilitación. EV-01 describe exclusivamente la migración histórica anterior.
- Contrato: DTO, límites, errores, idempotencia, carga pendiente, cierre de jornadas vacías y traducción de estados centralizados en Operación §4.1 [cite: 3].
- Frontend: validación de precisión y rangos, filtros/página y acción de vinculación; pruebas de interacción con transporte simulado. Resultado: 51 pruebas F-05 aprobadas, verificación de tipos y construcción de ambas aplicaciones aprobadas. La guía frontend de EV-02 conserva el historial previo y registra esta revisión en su versión posterior.
- Backend: filtro de perfil activo/vinculado y respuesta de indisponibilidad; pruebas adicionales de flota y de acceso. Resultado: compilación de producción y pruebas aprobada; siete pruebas unitarias de seguridad y 23 del Gateway aprobadas sin Docker. Los dobles JDBC/JWT no acreditan la consulta real de perfiles; el filtro completo se comprueba en la suite PostgreSQL pendiente.
- Límite: las nuevas pruebas PostgreSQL, concurrencia, exportación de respuestas y medición local no se acreditan como ejecutadas en esta revisión. Docker quedó apagado por indicación del usuario. No se usa Supabase como sustituto para pruebas que limpian datos.
- Aceptación: la evidencia local no completa EV-03 ni certifica los 200 ms en Render, la revisión visual humana, cuentas reales de Seguridad o el recorrido F-03/F-06. Seguridad continúa sin despliegue disponible.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción | Revisión humana |
|---|---|---|---|---|
| Migración y trazabilidad documental | Codex, revisión documental de F-05 | Fuente `f3849d9`, AGENTS.md, plantilla histórica, plantillas SDD, contratos, diseño y código de EV-02 | Migrar las nueve ES-F05 a carpetas SDD, conservando criterios y actualizando enlaces, con commits del usuario | Pendiente de Rhamses y del equipo |

La herramienta organiza y contrasta documentos; no se atribuye a una persona una revisión o prueba que no realizó.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterios afectados | Impacto | Acción y responsable |
|---|---|---|---|
| Alineado con Operación §4.1: registro local, asociación manual de UUID y estados `PENDIENTE`/`VINCULADO`; sin creación automática de cuentas ni rol global de repartidor. Los efectos integrados en F-03/F-06 siguen pendientes. | Criterios de spec.md; integración pendiente | Aceptación completa pendiente | Rhamses coordina DT-01 con los propietarios |
| Contrato ampliado; aceptación integrada pendiente | CA-01, CA-02, CA-03, CA-04, CA-05 según la operación | El código no reemplaza el contrato | Rhamses y Arquitectura, DT-02 |
| Recorrido con dependencias reales pendiente de comprobar | CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06 | Un resultado con dobles no demuestra integración real | Calidad y propietarios externos, DT-03/04 |

## 6. Entrega y revisión

- Código de referencia: EV-02 conserva el historial previo; EV-04 registra la revisión que también ajusta frontend y backend en sus repositorios.
- Commit de migración documental: [15f726a](https://github.com/Taller-SW-Web/G2-Despacho-Specs/commit/15f726a); la verificación documental posterior se identifica en el historial de esta carpeta.
- Revisor humano y fecha: pendientes.
- Estado del alcance: parcial documental; aceptación funcional pendiente.
- Integraciones pendientes: las que exige cada criterio, con Seguridad y F-03/F-06 cuando corresponda; validar configuración y disponibilidad antes del recorrido completo.

## 7. Referencias

1. [Especificación](./spec.md) y [UI](./ui.md), criterios esperados [cite: 1].
2. [Plan](./plan.md) y [tareas](./tasks.md), incrementos y comprobaciones [cite: 2].
3. [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor) [cite: 3].
