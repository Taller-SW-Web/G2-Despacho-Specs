# Módulo de Despacho y Entrega a Domicilio

> Documentación y especificaciones del módulo responsable de organizar, ejecutar y dar seguimiento al proceso de despacho y entrega de pedidos.

**Estado del proyecto:** En especificación y diseño inicial  
**Arquitectura prevista:** Dos microservicios con persistencia aislada, integrados mediante APIs  
**Repositorio:** Documentación funcional y técnica

---

## 📦 Acerca del módulo

El **Módulo de Despacho y Entrega a Domicilio** administra el ciclo operativo que comienza cuando un pedido está listo para ser despachado y termina con su entrega, reprogramación o devolución.

El módulo es responsable de la entidad **despacho** y mantiene sus propios datos. La información perteneciente a pedidos, productos y usuarios se obtiene mediante las APIs de los módulos propietarios, sin acceder directamente a sus bases de datos.

La implementación se divide en los microservicios **Gestión de Despachos** y **Operación de Reparto y Flota**. Cada uno mantiene su propia persistencia y se comunican mediante APIs internas.

Este repositorio centraliza las especificaciones funcionales, decisiones generales y contratos necesarios para que el frontend, el backend y los demás módulos puedan desarrollarse de manera coordinada.

## 🎯 Capacidades principales

| ID | Área funcional | Descripción |
|---|---|---|
| **F-01** | Zonas geográficas y cotización | Administra zonas de cobertura y calcula tarifas de entrega según las reglas definidas. |
| **F-02** | Programación y asignación | Organiza los despachos pendientes y permite asignarlos a repartidores o rutas disponibles. |
| **F-03** | Operación del repartidor | Ofrece una web responsive para consultar entregas, actualizar estados y registrar evidencias. |
| **F-04** | Entregas fallidas y reprogramaciones | Gestiona incidencias, nuevos intentos de entrega y devoluciones a almacén. |
| **F-05** | Repartidores y vehículos | Registra repartidores con vinculación a Seguridad y furgonetas con capacidades de carga. |
| **F-06** | Disponibilidad y capacidad diaria | Asigna repartidores a furgonetas y zonas por jornada, calcula ocupación y disponibilidad. |

### Seguimiento de pedidos

El módulo expondrá información de seguimiento mediante API para que los canales autorizados consulten el estado de un despacho. Esta capacidad es transversal y no constituye un área funcional independiente.

Los requisitos, escenarios y criterios de aceptación de cada capacidad se desarrollan en sus respectivas especificaciones.

## 🧭 Mapa de documentación

| Documento | Contenido |
|---|---|
| [Visión general](./overview.md) | Problema, objetivos, alcance, actores y flujo general del módulo. |
| [Índice de funcionalidades](./funcionalidades/funcionalidad.md) | Listado y estado de las especificaciones funcionales. |
| [Integraciones externas](./integraciones/api-contract.md) | Comunicaciones con otros módulos y convenciones compartidas. |
| [API de Gestión de Despachos](./integraciones/api-contract-gestion-despachos.md) | Zonas, programación, catálogo, incidencias y API interna provista por Gestión. |
| [API de Operación de Reparto y Flota](./integraciones/api-contract-operacion-reparto.md) | Repartidor, flota, jornadas, evidencias, capacidad y API interna provista por Operación. |
| [Modelo de datos](./arquitectura/modelo-datos.md) | Base evolutiva de entidades, relaciones y decisiones de persistencia. |
| [C4 de contexto](./arquitectura/c4-contexto.md) | Actores, límites del sistema e integraciones externas. |
| [C4 de contenedores](./arquitectura/c4-contenedores.md) | Aplicaciones, microservicios, persistencias y comunicaciones internas. |
| [Glosario de dominio](./arquitectura/glosario-dominio.md) | Significado común de pedidos, despachos, cotizaciones, capacidad y operación. |
| [Estados del despacho](./arquitectura/diagrama-estados-despacho.md) | Estados, transiciones, precondiciones y operaciones no permitidas. |
| [Componentes React compartidos](./disenio/componentes-react.md) | Contratos, criterios de aceptación y estilos con Mantine; reparto entre seis integrantes y ubicación en el paquete compartido del frontend. |
| [Macroproceso de despacho](./arquitectura/macroproceso-despacho.md) | Flujo funcional de alto nivel desde la solicitud de Ventas hasta el resultado final. |
| [Especificaciones funcionales](./funcionalidades/) | Requisitos, escenarios y criterios de completitud por funcionalidad. |
| [Especificaciones atómicas](./especificaciones/) | F-02 cuenta con sus ocho carpetas SDD preparadas: [recepción](./especificaciones/ES-F02-01-RecepcionSolicitudDespacho/spec.md), [simulación](./especificaciones/ES-F02-02-GenerarDespachoPrueba/spec.md), [cola de pendientes](./especificaciones/ES-F02-03-ConsultarColaPendientes/spec.md), [asignación](./especificaciones/ES-F02-04-AsignarDespachoRepartidor/spec.md), [secuencia de ruta](./especificaciones/ES-F02-05-ConsultarReordenarSecuenciaRuta/spec.md), [reasignación](./especificaciones/ES-F02-06-ReasignarDespachoRepartidor/spec.md), [cancelación](./especificaciones/ES-F02-07-CancelarDespachoPorAnulacion/spec.md) y [trazabilidad](./especificaciones/ES-F02-08-RegistrarTrazabilidadOperaciones/spec.md). F-04 tiene sus seis carpetas SDD preparadas: [listado](./especificaciones/ES-F04-01-ConsultarEntregasFallidas/spec.md), [detalle](./especificaciones/ES-F04-02-ConsultarDetalleIncidencia/spec.md), [recepción](./especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/spec.md), [reprogramación](./especificaciones/ES-F04-04-ReprogramarDespachoFallido/spec.md), [cierre](./especificaciones/ES-F04-05-CerrarDespachoComoDevueltoAOrigen/spec.md) y [trazabilidad](./especificaciones/ES-F04-06-RegistrarTrazabilidadOperaciones/spec.md). Incluyen plan, tareas, evidencia y UI cuando aplica. El avance implementado y sus verificaciones se registran en la evidencia de cada carpeta. |
| [Plantillas y flujo SDD](./plantillas/sdd/README.md) | Organización aprobada por especificación, con adopción progresiva: comportamiento, UI opcional, plan, tareas y evidencia; componentes React compartidos. |
| [Historias de usuario](./historias-usuario/) | Historias en formato Jira (COMO/QUIERO/PARA) con criterios de aceptación Gherkin y DoD. |
| [Reglas del repositorio](./AGENTS.md) | Convenciones para crear y mantener la documentación. |
| [Guía de contribución](./CONTRIBUTING.md) | Flujo de ramas, commits y revisión de cambios. |

F-01 cuenta con sus ocho carpetas SDD preparadas. Las últimas migraciones son [cotización con productos (ES-F01-06)](./especificaciones/ES-F01-06-CotizarEnvioConProductos/spec.md), [resolución de zona (ES-F01-07)](./especificaciones/ES-F01-07-ResolverZonaParaModulo/spec.md) y [trazabilidad de configuración (ES-F01-08)](./especificaciones/ES-F01-08-RegistrarTrazabilidadConfiguracion/spec.md), cada una con especificación, plan, tareas y evidencia. La UI no aplica en esas tres; su implementación y verificación funcional están pendientes. El [índice funcional](./funcionalidades/funcionalidad.md#especificaciones-atómicas-de-f-01) enlaza todos sus documentos.

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

La comunicación se realiza mediante APIs y sin compartir bases de datos entre módulos. Las solicitudes de cotización, seguimiento, creación y cancelación se atienden de forma síncrona. Los cambios de estado hacia Ventas y Postventa se notifican de forma asíncrona mediante webhook HTTPS con bandeja de salida y reintentos.

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
- Webhooks HTTPS con patrón outbox para notificaciones asíncronas a Ventas y Postventa.

Las dependencias específicas y sus versiones se documentarán en los repositorios de implementación correspondientes.

## 📜 Contrato y documentación de API

La documentación se distribuye en tres contratos: [integraciones externas y convenciones compartidas](./integraciones/api-contract.md), [Gestión de Despachos](./integraciones/api-contract-gestion-despachos.md) y [Operación de Reparto y Flota](./integraciones/api-contract-operacion-reparto.md). Cada operación tiene una sola definición; los consumidores enlazan el contrato de su proveedor y las convenciones comunes.

Cuando el backend esté desplegado, publicará su documentación interactiva mediante Swagger UI. Esta documentación representará la API implementada y permitirá explorar sus operaciones disponibles. El enlace se incorporará cuando exista el entorno correspondiente.

Los endpoints, modelos, códigos de respuesta y ejemplos no se duplicarán en este README.

## 👥 Equipo

El equipo está conformado por 6 integrantes:

| Integrante | Rol transversal o responsabilidad |
|---|---|
| **Tarqui** | Product Owner |
| **Gerardo** | Líder del equipo y responsable de Calidad |
| **Rhamses** | Responsable de DevOps y Cloud |
| **Max** | Responsable de Frontend y UI/UX |
| **Valqui** | Responsable de Arquitectura y Base de Datos |
| **Luis** | Responsable de F-06: disponibilidad y capacidad diaria de la flota |

## 🚧 Evolución del proyecto

La documentación evolucionará junto con el desarrollo. Se actualizarán progresivamente las especificaciones, las decisiones de integración y los enlaces a los entornos desplegados.

Ante cualquier diferencia entre este README y una especificación detallada, deberá revisarse y corregirse la documentación para mantener una única definición coherente del módulo.
