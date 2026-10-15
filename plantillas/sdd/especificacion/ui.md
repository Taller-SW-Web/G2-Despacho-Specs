# UI de ES-FXX-NN: [Nombre del comportamiento]

**Responsable:** [por completar].

**Estado:** Borrador.

**Aplicabilidad:** [Interfaz que se crea o modifica].

**Especificación funcional:** [spec.md](./spec.md).

> Copiar este archivo solo cuando haya interfaz propia o impacto visual en una interfaz existente. Ajustar las referencias al diseño visual y a los componentes compartidos; no duplicar sus definiciones.

## 1. Usuario, contexto y objetivo

- Usuario y permisos: [por completar, según spec.md].
- Contexto de uso: [administración / campo; dispositivo y condiciones relevantes].
- Objetivo visible: [acción que debe poder completar la persona].
- Acceso y navegación: [pantalla de origen, ruta frontend propuesta y destino].

## 2. Referencias visuales y componentes

| Fuente | Referencia | Aplicación |
|---|---|---|
| Diseño visual compartido | [Enlace y sección de SYSTEM-DESIGN.md] | [Tokens, estructura y pautas utilizadas] |
| Diseño de la funcionalidad | [Enlace a documento o frame de Figma, si existe] | [Pantalla o flujo] |
| Componentes React compartidos | [Enlace e identificadores de componentes] | [Propiedades, variantes y eventos utilizados] |

Los componentes exclusivos de este comportamiento se describen aquí. Si un componente se reutiliza en otras especificaciones, proponer su definición en la especificación compartida [cite: 2].

## 3. Pantallas e interacción

### UI-01. [Pantalla, modal o sección]

- Composición: [orden de elementos y componente utilizado para cada uno].
- Datos visibles: [contenido necesario para tomar la decisión].
- Acción principal: [etiqueta, condición de habilitación y resultado].
- Acciones secundarias: [cancelación, regreso u otras acciones].
- Confirmación: [cuándo se solicita y qué informa, si aplica].

| Paso | Acción de la persona | Respuesta de la interfaz | Criterio funcional |
|---|---|---|---|
| 1 | [por completar] | [por completar] | CA-01 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones disponibles | Criterio |
|---|---|---|---|
| Carga inicial | [por completar] | [por completar] | [CA-NN] |
| Con datos | [por completar] | [por completar] | [CA-NN] |
| Vacío o sin resultados | [por completar] | [por completar] | [CA-NN] |
| Envío en curso | [por completar] | [Tratamiento de clics repetidos] | [CA-NN] |
| Éxito | [Confirmación y actualización de datos] | [por completar] | [CA-NN] |
| Error o dependencia no disponible | [Mensaje comprensible] | [Reintentar o corregir, si aplica] | [CA-NN] |
| Sin permisos | [por completar] | [por completar] | [CA-NN] |

Adaptar la tabla a los estados reales; explicar los que no apliquen. La habilitación visual de acciones complementa la autorización obligatoria del backend.

## 5. Formularios y mensajes

| Campo o control | Obligatorio | Validación y momento | Mensaje visible | Fuente contractual |
|---|---|---|---|---|
| [por completar] | [Sí / No] | [por completar] | [por completar] | [Sección del contrato] |

| Resultado o error de API | Mensaje y comportamiento de UI | Recuperación |
|---|---|---|
| [Referencia al contrato] | [por completar] | [por completar] |

Definir cómo se conserva lo ingresado, se evita un envío accidental repetido y se informa un cambio concurrente cuando corresponda. No redefinir aquí el payload ni los códigos del contrato [cite: 3].

## 6. Accesibilidad y adaptación

- Teclado y foco: [orden, foco inicial, retorno de foco y comportamiento del modal si existe].
- Etiquetas y avisos: [nombres accesibles, relación con errores y anuncio de resultados].
- Percepción: [contraste y estados comunicados también con texto o iconos].
- Responsive: [cómo cambia la composición en los tamaños definidos por el diseño compartido].

## 7. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio funcional |
|---|---|---|---|
| CUI-01 | [por completar] | [por completar] | CA-01 |

- Pendientes de diseño: [decisión, responsable y efecto en el plan].
- Evidencia prevista: [pruebas de interacción, revisión con teclado o capturas de estados aplicables].

## 8. Referencias

1. [Especificación funcional](./spec.md): criterios y permisos.
2. [Completar enlaces al diseño visual, diseño de la funcionalidad y componentes React compartidos].
3. [Completar enlace y sección del contrato de API].
4. [Plan](./plan.md) y [evidencia](./evidence.md).
