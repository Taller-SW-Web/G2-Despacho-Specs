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
- [ ] Verificar en la versión del hito que se ejecuta la suite administrativa completa, incluida Zonas. La corrección de pruebas y la reincorporación a CI se prepararon en el [PR de Frontend #19](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/pull/19).
- [ ] Consolidar un **inventario enlazado a los tres contratos vigentes**. Separar integraciones con otros módulos, APIs consumidas por los dos frontends y llamadas privadas entre Gestión y Operación. Por operación del hito registrar proveedor, consumidor, método, ruta, datos, autenticación, errores y estado de verificación.
- [ ] Revisar con cada dueño sus operaciones en Swagger/OpenAPI y contrastarlas con el contrato y la respuesta real. Verificar especialmente permisos, códigos HTTP, formato de errores e idempotencia donde aplique.
- [ ] Alinear con Kevin el contrato de las llamadas internas con la decisión de autorizar por identidad de servicio. Retirar la solicitud de los seis scopes internos de la documentación de G2 y conservar los permisos acordados para las integraciones externas. Registrar el mecanismo de emisión y validación cuando quede definido.
- [ ] Apoyar a Kevin en la comparación de nube con compatibilidad de PostgreSQL/PostGIS, migraciones, conectividad entre servicios, CORS y almacenamiento de evidencias. Revisar el esquema y el historial de Flyway antes de plantear una migración sobre una base existente.

**Entregable** — Inventario y Swagger de Gestión y Operación listos para mostrar, más la prueba de F-01 que sustenta el escenario.

### Max Rojas · Frontend, sesiones y F-03

- [ ] Revisar con quien lleva la sesión el estado de su rama o PR. El PR de Frontend #19 aclara la vinculación en F-05 y la apertura de jornada en F-06. El acceso real de ambas apps se verifica por separado.
- [ ] Completar la sesión real en ambas apps según el contrato de G7. En el acceso del repartidor, reemplazar el formulario antiguo por JSON con `correo` y `contrasena`. Verificar MFA del gestor, renovación al vencer la sesión y cierre de sesión. Usar cuentas reales para el ensayo y mantener el probador y la demo de datos en memoria en el entorno de desarrollo.
- [ ] Coordinar con Kevin si las apps llaman directamente a G7 o pasan por el Gateway. Validar orígenes, rutas y configuración de las versiones publicadas según la decisión.
- [ ] Conectar la ruta, el inicio de traslado, la carga de evidencia y el reporte de fallo a las APIs reales de F-03. Mostrar errores accionables si la sesión, la jornada o la evidencia impiden continuar.
- [ ] Verificar con Tarqui que la ruta recibe la asignación y con Gerardo que el fallo reportado aparece en Administración. Conservar el ID y la respuesta de la operación para repetir la demo.

**Entregable** — Acceso con cuentas reales, llamada desde la app del repartidor y registro persistido visible en la app administrativa.

### Kevin Rhamses · DevOps, CI/CD, F-05 y F-06

- [ ] Liderar el **ADR de nube**. Comparar el alojamiento actual con al menos otra alternativa por costo total, región y latencia, esfuerzo operativo, portabilidad, acceso a dependencias y comportamiento de tareas programadas. Registrar qué componentes se migran y justificar la elección.
- [ ] Justificar **GitHub Actions** frente a otra herramienta vista en clase. Aprovechar los workflows existentes de frontend y backend. Enlazar compilación y pruebas con el despliegue de una versión aprobada y definir cuándo se promueve de pruebas al ambiente de entrega.
- [ ] Verificar que estén publicados y conectados los dos frontends, Gateway, Gestión y Operación. Configurar variables y secretos por ambiente, rutas internas, persistencia y acceso a evidencias. Confirmar que los modos de acceso sin autenticación del backend y la demo del frontend estén desactivados en el ambiente publicado. Conservar `seguridad-local` para Compose y pruebas.
- [ ] Verificar el estado del [PR de Backend #22](https://github.com/Taller-SW-Web/G2-Despacho-Backend/pull/22) y su presencia en la versión del hito. El PR prepara la validación JWT de Operación con pruebas locales. Comprobar después un token de G7 con un repartidor activo y vinculado.
- [ ] Acordar con Valqui y los responsables de Gestión y Operación qué identidad puede llamar a cada ruta interna y cómo obtendrá su credencial. Confirmar la audiencia del token antes de sustituir en el backend los seis scopes internos. Coordinar por canal privado las credenciales de integraciones externas que entren en la demo.
- [ ] Identificar cada despliegue por commit, tag cuando corresponda y revisión o imagen. Ordenar la salida por etapas y conservar reportes. Acordar cómo volver a una revisión anterior y qué hacer si hay migraciones de datos.
- [ ] Integrar con Gerardo el paso de verificación posterior al despliegue. Si falla una comprobación crítica, la versión queda pendiente de promoción y el reporte identifica el paso que falló.
- [ ] Preparar vehículo, perfiles de repartidor vinculados a Seguridad y jornada para la demo. Comprobar la reserva y la liberación de capacidad con valores antes y después. Verificar que el procesador de liberaciones funciona en el entorno elegido.

**Entregable** — ADR, workflows, ejecución exitosa, revisión activa, URLs de las apps y del Gateway, y evidencia de F-05/F-06.

### Gerardo · Calidad, CI/CD y F-04

- [ ] Acordar con Kevin qué resultados bloquean la promoción de una versión. Revisar con Valqui la reincorporación de las pruebas de Zonas y con cada responsable la evidencia de sus pruebas.
- [ ] Preparar y, con Kevin, incorporar la **prueba de humo posterior al despliegue**. Comprobar la salud del Gateway y que una consulta protegida de F-04 sin token devuelve `401`. Probar la misma consulta con un JWT de gestor del emisor local y repetirla en el ensayo con una sesión real de G7. Guardar entorno, SHA y resultado de cada comprobación.
- [ ] Probar el contrato de recepción de F-04. Incluir gestor autorizado con `202`, campos inválidos con `400`, token ausente o permiso insuficiente y repetición exacta sin duplicar historial ni liberación.
- [ ] Verificar F-04 con los servicios reales. Confirmar que la incidencia se puede consultar, que la recepción deja constancia, que Operación libera la reserva y que la reprogramación queda guardada. Coordinar con Kevin y Tarqui la comprobación de capacidad antes de una nueva asignación.
- [ ] Preparar con Max los casos de seguridad de la demo. Verificar MFA del gestor, acceso a la ruta propia, rechazo al consultar un despacho ajeno, sesión vencida y cierre de sesión. Con Kevin, comprobar la llamada interna desde el servicio autorizado y el rechazo de un token humano o de otro servicio. Pedir a otro integrante que revise los cambios de F-04.
- [ ] Coordinar el ensayo y registrar por cada caso el resultado, las incidencias y los pendientes de integración. Separar evidencia local, simulada y ejecutada en nube.

**Entregable** — Paso de Calidad visible en CI/CD, reporte de contrato de F-04 y evidencia del ensayo en la versión publicada.

**Avance de la prueba de humo · 05/11/2026.** La rama de backend `test/f04-humo-gateway`, commit `57f3465`, incorpora `pruebas/verificar_humo_f04.py`. Se ejecuta desde la raíz del backend con `python pruebas/verificar_humo_f04.py --local` para levantar y retirar un entorno desechable, o con `--gateway-url` y tokens de usuario en variables de entorno para consultar un despliegue existente. Comprueba salud del Gateway, `401` sin token, `403` sin rol de gestor y `200` con gestor. Un resultado incorrecto termina el proceso con código `1`. El informe de cada ejecución queda en `pruebas/resultados/humo-f04.json`, fuera de Git y sin tokens ni datos de despachos.

**Verificación local realizada.** Las cuatro comprobaciones aprobaron contra Gateway, Gestión y Operación reales, con PostgreSQL desechable y tokens del emisor temporal de Seguridad local. El entorno temporal se retiró al finalizar. También aprobaron las seis pruebas del verificador y `clean verify` de los tres servicios, con 28 pruebas de Gateway, 189 de Gestión y 131 de Operación, sin fallos ni pruebas omitidas. Este resultado acredita salud y autorización del listado de F-04 en ese entorno; quedan pendientes la conexión al pipeline y la repetición con sesiones reales de G7 en nube, coordinadas con Kevin cuando esté listo el despliegue.

## 4. Dependencias y orden de ejecución

| Momento | Trabajo en paralelo | Condición para avanzar |
|---|---|---|
| **Primero** | Tarqui confirma alcance. Kevin compara plataformas y prepara el ambiente. Valqui inventaría APIs y datos. Max revisa el contrato de sesión. Gerardo prepara los casos y el reporte. | Cada persona tiene un tramo, un criterio de cierre y un entorno acordado. Las pruebas locales pueden empezar mientras G7 confirma las cuentas. |
| **Integración** | Kevin conecta servicios y verifica CI/CD. Max conecta sesión y F-03. Tarqui verifica asignación. Valqui prepara cobertura y contrasta los contratos. Gerardo verifica F-04 y prepara la prueba posterior al despliegue. | La versión publicada responde y rechaza el acceso anónimo a F-04. G7 confirma las cuentas y, si aplica, los orígenes. Kevin verifica los vínculos de F-05 y la comunicación interna para reservar y liberar capacidad. |
| **Ensayo y cierre** | Los cinco recorren el mismo despacho. Gerardo registra resultados, Tarqui valida el alcance y Kevin identifica la revisión ejecutada. | Cada paso tiene evidencia asociada al mismo caso. Los fallos y dependencias pendientes quedan identificados con responsable. |

### 4.1 Pedido inicial a Seguridad

Tarqui y Gerardo confirman con G7 el ambiente y la fecha de prueba. Pedir **un gestor con MFA y dos repartidores sin rol global**, con sus enlaces de activación si faltan. G7 comunica los UUID de los repartidores y Kevin los vincula en F-05. Max aporta las URLs exactas de ambas apps si el navegador llama directamente a G7, para confirmar los orígenes permitidos.

### 4.2 Comunicación entre servicios

G2 acordó autorizar las llamadas entre Gestión y Operación por **identidad del servicio autorizado para la operación**. Los seis scopes internos quedan fuera del pedido a G7. El contrato y el backend actuales todavía los exigen. Antes de cambiar el código, Kevin y Valqui deben definir con los responsables cómo emitir una credencial interna con la audiencia esperada. G7 deriva la audiencia de los scopes concedidos, así que una credencial emitida para Ventas o Seguridad puede tener otra audiencia.

El login de las aplicaciones y la preparación de pruebas pueden avanzar en paralelo. La **demo completa** requiere además que Gestión y Operación puedan reservar y liberar capacidad en el ambiente publicado. Las credenciales de integraciones externas se coordinan por separado, según lo que se vaya a demostrar.

## 5. Evidencia para la sustentación

| Criterio | Qué abrir o ejecutar |
|---|---|
| **CI/CD** | PR y SHA → ejecución del pipeline → reportes de build, compilación y pruebas → revisión publicada → resultado de la prueba de humo. |
| **Diseño de APIs** | Inventario y Swagger → operación y contrato → petición real con éxito y con error → controlador o prueba que lo respalda. |
| **Seguridad en pantallas y APIs** | Login con G7, MFA del gestor, ruta propia del repartidor, rechazo al despacho ajeno y `401` sin token en una API protegida. Mostrar códigos HTTP y ocultar tokens y secretos. Registrar aparte la comprobación de identidad de servicio entre Gestión y Operación. |
| **Demo funcional** | Asignación → traslado → fallo con evidencia → recepción → liberación de capacidad y reprogramación. Mostrar los mismos IDs y los estados antes y después. |
| **Prácticas DevOps y versionado** | ADR de nube, comparación de herramientas, rama y revisión por pares, changelog, tag o SHA y revisión publicada. Cada integrante puede explicar su aporte con evidencia del equipo. |
| **Webhook** | Contrato Despacho → Ventas/Postventa, registro del evento en la bandeja de salida y código de envío. Explicar reintentos y deduplicación por `idEvento`. Si se ejecuta con Ventas, guardar la confirmación de recepción aparte. |

## 6. Qué se toma de la teoría

- **TEO 08, diaps. 4, 7, 19, 21–23 y 25.** Ambientes, prueba de humo, decisión de nube, elección de CI/CD, trazabilidad de la versión y evidencia de prácticas DevOps. Kevin lidera la decisión de nube y cada integrante prepara su sustentación. Las prácticas de Eventos de las diapositivas 13 y 24 corresponden al laboratorio.
- **TEO 09, diaps. 16–19 y 25.** Contratos verificables, OpenAPI/Swagger, pruebas de contrato, JWT y análisis de webhook. La diapositiva 25 aplica al proyecto. Si se pide también la práctica en parejas de la diapositiva 19, planificarla aparte con una entidad de más de diez columnas y las siete operaciones solicitadas. El CRUD de Eventos de la diapositiva 14 corresponde al laboratorio.

## 7. Referencias de trabajo

- Material del curso — TEO 08 Despliegue en Nube y CI/CD y TEO 09 Diseño de APIs y API REST.
- [Índice de funcionalidades](../funcionalidades/funcionalidad.md) · [Flujo de contribución y versiones](../CONTRIBUTING.md)
- [Contratos de integraciones externas](../integraciones/api-contract.md) · [API de Gestión](../integraciones/api-contract-gestion-despachos.md) · [API de Operación](../integraciones/api-contract-operacion-reparto.md)
- [Workflow de backend](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/develop/.github/workflows/ci.yaml) · [Workflow de frontend](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/blob/develop/.github/workflows/ci.yaml)
- Material de G7 — Kit de integración, matriz de scopes y SPEC-17 de tokens de servicio. Borrador de coordinación de G2 — `solicitud-integracion-seguridad.md`, en el espacio de trabajo compartido.
- [Evidencia y pendientes de F-04](../especificaciones/ES-F04-03-ConfirmarRecepcionPaquete/evidence.md) · [Validación de F-05/F-06](../especificaciones/ES-F06-01-AbrirJornada/evidencia/validacion.md)
