# Evidencia de ES-F04-04: Reprogramar un despacho fallido

**Estado:** Implementación local de Gestión y frontend verificada; aceptación conjunta e integraciones externas pendientes.

**Responsable de verificación:** Codex ejecutó las comprobaciones; Gerardo conserva la coordinación y la revisión humana pendiente.

**Última verificación funcional:** 24/10/2026, America/Lima.

## 1. Versión y entorno verificados

- Rama común: `feature/f04-reprogramar-despacho-fallido`, desde backend `60855de`, frontend `af94b54` y especificaciones `542a483`.
- Backend implementado: [57bd6ef](https://github.com/Taller-SW-Web/G2-Despacho-Backend/commit/57bd6ef507255d4104dc3306100fca8d44b021e7). Frontend implementado: [339cd66](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/commit/339cd66b04815308ef67409220e9baf77f237def). Este registro no declara despliegue ni merge.
- Gestión: Java 21, Spring Boot 4.1.1, Maven Wrapper, Docker y PostgreSQL 17/PostGIS 3.6 desechable con Testcontainers. No se usó Supabase ni la base de trabajo local.
- Frontend: React/Mantine existentes, Vitest/Testing Library/JSDOM y Playwright con Edge instalado. Navegador en `Asia/Tokyo`; el reloj del escenario HTTP es `2026-10-25T03:30Z`, todavía 24/10 en Lima.
- Se conserva la preparación SDD del 16/10 sobre `c8e6e29`; las bases antiguas `d2bc27d`/`1e7834b` describían inspección documental, no esta ejecución.
- Alcance modificado: F-04 del administrativo, paquete `incidencias` de Gestión, pruebas, V3 y documentación necesaria. Operación, su base, Gateway y contratos no se modificaron.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación ejecutada | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03/04/06/07 | HTTP, transacción, estado/fecha/versión, mismo contador, historial y evento. | EV-01/03 | Aprobado |
| CA-02 | T-02/04/06 | Fecha estricta, hoy/pasado, medianoche Lima/UTC y selector con navegador en otra zona. | EV-01/03 | Aprobado |
| CA-03 | T-02/04/06 | Máximo dinámico, igual/superado y 422; bloqueo UI desde detalle/POST. | EV-01/03 | Aprobado |
| CA-04 | T-04/05/06 | Incidencia/versión sustituidas y estado incompatible; sin actualización silenciosa. | EV-01/02/03 | Aprobado |
| CA-05 | T-04/06 | Recepción vigente pendiente; no hereda otra recepción. | EV-01/03 | Aprobado |
| CA-06 | T-04/07 | NO_INTENTADO conserva cero; caso base conserva uno; límite vigente independiente del motivo. | EV-01 | Aprobado |
| CA-07 | T-04/05/06 | Recepción antes que anulación; anulación antes que límite; rechazo sin escrituras. | EV-01/03 | Aprobado |
| CA-08 | T-03/05/06 | Resultado durable tras medianoche, reconstruir repositorio, otra salida y respuesta perdida real. | EV-02/03 | Aprobado |
| CA-09 | T-02/04/06 | Tipos/formato/campos/query estrictos, Unicode, espacios y 500/501 puntos de código. | EV-01/03 | Aprobado |
| CA-10 | T-05 | Otro contenido/actor en identidad aceptada: 409, sin sobrescritura. | EV-02 | Aprobado |
| CA-11 | T-05/07 | Carreras reales entre reprogramaciones y escritores SQL controlados de cierre/anulación. Falta competir con sus APIs reales. | EV-02/04 | Pendiente |
| CA-12 | T-06/07 | Sale de fallidos, detalle histórico y cola real de F-02; fecha futura bloquea asignación. Falta nueva reserva/asignación completa. | EV-01/03/04 | Pendiente |
| CA-13 | T-03/04/07 | Liberación pendiente/de revisión e instantáneas conservadas; incidencia posterior preparada sin heredar recepción. Falta productor F-03 real. | EV-01/04 | Pendiente |
| CA-14 | T-04/05/07 | Rollback en cada escritura; receptor HTTP devuelve 503/204 y el mismo evento se recupera fuera de transacción. | EV-01/02 | Aprobado |
| CA-15 | T-04/06 | 401/403 antes de datos y 404 autorizado; UI retira resumen/campos y descarta respuestas tardías. | EV-01/03 | Aprobado |
| CA-16 | T-04/07 | Zona inactiva, identidad/destino/carga preservados; simulado sin evento. | EV-01 | Aprobado |
| CA-17 | T-02/06 | Doble envío, errores, GET antes de replay exacto, recuperación tras cerrar y retorno con filtros/éxito. | EV-03 | Aprobado |
| CA-18 | T-04 | Política ausente, no entera, no positiva o desbordada: 500, sin valor inventado. | EV-01 | Aprobado |
| CUI-01 | T-01/02/06/08 | Contexto fijo, retorno y consulta de origen; página desaparecida corregida. | EV-03 | Aprobado |
| CUI-02 | T-01/02/06/08 | Fecha inicial vacía, civil, Lima y calendario en español. | EV-03 | Aprobado |
| CUI-03 | T-01/02/06/08 | Observación opcional, normalización y emojis sin truncamiento. | EV-03 | Aprobado |
| CUI-04 | T-01/02/06/08 | Bloqueos vigentes y rechazo de contexto sustituido. | EV-03 | Aprobado |
| CUI-05 | T-01/02/06/08 | Un POST, controles/cierre bloqueados y resultado anunciado. | EV-03 | Aprobado |
| CUI-06 | T-01/02/06/08 | Rechazos y recuperación conservan identidad; GET no atribuye aceptación propia. | EV-03 | Aprobado |
| CUI-07 | T-01/02/06/08 | Éxito conservado ante listado fallido y actualización sin repetir POST. | EV-03 | Aprobado |
| CUI-08 | T-01/02/06/08 | Foco contenido/retornado, móvil y reflujo equivalente al 200 % automatizados; 401/403. Revisión visual humana y zoom nativo pendientes. | EV-03 | Pendiente |

`Aprobado` acredita el comportamiento en el entorno descrito, sin convertir dobles en integración del proveedor real. La aceptación global sigue abierta por las filas pendientes.

## 3. Registros de verificación

### EV-01. Persistencia, fecha y seguridad

- Ejecutado por Codex el 24/10/2026. Código: [57bd6ef](https://github.com/Taller-SW-Web/G2-Despacho-Backend/commit/57bd6ef507255d4104dc3306100fca8d44b021e7).
- Artefactos: `ReprogramacionDespachoHttpTests`, `SolicitudesReprogramacionTests` y regresión `RecepcionCentroHttpTests`, bajo `servicio-gestion-despachos/src/test/java/com/modulodespacho/gestiondespachos/servicio_gestion_despachos/`.
- Desde Gestión: `.\mvnw.cmd clean verify`. Resultado final: **BUILD SUCCESS: 133 pruebas, 0 fallos, 0 errores y 0 omitidas**; incluye 21 HTTP de reprogramación, 3 unitarias del parser y regresión.
- Migración `V3__reprogramaciones_despacho.sql`: esquema vacío y actualización desde V2 con datos sintéticos preservados, sin fabricar comandos anteriores. V1/V2 permanecen intactas.
- Se comprobó recepción por incidencia, orden de errores, máximo vigente válido/inválido, fechas civiles/Lima, tipos estrictos, ausencia de escrituras en rechazos, referencias completas, contador y datos originales.
- La captura común `HistorialIncidenciasJdbc` exige transacción activa y la comparte recepción; insertar historial no confirma una transacción independiente. La aceptación de ES-F04-06 completa permanece fuera de este cambio.
- Resultado: Aprobado dentro de Gestión real y su base aislada. JWT de pruebas controlado; no acredita firma/JWKS del proveedor de Seguridad.

### EV-02. Concurrencia y recuperación durable

- Ejecutado por Codex el 24/10/2026. Código: [57bd6ef](https://github.com/Taller-SW-Web/G2-Despacho-Backend/commit/57bd6ef507255d4104dc3306100fca8d44b021e7); mismas pruebas y comando de EV-01.
- Dos transacciones PostgreSQL simultáneas: solicitud exacta obtiene 200/200 con una decisión; contenido o actor distintos obtienen 200/409. Las escrituras competidoras de cierre/anulación comparan la versión canónica y solo una mutación gana.
- Cierre/anulación son **escritores SQL de prueba**, no sus endpoints: no se declara integración de ES-F04-05 ni ES-F02-07.
- Replay devuelve el cuerpo original después de cambiar el día, reconstruir el repositorio, sustituir la incidencia o invalidar la política actual. Se comprueba cuerpo corrupto como inconsistencia y contenido/actor incompatible como conflicto. No se ejecutó un reinicio completo del proceso/JVM con la misma base.
- Reloj con nanosegundos: aceptación y persistencia usan microsegundos, precisión de PostgreSQL, para recuperar exactamente el mismo instante. El UUID del ejecutor reconoce su representación en mayúsculas/minúsculas sin atribuir el resultado a otro usuario.
- Fallo inducido en despacho, historial, outbox o registro durable revierte todas las escrituras; la recuperación posterior solo acepta una decisión.
- Outbox real de Gestión hacia receptor HTTP controlado: dos 503 y después 204; mismo id/payload en tres entregas, un solo evento y estado local conservado. La credencial se solicita fuera de transacción.
- Resultado: Aprobado para replay/concurrencia local; carrera con APIs de cierre/anulación reales pendiente en EV-04.

### EV-03. Modal, contrato y accesibilidad

- Ejecutado por Codex el 24/10/2026. Código: [339cd66](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/commit/339cd66b04815308ef67409220e9baf77f237def); Gestión: [57bd6ef](https://github.com/Taller-SW-Web/G2-Despacho-Backend/commit/57bd6ef507255d4104dc3306100fca8d44b021e7).
- `npm run test:f04`: **53 pruebas aprobadas de 53**, en 6 archivos. Incluye 19 casos del nuevo modal, 2 del recorrido detalle/listado y regresiones de recepción/listado/detalle/sesión.
- `npm test`: **207 aprobadas y 1 fallida de 208**. El fallo heredado es `ShellAdministrativo.test.tsx`, CCR-03-02: espera 2 enlaces y recibe 3. Reproducido al ejecutar ese archivo por separado; `git diff af94b54 -- packages/componentes-compartidos` vacío confirma que sus fuentes/pruebas no cambiaron en esta rama. No se corrigió un componente de otro alcance. `npm run typecheck` y `npm run build`: **ambos aprobados**; Vite advierte de bundles mayores a 500 kB, sin impedir el build de las dos aplicaciones.
- `npm run test:f04:e2e` con `PLAYWRIGHT_F04_CHANNEL=msedge`: **1 prueba aprobada de 1 (10,1 s)**, con la implementación final. Arranque reproducible `ReprogramacionNavegadorPruebas` documentado en README backend; aplica Flyway y reutiliza un escenario sintético en PostgreSQL desechable.
- Cadena observada: navegador → Vite/proxy de pruebas → Gestión HTTP real → PostgreSQL. Se acepta el POST en servidor y se corta deliberadamente su respuesta; cerrar/reabrir, consultar estado histórico y repetir el comando original recuperan el mismo 200, con un historial/evento y contador intacto. No se sustituye el comando con la incidencia que devuelva el GET.
- Se verificaron foco contenido y retorno al disparador, foco en título de listado, controles bloqueados durante envío, calendario español y fecha civil con navegador en Tokio. Móvil 390×844 y reflujo equivalente a 200 % (720×512 CSS, DPR 2 sobre 1440×1024 físicos); acciones alcanzables mediante scroll.
- Capturas del recorrido: [escritorio](./evidencias/modal-escritorio.png), [móvil](./evidencias/modal-movil.png) y [reflujo equivalente al 200 %](./evidencias/modal-escala-200.png).
- Los errores 400/409/422/500/503, autorizaciones revocadas y fallos de refresco se cubren además con fixtures explícitos de JSDOM. No acreditan una API externa.
- Límites: la herramienta de revisión manual del navegador falló al inicializar; se usó el recorrido automatizado y se inspeccionaron sus capturas. Revisión humana/zoom nativo pendientes. El proxy no acredita Gateway desplegado; JWT controlado y Operación no disponible en este recorrido.
- Resultado: Aprobado para implementación local/HTTP/UI automatizada; CUI-08 y cierre de T-06 conservan sus pendientes de aceptación conjunta.

### EV-04. Recorrido real de reprogramación

- Gestión y PostgreSQL reales: recepción ES-F04-03 → reprogramación → detalle histórico y salida de fallidos → cola F-02 marcada como reintento → rechazo de asignación futura.
- La liberación original pendiente/de revisión permanece intacta; no se llama a Operación para decidir ni se crea otra reserva. Otra incidencia sintética no hereda recepción.
- El emisor real de outbox se probó contra receptor HTTP controlado, con fallo y recuperación. Despacho simulado sin evento externo.
- Pendiente: Gateway/Seguridad reales, liberación efectiva en Operación, asignación a partir de su fecha con otra reserva, siguiente fallo originado por F-03 y cierre/anulación por sus APIs reales. La recepción real del webhook en Ventas requiere destino/credenciales del equipo.
- Responsable de coordinación: Gerardo con propietarios de F-02/F-03/F-06, Operación, Seguridad y Ventas. No se amplió la implementación hacia esos servicios.
- Resultado: Pendiente para el recorrido completo entre equipos; los tramos locales anteriores están acreditados en EV-01/02/03.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas e instrucción conservada | Revisión humana |
|---|---|---|---|
| Preparación SDD inicial. | Codex, 16/10/2026. | Revisión `c8e6e29`, plantillas, contratos/modelo/diseño; organizar ES-F04-04/05/06 sin atribuir implementación. | Gerardo; revisión de preparación pendiente en el registro original. |
| Implementación y verificación local de ES-F04-04. | Codex, 24/10/2026. | Solicitud de este chat: implementar frontend/backend, misma rama sin prefijo codex, commits y pruebas; solo Gestión/F-04 y actualización necesaria de SDD. Fuentes: spec/ui/plan/tasks, AGENTS, contratos y modelo vigentes. | Gerardo; revisión técnica/visual y aprobación de PR pendientes. |

## 5. Diferencias, fallos y pendientes

| Hallazgo | Impacto | Siguiente acción |
|---|---|---|
| V1/V2 no contenían registro durable de reprogramación. | Se añadió únicamente V3 en Gestión. | Aplicarla por el procedimiento de despliegue del equipo tras revisar su entorno; no se aplicó sobre bases persistentes. |
| F-02/Operación/F-03 y APIs de cierre/anulación no completaron este recorrido. | CA-11/12/13 y T-07 no pueden cerrarse con dobles. | Coordinación de Gerardo con sus propietarios; sin modificar otro microservicio. |
| Gateway, firma real de Seguridad y receptor real de Ventas no participaron. | No se declara integración/despliegue de esos proveedores. | Verificar el entorno conjunto con sus credenciales. |
| Revisión humana y zoom nativo no ejecutados. | CUI-08 y T-08 pendientes de aceptación final. | Gerardo y responsable UI revisan capturas y recorrido. |
| Regresión heredada de CR-03: 207/208 compartidas aprobadas; CCR-03-02 espera dos enlaces y recibe tres. | Fuera de F-04 y sin cambios de fuente/prueba en esta rama. | Coordinar con responsable del componente; fallo reproducido por separado. |
| Fallos iniciales de aserciones del calendario/tiempos de transición y métricas de ampliación. | Se corrigieron sincronización del test, nombres accesibles y emulación de reflujo; no se omitieron controles del modal. | Resultados finales registrados en EV-03. |

## 6. Entrega y revisión

- Commits de implementación: [57bd6ef](https://github.com/Taller-SW-Web/G2-Despacho-Backend/commit/57bd6ef507255d4104dc3306100fca8d44b021e7) y [339cd66](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/commit/339cd66b04815308ef67409220e9baf77f237def); sin push, PR, merge ni despliegue realizados por esta implementación.
- Estado del alcance propio: implementado y comprobado localmente. T-01 a T-05 cerradas; T-06/07/08 mantienen los pendientes descritos.
- Revisor/fecha/resultado de revisión humana: pendientes.
- Aceptación global de la especificación: abierta hasta completar los criterios e integraciones pendientes; no se la declara terminada solo por compilar.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md), [UI](./ui.md), [plan](./plan.md) y [tareas](./tasks.md).
- [cite: 2] [Gestión §5.2.2](../../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04), [modelo](../../arquitectura/modelo-datos.md) y [guía SDD](../../plantillas/sdd/README.md).
