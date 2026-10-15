# Plan de ES-F01-04: Configurar la tarifa vigente de una zona

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** Aplica; formulario de tarifas de la zona (Pantalla 3), ruta `/zonas/:id/tarifas`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-05 | Contenido previo en `12d5041`; migración en esta carpeta. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-07 | Misma revisión documental que este plan. |
| Contrato | [API](../../integraciones/api-contract.md), §§3.3, 3.5 y 9.1 | `12d5041`; equivalencia de campos con el modelo pendiente. |
| Componentes y diseño | [Componentes React](../../disenio/componentes-react.md), §4.5; [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | `12d5041`. |
| Arquitectura y datos | [C4 contenedores](../../arquitectura/c4-contenedores.md), §3.1; [modelo de datos](../../arquitectura/modelo-datos.md), §3.1 | `12d5041`. |

Este cambio prepara documentación. La modificación del contrato, el código y las pruebas se ejecutan en tareas posteriores. No se duplican contratos ni se da por cerrada la revisión técnica [cite: 1, 2].

## 2. Estrategia y responsabilidades

El panel consume la consulta y el guardado de la tarifa a través del Gateway con autorización administrativa. Gestión valida la consistencia de la regla, comprueba que la zona existe y está activa, y persiste una única tarifa vigente conservando la anterior como histórico. El frontend replica las validaciones conocidas solo como ayuda.

| Área | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Panel, validación en línea y adaptación de errores | `apps/despacho-administrativo/src/features/zonas/`; `FormularioTarifa.tsx`. |
| Componentes compartidos | Campos numéricos, validación y avisos sin HTTP ni acceso a tokens | `packages/componentes-compartidos/src/`. |
| Cliente de API | Petición y tratamiento del formato de errores vigente | Paquete existente `packages/cliente-api`. |
| Gateway | Enrutamiento y propagación de identidad/correlación | `api-gateway`. |
| Gestión de Despachos | Autorización, caso de uso, validaciones y persistencia | Funcionalidad `zonas/` bajo el paquete base existente. |

Los nombres de clases y subpaquetes son decisiones técnicas propuestas. No se crean módulos desplegables nuevos.

## 3. Frontend y componentes React

- Verificar primero tema, proveedores, dependencias y herramientas de pruebas según §4.5.1 del documento compartido.
- Componentes compartidos: CR-03 ShellAdministrativo, CR-05 EncabezadoPagina, campos numéricos del sistema de diseño, CR-15 NotificacionOperacion y el aviso de sustitución; enlazados a su especificación compartida [cite: 3].
- Componentes propios: el aviso de sustitución de la tarifa vigente y la agrupación de campos de la regla; se resuelven con patrones existentes y no se crea un componente compartido nuevo salvo reutilización futura.
- Estado y datos: el contenedor carga la tarifa vigente al abrir, conserva los datos ante errores y bloquea el guardado en zonas inactivas.
- Cliente de API: `GET /api/v1/zonas/{idZona}/tarifa` y `PUT /api/v1/zonas/{idZona}/tarifa`; el adaptador transforma los errores de validación al control correspondiente.
- Mock: antes del contrato completo pueden usarse fixtures locales para la presentación; no representan respuestas HTTP definitivas.

## 4. Backend, persistencia e integraciones

- Entradas: `GET` y `PUT /api/v1/zonas/{idZona}/tarifa`. Autorizar el JWT humano y exigir `GESTOR_DESPACHO`; el cliente no sustituye esta comprobación.
- Caso de uso: consultar la tarifa vigente y guardar una nueva regla, validando que la zona existe y está `ACTIVO`, y que los valores cumplen las reglas RN-01 a RN-04. Al guardar, marcar la nueva como vigente y la anterior como inactiva conservándola como histórico, de forma transaccional.
- Datos locales: `tarifas_zona`, con su índice único parcial para garantizar una sola tarifa vigente por zona.
- Migración: revisar el esquema existente y su gestión con Arquitectura; crear migraciones Flyway solo para cambios necesarios.
- Integraciones: ninguna con otros módulos; no publica eventos. El motor de cotización de esta misma funcionalidad consume la tarifa vigente.
- Efectos secundarios: crea una regla y actualiza la vigencia de la anterior; la auditoría se genera según ES-F01-08.
- Idempotencia: el guardado sustituye la vigencia de forma consistente; repetir una regla idéntica no debe crear un histórico innecesario (a concretar en el contrato).
- Fechas: el modelo establece `America/Lima` para presentación y UTC para instantes; la vigencia y el histórico usan marcas del servidor.
- Errores: aplicar el formato central de §3.5; el detalle de validación y de zona inactiva se concreta en el contrato.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Panel aislado con fixtures y validación en línea | Base frontend y CR de §3 | CUI-01 a CUI-07, solo presentación/interacción |
| I-02 | Consulta y guardado backend implementados y probados | DT-01/DT-02, persistencia y JWT disponibles | CA-01 a CA-05 |
| I-03 | Panel conectado y verificación del recorrido real | I-01 e I-02 | CA-01 a CA-05 y CUI-01 a CUI-07 |

La definición contractual puede prepararse mientras se desarrolla I-01.

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | Guardado de tarifa válida y aplicación posterior | Integración PostgreSQL del backend y recorrido UI | Real para backend; fixtures para UI aislada |
| CA-02 | Rechazo de regla inválida o zona inexistente | Datos inválidos y zona inexistente | Real |
| CA-03 | Sustitución con histórico conservado | Zona con tarifa vigente; consulta del histórico | Real |
| CA-04 | Zona activa sin tarifa identificada sin costo por defecto | Datos con y sin tarifa | Real |
| CA-05 | Rechazar usuario con otro rol o sin token | Pruebas de seguridad del endpoint | Real |

Comandos previstos: desde el frontend, `npm run typecheck` y `npm run build`; desde Gestión, `./mvnw.cmd test`. Las pruebas con Testcontainers requieren Docker. Los resultados se anotan en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Justificación y fuente | Responsable | Bloquea qué incremento |
|---|---|---|---|---|
| DT-01 | Cuerpo de la tarifa, validaciones contractuales y errores (`400`/`404`) | Contrato §9.1 (tabla de rutas) y DC-04 del documento compartido | Valqui con Backend/Frontend y Arquitectura | Adaptadores HTTP de I-02/03; no los fixtures de I-01 |
| DT-02 | Equivalencia entre los campos del contrato (`pesoIncluidoKg`, `plazoEstimadoDiasHabiles`) y la tabla `tarifas_zona` (`peso_base_kg`, `plazo_min_dias`, `plazo_max_dias`, `activa`) | Contrato §9.1 frente a modelo de datos §3.1 | Valqui con Arquitectura | CA-01, CA-03 e integración real |
| DT-03 | Esquema/migraciones necesarios y base compartida de JWT, errores, conexión de datos y rutas del Gateway | Inicialización actual del backend y modelo | Valqui coordina con Arquitectura y DevOps | Ejecución real de I-02/03 |
| DT-04 | Disponibilidad y verificación de componentes, tema y herramientas de pruebas | Componentes React §§4.5–4.6 | Valqui para los CR consumidos; coordinación con los responsables del resto | Composición y aceptación de I-01 según sus dependencias |
| DT-05 | Definición de «tarifa vigente» e índice único parcial; tratamiento del histórico y de una regla idéntica repetida | Modelo de datos, tabla `tarifas_zona` | Valqui con Arquitectura | CA-03 e integración real |

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
