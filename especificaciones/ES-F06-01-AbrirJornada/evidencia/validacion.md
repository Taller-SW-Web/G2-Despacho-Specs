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
