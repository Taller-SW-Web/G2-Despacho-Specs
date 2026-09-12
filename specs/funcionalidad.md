# Índice de Especificaciones Funcionales

Este documento centraliza el inventario y estado de madurez de las especificaciones funcionales del módulo de Despacho. Cada especificación cuenta con su archivo correspondiente dentro del directorio `specs/funcionalidades/` respetando la plantilla oficial y los lineamientos de [AGENTS.md](../AGENTS.md).

---

## Tabla de Control de Funcionalidades

| ID | Nombre | Descripción Breve | Responsable | Estado | Archivo de Especificación |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **F-01** | Gestor de Zonas Geográficas y Cotizador de Envíos | Administración de cobertura geográfica, matriz tarifaria y endpoint de cotización para carritos de venta. | **VALQUI** (Integrante 1) | `Especificado` | [F-01-Gestor_ZonasGeograficas.md](funcionalidades/F-01-Gestor_ZonasGeograficas.md) |
| **F-02** | Panel de Programación y Asignación de Despachos | Dashboard de cola de pendientes, asignación de paquetes por capacidad y generación autónoma de órdenes de prueba. | **NICOLÁS** (Integrante 2) | `Especificado` | [F-02-ProgramacionAsignacionDespachos.md](funcionalidades/F-02-ProgramacionAsignacionDespachos.md) |
| **F-03** | App Móvil del Repartidor y Evidencia de Entrega | PWA móvil para ruta diaria, transiciones hacia adelante (`ASIGNADO` $\rightarrow$ `EN_CAMINO` $\rightarrow$ `ENTREGADO`/`FALLIDO`) y captura de fotos y firmas. | **MAX ROJAS** (Integrante 3) | `Especificado` | [F-03-AppMovilRepartidor.md](funcionalidades/F-03-AppMovilRepartidor.md) |
| **F-04** | Portal Web de Tracking de Envíos (Cliente) | Interfaz pública de solo lectura con buscador por código de rastreo, línea de tiempo de hitos y mapa de zona. | **Integrante 4** | `Especificado` | [F-04-PortalTrackingCliente.md](funcionalidades/F-04-PortalTrackingCliente.md) |
| **F-05** | Centro de Entregas Fallidas y Reprogramaciones | Gestión de incidencias en ruta, control de límite de reintentos, reprogramación o derivación a devolución a almacén. | **GERARDO** (Integrante 5) | `Especificado` | [F-05-GestionEntregasFallidas.md](funcionalidades/F-05-GestionEntregasFallidas.md) |
| **F-06** | Panel de Monitoreo de Flota, Operadores y Capacidad Diaria | CRUD de choferes y vehículos, control de turnos, límites de carga y servicio de disponibilidad para asignación. | **RHAMSES** (Integrante 6) | `Especificado` | [F-06-MonitoreoFlotaCapacidad.md](funcionalidades/F-06-MonitoreoFlotaCapacidad.md) |

---

## Convención de Estados

- **`Borrador`**: Archivo inicial o plantilla pendiente de completar con requisitos y escenarios Gherkin formales.
- **`Especificado`**: Documento formalizado con contexto, alcance, requisitos, escenarios Gherkin y no funcionales aprobados.
- **`En Implementación`**: En fase de codificación en frontend y/o backend.
- **`Completado`**: Implementado y verificado contra los criterios de completitud.