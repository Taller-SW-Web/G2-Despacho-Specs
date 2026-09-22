# Reglas de mantenimiento del repositorio

## 1. Convención de nombres en Java

### 1.1 Clases y enums
- **Clases, enums y registros**: `PascalCase` (ej. `GestorZonasGeograficas`, `EstadoDespacho`).
- **Nombres de enums**: mayúsculas con guion bajo para los valores (ej. `PENDIENTE_ASIGNACION`, `FALLIDO`, `DEVUELTO_A_ALMACEN`).

### 1.2 Métodos
- **Métodos**: `camelCase` (ej. `obtenerDespachoPorId`, `validarReintentos`, `notificarModuloVentas`).
- Usar verbos o frases verbales que describan la acción (obtener, validar, crear, eliminar, notificar).

### 1.3 Variables y parámetros
- **Variables locales y parámetros**: `camelCase` (ej. `idDespacho`, `fechaEntrega`, `maximoReintentos`).
- **Constantes**: `UPPER_SNAKE_CASE` (ej. `MAXIMO_REINTENTOS`, `RUTA_API_VENTAS`).

### 1.4 Paquetes (packages)
- **Paquetes**: todo en minúsculas, separados por puntos (ej. `com.modulodespacho.gestionentregas`, `com.modulodespacho.api`).

### 1.5 Archivos Java
- Cada archivo contiene **una sola clase pública** cuyo nombre coincide con el nombre del archivo (ej. `GestorZonasGeograficas.java`).
- Los archivos de interfaces llevan prefijo `I` o terminan en `Interface` según el patrón del proyecto (ej. `IDespachoRepository.java` o `DespachoRepository.java`).

### 1.6 Nombres de archivos fuente
- Formato: `NombreClase.java` en su paquete correspondiente.
- Ejemplos: `GestorZonasGeograficas.java`, `EstadoDespacho.java`, `EntregaFallidaService.java`.

---

## 2. Idioma del código y documentación

### 2.1 Código fuente (Java)
- Todo el código escrito por el equipo debe estar **en español**: nombres de clases, métodos, variables, comentarios, javadoc, mensajes de error y log.
- **Excepciones** (permite inglés): nombres de librerías, frameworks, anotaciones (`@Service`, `@RestController`), nombres de tipos de la JDK, nombres de paquetes de terceros y palabras técnicas universalmente adoptadas (id, api, web, token, json, http, sql).

### 2.2 Documentación (Markdown)
- Todo el contenido de especificaciones, descripciones y textos en Markdown debe estar **en español**.
- Los términos técnicos ampliamente adoptados en inglés pueden conservarse (ej. microservicios, backend, frontend, webhook, JWT).

---

## 3. Formato correcto de Markdown

### 3.1 Estructura general
- Cada archivo Markdown comienza con **un solo título H1** (`# Título`).
- Usar encabezados jerárquicos en orden: `##` antes de `###`, sin saltar niveles.
- Dejar **una línea en blanco** entre párrafos, listas y bloques de código.

### 3.2 Listas
- Listas con guion `-` para elementos sin orden, o con números `1.` para pasos/secuencias.
- Sangría de 2 espacios para sub-listas.

### 3.3 Código
- Usar bloques de código con triple acento grave (```) y especificar el lenguaje cuando sea posible (```java, ```json).
- Valores enum, nombres de estado y rutas se escriben en `backticks`.

### 3.4 Referencias
- Citar fuentes o documentos usando la notación `[cite: N]` para trazabilidad.

### 3.5 Formato de especificaciones funcionales
- Cada especificación funcional sigue la plantilla establecida en `funcionalidades/F-04-GestionEntregasFallidas.md` con las secciones:
  1. Contexto
  2. Propósito
  3. Alcance
  4. Precondiciones, dependencias y resultados
  5. Requisitos y criterios de aceptación automatizables (con escenarios en formato Gherkin: DADO/CUANDO/ENTONCES)
  6. Frontend
  7. Backend
  8. Requisitos no funcionales
  9. Fuera de alcance
  10. Estrategia de verificación
  11. Criterio de completitud

### 3.6 Nombres de archivos de especificaciones
- Formato: `F-XX-NombreEnPascalCase.md` (ej. `F-01-Gestor_ZonasGeograficas.md`, `F-02-ProgramacionAsignacionDespachos.md`, `F-04-GestionEntregasFallidas.md`).

### 3.7 Especificaciones atómicas
- Las especificaciones derivadas de las funcionalidades se guardan juntas en `especificaciones/`, sin subcarpetas por funcionalidad.
- Cada archivo describe un único comportamiento concreto, implementable y verificable.
- Se usa como base `especificaciones/PLANTILLA-ESPECIFICACION.md`.
- El nombre sigue el formato `ES-FXX-NN-NombreEnPascalCase.md` (ej. `ES-F04-01-ConfirmarRecepcionPaquete.md`).
- La especificación referencia su funcionalidad padre y el contrato de API; no duplica el contenido completo de esos documentos.

---

## 4. Actualización del índice

### 4.1 Archivos índice
- `README.md`: índice principal del repositorio. Debe contener la descripción general, links a specs y guía de navegación.
- `funcionalidades/funcionalidad.md`: índice de todas las especificaciones funcionales. Debe contener una tabla con: ID, nombre, descripción breve, responsable y estado.

### 4.2 Regla de actualización
- **Toda vez que se cree, renombre o elimine** un archivo de especificación funcional dentro de `funcionalidades/`, se debe actualizar el índice en `funcionalidades/funcionalidad.md`.
- Toda vez que se agregue una sección relevante al repositorio, se debe actualizar `README.md`.
- No se permite agregar archivos de especificación sin actualizar el índice correspondiente.
- Toda vez que se cree, renombre o elimine una especificación atómica en `especificaciones/`, se debe actualizar su trazabilidad en `funcionalidades/funcionalidad.md`.

---

## 5. Prohibición de duplicar contratos

### 5.1 Un solo contrato por funcionalidad
- Cada funcionalidad del sistema tiene **un único archivo de especificación funcional** en `funcionalidades/`.
- Está **prohibido** crear dos o más archivos que describan la misma funcionalidad con diferente nombre o en diferente ubicación.
- Las especificaciones atómicas de `especificaciones/` detallan casos de uso de la funcionalidad padre y no la reemplazan ni repiten su alcance general.

### 5.2 Reutilización en lugar de duplicación
- Si una funcionalidad es compartida entre módulos, se referencia el archivo original usando `[cite: N]` en vez de copiar el contenido.
- Si existe duda sobre si una funcionalidad ya fue documentada, **consultar el índice** (`funcionalidades/funcionalidad.md`) antes de crear un nuevo archivo.

### 5.3 Contrato único de comunicación
- El archivo `integraciones/api-contract.md` es el **único** contrato de comunicación entre frontend y backend. No se crearán contratos adicionales fuera de este archivo.
