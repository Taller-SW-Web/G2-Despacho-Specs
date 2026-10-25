# ES-F03-08: Consulta autorizada de la evidencia

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md)

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor propietario o Gestor de Despacho

**UI:** Aplica; visor de evidencia.

## 1. Contexto y objetivo

Permitir visualizar la fotografía de evidencia de un despacho solo a usuarios autorizados, sin exponerla de forma pública, para que el repartidor y F-04 puedan revisarla. Concreta RF-09 de F-03.

## 2. Alcance

- Incluye: autorización de lectura, entrega de URL firmada temporal con vencimiento, visualización y renovación explícita de un enlace vencido.
- Fuera de alcance: carga, procesamiento y conservación de fotografías (ES-F03-05 y ES-F03-06); eliminación o edición de evidencias.

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor propietario del despacho (rol `REPARTIDOR`) o usuario con rol `GESTOR_DESPACHO`; al Gestor no se le exige perfil de repartidor.
- Precondiciones: el despacho tiene evidencia registrada.
- Disparador: el usuario solicita ver la evidencia.
- Resultado exitoso: URL firmada de lectura y su vencimiento.
- Resultado ante rechazo: `403` o acceso denegado al objeto, sin exponer la fotografía.

## 4. Flujo principal y alternativas

1. El usuario solicita ver la evidencia con el identificador obtenido del recurso autorizado.
2. El backend valida el token y verifica que sea el repartidor propietario o tenga rol `GESTOR_DESPACHO`.
3. El backend valida la asociación evidencia–despacho y concede una URL firmada temporal (Operación §3.4).
4. El frontend muestra la fotografía.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Sin firma válida o enlace vencido | Acceso directo al objeto | Acceso denegado | CA-02 |
| Renovación | El enlace venció en el visor | Nueva solicitud con validación de autorización | CA-01 |
| Usuario no autorizado | Ni propietario ni `GESTOR_DESPACHO` | `403 Forbidden` | CA-03 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | La evidencia nunca se expone de forma pública. | F-03 RF-09 |
| RN-02 | Un acceso al objeto sin firma válida o con enlace vencido se deniega. | F-03 CA-28 |
| RN-03 | Renovar el enlace exige validar otra vez la autorización del usuario. | F-03 RF-09 |
| RN-04 | Solo el repartidor propietario o un usuario `GESTOR_DESPACHO` obtienen la URL; otro usuario recibe `403`. | F-03 CA-29 |
| RN-05 | El visor no persiste URLs ni muestra la fotografía de otro recurso. | F-03 CA-27 |
| RN-06 | Un enlace vencido o un fallo de carga no significan ausencia de fotografía. | Operación §3.4 |

| Dato | Descripción |
|---|---|
| Entrada | JWT e identificador de evidencia obtenido del recurso autorizado |
| Salida | URL firmada de lectura, vencimiento e identificador del despacho asociado, o error contractual |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| Autorizar la lectura de evidencia | URL firmada, vigencia configurable, permisos y errores | [Operación §3.5](../../integraciones/api-contract-operacion-reparto.md#35-autorizar-la-lectura-de-evidencia) |
| Almacenamiento privado de evidencia | Origen de la fotografía | Operación de Reparto y Flota |
| F-04 Entregas Fallidas | Consulta de la evidencia de su incidencia, también después de resolver el despacho | F-04 |

## 6. Criterios de aceptación

### CA-01. Consulta autorizada de evidencia

- **DADO** un despacho con evidencia.
- **CUANDO** el repartidor propietario o un usuario con rol `GESTOR_DESPACHO` solicita verla.
- **ENTONCES** se devuelve una URL firmada y su vencimiento conforme a Operación §3.4; el visor la muestra y permite renovar explícitamente un enlace vencido, sin persistir URLs ni mostrar la fotografía de otro recurso.

### CA-02. Acceso sin autorización válida

- **DADO** un acceso al objeto sin firma válida o con enlace vencido.
- **CUANDO** se solicita la evidencia.
- **ENTONCES** el acceso es denegado.

### CA-03. Usuario no autorizado

- **DADO** un usuario que no es el repartidor propietario ni tiene rol `GESTOR_DESPACHO`.
- **CUANDO** solicita el acceso a la evidencia.
- **ENTONCES** el backend responde `403 Forbidden`.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: el contrato está definido en Operación §3.4; su implementación y comprobación real están pendientes.
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación

| Criterio | Tipo de comprobación | Datos o escenario |
|---|---|---|
| CA-01 | Integración y UI | Repartidor propietario y Gestor; enlace vencido y renovado |
| CA-02 | Seguridad | URL sin firma, firma alterada y enlace vencido |
| CA-03 | Seguridad | Otro repartidor y usuario de otro rol |

Tareas en [tasks.md](./tasks.md); resultados en [evidence.md](./evidence.md).

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-09 y CA-27 a CA-29.
2. [Pendientes](../../funcionalidades/pendiente.md), sección F-03.
3. [Contrato de operación de reparto, §3.5](../../integraciones/api-contract-operacion-reparto.md#35-autorizar-la-lectura-de-evidencia).
