# Evidencia de ES-F02-06: Reasignar despacho a otro repartidor

**Estado:** Coordinación durable, endpoint público y modal implementados y verificados localmente. Aceptación humana y proveedores externos reales pendientes.

**Entrega anterior:** la primitiva local F-06 de Operación §5.3.1 ya estaba probada; por sí sola no acreditaba CA-01. Esta iteración añade la intención, cerco, recuperación hacia adelante y confirmación canónica en Gestión, conforme a Gestión §3.2.2. No se incorpora cancelación comercial.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** 26/10/2026, America/Lima.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-07, CA-15, CA-16).
- Contratos asociados: `integraciones/api-contract-gestion-despachos.md` (§3.2) y `integraciones/api-contract-operacion-reparto.md` (§5.1).
- Rama compartida `feature/f02-rutas-transferencia-segura`; cambios de esta iteración sin commit atribuido. Bases: Backend `d854faa`, Frontend `b4c6ecf`.
- Java 21.0.13, PostgreSQL/PostGIS desechables con Flyway Gestión V1–V6 y Operación V1–V7, Docker y Chromium de Playwright. No se usan bases compartidas ni Supabase.
- `ReasignacionHttpTests`: persistencia y HTTP reales; emisor/decodificador y respuestas de F-06 controlados explícitamente. El recorrido de navegador usa Gateway, Gestión, Operación y sus dos bases reales, con JWT RS256 de Seguridad temporal de G2.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación ejecutada | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-02, T-03, T-04, T-05 | Nueva reserva, versión y posición al final del destino; retiro del origen; ambas capacidades y rutas F-03. | EV-01, EV-03 | Aprobado localmente |
| CA-02 | T-04, T-05 | Motivo vacío/espacios, mismo destino, datos adicionales y cabeceras inválidas; sin transferencia. | EV-01 | Aprobado |
| CA-03 | T-02, T-05 | F-06 rechaza carga por cada dimensión; Gestión conserva rechazo 422 y asignación, sin repetir transferencia. | EV-01 | Aprobado con proveedor controlado y regresión F-06 |
| CA-04 | T-03, T-05 | EN_CAMINO, ENTREGADO, FALLIDO, CANCELADO y DEVUELTO_A_ORIGEN: 409 antes de F-06. | EV-01 | Aprobado |
| CA-05 | T-02, T-05 | Rechazo operativo 409 recordado sin efectos; F-06 distingue saturación de exceso para una carga concreta. | EV-01 | Aprobado con proveedor controlado y pruebas de dominio F-06 |
| CA-06 | T-03, T-05 | Si traslado gana, no se transfiere. Si intención gana, cerco bloquea traslado y movimiento; dos gestores no transfieren dos veces. | EV-01 | Aprobado con PostgreSQL/concurrencia reales |
| CA-07 | T-04, T-05 | Sin token 401; humano sin rol y token de servicio 403 antes de consultar o transferir. | EV-01 | Aprobado con identidad controlada |
| CUI-01 | T-06 | No se ofrecen el conductor/jornada originales. | EV-02, EV-03 | Aprobado |
| CUI-02 | T-06 | Motivo obligatorio no vacío, destino obligatorio y límites de longitud. | EV-02, EV-03 | Aprobado |
| CUI-03 | T-06 | Tres barras con métricas reales/proyección; bloqueo por peso, volumen o paquetes. | EV-02, EV-03 | Aprobado |
| CUI-04 | T-06 | Ref de envío evita doble clic; loading y bloqueo durante resultado incierto; recuperación con el mismo comando. | EV-02, EV-03 | Aprobado |
| CUI-05 | T-07 | Éxito cierra modal y refresca ruta; error de permisos retira datos; respuestas tardías no afectan otra sesión. | EV-02, EV-03 | Aprobado localmente |

## 3. Registros de verificación

### EV-01. Pruebas de integración de la API de reasignación
- Tareas asociadas: T-02, T-03, T-04, T-05.
- Comando: `./mvnw clean verify` en Gestión y Operación con Java 21 y Docker.
- Resultado: **173 pruebas de Gestión** y **123 de Operación**, sin fallos/errores/omitidas. Incluye **9 pruebas `ReasignacionHttpTests`** y regresiones de ruta, asignación, transición, reprogramación y cierre.
- Fallos inducidos al insertar historial, outbox o confirmar intención: rollback local completo, intención pendiente, cerco vigente y recuperación de la misma transferencia. No se llama a liberación/compensación para deshacer una transferencia aceptada.
- Timeout de lectura, respuesta remota perdida tras aceptar y respuesta inválida: resultado desconocido, cerco conservado y misma clave técnica en la recuperación. La ruta refleja el cerco y rechaza mover el despacho.
- Una **instancia nueva del coordinador** retoma la intención persistida tras vencer el arrendamiento. Esto acredita independencia de memoria del coordinador; no se atribuye un reinicio real de JVM a ese test.

### EV-02. Pruebas de componentes React del modal de reasignación
- Tareas asociadas: T-06, T-07.
- Comandos: `NODE_OPTIONS=--no-experimental-webstorage npm run test:f02`, `npm run typecheck` y `npm run build`.
- Resultado: **29 pruebas F-02 aprobadas**, incluidas 9 del modal, 7 de rutas y 13 de cola/asignación. Tipos y construcción correctos.
- Se verifica transporte real del consumidor contra cliente HTTP simulado, comprobación de identidad de respuesta, misma clave/versión/cuerpo al recuperar, descarte bloqueado ante incertidumbre, 422, 409 definitivo/en proceso, 403 y respuestas posteriores al desmontaje. No equivale a verificar servicios reales ni layout.
- Suite administrativa completa con `NODE_OPTIONS=--no-experimental-webstorage npm run test -w @despacho/administrativo -- --maxWorkers=1`: **183 aprobadas y 2 fallidas de 185**, ambas en `Zonas.test.tsx`, previamente reproducidas en el commit base durante la iteración ES-F02-05. Una ejecución paralela inicial también falló en el caso de página desaparecida de `PaginasFlota.test.tsx`; no se reprodujo al ejecutar toda la suite en serie. Se conserva ese límite, sin deshabilitar ni debilitar pruebas. No se atribuye una ejecución nueva de la suite compartida a esta entrega.

### EV-03. Pruebas de flujo E2E
- Tareas asociadas: T-05, T-07.
- Comando desde backend: `python3 pruebas/verificar_f02_rutas.py`; ejecuta `npm run test:f02:rutas:e2e` del frontend.
- Resultado: **2 recorridos aprobados**, ruta/reordenamiento y reasignación. Se crean dos repartidores vinculados y jornadas en bases desechables. El rol global no sustituye el perfil operativo del repartidor.
- La reasignación se confirma por UI con motivo y tres métricas reales; se pierde únicamente la respuesta después de que el servidor acepta y se recupera exactamente la solicitud original. Se verifica retiro de la ruta de origen, ingreso al final de destino y ajustes reales en kg, m³ y paquetes; ambas rutas se consultan por la API F-03 hasta recibir la proyección.
- Capturas sintéticas: [escritorio](../../../G2-Despacho-Frontend/docs/evidencia/f02-reasignacion/modal-1440.png), [tableta](../../../G2-Despacho-Frontend/docs/evidencia/f02-reasignacion/modal-1024.png), [móvil](../../../G2-Despacho-Frontend/docs/evidencia/f02-reasignacion/modal-390.png). Sin desbordamiento horizontal de página; el contenido del modal admite desplazamiento vertical.

## 4. Límites

- Proyecciones eventualmente consistentes: no se promete visibilidad móvil inmediata ni una transacción distribuida.
- El cerco no expira por tiempo; un proveedor/guardado permanentemente averiado mantiene el despacho bloqueado para no permitir entrega desde una asignación incierta. La intención queda disponible para recuperación/revisión operativa.
- Seguridad G7, Productos y Ventas reales, aceptación humana y lector de pantalla no quedan acreditados. La cancelación comercial y la inmutabilidad integral de historial siguen fuera de esta entrega.
- Los fallos generales de frontend se conservan y se registran separadamente; no se declara toda la suite administrativa verde ni se debilitan sus aserciones para ocultarlos.
