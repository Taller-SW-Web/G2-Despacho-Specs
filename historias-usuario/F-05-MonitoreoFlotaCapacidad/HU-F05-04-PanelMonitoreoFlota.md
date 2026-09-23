# [HU-F05-04] Panel Gráfico de Monitoreo de Ocupación de Flota

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-05: Monitoreo de Flota, Operadores y Capacidad Diaria |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-05`, `sdd`, `monitoreo`, `dashboard`, `capacidad` |
| **Responsable sugerido** | Rhamses |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho
**QUIERO** visualizar en un dashboard el estado de ocupación de cada repartidor en turno y un resumen global de la flota, con indicadores visuales actualizados
**PARA** tomar decisiones operativas en tiempo real sobre la redistribución de carga y detectar rápidamente operadores saturados o sin actividad.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-05-MonitoreoFlotaCapacidad.md](../../funcionalidades/F-05-MonitoreoFlotaCapacidad.md) (Requisito `RF-04`, Criterios `CA-10`, `CA-11`).
- **Endpoints asociados:**
  - `GET /api/v1/flota/resumen-capacidad` — Panel resumen global de ocupación (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md) §7.2).
  - `GET /api/v1/repartidores/disponibles` — Datos individuales por repartidor con porcentaje de ocupación (§7.1).
- **Rol requerido:** `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Dashboard de Monitoreo: tarjetas de resumen global (`DISPONIBLES`, `EN_RUTA`, `SATURADOS`, `INACTIVOS`) y tabla por repartidor con barra de progreso coloreada por nivel de ocupación.
  - Actualización periódica sin recarga de página mediante polling con `@tanstack/react-query`.
- **Reglas de negocio y visuales:**
  - La barra de progreso muestra el porcentaje de paquetes asignados (estados `ASIGNADO` o `EN_CAMINO`) respecto al límite diario configurado.
  - Al superar el umbral de saturación (referencia ≥ 90%), la barra cambia a color rojo y el repartidor se etiqueta como `SATURADO`.
  - El resumen global se calcula en el backend a partir de los conteos actualizados de cada estado.
  - El panel debe soportar paginación para equipos con más de 50 operadores activos simultáneos.
- **Entidades de datos involucradas:** `repartidores`, `furgonetas`, `asignaciones_diarias`, `reservas_capacidad` y `proyecciones_despacho`.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-10: Visualización de repartidor saturado**
  - **DADO** que un repartidor tiene un tope de 50 paquetes y se le han asignado 48 despachos en estado `ASIGNADO` o `EN_CAMINO`.
  - **CUANDO** el Gestor de Despacho consulta el panel de monitoreo.
  - **ENTONCES** el sistema muestra al operador con una barra de progreso en color rojo, etiqueta de estado `SATURADO` y la relación numérica `48/50 paquetes (96%)`.

- [ ] **CA-11: Resumen global de disponibilidad de flota**
  - **DADO** que existen 8 repartidores en turno con distintos estados de carga.
  - **CUANDO** el Gestor accede al panel de monitoreo.
  - **ENTONCES** el sistema muestra tarjetas de resumen con el total de repartidores `DISPONIBLES`, `EN_RUTA`, `SATURADOS` e `INACTIVOS`, actualizadas sin necesidad de recargar la página.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Código implementado en Java 21 / Spring Boot siguiendo las convenciones de [AGENTS.md](../../AGENTS.md).
- [ ] Motor de cálculo de ocupación implementado en backend: suma de despachos activos (`ASIGNADO` + `EN_CAMINO`) por repartidor frente a su límite diario configurado.
- [ ] Endpoint `GET /api/v1/flota/resumen-capacidad` implementado y documentado en [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Tiempo de respuesta de `GET /api/v1/flota/resumen-capacidad` menor a 300 ms para 50 repartidores activos.
- [ ] Pruebas unitarias (`JUnit 5 + Mockito`) del motor de cálculo de ocupación y las reglas de coloreado por umbral.
- [ ] Prueba de integración verificando los conteos correctos por estado con datos en base de datos.
- [ ] Dashboard de Monitoreo implementado en React + Tailwind con tarjetas de resumen global y tabla con barras de progreso coloreadas.
- [ ] Actualización periódica implementada mediante polling con `@tanstack/react-query`.
- [ ] Paginación implementada en la tabla de repartidores para soportar más de 50 operadores.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
