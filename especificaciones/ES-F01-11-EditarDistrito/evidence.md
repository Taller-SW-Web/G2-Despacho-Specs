# Evidencia de ES-F01-11: Editar un distrito

## 1. Preparación — 13/11/2026

Contrato y especificación preparados mediante OpenCode por solicitud del usuario. Backend base `65adfd0`; frontend base `feb57e6`; Specs base `c2ea248`. Ramas de funcionalidad desde develop y documental desde main. Revisión humana pendiente.

## 2. Resultados

Verificación local del 13/11/2026 mediante OpenCode: aprobada; cambios en ramas de trabajo sin commit ni revisión humana. F-01 CA-35.

| Criterios | Comprobación ejecutada | Resultado |
|---|---|---|
| CA-01 | Alta/edición real conserva UUID e inserta anterior/nuevo en auditoría | Aprobado |
| CA-02 | `protegeCatalogoBaseEIdentidadAsociadaInclusoPostalYZonaInactiva`: protección de base y asociación exclusivamente postal en zona inactiva | Aprobado sin auditoría de rechazo |
| CA-03 | Dos ediciones concurrentes con versión cero: exactamente 200/409 y una modificación auditada | Aprobado |
| CA-04 | Repetición de edición idéntica con versión vigente no incrementa versión ni auditoría | Aprobado |
| CA-05 | Duplicados, versión/tipos/geografía inválidos y matriz de autorización | Aprobado local |
| CUI-01 a CUI-04 | `Distritos.test.tsx`: solo lectura de identidad, versión presentada, conflicto con valores conservados y nueva consulta explícita; Chromium: conflicto contra API real local | Aprobado, revisión humana pendiente |

Se corrigió la lectura posterior al `saveAndFlush` para que respuesta y auditoría utilicen los instantes realmente guardados por PostgreSQL y su trigger, no otra fecha calculada por JPA. No se relajó la igualdad de respuestas en las pruebas. Comandos y reportes en [ES-F01-12](../ES-F01-12-ActivarDesactivarDistrito/evidence.md#2-resultados-del-13112026).

## 3. Administración unificada — 13/11/2026

T-06 y CUI-01 a CUI-06 verificados localmente. Componentes con APIs simuladas cubren selección de fila con detalle vigente, marca En edición, alta tras guardar/cancelar, confirmaciones de borrador, identidad protegida, versión original conservada al actualizar la lista, detalle inexistente sin formulario vacío y respuestas atrasadas ignoradas.

El conflicto conserva valores y bloquea reenviar; consultar otra versión exige Descartar y consultar. Este flujo también se verifica en Chromium contra Gestión real mediante Gateway. En móvil, el foco de edición se desplaza al formulario y queda por debajo de la cabecera fija. Comandos y límites en [evidencia compartida de la unificación](../ES-F01-12-ActivarDesactivarDistrito/evidence.md#3-administración-unificada-de-distritos). Aceptación humana pendiente.
