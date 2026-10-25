# UI de ES-F04-04: Reprogramar un despacho fallido

**Responsable:** Gerardo; revisión visual con el responsable de UI pendiente.

**Estado:** Implementación local y pruebas automatizadas verificadas el 24/10/2026; revisión humana/zoom nativo pendientes.

**Aplicabilidad:** Modal administrativo sobre detalle, sin ruta propia.

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Gestor autenticado con `GESTOR_DESPACHO`; acceso desde `/entregas-fallidas/:idDespacho` mediante acción Reprogramar habilitada en detalle actualizado.
- Objetivo: elegir fecha futura y volver inmediatamente a cola sin consumir intento.
- Destino tras éxito: listado con filtros, página y tamaño de origen; sin origen previo, listado inicial. Cancelar conserva el detalle.
- El formulario es la confirmación explícita; no abre una segunda confirmación ni una operación masiva [cite: 1].

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| [SYSTEM-DESIGN](../../disenio/SYSTEM-DESIGN.md) | §23, P4; formularios y accesibilidad | Modal, jerarquía y mensajes. |
| [Diseño F-04](../../disenio/funcionalidades/f-04.md) | Pantalla 4 | Resumen, campos y navegación. |
| [Componentes](../../disenio/componentes-react.md) | CR-01/02/08/09/15 | Acciones, campos, estados, etiquetas y notificación. |

`ModalReprogramacionDespacho` es una composición local implementada con Modal, Textarea y DatePickerInput de Mantine. CR-12 es una confirmación genérica; no se lo transforma obligatoriamente en formulario. Reutilizar tema/proveedor; verificar controles compartidos en T-01 antes de consumirlos [cite: 2].

## 3. Pantallas e interacción

### UI-01. Modal de reprogramación

Composición: título → código operativo interno, motivo del fallo e intentos consumidos/máximo dinámicos → fecha y observación → explicación de retorno a cola → mensajes → Cancelar y Confirmar reprogramación.

| Paso | Acción de la persona | Respuesta de la interfaz | Criterios |
|---|---|---|---|
| 1 | Abre desde detalle. | Conserva despacho/incidencia/versión y verifica contexto antes de habilitar. | CA-04/17 |
| 2 | Completa fecha y observación opcional. | Valida los campos, explica el efecto y conserva entrada. | CA-02/09/17 |
| 3 | Confirma. | Un envío, controles bloqueados y resultado anunciado. | CA-01/11/17 |
| 4 | Recibe 200 nuevo/replay. | Informa `Despacho reprogramado para [fecha]` y consulta la situación actual. | CA-01/08/12/17 |
| 5 | Vuelve a listado. | Restaura consulta de origen, recarga filas/indicadores y retira la fila resuelta. | CA-12/17 |

Explicar visibilidad inmediata en F-02, asignación desde su fecha si la reserva anterior se liberó y contador sin aumento. Usar día civil en Lima, sin convertir el valor a UTC.

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones/recuperación |
|---|---|---|
| Carga/actualización | Resumen en carga, envío bloqueado. | Cancelar o reintentar lectura si falla. |
| Listo | Resumen y campos; acción permitida por detalle. | Cancelar o confirmar con datos válidos. |
| Contexto inexistente/ausente o acción no permitida | Razón comprensible, sin formulario operativo. | Cerrar y actualizar detalle. |
| Envío en curso | Carga y controles bloqueados. | Evitar doble clic/Enter y cierre accidental por Escape/fondo hasta resultado o recuperación. |
| Aceptado | `Despacho reprogramado para [fecha]`. | Cerrar y actualizar origen; no afirmar recepción en Ventas. |
| Validación/error recuperable | Error de campo o aviso, valores conservados. | Corregir/reintentar según contrato y contexto. |
| Conflicto | Información cambió, revisión necesaria. | Actualizar; no sustituir identidad/versión y reenviar automáticamente. |
| Resultado desconocido | No se pudo comprobar el resultado. | Consultar antes de recuperar exactamente la solicitud original. |
| Sin autorización | Datos protegidos retirados. | Recuperar sesión o volver a vista permitida. |

No hay lista vacía propia del modal: falta de contexto es un error de acceso/recurso. Una lectura fallida después de 200 muestra `Reprogramación registrada. No se pudo actualizar el listado`, conserva la confirmación y ofrece Actualizar sin volver a enviar.

## 5. Formularios y mensajes

| Campo/control | Obligatorio | Validación y momento | Mensaje/contenido |
|---|---|---|---|
| Resumen | Solo lectura | Código, incidencia y contador; contexto vigente antes de habilitar. | Motivo de fallo separado de la decisión. |
| Nueva fecha | Sí | Sin valor inicial; fecha civil futura en Lima desde `consultadoEn`. Backend valida al confirmar. | `Elige una fecha posterior a hoy.` |
| Observación | No | Hasta 500 puntos de código normalizados, omisión/null/espacios como ausencia. | `Máximo 500 caracteres.` |
| Confirmar reprogramación | Acción principal | Deshabilitada sin datos válidos/contexto o durante envío. | `Confirmar reprogramación`. |
| Cancelar | Acción secundaria | Antes del envío cierra sin mutar. | `Cancelar`. |

Contar puntos de código después de normalizar según el contrato; un límite nativo UTF-16 no basta para emojis. Usuario, fecha del servidor, IDs y reserva no son editables. La observación no modifica la recepción.

| Resultado contractual | Mensaje/comportamiento | Recuperación |
|---|---|---|
| 200 nuevo/replay | Aceptación local; cuerpo original no acredita situación actual de capacidad/comunicación. | Consultar y actualizar origen. |
| 400 | Error por campo, sin borrar entradas. | Corregir manteniendo contexto válido. |
| 404 | Despacho no disponible. | Cerrar y actualizar origen. |
| 409/422 | Cambio concurrente, identidad incompatible o límite. | Consultar y revisar antes de otra decisión. |
| 500 inconsistencia | No puede confirmarse con estos datos; requiere revisar la causa. | Conservar datos autorizados, sin inventar referencias/política. |
| 503, timeout o respuesta perdida | Resultado no comprobado; no afirmar reversión. | Consultar antes de replay con la solicitud original. |
| 401/403 | Acceso no permitido, sin datos protegidos. | Flujo de sesión/autorización vigente. |

Fecha futura se valida al confirmar en Lima; medianoche puede invalidar la selección y exige corregir. Liberación pendiente/de revisión, jornada, sello o visor no añaden bloqueos.

El contenedor conserva identidad/cuerpo enviados mientras recupera un resultado desconocido. Cerrar el modal no autoriza otra decisión sin consultar; si cambia la incidencia, no copiar el formulario a la nueva salida ni atribuirle el resultado antiguo. El detalle mantiene «Revisar reprogramación pendiente» aunque su lectura actual sea histórica, para recuperar ese mismo comando sin iniciar otra decisión [cite: 3].

## 6. Accesibilidad y adaptación

- Foco inicial en título/resumen, orden coherente, foco contenido y retorno al disparador al cancelar. Tras éxito, foco en encabezado del listado si ya no existe la fila.
- Etiquetas visibles, errores asociados y anuncio de carga/resultado/recuperación sin duplicados; no depender solo del color.
- Cancelar/Escape/fondo antes de enviar no mutan; durante envío evitar cierre accidental. Mantener reglas de recuperación ante resultado desconocido.
- Modal medio en escritorio y ajustado al ancho móvil, contenido desplazable y acciones alcanzables; verificar teclado y ampliación al 200 %.
- Selector operable con teclado, presentación DD/MM/YYYY y valor civil conservado; reloj del navegador no autoriza.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Abrir desde detalle autorizado y volver al listado. | Mismo despacho/incidencia/versión; conserva filtros/página. | CA-04/12/17 |
| CUI-02 | Fecha vacía, hoy/pasado, otra zona y cambio de día. | No preselecciona; valida desde Lima y conserva la fecha como día. | CA-02/17 |
| CUI-03 | Omitir, usar espacios, 500/501 puntos de código y emojis. | Opcionalidad/límite coinciden con contrato sin alterar recepción. | CA-09/17 |
| CUI-04 | Combinar recepción, anulación y máximo; cambiar política. | Explica bloqueos del detalle; no permite envío con contexto obsoleto. | CA-03/05/06/07/18 |
| CUI-05 | Doble clic/Enter con respuesta demorada. | Una solicitud en curso, campos bloqueados y confirmación anunciada. | CA-01/11/17 |
| CUI-06 | 400/409/422/500/503, timeout o cambio de incidencia. | Conserva entradas recuperables y consulta antes de replay; no cambia IDs. | CA-04/08/10/17 |
| CUI-07 | 200 o replay y fallo del refresco posterior. | Conserva éxito, actualiza origen y ofrece Actualizar sin reenviar. | CA-12/17 |
| CUI-08 | Teclado, móvil, zoom 200 % y pérdida de permisos. | Foco/errores utilizables; retira datos protegidos ante 401/403. | CA-15/17 |

- Composición local Mantine y base de interacción reutilizadas/verificadas; no se cambiaron componentes compartidos. La regresión de CR-03 tiene un fallo previo documentado en EV-03.
- Resultados ejecutados: EV-03 de [evidence.md](./evidence.md), con JSDOM y navegador contra Gestión/PostgreSQL reales. Se separan fixtures, proxy de pruebas y proveedores externos. CUI-08 mantiene pendiente revisión humana y zoom nativo.

## 8. Referencias

- [cite: 1] [Especificación](./spec.md), [detalle](../ES-F04-02-ConsultarDetalleIncidencia/spec.md) y [listado](../ES-F04-01-ConsultarEntregasFallidas/spec.md).
- [cite: 2] [SYSTEM-DESIGN](../../disenio/SYSTEM-DESIGN.md), [diseño F-04](../../disenio/funcionalidades/f-04.md) y [componentes](../../disenio/componentes-react.md), CR-01/02/08/09/15.
- [cite: 3] [Gestión §5.2.2](../../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04), fuente única de formatos y errores.
- [cite: 4] [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
