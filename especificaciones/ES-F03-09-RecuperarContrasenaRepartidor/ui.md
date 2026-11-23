# UI de ES-F03-09: Recuperación de contraseña del repartidor

**Responsable:** Max Rojas

**Estado:** Borrador.

**Aplicabilidad:** Modifica la pantalla de acceso y crea la pantalla «Recuperar contraseña» de la web responsive del repartidor.

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Usuario y permisos: repartidor sin sesión; no requiere permisos.
- Contexto de uso: campo, desde el celular, normalmente antes de iniciar la jornada.
- Objetivo visible: pedir un enlace para crear una contraseña nueva.
- Acceso y navegación: desde `/repartidor/acceso` mediante «¿Olvidaste tu contraseña?» hacia `/repartidor/recuperar-contrasena`; «Volver al ingreso» regresa al acceso.

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| Diseño visual compartido | [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | Tokens, tipografía y estados de formulario |
| Diseño de la funcionalidad | [f-03.md](../../disenio/funcionalidades/f-03.md), pantalla de acceso | Composición centrada y botón de ancho completo |
| Componentes React compartidos | `FormularioAcceso`, propiedad opcional `recuperacion` | Enlace deshabilitado o habilitado bajo «Ingresar» |

## 3. Pantallas e interacción

### UI-01. Enlace en la pantalla de acceso

- Composición: bajo el botón «Ingresar», un botón secundario de texto «¿Olvidaste tu contraseña?».
- Opción sin activar: el botón se muestra deshabilitado y debajo aparece «La recuperación de contraseña estará disponible próximamente.», asociado al botón como descripción accesible.
- Opción activada: el botón está habilitado y abre UI-02. Se deshabilita mientras se procesa un ingreso.
- El enlace no aparece durante la verificación del código OTP.

### UI-02. Pantalla «Recuperar contraseña»

- Composición: título «Recuperar contraseña», texto «Escribe el correo de tu cuenta. Te enviaremos un enlace para crear una nueva contraseña.», campo «Correo electrónico», botón principal «Enviar enlace» y botón secundario «Volver al ingreso».
- Acción principal: «Enviar enlace», habilitado salvo durante el envío.
- Tras el envío: se reemplaza el formulario por el mensaje neutro y se mantiene «Volver al ingreso».

| Paso | Acción de la persona | Respuesta de la interfaz | Criterio funcional |
|---|---|---|---|
| 1 | Pulsa «¿Olvidaste tu contraseña?» | Abre UI-02, o nada si la opción no está activada | CA-01, CA-02 |
| 2 | Escribe su correo y pulsa «Enviar enlace» | Botón en progreso; campo bloqueado | CA-01 |
| 3 | Recibe la respuesta | Mensaje neutro o error con el correo conservado | CA-01, CA-04 a CA-06 |
| 4 | Pulsa «Volver al ingreso» | Regresa a la pantalla de acceso | — |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones disponibles | Criterio |
|---|---|---|---|
| Opción no activada | Enlace deshabilitado con aviso; la ruta directa vuelve al acceso | Ingresar normalmente | CA-02 |
| Formulario | Texto, campo y botones | Enviar, volver | CA-01 |
| Envío en curso | Botón con indicador de carga; campo bloqueado | Ninguna; clics repetidos se ignoran | RN-04 |
| Éxito | Alerta verde con el mensaje neutro | Volver al ingreso | CA-01, CA-06 |
| Error de formato | Alerta roja «Ingresa un correo electrónico válido.» | Corregir y enviar | CA-03 |
| Límite de solicitudes | Alerta roja con la espera | Volver a intentar más tarde | CA-04 |
| Seguridad no disponible | Alerta roja de reintento | Enviar de nuevo | CA-05 |
| Sesión vigente | No se muestra; redirige a «Mi Ruta» | — | CA-07 |

## 5. Formularios y mensajes

| Campo o control | Obligatorio | Validación y momento | Mensaje visible | Fuente contractual |
|---|---|---|---|---|
| Correo electrónico | Sí | Formato de correo al enviar; se recortan espacios | «Ingresa un correo electrónico válido.» | §8.6.1 |

| Resultado o error de API | Mensaje y comportamiento de UI | Recuperación |
|---|---|---|
| `202` | «Si el correo está registrado, recibirás un enlace para restablecer tu contraseña. Revisa también tu carpeta de correo no deseado.» | Volver al ingreso |
| `429 DEMASIADAS_SOLICITUDES` | «Hiciste varias solicitudes seguidas. Espera unos minutos antes de intentarlo de nuevo.» | Conserva el correo |
| Sin conexión | «No pudimos conectar con Seguridad. Revisa tu conexión e inténtalo de nuevo.» | Conserva el correo; reintentar |
| `400`, `5xx` u otra respuesta | «No pudimos enviar la solicitud. Inténtalo nuevamente en unos minutos.» | Conserva el correo; reintentar |

## 6. Accesibilidad y adaptación

- Teclado y foco: «Enviar enlace» se activa con Enter desde el campo; el foco inicial está en el campo de correo.
- Etiquetas y avisos: el campo tiene etiqueta visible; los errores usan `role="alert"` y el éxito `role="status"`; el aviso del enlace deshabilitado se anuncia como descripción.
- Percepción: los estados se comunican con texto, no solo con color.
- Responsive: tarjeta de ancho completo hasta 440 px, centrada en pantalla, igual que el acceso.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Opción sin activar; ver el acceso | Enlace deshabilitado con aviso; pulsarlo no hace nada | CA-02 |
| CUI-02 | Opción activada; pulsar el enlace | Abre «Recuperar contraseña» | CA-01 |
| CUI-03 | Opción sin activar; abrir la ruta directa | Vuelve al acceso sin llamar a Seguridad | CA-02 |
| CUI-04 | Enviar con Seguridad simulada | Mensaje neutro sin formulario | CA-01 |

- Pendientes de diseño: no hay frame de Figma para UI-02; se sigue la composición de la pantalla de acceso.
- Evidencia prevista: pruebas de interacción en JSDOM y revisión en navegador móvil.

## 8. Referencias

1. [Especificación funcional](./spec.md): criterios y reglas.
2. [Diseño de F-03](../../disenio/funcionalidades/f-03.md) y [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md).
3. [Contrato externo §8.6.1](../../integraciones/api-contract.md#861-recuperación-de-contraseña-del-repartidor-propuesta-pendiente-de-seguridad).
4. [Plan](./plan.md) y [evidencia](./evidence.md).
