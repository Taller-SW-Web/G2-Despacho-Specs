# UI de ES-F03-02: Consulta de la ruta de la jornada

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** Vista «Mi Ruta» de la web responsive del repartidor.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario: titular del JWT humano con perfil local activo y vinculado; en turno o fuera de turno (ES-F03-01).
- Contexto: uso en campo desde el celular; diseño mobile-first.
- Objetivo visible: saber qué despachos entregar hoy y en qué orden.
- Salida: la operación de cada despacho se define en otras especificaciones de F-03.

## 2. Referencias visuales

| Fuente | Aplicación |
|---|---|
| Wireframe de la vista «Mi Ruta» de F-03 | Composición de la lista y la bandeja |
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | Tokens, badges de estado y estados vacíos |
| [Componentes React](../../disenio/componentes-react.md) | Componentes compartidos aplicables (DT-03 del plan) |

## 3. Pantallas e interacción

### UI-01. Lista «Mi Ruta»

| Elemento | Contenido y comportamiento |
|---|---|
| Elemento de la lista | Posición en la secuencia, código operativo interno, destinatario, dirección, badge de estado y número de intento |
| Dirección | Visible solo en `ASIGNADO` o `EN_CAMINO`; sin acción de exportar ni de copia masiva |
| Orden | Secuencia de F-02; no se puede reordenar desde esta vista |
| Modo | Operativo o de solo lectura según ES-F03-01 |

### UI-02. Bandeja «Pendientes de regularización»

| Elemento | Contenido y comportamiento |
|---|---|
| Ubicación | Sección separada de la ruta vigente; visible solo si hay despachos |
| Elementos | Despachos de jornadas anteriores sin cierre, con su fecha |
| Acciones | Ninguna; no pueden operarse |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Abrir «Mi Ruta» | Carga y luego lista ordenada | CA-01 |
| 2 | Abrir sin despachos | Mensaje de ruta vacía | CA-02 |
| 3 | Respuesta `403` | Se retiran los datos y se muestra acceso denegado | CA-03 |
| 4 | Existen despachos anteriores sin cierre | Bandeja separada sin acciones | CA-04 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Carga | Elementos skeleton | Esperar | CA-01 |
| Con datos | Lista ordenada | Consultar u operar según modo | CA-01 |
| Ruta vacía | «No tienes despachos asignados para hoy.» | Actualizar | CA-02 |
| Acceso denegado | Mensaje sin datos | Volver al acceso | CA-03 |
| Con pendientes de regularización | Bandeja separada | Ninguna | CA-04 |
| Error de red o `5xx` | Mensaje sin detalle técnico | «Reintentar» | CA-01 |

## 5. Accesibilidad y adaptación

- Lista navegable con teclado y lector de pantalla; posición anunciada.
- Estados diferenciados por texto e icono, no solo por color.
- Objetivos táctiles amplios y legibilidad en exteriores.
- Sin desbordamiento horizontal en viewport móvil.

## 6. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Abrir con despachos en varios estados | Orden, campos y badges correctos; dirección oculta fuera de `ASIGNADO` / `EN_CAMINO` | CA-01 |
| CUI-02 | Abrir sin despachos | Mensaje de ruta vacía | CA-02 |
| CUI-03 | Recibir `403` | Sin datos en pantalla | CA-03 |
| CUI-04 | Abrir con despachos anteriores sin cierre | Bandeja separada sin acciones | CA-04 |
| CUI-05 | Recorrer en viewport móvil y con lector de pantalla | Elementos alcanzables y anunciados | CA-01 a CA-04 |

## 7. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. Wireframe de la vista «Mi Ruta» de F-03.
