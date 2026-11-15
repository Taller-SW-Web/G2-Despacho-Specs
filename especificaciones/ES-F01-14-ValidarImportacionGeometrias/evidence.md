# Evidencia de ES-F01-14

## 1. Preparación — 14/11/2026

Contrato y criterios formalizados a solicitud del usuario. Exportación local previa: 50 GeoJSON, 43 Lima/7 Callao, 50 ubigeos únicos y 72 489 posiciones conservadas. Esto no acredita topología ni vigencia oficial.

## 2. Resultados

Implementación y verificación locales aprobadas. Revisiones, suites, entorno y comandos en [ES-F01-13](../ES-F01-13-ConsultarRepresentacionGeografica/evidence.md#3-suites-y-reproducción-compartidas).

| Criterios | Comprobación | Resultado |
|---|---|---|
| CA-01 | Validación HTTP/PostGIS sin geometrías, histórico ni auditorías nuevas; Chromium consulta geometría nula después de previsualizar y antes de confirmar | Aprobado |
| CA-02 | Mi Perú `"070107"` asociado al UUID existente; importación real de los 50 ubigeos | Aprobado |
| CA-03, CUI-02 | Backend y componentes exigen correspondencia explícita; una sugerencia no se confirma sola y no reemplaza un código declarado | Aprobado; UI con dobles |
| CA-04, CUI-01/03 | Casos de tipo, vacío, anillo abierto, autocruce, UTM/CRS, duplicado, desconocido y ubigeo numérico; Chromium rechaza autocruce y conserva archivo/metadatos | Aprobado |
| CA-05 | 101 entidades y más de 200 000 posiciones; límite de cuerpo en Gestión y Gateway, este último con/sin longitud; cuerpo real de 49 distritos superior a 1 MiB admitido por Gateway | Aprobado |
| CA-06, CUI-04/05 | Permisos HTTP, retirada de propuesta y recuperación de red en componentes; modal/teclado en Chromium | Aprobado local |

## 3. Datos reproducibles

`herramientas/preparar_geometrias.py` y `datos/geometrias/{catalogo,origen}.json` del backend fijan revisión `2c2a8ae7dc317767a389a37b6b5ef4d3fc51ec16`, licencias MIT/Apache-2.0, atribución y hash. Se ejecutó con el origen detallado y `--destino /tmp/opencode/distritos-f01-postgis --verificar-postgis`: 50/50 topologías válidas en PostGIS 16-3.4 desechable y 72 489 posiciones conservadas. Salida: 50 GeoJSON, manifiesto de huellas e informe `validacion-postgis.json`. El origen permaneció intacto.

SHA-256 del origen: `b0627d6c0a5617fef2054ef066f54dd2d1e4c15d2506c7fef034fef6fc48db9e`. Las 50 geometrías importadas por la API se compararon con los archivos completos. Revisión por pares, aceptación humana y vigencia oficial pendientes.
