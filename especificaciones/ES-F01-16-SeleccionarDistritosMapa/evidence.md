# Evidencia de ES-F01-16

## 1. Preparación — 14/11/2026

Contrato, comportamiento y UI formalizados a solicitud del usuario; entorno/ramas en [ES-F01-13](../ES-F01-13-ConsultarRepresentacionGeografica/evidence.md).

## 2. Resultados

Implementación y verificación locales aprobadas; comandos y revisiones en [ES-F01-13](../ES-F01-13-ConsultarRepresentacionGeografica/evidence.md#3-suites-y-reproducción-compartidas).

| Criterios | Comprobación | Resultado |
|---|---|---|
| CA-01 | Componentes: selección controlada desde renderer simulado actualiza formulario sin POST/PUT. Chromium enfoca un límite SVG real y usa Enter para seleccionar; lista refleja selección y permite retirarla | Aprobado local |
| CA-02 | Edición conserva código `15046` e indicador postal de Lince; Chromium comprueba relleno cero y datos persistidos al guardar | Aprobado local |
| CA-03 | Mi Perú inactivo asociado visible y retirable; tras retirarlo no puede añadirse; guardado conserva las otras asociaciones | Aprobado local |
| CA-04 | Capa identifica asociación de Miraflores a otra zona activa y la UI presenta conflicto/contorno; regresiones de exclusividad del backend siguen aprobadas | Aprobado local |
| CA-05 | Faltantes siguen disponibles por lista; caída de teselas controlada no impide editar/guardar; 403 geográfico retira formulario protegido | Aprobado local |
| CA-06, CUI-01 a CUI-04 | Chromium escritorio 1440×1024 y móvil 390×844, mapa/formulario sincronizados, teclado, guardado explícito y composición; capturas inspeccionadas | Aprobado local; aceptación humana pendiente |

El ajuste de layout detectado en la revisión de capturas evita anidar dos grillas horizontales en el panel de selección: el mapa dispone de más de 400 px en escritorio y la procedencia larga se ajusta al panel. Revisión humana y G6/G7 publicados pendientes; la prueba usa sus dobles explícitos.
