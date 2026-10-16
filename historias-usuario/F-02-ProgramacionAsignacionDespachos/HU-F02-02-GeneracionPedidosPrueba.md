# [HU-F02-02] Generación Autónoma de Despachos de Prueba para Simulación

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `f-02`, `sdd`, `simulacion`, `testing`, `panel-programacion` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho o Desarrollador  
**QUIERO** generar órdenes y despachos simulados con datos válidos desde la interfaz o mediante un endpoint REST  
**PARA** disponer de carga de trabajo inmediata en la cola de asignación y realizar pruebas autónomas sin depender de órdenes reales ni de la disponibilidad del módulo de Ventas y Postventa.

---

## 2. Descripción y Contexto Técnico

- **Especificación SDD origen:** [ES-F02-02: Generación de despachos de prueba para simulación](../../especificaciones/ES-F02-02-GenerarDespachoPrueba/spec.md).
- **Especificación funcional padre:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-09`; Criterio `CA-20`).
- **Endpoints asociados:** `POST /api/v1/despachos/simulaciones` (detallado en [integraciones/api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación)).
- **Roles requeridos:** `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Botón secundario "Generar pedido de prueba" en la cabecera del Panel de Programación (`EncabezadoPagina` CR-05).
  - Modal opcional de simulación personalizada (CR-12).
  - Badge neutral punteado "Simulado" en la fila de la tabla (CR-09).
- **Reglas de negocio:**
  - Si el cuerpo está vacío (`{}`), genera automáticamente datos realistas dentro de una zona activa de F-01, con peso y volumen coherentes, `cantidadPaquetes = 1` y fecha programada igual a hoy.
  - Si se envían parámetros (`idZona`, `pesoKg`, `volumenM3`), valida que la zona exista y esté activa, y que peso y volumen sean positivos.
  - Setea `esSimulacion = true` en base de datos.
  - Los despachos simulados no emiten eventos webhooks externos hacia Ventas y Postventa (RT-03).
  - El nuevo despacho aparece inmediatamente en la cola de asignación con código `DSP-SIM-XXXXX` y `TRK-SIM-XXXXX`.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-20: Generación autónoma de despachos de prueba**
  - **DADO** que el Gestor de Despacho o desarrollador requiere generar carga de trabajo de prueba en la cola sin depender de Ventas y Postventa.
  - **CUANDO** solicita la generación de prueba haciendo clic en el botón "Generar pedido de prueba" en la interfaz o invoca `POST /api/v1/despachos/simulaciones`.
  - **ENTONCES** el sistema crea un despacho simulado en `PENDIENTE_ASIGNACION` con código operativo y de rastreo único (ej. `DSP-SIM-XXXXX`), asigna una zona activa de F-01 con datos físicos válidos, fecha de hoy, `esSimulacion = true`, responde `201 Created` e incorpora el registro de inmediato a la cola visible en el panel con la etiqueta "Simulado".

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Endpoint `POST /api/v1/despachos/simulaciones` implementado en Spring Boot con autorización JWT.
- [ ] Generador pseudoaleatorio de datos coherentes (direcciones, pesos, volúmenes dentro de rangos operativos).
- [ ] Pruebas unitarias y de integración con `JUnit 5 + MockMvc` cubriendo payload vacío, personalizado y rechazo por zona inactiva.
- [ ] Botón integrado en React con mutación TanStack Query, spinner de carga y toast Mantine Notifications.
- [ ] Documentación y trazabilidad sincronizadas con [ES-F02-02](../../especificaciones/ES-F02-02-GenerarDespachoPrueba/spec.md).
