# Stack de dependencias: frontend

**Responsable:** Rhamses, con revisión de Max.
**Estado:** Conciliado con el monorepositorio y SYSTEM-DESIGN.md §15 el 16/10/2026; revisado contra `develop` `1bc5458` el 27/11/2026. Las fuentes ejecutables siguen siendo los `package.json` y el lockfile del repositorio frontend.

## 1. Organización y gestor

El frontend usa npm workspaces: dos aplicaciones (`apps/despacho-administrativo` y `apps/despacho-repartidor`) y tres paquetes compartidos. La fuente ejecutable de dependencias son sus `package.json`; `package-lock.json` fija la resolución reproducible. No copiar un manifiesto paralelo desde esta guía [cite: 1].

Requisitos declarados: Node.js >=20 y npm >=10. Desde la raíz de `despacho-frontend`:

```bash
npm ci
npm run dev:administrativo
npm run dev:repartidor
```

## 2. Stack y dependencias existentes

| Recurso | Versión declarada | Uso |
|---|---|---|
| React y React DOM | ^19.2.0 | Interfaz de las dos aplicaciones |
| TypeScript | ^5.0.0 | Tipado y comprobación estática |
| Vite | ^5.4.0 | Desarrollo y construcción |
| Plugin React de Vite | ^4.3.0 | Transformación de JSX |
| Mantine core, hooks, dates y notifications | 9.6.2 | Controles, fechas y proveedor de notificaciones |
| Tabler Icons React | ^3.0.0 | Iconos de la guía |
| React Router DOM | ^6.26.0 | Navegación |
| Axios | ^1.7.0 | Transporte desde cliente-api |
| React Hook Form | ^7.53.0 | Formularios |
| Zod y resolvers | ^4.6.7 / ^5.0.0 | Validación |
| Day.js | ^1.11.0 | Fechas de presentación |
| JWT Decode | ^4.0.0 | Utilidad declarada; no concede permisos |
| Zustand | ^4.5.0 | Dependencia existente; no obliga a crear otro almacén |
| TanStack React Table | ^8.20.0 | Dependencia administrativa para tablas |

No se incorporan dependencias nuevas ni se actualizan versiones en esta conciliación. Tailwind, react-hot-toast y Recharts del borrador anterior no forman parte de la base actual. Mantine sustituye las propuestas visuales anteriores [cite: 1, 2].

## 3. Estilos y componentes compartidos

Ampliación F-01 del 14/11/2026: Administración incorpora Leaflet 1.9.x, React Leaflet 5 y tipos GeoJSON/Leaflet, con carga diferida, CSS Modules y Mantine. El proveedor de teselas y su atribución se configuran mediante variables públicas. Resolución exacta en el lockfile del frontend.

Ambas aplicaciones importan el tema `tema` y `tokens.css` de `@despacho/componentes-compartidos`. Inter se utiliza en cuerpo y controles y Oswald 700 en H1–H3. Los estilos propios usan CSS Modules y variables del tema. Los breakpoints se ajustan al diseño: 576, 768, 992, 1200 y 1408 px [cite: 2].

Cada aplicación mantiene un `MantineProvider` y un `Notifications`; CR-15 adapta ese proveedor existente. No se crea un segundo sistema de notificaciones. Los componentes visuales reciben datos, permisos resueltos y callbacks del consumidor [cite: 3].

## 4. Herramientas y comprobaciones

Vitest ^3.2.0, JSDOM ^26.1.0, Testing Library React ^16.3.0, DOM ^10.4.0, jest-dom ^6.6.3, user-event ^14.6.1 y Playwright ^1.64.1 están declarados para las pruebas. JSDOM comprueba comportamiento del DOM; el layout y los recorridos requieren navegador. CI usa Node 22 para construir y probar ambas aplicaciones; Node >=20 es el requisito mínimo declarado.

```bash
npm test
npm run test:f04
npm run typecheck
npm run build
```

La evidencia de implementación y los resultados reales se mantienen en `despacho-frontend/docs/componentes/`; esta guía no certifica por sí sola que los componentes ni sus consumidores estén completos.

## 5. Configuración y despliegue

Cada aplicación mantiene su configuración de Vite y Vercel. Los servidores locales usan 5173 y 5174. `VITE_API_BASE_URL` identifica el origen público del Gateway, sin `/api/v1` al final; las variables `VITE_*` se exponen al navegador y no contienen secretos. Consultar los `.env.example` existentes y la guía frontend [cite: 1].

La autenticación está implementada como adaptador compartido de login, OTP, renovación, cierre y perfil, con la sesión normal en memoria y renovación programada antes del vencimiento. Administración exige `GESTOR_DESPACHO` y la aplicación del repartidor resuelve su perfil local por `sub`. Esto no acredita la integración con el proveedor G7 publicado: coexisten el HTTP normal contra el origen configurado, el desarrollo local con Seguridad temporal y el modo demo sin backend. El API de negocio se consume por HTTP con un timeout de 15 segundos y una sola repetición ante rechazos explícitos del filtro JWT; no hay reintento indiscriminado de mutaciones.

El estado de las pantallas se refresca con consultas periódicas de 30 segundos y al recuperar visibilidad, o con actualización manual; no hay cliente WebSocket, SSE ni STOMP. La PWA guarda la interfaz, no respuestas de negocio ni comandos offline. RabbitMQ comunica los microservicios directamente y no entrega eventos al navegador [cite: 4].

La marca inversa debe provenir del activo autorizado de Figma; el fallback textual no acredita su aprobación visual.

## 6. Referencias

- [cite: 1] Manifiestos, lockfile, configuraciones y README del repositorio hermano `../despacho-frontend`.
- [cite: 2] [Sistema de diseño](../disenio/SYSTEM-DESIGN.md), §§6, 15 y 17.
- [cite: 3] [Componentes React](../disenio/componentes-react.md), §§1.3–1.5 y 4.5.1.
- [cite: 4] [Frontend `develop`, commit `1bc5458`](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/tree/1bc5458115ed8caf48327a06926d2700d62f468c) y [contrato externo §3.6](../integraciones/api-contract.md#36-mensajería-interna-con-rabbitmq).
