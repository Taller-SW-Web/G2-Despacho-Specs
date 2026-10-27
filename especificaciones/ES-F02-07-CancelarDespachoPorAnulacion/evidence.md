# Evidencia de ES-F02-07: Cancelar despacho por anulación del pedido

**Estado:** Implementada y verificada localmente con G2 real y Seguridad temporal. No acredita aceptación humana ni proveedores externos reales.

**Responsable de verificación:** Tarqui.

**Última verificación funcional:** 26/10/2026 (America/Lima).

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md).
- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-08, CA-17, CA-18, CA-19).
- Contratos asociados: Común §7.2/§7.2.1, Gestión §3.2.3 y Operación §5.2. No se incorpora una API de cancelación administrativa.
- Rama `feature/f02-rutas-transferencia-segura`; cambios locales sin commit atribuido. Se conservan el incremento previo de reasignación y los cambios de grafo existentes, sin revertirlos.
- Java 21, PostgreSQL/PostGIS desechables, Docker/Testcontainers y Chromium de Playwright. Gestión migra hasta V7; Operación hasta V7. No se usan bases compartidas ni Supabase.
- Las pruebas HTTP de Gestión controlan identidad y proveedor F-06 explícitamente. El recorrido integrado utiliza Gateway/Gestión/Operación reales y un emisor JWT RS256 temporal de G2; Ventas se representa por un consumidor autenticado de prueba, no por su aplicación comercial real.

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación ejecutada | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-06 | Pendiente pasa a CANCELADO, sale de cola y no llama a F-06. | EV-01, EV-03 | Aprobado localmente y en navegador real |
| CA-02 | T-03, T-04, T-06 | Asignado libera la reserva exacta y confirma cancelación/historial/outbox; conserva cerco ante fallos. | EV-01, EV-03 | Aprobado con F-06/F-03 reales y resiliencia controlada |
| CA-03 | T-03, T-06 | Fallido registra marca temporal, incrementa versión, responde 202; F-04 impide reprogramar y permite cierre tras recepción. | EV-01, EV-02, EV-03 | Aprobado localmente y por API real G2 |
| CA-04 | T-03, T-06 | Traslado ganador produce 409 con estadoActual sin liberar; intención ganadora bloquea traslado. | EV-01 | Aprobado localmente |
| CA-05 | T-03, T-06 | Terminales incluyendo CANCELADO con nueva clave producen 409 sin efectos. | EV-01 | Aprobado localmente |
| CA-06 | T-05, T-06 | Mismo código/cuerpo incluso tras cierre; clave reutilizada rechazada, recuperación y concurrencia sin duplicación. | EV-01 | Aprobado localmente |
| CA-07 | T-02, T-06 | Sin token 401; token humano, otro módulo o scope insuficiente 403 antes de acceder a datos. | EV-01 | Aprobado con identidad controlada |

## 3. Registros de verificación

### EV-01. HTTP y persistencia de cancelación

- Tareas asociadas: T-01 a T-06. Comando de regresión: `./mvnw clean verify` con Java 21 dentro de cada servicio afectado.
- Resultado: **188 pruebas de Gestión** (incluidas **12 de CancelacionHttpTests**) y **123 de Operación**, sin fallos, errores ni omitidas. El primer pase detectó una expectativa antigua de rutas para `CANCELADO`: se sustituyó por prueba explícita de retiro de fotografía, rechazo de reintroducción y conservación histórica; el pase final completo terminó verde.
- `CancelacionHttpTests`: todos los estados; identidad técnica/emisor/scope; UUID, tipos y campos adicionales; mismo comando y reutilización con otro contenido; cancelaciones concurrentes y traslado confirmado primero; bloqueos ante asignación/compensación/reasignación pendiente.
- Timeout real de lectura, respuesta perdida tras liberar, respuesta inválida, motivo remoto ajeno y errores 403/404: intención/cerco conservados, versión local intacta y recuperación sobre la misma reserva. No se llama a reserva inicial ni transferencia para compensar.
- Fallos inducidos en despacho, historial, outbox y confirmación de intención: rollback local, cerco vigente y recuperación hacia adelante. Verifica también huella de ruta, rechazo de movimiento y reasignación, y retiro de cancelado sin perder su posición histórica.
- Nueva instancia de `CancelarDespacho` sobre intención persistida y lease vencido: recuperación sin depender de memoria del coordinador. No equivale a un reinicio real de JVM.
- Webhook HTTP controlado: fallo y reintento conservan cuerpo/idEvento, sin revertir cancelación ni duplicar liberación. No acredita aplicación real de Ventas.

### EV-02. Consumidores React y F-04

- `NODE_OPTIONS=--no-experimental-webstorage npm run test:f02`: **30 aprobadas**; incluye parada con cancelación pendiente fija, sin acción de reasignación, y regresiones de cola/modal/orden.
- `NODE_OPTIONS=--no-experimental-webstorage npm run test:f04`: **77 aprobadas**; consumidores existentes de marca de anulación, recepción, reprogramación y cierre, con APIs simuladas.
- `npm run typecheck` y `npm run build`: correctos.
- Suite administrativa completa en serie: **184 aprobadas y 2 fallidas de 186**. Persisten los dos fallos previos de `Zonas.test.tsx` («retira configuración y filtros si el catálogo revoca el permiso» y «precarga factor nulo y bloquea una tarifa con peso cero»). Sin deshabilitar ni debilitar esas pruebas.
- `CierreDespachoHttpTests` amplía verificación con anulación real por API: marca/versionado, rechazo de reprogramación y cierre sobre versión nueva; en orden inverso, reprogramación ganadora seguida de cancelación del pendiente vigente. PostgreSQL real, identidad controlada.

### EV-03. Recorrido integrado G2

- Comando: `python3 pruebas/verificar_f02_rutas.py` desde backend. El entorno es desechable, sin `.env`, con dos bases separadas y limpieza de sus propios contenedores/red.
- Recorrido de navegador: cancelación por consumidor autenticado de Ventas, retiro de pendiente en cola y de asignado en ruta administrativa/F-03; reintento con misma clave sin doble liberación, capacidad real exacta en kg/m³/paquetes y posiciones restantes conservadas. Verificación de anchuras 1440/1024/390 sin desbordamiento de página.
- Tramo API: prepara un `FALLIDO` por transición interna real (`NO_INTENTADO`, no acredita captura de evidencia en campo), registra anulación, recibe en centro, espera liberación F-06, rechaza reprogramación y cierra por F-04. Conserva el resultado `202` original al repetir después del cierre.
- Resultado final: **3 recorridos Playwright aprobados**, sin fallos ni omitidos: ruta/reordenamiento, reasignación y cancelación. El tramo adicional API terminó con `F02_ANULACION_FALLIDO_VERIFICADO`; el runner completo terminó con `F02_RUTAS_VERIFICADO` y limpió su entorno.
- El primer intento del nuevo escenario buscaba el código operativo en una cola que muestra rastreo; se corrigió el selector al código visible real y se repitió el runner completo. No se sustituyeron respuestas de negocio del escenario por mocks.

## 4. Límites

- No hay transacción distribuida: el cerco bloquea un despacho incierto; las proyecciones y entrega de eventos son eventualmente consistentes.
- El cerco no expira por reloj. Una referencia/motivo incompatible o un proveedor averiado mantiene la intención para recuperación/revisión operativa; no se borra ni sustituye la reserva automáticamente.
- No se acredita Ventas, Productos ni Seguridad G7 reales, aceptación humana o lector de pantalla. Los simulados no generan eventos comerciales externos.
- La inmutabilidad integral de auditoría continúa pendiente en ES-F02-08. Esta entrega no declara completa ni aceptada toda F-02.
