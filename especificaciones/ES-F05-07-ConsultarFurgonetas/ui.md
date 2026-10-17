# UI de ES-F05-07: Consultar furgonetas

**Responsable:** Rhamses.

**Estado:** Borrador; revisión visual y aceptación por criterio pendientes.

**Aplicabilidad:** Interfaz administrativa `/furgonetas`, acción «Consultar furgonetas».

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Usuario: Gestor de Despacho autenticado, con autorización según [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas).
- Contexto: aplicación administrativa; uso con teclado, puntero y pantalla reducida.
- Objetivo visible: Consultar y filtrar el catálogo paginado de furgonetas.
- Navegación: desde el menú administrativo a `/furgonetas`; regresar al catálogo al terminar o cancelar una operación modal.

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| Diseño compartido | [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | Tokens, tipografía, contraste, estructura y adaptación |
| Diseño F-05 | [Diseño funcional](../../disenio/funcionalidades/f-05.md) y [alta fidelidad](../../disenio/SystemDesign/f-05-alta-fidelidad.md) | Catálogo y flujo administrativo de recursos |
| Componentes React | [Especificación compartida](../../disenio/componentes-react.md) | CR-01/02 acciones y campos; CR-03 estructura; CR-05 encabezado; CR-06 filtros; CR-07 tabla; CR-08 estados; CR-09 etiquetas; CR-12 confirmación; CR-15 notificaciones |

Componer solo los componentes que necesita este flujo. Las definiciones y variantes compartidas pertenecen al documento de componentes [cite: 2].

## 3. Pantallas e interacción

### UI-01. Consultar furgonetas

- Composición: encabezado y contexto del catálogo; filtros, tabla y paginación.
- Datos visibles: los necesarios para identificar al recurso y revisar sus estados y los filtros aplicados.
- Acción principal: «Consultar furgonetas»; habilitarla solo con contexto válido y filtros admitidos.
- Acción secundaria: limpiar filtros y actualizar la consulta.
- Confirmación: revisar los datos antes de enviar; no agregar un segundo diálogo de confirmación sin necesidad funcional.

| Paso | Acción de la persona | Respuesta de la interfaz | Criterios |
|---|---|---|---|
| 1 | Iniciar «Consultar furgonetas» | Presentar el contexto y controles del comportamiento | CA-01 |
| 2 | Seleccionar filtros y página | Combinar estado y búsqueda, limpiar filtros y cambiar de página; conservar separados vacío, error y resultados anteriores sin confirmar. | CA-01, CA-02, CA-03, CA-04, CA-05 |
| 3 | Recibir el resultado | Mostrar el resultado confirmado y mantener diferenciados rechazo e incertidumbre | CA-01, CA-02, CA-03, CA-04, CA-05 |

## 4. Estados de la interfaz

| Estado | Presentación | Acciones disponibles | Criterios |
|---|---|---|---|
| Carga | Indicador de consulta o precarga sin aparentar resultados confirmados | Volver o esperar; bloquear acciones sobre datos sin confirmar | CA-01 |
| Con datos | Contexto y recurso o página confirmados | Acciones autorizadas para el comportamiento | CA-01 |
| Vacío o sin resultados | Distinguir catálogo vacío de ausencia de coincidencias | Limpiar filtros o iniciar un alta cuando esté autorizado | CA-04 |
| Procesamiento | Consulta pendiente; evitar acciones sobre resultados desfasados | Evitar solicitudes repetidas accidentales | CA-01 |
| Éxito | Confirmación y datos consultados nuevamente | Volver a operar con la información confirmada | CA-01 |
| Rechazo o dependencia no disponible | Mensaje comprensible, sin SQL, tokens ni detalles internos | Corregir si procede; actualizar el catálogo si el resultado es incierto | CA-01, CA-02, CA-03, CA-04, CA-05 |
| Sin permisos | Estado de acceso denegado; retirar datos protegidos | Regresar a una vista permitida o reautenticarse | Autorización de spec.md §3 |

## 5. Formularios y mensajes

| Campo o control | Obligatorio | Validación e interacción | Fuente |
|---|---|---|---|
| Página y tamaño | Sí | Paginación válida según el contrato. | [spec.md §5](./spec.md#5-reglas-datos-e-integraciones) y [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) |
| Estado | No | Opciones del catálogo, conservando la distinción con el valor persistido. | [spec.md §5](./spec.md#5-reglas-datos-e-integraciones) y [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) |
| Búsqueda por placa | No | Coincidencia de texto; no interpretar el valor como SQL. | [spec.md §5](./spec.md#5-reglas-datos-e-integraciones) y [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) |

| Resultado | Mensaje y comportamiento | Recuperación |
|---|---|---|
| Confirmado | Aviso de resultado y actualización de la consulta | Continuar desde el catálogo confirmado |
| Validación | Asociar el error a un campo conocido; conservar entradas corregibles | Corregir y volver a enviar cuando sea válido |
| Conflicto o recurso inexistente | Explicar el conflicto permitido por el contrato; conservar el estado conocido | Actualizar la consulta y revisar el recurso |
| Sin autenticación o permiso | Retirar contenido protegido y mostrar estado autorizado | Reautenticación o regreso |
| Respuesta incierta | Informar que no puede confirmarse la operación | Consultar el estado actual antes de una nueva mutación |

Los mensajes y los controles se revisan contra los criterios conservados; no se redefine aquí el payload ni se infiere éxito de una respuesta incompleta.

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
| CUI-02 | Combinar o limpiar filtros | Solicitar el conjunto correcto y reiniciar la página cuando corresponda | CA-01, CA-02, CA-03, CA-04, CA-05 |
| CUI-03 | Repetir la acción durante el procesamiento | Evitar solicitudes accidentales duplicadas y uso de datos sin confirmar | CA-01 |
| CUI-04 | Recibir los rechazos y alternativas de la especificación | Mostrar mensajes y recuperación coherentes sin afirmar éxito | CA-01, CA-02, CA-03, CA-04, CA-05 |
| CUI-05 | Completar la operación o consulta | Mostrar el resultado confirmado y actualizar la información visible | CA-01 |
| CUI-06 | Recorrer con teclado y en pantalla reducida | Mantener foco, etiquetas y acceso a todas las acciones disponibles | CA-01; requisitos de accesibilidad §6 |

- Pendiente: Alineado con Operación §4.1: registro local, asociación manual de UUID y estados `PENDIENTE`/`VINCULADO`; sin creación automática de cuentas ni rol global de repartidor. Los efectos integrados en F-03/F-06 siguen pendientes.
- Evidencia prevista: pruebas de interacción, revisión con teclado y capturas de estados identificadas en [evidence.md](./evidence.md).

## 8. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01, CA-02, CA-03, CA-04, CA-05 [cite: 1].
2. [Componentes compartidos](../../disenio/componentes-react.md), [diseño transversal](../../disenio/SYSTEM-DESIGN.md) y [diseño F-05](../../disenio/funcionalidades/f-05.md) [cite: 2].
3. [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
