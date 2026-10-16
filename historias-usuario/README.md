# Historias de Usuario: Módulo de Despacho

Este directorio centraliza las **Historias de Usuario (HU)** del Módulo de Despacho y Entrega a Domicilio, organizadas en subdirectorios por cada funcionalidad del sistema.

Las historias están redactadas en un formato Markdown **100% compatible con Jira Software**, permitiendo su importación o carga manual directa en tableros Scrum/Kanban, y manteniendo trazabilidad bidireccional con los Requisitos Funcionales (`RF-XX`) y Criterios de Aceptación (`CA-XX`) definidos en `funcionalidades/`.

---

## 1. Estructura de Directorios

```text
historias-usuario/
├── README.md                                    # Guía general y plantilla estándar para Jira
├── F-01-Gestor_ZonasGeograficas/                # HUs de Zonas de cobertura y matriz tarifaria (Valqui)
├── F-02-ProgramacionAsignacionDespachos/        # HUs de Asignación y simulación de pedidos (Tarqui)
├── F-03-AppMovilRepartidor/                     # HUs de Web Responsive para repartidores (Max Rojas)
├── F-04-GestionEntregasFallidas/                # HUs de Incidencias y reprogramaciones (Gerardo)
├── F-05-MonitoreoFlotaCapacidad/                # HUs de repartidores, furgonetas y capacidad (Rhamses)
└── transversal-seguimiento/                     # HUs del canal de rastreo para clientes
```

---

## 2. Plantilla Estándar para Jira

Cada archivo de historia de usuario (`HU-F<XX>-<YY>-NombreCorto.md`) sigue la siguiente estructura:

```markdown
# [ID-HU] Título conciso de la historia

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-XX: Nombre de la Funcionalidad |
| **Prioridad** | Alta / Media / Baja |
| **Estimación (Story Points)** | 1 / 2 / 3 / 5 / 8 |
| **Componentes** | Backend / Frontend / Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-xx`, `sdd` |
| **Responsable sugerido** | Nombre del integrante |

---

## 1. Declaración de la Historia (User Story)
**COMO** [rol / actor]  
**QUIERO** [acción o capacidad]  
**PARA** [beneficio o valor de negocio]  

---

## 2. Descripción y Contexto Técnico
- **Endpoints asociados:** Rutas en `integraciones/api-contract.md`.
- **Reglas de negocio:** Validaciones de dominio y transaccionalidad.
- **Entidades de datos:** Tablas en `arquitectura/modelo-datos.md`.

---

## 3. Criterios de Aceptación (Gherkin)
- [ ] **CA-XX: Nombre del criterio**
  - **DADO** ...
  - **CUANDO** ...
  - **ENTONCES** ...

---

## 4. Definición de Terminado (Definition of Done - DoD)
- [ ] Código implementado siguiendo las convenciones de [AGENTS.md](../AGENTS.md).
- [ ] Pruebas unitarias (`JUnit 5 + Mockito` o `Vitest`) aprobadas.
- [ ] Contrato HTTP validado contra [integraciones/api-contract.md](../integraciones/api-contract.md).
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
```

---

## 3. Estado de Historias por Funcionalidad

| Funcionalidad | Responsable | Historias de Usuario | Estado |
|---|---|---|---|
| **F-01: Gestor de Zonas Geográficas** | Valqui | [HU-F01-01](./F-01-Gestor_ZonasGeograficas/HU-F01-01-AdministracionZonasCobertura.md)<br>[HU-F01-02](./F-01-Gestor_ZonasGeograficas/HU-F01-02-ConsultaEstadoZonas.md)<br>[HU-F01-03](./F-01-Gestor_ZonasGeograficas/HU-F01-03-ConfiguracionMatrizTarifaria.md)<br>[HU-F01-04](./F-01-Gestor_ZonasGeograficas/HU-F01-04-CotizacionEnviosTiempoReal.md)<br>[HU-F01-05](./F-01-Gestor_ZonasGeograficas/HU-F01-05-SeguridadTrazabilidadConfiguracion.md) | 🟢 Completado (5 HUs) |
| **F-02: Programación y Asignación** | Tarqui | [HU-F02-01](./F-02-ProgramacionAsignacionDespachos/HU-F02-01-RecepcionSolicitudesDespacho.md)<br>[HU-F02-02](./F-02-ProgramacionAsignacionDespachos/HU-F02-02-GeneracionPedidosPrueba.md)<br>[HU-F02-03](./F-02-ProgramacionAsignacionDespachos/HU-F02-03-ConsultaColaPendientes.md)<br>[HU-F02-04](./F-02-ProgramacionAsignacionDespachos/HU-F02-04-AsignacionDespachoRepartidor.md)<br>[HU-F02-05](./F-02-ProgramacionAsignacionDespachos/HU-F02-05-TrazabilidadAuditoriaAsignacion.md) | 🟢 Completado (5 HUs) |
| **F-03: Web Repartidor y Evidencia** | Max Rojas | Pendiente de redacción | ⚪ Pendiente |
| **F-04: Entregas Fallidas** | Gerardo | [HU-F04-01](./F-04-GestionEntregasFallidas/HU-F04-01-ConsultaEntregasFallidas.md)<br>[HU-F04-02](./F-04-GestionEntregasFallidas/HU-F04-02-ConsultaDetalleIncidencia.md)<br>[HU-F04-03](./F-04-GestionEntregasFallidas/HU-F04-03-ReprogramacionDespachoFallido.md)<br>[HU-F04-04](./F-04-GestionEntregasFallidas/HU-F04-04-CierreDespachoDevueltoAOrigen.md)<br>[HU-F04-05](./F-04-GestionEntregasFallidas/HU-F04-05-TrazabilidadDecisiones.md)<br>[HU-F04-06](./F-04-GestionEntregasFallidas/HU-F04-06-ConfirmacionRecepcionPaquete.md) | Documentación actualizada (6 HUs); implementación pendiente |
| **F-05: Monitoreo de Flota** | Rhamses | [HU-F05-01](./F-05-MonitoreoFlotaCapacidad/HU-F05-01-GestionRepartidores.md)<br>[HU-F05-02](./F-05-MonitoreoFlotaCapacidad/HU-F05-02-GestionVehiculos.md)<br>[HU-F05-03](./F-05-MonitoreoFlotaCapacidad/HU-F05-03-AsignacionOperativaDiaria.md)<br>[HU-F05-04](./F-05-MonitoreoFlotaCapacidad/HU-F05-04-PanelMonitoreoFlota.md)<br>[HU-F05-05](./F-05-MonitoreoFlotaCapacidad/HU-F05-05-ApiDisponibilidadRepartidores.md) | 🟢 Completado (5 HUs) |
| **Transversal: Seguimiento** | Equipo | Pendiente de redacción | ⚪ Pendiente |

Los identificadores HU y ES no expresan una secuencia de ejecución. En F-04, HU-F04-06 cubre la recepción previa a las decisiones de HU-F04-03/04; HU-F04-05 registra automáticamente la trazabilidad de las tres operaciones. La actualización documental conserva los IDs de los criterios de F-04 y no acredita implementación ni pruebas [cite: 1].

### 3.1. Trazabilidad de F-04

| Historia | Alcance principal | Requisitos y criterios de F-04 | Especificación atómica |
|---|---|---|---|
| HU-F04-01 | Listado, filtros e indicadores | RF-01; CA-01 a CA-03 y CA-18; indicadores de RF-06/07 | [ES-F04-01](../especificaciones/ES-F04-01-ConsultarEntregasFallidas/spec.md) |
| HU-F04-02 | Incidencia, recepción, historial y evidencia | RF-02; CA-04 y CA-05 | [ES-F04-02](../especificaciones/ES-F04-02-ConsultarDetalleIncidencia/spec.md) |
| HU-F04-03 | Reprogramación y restricciones | RF-03 y RF-06; CA-06 a CA-09, CA-14, CA-15 y CA-17 | [ES-F04-04](../especificaciones/ES-F04-04-ReprogramarDespachoFallido.md) |
| HU-F04-04 | Cierre como devuelto a origen | RF-04; CA-10 a CA-12 y CA-17; restricción de CA-15 | [ES-F04-05](../especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen.md) |
| HU-F04-05 | Trazabilidad automática | RF-05; CA-13 | [ES-F04-06](../especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones.md) |
| HU-F04-06 | Recepción física antes de decidir | RF-07; CA-16 y CA-17; relación con CA-18 | [ES-F04-03](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/spec.md) |

- [cite: 1] [Funcionalidad F-04 vigente](../funcionalidades/F-04-GestionEntregasFallidas.md).

