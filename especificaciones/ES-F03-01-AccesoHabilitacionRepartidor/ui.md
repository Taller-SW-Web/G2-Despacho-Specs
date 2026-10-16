# UI de ES-F03-01: Acceso y habilitación operativa del repartidor

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** Pantalla de acceso y entrada a «Mi Ruta» de la web responsive del repartidor.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario: repartidor con rol `REPARTIDOR`.
- Contexto: uso en campo desde el celular; diseño mobile-first.
- Objetivo visible: ingresar y saber de inmediato si puede operar o solo consultar.
- Salida: «Mi Ruta» en modo operativo o de solo lectura; su contenido se define en otra especificación de F-03.

## 2. Referencias visuales

| Fuente | Aplicación |
|---|---|
| Wireframe de la pantalla de acceso de F-03 | Composición de la pantalla de acceso y mensajes de bloqueo |
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | Tokens, tipografía y estados |
| [Componentes React](../../disenio/componentes-react.md) | Componentes compartidos aplicables (DT-04 del plan) |

## 3. Pantallas e interacción

### UI-01. Pantalla de acceso

| Elemento | Contenido y comportamiento |
|---|---|
| Autenticación | Delegada a Seguridad y Usuarios (mecanismo pendiente, DT-01) |
| Mensaje de bloqueo | Indica el motivo: rol incorrecto o usuario no vinculado |
| Error de conexión | Mensaje comprensible con «Reintentar» |

### UI-02. Entrada a «Mi Ruta»

| Modo | Condición | Presentación |
|---|---|---|
| Operativo | En turno (RN-04) | Acciones de cambio de estado habilitadas |
| Solo lectura | `FUERA_DE_TURNO` | Aviso persistente «Tu turno no está activo»; acciones de transición ocultas o deshabilitadas; ruta y resumen del día visibles |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Abrir la web y autenticarse | Carga mientras se valida el acceso | CA-01 |
| 2 | Acceso válido en turno | «Mi Ruta» en modo operativo | CA-01 |
| 3 | Sesión ausente o vencida | Vuelta a la pantalla de acceso sin datos de despachos | CA-02 |
| 4 | Rol incorrecto o sin vínculo | Mensaje de bloqueo con el motivo | CA-03 |
| 5 | Fuera de turno | «Mi Ruta» en solo lectura con aviso | CA-04 |
| 6 | Transición rechazada con `409` | Mensaje de turno inactivo y paso a solo lectura | CA-04 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Validando acceso | Indicador de carga; sin datos de despachos | Esperar | CA-01 |
| Operativo | «Mi Ruta» con acciones de transición | Operar | CA-01 |
| Sesión inválida (`401`) | Pantalla de acceso | Autenticarse de nuevo | CA-02 |
| Acceso denegado (`403`) | Motivo del bloqueo, sin datos | Cerrar sesión | CA-03 |
| Solo lectura | Ruta, resumen y aviso de turno inactivo | Consultar | CA-04 |
| Error de red o `5xx` | Mensaje sin detalle técnico | «Reintentar» | CA-01 |

## 5. Mensajes por respuesta

| Respuesta | Mensaje | Recuperación |
|---|---|---|
| `401` | «Tu sesión expiró. Ingresa nuevamente.» | Pantalla de acceso |
| `403` rol | «Tu usuario no tiene perfil de repartidor.» | Cerrar sesión |
| `403` sin vínculo | «Tu usuario no está vinculado a un repartidor activo.» | Contactar a su supervisor |
| `409` | «Tu turno no está activo. Solo puedes consultar tu ruta.» | Solo lectura |

Los textos son propuesta; los códigos de error definitivos provienen del contrato (DT-02).

## 6. Accesibilidad y adaptación

- Objetivos táctiles amplios y legibilidad en exteriores.
- Estados diferenciados por texto e icono, no solo por color.
- Mensajes de bloqueo y avisos anunciados a lectores de pantalla.
- Sin desbordamiento horizontal en viewport móvil.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Ingresar en turno | «Mi Ruta» con acciones habilitadas | CA-01 |
| CUI-02 | Sesión vencida con datos en pantalla | Se retiran los datos y se vuelve al acceso | CA-02 |
| CUI-03 | Rol incorrecto y usuario sin vínculo | Motivo correcto en cada caso, sin datos | CA-03 |
| CUI-04 | Ingresar fuera de turno e intentar operar | Aviso visible, acciones bloqueadas y mensaje ante `409` | CA-04 |
| CUI-05 | Recorrer en viewport móvil y con lector de pantalla | Controles alcanzables y mensajes anunciados | CA-01 a CA-04 |

## 8. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. Wireframe de la pantalla de acceso de F-03.
