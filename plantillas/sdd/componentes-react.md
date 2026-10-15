# Plantilla de especificación compartida de componentes React

**Estado:** Plantilla reutilizable del flujo SDD; completar al utilizarla. Los ejemplos no acreditan componentes implementados.

**Responsable:** [por completar].

**Aplicaciones consumidoras:** [Administrativo / Repartidor, según corresponda].

> Utilizar esta plantilla para redactar la especificación compartida antes de implementar los componentes que usarán las pantallas. Ajustar los enlaces al copiarla a `disenio/`. Este documento define comportamiento reutilizable; la apariencia se referencia en el diseño visual.

## 1. Propósito y fuentes

[Definir qué partes de la interfaz se compartirán y qué beneficios de consistencia se esperan. Compartir un componente solo cuando sus responsabilidades y comportamiento sean comunes.]

- Diseño visual: [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md), secciones y revisión [por completar] [cite: 1].
- Especificaciones consumidoras: [enlaces a spec.md y ui.md revisados] [cite: 2].
- Stack frontend: [referencia vigente del proyecto] [cite: 3].

## 2. Catálogo y dependencias

| ID | Componente | Propósito | Consumidores | Depende de | Estado |
|---|---|---|---|---|---|
| CR-01 | [Nombre del componente] | [por completar] | [ES-FXX-NN / aplicación] | [Ninguna / CR-NN] | Propuesto |

Incluir componentes visuales básicos, estructura de navegación o componentes de dominio reutilizados cuando las especificaciones los requieran. Cada aplicación puede necesitar una estructura distinta. No agregar reglas de negocio ni llamadas a APIs a componentes visuales genéricos sin justificar esa responsabilidad.

## 3. Especificación por componente

### CR-01. [Nombre del componente]

- Propósito: [necesidad que resuelve].
- Responsabilidad y límites: [qué hace y qué delega al consumidor].
- Diseño de referencia: [tokens, variantes y enlace al componente o frame de Figma si existe].
- Consumidores: [especificaciones y pantallas].

| Propiedad | Tipo | Obligatoria | Valor por defecto | Comportamiento |
|---|---|---|---|---|
| [por completar] | [por completar] | [Sí / No] | [por completar] | [por completar] |

| Evento | Datos entregados | Cuándo se emite |
|---|---|---|
| [por completar] | [por completar] | [por completar] |

| Variante o estado | Apariencia referenciada | Interacción permitida |
|---|---|---|
| [Normal / deshabilitado / carga / error, según aplique] | [por completar] | [por completar] |

- Contenido y composición: [children, slots o composición prevista].
- Accesibilidad: [semántica, etiquetas, teclado, foco y anuncios necesarios].
- Responsive: [adaptación conforme al diseño compartido].
- Criterio CCR-01: [condición, interacción y resultado observable para verificar el componente].
- Pruebas previstas: [comprobaciones de interacción y accesibilidad aplicables].

Repetir esta sección para cada componente con identificadores únicos. Las propiedades y eventos descritos constituyen el contrato del componente React, no un contrato API adicional.

## 4. Orden de implementación y evidencia

| Incremento | Componentes | Prerrequisitos | Tarea o issue | Evidencia |
|---|---|---|---|---|
| [por completar] | [CR-NN] | [Diseño revisado / componente previo] | [Pendiente] | Pendiente |

Verificar los componentes compartidos necesarios antes de integrar las funcionalidades consumidoras. Registrar dónde quedan sus pruebas, implementación y evidencia; las especificaciones consumidoras enlazan estos resultados en lugar de duplicarlos.

## 5. Decisiones y evolución

| Decisión pendiente o cambio | Consumidores afectados | Responsable | Estado |
|---|---|---|---|
| [por completar] | [por completar] | [por completar] | Pendiente |

Cuando cambien propiedades, eventos o estados, actualizar la especificación y revisar las pantallas consumidoras. Registrar la revisión o commit utilizado en sus planes.

## 6. Referencias

1. [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md): pautas visuales compartidas.
2. [Completar enlaces a las especificaciones consumidoras].
3. [Completar enlace al stack frontend vigente].
