# Plan de ES-F01-01: Consultar el catálogo de zonas de cobertura

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** Aplica; Panel de Gestión de Zonas (Pantalla 1), ruta `/zonas`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-04 | Contenido previo en `12d5041`; migración y complementos en esta carpeta. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-05 | Misma revisión documental que este plan. |
| Contrato | [Gestión §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas) y [convenciones compartidas §§3.3 y 3.5](../../integraciones/api-contract.md#3-convenciones-comunes) | `12d5041`; referencias adaptadas a la división de `0fbd89a`; filtros, paginación y DTO del listado pendientes de detalle. |
| Componentes y diseño | [Componentes React](../../disenio/componentes-react.md), §4.5; [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md); [alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md) | `12d5041`. |
| Arquitectura y datos | [C4 contenedores](../../arquitectura/c4-contenedores.md), §3.1; [modelo de datos](../../arquitectura/modelo-datos.md), §3.1 | `12d5041`. |

Este cambio prepara documentación. La modificación del contrato, el código y las pruebas de comportamiento se ejecutan en tareas posteriores. No se duplican contratos ni se da por cerrada la revisión técnica [cite: 1, 2].

## 2. Estrategia y responsabilidades

La página consume una consulta autorizada de solo lectura a través del Gateway. Gestión recupera únicamente sus datos locales, aplica filtros y paginación y devuelve el resumen permitido. El contenedor frontend adapta ese resultado a componentes visuales controlados.

| Área | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Página, filtros, consulta y adaptación del resultado | `apps/despacho-administrativo/src/features/zonas/`; `PaginaZonas.tsx` y adaptador de consulta. |
| Componentes compartidos | Presentación e interacción sin HTTP ni acceso a tokens | `packages/componentes-compartidos/src/`; CR-01/02/03/05/06/07/08/09/10/12/15. |
| Cliente de API | Petición y tratamiento del formato de errores vigente | Paquete existente `packages/cliente-api`. |
| Gateway | Enrutamiento de la consulta y propagación de identidad/correlación | `api-gateway`. |
| Gestión de Despachos | Autorización, caso de uso y persistencia de consulta | Funcionalidad `zonas/` bajo el paquete base existente, con `api`, `application`, `domain` e `infrastructure` según necesidad. |

Los nombres de clases y subpaquetes son decisiones técnicas propuestas. No se crean módulos desplegables nuevos.

## 3. Frontend y componentes React

- Verificar primero tema, proveedores, dependencias y herramientas de pruebas según §4.5.1 del documento compartido.
- Componentes compartidos: CR-03 ShellAdministrativo, CR-05 EncabezadoPagina, CR-06 BarraFiltros, CR-07 TablaDatos, CR-08 EstadoVista, CR-09 BadgeEstado, CR-15 NotificacionOperacion y CR-01/02/10; enlazados a su especificación compartida [cite: 3].
- Componentes propios: la celda de distritos con indicador «+n» y la marca de advertencia «Sin tarifa» se resuelven con el patrón de tabla y CR-09; no se crea un componente compartido nuevo salvo reutilización futura.
- Estado y datos: el contenedor mantiene filtros, página y estado de consulta, sincroniza la URL y descarta respuestas obsoletas. Los cambios de filtro reinician la página.
- Cliente de API: `GET /api/v1/zonas`; el adaptador transforma la respuesta al modelo de UI y aplica el formato de errores.
- Mock: antes del contrato completo pueden usarse fixtures de presentación para los estados de UI; no representan respuestas HTTP definitivas.

## 4. Backend, persistencia e integraciones

- Entrada: `GET /api/v1/zonas`. Autorizar el JWT humano y exigir `GESTOR_DESPACHO`; el cliente no sustituye esta comprobación.
- Caso de uso: consultar zonas con filtros combinados y paginación, incorporando la tarifa vigente o su ausencia y la última modificación.
- Datos locales: `zonas`, `zona_distritos` y `tarifas_zona`. Resolver la tarifa vigente (`activa=true`) por zona antes de componer la página.
- Migración: revisar el esquema existente y su gestión con Arquitectura; crear migraciones Flyway solo para cambios necesarios. No asumir que las tablas ya están disponibles por aparecer en el modelo.
- Integraciones: ninguna con otros módulos; la operación es de solo lectura y no publica eventos.
- Efectos secundarios: no crea ni modifica recursos; no requiere clave de idempotencia.
- Fechas: el modelo establece `America/Lima` para presentación y UTC para instantes. La «última modificación» procede de `actualizado_en`.
- Errores: aplicar el formato central de §3.5; concretar los errores de filtros en el contrato antes de implementar el adaptador real.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Componentes requeridos disponibles y página aislada con fixtures identificados | Base frontend y CR de §3; no necesita una API real | CUI-01 a CUI-05, solo presentación/interacción |
| I-02 | Contrato y consulta backend implementados y probados | DT-01, persistencia y JWT disponibles para la prueba completa | CA-01 a CA-04 |
| I-03 | Página conectada y verificación del recorrido real | I-01 e I-02 | CA-01 a CA-04 y CUI-01 a CUI-05 |

La definición contractual puede prepararse mientras se desarrolla I-01.

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | Filtros combinados, paginación y campos de cada fila | Integración PostgreSQL del backend y recorrido UI | Real para backend; fixtures para UI aislada |
| CA-02 | Vacío, sin coincidencias y recuperación ante error | Backend con cero zonas/coincidencias; UI con fixtures y API | Real y simulada |
| CA-03 | Zona `ACTIVO` sin tarifa vigente | Datos sintéticos con tarifa y sin ella | Real |
| CA-04 | Rechazar usuario con otro rol o sin token sin datos | Pruebas de seguridad del endpoint y de interacción | Real |

Comandos previstos: desde el frontend, `npm run typecheck` y `npm run build`; desde Gestión, `./mvnw.cmd test`. Las pruebas con Testcontainers requieren Docker. Los resultados y la distinción entre dobles y servicios reales se anotan en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Justificación y fuente | Responsable | Bloquea qué incremento |
|---|---|---|---|---|
| DT-01 | Nombres y límites de filtros, paginación y orden; DTO de filas, tarifa vigente, estado y última modificación; catálogo de distritos y estados | Gestión §3.1 (tabla de rutas) y DC-04 del documento compartido | Valqui con Backend/Frontend y Arquitectura | Adaptadores HTTP de I-02/03; no los fixtures de I-01 |
| DT-02 | Fuente exacta de la última modificación (`actualizado_en` de `zonas` y de la tarifa) y su presentación | Modelo de datos §3.1 | Valqui con Arquitectura | CA-01 e integración real |
| DT-03 | Esquema/migraciones necesarios y base compartida de JWT, errores, conexión de datos y rutas del Gateway | Inicialización actual del backend y modelo | Valqui coordina con Arquitectura y DevOps | Ejecución real de I-02/03 |
| DT-04 | Disponibilidad y verificación de componentes, tema y herramientas de pruebas | Componentes React §§4.5–4.6 | Valqui para los CR consumidos; coordinación con los responsables del resto | Composición y aceptación de I-01 según sus dependencias |
| DT-05 | Conciliación entre `zona_distritos` (modelo §6) y `zonas_distritos` (modelo §3.1) y su efecto en la resolución de filtros por distrito | Modelo de datos §3.1 y §6 | Valqui con Arquitectura | CA-01/02 e integración real |

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas del incremento están revisadas y los pendientes bloqueantes resueltos.
- [ ] Los componentes requeridos están verificados antes de componer la pantalla consumidora.
- [ ] Las tareas cubren todos los criterios y tienen una comprobación concreta.
- [ ] La consulta respeta el contrato de Gestión, las convenciones compartidas y la propiedad de datos.
- [ ] Todos los criterios del alcance cuentan con evidencia, distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas), [convenciones compartidas](../../integraciones/api-contract.md#3-convenciones-comunes), [modelo de datos](../../arquitectura/modelo-datos.md) y [arquitectura de contenedores](../../arquitectura/c4-contenedores.md).
3. [Componentes React](../../disenio/componentes-react.md), [sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [flujo SDD](../../plantillas/sdd/README.md).
