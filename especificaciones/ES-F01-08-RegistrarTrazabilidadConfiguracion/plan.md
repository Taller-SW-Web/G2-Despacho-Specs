# Plan de ES-F01-08: Registrar la trazabilidad de la configuración

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** No aplica. Es captura automática transaccional. La presentación de última modificación y de configuración corresponde a las UI existentes de ES-F01-01 a ES-F01-04; no se modifica una interfaz ni se incluye `ui.md`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-06 | Original en `91db8f8`; migración SDD del 16/10/2026 |
| Funcionalidad padre | [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-01, RF-02 y §8 | `91db8f8` |
| Contratos | [Gestión §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas), [roles §3.3](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio), [idempotencia §9](../../integraciones/api-contract.md#9-reglas-de-idempotencia-y-concurrencia) | `91db8f8` |
| Datos | [Modelo §§3.1 y 3.5](../../arquitectura/modelo-datos.md), zonas, tarifas y auditoría | `91db8f8` |
| Operaciones de origen | [ES-F01-02](../ES-F01-02-RegistrarZonaCobertura/spec.md), [ES-F01-03](../ES-F01-03-ActivarDesactivarZona/spec.md), [ES-F01-04](../ES-F01-04-ConfigurarTarifaZona/spec.md) | `91db8f8` |

El plan conserva los requisitos y registra las decisiones de persistencia, consulta e idempotencia aún pendientes [cite: 1, 2].

## 2. Estrategia y responsabilidades

Invocar la captura de auditoría desde los casos de uso de configuración dentro de su misma transacción local. Preparar valores anteriores/nuevos, ejecutor autenticado e instante UTC, y confirmar negocio y registro juntos. Una operación rechazada o una repetición ya aceptada no inserta otra auditoría.

| Capa o aplicación | Responsabilidad | Elementos previstos |
|---|---|---|
| Gestión, configuración | Validar y confirmar el cambio de negocio | Casos de uso de ES-F01-02/03/04 |
| Gestión, auditoría | Capturar una decisión aceptada y conservar el histórico | Componente de auditoría y repositorio de inserción/lectura |
| Gestión, persistencia | Atomicidad, restricciones y protección del histórico | `auditoria_configuracion`, zonas y tarifas |
| Seguridad | Proporcionar identidad del JWT | Contexto autenticado; no campos libres del cliente |

## 3. Frontend y componentes React

No aplica. Se reutiliza el contrato de datos de las vistas de configuración sin definir una pantalla de auditoría. La consulta del histórico debe concretarse en Gestión (DT-04); cualquier cambio visual posterior requiere revisar la especificación de UI propietaria antes de implementarlo.

## 4. Backend, persistencia e integraciones

- Entrada: contexto de un cambio validado y autorizado con `GESTOR_DESPACHO`, no una llamada pública para crear auditorías.
- Caso de uso: conservar antes/después, entidad afectada, acción, `sub` del JWT e instante generado por el servidor. Las marcas de las entidades se mantienen coherentes con la operación aceptada.
- Transacción: insertar auditoría con la creación/edición/estado de zona o sustitución de tarifa. Si falla el registro obligatorio, revertir el cambio; no trasladar la auditoría esencial a un proceso asíncrono.
- Datos: reutilizar `auditoria_configuracion` de Gestión y el histórico de `tarifas_zona`; sin compartir tablas con Operación y sin duplicar registros en otra tabla de auditoría.
- Sustitución tarifaria: una operación produce un registro que permita reconstruir la nueva regla y la desactivación de la anterior con identidad y fecha de ambas. Conciliar esta representación con `entidad_id` único y campos del modelo antes de implementar (DT-01).
- Migración: revisar restricciones, acciones admitidas y permisos de inserción/lectura; cualquier ampliación necesaria se define primero en el modelo y se verifica con datos existentes (DT-01/02).
- Idempotencia: reconocer repeticiones en el caso de uso de origen antes de insertar. No deducir identidad únicamente de que dos cuerpos sean iguales; una nueva decisión legítima debe distinguirse de un reintento. La identidad concreta y protección concurrente se acuerdan en DT-03, sin imponer un encabezado nuevo.
- Integridad: no ofrecer edición/eliminación del histórico desde esta funcionalidad; ordenar por fecha persistida del servidor. Precisar desempate de fechas iguales en DT-04.
- Lectura: revisar exposición autorizada del histórico y última modificación en el contrato de Gestión; no crear una ruta paralela ni un contrato en esta carpeta.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Persistencia auditable con identidad, UTC e integridad | DT-01 y DT-02 | CA-01, CA-03 y CA-06 |
| I-02 | Captura transaccional en todas las operaciones de configuración | I-01 y casos de uso de origen | CA-01 a CA-04 |
| I-03 | Repetición, consulta y regresión completa verificadas | I-02, DT-03 y DT-04 | CA-01 a CA-06 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | Crear zona deja un registro con ejecutor e instante UTC | Integración PostgreSQL | JWT controlado |
| CA-02 | Activar/desactivar captura estados anterior y nuevo | Integración del caso de uso | Persistencia real |
| CA-03 | Sustituir tarifa conserva ambas reglas y trazabilidad sin duplicar la operación | Integración transaccional | Persistencia real |
| CA-04 | Rechazo no inserta éxito; fallo de inserción revierte negocio | Integración con fallo inyectado | Persistencia real y fallo controlado |
| CA-05 | Repetición exacta, incluso concurrente, conserva un único registro | Integración de idempotencia | Mecanismo acordado en DT-03 |
| CA-06 | No se puede editar ni eliminar auditoría desde la funcionalidad | Integridad y autorización | API y repositorio reales |

Verificar también edición de zona, estado sin cambio, intento de suplantar ejecutor/hora desde el cliente y consulta cronológica autorizada. Usar reloj controlable y comprobar instantes persistidos, no el reloj del navegador. Ejecutar la suite del backend con su Maven Wrapper disponible y registrar comando exacto, revisión, preparación y reportes en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Fuente y motivo | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | Representar una sustitución tarifaria en un solo registro con nueva/anterior, actor y fecha de ambas | CA-03; modelo tiene una `entidad_id` y no identifica ejecutor de desactivación de tarifa | Valqui con Arquitectura | CA-03 e I-01/02 |
| DT-02 | Conciliar marcas de entidad, acciones permitidas y protección de solo inserción | Modelo §§3.1/3.5; identidad UUID en zonas frente a `sub` y auditoría textual | Valqui con Arquitectura y Seguridad | Persistencia de I-01 |
| DT-03 | Definir identidad de operación y control concurrente de repetición en altas, ediciones, estados y tarifas | CA-05; contrato §9 no concreta comandos de configuración | Valqui con Backend y Arquitectura | CA-05 e I-03 |
| DT-04 | Definir consulta autorizada del histórico, datos de última modificación y desempate de orden | Gestión §3.1 solo publica tarifa vigente; spec exige histórico consultable | Valqui con Backend y responsables de vistas | Consulta e I-03 |

## 8. Condiciones para iniciar y cerrar

- [ ] Modelo y contrato resuelven las decisiones bloqueantes del incremento.
- [ ] Negocio y auditoría confirman o revierten juntos en todas las operaciones de origen.
- [ ] Rechazos, repeticiones y estados sin cambio no producen registros adicionales de éxito.
- [ ] Histórico íntegro y consulta autorizada cuentan con evidencia reproducible.
- [ ] Todos los criterios, commits y revisión del equipo están enlazados.

## 9. Referencias

1. [cite: 1] [Especificación](./spec.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [cite: 2] [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md), [modelo](../../arquitectura/modelo-datos.md) y [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).
3. [Flujo SDD](../../plantillas/sdd/README.md).
