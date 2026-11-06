# Plan de ES-F03-09: Recojo de una devolución en el domicilio

**Responsable:** Max Rojas

**Estado:** Borrador; pendiente de revisión técnica.

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-11 |
| UI | [ui.md](./ui.md), UI-01 a UI-05 y CUI-01 a CUI-07 |
| Contratos | [Operación §3.7](../../integraciones/api-contract-operacion-reparto.md#37-recojo-de-una-devolución), [Gestión §3.3 y §6.3](../../integraciones/api-contract-gestion-despachos.md#33-recojos-de-devoluciones) y [externo §7.4](../../integraciones/api-contract.md#74-solicitar-y-cancelar-el-recojo-de-una-devolución) |
| Datos y estados | [Modelo §3.6](../../arquitectura/modelo-datos.md#36-recojos-de-devoluciones) y [estados §7](../../arquitectura/diagrama-estados-despacho.md#7-estados-del-recojo) |
| Patrones reutilizados | [ES-F03-04](../ES-F03-04-InicioTraslado/plan.md), [ES-F03-05](../ES-F03-05-EntregaExitosaEvidencia/plan.md), [ES-F03-06](../ES-F03-06-EntregaFallida/plan.md) y [ES-F03-07](../ES-F03-07-CierreJornada/plan.md) |

## 2. Estrategia y responsabilidades

El recojo sigue el mismo recorrido de una entrega: Gestión es dueño del estado, Operación guarda una copia para la ruta y el repartidor actúa desde la web de campo. Se crea como entidad propia porque `ENTREGADO` es un estado final del despacho y no debe reabrirse.

| Área | Responsabilidad | Archivos o componentes previstos |
|---|---|---|
| Web del repartidor | Mostrar recojos, formularios y resumen | `apps/despacho-repartidor`: `PaginaRuta`, `PaginaDetalle`, `PaginaResumen` y páginas nuevas de recojo |
| Operación de Reparto | Copia para la ruta, validaciones, evidencia, reserva y cierre de jornada | Paquetes `campo`, `evidencias` y `jornadas` |
| Gestión de Despachos | Recojo, estados, historial, eventos, asignación y recepción | Paquete nuevo de recojos y catálogo de motivos |
| Panel del Gestor | Asignar, recibir, reprogramar y cerrar | Fuera de esta especificación; ver [F-02 RF-10](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md#rf-10-asignación-de-recojos) y [F-04 RF-08](../../funcionalidades/F-04-GestionEntregasFallidas.md#rf-08-recepción-y-resolución-de-recojos) |
| Ventas y Postventa | Solicitar el recojo y recibir eventos | Módulo externo; requiere acuerdo (DT-01) |

## 3. Frontend

- Unir despachos y recojos en una sola lista ordenada por `secuenciaRuta`.
- Reutilizar la carga de fotos de entrega y fallo: reducción en el navegador, `PUT` firmado y conservación ante error.
- Cargar los motivos desde el backend; no mantener una lista local.
- Conservar la clave de idempotencia en los reintentos.
- Probar con API simulada hasta tener el backend, e identificarlo como simulado.

## 4. Backend, persistencia e integraciones

- Entrada: nuevas rutas de §3.7 en Operación, con el procedimiento de comandos de §3.1.1.
- Caso de uso: Gestión valida el origen y aplica estado, contador, historial y evento en una transacción.
- Datos: tablas nuevas `recojos`, `historial_estados_recojo` y `proyecciones_recojo`; cambios en `evidencias`, `reservas_capacidad`, `motivos_fallo` y `eventos_salientes`.
- Migración: incremental y compatible; los registros actuales conservan sus valores.
- Integraciones: Operación llama a `/internal/v1/recojos/{idRecojo}/transiciones` y recibe la copia en `/internal/v1/proyecciones/recojos/{idRecojo}`.
- Efectos: al registrar `FALLIDO` se libera la reserva con motivo `RECOJO_NO_REALIZADO`; al recibir en el centro, con `RECEPCION_EN_CENTRO`.
- Seguridad: el repartidor se resuelve desde el `sub`; solo accede a sus recojos.
- Concurrencia: control de versión en `recojos` e `Idempotency-Key` en cada comando.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Contratos revisados y migraciones listas | DT-01 a DT-04 | Todos |
| I-02 | Gestión: recojo, estados, historial y eventos | I-01 | CA-05, CA-06, CA-09, CA-11 |
| I-03 | Operación: ruta, comandos, evidencia, reserva y cierre | I-02 | CA-01 a CA-03, CA-05 a CA-07, CA-09, CA-10 |
| I-04 | Pantallas con API simulada | Contrato revisado, DT-05 | CUI-01 a CUI-07 |
| I-05 | Recorrido integrado | I-03, I-04, [F-02 RF-10](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md#rf-10-asignación-de-recojos) | CA-01 a CA-11 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01, CA-02 | Ruta mixta e inicio de traslado | Real |
| CA-03, CA-05 | Estado, evidencia, contador, reserva y evento; despacho sin cambios | Real, con Storage |
| CA-04, CA-08 | Envío bloqueado y datos conservados | API simulada |
| CA-06 | Motivos permitidos en UI y backend | Real |
| CA-07 | Recojo ajeno, cancelado y reasignado | Real |
| CA-09 | Reintento sin duplicados | Real |
| CA-10 | Cierre de jornada mixto | Real |
| CA-11 | Historial completo | Real |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Propuesta actual | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | Acuerdo con Ventas y Postventa: solicitud, cancelación y eventos | [Contrato externo §7.4](../../integraciones/api-contract.md#74-solicitar-y-cancelar-el-recojo-de-una-devolución); Seguridad concede los scopes | Max Rojas con Ventas | Integración real, no I-02 a I-04 |
| DT-02 | Devolución parcial | Ventas informa los SKU y cantidades a recoger; la capacidad se calcula solo con ellos | Max Rojas con Ventas | I-01 |
| DT-03 | Límite de intentos del recojo | Sin máximo automático; el Gestor decide reprogramar o cerrar | Max Rojas con Gerardo | I-02 |
| DT-04 | Secuencia compartida con despachos | Una sola numeración por jornada; el reordenamiento acepta ambos | Max Rojas con Tarqui | I-01 |
| DT-05 | Diseño visual del recojo | Reutilizar los frames de entrega y fallo | Max Rojas | No bloquea |
| DT-06 | Cambio combinado (entregar y recoger en una visita) | Fuera de alcance; sigue en [Pendientes](../../funcionalidades/pendiente.md) | Max Rojas con Ventas | No bloquea |

## 8. Condiciones para iniciar y cerrar

- [ ] Pendientes bloqueantes resueltos y contratos revisados.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo simulaciones y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Overview §12](../../overview.md#12-devolución-del-producto).
