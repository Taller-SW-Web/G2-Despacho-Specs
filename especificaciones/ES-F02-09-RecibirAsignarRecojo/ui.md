# UI de ES-F02-09: Recibir y asignar un recojo

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** cola de programación y modal de asignación.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario y permisos: Gestor con rol `GESTOR_DESPACHO`.
- Objetivo visible: generar recojos de prueba y asignarlos a una jornada de recojos.
- Acceso: panel administrativo → Programación.

## 2. Pantallas e interacción

### UI-01. Generar recojo de prueba

Acción «Generar recojo de prueba» sobre un despacho simulado `ENTREGADO`, identificada como prueba.

### UI-02. Cola

La tabla actual añade la etiqueta de texto «Recojo» y el filtro por tipo.

### UI-03. Modal de asignación

El modal actual lista solo jornadas `RECOJOS`, con las mismas barras de ocupación. Sin candidatos muestra: «No hay jornadas de recojos con capacidad.»

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Generar el recojo | Aparece en la cola | CA-01, CA-03 |
| 2 | Abrir la asignación | Solo jornadas `RECOJOS` | CA-05 |
| 3 | Confirmar | El recojo sale de la cola | CA-04 |
| 4 | Sin capacidad | Aviso de capacidad y recojo en la cola | CA-06 |

## 3. Accesibilidad

- La etiqueta «Recojo» usa texto, no solo color.
- Los errores del modal se anuncian.

## 4. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Cola con despachos y recojos | Etiqueta y filtro correctos | CA-03 |
| CUI-02 | Abrir el modal de un recojo y el de un despacho | Solo jornadas del tipo correcto | CA-05 |
| CUI-03 | Asignar con y sin capacidad | Confirmación o aviso | CA-04, CA-06 |

## 5. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
