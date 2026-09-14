# [HU-F02-02] Generación Autónoma de Pedidos de Prueba (Testing)

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 2 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-02`, `sdd`, `simulacion`, `testing` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho o Desarrollador  
**QUIERO** generar órdenes y despachos simulados con datos válidos desde la interfaz o mediante un endpoint REST  
**PARA** disponer de carga de trabajo inmediata en la cola de asignación y realizar pruebas autónomas sin depender del módulo de Ventas ni de integraciones externas.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-02-ProgramacionAsignacionDespachos.md](../../specs/funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-01`, Criterio `CA-02`).
- **Endpoints asociados:**
  - `POST /api/v1/despachos/solicitudes/simular` (detallado en [specs/api-contract.md](../../specs/api-contract.md)).
- **Componentes de Frontend:**
  - Botón "Generar Pedido de Prueba" ubicado en la barra superior o cabecera del Panel de Programación.
- **Roles requeridos:** `GESTOR_DESPACHO` (autenticación JWT).
- **Reglas de negocio:**
  - El cuerpo de la solicitud es opcional. Puede recibir `{ "zona": "ZONA-LIMA-CENTRO", "pesoKg": 5.0 }` o `{}` para autogenerar todos los campos con valores realistas y válidos.
  - El sistema crea un pedido simulado (`PED-SIM-XXXXX`), genera un código de rastreo (`TRK-SIM-XXXXX`) y asigna estado `PENDIENTE_ASIGNACION`.
  - La dirección, coordenadas geográficas, teléfono y dimensiones se completan automáticamente dentro de una zona de cobertura válida.
  - El despacho generado debe ser visible de forma instantánea en la cola de asignación del dashboard.
- **Entidades de datos involucradas:** `despachos`, `historial_estados_despacho`.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-02: Generación autónoma de pedidos de prueba (testing)**
  - **DADO** que el Gestor de Despacho o desarrollador requiere generar carga de trabajo de prueba sin depender del módulo de Ventas.
  - **CUANDO** solicita la generación de prueba haciendo clic en el botón "Generar Pedido de Prueba" en la interfaz o invocando `POST /api/v1/despachos/solicitudes/simular`.
  - **ENTONCES** el sistema autogenera un pedido y despacho con datos consistentes en estado `PENDIENTE_ASIGNACION`, retorna código `201 Created` y lo incorpora de inmediato a la cola de asignación visible en el panel.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Servicio simulador implementado en Spring Boot con generador de datos coherentes (direcciones, pesos, volúmenes realistas).
- [ ] Endpoint `POST /api/v1/despachos/solicitudes/simular` probado con `JUnit 5 + Mockito` y `MockMvc`.
- [ ] Botón integrado en el frontend React + Tailwind que invoca la mutación y actualiza la lista mediante React Query / revalidación de estado.
- [ ] Notificación tipo toast ("Pedido de prueba creado exitosamente") en la interfaz al completarse la acción.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
