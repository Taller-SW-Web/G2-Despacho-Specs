# UI de ES-F01-04: Configurar la tarifa vigente de una zona

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión e implementación.

**Aplicabilidad:** Formulario de tarifas de la zona (Pantalla 3) en la aplicación administrativa.

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- Usuario y permisos: Gestor de Despacho con rol `GESTOR_DESPACHO`; sin ese rol se muestra acceso denegado sin datos de configuración.
- Contexto de uso: centro de despacho; uso principal en escritorio, con adaptación responsive.
- Objetivo visible: definir la regla de cobro de una zona y dejar la nueva regla como única tarifa vigente.
- Acceso y navegación: se abre desde la acción «Tarifas» de una fila del catálogo (ES-F01-01) o desde la notificación de una zona recién creada; la ruta frontend propuesta es `/zonas/:id/tarifas`.
- Salidas: «Guardar» persiste la nueva tarifa vigente y regresa al catálogo; «Cancelar» descarta sin persistir. Guardar sobre una zona inactiva o sin tarifa previa muestra el estado correspondiente [cite: 1].

## 2. Referencias visuales y componentes

| Fuente | Secciones | Aplicación |
|---|---|---|
| [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md) | Formularios, campos numéricos, validación y avisos | Estructura, tokens y pautas del panel. |
| [Diseño F-01](../../disenio/funcionalidades/f-01.md) | Pantalla 3: Formulario de Tarifas de la Zona | Contenido y campos del panel. |
| [Alta fidelidad F-01](../../disenio/SystemDesign/f-01-alta-fidelidad.md) | Panel de tarifas | Presentación de campos y advertencia. |
| [Componentes React](../../disenio/componentes-react.md) | §4.5 y §4.6; CR de formulario y avisos | Contratos de componentes y responsables propuestos. |

La tarifa se expresa sin rangos por tramos: tarifa base, peso incluido y recargo por kilogramo adicional, con factor volumétrico y plazo estimado. Los fragmentos del wireframe que mostraban una «tabla editable de rangos» quedan fuera de alcance [cite: 1, 2].

## 3. Pantallas e interacción

### UI-01. Formulario de Tarifas de la Zona

Composición: estructura administrativa CR-03 → encabezado CR-05 con el nombre de la zona → campos numéricos con validación en línea → aviso de sustitución → acciones «Cancelar» y «Guardar».

| Elemento | Contenido y comportamiento |
|---|---|
| Encabezado | Nombre de la zona y su estado; si la zona está inactiva se advierte que no puede configurarse su tarifa. |
| Tarifa base | Campo numérico obligatorio, no negativo, en `PEN`. |
| Peso incluido | Campo numérico obligatorio, mayor que cero, en kilogramos. |
| Recargo por kg adicional | Campo numérico obligatorio, no negativo, en `PEN`. |
| Factor volumétrico | Campo numérico opcional, mayor que cero, en kg equivalentes por m³. |
| Plazo estimado | Campo numérico obligatorio, entero, en días hábiles. |
| Aviso de sustitución | Si ya existe tarifa vigente, se advierte que la anterior pasará a histórico. |
| Acciones | «Cancelar» descarta; «Guardar» permanece deshabilitado mientras haya campos inválidos. |

| Paso | Acción de la persona | Respuesta de la interfaz | Criterio funcional |
|---|---|---|---|
| 1 | Abrir el panel desde «Tarifas» | Presentar campos con los valores vigentes o vacíos | CA-01, CA-04 |
| 2 | Completar la regla | Habilitar «Guardar» al ser válida | CA-01, CA-02 |
| 3 | Confirmar | Enviar y mostrar el estado de guardado | CA-01, CA-03 |
| 4 | Recibir un rechazo de validación | Marcar los campos inválidos | CA-02 |
| 5 | Recibir un rechazo de permisos | Retirar el panel y sus datos | CA-05 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones disponibles | Criterio |
|---|---|---|---|
| Zona sin tarifa | Campos vacíos con valores por defecto sugeridos | Completar y guardar | CA-01 |
| Zona con tarifa | Campos con los valores vigentes y aviso de sustitución | Modificar y guardar | CA-03 |
| Guardando | Controles deshabilitados y estado de progreso | Esperar | CA-01, CA-03 |
| Error de validación | Mensajes junto a cada campo | Corregir y reintentar | CA-02 |
| Zona inactiva | Aviso de que la zona debe activarse para configurar su tarifa | Volver al catálogo | RN-01 |
| Error de red | Mensaje comprensible sin detalle técnico | «Reintentar» conservando los datos | CA-01 |
| Sin permisos | Acceso denegado sin datos del panel | Navegación permitida por la aplicación | CA-05 |

## 5. Formularios y mensajes

| Control | Obligatorio | Validación y momento | Mensaje visible | Fuente contractual |
|---|---|---|---|---|
| Tarifa base | Sí | Número ≥ 0; en línea y al enviar | «La tarifa base no puede ser negativa» | Gestión §3.1 |
| Peso incluido | Sí | Número > 0 | «El peso incluido debe ser mayor que cero» | Gestión §3.1 |
| Recargo por kg adicional | Sí | Número ≥ 0 | «El recargo no puede ser negativo» | Gestión §3.1 |
| Factor volumétrico | No | Número > 0 si se informa | «El factor debe ser mayor que cero» | Gestión §3.1 |
| Plazo estimado | Sí | Entero de días hábiles | «Informa un plazo en días hábiles» | Gestión §3.1 |
| Moneda | Sí (fija) | `PEN` | Sin edición | Gestión §3.1 |

| Resultado o error de API | Mensaje y comportamiento de UI | Recuperación |
|---|---|---|
| `400` | Marcar los campos inválidos con su mensaje | Corregir y reintentar |
| `404` | Informar que la zona no existe | Volver al catálogo |
| `401` / `403` | Acceso denegado sin datos | Navegación permitida |
| Error de red o `5xx` | Mensaje comprensible con reintento | «Reintentar» conservando los datos |

La equivalencia entre los nombres del contrato y los campos del modelo (`pesoBaseKg`, `plazoMinDias`, `plazoMaxDias`, `activa`) es un pendiente registrado en el plan; no se redefine aquí un payload alternativo [cite: 3].

## 6. Accesibilidad y adaptación

- Teclado y foco: recorrer los campos y acciones con teclado; el foco se sitúa en el primer campo inválido al enviar.
- Etiquetas y avisos: etiquetas asociadas a cada control con su unidad; los errores se anuncian y se asocian al campo.
- Percepción: no depender solo del color para indicar errores; usar texto e iconos.
- Responsive: una columna en móvil y diseño de dos columnas en escritorio según los breakpoints del diseño.

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | Guardar una regla válida para una zona sin tarifa | «Guardar» habilitado y confirmación | CA-01 |
| CUI-02 | Introducir valores negativos o no positivos | Campos marcados y guardado bloqueado | CA-02 |
| CUI-03 | Guardar una nueva regla sobre una zona con tarifa | Aviso de sustitución y confirmación | CA-03 |
| CUI-04 | Abrir el panel de una zona sin tarifa vigente | Campos vacíos con valores sugeridos | CA-04 |
| CUI-05 | Abrir el panel de una zona inactiva | Aviso de activación requerida y guardado bloqueado | RN-01 |
| CUI-06 | Recibir `403` tras abrir el panel | Se retiran panel y datos | CA-05 |
| CUI-07 | Recorrer el panel con teclado en escritorio y móvil | Campos y acciones alcanzables; foco en primer error; responde bien en móvil | CA-01 a CA-05 |

- Pendientes de diseño: nombres y unidades definitivos de los campos (DT-01 del plan).
- Evidencia prevista: pruebas de interacción, revisión con teclado y capturas de los estados aplicables.

## 8. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-05.
2. [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [guía F-01](../../disenio/funcionalidades/f-01.md); [componentes React](../../disenio/componentes-react.md).
3. [Contrato de Gestión, §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas) y [convenciones compartidas, §§3.3 y 3.5](../../integraciones/api-contract.md#3-convenciones-comunes); [modelo de datos](../../arquitectura/modelo-datos.md), tabla `tarifas_zona`.
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
