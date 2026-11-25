# ES-F02-09: Adelantar despacho a hoy

## 1. Contexto y alcance

Aprovechar disponibilidad imprevista de repartidores adelantando individualmente un pendiente futuro a hoy, sin asignarlo automáticamente. Funcionalidad padre: [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-06 y CA-13. Servicio propietario: Gestión. Actor: `GESTOR_DESPACHO`.

La operación y su transporte se definen únicamente en [Gestión §3.2.3](../../integraciones/api-contract-gestion-despachos.md#323-adelantar-un-despacho-a-hoy) [cite: 1]. Plan, UI, tareas y resultados: [plan](./plan.md), [ui](./ui.md), [tasks](./tasks.md), [evidence](./evidence.md).

## 2. Reglas

- Solo pendientes futuros, versión vigente y sin comandos incompatibles pendientes.
- Hoy lo decide el servidor en `America/Lima`; motivo obligatorio y auditoría atómica.
- Conservar estado, intentos, espera en cola, identidad, carga e históricos.
- No reservar/liberar capacidad ni emitir transiciones, notificaciones de progreso o proyecciones. No reescribir eventos pendientes.
- La posterior asignación conserva todas las validaciones de [ES-F02-04](../ES-F02-04-AsignarDespachoRepartidor/spec.md) y sus comunicaciones con fecha actualizada.
- Fuera de alcance: adelanto masivo, fechas arbitrarias, asignación automática, cambios a progreso en campo.

## 3. Criterios de aceptación

- **CA-01:** DADO un pendiente futuro, CUANDO el gestor confirma el adelanto con motivo, ENTONCES queda pendiente para hoy, incrementa versión y registra fecha anterior/nueva, actor, motivo y momento.
- **CA-02:** DADO fecha no futura, estado incompatible, versión obsoleta o comando pendiente, CUANDO se solicita adelanto, ENTONCES rechaza sin escrituras parciales.
- **CA-03:** DADO un adelanto confirmado, CUANDO se repite el mismo comando, ENTONCES recupera la respuesta original sin duplicar auditoría; cambiar contenido con la misma clave rechaza.
- **CA-04:** DADO un adelanto, CUANDO se confirma, ENTONCES no modifica intentos, reservas ni eventos existentes; la asignación posterior emite sus comunicaciones normales con fecha actualizada.
- **CA-05:** DADO una petición sin identidad/rol o con formato inválido, CUANDO se solicita adelanto, ENTONCES aplica errores contractuales sin modificar datos.
- **CA-06:** DADA la cola, CUANDO se adelanta un futuro, ENTONCES requiere confirmación y motivo, evita doble envío y refresca datos e indicadores sin asignar; un resultado incierto permite recuperar solo el comando original.
