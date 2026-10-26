# Plan de ES-F01-03: Activar y desactivar una zona de cobertura

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** Aplica; confirmación de desactivación de zona (Pantalla 4), iniciada desde `/zonas`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-06 | Contenido previo en `12d5041`; migración en esta carpeta. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-07 | Misma revisión documental que este plan. |
| Contrato | [Gestión §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas), [roles §3.3](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio) e [idempotencia §9](../../integraciones/api-contract.md#9-reglas-de-idempotencia-y-concurrencia) | `12d5041`; referencias adaptadas a la división de `0fbd89a`; formato del `409` pendiente de detalle. |
| Componentes y diseño | [Componentes React](../../disenio/componentes-react.md), §4.5; [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | `12d5041`. |
| Arquitectura y datos | [C4 contenedores](../../arquitectura/c4-contenedores.md), §3.1; [modelo de datos](../../arquitectura/modelo-datos.md), §3.1 | `12d5041`. |

Este cambio prepara documentación. La modificación del contrato, el código y las pruebas se ejecutan en tareas posteriores. No se duplican contratos ni se da por cerrada la revisión técnica [cite: 1, 2].

## 2. Estrategia y responsabilidades

El cambio de estado se aplica a través del Gateway con autorización administrativa. Gestión valida el estado actual, la ausencia de solapamiento en la activación y la versión de la zona, y resuelve la operación de forma idempotente. La confirmación visual se resuelve en el frontend, que nunca desactiva directamente desde la tabla. Los consumidores (F-02 y los canales) observan el efecto sin recibir notificaciones.

| Área | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Confirmación, envío y refresco de la fila | `apps/despacho-administrativo/src/features/zonas/`; componente de confirmación del catálogo. |
| Componentes compartidos | Modal de confirmación, botones y avisos sin HTTP ni acceso a tokens | `packages/componentes-compartidos/src/`. |
| Cliente de API | Petición y tratamiento del formato de errores vigente | Paquete existente `packages/cliente-api`. |
| Gateway | Enrutamiento y propagación de identidad/correlación | `api-gateway`. |
| Gestión de Despachos | Autorización, caso de uso, idempotencia y control de versión | Funcionalidad `zonas/` bajo el paquete base existente. |

Los nombres de clases y subpaquetes son decisiones técnicas propuestas. No se crean módulos desplegables nuevos.

## 3. Frontend y componentes React

- Verificar primero tema, proveedores, dependencias y herramientas de pruebas según §4.5.1 del documento compartido.
- Componentes compartidos: CR-07 TablaDatos, CR-08 EstadoVista, CR-09 BadgeEstado, CR-15 NotificacionOperacion y el modal de confirmación del sistema de diseño; enlazados a su especificación compartida [cite: 3].
- Componentes propios: la advertencia de desactivación se compone con el modal de confirmación; no se crea un componente compartido nuevo salvo reutilización futura.
- Estado y datos: el contenedor gestiona el estado de proceso, actualiza la fila con el estado devuelto y muestra el aviso de «sin cambio» cuando el estado ya era el solicitado.
- Cliente de API: `PATCH /api/v1/zonas/{idZona}/estado`; el adaptador transforma el `409` al mensaje de conflicto correspondiente.
- Mock: antes del contrato completo pueden usarse fixtures locales para la presentación; no representan respuestas HTTP definitivas.

## 4. Backend, persistencia e integraciones

- Entrada: `PATCH /api/v1/zonas/{idZona}/estado`. Autorizar el JWT humano y exigir `GESTOR_DESPACHO`; el cliente no sustituye esta comprobación.
- Caso de uso: cambiar el estado de la zona con estas reglas: si ya está en el estado solicitado, devolverlo sin cambio ni auditoría; si es una activación, verificar que no colisione con otra zona `ACTIVO`; aplicar el cambio con control de versión de forma transaccional.
- Datos locales: `zonas` (columna `estado`) y la relación con `despachos`, que conservan su zona sin reasignación.
- Migración: revisar el esquema existente y su gestión con Arquitectura; crear migraciones Flyway solo para cambios necesarios. Evaluar si se requiere añadir control de versión (DT-05).
- Integraciones: ninguna con otros módulos; no publica eventos. F-02 y los canales observan el efecto mediante la resolución de zona y la cotización.
- Efectos secundarios: un cambio de estado sobre una zona; la auditoría se genera según ES-F01-08, con un único registro por operación aceptada.
- Idempotencia: la operación es idempotente por zona y estado; una repetición no produce duplicados. El uso de clave de idempotencia se concreta en el contrato.
- Concurrencia: control de versión para que dos operaciones simultáneas no se pisen; la perdida recibe `409 Conflict` con el estado vigente (DT-05).
- Errores: aplicar el formato central de §3.5; el detalle del `409` (solapamiento y versión) se concreta en el contrato antes de implementar el adaptador real.
- Fechas: el modelo establece `America/Lima` para presentación y UTC para instantes.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Confirmación aislada con fixtures y estados de UI | Base frontend y CR de §3 | CUI-01 a CUI-07, solo presentación/interacción |
| I-02 | Cambio de estado backend implementado y probado | DT-01, persistencia, JWT y control de versión disponibles | CA-01 a CA-06 |
| I-03 | Confirmación conectada y verificación del recorrido real | I-01 e I-02 | CA-01 a CA-06 y CUI-01 a CUI-07 |

La definición contractual puede prepararse mientras se desarrolla I-01.

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | Activación sin conflicto y cobertura posterior | Integración PostgreSQL del backend y recorrido UI | Real para backend; fixtures para UI aislada |
| CA-02 | Conflicto de solapamiento conservando `INACTIVO` | Datos con otra zona `ACTIVO` | Real |
| CA-03 | Desactivación con despachos existentes que conservan su zona | Datos sintéticos con despachos y reprogramación | Real |
| CA-04 | Idempotencia por repetición, sin auditoría duplicada | Repetición de la misma operación y conteo de auditorías | Real |
| CA-05 | Concurrencia: una sola se aplica | Dos solicitudes simultáneas sobre la misma zona | Real |
| CA-06 | Rechazar usuario con otro rol o sin token | Pruebas de seguridad del endpoint | Real |

Comandos previstos: desde el frontend, `npm run typecheck` y `npm run build`; desde Gestión, `./mvnw.cmd test`. Las pruebas con Testcontainers requieren Docker. Los resultados se anotan en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Justificación y fuente | Responsable | Bloquea qué incremento |
|---|---|---|---|---|
| DT-01 | Formato del `409 Conflict` para solapamiento y para versión concurrente; uso de `Idempotency-Key` | Gestión §3.1 (rutas) y contrato externo §9 (idempotencia y concurrencia) | Valqui con Backend/Frontend y Arquitectura | Adaptadores HTTP de I-02/03; no los fixtures de I-01 |
| DT-02 | Verificar solapamiento por distrito en `zonas_distritos` y por postal en `zonas_codigos_postales` antes de activar; la terna única no garantiza exclusividad activa | Modelo §3.1 actualizado; datos postales comunicados y validador pendiente | Arquitectura | CA-02 e integración real |
| DT-03 | Esquema/migraciones necesarios y base compartida de JWT, errores, conexión de datos y rutas del Gateway | Inicialización actual del backend y modelo | Valqui coordina con Arquitectura y DevOps | Ejecución real de I-02/03 |
| DT-04 | Disponibilidad y verificación de componentes, tema y herramientas de pruebas | Componentes React §§4.5–4.6 | Valqui para los CR consumidos; coordinación con los responsables del resto | Composición y aceptación de I-01 según sus dependencias |
| DT-05 | Mecanismo de control de versión de `zonas`, cuya tabla no define una columna de versión en el modelo | Modelo de datos §3.1 (solo `despachos` declara `version`) | Valqui con Arquitectura | CA-05 e integración real |
| DT-06 | Alcance de la conservación de `despachos` y `asignaciones_diarias` tras la desactivación | Modelo de datos y RF-01/CA-13 | Valqui con Arquitectura | CA-03 e integración real |

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas del incremento están revisadas y los pendientes bloqueantes resueltos.
- [ ] Los componentes requeridos están verificados antes de componer la pantalla consumidora.
- [ ] Las tareas cubren todos los criterios y tienen una comprobación concreta.
- [ ] Las operaciones respetan el contrato de Gestión y las convenciones compartidas, la propiedad de datos y no publican eventos no acordados.
- [ ] Todos los criterios del alcance cuentan con evidencia, distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas), [convenciones compartidas](../../integraciones/api-contract.md#3-convenciones-comunes), [idempotencia](../../integraciones/api-contract.md#9-reglas-de-idempotencia-y-concurrencia), [modelo de datos](../../arquitectura/modelo-datos.md) y [arquitectura de contenedores](../../arquitectura/c4-contenedores.md).
3. [Componentes React](../../disenio/componentes-react.md), [sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [flujo SDD](../../plantillas/sdd/README.md).
