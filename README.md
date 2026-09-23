# Módulo de Despacho y Entrega a Domicilio

> Documentación y especificaciones del módulo responsable de organizar, ejecutar y dar seguimiento al proceso de despacho y entrega de pedidos.

**Estado del proyecto:** En especificación y diseño inicial  
**Arquitectura prevista:** Sistema modular integrado mediante APIs  
**Repositorio:** Documentación funcional y técnica

---

## 📦 Acerca del módulo

El **Módulo de Despacho y Entrega a Domicilio** administra el ciclo operativo que comienza cuando un pedido está listo para ser despachado y termina con su entrega, reprogramación o devolución.

El módulo es responsable de la entidad **despacho** y mantiene sus propios datos. La información perteneciente a pedidos, productos y usuarios se obtiene mediante las APIs de los módulos propietarios, sin acceder directamente a sus bases de datos.

Este repositorio centraliza las especificaciones funcionales, decisiones generales y contratos necesarios para que el frontend, el backend y los demás módulos puedan desarrollarse de manera coordinada.

## 🎯 Capacidades principales

| ID | Área funcional | Descripción |
|---|---|---|
| **F-01** | Zonas geográficas y cotización | Administra zonas de cobertura y calcula tarifas de entrega según las reglas definidas. |
| **F-02** | Programación y asignación | Organiza los despachos pendientes y permite asignarlos a repartidores o rutas disponibles. |
| **F-03** | Operación del repartidor | Ofrece una web responsive para consultar entregas, actualizar estados y registrar evidencias. |
| **F-04** | Entregas fallidas y reprogramaciones | Gestiona incidencias, nuevos intentos de entrega y devoluciones a almacén. |
| **F-05** | Flota, operadores y capacidad | Administra repartidores, vehículos, turnos, disponibilidad y capacidad diaria. |

### Seguimiento de pedidos

El módulo expondrá información de seguimiento mediante API para que los canales autorizados consulten el estado de un despacho. Esta capacidad es transversal y no constituye un área funcional independiente.

Los requisitos, escenarios y criterios de aceptación de cada capacidad se desarrollan en sus respectivas especificaciones.

## 🧭 Mapa de documentación

| Documento | Contenido |
|---|---|
| [Visión general](./overview.md) | Problema, objetivos, alcance, actores y flujo general del módulo. |
| [Índice de funcionalidades](./funcionalidades/funcionalidad.md) | Listado y estado de las especificaciones funcionales. |
| [Contrato de API](./integraciones/api-contract.md) | Convenciones, autenticación, errores y organización de las APIs. |
| [Modelo de datos](./arquitectura/modelo-datos.md) | Base evolutiva de entidades, relaciones y decisiones de persistencia. |
| [Especificaciones funcionales](./funcionalidades/) | Requisitos, escenarios y criterios de completitud por funcionalidad. |
| [Especificaciones atómicas](./especificaciones/) | Casos de uso concretos derivados de las funcionalidades y su plantilla común. |
| [Historias de usuario](./historias-usuario/) | Historias en formato Jira (COMO/QUIERO/PARA) con criterios de aceptación Gherkin y DoD. |
| [Reglas del repositorio](./AGENTS.md) | Convenciones para crear y mantener la documentación. |
| [Guía de contribución](./CONTRIBUTING.md) | Flujo de ramas, commits y revisión de cambios. |

## 🗂️ Repositorios del módulo

El módulo se divide en repositorios independientes que comparten las especificaciones de este proyecto.

| Repositorio | Propósito | Estado |
|---|---|---|
| [despacho-docs](https://github.com/Taller-SW-Web/despacho-docs) | Documentación, especificaciones y contrato de integración. | Disponible |
| Frontend | Interfaz web para gestores y repartidores. | En creación |
| Backend | Servicios, reglas de negocio, persistencia e integraciones. | En creación |

Los enlaces del frontend y backend se incorporarán cuando sus repositorios estén disponibles.

## 🔗 Integraciones

De acuerdo con la arquitectura general, Despacho y Entrega se relacionará con:

- Canal Marketplace.
- Canal Chatbot.
- Ventas y Postventa.
- Productos y Ofertas.
- Seguridad y Usuarios.

La comunicación se realizará mediante APIs y sin compartir bases de datos entre módulos. La mayoría de las operaciones serán **síncronas**. Los casos que necesiten comunicación asíncrona y la tecnología que utilizarán todavía se encuentran en evaluación.

## 🛠️ Tecnologías previstas

### Backend

- Java 21 y Spring Boot 4.1.1.
- Maven como herramienta de construcción y gestión de dependencias.
- Spring Web MVC para las APIs REST.
- Spring Data JPA e Hibernate para persistencia.
- Spring Security para autenticación y autorización.
- PostgreSQL Driver, Lombok y Bean Validation.
- Swagger UI para documentar y explorar la API desplegada.

### Frontend

- React con Vite.
- Tailwind CSS.
- Diseño web responsive para escritorio y dispositivos móviles.

### Datos, calidad y despliegue

- PostgreSQL administrado mediante Supabase.
- JUnit, Mockito, Spring Boot Test y Testcontainers.
- Figma para el diseño de interfaces.
- Vercel para el frontend y Render para el backend.
- Webhooks o RabbitMQ como alternativas de mensajería aún por evaluar.

Las dependencias específicas y sus versiones se documentarán en los repositorios de implementación correspondientes.

## 📜 Contrato y documentación de API

El archivo [Contrato de API](./integraciones/api-contract.md) reúne las convenciones de comunicación, autenticación, errores y organización de los endpoints del módulo.

Cuando el backend esté desplegado, publicará su documentación interactiva mediante Swagger UI. Esta documentación representará la API implementada y permitirá explorar sus operaciones disponibles. El enlace se incorporará cuando exista el entorno correspondiente.

Los endpoints, modelos, códigos de respuesta y ejemplos no se duplicarán en este README.

## 👥 Equipo

El equipo está conformado por 5 integrantes:

| Integrante | Rol transversal |
|---|---|
| **Tarqui** | Product Owner |
| **Gerardo** | Líder del equipo y responsable de Calidad |
| **Rhamses** | Responsable de DevOps y Cloud |
| **Max** | Responsable de Frontend y UI/UX |
| **Valqui** | Responsable de Arquitectura y Base de Datos |

## 🚧 Evolución del proyecto

La documentación evolucionará junto con el desarrollo. Se actualizarán progresivamente las especificaciones, las decisiones de integración y los enlaces a los entornos desplegados.

Ante cualquier diferencia entre este README y una especificación detallada, deberá revisarse y corregirse la documentación para mantener una única definición coherente del módulo.
