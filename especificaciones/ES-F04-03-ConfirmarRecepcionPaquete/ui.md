# UI de ES-F04-03: Confirmar la recepción del paquete

**Responsable:** Gerardo.

**Estado:** Modal implementado desde listado y detalle; pruebas con APIs simuladas y revisión local de teclado/móvil aprobadas. Integración real, ampliación al 200 % y revisión visual con Max pendientes; ver [EV-04](./evidence.md#ev-04-modal-estados-y-accesibilidad), 24/10/2026.

**Aplicabilidad:** Modal de recepción desde listado o detalle de entregas fallidas.

**Especificación funcional:** [spec.md](./spec.md), CA-01 a CA-12.

## 1. Usuario, contexto y objetivo

- Usuario: Gestor de Despacho autenticado con `GESTOR_DESPACHO`.
- Contexto: centro de despacho, con el paquete físicamente presente; escritorio, tableta o móvil.
- Objetivo: registrar el retorno individual y la condición del sello, distinguiendo recepción de liberación de capacidad.
- Entrada: `Confirmar recepción` desde [listado](../ES-F04-01-ConsultarEntregasFallidas/ui.md) o [detalle](../ES-F04-02-ConsultarDetalleIncidencia/ui.md), si la acción está habilitada.
- Navegación: modal sobre la pantalla existente; conservar filtros, página y consulta de origen. No requiere una ruta independiente ni una confirmación masiva al cerrar jornada [cite: 1].

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | §23, P3; pautas de formularios, mensajes y accesibilidad | Modal, jerarquía de acciones y estados. |
| [Diseño F-04](../../disenio/funcionalidades/f-04.md) | Pantalla 3 | Resumen y formulario de recepción. |
| [Componentes React](../../disenio/componentes-react.md) | CR-01/02/08/09/15 | Acciones, campos, estados, etiquetas y notificación. |

`ModalRecepcionPaquete` está implementado como composición local con `Modal`, `Radio.Group` y `Textarea` de Mantine, reutilizando el tema y el cliente existentes. El resultado se anuncia en la pantalla de origen. CR-12 es una confirmación genérica y no contiene este formulario; no se crea otro proveedor de notificaciones ni una biblioteca de formularios [cite: 2].

## 3. Pantallas e interacción

### UI-01. Modal de recepción

Composición: título `Confirmar recepción del paquete` → código operativo interno y resumen de incidencia, repartidor y fecha → sello Sí/No → observación opcional y contador → mensaje de error si existe → Cancelar y Confirmar recepción.

| Paso | Acción de la persona | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Abre desde una fila o detalle. | Conserva identidad/versión y obtiene contexto vigente antes de habilitar el envío; muestra carga si lo necesita. | CA-04/07/12 |
| 2 | Verifica el paquete y selecciona Sí o No. | No hay selección inicial; ambas respuestas habilitan la validación. | CA-01/02/05 |
| 3 | Escribe observación o la deja vacía. | Campo opcional; con No invita a describir el estado sin exigir texto. | CA-02/05 |
| 4 | Confirma. | Valida, bloquea un segundo envío y comunica que está registrando el retorno. | CA-01/10/12 |
| 5 | Recibe `202`. | Anuncia recepción registrada y liberación pendiente, cierra y actualiza la pantalla de origen. | CA-01/09/12 |
| 6 | Revisa el detalle. | Presenta el estado actual de liberación; no ofrece recibir de nuevo una recepción aceptada. | CA-03/09/12 |

La recepción solo requiere esta confirmación explícita; no abre otro modal de confirmación. Jornada cerrada/activa, máximo, anulación o falta de foto no añaden bloqueos si el backend permite recibir. La pantalla aporta el contexto; el Gestor verifica físicamente el paquete.

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones disponibles | Criterio |
|---|---|---|---|
| Carga o actualización de contexto | Resumen en carga y envío bloqueado. | Cancelar; reintentar lectura si falla. | CA-04/12 |
| Listo para recibir | Resumen y campos editables, sin sello inicial. | Cancelar y confirmar con datos válidos. | CA-01/02/05/11 |
| Sin incidencia, inexistente o acción no permitida | Motivo concreto, sin formulario operativo. | Cerrar y actualizar origen. | CA-04/12 |
| Envío en curso | Botón con carga y campos bloqueados. | No confirmar ni cerrar accidentalmente por Escape/fondo hasta obtener resultado o pasar a recuperación. | CA-10/12 |
| Recepción aceptada | `Paquete recibido. Liberación de capacidad pendiente`. | Modal cerrado; actualizar origen y consultar detalle. | CA-01/09/12 |
| Validación o rechazo recuperable | Error junto al campo o en un aviso; se conservan los valores. | Corregir o reintentar según el error contractual. | CA-05/08/12 |
| Conflicto | `La información cambió. Actualiza y revisa antes de confirmar.` | Actualizar; una recepción ajena se muestra sin edición. | CA-04/10/12 |
| Resultado desconocido | `No pudimos comprobar el resultado. Consulta antes de volver a confirmar.` | Consultar detalle; después, si procede, repetir exactamente la solicitud original. | CA-03/12 |
| Sin autorización | Retirada del resumen y datos protegidos. | Recuperar sesión o volver a una vista autorizada. | CA-06 |

No existe una lista vacía propia del modal: la falta de contexto es un error de acceso al recurso. Una caída de Operación después de aceptar no convierte la recepción en error. El detalle muestra pendiente, pendiente de revisión o liberada; el listado cuenta retorno físico [cite: 1, 3].

## 5. Formularios y mensajes

| Campo o control | Obligatorio | Validación y momento | Mensaje visible | Fuente |
|---|---|---|---|---|
| Resumen del paquete/incidencia | Solo lectura | Antes de habilitar; no permite editar IDs, usuario, fecha o reserva. | Código operativo interno, repartidor y fecha local. | Gestión §5.3 |
| Sello intacto, Sí/No | Sí | Al confirmar; selección explícita, `false` válido. | `Indica si el sello está intacto.` | Gestión §5.2.1 |
| Observación | No | Hasta 500 puntos de código Unicode después de recortar extremos; misma normalización en cliente/servidor. | `Máximo 500 caracteres.`; contador del texto normalizado. | Gestión §5.2.1 |
| Confirmar recepción | Acción principal | Deshabilitada sin selección, con contexto inválido o mientras envía. | `Confirmar recepción`. | CR-01; CA-05/12 |

No usar un límite nativo que cuente unidades UTF-16 como única validación; comprobar caracteres Unicode, incluyendo emojis. El campo no lleva asterisco ni se vuelve obligatorio al elegir No.

| Resultado contractual | Mensaje y comportamiento | Recuperación |
|---|---|---|
| `202` nuevo o repetido | Recepción aceptada; la respuesta original no prueba el estado actual de sincronización. | Consultar y refrescar filas, indicadores, historial y acciones. |
| `400` | Errores por campo, sin borrar lo ingresado. | Corregir y enviar solo con contexto aún válido. |
| `404` | `El despacho ya no está disponible.` | Cerrar y actualizar origen. |
| `409` | Cambio concurrente, recepción existente o solicitud incompatible; mostrar motivo comprensible. | Actualizar y revisar; nunca reemplazar IDs/versión silenciosamente. |
| `500` por inconsistencia | `No se puede registrar la recepción con estos datos. Solicita revisión.` | Conservar formulario; corregir la causa antes de otra confirmación. |
| `503`, timeout o respuesta perdida | Resultado no comprobado; no asegurar que el registro falló. | Consultar primero y conservar la solicitud original para repetición exacta. |
| `401/403` | Acceso no permitido, sin contenido protegido. | Flujo de sesión/autorización vigente. |

Si falla la lectura posterior a un `202`, mantener `Paquete recibido` y ofrecer Actualizar; no reabrir una recepción nueva. Si cambia la incidencia durante la recuperación, no atribuirle el resultado original ni copiarle el formulario. La repetición recupera únicamente la solicitud original; una confirmación sobre otro contexto exige revisión explícita [cite: 3].

## 6. Accesibilidad y adaptación

- Foco inicial en título/resumen y después en el grupo Sí/No; orden coherente, foco contenido en el modal y retorno al disparador. Si la fila desapareció, llevarlo al encabezado/listado actualizado.
- Antes del envío, Cancelar/Escape/fondo cierran sin mutar; abrir de nuevo comienza un formulario nuevo. Durante un resultado desconocido, cerrar no autoriza otra confirmación sin consultar primero.
- Etiquetas visibles, selección operable por teclado, ayuda y errores asociados; anunciar resultado y recuperación sin anuncios duplicados. El color no es el único indicador.
- Modal de ancho medio en escritorio y ajustado al ancho disponible en móvil, contenido desplazable y botones accesibles con teclado; en móvil principal debajo de Cancelar. Verificar ampliación al 200 %.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Abrir desde listado/detalle y contrastar paquete, incidencia y fecha. | Contexto correcto, fecha `America/Lima` y origen conservado. | CA-07/11/12 |
| CUI-02 | Elegir No sin observación y comprobar límites con espacios/emojis. | `No` se acepta; opcionalidad y longitud coinciden con contrato. | CA-02/05 |
| CUI-03 | Confirmar con respuesta demorada y repetir clic/Enter. | Un envío, campos bloqueados y resultado anunciado. | CA-01/10/12 |
| CUI-04 | Simular `400/500/503` y pérdida de respuesta. | Valores conservados; resultado desconocido exige consulta y repetición exacta si procede. | CA-03/05/08/12 |
| CUI-05 | Recibir `409`, cambio de incidencia o confirmación por otro Gestor. | Revisión del contexto, sin sobrescritura ni traslado automático de la decisión. | CA-04/07/10/12 |
| CUI-06 | Aceptar con Operación caída y fallar después el refresco. | Recepción sigue aceptada, sincronización distinguible y Actualizar disponible. | CA-01/09/12 |
| CUI-07 | Perder autorización durante apertura o recuperación. | Datos retirados y acceso bloqueado. | CA-06 |
| CUI-08 | Recorrer con teclado, móvil y ampliación. | Selección, errores, envío, cierre y retorno de foco utilizables. | CA-02/12 |

- Verificado localmente: 10 pruebas del modal y una prueba de integración de componentes en cada pantalla; `npm run test:f04` aprueba 32 pruebas contando las regresiones. Se comprobaron No sin observación, Unicode, doble envío, errores, permisos, recuperación, refresco y conservación del origen con APIs simuladas.
- Revisión manual con datos simulados: apertura desde ambos orígenes, teclado/Tab/Escape, foco inicial y retorno al disparador o encabezado; a 390 × 844 píxeles CSS el modal no desborda y la acción principal queda debajo de Cancelar.
- Pendientes: recorrido con Gateway y servicios reales, ampliación al 200 % y revisión visual con Max. La reutilización comprobada no cierra las tareas generales de los componentes compartidos. Resultados, captura, commits y límites en [EV-04](./evidence.md#ev-04-modal-estados-y-accesibilidad) y [EV-05](./evidence.md#ev-05-recorrido-real-y-coherencia-del-módulo) [cite: 4].

## 8. Referencias

- [cite: 1] [Especificación](./spec.md), [listado](../ES-F04-01-ConsultarEntregasFallidas/spec.md) y [detalle](../ES-F04-02-ConsultarDetalleIncidencia/spec.md).
- [cite: 2] [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md), §23/P3; [diseño F-04](../../disenio/funcionalidades/f-04.md); [componentes React](../../disenio/componentes-react.md), CR-01/02/08/09/15.
- [cite: 3] [Gestión §5.2.1](../../integraciones/api-contract-gestion-despachos.md#521-confirmar-recepción-en-centro--es-f04-03) y §5.3: única definición de formatos y errores.
- [cite: 4] [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
