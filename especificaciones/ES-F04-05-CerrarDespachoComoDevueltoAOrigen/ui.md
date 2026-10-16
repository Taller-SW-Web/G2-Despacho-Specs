# UI de ES-F04-05: Cerrar un despacho como devuelto a origen

**Responsable:** Gerardo; revisión visual con el responsable de UI pendiente.

**Estado:** Preparada documentalmente; implementación y verificación pendientes.

**Aplicabilidad:** Modal administrativo sobre detalle, sin ruta propia.

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Gestor autenticado con `GESTOR_DESPACHO`; acceso desde `/entregas-fallidas/:idDespacho` mediante acción Cerrar como devuelto a origen habilitada en detalle actualizado.
- Objetivo: confirmar que no habrá otro intento y registrar el motivo del fin logístico.
- Destino tras éxito: listado con filtros, página y tamaño de origen; sin origen previo, listado inicial. Cancelar conserva el detalle.
- El formulario es la confirmación explícita; no abre una segunda confirmación ni una operación masiva [cite: 1].

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| [SYSTEM-DESIGN](../../disenio/SYSTEM-DESIGN.md) | §23, P5; formularios y accesibilidad | Modal, jerarquía y mensajes. |
| [Diseño F-04](../../disenio/funcionalidades/f-04.md) | Pantalla 5 | Resumen, campos y navegación. |
| [Componentes](../../disenio/componentes-react.md) | CR-01/02/08/09/15 | Acciones, campos, estados, etiquetas y notificación. |

`ModalCierreDespacho` es una composición local propuesta con Modal, Textarea de Mantine. CR-12 es una confirmación genérica; no se lo transforma obligatoriamente en formulario. Reutilizar tema/proveedor; verificar controles compartidos en T-01 antes de consumirlos [cite: 2].

## 3. Pantallas e interacción

### UI-01. Modal de cierre

Composición: título → código operativo interno, motivo del fallo e intentos consumidos/máximo dinámicos → advertencia final → motivo del cierre y observación → mensajes → Cancelar y Cerrar despacho.

| Paso | Acción de la persona | Respuesta de la interfaz | Criterios |
|---|---|---|---|
| 1 | Abre desde detalle. | Conserva despacho/incidencia/versión y verifica contexto antes de habilitar. | CA-04/09/14 |
| 2 | Completa motivo y observación opcional. | Valida los campos, explica el efecto y conserva entrada. | CA-06/14 |
| 3 | Confirma. | Un envío, controles bloqueados y resultado anunciado. | CA-01/10/14 |
| 4 | Recibe 200 nuevo/replay. | Informa `Despacho cerrado como devuelto a origen` y consulta la situación actual. | CA-01/02/14/15 |
| 5 | Vuelve a listado. | Restaura consulta de origen, recarga filas/indicadores y retira la fila resuelta. | CA-14/15 |

La advertencia informa que no habrá más entregas y el paquete queda en el centro a disposición de Ventas. No anuncia reembolso ni procesamiento del webhook. Motivo es texto libre obligatorio, distinto del fallo; no se crea selector/catálogo.

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones/recuperación |
|---|---|---|
| Carga/actualización | Resumen en carga, envío bloqueado. | Cancelar o reintentar lectura si falla. |
| Listo | Resumen y campos; acción permitida por detalle. | Cancelar o confirmar con datos válidos. |
| Contexto inexistente/ausente o acción no permitida | Razón comprensible, sin formulario operativo. | Cerrar y actualizar detalle. |
| Envío en curso | Carga y controles bloqueados. | Evitar doble clic/Enter y cierre accidental por Escape/fondo hasta resultado o recuperación. |
| Aceptado | `Despacho cerrado como devuelto a origen`. | Cerrar y actualizar origen; no afirmar recepción en Ventas. |
| Validación/error recuperable | Error de campo o aviso, valores conservados. | Corregir/reintentar según contrato y contexto. |
| Conflicto | Información cambió, revisión necesaria. | Actualizar; no sustituir identidad/versión y reenviar automáticamente. |
| Resultado desconocido | No se pudo comprobar el resultado. | Consultar antes de recuperar exactamente la solicitud original. |
| Sin autorización | Datos protegidos retirados. | Recuperar sesión o volver a vista permitida. |

No hay lista vacía propia del modal: falta de contexto es un error de acceso/recurso. Una lectura fallida después de 200 muestra `Cierre registrado. No se pudo actualizar el listado`, conserva la confirmación y ofrece Actualizar sin volver a enviar.

## 5. Formularios y mensajes

| Campo/control | Obligatorio | Validación y momento | Mensaje/contenido |
|---|---|---|---|
| Resumen | Solo lectura | Código, incidencia y contador; contexto vigente antes de habilitar. | Motivo de fallo separado de la decisión. |
| Motivo del cierre | Sí | Textarea de 1 a 500 puntos de código normalizados, sin solo espacios. | `Indica el motivo del cierre.` |
| Observación | No | Hasta 500 puntos de código normalizados, omisión/null/espacios como ausencia. | `Máximo 500 caracteres.` |
| Cerrar despacho | Acción principal | Deshabilitada sin datos válidos/contexto o durante envío. | `Cerrar despacho`. |
| Cancelar | Acción secundaria | Antes del envío cierra sin mutar. | `Cancelar`. |

Contar puntos de código después de normalizar según el contrato; un límite nativo UTF-16 no basta para emojis. Usuario, fecha del servidor, IDs y reserva no son editables. La observación no modifica la recepción.

| Resultado contractual | Mensaje/comportamiento | Recuperación |
|---|---|---|
| 200 nuevo/replay | Aceptación local; cuerpo original no acredita situación actual de capacidad/comunicación. | Consultar y actualizar origen. |
| 400 | Error por campo, sin borrar entradas. | Corregir manteniendo contexto válido. |
| 404 | Despacho no disponible. | Cerrar y actualizar origen. |
| 409 | Cambio concurrente, identidad incompatible. | Consultar y revisar antes de otra decisión. |
| 500 inconsistencia | No puede confirmarse con estos datos; requiere revisar la causa. | Conservar datos autorizados, sin inventar referencias/política. |
| 503, timeout o respuesta perdida | Resultado no comprobado; no afirmar reversión. | Consultar antes de replay con la solicitud original. |
| 401/403 | Acceso no permitido, sin datos protegidos. | Flujo de sesión/autorización vigente. |

Liberación pendiente/de revisión, jornada, sello o visor no añaden bloqueos. Máximo alcanzado, anulado, NO_INTENTADO o intentos disponibles permiten cierre explícito; ninguna condición cierra automáticamente.

El contenedor conserva identidad/cuerpo enviados mientras recupera un resultado desconocido. Cerrar el modal no autoriza otra decisión sin consultar; si cambia la incidencia, no copiar el formulario a la nueva salida ni atribuirle el resultado antiguo [cite: 3].

## 6. Accesibilidad y adaptación

- Foco inicial en título/resumen, orden coherente, foco contenido y retorno al disparador al cancelar. Tras éxito, foco en encabezado del listado si ya no existe la fila.
- Etiquetas visibles, errores asociados y anuncio de carga/resultado/recuperación sin duplicados; no depender solo del color.
- Cancelar/Escape/fondo antes de enviar no mutan; durante envío evitar cierre accidental. Mantener reglas de recuperación ante resultado desconocido.
- Modal medio en escritorio y ajustado al ancho móvil, contenido desplazable y acciones alcanzables; verificar teclado y ampliación al 200 %.
- Advertencia final legible, botón destructivo identificado por texto y motivo claramente separado del fallo.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Abrir sobre detalle actualizado con recepción confirmada. | Código operativo, incidencia y versión correctos; motivo de fallo separado del cierre. | CA-04/09/14 |
| CUI-02 | Omitir motivo, espacios, 500/501 puntos de código y emojis. | Motivo requerido en texto libre; observación opcional; errores por campo. | CA-06/14 |
| CUI-03 | Límite, anulado, NO_INTENTADO, intentos disponibles y liberación pendiente. | Se respetan acciones del detalle sin añadir bloqueos o cierre automático. | CA-04/05/08/11 |
| CUI-04 | Clic/Enter repetidos durante respuesta demorada. | Un envío y advertencia final accesible; controles bloqueados durante envío. | CA-01/10/14 |
| CUI-05 | 409, otro Gestor o cambio de incidencia/versión. | Actualiza y exige revisar; no reaplica el motivo automáticamente. | CA-02/09/10/14 |
| CUI-06 | Timeout/503, 500 o respuesta perdida. | Conserva solicitud/entradas y consulta antes del replay; distingue inconsistencia de resultado desconocido. | CA-02/12/14 |
| CUI-07 | 200 y refresco fallido; comunicación pendiente/fallida. | Conserva cierre aceptado, restaura filtros/página y no promete recepción en Ventas. | CA-03/14/15 |
| CUI-08 | Teclado, móvil, zoom 200 % y pérdida de autorización. | Foco/etiquetas/errores utilizables; 401/403 retiran datos. | CA-07/14 |

- No hay decisiones funcionales nuevas de UI pendientes. Disponibilidad/revisión de controles y herramienta de interacción: DT-01 del plan, pendiente de ejecución.
- Evidencia prevista: EV-03 de [evidence.md](./evidence.md); distinguir fixtures, API real y revisión manual de foco/móvil. Ningún CUI fue ejecutado al preparar esta carpeta.

## 8. Referencias

- [cite: 1] [Especificación](./spec.md), [detalle](../ES-F04-02-ConsultarDetalleIncidencia/spec.md) y [listado](../ES-F04-01-ConsultarEntregasFallidas/spec.md).
- [cite: 2] [SYSTEM-DESIGN](../../disenio/SYSTEM-DESIGN.md), [diseño F-04](../../disenio/funcionalidades/f-04.md) y [componentes](../../disenio/componentes-react.md), CR-01/02/08/09/15.
- [cite: 3] [Gestión §5.2.3](../../integraciones/api-contract-gestion-despachos.md#523-cerrar-como-devuelto-a-origen--es-f04-05), fuente única de formatos y errores.
- [cite: 4] [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
