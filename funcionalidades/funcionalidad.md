# Índice de funcionalidades

Este documento reúne las áreas funcionales del **Módulo de Despacho y Entrega a Domicilio** y permite consultar el estado de sus especificaciones.

| ID | Funcionalidad | Descripción breve | Responsable | Estado | Especificación |
|---|---|---|---|---|---|
| **F-01** | Gestión de zonas geográficas y cotización | Define cobertura, tarifas y la zona de cada despacho. | Valqui | En especificación | [Ver especificación](./F-01-Gestor_ZonasGeograficas.md) |
| **F-02** | Programación y asignación de despachos | Recibe solicitudes y asigna despachos con jornada y secuencia. | Tarqui | En especificación | [Ver especificación](./F-02-ProgramacionAsignacionDespachos.md) |
| **F-03** | Operación del repartidor y evidencia de entrega | Permite ejecutar entregas y registrar estados y evidencias. | Max | En especificación | [Ver especificación](./F-03-AppMovilRepartidor.md) |
| **F-04** | Entregas fallidas y reprogramaciones | Recibe en el centro los paquetes no entregados y decide su reprogramación o cierre. | Gerardo | Implementación parcial iniciada en ES-F04-01 | [Ver especificación](./F-04-GestionEntregasFallidas.md) |
| **F-05** | Gestión de repartidores y vehículos | CRUD de repartidores con baja lógica y vinculación con Seguridad, y gestión de furgonetas con capacidades de carga. | Rhamses | En especificación | [Ver especificación](./F-05-GestionRepartidoresVehiculos.md) |
| **F-06** | Disponibilidad y capacidad diaria de la flota | Asignación diaria repartidor – furgoneta – zona, cálculo de ocupación, disponibilidad y saturación para F-02. | Luis | En especificación | [Ver especificación](./F-06-DisponibilidadCapacidadDiaria.md) |

## Especificaciones atómicas de F-01

| ID | Comportamiento | Especificación | Estado |
|---|---|---|---|
| **ES-F01-01** | Consultar el catálogo de zonas de cobertura | [Especificación](../especificaciones/ES-F01-01-ConsultarCatalogoZonas/spec.md) · [UI](../especificaciones/ES-F01-01-ConsultarCatalogoZonas/ui.md) · [Plan](../especificaciones/ES-F01-01-ConsultarCatalogoZonas/plan.md) · [Tareas](../especificaciones/ES-F01-01-ConsultarCatalogoZonas/tasks.md) · [Evidencia](../especificaciones/ES-F01-01-ConsultarCatalogoZonas/evidence.md) | Borrador SDD; implementación pendiente |
| **ES-F01-02** | Registrar y editar una zona de cobertura | [Especificación](../especificaciones/ES-F01-02-RegistrarZonaCobertura/spec.md) · [UI](../especificaciones/ES-F01-02-RegistrarZonaCobertura/ui.md) · [Plan](../especificaciones/ES-F01-02-RegistrarZonaCobertura/plan.md) · [Tareas](../especificaciones/ES-F01-02-RegistrarZonaCobertura/tasks.md) · [Evidencia](../especificaciones/ES-F01-02-RegistrarZonaCobertura/evidence.md) | Borrador SDD; implementación pendiente |
| **ES-F01-03** | Activar y desactivar una zona de cobertura | [Especificación](../especificaciones/ES-F01-03-ActivarDesactivarZona/spec.md) · [UI](../especificaciones/ES-F01-03-ActivarDesactivarZona/ui.md) · [Plan](../especificaciones/ES-F01-03-ActivarDesactivarZona/plan.md) · [Tareas](../especificaciones/ES-F01-03-ActivarDesactivarZona/tasks.md) · [Evidencia](../especificaciones/ES-F01-03-ActivarDesactivarZona/evidence.md) | Borrador SDD; implementación pendiente |
| **ES-F01-04** | Configurar la tarifa vigente de una zona | [Especificación](../especificaciones/ES-F01-04-ConfigurarTarifaZona/spec.md) · [UI](../especificaciones/ES-F01-04-ConfigurarTarifaZona/ui.md) · [Plan](../especificaciones/ES-F01-04-ConfigurarTarifaZona/plan.md) · [Tareas](../especificaciones/ES-F01-04-ConfigurarTarifaZona/tasks.md) · [Evidencia](../especificaciones/ES-F01-04-ConfigurarTarifaZona/evidence.md) | Borrador SDD; implementación pendiente |
| **ES-F01-05** | Consultar la cobertura de un destino | [Especificación](../especificaciones/ES-F01-05-ConsultarCoberturaDestino/spec.md) · [Plan](../especificaciones/ES-F01-05-ConsultarCoberturaDestino/plan.md) · [Tareas](../especificaciones/ES-F01-05-ConsultarCoberturaDestino/tasks.md) · [Evidencia](../especificaciones/ES-F01-05-ConsultarCoberturaDestino/evidence.md) | Borrador SDD; implementación pendiente |
| **ES-F01-06** | Cotizar el envío con datos físicos de productos | [Ver especificación](../especificaciones/ES-F01-06-CotizarEnvioConProductos.md) | Borrador |
| **ES-F01-07** | Resolver la zona de un destino para el módulo | [Ver especificación](../especificaciones/ES-F01-07-ResolverZonaParaModulo.md) | Borrador |
| **ES-F01-08** | Registrar la trazabilidad de la configuración | [Ver especificación](../especificaciones/ES-F01-08-RegistrarTrazabilidadConfiguracion.md) | Borrador |

## Especificaciones atómicas de F-02

| ID | Comportamiento | Especificación | Estado |
|---|---|---|---|
| **ES-F02-01** | Recepción de solicitudes de despacho | [Ver especificación](../especificaciones/ES-F02-01-RecepcionSolicitudDespacho.md) | Borrador |
| **ES-F02-02** | Generación de despachos de prueba para simulación | [Ver especificación](../especificaciones/ES-F02-02-GenerarDespachoPrueba.md) | Borrador |
| **ES-F02-03** | Consultar la cola de despachos pendientes | [Ver especificación](../especificaciones/ES-F02-03-ConsultarColaPendientes.md) | Borrador |
| **ES-F02-04** | Asignar despacho a un repartidor | [Ver especificación](../especificaciones/ES-F02-04-AsignarDespachoRepartidor.md) | Borrador |
| **ES-F02-05** | Consultar y reordenar la secuencia de ruta | [Ver especificación](../especificaciones/ES-F02-05-ConsultarReordenarSecuenciaRuta.md) | Borrador |
| **ES-F02-06** | Reasignar despacho a otro repartidor | [Ver especificación](../especificaciones/ES-F02-06-ReasignarDespachoRepartidor.md) | Borrador |
| **ES-F02-07** | Cancelar despacho por anulación del pedido | [Ver especificación](../especificaciones/ES-F02-07-CancelarDespachoPorAnulacion.md) | Borrador |
| **ES-F02-08** | Registrar la trazabilidad de las operaciones | [Ver especificación](../especificaciones/ES-F02-08-RegistrarTrazabilidadOperaciones.md) | Borrador |

## Especificaciones atómicas de F-04

| ID | Comportamiento | Especificación | Estado |
|---|---|---|---|
| **ES-F04-01** | Consultar entregas fallidas | [Especificación](../especificaciones/ES-F04-01-ConsultarEntregasFallidas/spec.md) · [UI](../especificaciones/ES-F04-01-ConsultarEntregasFallidas/ui.md) · [Plan](../especificaciones/ES-F04-01-ConsultarEntregasFallidas/plan.md) · [Tareas](../especificaciones/ES-F04-01-ConsultarEntregasFallidas/tasks.md) · [Evidencia](../especificaciones/ES-F04-01-ConsultarEntregasFallidas/evidence.md) | T-06/T-07 en curso; lectores y caso de uso con indicadores/paginación verificados por partes; migraciones compartidas, endpoint e integración real pendientes |
| **ES-F04-02** | Consultar el detalle de una incidencia | [Especificación](../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/spec.md) · [UI](../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/ui.md) · [Plan](../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/plan.md) · [Tareas](../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/tasks.md) · [Evidencia](../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/evidence.md) | Borrador SDD; implementación y verificación pendientes |
| **ES-F04-03** | Confirmar la recepción del paquete | [Especificación](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/spec.md) · [UI](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/ui.md) · [Plan](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/plan.md) · [Tareas](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/tasks.md) · [Evidencia](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/evidence.md) | Borrador SDD; implementación y verificación pendientes |
| **ES-F04-04** | Reprogramar un despacho fallido | [Especificación](../especificaciones/ES-F04-04-ReprogramarDespachoFallido/spec.md) · [UI](../especificaciones/ES-F04-04-ReprogramarDespachoFallido/ui.md) · [Plan](../especificaciones/ES-F04-04-ReprogramarDespachoFallido/plan.md) · [Tareas](../especificaciones/ES-F04-04-ReprogramarDespachoFallido/tasks.md) · [Evidencia](../especificaciones/ES-F04-04-ReprogramarDespachoFallido/evidence.md) | Preparación SDD completada; implementación y pruebas pendientes |
| **ES-F04-05** | Cerrar un despacho como devuelto a origen | [Especificación](../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen/spec.md) · [UI](../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen/ui.md) · [Plan](../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen/plan.md) · [Tareas](../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen/tasks.md) · [Evidencia](../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen/evidence.md) | Preparación SDD completada; implementación y pruebas pendientes |
| **ES-F04-06** | Registrar la trazabilidad de las operaciones | [Especificación](../especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones/spec.md) · [Plan](../especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones/plan.md) · [Tareas](../especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones/tasks.md) · [Evidencia](../especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones/evidence.md) | Preparación SDD completada; UI propia no aplica; implementación y pruebas pendientes |

## Especificaciones atómicas de F-05

| ID | Comportamiento | Especificación | Estado |
|---|---|---|---|
| **ES-F05-01** | Registrar un nuevo repartidor | [Ver especificación](../especificaciones/ES-F05-01-RegistrarRepartidor.md) | Borrador |
| **ES-F05-02** | Consultar repartidores | [Ver especificación](../especificaciones/ES-F05-02-ConsultarRepartidores.md) | Borrador |
| **ES-F05-03** | Editar datos del repartidor | [Ver especificación](../especificaciones/ES-F05-03-EditarRepartidor.md) | Borrador |
| **ES-F05-04** | Dar de baja lógica al repartidor | [Ver especificación](../especificaciones/ES-F05-04-DarDeBajaRepartidor.md) | Borrador |
| **ES-F05-05** | Vincular repartidor con Seguridad y Usuarios | [Ver especificación](../especificaciones/ES-F05-05-VincularRepartidorConSeguridad.md) | Borrador |
| **ES-F05-06** | Registrar una nueva furgoneta | [Ver especificación](../especificaciones/ES-F05-06-RegistrarFurgoneta.md) | Borrador |
| **ES-F05-07** | Consultar furgonetas | [Ver especificación](../especificaciones/ES-F05-07-ConsultarFurgonetas.md) | Borrador |
| **ES-F05-08** | Editar furgoneta y límites de carga | [Ver especificación](../especificaciones/ES-F05-08-EditarFurgoneta.md) | Borrador |
| **ES-F05-09** | Cambiar estado de furgoneta | [Ver especificación](../especificaciones/ES-F05-09-CambiarEstadoFurgoneta.md) | Borrador |

## Requisitos transversales

La gestión de estados del despacho y el seguimiento del pedido en ruta se especifican como requisitos transversales (RT-01 a RT-04) en la sección 6 de [overview.md](../overview.md). No constituyen una funcionalidad independiente.

Los responsables deben mantener este índice actualizado cuando una especificación sea creada, revisada o cambie de estado.
