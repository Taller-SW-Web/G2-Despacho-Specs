# Evidencia de ES-F01-13

## 1. Preparación — 14/11/2026

Ejecución solicitada por el usuario sobre el plan backend. Ramas `feature/f01-geometrias-mapas` desde develop en backend/frontend y `docs/f01-geometrias-mapas` desde main en Specs. Sin commit ni revisión humana.

## 2. Resultados

Verificación local ejecutada mediante OpenCode por solicitud del usuario. Bases de las ramas: backend `ffdd4bff8ce078c243077a082e86e94505532450`, frontend `1c26838763c55d083205fe9e57552854168b7688`, Specs `811ae9dbe0b084cfcef69705d03b83134997a019`; cambios de trabajo sin commit.

| Criterios | Comprobación | Resultado |
|---|---|---|
| CA-01 | `GeometriasHttpTests.consultaFaltantesFiltrosYComposicionPostalSinModificarCatalogo`: 50 registros sin geometría, filtros, listado ordinario liviano; Chromium consulta 50 límites iguales al conjunto importado y ficha con procedencia/versión | Aprobado local |
| CA-02 | Consulta derivada de asociación exclusivamente postal y zona inexistente; Chromium muestra composición y referencia postal sin relleno | Aprobado local |
| CA-03 | Cuatro operaciones sin token, con otro rol y token técnico; Gateway real rechaza consulta anónima/técnica | Aprobado local |
| CA-04, CUI-01/02 | Componentes: recuperación de consulta, faltantes/ficha, respuestas atrasadas y retirada de formulario ante 403; renderer y HTTP simulados | Aprobado con dobles |
| CUI-03 | Leaflet real en Chromium: teclado sobre SVG, lista/centrado, escritorio y móvil sin desbordamiento; caída de teselas controlada | Aprobado local; aceptación humana pendiente |

## 3. Suites y reproducción compartidas

- Gestión: `SPRING_FLYWAY_ENABLED=true ./mvnw clean verify`, 284 pruebas, cero fallos/errores/omisiones; Testcontainers PostgreSQL/PostGIS 17-3.6 con V12. Incluye 17 casos de `GeometriasHttpTests` y regresiones existentes. Dos pruebas previas de migración ajustan la versión final esperada de 11 a 12 y conservan sus aserciones históricas.
- Gateway: `./mvnw clean verify`, 36 pruebas aprobadas.
- Frontend: `npm run test:f01`, 62 pruebas; `npm run test:administrativo`, 272; `npm run typecheck` y `npm run build` aprobados. Diez pruebas de geometrías con API/renderer simulados.
- Chromium: `F01_GEOMETRIAS_DIR=/tmp/opencode/distritos-f01-postgis npm run test:geometrias:e2e`, dos recorridos aprobados; `npm run test:distritos:e2e`, dos regresiones existentes aprobadas en otra base recreada.

Entorno reproducible en [guía backend](https://github.com/Taller-SW-Web/G2-Despacho-Backend/blob/develop/docs/pruebas.md#geometrías-y-mapas-administrativos-f-01): Gateway/Gestión reales locales, PostGIS en tmpfs, Seguridad temporal y Productos simulados. Los proyectos de prueba fueron retirados al terminar; no se ejecutaron migraciones ni cargas sobre Supabase o una base persistente.

Capturas inspeccionadas en `G2-Despacho-Frontend/test-results/geometrias/`: `01-previsualizacion.png`, `02-incidencias.png`, `03-mapa-distrito.png`, `04-seleccion-escritorio.png`, `05-seleccion-movil.png`, `06-composicion-zona.png` dentro de las carpetas de cada recorrido. Informes Maven en `target/surefire-reports/` de cada servicio; artefactos fuera de Git. El proveedor de teselas se hace fallar deliberadamente; estos resultados no acreditan su disponibilidad, G6/G7 publicados, aceptación humana ni vigencia oficial de los límites.
