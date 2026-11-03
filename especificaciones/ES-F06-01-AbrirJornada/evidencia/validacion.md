# Verificación local de F-06

**Responsable:** Kevin Rhamses Bohorquez con asistencia de Codex. **Estado:** Implementación y pruebas locales verificadas; aceptación desplegada pendiente.

## 1. Revisiones

- Specs base `2b92674`; preparación SDD en `16d358b`, `46e47c7` y `45121ae`. Esta revisión incorpora ajustes de consistencia y resultados reales.
- [Frontend `f73c268`](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/commit/f73c268): componentes compartidos `1bbbdb7`, módulo y pruebas `52321b2`, guía `f73c268`.
- [Backend `3ce1964`](https://github.com/Taller-SW-Web/G2-Despacho-Backend/commit/3ce1964): esquema `d3a2a43`, jornadas `5759224`, integración `389eeaa`, pruebas `0ac58f2` y guía `3ce1964`.
- Autor y committer: identidad Git confirmada `KevinBohorquez`. La asignación funcional original continúa siendo de Luis Alfonso; Kevin asumió el desarrollo por solicitud del usuario.

Entorno Windows, Java 21, Vitest y PostgreSQL 17.11 temporal. Docker ya estaba iniciado por el usuario; Testcontainers creó los contenedores de prueba y no necesitó un proyecto instalado dentro de Docker.

## 2. Comandos y resultados

Los comandos se ejecutan dentro del repositorio o servicio indicado. Las cantidades de suites solapadas no se suman como casos distintos.

| Área | Comando | Resultado observado |
|---|---|---|
| Frontend | `npm run typecheck` | Aprobado en compartidos y ambas aplicaciones |
| Frontend | `npm run build` | Ambas aplicaciones construidas; aviso de bundle administrativo mayor de 500 kB |
| F-06 frontend | `npm run test:f06` | 19 pruebas aprobadas, 4 archivos |
| Regresión administrativa | `npm run test:administrativo -- --maxWorkers=1` | 96 pruebas aprobadas, 11 archivos |
| Regresión compartidos | `npm test -- --maxWorkers=1` | 206 pruebas aprobadas, 16 archivos |
| CR-10/11/14 final | `npm test -- src/indicadores/TarjetaKpi.test.tsx src/feedback/FranjaEstado.test.tsx src/dominio/BarraOcupacion.test.tsx` | 18 pruebas aprobadas |
| Captura del proveedor | `npm run test -w @despacho/administrativo -- src/features/jornadas/contratoBackend.test.tsx` | 1 prueba aprobada con JSON exportado por PostgreSQL real |
| Operación, regresión | `mvn -B verify` | 76 pruebas aprobadas; empaquetado aprobado |
| Operación, compatibilidad final | `mvn -B -Dtest=JornadasPostgresTests,JornadasHeredadasTests,JornadasHttpTests test` | 17 pruebas aprobadas después de ajustar restricciones heredadas y scopes |
| Operación, reglas finales | `mvn -B -Dtest=GestorJornadasTests test` | 15 pruebas aprobadas; incluye rechazo de proyección con reserva ajena |
| Gateway | `mvn -B verify` | 24 pruebas aprobadas; enrutamiento F-06, JWT y bloqueo de rutas internas |
| Gestión, consumidor y tokens | `mvn -B -Dtest=ContratoCapacidadF06Tests,AsignarDespachoTests,ProveedorTokenServicioTests test` | 4 pruebas aprobadas |
| Gestión, regresión completa | `mvn -B verify` | Fallido: 76 pruebas ejecutadas, 38 errores por migraciones duplicadas V3 preexistentes |

La primera regresión administrativa paralela encontró un timeout de espera en una prueba F-04 existente. Se repitió con un solo trabajador y aprobaron las 96 pruebas sin modificar el código ni la prueba F-04. Durante la implementación se corrigieron referencias de métodos Java al aplicar nomenclatura, codificación UTF-8 del SQL y la configuración del token de prueba para aislar scopes. Los resultados finales anteriores corresponden a las correcciones verificadas.

### 2.1. Trazabilidad de casos

- `CalculoOcupacionTests`: prioridad de estados, saturación dimensional y retorno retenido.
- `GestorJornadasTests`: fotografía, fecha, habilitación, resumen global, exclusión de candidatos, cierre, idempotencia, conflicto de clave, dimensiones excedidas, reserva previa, referencia de liberación y propiedad del contexto/cierre.
- `ConsultaZonaHttpTests`: DTO real F-01 con `id` y `estado=ACTIVO`, zona inactiva y dependencia indisponible.
- `JornadasHttpTests`: roles, formatos, errores por dimensión, sujeto técnico y scopes separados. Un token que solo reserva no puede liberar ni proyectar.
- `JornadasPostgresTests`: transacciones y auditoría reales, reservas concurrentes, cierre frente a reserva, proyecciones versionadas, retención hasta liberar, repetición del cierre propio anterior, exportación del proveedor y medición local.
- `JornadasHeredadasTests`: esquema singular, vista plural preexistente y `pedido_id` UUID obligatorio antes de adaptar; CRUD F-05, jornada, reserva, proyección de código no UUID, cierre y liberación sobre PostgreSQL real.
- `ContratoCapacidadF06Tests`: adaptador F-02 existente consume confirmación y liberación capturadas del proveedor F-06 real; verifica credencial e idempotencia en el transporte controlado.
- `modelo.test.tsx`, `PaginaJornadas.test.tsx`, `useConsultaJornadas.test.tsx` y `contratoBackend.test.tsx`: validación, identidad y paginación, URL, KPI globales, ocupación, apertura/cierre/detalle, respuesta incierta, red, autorización y descarte de respuestas tardías.

Los JWT y la consulta de zona son dobles en las pruebas PostgreSQL. El adaptador HTTP de zonas se prueba con servidor simulado. Las capturas contienen exclusivamente datos sintéticos y no tokens. Estos casos no acreditan comunicación con Seguridad real.

## 3. Supabase y medición

Se inspeccionaron solo metadatos y conteos de Operadores y Flota. Se detectaron una vista `proyecciones_despacho` existente y el campo histórico `pedido_id` UUID obligatorio. El script conserva columnas de la vista en su orden, conserva valores históricos y permite códigos externos en el nuevo `id_pedido`.

La adaptación F-06 se verificó primero en PostgreSQL aislado, después en Supabase con `ROLLBACK` obligatorio y finalmente con `COMMIT`. Tras el ensayo revertido no existía `respuesta_confirmacion`. Tras aplicar se comprobaron las cuatro nuevas columnas de reservas y siete de la proyección plural. Conteos de jornadas, reservas y proyecciones: `0/0/0` antes y después. No se crearon datos sintéticos, no se borraron filas y no se activó Flyway en Render. No repetir el script en ese entorno.

La [medición local](./rendimiento-local.json) registra disponibilidad con 1.001 perfiles, cinco calentamientos y veinte muestras. El resultado solo mide MockMvc y PostgreSQL local con JWT doble; no certifica p95 ni disponibilidad en Render. Se preservan muestras y entorno en el JSON.

## 4. Límites y pendientes

- Seguridad no está desplegada según lo confirmado por el usuario. Faltan issuer/JWKS real, permisos efectivos del cliente técnico y cuentas vinculadas; no se omitió JWT en producción.
- La sesión administrativa continúa siendo la provisional del proyecto. El login transversal no pertenece a F-06.
- Verificar en Render que estén desplegados los commits y las variables vigentes. Operación usa `GESTION_DESPACHOS_URL`; Gestión necesita la URL de Operación y los tres scopes de reserva, liberación y proyección. Una variable explícita antigua en Render prevalece sobre el nuevo valor por defecto.
- La API pública usa el Gateway `https://taller-api-gateway.onrender.com`; los servicios usan los dominios `taller-servicio-gestion-despachos` y `taller-servicio-operacion-reparto` de Render.
- La colisión preexistente entre `V3__programacion_despachos.sql` y `V3__zonas_codigos_postales.sql` impide crear Gestión mediante Flyway. No se renumeraron versiones históricas sin conciliar qué revisión aplicó cada entorno. Esta suite completa continúa fallida; Render conserva Flyway desactivado.
- F-02 y F-03 mantienen sus pantallas y responsabilidades originales. F-06 entrega contratos y proveedores de capacidad, proyección y contexto; no acredita que esas funcionalidades de otros responsables estén completas.
- CUI-06 y aceptación humana quedan pendientes: no se ejecutó revisión visual en navegador real ni auditoría completa de foco, teclado y tamaños reducidos. JSDOM no reemplaza esa comprobación.
- No se acredita el SLA de 200 ms en Render ni el recorrido autenticado Vercel–Gateway–servicios–Seguridad. Un push no confirma el despliegue automático.

## 5. Referencias

1. [Funcionalidad F-06](../../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md) [cite: 1].
2. [Contrato canónico de Operación](../../../integraciones/api-contract-operacion-reparto.md) [cite: 2].
3. [Evidencia de apertura](../evidence.md) y las demás evidencias F-06 enlazadas desde el índice [cite: 3].


<a id="revision-f05-f06-2026-10-26"></a>

## Revisión de F-05 y F-06 (26/10/2026)

### Revisiones y entorno

Base documental `03343ce`. Backend: `4163b80` (auditoría de cierres) y `b81fc39` (artefactos de medición); frontend: `39a361b` (sesiones y recorridos). Código desde `develop`, documentación desde `main`, sin mezclar la rama ajena `feature/f02-rutas-transferencia-segura`. Esa integración de F-02 se revisará cuando su propietario la integre.

Responsable actual de F-05 y F-06: Kevin Rhamses Bohorquez. La asignación original de F-06 se conserva como antecedente; no representa responsabilidad ni aprobación de quien dejó de trabajar en ella.

### Resultados ejecutados

| Comprobación | Resultado | Alcance |
|---|---|---|
| [CI backend](https://github.com/Taller-SW-Web/G2-Despacho-Backend/actions/runs/40419989916) | Cuatro comprobaciones aprobadas | Gateway, Gestión, Operación y Seguridad temporal |
| Operación en CI | 119 pruebas; cero fallos, errores u omisiones | PostgreSQL 17.11 desechable; atomicidad, idempotencia, concurrencia y esquema heredado |
| Selección backend sin Docker, local | 44 pruebas aprobadas y JAR generado | Motor de jornadas, cálculos, HTTP y validadores; no sustituye PostgreSQL |
| [CI frontend](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/actions/runs/40419367650) | Seis comprobaciones aprobadas | Componentes, administrativo, repartidor, tipos/compilación y E2E |
| Administrativo en CI | 165 pruebas aprobadas | F-05/F-06 y regresión; se mantiene la exclusión temporal de Zonas solicitada previamente |
| Componentes compartidos | 208 pruebas aprobadas | Incluye enlace de inicio, destinos, teclado y foco del menú |
| Repartidor | 13 pruebas aprobadas | Regresión del consumidor F-03 |
| Navegador F-05/F-06 | Seis pruebas aprobadas, también localmente | Altas, edición, vínculo manual, bajas, estados, apertura/detalle/cierre y cambio de sesión a 1440/390 px; APIs simuladas |
| Navegador F-02 | Cuatro pruebas aprobadas en CI | Regresión con APIs simuladas |
| Tipos y construcción | Aprobados en CI | Componentes y ambas aplicaciones; avisos de tamaño de bundle existentes |

La ejecución administrativa simultánea en Windows presentó timeouts y no se considera aprobada. La misma revisión aprobó 165/165 en GitHub Actions. Docker Desktop local no pudo iniciar por un socket `dockerInference` inaccesible; no se restableció Docker a valores de fábrica ni se borraron bases/volúmenes. Las pruebas de PostgreSQL se verificaron en Actions.

### Cambios y trazabilidad

Mediciones de la revisión backend `b81fc39`, conservadas en el artefacto `pruebas-servicio-operacion-reparto` de la ejecución enlazada: p95 de 10.87 ms para repartidores y 11.81 ms para furgonetas (100 registros por catálogo, páginas de 50); p95 de 10.22 ms para disponibilidad con 1001 perfiles. Cada medición descarta cinco calentamientos y usa veinte muestras. Son tiempos de MockMvc con PostgreSQL aislado y JWT doble en GitHub Actions; no incluyen red, autenticación real ni latencia de Render y no certifican un SLA desplegado.

Se completó la invalidación de consultas, formularios y respuestas tardías al cambiar/cerrar sesión, también entre pestañas. Se completó la auditoría de las jornadas vacías cerradas por baja de repartidor o retiro de vehículo, dentro de la misma transacción y sin nueva migración. Una falla de esa auditoría revierte el cierre y el cambio del recurso. Las pruebas cubren también el esquema heredado.

Las 17 especificaciones conservan sus identificadores y criterios. Los criterios se contrastan con las pruebas de cada servicio y la interfaz, sin aprobar automáticamente los casos de Seguridad real.

| Especificación | Criterios revisados | Registro |
|---|---|---|
| ES-F05-01 | CA-01 a CA-05 | [Evidencia](../../ES-F05-01-RegistrarRepartidor/evidence.md#ev-05-revision-f05-f06) |
| ES-F05-02 | CA-01 a CA-04 | [Evidencia](../../ES-F05-02-ConsultarRepartidores/evidence.md#ev-05-revision-f05-f06) |
| ES-F05-03 | CA-01 a CA-04 | [Evidencia](../../ES-F05-03-EditarRepartidor/evidence.md#ev-05-revision-f05-f06) |
| ES-F05-04 | CA-01 a CA-05 | [Evidencia](../../ES-F05-04-DarDeBajaRepartidor/evidence.md#ev-05-revision-f05-f06) |
| ES-F05-05 | CA-01 a CA-07 | [Evidencia](../../ES-F05-05-VincularRepartidorConSeguridad/evidence.md#ev-05-revision-f05-f06) |
| ES-F05-06 | CA-01 a CA-05 | [Evidencia](../../ES-F05-06-RegistrarFurgoneta/evidence.md#ev-05-revision-f05-f06) |
| ES-F05-07 | CA-01 a CA-05 | [Evidencia](../../ES-F05-07-ConsultarFurgonetas/evidence.md#ev-05-revision-f05-f06) |
| ES-F05-08 | CA-01 a CA-05 | [Evidencia](../../ES-F05-08-EditarFurgoneta/evidence.md#ev-05-revision-f05-f06) |
| ES-F05-09 | CA-01 a CA-07 | [Evidencia](../../ES-F05-09-CambiarEstadoFurgoneta/evidence.md#ev-05-revision-f05-f06) |
| ES-F06-01 | CA-01 a CA-06 | [Evidencia](../../ES-F06-01-AbrirJornada/evidence.md#ev-02-revision-f05-f06) |
| ES-F06-02 | CA-01 a CA-03 | [Evidencia](../../ES-F06-02-ConsultarMonitoreoFlota/evidence.md#ev-02-revision-f05-f06) |
| ES-F06-03 | CA-01 a CA-03 | [Evidencia](../../ES-F06-03-ConsultarDisponibilidad/evidence.md#ev-02-revision-f05-f06) |
| ES-F06-04 | CA-01 a CA-03 | [Evidencia](../../ES-F06-04-CalcularOcupacionEstado/evidence.md#ev-02-revision-f05-f06) |
| ES-F06-05 | CA-01 a CA-03 | [Evidencia](../../ES-F06-05-CerrarJornada/evidence.md#ev-02-revision-f05-f06) |
| ES-F06-06 | CA-01 a CA-05 | [Evidencia](../../ES-F06-06-ReservarCapacidad/evidence.md#ev-02-revision-f05-f06) |
| ES-F06-07 | CA-01 a CA-04 | [Evidencia](../../ES-F06-07-LiberarReserva/evidence.md#ev-02-revision-f05-f06) |
| ES-F06-08 | CA-01 a CA-04 | [Evidencia](../../ES-F06-08-ActualizarProyeccionDespacho/evidence.md#ev-02-revision-f05-f06) |

### Entrega y pendientes externos

[PR backend](https://github.com/Taller-SW-Web/G2-Despacho-Backend/pull/19) hacia `develop`; [PR frontend](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/pull/17) hacia `develop`. La documentación mantiene `main` como base conforme a CONTRIBUTING. Todos los cambios se presentan para revisión; no se realiza merge ni despliegue.

Seguridad real, homologación de sus cuentas/scopes, aceptación humana, recorrido desplegado y SLA de Render siguen pendientes. El emisor temporal y los mocks no acreditan esos puntos. La revisión visual de capturas y las comprobaciones automáticas de ancho no equivalen a una aprobación humana de accesibilidad. No se consultaron ni modificaron bases compartidas de Supabase ni configuraciones de Render/Vercel.
