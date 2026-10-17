# Plan de ES-F05-08: Editar furgoneta y límites de carga

**Responsable:** Rhamses.

**Estado:** Borrador de mantenimiento y aceptación de código existente; pendiente de revisión técnica.

**UI:** Aplica; editar límites en `/furgonetas`.

## 1. Entradas y revisiones

| Documento | Referencia | Revisión utilizada |
|---|---|---|
| Especificación | [spec.md](./spec.md), CA-01, CA-02, CA-03, CA-04, CA-05 | Fuente `f3849d9`; criterios conservados en esta migración |
| UI | [ui.md](./ui.md), CUI-01 a CUI-06 | Borrador preparado con esta migración |
| Contrato | [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas), [roles §3.3](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor) | `f3849d9`; pendientes registrados en §7 |
| Componentes y diseño | [Componentes React](../../disenio/componentes-react.md) y [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | `f3849d9` |
| Datos | [Modelo de datos](../../arquitectura/modelo-datos.md), §3.2 | `f3849d9`; contrastar con el esquema desplegado |
| Código existente | [Frontend](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/9c7a99d/apps/despacho-administrativo/src/features/flota/FormularioFurgoneta.tsx) y [backend](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/8f8282a/servicio-operacion-reparto/src/main/java/com/modulodespacho/operacionreparto/servicio_operacion_reparto/flota/application/GestorFlota.java) | Frontend `9c7a99d`; backend `8f8282a` |

Este plan documenta cómo revisar y aceptar un comportamiento que ya tiene código de referencia; no se presenta como un plan aprobado antes de esa implementación. La migración conserva los criterios y señala los acuerdos que deben conciliarse antes de cerrar la aceptación [cite: 1, 2].

## 2. Estrategia y responsabilidades

Editar capacidades maestras de la furgoneta y conservar las instantáneas de jornadas existentes. El frontend consume el Gateway; Operación es propietaria de la autorización, reglas y persistencia.

| Área | Responsabilidad | Código de referencia |
|---|---|---|
| Frontend administrativo | Contexto, interacción y recuperación de errores | `apps/despacho-administrativo/src/features/flota/FormularioFurgoneta.tsx` |
| Componentes compartidos | Acciones, campos, estructura, tabla, estados y notificaciones | `packages/componentes-compartidos/src/`; CR indicados en UI §2 |
| Cliente de API | Adaptación de `PUT /api/v1/furgonetas/{idFurgoneta}`, sin inventar resultados | `features/flota/api.ts` y cliente autenticado existente |
| Gateway | Enrutar a Operación y propagar la identidad/correlación | `api-gateway` del backend |
| Operación | Caso de uso `editarFurgoneta`, validación y datos locales | `flota/api`, `flota/application`, `flota/domain`, `flota/infrastructure` |
| Otros consumidores | Verificar efectos acordados sin compartir tablas entre servicios | F-03/F-06 y Seguridad cuando corresponda |

## 3. Frontend y componentes React

- Verificar primero los CR consumidos; sus cambios compartidos se coordinan con sus responsables.
- Componentes propios: `FormularioFurgoneta.tsx`, composición del catálogo y hooks `useCatalogoFlota`/`useOperacionFlota` cuando correspondan.
- Interacción: Precargar los límites y explicar que se aplican a jornadas futuras; confirmar sin ofrecer edición de placa o estado.
- Estado y datos: mantener separados carga, error, vacío y resultado confirmado; bloquear acciones sobre una consulta desfasada.
- Transporte: verificar la adaptación frente a [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas); no usar la implementación provisional como sustituto del contrato.
- Simulación: los fixtures y las respuestas HTTP de prueba solo acreditan los escenarios identificados; una aceptación integrada requiere servicios y cuentas reales.

## 4. Backend, persistencia e integraciones

- Entrada: `PUT /api/v1/furgonetas/{idFurgoneta}`; validar identidad y rol antes de consultar o modificar datos.
- Caso de uso y datos: Actualizar el maestro y auditar en una transacción; no recalcular ni actualizar capacidades en asignaciones_diarias.
- Propietario: Operación de Reparto y Flota, datos `furgonetas y lectura de asignaciones_diarias`; no consultar la base de Gestión.
- Persistencia: revisar V1/V2 y la adaptación del esquema heredado descritas en la [guía backend de flota](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/8f8282a/docs/gestion-flota.md). No activar Flyway sobre el esquema heredado sin revisión.
- Efectos: la auditoría debe confirmarse con la mutación y revertirse si falla.
- Integraciones: los consumidores F-03/F-06 verifican sus reglas operativas mediante los contratos del servicio propietario.
- Seguridad: JWT y rol `GESTOR_DESPACHO`; la identidad de auditoría proviene del token, no del formulario.
- Concurrencia e idempotencia: verificar repetición y operaciones concurrentes sin pérdida de datos ni auditorías duplicadas; no introducir encabezados nuevos no acordados.

## 5. Orden de implementación y aceptación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Contrato, diferencias y componentes revisados | Fuentes de §1; DT-01 y DT-02 | Todos los CA y CUI como entradas revisadas |
| I-02 | Backend y UI contrastados por separado con los criterios | I-01 y código existente; PostgreSQL de prueba para backend | CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06 en entorno aislado |
| I-03 | Recorrido integrado y revisión registrados | I-02, acuerdos funcionales resueltos y dependencias reales disponibles | CA-01, CA-02, CA-03, CA-04, CA-05; CUI-01 a CUI-06 |

Los ajustes de código que surjan de la revisión se tramitan en sus repositorios. Esta entrega modifica documentación, no ejecuta migraciones de base de datos ni despliegues.

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno |
|---|---|---|
| CA-01 | Editar capacidades y comprobar valores, auditoría, placa y estado. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-02 | Crear jornada con capacidades originales, editar el maestro y comprobar que solo las jornadas futuras toman los nuevos límites. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-03 | Enviar límites inválidos y comprobar que el maestro no cambia. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-04 | Editar un UUID ausente y comprobar recurso inexistente. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-05 | Editar con otro rol y comprobar rechazo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |

Comandos previstos, desde el repositorio correspondiente:

```powershell
# Frontend, desde su raíz:
npm run test:f05
npm run typecheck
# Backend, desde servicio-operacion-reparto:
./mvnw.cmd test
```

Complementar con las comprobaciones CUI, teclado y recorrido integrado. Registrar versión, datos, permisos, dependencias reales o simuladas y resultados individuales en [evidence.md](./evidence.md). No ejecutar estas pruebas contra datos reales de producción.

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Fuente y efecto | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | La comprobación de las capacidades de una jornada futura necesita el consumidor F-06. Una lectura de instantáneas anteriores demuestra conservación, pero no acredita por sí sola la apertura real de nuevas jornadas. | P-01 de spec.md; contrato y modelo vigentes | Rhamses con Arquitectura | Aceptación de los criterios afectados e I-03 |
| DT-02 | Ratificar los DTO, límites, filtros y errores utilizados por la adaptación frontend | Operación §4.1 y DC-04 de componentes React; no duplicar esquemas aquí | Rhamses con responsables del contrato | Aceptación de transporte en I-02/03 |
| DT-03 | Disponibilidad de Seguridad y recursos para el recorrido real | Separar pruebas con doble JWT de cuentas reales; validar configuración de Render/Vercel/Supabase | Responsables de Seguridad y DevOps | I-03 |
| DT-04 | Revisión de accesibilidad, componentes y diseño | UI §6/7; los resultados de pruebas no sustituyen la revisión visual acordada | Rhamses con Max y Calidad | Cierre de CUI e I-03 |

## 8. Condiciones para iniciar y cerrar

- [ ] Las fuentes y el contrato aplicables al incremento están revisados.
- [ ] Los componentes requeridos están disponibles y verificados antes de la aceptación de la pantalla.
- [ ] Los pendientes que alteran criterios se resolvieron en sus documentos propietarios.
- [ ] Cada CA y CUI tiene tarea, comprobación y evidencia identificada.
- [ ] La revisión humana y las limitaciones de integración se registraron expresamente.

## 9. Referencias

1. [Especificación](./spec.md), [UI](./ui.md) y [tareas](./tasks.md) [cite: 1].
2. [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas), [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor) y [modelo de datos](../../arquitectura/modelo-datos.md) [cite: 2].
3. [Componentes React](../../disenio/componentes-react.md) y [evidencia](./evidence.md) [cite: 3].
