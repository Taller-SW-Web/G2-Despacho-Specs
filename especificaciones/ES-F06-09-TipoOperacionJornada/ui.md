# UI de ES-F06-09: Elegir el tipo de operación de la jornada

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** apertura de jornada y monitoreo del panel administrativo.

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuario y permisos: Gestor con rol `GESTOR_DESPACHO`.
- Objetivo visible: decidir si la jornada es de entregas o de recojos, y ver el tipo de cada jornada.
- Acceso: panel administrativo → Jornadas.

## 2. Pantallas e interacción

### UI-01. Apertura de jornada

Añade el selector obligatorio «Tipo de jornada», con las opciones «Entregas» y «Recojos», sin valor preseleccionado. Se usa el formulario y los componentes actuales.

### UI-02. Monitoreo

Cada jornada muestra su tipo con texto.

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Abrir el formulario | Selector vacío y obligatorio | CA-01 |
| 2 | Confirmar sin tipo | Envío bloqueado: «Selecciona el tipo de jornada.» | CA-01 |
| 3 | Confirmar con tipo | Jornada visible en el monitoreo con su tipo | CA-01 |

## 3. Accesibilidad

- El selector tiene etiqueta visible y su error se anuncia.
- El tipo se muestra con texto, no solo con color.

## 4. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Abrir una jornada sin elegir tipo | Envío bloqueado | CA-01 |
| CUI-02 | Abrir una jornada de cada tipo | Tipo correcto en el monitoreo | CA-01, CA-02 |

## 5. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
