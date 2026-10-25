# Evidencia de ES-F04-05: Cerrar un despacho como devuelto a origen

**Estado:** Implementación local verificada; integración conjunta y revisión humana pendientes.

**Responsable de verificación:** Gerardo. Ejecución asistida por Codex.

**Última verificación funcional:** 24/10/2026, America/Lima.

## 1. Versión y entorno verificados

- Rama común: `feature/f04-cerrar-devuelto-origen` en los tres repositorios.
- Bases: backend `8fff3d9` y frontend `0989de1`, desde `develop`; Specs `d833e55`, desde `main` según CONTRIBUTING. Se contrastaron con `origin`; sin cambios remotos adicionales.
- Backend `124727b` y frontend `b6823ed`: implementación, pruebas e instrucciones reproducibles; detalle en §6.
- Windows, Java 21, Maven Wrapper, Docker Desktop y PostgreSQL 17/PostGIS desechable mediante Testcontainers. Flyway V1 a V4; ninguna prueba usa Supabase ni la base persistente de trabajo.
- Frontend React/Mantine existentes, Vitest/Testing Library/JSDOM y Playwright con Edge instalado. Sin dependencias nuevas.
- Alcance backend: exclusivamente Gestión de Despachos; sin cambios en Operación ni Gateway. El navegador utiliza un proxy de pruebas, no acredita el Gateway desplegado.
- Identidad JWT y productores externos controlados. Los eventos se entregaron por HTTP a un receptor de prueba; no se acredita procesamiento comercial de Ventas.

## 2. Cobertura de criterios

`Aprobado` en esta matriz significa comprobación local en el entorno y con los límites de EV-01 a EV-04. No equivale a aceptación humana ni integración de los servicios desplegados [cite: 1, 2].

| Criterio | Tareas | Comprobación observada | Registro | Resultado local |
|---|---|---|---|---|
| CA-01 | T-03/04/06/07 | 200, estado final, versión, motivo normalizado, historial con resultado original y evento atómicos. | EV-01/03 | Aprobado |
| CA-02 | T-03/05/06 | Mismo cuerpo tras recrear el servicio, avanzar tres días y cambiar comunicación/liberación; GET antes del replay en UI. | EV-02/03 | Aprobado |
| CA-03 | T-04/07 | Seis errores HTTP del receptor controlado dejan ENVIO_FALLIDO; conserva cierre/idEvento; reenvío controlado del mismo evento. | EV-04 | Aprobado |
| CA-04 | T-02/04/06 | Recepción pendiente, incluida otra incidencia histórica recibida, rechazada con 409. | EV-01/03 | Aprobado |
| CA-05 | T-02/04/06/07 | Anulación no bloquea cerrar tras recibir; no genera otra cancelación. | EV-01/03 | Aprobado |
| CA-06 | T-02/04/06 | Tipos, campos extra, parámetros, versiones, motivo ausente y 500/501 puntos Unicode; observación opcional normalizada. | EV-01/03 | Aprobado |
| CA-07 | T-04/06 | 401/403/404; token de servicio rechazado; sesión revocada retira resumen/campos y descarta respuesta tardía. | EV-01/03 | Aprobado |
| CA-08 | T-02/04/07 | Cero, uno, dos y tres intentos, NO_INTENTADO, anulación y decisión explícita; contador conservado. | EV-01/03 | Aprobado |
| CA-09 | T-05/06 | Versión/incidencia/estado incompatibles responden 409; el modal exige revisar. | EV-02/03 | Aprobado |
| CA-10 | T-03/05/07 | Dos cierres, actores y contenidos distintos, cierre/reprogramación real y anulación controlada: una mutación por versión. | EV-02 | Aprobado |
| CA-11 | T-04/07 | Liberación original pendiente/de revisión preservada; procesador continúa después del cierre sin cambiar versión. | EV-01/04 | Aprobado |
| CA-12 | T-03/04/05 | Referencias inconsistentes y recepción sin solicitud rechazan; fallo inyectado en cada escritura revierte el conjunto; metadatos incompletos no fabrican éxito. | EV-01/02 | Aprobado |
| CA-13 | T-03/04/07 | Identidad, fecha, destino, carga, referencias, incidencia/recepción conservados; simulado sin evento. | EV-01 | Aprobado |
| CA-14 | T-02/06 | Doble envío bloqueado, conflictos, timeout/503, replay exacto, 200 seguido de lectura fallida, navegación y foco. | EV-03 | Aprobado |
| CA-15 | T-04/06/07 | Ausente de fallidos/cola; detalle final consultable, acciones bloqueadas y controlCierre fuera de la proyección pública. | EV-01/03 | Aprobado |
| CUI-01 | T-01/02/06 | Contexto leído antes de habilitar; resumen y motivo del fallo separados. | EV-03 | Aprobado |
| CUI-02 | T-01/02/06 | Motivo libre requerido y longitudes Unicode de ambos textos; sin truncar emojis. | EV-03 | Aprobado |
| CUI-03 | T-01/02/06 | Cierre explícito con anulación, límite, NO_INTENTADO y capacidad pendiente. | EV-03 | Aprobado |
| CUI-04 | T-01/02/06 | Un POST; campos, Escape y cierre accidental bloqueados durante envío. | EV-03 | Aprobado |
| CUI-05 | T-01/02/06 | 409 exige nueva lectura/revisión; no traslada motivo a otra identidad. | EV-03 | Aprobado |
| CUI-06 | T-01/02/06 | Conserva solicitud desconocida al cerrar/reabrir; consulta antes de repetir; distingue inconsistencia 500. | EV-03 | Aprobado |
| CUI-07 | T-01/02/06 | Conserva éxito si falla listado; filtros/tamaño/página y foco restaurados; no afirma procesamiento comercial. | EV-03 | Aprobado |
| CUI-08 | T-01/02/06 | Teclado/foco, móvil, reflujo equivalente a 200 %, etiquetas y retirada de datos por permisos. | EV-03 | Aprobado |

## 3. Registros de verificación

### EV-01. Cierre, datos y seguridad

- Backend: `CierreDespachoHttpTests` (15 pruebas) y `SolicitudesCierreTests` (3); ambas suites también se ejecutaron de forma focalizada. Suite completa de Gestión: **157 pruebas, cero fallos/errores/omisiones**, mediante `.\mvnw.cmd clean verify`.
- HTTP MockMvc con filtros de seguridad reales y `JwtDecoder` controlado; JDBC, transacciones, Flyway y PostgreSQL reales.
- Se contrastaron datos del despacho antes/después excluyendo únicamente estado, versión y actualización; recepción, motivo original, observación de recepción, reserva, jornada y solicitud de liberación permanecen.
- La ampliación de casos reales/simulados con anulación, límite y NO_INTENTADO se verificó además con una ejecución focalizada de ese método: ocho combinaciones, un evento solo para reales y respuesta idEvento null solo para simulados.
- V4 crea un índice único parcial en `historial_estados_despacho`, sin tabla de cierres. Se verificó base vacía, actualización desde V3 con cierre histórico sin controlCierre y SQLState `23505` ante otro cierre final. No se fabrican respuestas históricas.
- Pruebas de seguridad, formato, anulación/límite/NO_INTENTADO, simulado, consultas y proyección pública en las clases citadas.
- Resultado local: **Aprobado**. La migración no se ejecutó sobre una base compartida.

### EV-02. Concurrencia y resultado original

- Transacciones concurrentes reales con barrera inicial: duplicado exacto devuelve dos 200 con cuerpos iguales; otro motivo o ejecutor produce 200/409, un historial, un evento y un incremento de versión.
- Cierre compite con el endpoint real de reprogramación y con un productor SQL de anulación controlado que compara la misma versión. El segundo no acredita integración con Ventas/F-02 desplegados.
- Recreación de `CierreDespachoJdbc`, reloj avanzado tres días y cambios técnicos en comunicación/liberación conservan el cuerpo original. Prueba de precisión a microsegundos.
- Triggers de fallo antes de UPDATE de despacho e INSERT de historial/evento verifican rollback total y respuesta 503. Recuperación con metadatos incompletos responde 500, sin reconstruir un éxito desde estado actual.
- Resultado local: **Aprobado**. La recreación del componente prueba ausencia de caché en memoria; no se ejecutó un reinicio de un despliegue productivo.

### EV-03. Modal, recuperación y accesibilidad

- `npm.cmd run test:f04 -- --maxWorkers=1`: **77 pruebas aprobadas**, ocho archivos, con APIs simuladas. Incluye **22 pruebas nuevas** del modal y **dos** del recorrido cierre → listado, además de regresión de recepción/reprogramación/detalle/sesión.
- `npm run typecheck`: correcto para componentes compartidos y ambas aplicaciones. `npm run build`: correcto para ambas; Vite conserva advertencias de tamaño de chunks, sin errores de construcción.
- `npm run test:f04:cierre:e2e` con `PLAYWRIGHT_F04_CHANNEL=msedge`: **un recorrido aprobado** con Gestión HTTP, Flyway y PostgreSQL reales, JWT sintético, proxy exclusivo y sin Operación/Ventas desplegados.
- Se abortó la primera respuesta después del 200 del servidor. El modal conserva el comando, se cierra/reabre, consulta y repite exactamente; dos respuestas idénticas, un cierre/historial/evento, contador conservado y liberación pendiente. El GET no se usa como prueba de autoría.
- Navegación conserva filtros, ajusta una página desaparecida y enfoca el encabezado del listado. La pérdida de lectura posterior al éxito se comprueba con fixtures y solo reintenta el GET.
- El navegador comprueba foco contenido, retorno al disparador, bloqueo de otras decisiones mientras el cierre sea desconocido, validación de 500/501 emojis y botones alcanzables mediante desplazamiento en móvil 390×844 y reflujo a 720×512 CSS con DPR 2 (equivalente visual de 200 %, no zoom físico del navegador).
- Capturas revisadas visualmente por Codex: [escritorio](./evidencias/cierre-escritorio.png), [móvil](./evidencias/cierre-movil.png), [acciones móviles](./evidencias/cierre-movil-acciones.png) y [reflujo 200 %](./evidencias/cierre-escala-200.png). Datos completamente sintéticos, sin JWT ni credenciales visibles.
- Los dos recorridos JSDOM inicialmente excedieron el límite de espera de 1 s con las verificaciones concurrentes. Se amplió solo la espera del resultado a 5 s y se ejecutó con un proceso; se conservaron todas las aserciones. Se corrigieron también opciones de selector incompatibles con los tipos de Testing Library y una consulta de prueba que confundía el operador JSON `?` con un parámetro JDBC.
- Resultado local: **Aprobado**. Revisión humana, lector de pantalla y zoom físico en navegador pendientes; JSDOM no acredita layout.

### EV-04. Cierre logístico e integraciones reales

- Recepción, cierre, historial, outbox, consultas y procesadores de Gestión sobre PostgreSQL real.
- Receptor HTTP controlado responde 503 seis veces: mismo payload/idEvento, cierre conservado y `ENVIO_FALLIDO`; al habilitar de forma controlada otro envío del mismo evento se registra `ENVIADO`. No se probó una interfaz de reenvío manual ni se acredita que Ventas aplique el evento.
- Procesador real de liberaciones usa un puerto doble de Operación que confirma la reserva original; completa la solicitud después del cierre y conserva versión 10. No se modifican tablas de otro servicio.
- Navegador integrado confirma estado final, contador, unicidad del historial/evento, continuidad de recepción y retirada de la fila.
- Resultado de integración local: **Aprobado**. Resultado de integración conjunta con Gateway, Seguridad, Operación y Ventas desplegados: **No ejecutado**. T-07 permanece en curso por ese límite.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas e instrucción | Revisión humana |
|---|---|---|---|
| Preparación SDD | Codex, 16/10/2026 | Revisión `c8e6e29`, plantillas, contratos, modelo y diseño; conservar criterios y preparar plan/tareas/evidencia. | Pendiente. |
| Implementación y verificación | Codex, 24/10/2026 | Solicitud de Gerardo: misma rama en tres repositorios, implementar ES-F04-05 según Specs, limitar backend a Gestión, migración siguiente, pruebas, actualización SDD y Conventional Commits en español. | Gerardo; revisión pendiente. |

Se generaron código, pruebas, migración, recorrido de navegador y seguimiento. Los resultados automáticos y la inspección de capturas no se presentan como aprobación humana.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Impacto | Acción pendiente |
|---|---|---|
| Servicios desplegados y credenciales externas fuera del recorrido aislado. | No hay aceptación conjunta ni resultado comercial garantizado. | Gerardo coordina prueba con responsables de Gateway, Seguridad, Operación y Ventas. |
| Anulación concurrente usa productor controlado; liberación usa puerto doble. | No acredita esas integraciones desplegadas. | Completar T-07 en el entorno conjunto. |
| Revisión humana de CA/CUI, lector de pantalla y zoom físico pendientes. | T-08 y aceptación global siguen abiertas. | Gerardo/revisor verifican capturas y criterios. |
| V4 detecta duplicados históricos, sin regularizarlos automáticamente. | Una base con cierres duplicados requiere revisión verificable. | Revisar datos antes de desplegar; no alterar historial Flyway ni inventar respuestas. |

## 6. Entrega y revisión

- Implementación local terminada en frontend y Gestión, migración V4 y documentación actualizada.

| Repositorio | Commit | Título |
|---|---|---|
| Backend | `124727b1eedb26721e953ac2474226052caf79f4` | feat(f04): implementar cierre atómico de despachos a origen |
| Frontend | `b6823ed033e4a3700104fbb955e40ee20c972b60` | feat(f04): integrar cierre de despachos devueltos a origen |

- No se publicaron ramas, PR, tags ni Release; los tres repositorios quedan en su rama de trabajo con commits locales.
- T-01 a T-06 completadas en el entorno local. T-07/T-08 en curso por integración conjunta y revisión humana; no se sustituyen por una aprobación ficticia.
- El commit de Specs que contiene esta evidencia registra el seguimiento; revisión por pares pendiente.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md) y [UI](./ui.md).
- [cite: 2] [Plan](./plan.md) y [tareas](./tasks.md).
- [cite: 3] [Contrato de Gestión §5.2.3](../../integraciones/api-contract-gestion-despachos.md#523-cerrar-como-devuelto-a-origen--es-f04-05), [modelo](../../arquitectura/modelo-datos.md) y [guía SDD](../../plantillas/sdd/README.md).
