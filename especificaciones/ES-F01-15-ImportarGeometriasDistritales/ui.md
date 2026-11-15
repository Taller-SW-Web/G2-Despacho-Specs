# UI de ES-F01-15: Confirmar importación

## 1. Interacción

Continuación del [importador](../ES-F01-14-ValidarImportacionGeometrias/ui.md). Mostrar fuente/versión, distritos afectados, primera carga/reemplazo y comparación geográfica. Confirmación explícita «Confirmar importación» solo con informe válido y vigente. Envío bloquea cambios/cierre y conserva clave para recuperar respuesta perdida. Éxito muestra cantidad/importación y refresca capa.

## 2. Criterios UI

CUI-01: no confirmar antes de validar. CUI-02: error de red conserva propuesta y clave. CUI-03: conflicto/expiración exige nueva validación. CUI-04: 401/403 retira datos. CUI-05: resultado confirmado y navegación accesible. Maqueta 05 del plan backend; Mantine según sistema de diseño.
