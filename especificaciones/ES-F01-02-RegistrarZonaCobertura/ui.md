# UI de ES-F01-02: Registrar y editar una zona de cobertura

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión e implementación.

**Aplicabilidad:** Formulario de zona (Pantalla 2) en la aplicación administrativa.

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Usuario y permisos: Gestor de Despacho con rol `GESTOR_DESPACHO`; sin ese rol se muestra acceso denegado sin datos de configuración.
- Contexto de uso: centro de despacho; uso principal en escritorio, con adaptación responsive.
- Objetivo visible: crear o editar una zona y delimitarla por distritos y códigos postales.
- Acceso y navegación: se abre desde «Nueva zona» o «Editar» del catálogo (ES-F01-01); la ruta frontend propuesta es `/zonas/nueva` y `/zonas/:id/editar`.
- Salidas: «Guardar» persiste y regresa al catálogo; «Cancelar» descarta sin persistir. Si el backend devuelve un conflicto de cobertura, se ofrece revisar la zona en conflicto [cite: 1].

## 2. Referencias visuales y componentes

| Fuente | Secciones | Aplicación |
|---|---|---|
| [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | Formularios, campos, validación y modales | Estructura, tokens y pautas del formulario. |
| [Diseño F-01](../../disenio/funcionalidades/f-01.md) | Pantalla 2: Formulario de Zona | Contenido y campos del formulario. |
| [Alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md) | Formulario de zona y estados de validación | Presentación de campos y errores. |
| [Componentes React](../../disenio/componentes-react.md) | §4.5 y §4.6; CR de formulario | Contratos de componentes y responsables propuestos. |

La delimitación se realiza por distritos y códigos postales, sin mapa, sin polígonos y sin rangos. Los fragmentos del wireframe que mostraban un mapa quedan fuera de alcance [cite: 1, 2].

## 3. Pantallas e interacción

### UI-01. Formulario de Zona

Composición: estructura administrativa CR-03 → encabezado CR-05 → campos de formulario con validación en línea → acciones «Cancelar» y «Guardar». El título cambia entre «Nueva zona» y «Editar zona».

| Elemento | Contenido y comportamiento |
|---|---|
| Nombre | Campo de texto obligatorio, entre 1 y 80 caracteres; se marca el error junto al campo. |
| Distritos | Selector múltiple obligatorio; el formulario exige al menos un distrito o un código postal. |
| Códigos postales | Campo múltiple opcional. |
| Estado inicial | Selector Activo / Inactivo; en edición se muestra el estado vigente y no se modifica desde este formulario. |
| Acciones | «Cancelar» descarta; «Guardar» permanece deshabilitado mientras falten el nombre o la delimitación. |
| Conflicto | Un `409 Conflict` presenta la zona y el elemento en conflicto junto al control afectado. |

| Paso | Acción de la persona | Respuesta de la interfaz | Criterio funcional |
|---|---|---|---|
| 1 | Abrir el formulario | Presentar campos vacíos (alta) o con los valores actuales (edición) | CA-01, CA-04 |
| 2 | Completar nombre y delimitación | Habilitar «Guardar» al cumplirse los mínimos | CA-01, CA-03 |
| 3 | Confirmar | Enviar y mostrar el estado de guardado | CA-01, CA-04 |
| 4 | Recibir un conflicto | Marcar los campos afectados y explicar el conflicto | CA-02, CA-05 |
| 5 | Recibir un rechazo de permisos | Retirar el formulario y sus datos | CA-06 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones disponibles | Criterio |
|---|---|---|---|
| Alta | Formulario vacío | Completar y guardar; cancelar | CA-01 |
| Edición | Formulario con los valores actuales | Modificar y guardar; cancelar | CA-04 |
| Guardando | Controles deshabilitados y estado de progreso | Esperar | CA-01, CA-04 |
| Error de validación | Mensajes junto a cada campo | Corregir y reintentar | CA-02, CA-03, CA-05 |
| Conflicto de cobertura | Detalle de la zona y el elemento en conflicto | Corregir la delimitación | CA-02, CA-05 |
| Error de red | Mensaje comprensible sin detalle técnico | «Reintentar» conservando los datos | CA-01 |
| Sin permisos | Acceso denegado sin datos del formulario | Navegación permitida por la aplicación | CA-06 |

## 5. Formularios y mensajes

| Control | Obligatorio | Validación y momento | Mensaje visible | Fuente contractual |
|---|---|---|---|---|
| Nombre | Sí | No vacío; 1 a 80 caracteres; en línea y al enviar | «El nombre es obligatorio» / «Máximo 80 caracteres» | Contrato §9.1 |
| Distritos | Sí (con códigos postales) | Al menos un distrito o un código postal | «Selecciona al menos un distrito o código postal» | Contrato §9.1 |
| Códigos postales | No | Formato de código postal; opcional | «Código postal inválido» | Contrato §9.1 |
| Estado inicial | Sí | Activo / Inactivo; solo en alta | Valor por defecto Activo | Contrato §9.1 |

| Resultado o error de API | Mensaje y comportamiento de UI | Recuperación |
|---|---|---|
| `400` | Marcar los campos inválidos con su mensaje | Corregir y reintentar |
| `409` | Mostrar la zona y el elemento en conflicto | Corregir la delimitación |
| `401` / `403` | Acceso denegado sin datos | Navegación permitida |
| Error de red o `5xx` | Mensaje comprensible con reintento | «Reintentar» conservando los datos |

La presentación usa fechas de la zona operativa `America/Lima`; los nombres definitivos de los campos provienen del contrato central y se registran en los pendientes del plan [cite: 3].

## 6. Accesibilidad y adaptación

- Teclado y foco: recorrer los campos y acciones con teclado; el foco se sitúa en el primer campo inválido al enviar.
- Etiquetas y avisos: etiquetas asociadas a cada control; los errores se anuncian y se asocian al campo mediante atributos accesibles.
- Percepción: no depender solo del color para indicar errores; usar texto e iconos.
- Responsive: una columna en móvil y diseño de dos columnas en escritorio según los breakpoints del diseño.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Alta válida con distrito y estado Activo | «Guardar» habilitado y confirmación al guardar | CA-01 |
| CUI-02 | Alta con nombre o distrito ya existente | Mensaje de conflicto con la zona en conflicto | CA-02 |
| CUI-03 | Intentar guardar sin delimitación | «Guardar» deshabilitado y mensaje claro | CA-03 |
| CUI-04 | Editar nombre y delimitación válidos | Campos precargados y confirmación al guardar | CA-04 |
| CUI-05 | Editar con distrito de otra zona activa | Conflicto marcado y delimitación anterior conservada | CA-05 |
| CUI-06 | Recibir `403` tras abrir el formulario | Se retiran formulario y datos | CA-06 |
| CUI-07 | Recorrer el formulario con teclado en escritorio y móvil | Campos y acciones alcanzables; foco en primer error; responde bien en móvil | CA-01 a CA-06 |

- Pendientes de diseño: nombres y formatos definitivos de los campos (DT-01 del plan).
- Evidencia prevista: pruebas de interacción, revisión con teclado y capturas de los estados aplicables.

## 8. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-06.
2. [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [guía F-01](../../disenio/funcionalidades/f-01.md); [componentes React](../../disenio/componentes-react.md).
3. [Contrato de API](../../integraciones/api-contract.md), §§3.3, 3.5 y 9.1; [modelo de datos](../../arquitectura/modelo-datos.md), §3.1.
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
