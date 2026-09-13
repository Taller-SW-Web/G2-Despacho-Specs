# Índice de funcionalidades

Este documento reúne las áreas funcionales del **Módulo de Despacho y Entrega a Domicilio** y permite consultar el estado de sus especificaciones.

| ID | Funcionalidad | Descripción breve | Responsable | Estado | Especificación |
|---|---|---|---|---|---|
| **F-01** | Gestión de zonas geográficas y cotización | Define cobertura geográfica y tarifas de entrega. | Valqui | En especificación | [Ver especificación](./funcionalidades/F-01-Gestor_ZonasGeograficas.md) |
| **F-02** | Programación y asignación de despachos | Gestiona la cola y asigna despachos a repartidores disponibles. | Tarqui | En especificación | [Ver especificación](./funcionalidades/F-02-ProgramacionAsignacionDespachos.md) |
| **F-03** | Operación del repartidor y evidencia de entrega | Permite ejecutar entregas y registrar estados y evidencias. | Max | Borrador inicial | [Ver especificación](./funcionalidades/F-03-AppMovilRepartidor.md) |
| **F-04** | Entregas fallidas y reprogramaciones | Resuelve incidencias mediante reprogramación o devolución a almacén. | Gerardo | En especificación | [Ver especificación](./funcionalidades/F-04-GestionEntregasFallidas.md) |
| **F-05** | Monitoreo de flota, operadores y capacidad diaria | Administra disponibilidad, turnos, vehículos y capacidad operativa. | Rhamses | Borrador inicial | [Ver especificación](./funcionalidades/F-05-MonitoreoFlotaCapacidad.md) |

## Capacidad transversal

El seguimiento de pedidos se expondrá mediante API para los canales autorizados. No se registra como una sexta funcionalidad independiente, ya que será una capacidad compartida por el backend del módulo.

Los responsables deben mantener este índice actualizado cuando una especificación sea creada, revisada o cambie de estado.
