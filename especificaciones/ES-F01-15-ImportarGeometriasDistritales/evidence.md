# Evidencia de ES-F01-15

## 1. Preparación — 14/11/2026

Contrato y criterios formalizados a solicitud del usuario. Ramas y entorno en [ES-F01-13](../ES-F01-13-ConsultarRepresentacionGeografica/evidence.md).

## 2. Resultados

Implementación y verificación locales aprobadas; comandos, revisiones y entorno en [ES-F01-13](../ES-F01-13-ConsultarRepresentacionGeografica/evidence.md#3-suites-y-reproducción-compartidas).

| Criterios | Comprobación | Resultado |
|---|---|---|
| CA-01/02 | V12 y HTTP/PostGIS reales: primera carga, reemplazo, conservación de multipartes/huecos, identidad del CRUD y versión geográfica independiente; histórico previo íntegro y nombre de archivo trazable desde importación vigente/histórica. Chromium consulta el nombre del archivo importado | Aprobado |
| CA-03 | Respuesta exacta tras cambios posteriores, clave reutilizada y validación consumida; dos reintentos concurrentes producen una sola decisión. Chromium pierde deliberadamente la primera respuesta aceptada y recupera con la misma clave | Aprobado |
| CA-04 | Otro ejecutor, expiración, cambio distrital y geográfico; dos confirmaciones concurrentes de propuestas obsoletas producen 200/409 | Aprobado |
| CA-05 | Fallo sintético de auditoría en la segunda entidad revierte límite, metadatos, importación, auditoría y comando idempotente de todo el lote | Aprobado |
| CA-06 | Cotización exacta con reloj y Productos controlados idéntica antes de tener geometría, tras importar y reemplazar; Chromium compara cobertura, costo, moneda, peso, volumen, plazo y fecha, sin campos nuevos | Aprobado local |
| CUI-01 a CUI-05 | Componentes con HTTP/renderer simulados: previsualización, invalidez, cambios de metadatos, respuesta perdida, conflicto y permisos. Chromium confirma, recupera y actualiza mapas | Aprobado local |

Después del recorrido geográfico, consulta de la base desechable: 50 metadatos/geometrías válidas, tres importaciones, un límite histórico y 51 auditorías geográficas. La respuesta perdida no generó otra importación. El proyecto se retiró al terminar. Aceptación humana e integración publicada pendientes.
