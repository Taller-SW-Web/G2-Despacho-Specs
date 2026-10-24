# ES-F03-03: Consulta del detalle de un despacho

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md)

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor

**UI:** Aplica; vista de detalle del despacho de la web responsive del repartidor.

## 1. Contexto y objetivo

Mostrar al repartidor la información necesaria para ejecutar la entrega de un despacho y contactar al destinatario, protegiendo los datos personales frente a usuarios no autorizados. Concreta RF-03 y la sección 8 de F-03.

## 2. Alcance

- Incluye: consulta del detalle de un despacho propio, llamada directa al destinatario y protección de teléfono y dirección según estado.
- Fuera de alcance: geolocalización y navegación propia; edición de datos del destinatario; notificación al cliente final.

## 3. Actor, precondiciones y resultados

- Actor y autorización: JWT humano con perfil local activo y vinculado resuelto por `sub`, sin exigir rol global `REPARTIDOR`.
- Precondiciones: el despacho existe, está asignado al repartidor del token y pertenece a la jornada en curso.
- Disparador: el repartidor selecciona un despacho en «Mi Ruta» (ES-F03-02).
- Resultado exitoso: detalle del despacho.
- Resultado ante rechazo: `403` o `404` sin datos parciales.

## 4. Flujo principal y alternativas

1. El repartidor selecciona un despacho en «Mi Ruta».
2. El backend verifica que el despacho exista y pertenezca al repartidor del token.
3. El backend recupera los datos de entrega.
4. El frontend muestra el detalle con la opción de llamada directa.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Despacho ajeno | Asignado a otro repartidor | `403 Forbidden` | CA-02 |
| Despacho inexistente | El código no corresponde a ningún despacho | `404 Not Found` sin datos parciales | CA-03 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | El detalle muestra dirección, referencia, destinatario, teléfono con llamada directa, intento actual sobre el máximo configurado, fecha programada y estado. | F-03 CA-09 |
| RN-02 | Teléfono, dirección y destinatario se muestran solo al repartidor propietario y solo en `ASIGNADO` o `EN_CAMINO`; en otros estados se omiten. | F-03 §8 |
| RN-03 | No hay exportación ni copia masiva de datos del destinatario. | F-03 §8 |
| RN-04 | Un despacho asignado a otro repartidor responde `403`. | F-03 CA-10 |
| RN-05 | Un código inexistente responde `404` sin datos parciales. | F-03 CA-11 |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| F-02 Programación y Asignación | Destinatario, dirección, teléfono y fecha programada | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| F-02 Programación y Asignación | Proyección de destinatario, teléfono, dirección y referencia | Contrato de API; Gestión es la fuente canónica |

## 6. Criterios de aceptación

### CA-01. Detalle exitoso

- **DADO** un despacho asignado al repartidor en `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** abre su detalle.
- **ENTONCES** ve dirección, referencia, destinatario, teléfono con llamada directa, intento actual sobre el máximo configurado, fecha programada y estado.

### CA-02. Despacho de otro repartidor

- **DADO** un despacho asignado a otro repartidor.
- **CUANDO** se solicita su detalle.
- **ENTONCES** el backend responde `403 Forbidden`.

### CA-03. Despacho inexistente

- **DADO** un código que no corresponde a ningún despacho.
- **CUANDO** se solicita su detalle.
- **ENTONCES** el backend responde `404 Not Found` sin datos parciales.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: consulta de solo lectura; aplica RN-02 en la respuesta, no solo en la interfaz.
- Pendientes: [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación

| Criterio | Tipo de comprobación | Datos o escenario |
|---|---|---|
| CA-01 | Integración y UI | Despachos propios en `ASIGNADO`, `EN_CAMINO` y `ENTREGADO` |
| CA-02 | Seguridad | Despacho de otro repartidor |
| CA-03 | Integración | Código inexistente |

Tareas en [tasks.md](./tasks.md); resultados en [evidence.md](./evidence.md).

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-03, CA-09 a CA-11 y sección 8.
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
3. Wireframe del detalle del despacho.
