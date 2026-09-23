# Índice de funcionalidades

Este documento reúne las áreas funcionales del **Módulo de Despacho y Entrega a Domicilio** y permite consultar el estado de sus especificaciones.

| ID | Funcionalidad | Descripción breve | Responsable | Estado | Especificación |
|---|---|---|---|---|---|
| **F-01** | Gestión de zonas geográficas y cotización | Define cobertura, tarifas y la zona de cada despacho. | Valqui | En especificación | [Ver especificación](./F-01-Gestor_ZonasGeograficas.md) |
| **F-02** | Programación y asignación de despachos | Recibe solicitudes y asigna despachos con jornada y secuencia. | Tarqui | En especificación | [Ver especificación](./F-02-ProgramacionAsignacionDespachos.md) |
| **F-03** | Operación del repartidor y evidencia de entrega | Permite ejecutar entregas y registrar estados y evidencias. | Max | En especificación | [Ver especificación](./F-03-AppMovilRepartidor.md) |
| **F-04** | Entregas fallidas y reprogramaciones | Recibe en el centro los paquetes no entregados y decide su reprogramación o cierre. | Gerardo | En especificación | [Ver especificación](./F-04-GestionEntregasFallidas.md) |
| **F-05** | Monitoreo de flota, operadores y capacidad diaria | Administra repartidores, vehículos, jornadas y ocupación. | Rhamses | En especificación | [Ver especificación](./F-05-MonitoreoFlotaCapacidad.md) |

## Requisitos transversales

La gestión de estados del despacho y el seguimiento del pedido en ruta se especifican como requisitos transversales (RT-01 a RT-04) en la sección 6 de [overview.md](../overview.md). No constituyen una funcionalidad independiente.

Los responsables deben mantener este índice actualizado cuando una especificación sea creada, revisada o cambie de estado.
