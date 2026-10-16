# Evidencia de ES-F04-06: Registrar la trazabilidad de las operaciones

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Gerardo.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), migración SDD del 16/10/2026.
- Origen funcional: base documental `c8e6e29`; se conservan CA-01 a CA-12.
- Bases de código inspeccionadas: frontend `d2bc27d` y backend `1e7834b`; lectura estática, sin compilaciones ni pruebas funcionales ejecutadas.
- Commits de implementación, despliegue funcional, datos ejecutados y servicios realmente comprobados: pendientes.
- Esta entrega prepara documentos y referencias. La validación documental no acredita los comandos, las migraciones ni sus integraciones [cite: 1, 2].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02/03/04; T-08 | Recepción, reserva/sello y transacción conjunta sin evento externo. | EV-01 | No ejecutado |
| CA-02 | T-02/03/04; T-08 | Reprogramación con fecha civil y conjunto atómico. | EV-01 | No ejecutado |
| CA-03 | T-02/03/04; T-08 | Cierre, motivo separado y resultado durable en historial. | EV-01 | No ejecutado |
| CA-04 | T-03/04/05; T-08 | Rechazos conservan historial previo sin auditoría aceptada nueva. | EV-01/02 | No ejecutado |
| CA-05 | T-02/03/04/05/07; T-08 | Replay tras reinicio/cambio de incidencia conserva la entrada original. | EV-01/02/04 | No ejecutado |
| CA-06 | T-02/06; T-08 | Historial completo, varios ciclos y desempate estable en detalle. | EV-03 | No ejecutado |
| CA-07 | T-01/03/05; T-08 | Rollback de historial y cualquier escritura del comando. | EV-01/02 | No ejecutado |
| CA-08 | T-05; T-08 | Concurrencia e identidad incompatible sin doble captura. | EV-02 | No ejecutado |
| CA-09 | T-01/02/03/04/05/06; T-08 | Inmutabilidad, sub del JWT, hora del servidor y origen MANUAL. | EV-01/02/03 | No ejecutado |
| CA-10 | T-07; T-08 | Reintentos/liberación/envío no modifican historial. | EV-04 | No ejecutado |
| CA-11 | T-02/06; T-08 | Proyección pública sin controlCierre/huellas ni lectura no autorizada. | EV-03 | No ejecutado |
| CA-12 | T-02/03/04/07; T-08 | Simulado conserva la auditoría aplicable sin evento externo. | EV-01/04 | No ejecutado |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Ningún criterio está aprobado por generar esta carpeta. Un fixture o doble acredita solo lo observado en ese entorno.

## 3. Registros de verificación

### EV-01. Captura y transacciones de los productores

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-01/02/03/04/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Migrar datos sintéticos y ejecutar cada comando; comparar historial, estados, autoría, datos propios y conjunto atómico.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: PostgreSQL/Testcontainers real; registrar versiones exactas de los tres productores.

### EV-02. Rechazos, rollback y concurrencia

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-05/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Forzar errores antes/después de capturar; dos decisiones concurrentes, replay y otro ejecutor/contenido; comparar filas y resultados.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: Transacciones reales; los dobles no acreditan carreras ni rollback de base.

### EV-03. Historial público y autorización

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-06/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Consultar varios ciclos y marcas iguales con distintos permisos; contrastar orden, datos propios y exclusión de metadatos internos.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: GET real de ES-F04-02, con datos sintéticos y tokens de prueba sin exponerlos.

### EV-04. Reintentos técnicos y simulados

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-07/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Ejecutar/reiniciar procesadores, perder respuestas, reenviar evento y confirmar reserva; comparar historial antes/después.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: Liberación/envío reales al acreditar integración; fixtures aislados se distinguen.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción conservada | Revisión humana |
|---|---|---|---|---|
| Preparación documental SDD; ninguna T-NN de implementación completada. | Codex, 16/10/2026. | Revisión funcional `c8e6e29`, plantillas SDD, contratos, modelo, diseño y bases de código citadas en el plan. | Conversación de esta entrega: completar carpetas SDD de ES-F04-04/05/06, conservar reglas y dejar pruebas pendientes. | Gerardo; revisión de esta entrega pendiente. |

Se generaron organización, plan, tareas, matrices de verificación. Las comprobaciones documentales y el commit de esta entrega son trazabilidad de preparación, no evidencia de aceptación funcional. Al ejecutar tareas con IA se añadirán herramienta, instrucciones, cambios y revisión humana reales.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterios afectados | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| Comportamiento todavía por implementar/verificar. | Todos los CA. | No se acredita aceptación funcional. | Gerardo ejecuta tareas del plan y registra resultados. |
| Dependencias técnicas/servicios pendientes de disponibilidad real, DT-01 a DT-03. | Los de cada incremento dependiente. | Mocks no cierran el recorrido integrado. | Coordinación de Gerardo con responsables indicados en el plan. |
| Revisión humana y entorno reproducible de pruebas pendientes. | Cierre del alcance. | No declarar verificado. | Registrar commits, datos sintéticos, reportes y revisión al ejecutar. |

## 6. Entrega y revisión

- Commits/PR de implementación: pendientes; el commit que incorpora esta carpeta es solo documental.
- Revisor, fecha y resultado de revisión funcional/técnica de la implementación: pendientes.
- Estado del alcance implementado: Pendiente.
- Integraciones reales pendientes: las identificadas en EV-04 y en el plan.
- Verificación de criterios: No ejecutada; no hay capturas, reportes o resultados funcionales ficticios.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md): comportamiento y aceptación.
- [cite: 2] [Plan](./plan.md) y [tareas](./tasks.md): fuentes, incrementos y preparación reproducible.
- [cite: 3] [Gestión §5.3](../../integraciones/api-contract-gestion-despachos.md#53-consultar-el-detalle-de-una-incidencia--es-f04-02), [modelo](../../arquitectura/modelo-datos.md) y [guía SDD](../../plantillas/sdd/README.md).
