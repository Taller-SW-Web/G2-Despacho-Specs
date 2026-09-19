# Especificaciones Detalladas: Formularios y Procesos

Este directorio centraliza las **especificaciones técnicas granulares** del Módulo de Despacho y Entrega a Domicilio. Cada archivo describe de forma exhaustiva y sin ambigüedades un único componente del sistema, clasificado según su naturaleza:

1. **Formularios / Vistas (`FORM`):** Pantallas, paneles, modales y formularios interactivos orientados al usuario (Gestor de Despacho, Gestor de Flota, Repartidor o Administrador).
2. **Procesos Internos (`PROC`):** Servicios transaccionales de backend, casos de uso de dominio, jobs programados (cron), integraciones entre módulos o APIs síncronas/asíncronas no visibles directamente por el usuario.

Todas las especificaciones se almacenan en este mismo directorio plano para facilitar su localización, versionado y trazabilidad directa con `specs/funcionalidades/`, `specs/api-contract.md` y `specs/modelo-datos.md`.

---

## 1. Convención de Nombres

Cada especificación granular sigue el formato:

```text
SPEC-F<XX>-[FORM|PROC]-<NombreEnPascalCase>.md
```

- `SPEC`: Prefijo identificador de especificación detallada.
- `F<XX>`: Macro-funcionalidad de origen (`F01`, `F02`, `F03`, `F04`, `F05`, o `TRANS` para transversales).
- `FORM` o `PROC`: Naturaleza del componente (Formulario/Vista o Proceso interno).
- `NombreEnPascalCase`: Nombre descriptivo del formulario o proceso.

---

## 2. Plantilla Estándar de Especificación (11 Secciones)

Cada documento cumple con las secciones obligatorias establecidas en las reglas de arquitectura (`AGENTS.md`):

1. **Encabezado y Metadatos:** ID, Título, Tipo (`Formulario/Vista` o `Proceso Interno`), Macro-funcionalidad padre, Responsable (`Por definir`), Estado.
2. **Contexto:** Ubicación del componente dentro del flujo operativo global.
3. **Propósito:** Objetivo concreto de negocio o técnico que resuelve.
4. **Alcance:** Capacidades incluidas y delimitación técnica.
5. **Precondiciones, dependencias y resultados:** Requisitos previos, servicios consumidos y efectos persistentes.
6. **Requisitos y criterios de aceptación (Gherkin):** Escenarios automatizables bajo estructura `DADO / CUANDO / ENTONCES`.
7. **Frontend:** Estructura visual, campos, validaciones de cliente, feedback de errores (o `N/A - Componente de backend` en procesos puros).
8. **Backend:** Endpoints, DTOs, lógica de dominio, transaccionalidad `@Transactional`, control de concurrencia e integraciones.
9. **Requisitos no funcionales:** Rendimiento, seguridad RBAC, concurrencia, idempotencia y auditoría.
10. **Fuera de alcance:** Límites estrictos para prevenir solapamiento entre componentes.
11. **Estrategia de verificación y Criterio de completitud:** Pruebas unitarias, integración y criterios de aceptación definitivos.

---

## 3. Cuadro de Asignación de Responsabilidades y Estado

El siguiente cuadro consolida el catálogo completo de especificaciones granulares. La asignación de responsables se encuentra **pendiente de distribución por el equipo**:

| ID Spec | Tipo | Título del Componente | Funcionalidad Origen | Responsable Asignado | Estado |
|---|---|---|---|---|---|
| **`SPEC-F01-FORM-01`** | Formulario | [Panel y Delimitación Geoespacial de Zonas](./SPEC-F01-FORM-01-GestionZonasGeograficas.md) | F-01 (Zonas y Tarifas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F01-FORM-02`** | Formulario | [Parametrización de Matriz Tarifaria](./SPEC-F01-FORM-02-MatrizTarifaria.md) | F-01 (Zonas y Tarifas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F01-PROC-01`** | Proceso | [Motor de Cotización en Tiempo Real con Rate Limit](./SPEC-F01-PROC-01-MotorCotizacionEnvios.md) | F-01 (Zonas y Tarifas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F01-PROC-02`** | Proceso | [Servicio PostGIS de Resolución de Cobertura y Zona](./SPEC-F01-PROC-02-ResolucionGeoespacialZona.md) | F-01 (Zonas y Tarifas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F02-FORM-01`** | Formulario | [Dashboard de Cola de Despachos Pendientes](./SPEC-F02-FORM-01-DashboardColaPendientes.md) | F-02 (Programación) | *Por definir* | 🟢 Especificado |
| **`SPEC-F02-FORM-02`** | Formulario | [Modal de Asignación de Repartidor y Ocupación](./SPEC-F02-FORM-02-ModalAsignacionRepartidor.md) | F-02 (Programación) | *Por definir* | 🟢 Especificado |
| **`SPEC-F02-FORM-03`** | Formulario | [Diálogo de Generación de Pedidos de Prueba](./SPEC-F02-FORM-03-DialogoSimulacionPedidos.md) | F-02 (Programación) | *Por definir* | 🟢 Especificado |
| **`SPEC-F02-PROC-01`** | Proceso | [Recepción y Validación de Solicitudes Externas](./SPEC-F02-PROC-01-RecepcionValidacionSolicitudes.md) | F-02 (Programación) | *Por definir* | 🟢 Especificado |
| **`SPEC-F02-PROC-02`** | Proceso | [Asignación Transaccional y Control de Capacidad](./SPEC-F02-PROC-02-AsignacionTransaccionalCapacidad.md) | F-02 (Programación) | *Por definir* | 🟢 Especificado |
| **`SPEC-F02-PROC-03`** | Proceso | [Auditoría Inmutable y Trazabilidad de Asignaciones](./SPEC-F02-PROC-03-AuditoriaTrazabilidadAsignacion.md) | F-02 (Programación) | *Por definir* | 🟢 Especificado |
| **`SPEC-F03-FORM-01`** | Formulario | [Vista Mobile "Mi Ruta" y Detalle de Despacho](./SPEC-F03-FORM-01-VistaMiRutaDetalle.md) | F-03 (App Repartidor) | *Por definir* | 🟢 Especificado |
| **`SPEC-F03-FORM-02`** | Formulario | [Formulario de Entrega Exitosa y Captura Fotográfica](./SPEC-F03-FORM-02-FormularioEntregaExitosa.md) | F-03 (App Repartidor) | *Por definir* | 🟢 Especificado |
| **`SPEC-F03-FORM-03`** | Formulario | [Formulario de Reporte de Incidencias en Campo](./SPEC-F03-FORM-03-FormularioEntregaFallida.md) | F-03 (App Repartidor) | *Por definir* | 🟢 Especificado |
| **`SPEC-F03-FORM-04`** | Formulario | [Vista de Cierre de Jornada y Resumen Diario](./SPEC-F03-FORM-04-VistaCierreJornadaResumen.md) | F-03 (App Repartidor) | *Por definir* | 🟢 Especificado |
| **`SPEC-F03-PROC-01`** | Proceso | [Transiciones de Estado de Campo e Idempotencia](./SPEC-F03-PROC-01-TransicionesCampoIdempotencia.md) | F-03 (App Repartidor) | *Por definir* | 🟢 Especificado |
| **`SPEC-F03-PROC-02`** | Proceso | [Gestión de Storage Privado y URLs Firmadas](./SPEC-F03-PROC-02-AlmacenamientoUrlsFirmadas.md) | F-03 (App Repartidor) | *Por definir* | 🟢 Especificado |
| **`SPEC-F03-PROC-03`** | Proceso | [Corte Automático de Jornada de Respaldo (Batch)](./SPEC-F03-PROC-03-CorteAutomaticoJornadaBatch.md) | F-03 (App Repartidor) | *Por definir* | 🟢 Especificado |
| **`SPEC-F04-FORM-01`** | Formulario | [Panel Operativo de Entregas Fallidas](./SPEC-F04-FORM-01-PanelEntregasFallidas.md) | F-04 (Entregas Fallidas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F04-FORM-02`** | Formulario | [Formulario de Confirmación de Recepción en Centro](./SPEC-F04-FORM-02-FormularioRecepcionCentro.md) | F-04 (Entregas Fallidas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F04-FORM-03`** | Formulario | [Modal de Reprogramación de Despacho](./SPEC-F04-FORM-03-ModalReprogramacionDespacho.md) | F-04 (Entregas Fallidas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F04-FORM-04`** | Formulario | [Modal de Cierre como Devuelto a Origen](./SPEC-F04-FORM-04-ModalCierreDevolucionOrigen.md) | F-04 (Entregas Fallidas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F04-PROC-01`** | Proceso | [Evaluación de Política de Intentos y Transición](./SPEC-F04-PROC-01-PoliticaIntentosTransicion.md) | F-04 (Entregas Fallidas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F04-PROC-02`** | Proceso | [Publicación de Eventos de Devolución hacia Ventas](./SPEC-F04-PROC-02-PublicacionEventosVentas.md) | F-04 (Entregas Fallidas) | *Por definir* | 🟢 Especificado |
| **`SPEC-F05-FORM-01`** | Formulario | [Panel y Formulario de Repartidores](./SPEC-F05-FORM-01-PanelFormularioRepartidores.md) | F-05 (Flota y Capacidad) | *Por definir* | 🟢 Especificado |
| **`SPEC-F05-FORM-02`** | Formulario | [Panel y Formulario de Catálogo de Vehículos](./SPEC-F05-FORM-02-PanelFormularioVehiculos.md) | F-05 (Flota y Capacidad) | *Por definir* | 🟢 Especificado |
| **`SPEC-F05-FORM-03`** | Formulario | [Formulario de Asignación Diaria de Jornada](./SPEC-F05-FORM-03-FormularioAsignacionDiaria.md) | F-05 (Flota y Capacidad) | *Por definir* | 🟢 Especificado |
| **`SPEC-F05-FORM-04`** | Formulario | [Dashboard de Monitoreo Semafórico de Ocupación](./SPEC-F05-FORM-04-DashboardOcupacionFlota.md) | F-05 (Flota y Capacidad) | *Por definir* | 🟢 Especificado |
| **`SPEC-F05-PROC-01`** | Proceso | [Motor Dinámico de Ocupación y Estado Operativo](./SPEC-F05-PROC-01-MotorCalculoOcupacion.md) | F-05 (Flota y Capacidad) | *Por definir* | 🟢 Especificado |
| **`SPEC-F05-PROC-02`** | Proceso | [Servicio REST de Disponibilidad y Saldo Remanente](./SPEC-F05-PROC-02-ConsultaDisponibilidadFlota.md) | F-05 (Flota y Capacidad) | *Por definir* | 🟢 Especificado |
| **`SPEC-F05-PROC-03`** | Proceso | [Integración y Sincronización con Seguridad](./SPEC-F05-PROC-03-VinculacionSeguridadUsuarios.md) | F-05 (Flota y Capacidad) | *Por definir* | 🟢 Especificado |
| **`SPEC-TRANS-PROC-01`** | Proceso | [Motor Transversal de Máquina de Estados](./SPEC-TRANS-PROC-01-MaquinaEstadosCicloVida.md) | Transversal | *Por definir* | 🟢 Especificado |
| **`SPEC-TRANS-PROC-02`** | Proceso | [Servicio Centralizado de Historial y Auditoría](./SPEC-TRANS-PROC-02-HistorialAuditoriaComun.md) | Transversal | *Por definir* | 🟢 Especificado |
| **`SPEC-TRANS-PROC-03`** | Proceso | [Mecanismo Outbox de Eventos hacia Ventas](./SPEC-TRANS-PROC-03-MecanismoOutboxEventos.md) | Transversal | *Por definir* | 🟢 Especificado |
