# Plan de trabajo del Hito 4 · Despacho

**Equipo activo** — Tarqui, Valqui, Max Rojas, Kevin Rhamses y Gerardo.  
**Estado** — Propuesta de reparto. Cada casilla se cierra con evidencia de la versión probada.

## 1. Alcance y criterio de entrega

El objetivo es presentar **las dos aplicaciones web y los tres componentes del backend funcionando en nube**. Los frontends administrativo y del repartidor consumen el API Gateway publicado. El Gateway comunica con Gestión de Despachos y Operación de Reparto, que necesitan acceso a sus bases y al almacenamiento de evidencias según corresponda. Seguridad de G7 es una dependencia externa que se integra al recorrido.

**Demo principal propuesta** — El gestor inicia sesión, abre una jornada y asigna un despacho. El repartidor ingresa, inicia traslado y reporta un fallo con evidencia. El gestor ve la incidencia, confirma la recepción y reprograma. El equipo verifica la liberación de la reserva antes de intentar una nueva asignación. La recepción deja una liberación asíncrona y la reprogramación confirma una decisión local. Cada resultado se comprueba por separado.

**Confirmar con el profesor** — Qué componentes deben cambiar de proveedor, cómo se califica el alcance completo de la demo que aparece truncado en la captura y si el ejercicio de OpenAPI en parejas se entrega junto al hito. Mientras se confirma, el equipo puede avanzar con el despliegue completo y comparar proveedores con los mismos criterios.

## 2. Cuadro de responsabilidades

| Integrante | Funcionalidad | Responsabilidad transversal | Por qué le corresponde | Evidencia principal |
|---|---|---|---|---|
| **Tarqui** | F-02 · Programación y asignación | Producto, alcance y aceptación funcional | Define qué recorrido se presenta y es dueño de la asignación que inicia la demo. | Despacho asignado que aparece en la ruta y guion con criterios de aceptación. |
| **Valqui** | F-01 · Zonas y cotización | Arquitectura, datos y revisión de contratos API | Puede comprobar que rutas, esquemas y datos coincidan entre servicios, documentación y consumidores. | Zona operativa, pruebas de Zonas recuperadas e inventario contrastado con Swagger. |
| **Max Rojas** | F-03 · Operación del repartidor | Frontend, UX e integración de sesión en ambas apps | Es dueño de la experiencia del repartidor y de la integración de las pantallas con el Gateway y G7. | Sesiones reales y fallo con evidencia visible después en Administración. |
| **Kevin Rhamses** | F-05 y F-06 · Repartidores, vehículos, jornadas y capacidad | DevOps, CI/CD y decisión de nube | Opera la plataforma y mantiene la jornada y las reservas que requiere el recorrido. | ADR, ejecución del pipeline, revisión activa y ocupación antes y después. |
| **Gerardo** | F-04 · Entregas fallidas, recepción y reprogramación | Liderazgo, Calidad y verificación posterior al despliegue | Es dueño del tramo final y coordina pruebas que atraviesan varias funcionalidades. | Prueba de humo en CI/CD, prueba de contrato de F-04 y evidencia integrada. |

## 3. Tareas por integrante

### Tarqui · Producto y F-02

- [ ] Acordar el alcance y la secuencia de la demo. Confirmar con el profesor las preguntas de la sección 1 y comunicar la decisión al equipo.
- [ ] Verificar en el ambiente publicado la cola y la asignación a una jornada activa con capacidad. Probar que el despacho asignado aparece en la ruta que consume F-03.
- [ ] Revisar qué cambios de rutas y cancelación ya entraron al backend. Actualizar el estado y la evidencia de las operaciones que se prueben para el hito.
- [ ] Acordar con Max, Kevin y Gerardo los datos del caso principal, el estado inicial del despacho y el resultado esperado en cada transición.
- [ ] Validar el alcance funcional al final del ensayo. Preparar una demostración corta de la asignación y su efecto en la ruta.

**Entregable** — Caso de F-02 reproducible con ID de despacho, petición o respuesta de API, captura de la ruta y visto bueno funcional.

### Valqui · Arquitectura, APIs y F-01

- [ ] Preparar y verificar una zona de cobertura que sirva para el despacho de prueba. Si la cotización exacta entra en la demo, registrar qué falta de F-01 o de la integración con Productos y confirmar los datos y permisos con los responsables.
- [ ] Diagnosticar la exclusión temporal de Zonas de la suite administrativa. Corregir los mensajes esperados o los datos de prueba con Max según corresponda. Coordinar con Kevin la reincorporación después de comprobar que pasa.
- [ ] Consolidar un **inventario enlazado a los tres contratos vigentes**. Separar integraciones con otros módulos, APIs consumidas por los dos frontends y llamadas privadas entre Gestión y Operación. Por operación del hito registrar proveedor, consumidor, método, ruta, datos, autenticación, errores y estado de verificación.
- [ ] Revisar con cada dueño sus operaciones en Swagger/OpenAPI y contrastarlas con el contrato y la respuesta real. Verificar especialmente permisos, códigos HTTP, formato de errores e idempotencia donde aplique.
- [ ] Apoyar a Kevin en la comparación de nube con compatibilidad de PostgreSQL/PostGIS, migraciones, conectividad entre servicios, CORS y almacenamiento de evidencias. Revisar el esquema y el historial de Flyway antes de plantear una migración sobre una base existente.

**Entregable** — Inventario y Swagger de Gestión y Operación listos para mostrar, más la prueba de F-01 que sustenta el escenario.

### Max Rojas · Frontend, sesiones y F-03

- [ ] Identificar con quien ya está avanzando Seguridad la rama o PR, sus cambios y lo que falta. Repartir cualquier ajuste de sesión antes de implementar en paralelo.
- [ ] Integrar o completar el inicio de sesión real en ambas apps conforme al contrato de G7. Verificar el flujo de MFA del gestor, la sesión del repartidor, el comportamiento al vencer la sesión y el cierre de sesión.
- [ ] Coordinar con Kevin si las apps llaman directamente a G7 o pasan por el Gateway. Validar orígenes, rutas y configuración de las versiones publicadas según la decisión.
- [ ] Conectar la ruta, el inicio de traslado, la carga de evidencia y el reporte de fallo a las APIs reales de F-03. Mostrar errores accionables si la sesión, la jornada o la evidencia impiden continuar.
- [ ] Verificar con Tarqui que la ruta recibe la asignación y con Gerardo que el fallo reportado aparece en Administración. Conservar el ID y la respuesta de la operación para repetir la demo.

**Entregable** — Acceso con cuentas reales, llamada desde la app del repartidor y registro persistido visible en la app administrativa.

### Kevin Rhamses · DevOps, CI/CD, F-05 y F-06

- [ ] Liderar el **ADR de nube**. Comparar el alojamiento actual con al menos otra alternativa por costo total, región y latencia, esfuerzo operativo, portabilidad, acceso a dependencias y comportamiento de tareas programadas. Registrar qué componentes se migran y justificar la elección.
- [ ] Justificar **GitHub Actions** frente a otra herramienta vista en clase. Aprovechar los workflows existentes de frontend y backend. Enlazar compilación y pruebas con el despliegue de una versión aprobada y definir cuándo se promueve de pruebas al ambiente de entrega.
- [ ] Verificar que estén publicados y conectados los dos frontends, Gateway, Gestión y Operación. Configurar variables y secretos por ambiente, rutas internas, persistencia y acceso a evidencias. Coordinar con G7 la configuración de orígenes o proxy y las credenciales técnicas necesarias para el recorrido.
- [ ] Identificar cada despliegue por commit, tag cuando corresponda y revisión o imagen. Ordenar la salida por etapas y conservar reportes. Acordar cómo volver a una revisión anterior y qué hacer si hay migraciones de datos.
- [ ] Integrar con Gerardo el paso de verificación posterior al despliegue. Si falla una comprobación crítica, la versión queda pendiente de promoción y el reporte identifica el paso que falló.
- [ ] Preparar vehículo, perfiles de repartidor vinculados a Seguridad y jornada para la demo. Comprobar la reserva y la liberación de capacidad con valores antes y después. Verificar que el procesador de liberaciones funciona en el entorno elegido.

**Entregable** — ADR, workflows, ejecución exitosa, revisión activa, URLs de las apps y del Gateway, y evidencia de F-05/F-06.

### Gerardo · Calidad, CI/CD y F-04

- [ ] Acordar con Kevin qué resultados bloquean la promoción de una versión. Revisar con Valqui la reincorporación de las pruebas de Zonas y con cada responsable la evidencia de sus pruebas.
- [ ] Preparar y, con Kevin, incorporar la **prueba de humo posterior al despliegue**. Automatizar la salud del Gateway y una consulta protegida si hay una identidad técnica de prueba autorizada para esa operación. El acceso humano a F-04 se comprueba con una sesión real y MFA durante el ensayo. Guardar entorno, SHA y resultado de cada comprobación.
- [ ] Probar el contrato de recepción de F-04. Incluir gestor autorizado con `202`, campos inválidos con `400`, token ausente o permiso insuficiente y repetición exacta sin duplicar historial ni liberación.
- [ ] Verificar F-04 con los servicios reales. Confirmar que la incidencia se puede consultar, que la recepción deja constancia, que Operación libera la reserva y que la reprogramación queda guardada. Coordinar con Kevin y Tarqui la comprobación de capacidad antes de una nueva asignación.
- [ ] Preparar con Max los casos de seguridad de la demo. Verificar MFA del gestor, acceso a la ruta propia y rechazo al consultar un despacho ajeno. Pedir a otro integrante que revise los cambios de F-04.
- [ ] Coordinar el ensayo y registrar por cada caso el resultado, las incidencias y los pendientes de integración. Separar evidencia local, simulada y ejecutada en nube.

**Entregable** — Paso de Calidad visible en CI/CD, reporte de contrato de F-04 y evidencia del ensayo en la versión publicada.

## 4. Dependencias y orden de ejecución

| Momento | Trabajo en paralelo | Condición para avanzar |
|---|---|---|
| **Primero** | Tarqui confirma alcance. Kevin compara plataformas y prepara el ambiente. Valqui inventaría APIs y datos. Max ubica la rama de Seguridad. Gerardo prepara los casos y el reporte. | Cada persona tiene un tramo, un criterio de cierre y un entorno acordado. |
| **Integración** | Kevin conecta servicios y verifica CI/CD. Max conecta sesión y F-03. Tarqui verifica asignación. Valqui prepara cobertura y contrasta los contratos. Gerardo verifica F-04 y prepara la prueba posterior al despliegue. | La versión publicada pasa la prueba básica. G7 confirma las cuentas y, si aplica, los orígenes y permisos. Kevin verifica los vínculos de repartidor en F-05. |
| **Ensayo y cierre** | Los cinco recorren el mismo despacho. Gerardo registra resultados, Tarqui valida el alcance y Kevin identifica la revisión ejecutada. | Cada paso tiene evidencia asociada al mismo caso. Los fallos y dependencias pendientes quedan identificados con responsable. |

**Coordinación con G7** — Tarqui y Gerardo acuerdan el horario de la prueba. Max aporta las URLs de las apps y valida el flujo humano. Kevin coordina la configuración de ambiente y las credenciales técnicas por un canal privado. Para probar permisos de usuario, preparar un gestor con MFA y dos repartidores activos vinculados por UUID. Los tokens de servicio de integraciones se gestionan por separado de las sesiones humanas.

## 5. Evidencia para la sustentación

| Criterio | Qué abrir o ejecutar |
|---|---|
| **CI/CD** | PR y SHA → ejecución del pipeline → reportes de build, compilación y pruebas → revisión publicada → resultado de la prueba de humo. |
| **Diseño de APIs** | Inventario y Swagger → operación y contrato → petición real con éxito y con error → controlador o prueba que lo respalda. |
| **Seguridad en pantallas y APIs** | Login con G7, MFA del gestor, ruta del repartidor y llamadas permitidas y rechazadas. Mostrar códigos HTTP y ocultar tokens y secretos. Explicar quién emite el JWT y qué verifica Despacho. |
| **Demo funcional** | Asignación → traslado → fallo con evidencia → recepción → liberación de capacidad y reprogramación. Mostrar los mismos IDs y los estados antes y después. |
| **Prácticas DevOps y versionado** | ADR de nube, comparación de herramientas, rama y revisión por pares, changelog, tag o SHA y revisión publicada. Cada integrante puede explicar su aporte con evidencia del equipo. |
| **Webhook** | Contrato Despacho → Ventas/Postventa, registro del evento en la bandeja de salida y código de envío. Explicar reintentos y deduplicación por `idEvento`. Si se ejecuta con Ventas, guardar la confirmación de recepción aparte. |

## 6. Qué se toma de la teoría

- **TEO 08, diaps. 4, 7, 19, 21–23 y 25.** Ambientes, prueba de humo, decisión de nube, elección de CI/CD, trazabilidad de la versión y evidencia de prácticas DevOps. Kevin lidera la decisión de nube y cada integrante prepara su sustentación. Las prácticas de Eventos de las diapositivas 13 y 24 corresponden al laboratorio.
- **TEO 09, diaps. 16–19 y 25.** Contratos verificables, OpenAPI/Swagger, pruebas de contrato, JWT y análisis de webhook. La diapositiva 25 aplica al proyecto. Si se pide también la práctica en parejas de la diapositiva 19, planificarla aparte con una entidad de más de diez columnas y las siete operaciones solicitadas. El CRUD de Eventos de la diapositiva 14 corresponde al laboratorio.

## 7. Referencias de trabajo

- [Teoría de despliegue y CI/CD](../TEO_08_Despliegue_Nube_CICD_DevOps.pdf) · [Teoría de APIs REST](../TEO_09_APIs.pdf)
- [Índice de funcionalidades](G2-Despacho-Specs/funcionalidades/funcionalidad.md) · [Flujo de contribución y versiones](G2-Despacho-Specs/CONTRIBUTING.md)
- [Contratos de integraciones externas](G2-Despacho-Specs/integraciones/api-contract.md) · [API de Gestión](G2-Despacho-Specs/integraciones/api-contract-gestion-despachos.md) · [API de Operación](G2-Despacho-Specs/integraciones/api-contract-operacion-reparto.md)
- [Workflow de backend](G2-Despacho-Backend/.github/workflows/ci.yaml) · [Workflow de frontend](G2-Despacho-Frontend/.github/workflows/ci.yaml)
- [Avance y contrato de Seguridad](seguridad-avance-equipo.md) · [Pendientes de coordinación con G7](solicitud-integracion-seguridad.md)
- [Evidencia y pendientes de F-04](G2-Despacho-Specs/especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/evidence.md) · [Validación de F-05/F-06](G2-Despacho-Specs/especificaciones/ES-F06-01-AbrirJornada/evidencia/validacion.md)
