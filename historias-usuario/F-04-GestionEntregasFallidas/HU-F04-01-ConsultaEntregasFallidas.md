# [HU-F04-01] Consulta de Entregas Fallidas

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-04: Entregas Fallidas y Reprogramaciones |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-04`, `sdd`, `entrega-fallida`, `consulta` |
| **Responsable sugerido** | Gerardo |

---

## 1. Declaración de la Historia (User Story)

**COMO** Gestor de Despacho  
**QUIERO** consultar en una bandeja paginada los despachos que se encuentran en estado `FALLIDO`  
**PARA** identificar las incidencias pendientes de evaluación y decidir oportunamente cómo resolverlas.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md) (Requisito `RF-01`, Criterios `CA-01`, `CA-02`, `CA-03`).
- **Endpoints asociados:** pendientes de validación en el contrato único [integraciones/api-contract.md](../../integraciones/api-contract.md). Esta historia no establece rutas ni estructuras de respuesta.
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada. Un usuario sin el rol requerido no debe acceder a la información.
- **Componentes de Frontend:**
  - Pantalla responsive de Entregas Fallidas.
  - Listado paginado con estados de carga, vacío, error y éxito.
  - Filtros operativos cuya definición final debe conservar el criterio obligatorio de mostrar exclusivamente despachos `FALLIDO`.
- **Reglas de negocio y visuales:**
  - Solo deben incluirse despachos cuyo estado vigente sea `FALLIDO`.
  - Cada resultado debe mostrar, como mínimo, código de rastreo, fecha del incidente, motivo, número de intento y disponibilidad de evidencia.
  - La ausencia de incidencias debe representarse mediante un estado vacío y no mediante datos pertenecientes a otros estados.
  - El listado debe admitir paginación y no cargar todas las incidencias en una sola solicitud.
- **Datos involucrados:** despacho, reporte de fallo, intento y referencia de evidencia disponibles en el módulo.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-01: Listado con incidencias**
  - **DADO** que existen despachos en estado `FALLIDO`.
  - **CUANDO** el Gestor abre la pantalla de Entregas Fallidas.
  - **ENTONCES** el sistema muestra el código de rastreo, fecha del incidente, motivo, número de intento y evidencia disponible.

- [ ] **CA-02: Listado sin incidencias**
  - **DADO** que no existen despachos en estado `FALLIDO`.
  - **CUANDO** el Gestor abre la pantalla.
  - **ENTONCES** el sistema muestra un estado vacío y no presenta información de otros estados.

- [ ] **CA-03: Acceso sin permisos**
  - **DADO** que un usuario sin el rol requerido intenta consultar las incidencias.
  - **CUANDO** realiza la solicitud con su credencial de acceso.
  - **ENTONCES** el backend rechaza la operación con `403 Forbidden` y no expone información del despacho.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Consulta paginada implementada en backend, limitada a despachos con estado `FALLIDO`.
- [ ] Control de acceso implementado y validado para el rol `GESTOR_DESPACHO`.
- [ ] Pantalla responsive implementada con estados de carga, vacío, error y éxito.
- [ ] Pruebas unitarias y de integración cubren el listado con datos, el estado vacío y el acceso sin permisos.
- [ ] Pruebas de frontend verifican la información mínima y los estados visuales definidos.
- [ ] Contrato HTTP validado y actualizado en [integraciones/api-contract.md](../../integraciones/api-contract.md) antes de cerrar la historia.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
