# UI de ES-F02-02: Generación de despachos de prueba para simulación

**Responsable:** Tarqui.

**Estado:** Especificación de UI preparada el 16/10/2026; implementación pendiente.

**Aplicabilidad:** Botón de acción y modal de simulación en la cabecera del Panel de Programación (`/programacion`).

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- **Usuario:** Gestor de Despacho (`GESTOR_DESPACHO`) o perfil técnico en entorno de desarrollo/pruebas.
- **Contexto:** Vista principal de Programación y Asignación de Despachos. El usuario necesita alimentar la cola de trabajo de forma rápida sin cambiar de aplicación ni depender de la integración con Ventas.
- **Objetivo:** Disparar la creación de un despacho simulado con un solo clic (valores por omisión) o mediante modal rápido (parámetros personalizados) y ver el resultado reflejado de inmediato en la tabla.
- **Componentes React asociados:** Mantine `Button` (patrón CR-01), Mantine `Modal` / `Drawer` (CR-12), `NotificacionOperacion` (CR-15) y `BadgeEstado` (CR-09).

## 2. Referencias visuales

- [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md): sección 21 (diseño administrativo).
- [Diseño F-02](../../disenio/funcionalidades/f-02.md): Pantalla 1 (cabecera con botón "Generar pedido de prueba").
- [Componentes React](../../disenio/componentes-react.md): CR-01 (AccionesUi), CR-12 (ModalConfirmacion), CR-15 (NotificacionOperacion).

## 3. Pantallas e interacción

### UI-01. Disparador en cabecera

- En la esquina superior derecha del Panel de Programación, junto al título de la página, se ubica el botón secundario tipo `outline` con etiqueta "Generar pedido de prueba" e ícono `IconFlask` o `IconPackagePlus`.
- Al hacer clic simple: envía la petición con `{}` para generación instantánea automática con valores por omisión.
- Al hacer clic en la flecha adyacente (botón dividido / dropdown) o doble clic: abre un modal opcional "Generar despacho de prueba personalizado" que permite seleccionar zona y valores de peso/volumen.

### UI-02. Modal de simulación personalizada (opcional)

- Campos:
  - Selector de Zona (desplegable con zonas activas de F-01).
  - Campo numérico "Peso (kg)" (valor por omisión: 5.0).
  - Campo numérico "Volumen (m³)" (valor por omisión: 0.025).
  - Campo de texto "Observaciones" (opcional).
- Acciones:
  - "Cancelar": cierra el modal sin mutaciones.
  - "Generar": ejecuta la mutación y deshabilita el botón mostrando spinner mientras procesa.

### UI-03. Respuesta e integración reactiva

- Mientras la petición está en vuelo: el botón muestra spinner y queda deshabilitado (prevención de doble envío, CCR-01-01).
- Éxito (HTTP 201):
  - Se muestra notificación toast flotante (CR-15): *"Despacho de prueba DSP-SIM-XXXXX generado exitosamente"*.
  - La tabla de la cola de pendientes se invalida y actualiza reactivamente (`queryClient.invalidateQueries(['despachos-pendientes'])`).
  - La fila recién creada aparece al tope o según el orden de fecha y se resalta con animación suave y distintivo temporal "Nuevo".
  - La fila muestra permanentemente el badge neutral punteado "Simulado" (CR-09).
- Error (HTTP 400 / 422 / 500):
  - Toast de error con el mensaje descriptivo retornado por el backend.

## 4. Criterios de aceptación de interfaz (CUI)

### CUI-01. Acción rápida accesible en cabecera
- **DADO** un usuario con rol `GESTOR_DESPACHO` en la vista de programación.
- **CUANDO** visualiza la cabecera.
- **ENTONCES** el botón "Generar pedido de prueba" está visible, con foco accesible por teclado (`Tab`), contraste adecuado y nombre accesible para lectores de pantalla.

### CUI-02. Deshabilitación durante el procesamiento
- **DADO** que el usuario pulsó el botón de generar prueba.
- **CUANDO** la solicitud HTTP está en tránsito.
- **ENTONCES** el control muestra estado `loading`, bloquea clics sucesivos y no envía peticiones duplicadas.

### CUI-03. Feedback de éxito y visualización en tabla
- **DADO** que el backend respondió `201 Created`.
- **CUANDO** la interfaz procesa la respuesta.
- **ENTONCES** se despliega toast de éxito de Mantine Notifications, la tabla de pendientes se actualiza y la fila creada muestra el badge "Simulado".

### CUI-04. Manejo de error en la UI
- **DADO** un fallo de red o rechazo de parámetros.
- **CUANDO** la petición falla.
- **ENTONCES** se presenta un banner o toast de alerta informando el error sin alterar la tabla ni descolocar los filtros actuales.
