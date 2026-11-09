# Módulo de Despacho y Entrega a Domicilio

Este repositorio reúne las especificaciones, contratos y evidencias de Despacho. El módulo organiza pedidos para reparto, asigna capacidad, registra entregas e incidencias y ofrece seguimiento a los canales autorizados. Gestión de Despachos y Operación de Reparto y Flota se comunican mediante APIs y conservan sus propias bases.

El módulo está en implementación y pruebas de integración. El [índice funcional](./funcionalidades/funcionalidad.md) distingue el avance por especificación, las comprobaciones locales y la aceptación pendiente.

## Backend desplegado: pruebas de integración

El origen publicado del Gateway para coordinar pruebas es [taller-api-gateway.onrender.com](https://taller-api-gateway.onrender.com). Los módulos consumidores usan un token técnico de G7 con audiencia `api-despacho` y los permisos de la operación. Consultar [autenticación, endpoints y ejemplos](./integraciones/api-contract.md) antes de probar; las primeras solicitudes pueden demorar si los servicios estaban en reposo.

Para pruebas locales, seguir las instrucciones de los repositorios de implementación. Seguridad temporal, catálogos simulados y bases de prueba permiten verificar flujos de Despacho por separado. La aceptación conjunta y los resultados de cada entorno se registran en la evidencia correspondiente.

## Mapa de documentación

| Documento | Contenido |
|---|---|
| [Visión general](./overview.md) e [índice funcional](./funcionalidades/funcionalidad.md) | Alcance, responsables, estados y acceso a las especificaciones. |
| [Especificaciones atómicas](./especificaciones/) e [historias de usuario](./historias-usuario/) | Requisitos, planes, tareas y evidencia de cada caso. |
| [Contrato externo](./integraciones/api-contract.md) | Integraciones con Marketplace, Chatbot, Productos, Ventas y Seguridad; incluye cotización y seguimiento por pedido. |
| [API de Gestión](./integraciones/api-contract-gestion-despachos.md) | Zonas, tarifas, programación, incidencias y operaciones internas de Gestión. |
| [API de Operación](./integraciones/api-contract-operacion-reparto.md) | Reparto, flota, jornadas, evidencias, capacidad y operaciones internas de Operación. |
| [Contexto](./arquitectura/c4-contexto.md), [contenedores](./arquitectura/c4-contenedores.md) y [modelo de datos](./arquitectura/modelo-datos.md) | Límites del módulo, servicios y persistencia. |
| [Estados del despacho](./arquitectura/diagrama-estados-despacho.md), [macroproceso](./arquitectura/macroproceso-despacho.md) y [glosario](./arquitectura/glosario-dominio.md) | Flujo de negocio, transiciones y términos compartidos. |
| [Sistema de diseño](./disenio/SYSTEM-DESIGN.md) y [componentes React](./disenio/componentes-react.md) | Referencias de interfaz de las dos aplicaciones. |
| [Plan del Hito 4](./hitos/Plan_Hito_4_Despacho.md) y [ejecución F-02](./hitos/Plan_Hito_4_F02.md) | Coordinación y evidencia de integración por hito. |
| [Entrega v0.2.0](./entregas/v0.2.0.md) | Alcance, revisiones del corte y validaciones pendientes. |
| [Guía SDD](./plantillas/sdd/README.md), [reglas](./AGENTS.md) y [contribución](./CONTRIBUTING.md) | Plantillas y flujo de revisión y entregas. |

## Repositorios del módulo

| Repositorio | Propósito |
|---|---|
| [G2-Despacho-Backend](https://github.com/Taller-SW-Web/G2-Despacho-Backend) | Gateway, reglas de negocio, persistencia e integraciones. |
| [G2-Despacho-Frontend](https://github.com/Taller-SW-Web/G2-Despacho-Frontend) | Aplicación administrativa, PWA del repartidor y paquetes compartidos. |
| [G2-Despacho-Specs](https://github.com/Taller-SW-Web/G2-Despacho-Specs) | Especificaciones, contratos y evidencia. |

Specs recibe cambios por PR a `main`. Los repositorios de código integran el desarrollo en `develop` y promueven las entregas a `main` por PR.

## Equipo

| Integrante | Rol transversal o responsabilidad |
|---|---|
| Tarqui | Product Owner |
| Gerardo | Líder del equipo y Calidad |
| Rhamses | DevOps y Cloud |
| Max | Frontend y UI/UX |
| Valqui | Arquitectura y Base de Datos |
| Luis | Disponibilidad y capacidad diaria de flota |
