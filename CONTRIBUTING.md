# Guía de Contribución y Flujo de Trabajo del Equipo

Este documento establece los acuerdos de colaboración, estrategia de ramas en Git, convenciones de commits y procesos de revisión de código (*Pull Requests*) para el equipo de desarrollo del **Módulo de Despacho**.

---

## 1. Estrategia de Ramas en Git

Para asegurar que los 6 integrantes puedan trabajar de forma simultánea sin generar conflictos de integración:

### 1.1 Rama Principal (`main`)

- Contiene el código fuente y la documentación estable, probada y lista para despliegue en la nube (Render para backend y Vercel para frontend).
- **Protección:** No se permite realizar *push* directo a `main`. Todo cambio debe ingresar mediante un *Pull Request* (PR).

### 1.2 Rama de integración (`develop`)

- En los repositorios de backend y frontend, `develop` reúne los cambios de trabajo antes de una entrega. Las ramas de funcionalidad, corrección y configuración parten de `develop` y regresan mediante PR.
- No realizar *push* directo a `develop`. Exigir la revisión de otro compañero y las comprobaciones de CI configuradas para cada repositorio.
- La promoción de una entrega se hace mediante un PR de `develop` a `main`; `main` puede quedar detrás mientras se integran los cambios de la siguiente entrega.
- Este repositorio de especificaciones mantiene actualmente `main` como base documental, sin una rama `develop`. Las ramas documentales parten de `main` y vuelven a ella por PR. Esta diferencia no cambia el flujo de integración del código.

### 1.3 Nomenclatura de Ramas de Trabajo

Cada integrante crea una rama desde la base correspondiente a su repositorio siguiendo la nomenclatura oficial. Usar nombres significativos, sin el prefijo `codex/`:

| Tipo de Rama | Formato de Nombre | Ejemplo |
| :--- | :--- | :--- |
| **Funcionalidad (Feature)** | `feature/f<XX>-<descripcion-corta>` | `feature/f01-zonas-cotizador`<br>`feature/f02-programacion-asignacion`<br>`feature/f03-app-movil-repartidor`<br>`feature/f04-entregas-fallidas`<br>`feature/f05-monitoreo-flota` |
| **Corrección de Error (Bugfix)** | `fix/<descripcion-corta>` | `fix/validacion-capacidad-peso`<br>`fix/compresion-foto-pwa` |
| **Documentación (Docs)** | `docs/<descripcion-corta>` | `docs/actualizar-api-contract` |
| **Configuración y mantenimiento (Chore)** | `chore/<descripcion-corta>` | `chore/ci-y-versionado-backend` |

---

## 2. Convención de Mensajes de Commit (Conventional Commits)

Todos los mensajes de commit deben redactarse **en español** y utilizar el estándar de *Conventional Commits*:

### 2.1 Estructura del Mensaje
```text
<tipo>(<alcance>): <descripción concisa en minúsculas>
```

### 2.2 Tipos Permitidos
- **`feat`**: Nueva funcionalidad para el usuario o sistema (ej. `feat(f02): implementar endpoint para generar pedidos de prueba`).
- **`fix`**: Corrección de un error o falla funcional (ej. `fix(f06): corregir calculo de capacidad remanente en repartidores`).
- **`docs`**: Modificaciones en documentación o contratos (ej. `docs(f03): documentar schemas json en api-contract`).
- **`refactor`**: Cambios de código que no corrigen errores ni añaden funcionalidades (ej. `refactor(seguridad): modularizar filtro jwt`).
- **`test`**: Añadir o corregir pruebas unitarias o de integración (ej. `test(f05): agregar pruebas mockito para límite de reintentos`).
- **`chore`**: Tareas auxiliares, actualización de dependencias o configuración de build (ej. `chore: configurar dependencias de react query en vite`).

---

## 3. Ciclo de Trabajo Diario del Desarrollador

En los repositorios de código, usar `develop` como base:

1. **Sincronización inicial:**

   ```bash
   git switch develop
   git pull --ff-only origin develop
   ```

2. **Crear o retomar rama de trabajo:**

   ```bash
   git switch -c feature/f02-programacion-asignacion
   ```

3. **Desarrollar y probar localmente:** En el backend, ejecutar Maven Wrapper con `clean verify` dentro de cada servicio afectado; incluye las pruebas unitarias y las integraciones existentes con bases temporales. En el frontend, ejecutar los comandos de pruebas y construcción indicados en su README. No apuntar las pruebas a bases compartidas.
4. **Sincronizar cambios de develop antes de publicar:**

   ```bash
   git switch develop
   git pull --ff-only origin develop
   git switch feature/f02-programacion-asignacion
   git merge develop
   ```

5. **Publicar rama y abrir Pull Request hacia develop:**

   ```bash
   git push origin feature/f02-programacion-asignacion
   ```

Para cambios de este repositorio documental, el mismo proceso utiliza `main` en lugar de `develop` y una rama como `docs/actualizar-api-contract`. Las comprobaciones son las que correspondan a los documentos modificados; no se atribuyen resultados de pruebas de código a una revisión documental.

### 3.1 Entregas y versiones

- Revisar el corte de entrega aproximadamente cada dos semanas, sin que esa cadencia requiera adoptar Scrum ni obligue a publicar una versión sin cambios.
- Actualizar `CHANGELOG.md` únicamente al preparar y publicar una nueva línea base en `main`. No añadir entradas por especificación durante el desarrollo; el avance se registra en commits y en los documentos SDD. El README conserva las instrucciones de ejecución.
- Al preparar esa línea base, consolidar los cambios entregados con su versión y fecha, verificar el alcance y abrir el PR de `develop` a `main`. El changelog viaja con ese PR; no se actualiza mediante *push* directo a `main`.
- Usar `0.x.y` durante el desarrollo inicial. La primera línea base de código se identifica como `0.1.0`; las versiones siguientes dependen de los cambios entregados, no del número de hito.
- Crear manualmente el tag sobre el commit aprobado de `main`, sin mover tags de entregas anteriores. No se requiere crear una GitHub Release.

---

## 4. Reglas para Pull Requests (PR) y Code Review

Antes de solicitar la aprobación de un Pull Request:

- [ ] **Contrato por ámbito:** Si se modificaron o crearon endpoints, documentarlos una sola vez en el contrato correspondiente de `integraciones/`: `api-contract.md` para módulos externos, `api-contract-gestion-despachos.md` para Gestión o `api-contract-operacion-reparto.md` para Operación. Actualizar enlaces y anclas; no duplicar payloads entre contratos.
- [ ] **Matriz de Funcionalidades:** Actualizar el estado correspondiente en `funcionalidades/funcionalidad.md` si la tarea representa un cambio de fase.
- [ ] **Calidad de Código:** El proyecto debe compilar y superar las pruebas unitarias y de integración existentes que le correspondan. No omitir pruebas fallidas para obtener un CI aprobado.
- [ ] **Revisión por Pares:** Al menos 1 compañero de equipo debe revisar y aprobar el PR antes del merge a `develop` o `main`.
- [ ] **Comprobaciones de GitHub:** Las comprobaciones configuradas como obligatorias deben aprobarse y las conversaciones de revisión deben quedar resueltas. El workflow de CI y la protección de ramas se configuran por separado.
- [ ] **Historial claro:** Mantener commits y PR acotados, con mensajes en español. Puede usarse *Squash and Merge* para ramas de trabajo; al promover `develop` a `main`, conservar una estrategia que permita continuar integrando ambas ramas sin reescribir su historial.
