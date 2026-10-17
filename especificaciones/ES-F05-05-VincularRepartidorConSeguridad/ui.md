# UI de ES-F05-05: Vincular repartidor con Seguridad y Usuarios

**Responsable:** Rhamses.

**Estado:** Borrador; revisión visual y aceptación por criterio pendientes.

**Aplicabilidad:** Interfaz administrativa `/repartidores`, acción «Vincular cuenta / reintentar según acuerdo pendiente».

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Usuario: Gestor de Despacho autenticado, con autorización según [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas).
- Contexto: aplicación administrativa; uso con teclado, puntero y pantalla reducida.
- Objetivo visible: Documentar el vínculo entre perfil local y cuenta de Seguridad, pendiente de conciliar el flujo heredado.
- Navegación: desde el menú administrativo a `/repartidores`; regresar al catálogo al terminar o cancelar una operación modal.

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| Diseño compartido | [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | Tokens, tipografía, contraste, estructura y adaptación |
| Diseño F-05 | [Diseño funcional](../../disenio/funcionalidades/f-05.md) y [alta fidelidad](../../disenio/SystemDesign/f-05-alta-fidelidad.md) | Catálogo y flujo administrativo de recursos |
| Componentes React | [Especificación compartida](../../disenio/componentes-react.md) | CR-01/02 acciones y campos; CR-03 estructura; CR-05 encabezado; CR-06 filtros; CR-07 tabla; CR-08 estados; CR-09 etiquetas; CR-12 confirmación; CR-15 notificaciones |

Componer solo los componentes que necesita este flujo. Las definiciones y variantes compartidas pertenecen al documento de componentes [cite: 2].

## 3. Pantallas e interacción

### UI-01. Vincular cuenta / reintentar según acuerdo pendiente

- Composición: encabezado y contexto del catálogo; acción por fila o de alta, formulario o confirmación, y retorno al catálogo.
- Datos visibles: los necesarios para identificar al recurso y revisar los valores o el efecto de la operación.
- Acción principal: «Vincular cuenta / reintentar según acuerdo pendiente»; habilitarla solo con contexto válido y sin otro envío en curso.
- Acción secundaria: cancelar y volver al catálogo; la cancelación no envía una mutación.
- Confirmación: revisar los datos antes de enviar; no agregar un segundo diálogo de confirmación sin necesidad funcional.

| Paso | Acción de la persona | Respuesta de la interfaz | Criterios |
|---|---|---|---|
| 1 | Iniciar «Vincular cuenta / reintentar según acuerdo pendiente» | Presentar el contexto y controles del comportamiento | CA-01 |
| 2 | Completar, revisar o confirmar los datos | Presentar el vínculo del perfil y la acción contractual vigente; el formulario manual existente se identifica expresamente como distinto del reintento automático de la fuente. | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07 |
| 3 | Recibir el resultado | Mostrar el resultado confirmado y mantener diferenciados rechazo e incertidumbre | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07 |

## 4. Estados de la interfaz

| Estado | Presentación | Acciones disponibles | Criterios |
|---|---|---|---|
| Carga | Indicador de consulta o precarga sin aparentar resultados confirmados | Volver o esperar; bloquear acciones sobre datos sin confirmar | CA-01 |
| Con datos | Contexto y recurso o página confirmados | Acciones autorizadas para el comportamiento | CA-01 |
| Vacío o sin resultados | Informar si desaparece el recurso; un formulario de alta vacío es un estado inicial, no un resultado del catálogo | Volver al listado o completar datos de alta | CA-01 |
| Procesamiento | Envío en curso y controles de confirmación bloqueados | Evitar solicitudes repetidas accidentales | CA-01 |
| Éxito | Confirmación y datos consultados nuevamente | Volver a operar con la información confirmada | CA-01 |
| Rechazo o dependencia no disponible | Mensaje comprensible, sin SQL, tokens ni detalles internos | Corregir si procede; actualizar el catálogo si el resultado es incierto | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07 |
| Sin permisos | Estado de acceso denegado; retirar datos protegidos | Regresar a una vista permitida o reautenticarse | Autorización de spec.md §3 |

## 5. Formularios y mensajes

| Campo o control | Obligatorio | Validación e interacción | Fuente |
|---|---|---|---|
| Repartidor y estado del vínculo | Solo lectura | Conservar el contexto de la cuenta asociada. | [spec.md §5](./spec.md#5-reglas-datos-e-integraciones) y [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) |
| Identificador comunicado por Seguridad | Según contrato vigente | La UI existente usa un UUID; no solicitar contraseña ni tokens. | [spec.md §5](./spec.md#5-reglas-datos-e-integraciones) y [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) |
| Acción de reintento | Pendiente de conciliación | No habilitar un flujo automático no acordado. | [spec.md §5](./spec.md#5-reglas-datos-e-integraciones) y [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) |

| Resultado | Mensaje y comportamiento | Recuperación |
|---|---|---|
| Confirmado | Aviso de resultado y actualización de la consulta | Continuar desde el catálogo confirmado |
| Validación | Asociar el error a un campo conocido; conservar entradas corregibles | Corregir y volver a enviar cuando sea válido |
| Conflicto o recurso inexistente | Explicar el conflicto permitido por el contrato; conservar el estado conocido | Actualizar la consulta y revisar el recurso |
| Sin autenticación o permiso | Retirar contenido protegido y mostrar estado autorizado | Reautenticación o regreso |
| Respuesta incierta | Informar que no puede confirmarse la operación | Consultar el estado actual antes de una nueva mutación |

El formulario manual existente recibe el identificador comunicado por Seguridad. No demuestra el flujo automático, los estados de activación ni los reintentos de los criterios heredados; P-01 debe resolverse antes de aceptar ese recorrido.

## 6. Accesibilidad y adaptación

- Teclado y foco: mantener orden lógico; en un modal, foco inicial útil, contención mientras esté abierto y retorno al disparador al cerrar.
- Etiquetas: todos los campos y acciones tienen nombre accesible; asociar errores mediante descripción y anunciar los resultados.
- Percepción: acompañar estados con texto, sin depender solo del color; aplicar contraste y tokens del diseño compartido.
- Adaptación: filtros y acciones se reorganizan sin perder etiquetas; permitir desplazamiento de la tabla sin provocar desbordamiento de toda la pantalla.
- Evitar registrar credenciales o datos personales reales en capturas de evidencia.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Abrir el flujo con permiso | Mostrar contexto y controles identificables | CA-01 |
| CUI-02 | Introducir datos inválidos o intentar cambiar un campo de solo lectura | Validar sin modificar campos protegidos ni perder datos corregibles | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07 |
| CUI-03 | Repetir la acción durante el procesamiento | Evitar solicitudes accidentales duplicadas y uso de datos sin confirmar | CA-01 |
| CUI-04 | Recibir los rechazos y alternativas de la especificación | Mostrar mensajes y recuperación coherentes sin afirmar éxito | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07 |
| CUI-05 | Completar la operación o consulta | Mostrar el resultado confirmado y actualizar la información visible | CA-01 |
| CUI-06 | Recorrer con teclado y en pantalla reducida | Mantener foco, etiquetas y acceso a todas las acciones disponibles | CA-01; requisitos de accesibilidad §6 |

- Pendiente: Los siete criterios heredados describen creación automática, activación y reintento; Seguridad §8.4 y Operación §4.1 acuerdan asociar el usuario creado previamente por ADMIN_SISTEMA. No se reemplazan esos criterios durante una migración de estructura: requieren revisión de Rhamses con Seguridad y Arquitectura antes de aceptar el comportamiento.
- Evidencia prevista: pruebas de interacción, revisión con teclado y capturas de estados identificadas en [evidence.md](./evidence.md).

## 8. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07 [cite: 1].
2. [Componentes compartidos](../../disenio/componentes-react.md), [diseño transversal](../../disenio/SYSTEM-DESIGN.md) y [diseño F-05](../../disenio/funcionalidades/f-05.md) [cite: 2].
3. [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
