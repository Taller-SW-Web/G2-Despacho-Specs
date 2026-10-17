# UI de ES-F06-02: Consultar el monitoreo de flota

**Responsable de implementación:** Kevin Rhamses Bohorquez. **Estado:** Implementada; automatización local y revisión visual pendiente.

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

Gestor autenticado en `/jornadas`; navegar desde «Jornadas y monitoreo». Consultar el monitoreo de flota. Los datos se obtienen del Gateway y no de fixtures en producción.

## 2. Referencias visuales y componentes

[SYSTEM-DESIGN](../../disenio/SYSTEM-DESIGN.md), [diseño agrupado F-05/F-06](../../disenio/funcionalidades/f-05.md) y [componentes React](../../disenio/componentes-react.md): CR-03 estructura; CR-05/06/07 encabezado, filtros y tabla; CR-10 KPI global; CR-11 tres ocupaciones; CR-14 datos desactualizados; CR-12 confirmación y CR-15 resultado [cite: 2].

## 3. Pantallas e interacción

### UI-01. Jornadas y monitoreo

Encabezado con Actualizar y Abrir jornada; fecha/filtros; cuatro KPI; tabla paginada; detalle con ocupación, límites, remanente y referencias operativas. Apertura en modal con selectores de catálogos reales y fecha del servidor; cierre confirmado indicando que no libera reservas ni resuelve pendientes.

## 4. Estados de la interfaz

Carga sin falsos ceros; lista vacía explícita; error inicial con reintento; datos previos con franja si falla actualización; 401/403 retira datos y modales; mutación pendiente bloquea doble envío; respuesta incierta conserva formulario y exige consultar antes de repetir.

## 5. Formularios y mensajes

Apertura requiere repartidor activo/vinculado, furgoneta disponible y zona activa. La UI no reemplaza la validación del servidor. Conflictos conservan los datos corregibles; éxito se muestra solo con respuesta verificada y consulta posterior. No imprimir detail remoto, SQL ni tokens.

## 6. Accesibilidad y adaptación

Mantener etiquetas, navegación por teclado, foco contenido/retornado en modal, texto además de color en barras/KPI y tabla desplazable sin desbordar la página. En móvil apilar controles y métricas. No anunciar cada refresco como una nueva alerta.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable |
|---|---|---|
| CUI-01 | Abrir pantalla autorizada | Contexto y controles accesibles |
| CUI-02 | Introducir parámetros inválidos | Error visible sin solicitud inválida |
| CUI-03 | Doble envío y respuesta incierta | Sin duplicados ni éxito inventado |
| CUI-04 | Fallo de actualización y recuperación | Datos previos con aviso y posterior actualización |
| CUI-05 | Perder autorización | Retirar datos y formularios protegidos |
| CUI-06 | Teclado y pantalla reducida | Foco, etiquetas y todas las acciones accesibles |

Los seis CUI concretan los CA de spec.md; JSDOM no acredita revisión visual humana.

## 8. Referencias

1. [Especificación](./spec.md) [cite: 1].
2. [Componentes compartidos](../../disenio/componentes-react.md) [cite: 2].
3. [Plan](./plan.md) y [evidencia](./evidence.md) [cite: 3].
