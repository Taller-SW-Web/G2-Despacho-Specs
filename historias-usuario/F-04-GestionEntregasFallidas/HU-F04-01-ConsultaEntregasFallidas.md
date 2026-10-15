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

**PARA** identificar qué paquetes faltan retornar al centro, cuáles ya fueron recibidos y cuáles están pendientes de una decisión.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-04-GestionEntregasFallidas.md](../../funcionalidades/F-04-GestionEntregasFallidas.md), `RF-01`, indicadores de `RF-06` y `RF-07`; `CA-01`, `CA-02`, `CA-03` y `CA-18` [cite: 1].
- **Especificación atómica:** [ES-F04-01](../../especificaciones/ES-F04-01-ConsultarEntregasFallidas/spec.md).
- **Contrato asociado:** [API, sección 11](../../integraciones/api-contract.md#11-api-de-f-04-entregas-fallidas). La ruta de consulta ya está definida; los parámetros y respuestas completos siguen pendientes de concreción en el contrato único [cite: 2].
- **Roles requeridos:** `GESTOR_DESPACHO` con identidad autenticada. Un usuario sin el rol requerido no debe acceder a la información.
- **Componentes de Frontend:**
  - Pantalla responsive de Entregas Fallidas.
  - Listado paginado con estados de carga, vacío, error y éxito.
  - Filtros combinables por motivo, fecha de incidencia y recepción: todos, pendiente de retorno o recibido en centro.
  - Acciones `Ver detalle` y `Confirmar recepción`; la confirmación pertenece a HU-F04-06.
- **Reglas de negocio y visuales:**
  - Solo deben incluirse despachos cuyo estado vigente sea `FALLIDO`.
  - Cada resultado muestra código operativo interno, fecha del incidente, motivo, contador sobre el máximo configurado, repartidor, recepción, indicador de evidencia e indicador de pedido anulado.
  - `NO_INTENTADO` se identifica como `No intentado` y no consume intentos. La definición del catálogo para filtrar se resolverá en el contrato único; esta historia no autoriza a seleccionar ese motivo al registrar un fallo en campo.
  - Un paquete sin recepción cuya jornada ya terminó se identifica como `Retorno atrasado`, junto con el repartidor responsable. La fuente del cierre de jornada se concretará con Operación según los pendientes del plan de ES-F04-01.
  - La ausencia de incidencias debe representarse mediante un estado vacío y no mediante datos pertenecientes a otros estados.
  - El listado debe admitir paginación y no cargar todas las incidencias en una sola solicitud.
- **Datos involucrados:** despacho, reporte de fallo, intento y referencia de evidencia disponibles en el módulo.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-01: Listado con incidencias**
  - **DADO** que existen despachos en estado `FALLIDO`.
  - **CUANDO** el Gestor abre la pantalla de Entregas Fallidas.
  - **ENTONCES** el sistema muestra código operativo interno, fecha del incidente, motivo, contador sobre el máximo, repartidor, recepción, indicador de evidencia y pedido anulado, con paginación y filtros por motivo, fecha y recepción.

- [ ] **CA-02: Listado sin incidencias**
  - **DADO** que no existen despachos en estado `FALLIDO`.
  - **CUANDO** el Gestor abre la pantalla.
  - **ENTONCES** el sistema muestra un estado vacío y no presenta información de otros estados.

- [ ] **CA-03: Acceso sin permisos**
  - **DADO** que un usuario sin el rol requerido intenta consultar las incidencias.
  - **CUANDO** realiza la solicitud con su credencial de acceso.
  - **ENTONCES** el backend rechaza la operación con `403 Forbidden` y no expone información del despacho.

- [ ] **CA-18: Paquete no retornado al cierre de la jornada**
  - **DADO** un despacho `FALLIDO` cuyo repartidor ya cerró su jornada y cuyo paquete no tiene recepción confirmada.
  - **CUANDO** el Gestor consulta el listado.
  - **ENTONCES** el sistema lo resalta como `Retorno atrasado` y muestra el repartidor responsable.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Consulta paginada implementada en backend, limitada a despachos con estado `FALLIDO`.
- [ ] Control de acceso implementado y validado para el rol `GESTOR_DESPACHO`.
- [ ] Pantalla responsive implementada con estados de carga, vacío, error y éxito.
- [ ] Pruebas de integración cubren filtros combinados, paginación, listado con datos, vacío, acceso sin permisos y retorno atrasado.
- [ ] Se distinguen recepción pendiente/confirmada, `NO_INTENTADO`, pedido anulado y presencia/ausencia de evidencia.
- [ ] La consulta no confirma recepciones, cambia estados, libera capacidad ni publica eventos.
- [ ] Pruebas de frontend verifican la información mínima y los estados visuales definidos.
- [ ] Contrato HTTP validado y actualizado en [integraciones/api-contract.md](../../integraciones/api-contract.md) antes de cerrar la historia.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
