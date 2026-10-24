# UI de ES-F03-03: Consulta del detalle de un despacho

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** Vista de detalle del despacho de la web responsive del repartidor.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario: titular del JWT humano con perfil local activo y vinculado; el backend comprueba propiedad y estado antes de mostrar datos personales.
- Contexto: en campo, desde el celular; diseño mobile-first.
- Objetivo visible: tener a mano los datos para entregar y llamar al destinatario.
- Entrada: elemento de «Mi Ruta» (ES-F03-02). Salidas: «En camino» (ES-F03-04), «Confirmar entrega» (ES-F03-05) y «Marcar como fallido» (ES-F03-06), según estado y modo de ES-F03-01.

## 2. Referencias visuales

| Fuente | Aplicación |
|---|---|
| Wireframe del detalle del despacho de F-03 | Composición del detalle |
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | Tokens, badges y botones |
| [Componentes React](../../disenio/componentes-react.md) | Componentes compartidos aplicables (DT-03 del plan) |

## 3. Pantallas e interacción

### UI-01. Detalle del despacho

| Elemento | Contenido y comportamiento |
|---|---|
| Encabezado | Código operativo interno y badge de estado |
| Destinatario | Nombre y teléfono con botón de llamada directa (`tel:`) |
| Entrega | Dirección, referencia y fecha programada |
| Intentos | «Intento X de N» |
| Protección | Teléfono y dirección ocultos fuera de `ASIGNADO` / `EN_CAMINO`; sin exportar ni copia masiva |
| Acciones | Solo las permitidas por el estado y el modo operativo |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Seleccionar un despacho en «Mi Ruta» | Carga y detalle | CA-01 |
| 2 | Pulsar llamar | Abre el marcador del celular | CA-01 |
| 3 | Respuesta `403` | Mensaje sin datos y vuelta a «Mi Ruta» | CA-02 |
| 4 | Respuesta `404` | «El despacho no existe» y vuelta a «Mi Ruta» | CA-03 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Carga | Skeleton del detalle | Esperar | CA-01 |
| Con datos | Detalle completo según RN-02 | Llamar y acciones permitidas | CA-01 |
| Acceso denegado | Mensaje sin datos | Volver a «Mi Ruta» | CA-02 |
| No encontrado | Mensaje sin datos parciales | Volver a «Mi Ruta» | CA-03 |
| Error de red o `5xx` | Mensaje sin detalle técnico | «Reintentar» | CA-01 |

## 5. Accesibilidad y adaptación

- Botón de llamada con nombre accesible y objetivo táctil amplio.
- Estado identificado por texto e icono, no solo por color.
- Legibilidad en exteriores; sin desbordamiento horizontal en móvil.

## 6. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Abrir despacho en `ASIGNADO` o `EN_CAMINO` | Todos los campos y llamada directa | CA-01 |
| CUI-02 | Abrir despacho en otro estado | Teléfono y dirección ocultos | CA-01 |
| CUI-03 | Recibir `403` o `404` | Sin datos en pantalla | CA-02, CA-03 |
| CUI-04 | Recorrer en móvil y con lector de pantalla | Controles alcanzables y anunciados | CA-01 a CA-03 |

## 7. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. Wireframe del detalle del despacho de F-03.
