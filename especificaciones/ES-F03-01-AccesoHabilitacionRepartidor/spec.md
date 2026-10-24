# ES-F03-01: Acceso y habilitación operativa del repartidor

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md)

**Responsable:** Max Rojas

**Estado:** Borrador

**Actor principal:** Repartidor

**UI:** Aplica; pantalla de acceso y entrada a «Mi Ruta» de la web responsive del repartidor.

## 1. Contexto y objetivo

Permitir el ingreso a la vista de campo solo a usuarios cuyo `sub` esté vinculado a un perfil local activo de F-05, y determinar si ese repartidor puede ejecutar cambios de estado (en turno) o solo consultar (fuera de turno). No se requiere un rol global `REPARTIDOR`. Así ningún despacho es operado por alguien no autorizado y solo el personal en turno registra transiciones. Concreta RF-01 y la sección 8 (Seguridad) de F-03.

## 2. Alcance

- Incluye: validación del JWT, resolución del repartidor desde el token, consulta de su estado operativo y asignación diaria, y habilitación del modo operativo o de solo lectura.
- Fuera de alcance: emisión de credenciales, gestión de contraseñas y del token (Seguridad y Usuarios); registro de repartidores, asignación diaria y cambios de estado operativo (F-05); contenido de «Mi Ruta» y ejecución de las transiciones (otras especificaciones de F-03).

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor desde su celular, con JWT humano `tipo=acceso` emitido por Seguridad y Usuarios y un perfil local activo y vinculado por `sub`.
- Precondiciones: el usuario del token está vinculado a un repartidor registrado y activo en F-05; existe conexión activa.
- Condición de habilitación operativa: asignación diaria activa y estado operativo `DISPONIBLE`, `EN_RUTA` o `SATURADO`.
- Resultado exitoso: contexto del repartidor (identificador resuelto, estado operativo, habilitación para transiciones) y vista «Mi Ruta» en modo operativo o de solo lectura.
- Resultado ante rechazo: `401` o `403` sin información de despachos.

## 4. Flujo principal y alternativas

1. El repartidor abre la vista web y se autentica.
2. El backend valida el JWT y resuelve el perfil local activo vinculado a su `sub`.
3. El backend resuelve en F-05 el repartidor vinculado al usuario del token.
4. El backend consulta en F-05 su estado operativo y asignación diaria.
5. El sistema muestra «Mi Ruta» con las acciones de cambio de estado habilitadas.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Credencial inválida | Sin token o token vencido | `401 Unauthorized`; sin datos de despachos | CA-02 |
| Acceso no autorizado | Usuario no vinculado a un perfil local activo | `403 Forbidden`; la pantalla indica el motivo | CA-03 |
| Fuera de turno | Estado operativo `FUERA_DE_TURNO` | Solo consulta de ruta y resumen del día; toda transición recibe `409 Conflict` | CA-04 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | El repartidor se resuelve siempre desde el token; el backend ignora identificadores enviados por el cliente. | F-03 §8 |
| RN-02 | Sin token o con token vencido se responde `401` sin exponer información de despachos. | F-03 CA-02 |
| RN-03 | Un usuario sin perfil local activo y vinculado se responde `403`; el backend no exige un rol global `REPARTIDOR`. | F-03 CA-03 y contrato de API |
| RN-04 | Las transiciones solo se habilitan con asignación diaria activa y estado `DISPONIBLE`, `EN_RUTA` o `SATURADO`. | F-03 RF-01 |
| RN-05 | En `FUERA_DE_TURNO` se permite consultar ruta y resumen; toda transición se rechaza con `409` indicando turno inactivo. | F-03 CA-04 |
| RN-06 | La interfaz oculta o deshabilita lo no permitido, pero la validación definitiva ocurre siempre en el backend. | F-03 §8 |

| Operación o dependencia | Uso | Contrato o fuente |
|---|---|---|
| Seguridad y Usuarios | Emisión y validación del JWT humano; la identidad de aplicación se resuelve por `sub` | Contrato de API y F-05 |
| F-05 Monitoreo de Flota | Vínculo usuario–repartidor, estado operativo y asignación diaria | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| Rutas y códigos de respuesta | Contexto del repartidor y rechazo de transiciones | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |

## 6. Criterios de aceptación

### CA-01. Acceso exitoso

- **DADO** un repartidor vinculado, con asignación diaria activa y estado operativo `DISPONIBLE`.
- **CUANDO** se autentica desde su celular.
- **ENTONCES** el sistema muestra «Mi Ruta» y habilita las acciones de cambio de estado.

### CA-02. Credencial ausente o expirada

- **DADO** una solicitud sin token o con token vencido.
- **CUANDO** se invoca cualquier recurso de la funcionalidad.
- **ENTONCES** el backend responde `401 Unauthorized` y no expone información de despachos.

### CA-03. Rol distinto o usuario no vinculado

- **DADO** un token humano válido cuyo usuario no está vinculado a un perfil local activo en F-05.
- **CUANDO** se invocan los recursos de operación de campo.
- **ENTONCES** el backend responde `403 Forbidden`.

### CA-04. Repartidor fuera de turno

- **DADO** un repartidor activo con estado operativo `FUERA_DE_TURNO` en F-05.
- **CUANDO** accede a la aplicación.
- **ENTONCES** puede consultar su ruta y su resumen del día, y toda transición se rechaza con `409 Conflict` informando que su turno no está activo.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: autorización y resolución del contexto del repartidor; no modifica datos de F-05.
- No funcionales: uso móvil; ninguna respuesta de rechazo incluye datos de despachos.
- Pendientes: registrados en [plan.md, sección 7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación

| Criterio | Tipo de comprobación | Datos o escenario |
|---|---|---|
| CA-01 | Integración y UI | Repartidor vinculado, asignación activa, estado `DISPONIBLE` |
| CA-02 | Seguridad | Solicitud sin token y con token vencido |
| CA-03 | Seguridad | Token humano sin vínculo o con perfil local inactivo |
| CA-04 | Integración y UI | Repartidor `FUERA_DE_TURNO` que intenta una transición |

Tareas en [tasks.md](./tasks.md); resultados en [evidence.md](./evidence.md).

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-01, CA-01 a CA-04 y sección 8.
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
3. Wireframe de la pantalla de acceso de F-03.
