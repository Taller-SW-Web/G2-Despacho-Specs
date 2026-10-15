# Plan de ES-F01-02: Registrar y editar una zona de cobertura

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** Aplica; formulario de zona (Pantalla 2), rutas `/zonas/nueva` y `/zonas/:id/editar`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-06 | Contenido previo en `12d5041`; migración en esta carpeta. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-07 | Misma revisión documental que este plan. |
| Contrato | [API](../../integraciones/api-contract.md), §§3.3, 3.5 y 9.1 | `12d5041`; cuerpos de alta y edición pendientes de detalle. |
| Componentes y diseño | [Componentes React](../../disenio/componentes-react.md), §4.5; [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | `12d5041`. |
| Arquitectura y datos | [C4 contenedores](../../arquitectura/c4-contenedores.md), §3.1; [modelo de datos](../../arquitectura/modelo-datos.md), §3.1 | `12d5041`. |

Este cambio prepara documentación. La modificación del contrato, el código y las pruebas se ejecutan en tareas posteriores. No se duplican contratos ni se da por cerrada la revisión técnica [cite: 1, 2].

## 2. Estrategia y responsabilidades

El formulario consume altas y ediciones autorizadas a través del Gateway. Gestión valida las reglas en el backend (unicidad, delimitación mínima y solapamiento entre zonas activas) antes de persistir y devuelve los conflictos con el elemento afectado. El frontend replica las validaciones conocidas solo como ayuda, sin sustituir la comprobación del servidor.

| Área | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Formulario, validación en línea y adaptación de errores | `apps/despacho-administrativo/src/features/zonas/`; `FormularioZona.tsx`. |
| Componentes compartidos | Campos, validación y acciones sin HTTP ni acceso a tokens | `packages/componentes-compartidos/src/`. |
| Cliente de API | Petición y tratamiento del formato de errores vigente | Paquete existente `packages/cliente-api`. |
| Gateway | Enrutamiento y propagación de identidad/correlación | `api-gateway`. |
| Gestión de Despachos | Autorización, caso de uso, validaciones y persistencia | Funcionalidad `zonas/` bajo el paquete base existente, con `api`, `application`, `domain` e `infrastructure` según necesidad. |

Los nombres de clases y subpaquetes son decisiones técnicas propuestas. No se crean módulos desplegables nuevos.

## 3. Frontend y componentes React

- Verificar primero tema, proveedores, dependencias y herramientas de pruebas según §4.5.1 del documento compartido.
- Componentes compartidos: CR-03 ShellAdministrativo, CR-05 EncabezadoPagina, campos y validación del sistema de diseño, CR-15 NotificacionOperacion y CR-12 Modal si se confirma el descarte con cambios sin guardar; enlazados a su especificación compartida [cite: 3].
- Componentes propios: selector múltiple de distritos y selector múltiple de códigos postales; se resuelven con el patrón de campos del sistema de diseño y no se crea un componente compartido nuevo salvo reutilización futura.
- Estado y datos: el contenedor distingue alta y edición, precarga la zona al editar y conserva los datos ante errores; el descarte de cambios sin guardar pide confirmación.
- Cliente de API: `POST /api/v1/zonas`, `GET /api/v1/zonas/{idZona}` y `PUT /api/v1/zonas/{idZona}`; el adaptador transforma errores de validación al control correspondiente.
- Mock: antes del contrato completo pueden usarse fixtures locales para la presentación; no representan respuestas HTTP definitivas.

## 4. Backend, persistencia e integraciones

- Entradas: `POST /api/v1/zonas` y `PUT /api/v1/zonas/{idZona}`. Autorizar el JWT humano y exigir `GESTOR_DESPACHO`; el cliente no sustituye esta comprobación.
- Caso de uso: crear una zona nueva o actualizar una existente, validando presencia de delimitación, unicidad de nombre y ausencia de solapamiento con zonas `ACTIVO`.
- Datos locales: `zonas` y `zona_distritos`, con referencia a `distrito`. Resolver la delimitación de forma transaccional para no persistir cambios parciales.
- Migración: revisar el esquema existente y su gestión con Arquitectura; crear migraciones Flyway solo para cambios necesarios.
- Integraciones: ninguna con otros módulos; no publica eventos. La delimitación pertenece a esta funcionalidad.
- Efectos secundarios: crea o actualiza una zona y su delimitación; la auditoría se genera según ES-F01-08. No requiere clave de idempotencia para un alta o una edición explícitas.
- Fechas: el modelo establece `America/Lima` para presentación y UTC para instantes; la identidad del usuario y la marca temporal proceden del JWT y del servidor.
- Errores: aplicar el formato central de §3.5; el detalle de validación y del conflicto se concreta en el contrato antes de implementar el adaptador real.
- Concurrencia: evaluar si la edición requiere control de versión; relacionado con el control de versión de ES-F01-03 (DT-03) y con DT-06 de este plan.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Formulario aislado con fixtures y validación en línea | Base frontend y CR de §3 | CUI-01 a CUI-07, solo presentación/interacción |
| I-02 | Alta y edición backend implementadas y probadas | DT-01, persistencia y JWT disponibles | CA-01 a CA-06 |
| I-03 | Formulario conectado y verificación del recorrido real | I-01 e I-02 | CA-01 a CA-06 y CUI-01 a CUI-07 |

La definición contractual puede prepararse mientras se desarrolla I-01.

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | Alta válida persistida y recurso devuelto | Integración PostgreSQL del backend y recorrido UI | Real para backend; fixtures para UI aislada |
| CA-02 | Conflicto por nombre, distrito o código postal | Datos sintéticos con zona activa previa | Real |
| CA-03 | Rechazo sin delimitación en UI y en API | Prueba de interacción y prueba directa del endpoint | Real y simulada |
| CA-04 | Edición conservando identificador y resolviendo la nueva cobertura | Integración y recorrido UI | Real |
| CA-05 | Conflicto de solapamiento sin cambios parciales | Datos con otra zona activa | Real |
| CA-06 | Rechazar usuario con otro rol o sin token | Pruebas de seguridad del endpoint | Real |

Comandos previstos: desde el frontend, `npm run typecheck` y `npm run build`; desde Gestión, `./mvnw.cmd test`. Las pruebas con Testcontainers requieren Docker. Los resultados se anotan en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Justificación y fuente | Responsable | Bloquea qué incremento |
|---|---|---|---|---|
| DT-01 | Cuerpo de alta y edición, validaciones contractuales y formato de conflicto (`409`) | Contrato §9.1 (tabla de rutas) y DC-04 del documento compartido | Valqui con Backend/Frontend y Arquitectura | Adaptadores HTTP de I-02/03; no los fixtures de I-01 |
| DT-02 | Fuente y formato del catálogo de distritos y códigos postales de selección | Modelo de datos, tabla `distrito` | Valqui con Arquitectura | CA-01 a CA-05 e integración real |
| DT-03 | Esquema/migraciones necesarios y base compartida de JWT, errores, conexión de datos y rutas del Gateway | Inicialización actual del backend y modelo | Valqui coordina con Arquitectura y DevOps | Ejecución real de I-02/03 |
| DT-04 | Disponibilidad y verificación de componentes, tema y herramientas de pruebas | Componentes React §§4.5–4.6 | Valqui para los CR consumidos; coordinación con los responsables del resto | Composición y aceptación de I-01 según sus dependencias |
| DT-05 | Conciliación entre `zona_distritos` (modelo §6) y `zonas_distritos` (modelo §3.1) y su efecto en la unicidad de cobertura por zona activa | Modelo de datos §3.1 y §6 | Arquitectura | CA-02, CA-05 e integración real |
| DT-06 | Necesidad de control de versión en la edición de zonas | Modelo de datos; el modelo no define una columna de versión en `zonas` | Valqui con Arquitectura | CA-04/CA-05 e integración real |

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas del incremento están revisadas y los pendientes bloqueantes resueltos.
- [ ] Los componentes requeridos están verificados antes de componer la pantalla consumidora.
- [ ] Las tareas cubren todos los criterios y tienen una comprobación concreta.
- [ ] Las operaciones respetan el contrato único y la propiedad de datos.
- [ ] Todos los criterios del alcance cuentan con evidencia, distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [Contrato central](../../integraciones/api-contract.md#91-zonas-y-tarifas), [modelo de datos](../../arquitectura/modelo-datos.md) y [arquitectura de contenedores](../../arquitectura/c4-contenedores.md).
3. [Componentes React](../../disenio/componentes-react.md), [sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [flujo SDD](../../plantillas/sdd/README.md).
