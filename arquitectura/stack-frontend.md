# Stack de Dependencias: Frontend

**Responsable de definición:** Rhamses
**Estado:** Definido
**Aplica a:** Repositorio frontend del Módulo de Despacho y Entrega a Domicilio

---

## 1. Gestor de dependencias

El frontend usa **npm** y un archivo `package.json` como gestor de dependencias. **Maven no aplica al frontend**; Maven es exclusivo del backend Java.

Para instalar todas las dependencias del proyecto basta ejecutar:

```bash
npm install
```

---

## 2. Stack base

| Herramienta | Versión mínima | Propósito |
|---|---|---|
| Node.js | 20.x LTS | Entorno de ejecución para desarrollo local |
| npm | 10.x | Gestor de paquetes |
| React | 18.3.x | Biblioteca principal de interfaz de usuario |
| Vite | 5.x | Servidor de desarrollo y bundler de producción |

---

## 3. Dependencias de producción

Estas dependencias se incluyen en el bundle final que se despliega en **Vercel**.

### 3.1. Enrutamiento

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `react-router-dom` | ^6.26.0 | Navegación entre páginas y rutas protegidas | Todas (F-01 a F-05) |

### 3.2. Peticiones HTTP

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `axios` | ^1.7.0 | Llamadas al backend REST y manejo de interceptores JWT | Todas (F-01 a F-05) |

### 3.3. Estilos y componentes visuales

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `tailwindcss` | ^3.4.0 | Sistema de diseño por clases utilitarias | Todas |
| `@tailwindcss/forms` | ^0.5.7 | Estilos base para inputs, selects y checkboxes | Formularios en general |

### 3.4. Gráficos y dashboard

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `recharts` | ^2.12.0 | Barras de progreso de saturación, tarjetas de resumen y gráficos del panel de monitoreo | **F-05** (panel de flota) |

### 3.5. Tablas con filtros y paginación

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `@tanstack/react-table` | ^8.20.0 | Listados paginados y filtrables de repartidores, vehículos y despachos | **F-02, F-05** |

### 3.6. Formularios y validación

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `react-hook-form` | ^7.53.0 | Gestión de formularios con bajo re-render | Todos los formularios |
| `zod` | ^3.23.0 | Esquemas de validación (DNI obligatorio, peso > 0, fechas futuras, etc.) | Todos los formularios |
| `@hookform/resolvers` | ^3.9.0 | Conector entre react-hook-form y Zod | Todos los formularios |

### 3.7. Notificaciones y feedback

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `react-hot-toast` | ^2.4.0 | Mensajes de éxito, error y advertencia | Todas |

### 3.8. Autenticación y sesión

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `jwt-decode` | ^4.0.0 | Decodificación del token JWT para leer el rol y la expiración en el cliente | Todas (rutas protegidas) |

### 3.9. Estado global

| Paquete | Versión | Uso principal | Funcionalidades que lo usan |
|---|---|---|---|
| `zustand` | ^4.5.0 | Almacén global liviano para sesión del usuario y datos compartidos entre componentes | Todas |

---

## 4. Dependencias de desarrollo

Estas dependencias solo se usan en desarrollo local y no forman parte del bundle de producción.

| Paquete | Versión | Propósito |
|---|---|---|
| `vite` | ^5.x | Servidor de desarrollo con hot reload y build de producción |
| `@vitejs/plugin-react` | ^4.x | Plugin de Vite para soporte de JSX y Fast Refresh |
| `postcss` | ^8.4.0 | Procesador CSS requerido por Tailwind |
| `autoprefixer` | ^10.4.0 | Agrega prefijos CSS para compatibilidad con navegadores |
| `vitest` | ^1.6.0 | Framework de pruebas unitarias compatible con Vite |
| `@testing-library/react` | ^14.3.0 | Utilidades para renderizar y testear componentes React |
| `@testing-library/jest-dom` | ^6.4.0 | Matchers adicionales para assertions sobre el DOM |
| `@testing-library/user-event` | ^14.5.0 | Simulación de interacciones del usuario en pruebas |

---

## 5. Archivo `package.json` de referencia

```json
{
  "name": "despacho-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.26.0",
    "axios": "^1.7.0",
    "recharts": "^2.12.0",
    "@tanstack/react-table": "^8.20.0",
    "react-hook-form": "^7.53.0",
    "zod": "^3.23.0",
    "@hookform/resolvers": "^3.9.0",
    "react-hot-toast": "^2.4.0",
    "jwt-decode": "^4.0.0",
    "zustand": "^4.5.0"
  },
  "devDependencies": {
    "vite": "^5.4.0",
    "@vitejs/plugin-react": "^4.3.0",
    "tailwindcss": "^3.4.0",
    "@tailwindcss/forms": "^0.5.7",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "vitest": "^1.6.0",
    "@testing-library/react": "^14.3.0",
    "@testing-library/jest-dom": "^6.4.0",
    "@testing-library/user-event": "^14.5.0"
  }
}
```

---

## 6. Despliegue

El frontend se despliega en **Vercel**. El archivo `vite.config.js` debe configurar la variable de entorno `VITE_API_BASE_URL` para apuntar al backend desplegado en Render.

```js
// vite.config.js (referencial)
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

```env
# .env.production
VITE_API_BASE_URL=https://despacho-backend.onrender.com
```

---

## 7. Notas

- Las versiones exactas se fijarán cuando se cree el repositorio de frontend ejecutando `npm install` y commiteando el `package-lock.json`.
- No agregar dependencias nuevas sin coordinarlo con el equipo, para evitar conflictos entre ramas.
- El diseño de interfaces usa **Figma** (a cargo de Valqui) como referencia antes de implementar en código.
