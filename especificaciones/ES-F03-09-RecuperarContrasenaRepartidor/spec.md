# ES-F03-09: Recuperación de contraseña del repartidor

**Funcionalidad padre:** [F-03 — Web Responsive del Repartidor y Evidencia de Entrega](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-01 y sección 8 (Seguridad).

**Responsable:** Max Rojas

**Estado:** Borrador; operación de Seguridad propuesta y pendiente de confirmación.

**Actor principal:** Repartidor sin sesión que olvidó su contraseña.

**UI:** Aplica; enlace en la pantalla de acceso y pantalla «Recuperar contraseña» de la web responsive del repartidor.

**Servicio propietario:** Seguridad y Usuarios (G7) ejecuta la recuperación. Despacho solo aporta la interfaz en su app; ningún microservicio de Despacho participa.

## 1. Contexto y objetivo

Seguridad y Usuarios crea las cuentas de los repartidores, con su correo y contraseña ([contrato externo §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor)). Si un repartidor olvida su contraseña, no puede ingresar a «Mi Ruta» ni operar su jornada. Se solicita que la app le permita pedir por sí mismo la recuperación: escribe su correo y Seguridad le envía un enlace para crear una contraseña nueva en una página propia de Seguridad [cite: 1, 2].

El kit G7 vigente no incluye esta operación. Despacho la propone en [§8.6.1](../../integraciones/api-contract.md#861-recuperación-de-contraseña-del-repartidor-propuesta-pendiente-de-seguridad). Mientras Seguridad no la confirme, la opción se muestra **deshabilitada** y no realiza llamadas [cite: 2].

## 2. Alcance

- Incluye: enlace «¿Olvidaste tu contraseña?» en la pantalla de acceso de la app del repartidor; pantalla para ingresar el correo; envío de la solicitud a Seguridad; mensaje neutro de confirmación; errores de formato, límite de solicitudes y falta de servicio; activación por configuración cuando Seguridad confirme la operación.
- Fuera de alcance: crear cuentas o contraseñas, enviar el correo, generar o validar el enlace, la página donde se escribe la nueva contraseña y la política de contraseñas (Seguridad y Usuarios); recuperación para el Gestor de Despacho en la app administrativa, que usa MFA y no se solicitó; cambiar la contraseña con la sesión iniciada; desbloquear cuentas.

## 3. Actor, precondiciones y resultados

- Actor y autorización: repartidor sin sesión. La operación es pública, no exige JWT y no depende de su perfil local en F-05.
- Precondiciones: Seguridad publicó la operación de §8.6.1 en el ambiente y la app tiene activada la opción (`VITE_RECUPERACION_CONTRASENA=true`).
- Disparador: el repartidor pulsa «¿Olvidaste tu contraseña?» en la pantalla de acceso.
- Resultado exitoso: la app muestra un mensaje neutro. Si el correo pertenece a una cuenta habilitada, Seguridad le envía un enlace de restablecimiento.
- Resultado ante rechazo: la app conserva el correo escrito, informa el motivo y permite reintentar. Ninguna sesión cambia.

## 4. Flujo principal y alternativas

1. En la pantalla de acceso, el repartidor pulsa «¿Olvidaste tu contraseña?».
2. La app abre «Recuperar contraseña» y le pide su correo.
3. La app valida el formato y envía la solicitud a Seguridad.
4. Seguridad responde `202` y, si la cuenta existe y está habilitada, envía el enlace.
5. La app muestra el mensaje neutro y la opción de volver al ingreso.
6. El repartidor abre el enlace desde su correo, crea la contraseña en la página de Seguridad y vuelve a la app para ingresar.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Operación no publicada | La opción no está activada | El enlace aparece deshabilitado con el aviso «estará disponible próximamente»; no abre la pantalla ni llama a Seguridad. La ruta directa vuelve al acceso | CA-02 |
| Correo inválido | Vacío o sin formato de correo | Mensaje de corrección; no se envía la solicitud | CA-03 |
| Límite de solicitudes | Seguridad responde `429 DEMASIADAS_SOLICITUDES` | Informa que debe esperar; conserva el correo | CA-04 |
| Seguridad no disponible | Sin conexión, error `5xx` o respuesta no esperada | Mensaje de reintento; conserva el correo y habilita reenviar | CA-05 |
| Correo no registrado | Seguridad no encuentra la cuenta | Mismo mensaje neutro que el éxito | CA-06 |
| Sesión vigente | Ya existe una sesión en la app | La ruta lleva a «Mi Ruta» | CA-07 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Despacho nunca recibe, transporta ni almacena la contraseña ni el enlace; la app solo envía el correo. | Contrato externo §8.4 y §8.6.1 |
| RN-02 | El mensaje tras enviar es el mismo exista o no la cuenta, para no revelar qué correos están registrados. | §8.6.1 |
| RN-03 | Mientras la operación no esté confirmada, la opción se muestra deshabilitada y no se realiza ninguna llamada. | Decisión del responsable, 23/11/2026 |
| RN-04 | Un envío en curso no se repite con pulsaciones adicionales. | Convención de formularios del módulo |
| RN-05 | La recuperación no inicia sesión: tras restablecer, el repartidor ingresa con el flujo normal de §8.6. | §8.6 y §8.6.1 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `POST /api/v1/auth/recuperacion-contrasena` (Seguridad) | Solicitar el enlace de restablecimiento | [§8.6.1](../../integraciones/api-contract.md#861-recuperación-de-contraseña-del-repartidor-propuesta-pendiente-de-seguridad), propuesta |
| Gateway de Despacho | Publicar la ruta junto con las operaciones humanas, si se mantiene el proxy | [§8.6](../../integraciones/api-contract.md#86-acceso-humano-de-ambas-aplicaciones) |
| Página de restablecimiento (Seguridad) | Crear la contraseña nueva | Pendiente de Seguridad |

## 6. Criterios de aceptación

### CA-01. Solicitud enviada

- **DADO** la opción activada y un repartidor sin sesión en la pantalla de acceso.
- **CUANDO** pulsa «¿Olvidaste tu contraseña?», escribe `gerardo@despacho.pe` y pulsa «Enviar enlace».
- **ENTONCES** la app envía el correo, sin espacios al inicio o al final, a la operación de §8.6.1 y muestra el mensaje neutro, sin el formulario.

### CA-02. Opción deshabilitada mientras Seguridad no la publique

- **DADO** la opción sin activar.
- **CUANDO** el repartidor ve la pantalla de acceso, pulsa el enlace o abre `/repartidor/recuperar-contrasena`.
- **ENTONCES** el enlace aparece deshabilitado con el aviso «La recuperación de contraseña estará disponible próximamente.», no abre ninguna pantalla, la ruta vuelve al acceso y no se llama a Seguridad.

### CA-03. Correo con formato inválido

- **DADO** la pantalla «Recuperar contraseña».
- **CUANDO** el repartidor envía `gerardo`.
- **ENTONCES** la app muestra «Ingresa un correo electrónico válido.» y no envía la solicitud.

### CA-04. Límite de solicitudes

- **DADO** que Seguridad responde `429 DEMASIADAS_SOLICITUDES`.
- **CUANDO** el repartidor envía su correo.
- **ENTONCES** la app indica que debe esperar unos minutos y conserva el correo escrito.

### CA-05. Seguridad no disponible

- **DADO** que Seguridad no responde o responde con un error no previsto.
- **CUANDO** el repartidor envía su correo.
- **ENTONCES** la app muestra un mensaje de reintento, conserva el correo y vuelve a habilitar «Enviar enlace».

### CA-06. Respuesta neutra

- **DADO** un correo que no pertenece a ninguna cuenta.
- **CUANDO** el repartidor lo envía.
- **ENTONCES** ve el mismo mensaje que en CA-01 y Seguridad no envía ningún correo.

### CA-07. Repartidor con sesión vigente

- **DADO** una sesión vigente en la app.
- **CUANDO** se abre `/repartidor/recuperar-contrasena`.
- **ENTONCES** la app lleva a «Mi Ruta».

### CA-08. Restablecimiento completo con Seguridad

- **DADO** una cuenta de repartidor de prueba habilitada en Seguridad.
- **CUANDO** solicita el enlace, crea una contraseña nueva en la página de Seguridad e ingresa a la app.
- **ENTONCES** ingresa con la contraseña nueva y la anterior es rechazada con `CREDENCIALES_INVALIDAS`.

## 7. UI, backend y requisitos no funcionales

- UI: detallada en [ui.md](./ui.md).
- Backend: no aplica en Despacho. La operación pertenece a Seguridad; el Gateway solo la publica.
- Requisitos no funcionales: la app no registra el correo en logs ni en almacenamiento local; la respuesta es neutra (RN-02); uso móvil y accesible con teclado.
- Pendientes: confirmación de §8.6.1 por Seguridad y página de restablecimiento. Bloquean CA-01, CA-04 a CA-06 con el servicio real y CA-08. Ver [plan.md §7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | UI con Seguridad simulada; luego integración | Correo con espacios alrededor |
| CA-02 | UI | Opción sin activar |
| CA-03 | UI | Correo sin dominio |
| CA-04 | UI con Seguridad simulada; luego integración | Respuesta `429` |
| CA-05 | UI con Seguridad simulada | Error `503` o sin conexión |
| CA-06 | Integración con Seguridad | Correo inexistente |
| CA-07 | UI | Sesión iniciada |
| CA-08 | Manual con Seguridad real | Cuenta de prueba y buzón de correo |

- [ ] Todos los criterios aplicables cuentan con resultados comprobables en `evidence.md`.
- [ ] Los documentos, el contrato y el comportamiento implementado son consistentes.
- [ ] Seguridad confirmó la operación y la revisión del equipo está registrada.

## 9. Referencias

1. [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-01 y sección 8.
2. [Contrato externo](../../integraciones/api-contract.md), §8.4, §8.6 y §8.6.1 (propuesta del 23/11/2026).
3. [ES-F03-01](../ES-F03-01-AccesoHabilitacionRepartidor/spec.md): acceso del repartidor.
4. Archivos de esta especificación: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
