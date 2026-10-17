# Evidencia de ES-F06-04: Calcular ocupación y estado operativo

**Responsable:** Kevin Rhamses Bohorquez, con asistencia de Codex. **Estado:** Implementación y automatización local verificadas; aceptación desplegada y revisión humana pendientes.

## 1. Versión y entorno verificados

Frontend `f73c268`, backend `3ce1964`; especificaciones preparadas en `16d358b`, `46e47c7` y `45121ae`, con ajustes de consistencia registrados en esta entrega. Ver [reporte reproducible](../ES-F06-01-AbrirJornada/evidencia/validacion.md) [cite: 4]. Entorno Windows, Java 21, Node/Vitest y PostgreSQL 17.11 temporal sobre Docker ya iniciado. Datos sintéticos; JWT y consulta de zona como dobles en las pruebas de persistencia.

## 2. Cobertura de criterios

Los resultados «Aprobado» se limitan a las comprobaciones locales indicadas; no certifican Seguridad, Render/Vercel ni revisión humana.

| Criterio | Tarea | Prueba o comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-01 a T-04 | Prioridad de estados: CalculoOcupacionTests y proyecciones PostgreSQL. | EV-01 | Aprobado |
| CA-02 | T-01 a T-04 | Saturación por las tres dimensiones y exceso: CalculoOcupacionTests y pruebas de BarraOcupacion. | EV-01 | Aprobado |
| CA-03 | T-01 a T-04 | FALLIDO conserva reserva hasta liberar: recorrido reserva/proyección/retorno/cierre PostgreSQL. | EV-01 | Aprobado |
| CUI-01 | T-02 y T-04 | Contexto, controles con nombre y métricas: PaginaJornadas y componentes compartidos. | EV-01 | Aprobado |
| CUI-02 | T-02 y T-04 | URL inválida y modelos: modelo.test.tsx y PaginaJornadas.test.tsx. | EV-01 | Aprobado |
| CUI-03 | T-02 y T-04 | Resultado incierto y bloqueo de envíos: apertura y hook de mutación en PaginaJornadas.test.tsx. | EV-01 | Aprobado |
| CUI-04 | T-02 y T-04 | Fallo, datos anteriores y recuperación: PaginaJornadas y useConsultaJornadas. | EV-01 | Aprobado |
| CUI-05 | T-02 y T-04 | 401/403 retira contenido y formularios: PaginaJornadas.test.tsx. | EV-01 | Aprobado |
| CUI-06 | T-02 y T-04 | Revisión visual en navegador, foco completo y pantallas reducidas no ejecutados. | EV-01 | Pendiente |

## 3. Registros de verificación

### EV-01. Verificación del incremento

- Ejecución: Codex por solicitud de Kevin Rhamses; revisión humana pendiente. No se atribuye ejecución ni aprobación a Luis.
- Comandos, resultados y revisiones: [reporte común](../ES-F06-01-AbrirJornada/evidencia/validacion.md#2-comandos-y-resultados) y [trazabilidad](../ES-F06-01-AbrirJornada/evidencia/validacion.md#1-revisiones) [cite: 4].
- Resultado esperado: reglas de spec.md, representación de ui.md cuando aplica y contrato canónico.
- Resultado observado: comprobaciones automatizadas aprobadas según la tabla; PostgreSQL confirma consistencia, auditoría, concurrencia e idempotencia. Las capturas del proveedor se consumen en frontend y en el adaptador F-02 real con transporte controlado.
- Integración de esquema: adaptación F-06 probada en copia heredada, ensayada con ROLLBACK y aplicada en Operadores y Flota. Conteos antes/después: jornadas 0, reservas 0, proyecciones 0; no se crearon filas de prueba en Supabase.
- Límites: JWT y zona simulados en persistencia; ningún mock acredita comunicación desplegada ni permisos concedidos por G7.

## 4. Uso de IA

Codex preparó SDD, componentes, casos de uso, migración, pruebas y registro por solicitud de Kevin Rhamses. Luis conserva la asignación funcional original; implementación asumida por Kevin. No se inventan fechas, aprobación humana ni resultados.

## 5. Diferencias, fallos y pendientes

Seguridad real y concesión de scopes, sesión administrativa, recorrido autenticado Render/Vercel, revisión visual y aceptación humana pendientes. El p95 local está medido, pero no acredita el objetivo en Render. Gestión tiene dos migraciones V3 preexistentes: su suite completa falla por esa colisión; el consumidor F02/F06 pasó por separado. Véase el [detalle de límites](../ES-F06-01-AbrirJornada/evidencia/validacion.md#4-límites-y-pendientes).

## 6. Entrega y revisión

Código identificado en §1; publicación en `develop` para frontend/backend y `main` para Specs. T-01/T-02/T-03 completadas con alcance local; T-04 parcial por dependencias reales y revisión humana pendientes. Esta evidencia no declara aceptación final.

## 7. Referencias

1. [Spec](./spec.md) [cite: 1].
2. [Plan](./plan.md) y [tareas](./tasks.md) [cite: 2].
3. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md) [cite: 3].
4. [Reporte de verificación](../ES-F06-01-AbrirJornada/evidencia/validacion.md) [cite: 4].
