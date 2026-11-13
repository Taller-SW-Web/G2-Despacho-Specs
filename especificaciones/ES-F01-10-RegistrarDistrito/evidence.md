# Evidencia de ES-F01-10: Registrar un distrito

## 1. Preparación — 13/11/2026

Contrato y especificación preparados mediante OpenCode por solicitud del usuario. Backend base `65adfd0`; frontend base `feb57e6`; Specs base `c2ea248`. Ramas de funcionalidad desde develop y documental desde main. Revisión humana pendiente.

## 2. Resultados

Verificación local del 13/11/2026 mediante OpenCode: aprobada; cambios en ramas de trabajo sin commit ni revisión humana. F-01 CA-34.

| Criterios | Comprobación ejecutada | Resultado |
|---|---|---|
| CA-01 | `altaEdicionBajaReactivacionYAuditoriaSinCambiosDuplicados`: normalización, UUID, estado activo, versión, fechas y ejecutor del JWT | Aprobado |
| CA-02 | `unicidadIncluyeInactivosYNormalizaMayusculas` y dos altas concurrentes con el mismo nombre/ubigeo | Aprobado; un alta y un 409 |
| CA-03 | Seis variantes de `validaTiposGeografiaYCamposEscribibles`; filtros/versiones inválidos y campos no permitidos | Aprobado; sin filas nuevas |
| CA-04 | `coberturaPostalExclusivaZonaInactivaYSinTarifa` y Chromium: nuevo sin zona no cotiza | Aprobado |
| CA-05 | Seguridad y fallo controlado de auditoría con reversión del alta | Aprobado local |
| CUI-01 a CUI-04 | `Distritos.test.tsx`: formulario, prefijo, duplicado por campo y preservación; Chromium: alta y conflicto reales, captura móvil y foco de teclado | Aprobado; API simulada en componentes, real local en Chromium |

V11 se prueba sobre V10 con 51 registros, asociaciones distritales/postales y comparación íntegra de todos los campos previos, incluidas fechas. Reportes y comandos en [ES-F01-12](../ES-F01-12-ActivarDesactivarDistrito/evidence.md#2-resultados-del-13112026). G6/G7 publicados y aceptación humana pendientes.
