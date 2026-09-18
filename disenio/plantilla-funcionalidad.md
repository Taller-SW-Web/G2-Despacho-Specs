# Especificación de Interfaz y Wireframes: [Nombre de la Funcionalidad]

**Módulo:** [Nombre del módulo]  
**Responsable:** [Nombre del responsable]  
**Referencia transversal:** Utilizar las pautas de `../lineamientos-wireframes.md`

---

## 1. CONTEXTO GLOBAL Y USUARIO OBJETIVO

- **Rol / Persona:** [Ej. Gestor de Despacho (aplicación web) / Repartidor (aplicación móvil)].
- **Contexto Operativo:** [Describir dónde, cuándo y bajo qué condiciones utilizará esta funcionalidad].
- **Objetivo General:** [Indicar qué necesidad del usuario resuelve la funcionalidad].
- **Plataforma Principal:** [Escritorio / tableta / móvil].
- **Tamaño de Referencia:** [Ej. escritorio de 1440 × 1024 px o móvil de 390 × 844 px].
- **Estructura Común:** [Aplicación administrativa de escritorio / aplicación móvil del repartidor].
- **Tono Visual del Wireframe:** Baja fidelidad, escala de grises, interfaz limpia y sin elementos decorativos.
- **Restricciones Globales:** [Ej. diseño responsivo, accesibilidad, reglas de negocio o limitaciones técnicas relevantes].

> Las funcionalidades F-01, F-02, F-04 y F-05 utilizan la estructura administrativa con barra lateral izquierda, encabezado superior compacto y área principal de contenido. La funcionalidad F-03 utiliza la estructura móvil del repartidor. La navegación debe representarse de forma sencilla; el detalle del wireframe debe concentrarse en el contenido específico de cada pantalla.

---

## 2. FLUJO PRINCIPAL

1. [Primera acción del usuario].
2. [Segunda acción del usuario].
3. [Tercera acción del usuario].
4. [Resultado esperado del flujo].

**Flujos alternativos o excepciones:**

- [Ej. Qué ocurre si no existen resultados].
- [Ej. Qué ocurre si una operación falla].

---

## 3. PANTALLAS Y COMPONENTES (PROMPTS PARA IA)

### Pantalla 1: [Nombre de la vista principal]

**Tipo de interfaz:** [Página completa / modal / panel lateral / otro].  
**Objetivo de la pantalla:** [Describir qué debe lograr el usuario en esta pantalla].

**Estructura y contenido principal:**

- [Indicar cómo se organiza el contenido dentro de la estructura común seleccionada].
- [Describir únicamente los elementos propios de esta pantalla; la navegación global puede mantenerse simplificada].

**Componentes requeridos:**

- [Ej. Encabezado con título de la vista].
- [Ej. Barra de búsqueda].
- [Ej. Filtros].
- [Ej. Tabla, listado, formulario o tarjetas].
- [Ej. Acción principal y acciones secundarias].

**Estados requeridos:**

- [Ej. Estado normal].
- [Ej. Estado de carga].
- [Ej. Estado sin resultados].
- [Ej. Estado de error].
- [Ej. Confirmación de la operación].

**Restricciones específicas:**

- [Ej. El botón principal se deshabilita mientras falten datos obligatorios].
- [Ej. Los registros que requieren atención deben mostrar una advertencia visible].

**Navegación:**

- **Origen:** [Pantalla o acción desde la que se accede].
- **Destino:** [Pantalla a la que conduce la acción principal].

### Pantalla 2: [Nombre de la vista secundaria]

**Tipo de interfaz:** [Página completa / modal / panel lateral / otro].  
**Objetivo de la pantalla:** [Describir qué debe lograr el usuario en esta pantalla].

**Estructura y contenido principal:**

- [Indicar cómo se organiza el contenido dentro de la estructura común seleccionada].
- [Describir únicamente los elementos propios de esta pantalla; la navegación global puede mantenerse simplificada].

**Componentes requeridos:**

- [Componente requerido].
- [Componente requerido].
- [Acción principal y acciones secundarias].

**Estados requeridos:**

- [Estado requerido].
- [Estado requerido].

**Restricciones específicas:**

- [Restricción específica].

**Navegación:**

- **Origen:** [Pantalla o acción desde la que se accede].
- **Destino:** [Pantalla a la que conduce la acción principal].

<!-- Copiar el bloque anterior para agregar las demás pantallas de la funcionalidad. -->

---

## 4. REGISTRO DEL WIREFRAME GENERADO

- **Herramienta utilizada:** [Ej. Figma AI].
- **Fecha de generación:** [YYYY-MM-DD].
- **Nombre de la página o sección en Figma:** [Nombre].
- **Enlace al archivo:** [Agregar enlace].
- **Versión seleccionada:** [Ej. Wireframe v1].
- **Cambios manuales realizados:** [Describir los cambios o indicar “Ninguno”].

---

## 5. EVALUACIÓN HEURÍSTICA DE NIELSEN (REVISIÓN MANUAL EXTERNA)

> Este cuadro no lo genera la IA. Debe ser completado por otro compañero después de navegar y revisar el wireframe generado.

- **Evaluador:** [Nombre del compañero].
- **Fecha:** [YYYY-MM-DD].

| Principio Heurístico | ¿Cumple? (Sí/No) | Observación / Problema Encontrado | Acción de Mejora |
| :--- | :--- | :--- | :--- |
| **1. Visibilidad del estado del sistema** | | | |
| **2. Relación entre el sistema y el mundo real** | | | |
| **3. Control y libertad del usuario** | | | |
| **4. Consistencia y estándares** | | | |
| **5. Prevención de errores** | | | |
| **6. Reconocimiento antes que recuerdo** | | | |
| **7. Flexibilidad y eficiencia de uso** | | | |
| **8. Diseño estético y minimalista** | | | |
| **9. Ayuda para reconocer, diagnosticar y recuperarse de errores** | | | |
| **10. Ayuda y documentación** | | | |
