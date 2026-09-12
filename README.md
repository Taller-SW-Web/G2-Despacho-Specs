# Módulo de Despacho - Documentación Técnica y Especificaciones

Repositorio central de documentación de arquitectura, especificaciones funcionales y contratos de interfaz para el **Módulo de Despacho y Logística de Última Milla**.

El módulo opera como un microservicio autónomo responsable de gestionar el ciclo de vida completo del transporte de paquetes: desde la cotización y recepción de órdenes, asignación a repartidores según capacidad, seguimiento en ruta y captura de evidencias, hasta la resolución de entregas fallidas y notificaciones asíncronas hacia Ventas y Devoluciones.

---

## 1. Distribución Oficial de Funcionalidades e Integrantes

| Integrante | Rol / Componente | Negocio e Independencia Operativa | Enlace a Especificación |
| :--- | :--- | :--- | :--- |
| **Integrante 1: VALQUI** | Gestor de Zonas Geográficas y Cotizador de Envíos | Delimitación de cobertura y matriz de tarifas (peso/volumen/distancia). Expone endpoint de cotización para clientes y carritos de venta. | [F-01-Gestor_ZonasGeograficas.md](specs/funcionalidades/F-01-Gestor_ZonasGeograficas.md) |
| **Integrante 2: NICOLÁS** | Panel de Programación y Asignación de Despachos | Dashboard de cola de pendientes y asignación según capacidad. Incluye endpoint y botón para generar pedidos de prueba de forma autónoma. | [F-02-ProgramacionAsignacionDespachos.md](specs/funcionalidades/F-02-ProgramacionAsignacionDespachos.md) |
| **Integrante 3: MAX ROJAS** | App Móvil del Repartidor y Evidencia de Entrega | PWA móvil para choferes: hoja de ruta, transiciones de estado (`ASIGNADO` $\rightarrow$ `EN_CAMINO` $\rightarrow$ `ENTREGADO`/`FALLIDO`), captura obligatoria de foto y firma. | [F-03-AppMovilRepartidor.md](specs/funcionalidades/F-03-AppMovilRepartidor.md) |
| **Integrante 4** | Portal Web de Tracking de Envíos (Cliente) | Vista pública de solo lectura para el cliente final: buscador por código de rastreo, timeline de hitos y mapa referencial de entrega. | [F-04-PortalTrackingCliente.md](specs/funcionalidades/F-04-PortalTrackingCliente.md) |
| **Integrante 5: GERARDO** | Centro de Entregas Fallidas y Reprogramaciones | Gestión de incidencias en ruta reportadas por choferes. Reprogramación de nueva fecha o derivación a devolución a almacén (coordina con Devoluciones). | [F-05-GestionEntregasFallidas.md](specs/funcionalidades/F-05-GestionEntregasFallidas.md) |
| **Integrante 6: RHAMSES** | Panel de Monitoreo de Flota, Operadores y Capacidad Diaria | CRUD de choferes y vehículos, control de turnos y límites de carga. Expone `GET /api/v1/repartidores/disponibles` consumido por el Integrante 2. | [F-06-MonitoreoFlotaCapacidad.md](specs/funcionalidades/F-06-MonitoreoFlotaCapacidad.md) |

---

## 2. Acuerdos Transversales (DevOps, Seguridad y Despliegue)

- **Seguridad y JWT:** Cada integrante protege sus endpoints en el backend inyectando la configuración común de validación de tokens JWT y autorización basada en roles (`GESTOR_DESPACHO`, `GESTOR_FLOTA`, `REPARTIDOR`, `ADMIN`).
- **Integración Asíncrona / Webhooks:** Notificación a módulos externos (Ventas y Devoluciones) al producirse entregas efectivas o devoluciones a almacén mediante un servicio común reutilizable de emisión de eventos.
- **Despliegue Continuo en la Nube:** Un integrante actúa como líder de despliegue configurando la vinculación inicial del repositorio con las plataformas en la nube (Render para el backend y Vercel para el frontend), desplegándose automáticamente el código integrado del equipo.

---

## 3. Stack Tecnológico Unificado

| Capa | Tecnologías Clave | Propósito / Alcance |
| :--- | :--- | :--- |
| **Backend** | **Java 21 (LTS)**, **Spring Boot 3.3.x**, **Maven** | Microservicio REST autónomo, Spring Data JPA / Hibernate, Spring Security (JWT), Lombok, JUnit 5 + Mockito. |
| **Frontend** | **React 18/19**, **Vite**, **Tailwind CSS** | SPA administrativa y PWA móvil para repartidor (`react-router-dom`, `@tanstack/react-query`, `axios`, `leaflet`, `vite-plugin-pwa`, `react-signature-canvas`). |
| **Base de Datos** | **PostgreSQL (v15/v16)** en **Supabase** | Persistencia relacional en la nube con *Connection Pooling* (Supavisor) y extensión `PostGIS` para coordenadas geográficas. |
| **Mensajería / Eventos** | **Webhooks asíncronos (`@Async`)** / **RabbitMQ** | Emisión asíncrona desacoplada hacia Ventas y Devoluciones (`IEventoPublisher`), extensible a broker AMQP. |

---

## 4. Guía de Navegación del Repositorio

La documentación se organiza bajo los lineamientos de [AGENTS.md](AGENTS.md):

- **[CONTRIBUTING.md](CONTRIBUTING.md):** Guía de trabajo colaborativo, nomenclatura de ramas, conventional commits y reglas de Pull Requests.
- **[specs/overview.md](specs/overview.md):** Visión general de arquitectura, interacción de los 6 integrantes, máquina de estados y detalle del stack tecnológico.
- **[specs/modelo-datos.md](specs/modelo-datos.md):** Estructura base del modelo relacional para PostgreSQL en Supabase.
- **[specs/funcionalidad.md](specs/funcionalidad.md):** Matriz e inventario de seguimiento de todas las especificaciones funcionales.
- **[specs/api-contract.md](specs/api-contract.md):** **Contrato único de comunicación** entre frontend y backend (todos los endpoints de las 6 funcionalidades, esquemas JSON y códigos de error).
- **`specs/funcionalidades/`:** Carpeta con los archivos de especificación detallados con escenarios en formato Gherkin.

---

## 5. Repositorios del Proyecto

- **Documentación:** `despacho-docs` (este repositorio)
- **Backend (Spring Boot / Java):** `despacho-backend`
- **Frontend (Web & PWA):** `despacho-frontend`