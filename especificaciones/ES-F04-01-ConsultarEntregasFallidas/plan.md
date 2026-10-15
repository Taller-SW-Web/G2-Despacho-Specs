# Plan de ES-F04-01: Consultar entregas fallidas

**Responsable:** Gerardo.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** Aplica; página administrativa `/entregas-fallidas`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-05 | Contenido previo en `8586a78`; migración y complementos en esta carpeta. |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-06 | Misma revisión documental que este plan. |
| Contrato | [API](../../integraciones/api-contract.md), §§3.3, 3.5, 8, 11 y 13 | `8586a78`; parámetros y DTO del listado pendientes. |
| Componentes y diseño | [Componentes React](../../disenio/componentes-react.md), §§4.5–4.6; [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md), §23 | `8586a78`. |
| Arquitectura y datos | [Contenedores](../../arquitectura/c4-contenedores.md), §3; [modelo de datos](../../arquitectura/modelo-datos.md), §§1, 3.3 y 3.4 | `8586a78`. |
| Base de código | Backend `af13989`; frontend `d2bc27d` | Inicialización de aplicaciones; sin endpoint de consulta ni página funcional de F-04. |

Este cambio prepara documentación. La modificación del contrato, el código y las pruebas de comportamiento se ejecutarán en tareas posteriores. No se duplican contratos ni se da por cerrada la revisión técnica [cite: 1, 2].

## 2. Estrategia y responsabilidades

La página consume una consulta autorizada a través del Gateway. Gestión obtiene sus datos locales y la información acordada con Operación, aplica la restricción `FALLIDO`, filtros, orden y paginación, y devuelve únicamente el resumen permitido. El contenedor frontend adapta ese resultado a componentes visuales controlados.

| Área | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Frontend administrativo | Página, filtros, consulta y adaptación del resultado. | `apps/despacho-administrativo/src/features/entregas-fallidas/`; `PaginaEntregasFallidas.tsx` y adaptador de consulta. |
| Componentes compartidos | Presentación e interacción sin HTTP ni acceso a tokens. | `packages/componentes-compartidos/src/`; CR-01/02/03/05/06/07/08/09/10. |
| Cliente de API | Petición y tratamiento del formato de errores vigente. | Paquete existente `packages/cliente-api`; tipos de transporte tras DT-01. |
| Gateway | Enrutamiento de la consulta y propagación de identidad/correlación. | `api-gateway`; configuración base pendiente de habilitar y comprobar. |
| Gestión de Despachos | Autorización, caso de uso y persistencia de consulta. | Funcionalidad propuesta `incidencias/`, bajo el paquete base existente, con `api`, `application`, `domain` e `infrastructure` según necesidad. |
| Operación de Reparto y Flota | Datos propios de repartidor y jornada mediante contrato. | Adaptador de salida de Gestión; mecanismo de lectura pendiente en DT-02. |

Los nombres de clases y subpaquetes son decisiones técnicas propuestas. No se crean módulos desplegables nuevos ni se comparten entidades JPA entre servicios.

## 3. Frontend y componentes React

- Verificar primero tema, proveedores, dependencias y herramientas de pruebas según §4.5.1 del documento compartido.
- Gerardo implementará CR-08 EstadoVista como trabajo posterior y lo verificará contra CCR-08-01. Coordinar los demás CR con sus responsables documentados; la preparación de esta carpeta no los declara disponibles.
- CR-12/15 corresponden a confirmaciones y sus resultados; CR-18/19 al detalle. No son prerrequisitos de la consulta aislada.
- El contenedor mantiene filtros, página y estado de consulta, sincroniza la URL y descarta respuestas obsoletas. Los cambios de filtro reinician la página.
- Antes del contrato completo pueden usarse fixtures de presentación para los seis estados de UI y las combinaciones de indicadores. No representan respuestas HTTP definitivas ni prueban filtros del backend.
- Tras DT-01, implementar el adaptador de HTTP y reemplazar los fixtures por resultados reales. No calcular indicadores globales con las filas de una página.
- La navegación al detalle y la apertura de recepción se enlazan con ES-F04-02/03 cuando existan; registrar esa disponibilidad por separado del alcance de consulta.

## 4. Backend, persistencia e integraciones

- Entrada: `GET /api/v1/despachos/fallidos`. Autorizar el JWT humano y exigir `GESTOR_DESPACHO`; el cliente no sustituye esta comprobación.
- Caso de uso: consultar solo despachos cuyo estado vigente sea `FALLIDO`, combinar filtros y producir una página de resúmenes sin datos del detalle. Elegir y verificar un orden estable conforme a DT-01.
- Datos locales: despachos, intentos, motivos, recepción, anulación y política de intentos según el modelo. Resolver el intento/incidencia vigente antes de paginar para evitar filas duplicadas.
- Migración: revisar el esquema existente y su forma de gestión con Arquitectura; crear migraciones Flyway solo para cambios necesarios. No asumir que las tablas o migraciones ya están disponibles por aparecer en el modelo.
- Integraciones: resolver nombre del repartidor y cierre de jornada según DT-02, mediante APIs o una proyección acordada. No consultar tablas de Operación ni inventar nuevos endpoints. Definir tratamiento de datos no disponibles antes de aceptar CA-05.
- Retorno atrasado: jornada cerrada confirmada y recepción pendiente. No inferirlo solo a partir de la fecha o del reloj del frontend.
- Fechas: el modelo establece `America/Lima` para la jornada y UTC para instantes. DT-01 concreta los límites del rango de consulta y su representación HTTP.
- Efectos secundarios: la consulta no crea intentos, confirma recepciones, libera capacidad ni emite eventos de negocio. No requiere una clave de idempotencia de comando.
- Errores: aplicar el formato central de §3.5; concretar los errores de filtros y de dependencias en el contrato antes de implementar el adaptador real.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Componentes requeridos disponibles y página aislada con fixtures identificados. | Base frontend y CR de §3; no necesita una API real. | CUI-01 a CUI-06, solo presentación/interacción. |
| I-02 | Contrato, fuentes y consulta backend implementados y probados. | DT-01/02/03; persistencia, JWT y Gateway disponibles para la prueba completa. | CA-01 a CA-05. |
| I-03 | Página conectada y verificación del recorrido real. | I-01 e I-02. | CA-01 a CA-05 y CUI-01 a CUI-06. |

La definición contractual y de fuentes puede prepararse mientras se desarrolla I-01. Solo el incremento afectado queda detenido por cada pendiente.

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y datos |
|---|---|---|
| CA-01 | Excluir otros estados; campos e indicadores correctos; página sin duplicados. | Integración PostgreSQL del backend y recorrido UI; varios estados y más de una página. |
| CA-02 | Combinar filtros, probar límites de fechas, orden estable y cambio de página. | Integración con contrato cerrado; fixtures de UI para interacción. |
| CA-03 | Diferenciar vacío, ausencia de coincidencias y error. | Backend con cero fallidos/coincidencias; UI con fixtures y API real. |
| CA-04 | Rechazar usuario con otro rol sin datos y retirar resultados previos en UI. | Pruebas de seguridad del endpoint y de interacción. |
| CA-05 | Matriz de jornada activa/cerrada y recepción pendiente/confirmada. | Regla backend y adaptador; después fuente real de Operación. |
| CUI-01 a CUI-06 | Contenido, controles, recuperaciones, foco, nombres accesibles y responsive. | Pruebas de interacción y recorrido manual reproducible. |

Comandos previstos: desde el frontend, `npm run typecheck` y `npm run build`; desde Gestión, `./mvnw.cmd test` en PowerShell. Las herramientas y el comando de pruebas frontend se definirán al habilitarlas; no existe actualmente un script de pruebas. Las pruebas con Testcontainers requieren Docker. Los resultados y la distinción entre dobles y servicios reales se anotarán en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Punto por resolver | Fuente y responsable de coordinación | Bloquea |
|---|---|---|---|
| DT-01 | Nombres/límites de filtros, página y tamaño; DTO de filas, totales e indicadores; orden estable y desempate; catálogo de motivos; límites del rango y filtros derivados de KPI. | Contrato §11 y DC-04 del documento compartido. Gerardo con Backend/Frontend y Arquitectura. La revisión del contrato se hará después de esta preparación documental. | Adaptadores HTTP de I-02/03; no los fixtures visuales de I-01. |
| DT-02 | Fuente y frescura de los datos de repartidor y cierre de jornada; tratamiento de una dependencia no disponible. | Modelo de datos, F-03/F-05/F-06 y contrato §13. Gerardo con responsables de Operación y Arquitectura. | CA-01/05 e integración real de I-02/03. |
| DT-03 | Esquema/migraciones necesarios y base compartida de JWT, errores, conexión de datos y rutas del Gateway. | Inicialización actual del backend y modelo. Gerardo coordina con Arquitectura y DevOps. | Ejecución real de I-02/03. |
| DT-04 | Disponibilidad y verificación de componentes, tema y herramientas de pruebas. | Componentes React §§4.5–4.6. Gerardo para CR-08; coordinación con los responsables del resto. | Composición y aceptación de I-01 según sus dependencias. |

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas del incremento están revisadas y sus pendientes bloqueantes resueltos.
- [ ] Los componentes requeridos están verificados antes de componer la pantalla consumidora.
- [ ] Las tareas cubren todos los criterios y tienen una comprobación concreta.
- [ ] La consulta respeta el contrato único y la propiedad de datos de cada servicio.
- [ ] Todos los criterios del alcance cuentan con evidencia, distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [Especificación](./spec.md), [UI](./ui.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [Contrato central](../../integraciones/api-contract.md#11-api-de-f-04-entregas-fallidas), [modelo de datos](../../arquitectura/modelo-datos.md) y [arquitectura de contenedores](../../arquitectura/c4-contenedores.md).
3. [Componentes React](../../disenio/componentes-react.md), [sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [flujo SDD](../../plantillas/sdd/README.md).
