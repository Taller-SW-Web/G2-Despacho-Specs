# [HU-F05-05] API de Disponibilidad de Repartidores para Programación

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-05: Monitoreo de Flota, Operadores y Capacidad Diaria |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-05`, `sdd`, `disponibilidad`, `api`, `integracion-f02` |
| **Responsable sugerido** | Rhamses |

---

## 1. Declaración de la Historia (User Story)

**COMO** Panel de Programación y Asignación (F-02)
**QUIERO** invocar un endpoint que retorne únicamente los repartidores habilitados para recibir nuevos despachos, con su balance de capacidad actualizado
**PARA** tomar decisiones de asignación precisas sin saturar operadores ni asignar paquetes que excedan la capacidad remanente del vehículo.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-05-MonitoreoFlotaCapacidad.md](../../specs/funcionalidades/F-05-MonitoreoFlotaCapacidad.md) (Requisito `RF-05`, Criterios `CA-12`, `CA-13`).
- **Endpoints asociados:**
  - `GET /api/v1/repartidores/disponibles` (detallado en [specs/api-contract.md](../../specs/api-contract.md) §7.1).
  - Parámetros de consulta opcionales: `zona` (string) y `pesoRequeridoKg` (float).
- **Roles requeridos:** `GESTOR_DESPACHO` o `GESTOR_FLOTA` (autenticación JWT). Endpoint de uso interno entre componentes del módulo.
- **Reglas de negocio y rendimiento:**
  - Solo se incluyen repartidores en estado `DISPONIBLE` o `EN_RUTA` con capacidad remanente mayor a cero.
  - Los repartidores `SATURADOS`, `FUERA_DE_TURNO` o `INACTIVOS` NO aparecen en la respuesta.
  - Si se proporciona `pesoRequeridoKg`, el endpoint filtra y retorna solo los operadores con capacidad de peso remanente mayor o igual al valor indicado.
  - Cuando no hay repartidores disponibles, el sistema retorna `200 OK` con lista vacía — no se genera error.
  - **Requisito de rendimiento:** respuesta en menos de 200 ms para no agregar latencia al flujo de asignación de F-02.
- **Entidades de datos involucradas:** `repartidores`, `vehiculos`, `despachos` (lectura del conteo activo).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-12: Respuesta con operadores disponibles y su balance de carga**
  - **DADO** que existen 5 repartidores en turno, de los cuales 3 tienen capacidad remanente (estados `DISPONIBLE` o `EN_RUTA`) y 2 están `SATURADOS` o `FUERA_DE_TURNO`.
  - **CUANDO** el servicio de F-02 invoca `GET /api/v1/repartidores/disponibles`.
  - **ENTONCES** el sistema retorna la lista de los 3 operadores habilitados, incluyendo por cada uno: identificador, nombre, tipo de vehículo, capacidad máxima, paquetes asignados, porcentaje de ocupación y estado.

- [ ] **CA-13: Respuesta vacía cuando no hay repartidores disponibles**
  - **DADO** que todos los repartidores en turno están `SATURADOS` o `FUERA_DE_TURNO`.
  - **CUANDO** F-02 invoca el endpoint de disponibilidad.
  - **ENTONCES** el sistema retorna código `200 OK` con una lista vacía, sin generar error.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Código implementado en Java 21 / Spring Boot siguiendo las convenciones de [AGENTS.md](../../AGENTS.md).
- [ ] Consulta optimizada en Spring Data JPA filtrando por estado (`DISPONIBLE`, `EN_RUTA`) y calculando capacidad remanente en tiempo real.
- [ ] Filtro opcional por `pesoRequeridoKg` implementado y validado con prueba unitaria.
- [ ] Pruebas unitarias (`JUnit 5 + Mockito`) cubriendo los 2 escenarios (`CA-12`, `CA-13`) y el filtro por peso.
- [ ] Prueba de rendimiento verificando tiempo de respuesta menor a 200 ms para al menos 30 repartidores activos.
- [ ] Prueba de integración con F-02: verificar que `HU-F02-04` consume este endpoint correctamente antes de asignar un despacho.
- [ ] Respuesta JSON alineada al contrato en [specs/api-contract.md](../../specs/api-contract.md) §7.1.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
