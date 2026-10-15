# UI de ES-F01-03: Activar y desactivar una zona de cobertura

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión e implementación.

**Aplicabilidad:** Confirmación de desactivación de zona (Pantalla 4) en la aplicación administrativa; la acción se inicia desde el catálogo (Pantalla 1).

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Usuario y permisos: Gestor de Despacho con rol `GESTOR_DESPACHO`; sin ese rol se muestra acceso denegado sin datos de configuración.
- Contexto de uso: centro de despacho; uso principal en escritorio, con adaptación responsive.
- Objetivo visible: activar o desactivar una zona, advirtiendo el efecto sobre cotizaciones, solicitudes y despachos existentes.
- Acceso y navegación: la acción se lanza desde las filas del catálogo (ES-F01-01); «Activar» aplica directamente y «Desactivar» abre siempre la confirmación.
- Salidas: confirmada la operación, se actualiza la fila del catálogo y se notifica el resultado. Cancelar cierra sin persistir [cite: 1].

## 2. Referencias visuales y componentes

| Fuente | Secciones | Aplicación |
|---|---|---|
| [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | Modales, confirmaciones y estados | Estructura y tokens del modal de confirmación. |
| [Diseño F-01](../../disenio/funcionalidades/f-01.md) | Pantalla 4: Confirmación de Desactivación de Zona | Contenido de la advertencia. |
| [Alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md) | Modal de desactivación | Presentación y acento de advertencia. |
| [Componentes React](../../disenio/componentes-react.md) | §4.5; CR de modal, botones y avisos | Contratos de componentes y responsables propuestos. |

La advertencia de desactivación es obligatoria; no existe un atajo que desactive desde la tabla sin confirmación [cite: 1, 2].

## 3. Pantallas e interacción

### UI-01. Confirmación de Desactivación de Zona

Composición: catálogo con modal CR de confirmación sobre el fondo desenfocado → encabezado de advertencia → descripción del efecto → acciones «Cancelar» y «Desactivar». Para la activación se usa el mismo patrón de confirmación con texto de reactivación.

| Elemento | Contenido y comportamiento |
|---|---|
| Título | «Desactivar zona» o «Activar zona». |
| Advertencia | Efecto sobre cotizaciones y solicitudes nuevas; en desactivación se aclara que los despachos existentes conservan su zona. |
| Acciones | «Cancelar» cierra sin persistir; «Desactivar» / «Activar» confirma y muestra el estado de proceso. |
| Conflicto | Un `409 Conflict` explica la zona en conflicto (activación) o la versión concurrente, sin cerrar el contexto. |

| Paso | Acción de la persona | Respuesta de la interfaz | Criterio funcional |
|---|---|---|---|
| 1 | Elegir «Desactivar» en una fila | Abrir la confirmación con la advertencia | RN-09, CA-03 |
| 2 | Elegir «Activar» en una fila inactiva | Confirmar y enviar | CA-01 |
| 3 | Confirmar | Enviar y mostrar el estado de proceso | CA-01, CA-03 |
| 4 | Recibir un conflicto | Explicar el motivo sin cerrar el contexto | CA-02, CA-05 |
| 5 | Recibir un rechazo de permisos | Cerrar y retirar datos | CA-06 |

La repetición de la misma operación devuelve el estado vigente sin cambio visible nuevo ni auditoría duplicada.

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones disponibles | Criterio |
|---|---|---|---|
| Confirmación | Modal con la advertencia del efecto | Cancelar o confirmar | CA-03 |
| Procesando | Confirmación deshabilitada con estado de proceso | Esperar | CA-01, CA-03 |
| Éxito | Notificación y fila actualizada | Volver al catálogo | CA-01, CA-03 |
| Sin cambio | Notificación de que la zona ya está en ese estado | Cerrar | CA-04 |
| Conflicto de cobertura o versión | Explicación de la zona en conflicto o de la versión | Cerrar o revisar | CA-02, CA-05 |
| Error de red | Mensaje comprensible sin detalle técnico | «Reintentar» | CA-01 |
| Sin permisos | Acceso denegado sin datos de la zona | Navegación permitida por la aplicación | CA-06 |

## 5. Formularios y mensajes

No es un formulario de campos; es una confirmación con un único parámetro (el estado solicitado), cuyo nombre definitivo proviene del contrato central y se registra en los pendientes del plan [cite: 3].

| Control | Obligatorio | Validación y momento | Mensaje visible | Fuente contractual |
|---|---|---|---|---|
| Confirmación de estado | Sí | El sistema revalida el estado y la versión al enviar | Efecto sobre cotizaciones y despachos | Contrato §9.1 |

| Resultado o error de API | Mensaje y comportamiento de UI | Recuperación |
|---|---|---|
| `409` | Explicar el conflicto (solapamiento o versión) | Cerrar o revisar el catálogo |
| `401` / `403` | Acceso denegado sin datos | Navegación permitida |
| Error de red o `5xx` | Mensaje comprensible con reintento | «Reintentar» |

## 6. Accesibilidad y adaptación

- Teclado y foco: abrir el modal moviendo el foco al título; mantenerlo dentro del modal y devolverlo al elemento que lo abrió al cerrar.
- Etiquetas y avisos: anunciar el título y la advertencia; las notificaciones de resultado y los errores se anuncian sin repetición.
- Percepción: la advertencia no depende solo del color; se expresa en texto.
- Responsive: el modal ocupa el ancho disponible en móvil con acciones apiladas y alcanzables.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Desactivar desde la fila | Se abre siempre la confirmación con advertencia | CA-03 |
| CUI-02 | Activar una zona inactiva sin conflicto | Confirmación y fila actualizada a Activo | CA-01 |
| CUI-03 | Activar con solapamiento | Mensaje de conflicto con la zona activa en conflicto | CA-02 |
| CUI-04 | Repetir la misma operación | Aviso de sin cambio, sin notificación duplicada | CA-04 |
| CUI-05 | Enviar dos cambios concurrentes | Segundo intento informa de versión concurrente | CA-05 |
| CUI-06 | Recibir `403` tras abrir la confirmación | Se cierra y se retiran los datos | CA-06 |
| CUI-07 | Recorrer la confirmación con teclado en escritorio y móvil | Foco contenido en el modal, acciones alcanzables y bien presentadas en móvil | CA-01 a CA-06 |

- Pendientes de diseño: nombre del parámetro de estado y formato del `409` (DT-01 del plan).
- Evidencia prevista: pruebas de interacción, revisión con teclado y capturas de los estados aplicables.

## 8. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-06.
2. [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [guía F-01](../../disenio/funcionalidades/f-01.md); [componentes React](../../disenio/componentes-react.md).
3. [Contrato de API](../../integraciones/api-contract.md), §§3.3, 9.1 y 14; [modelo de datos](../../arquitectura/modelo-datos.md).
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
