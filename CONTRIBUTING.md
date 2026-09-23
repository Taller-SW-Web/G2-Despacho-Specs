# Guía de Contribución y Flujo de Trabajo del Equipo

Este documento establece los acuerdos de colaboración, estrategia de ramas en Git, convenciones de commits y procesos de revisión de código (*Pull Requests*) para el equipo de desarrollo del **Módulo de Despacho**.

---

## 1. Estrategia de Ramas en Git

Para asegurar que los 5 integrantes puedan trabajar de forma simultánea sin generar conflictos de integración:

### 1.1 Rama Principal (`main`)
- Contiene el código fuente y la documentación estable, probada y lista para despliegue en la nube (Render para backend y Vercel para frontend).
- **Protección:** No se permite realizar *push* directo a `main`. Todo cambio debe ingresar mediante un *Pull Request* (PR).

### 1.2 Nomenclatura de Ramas de Trabajo
Cada integrante crea una rama derivada de `main` siguiendo la nomenclatura oficial:

| Tipo de Rama | Formato de Nombre | Ejemplo |
| :--- | :--- | :--- |
| **Funcionalidad (Feature)** | `feature/f<XX>-<descripcion-corta>` | `feature/f01-zonas-cotizador`<br>`feature/f02-programacion-asignacion`<br>`feature/f03-app-movil-repartidor`<br>`feature/f04-entregas-fallidas`<br>`feature/f05-monitoreo-flota` |
| **Corrección de Error (Bugfix)** | `fix/<descripcion-corta>` | `fix/validacion-capacidad-peso`<br>`fix/compresion-foto-pwa` |
| **Documentación (Docs)** | `docs/<descripcion-corta>` | `docs/actualizar-api-contract` |

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

1. **Sincronización inicial:**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Crear o retomar rama de trabajo:**
   ```bash
   git checkout -b feature/f02-programacion-asignacion
   ```
3. **Desarrollar y probar localmente:** Ejecutar pruebas unitarias (`mvn test` o `npm test`).
4. **Sincronizar cambios de main antes de publicar:**
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/f02-programacion-asignacion
   git merge main
   ```
5. **Publicar rama y abrir Pull Request:**
   ```bash
   git push origin feature/f02-programacion-asignacion
   ```

---

## 4. Reglas para Pull Requests (PR) y Code Review

Antes de solicitar la aprobación de un Pull Request:
- [ ] **Contrato Único:** Si se modificaron o crearon endpoints, verificar que estén debidamente documentados en `integraciones/api-contract.md`.
- [ ] **Matriz de Funcionalidades:** Actualizar el estado correspondiente en `funcionalidades/funcionalidad.md` si la tarea representa un cambio de fase.
- [ ] **Calidad de Código:** El proyecto debe compilar sin errores y superar las pruebas unitarias existentes.
- [ ] **Revisión por Pares:** Al menos 1 compañero de equipo debe revisar y aprobar el PR antes del merge a `main`.
- [ ] **Sin Merge Commits Sucios:** Preferir *Squash and Merge* o *Rebase* para mantener un historial lineal y limpio en `main`.
