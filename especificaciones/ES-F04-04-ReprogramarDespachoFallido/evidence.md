# Evidencia de ES-F04-04: Reprogramar un despacho fallido

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Gerardo.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), migración SDD del 16/10/2026.
- Origen funcional: base documental `c8e6e29`; se conservan CA-01 a CA-18 y se añaden los CUI de presentación en `ui.md`.
- Bases de código inspeccionadas: frontend `d2bc27d` y backend `1e7834b`; lectura estática, sin compilaciones ni pruebas funcionales ejecutadas.
- Commits de implementación, despliegue funcional, datos ejecutados y servicios realmente comprobados: pendientes.
- Esta entrega prepara documentos y referencias. La validación documental no acredita los comandos, el modal, las migraciones ni sus integraciones [cite: 1, 2].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-03/04/06/07; T-08 | Recepción/versión actuales, nueva fecha, contador y transacción. | EV-01/03/04 | No ejecutado |
| CA-02 | T-02/04/06; T-08 | Hoy/pasado, fecha inexistente y medianoche en Lima. | EV-01/03 | No ejecutado |
| CA-03 | T-02/04/06; T-08 | Máximo vigente igual/superado y cambio de configuración. | EV-01/03 | No ejecutado |
| CA-04 | T-04/05/06; T-08 | Otra incidencia/versión o estado distinto, sin nueva decisión. | EV-01/02/03 | No ejecutado |
| CA-05 | T-04/06; T-08 | Recepción vigente pendiente, aunque exista una histórica. | EV-01/03 | No ejecutado |
| CA-06 | T-04/07; T-08 | NO_INTENTADO con cero/uno y sin incremento. | EV-01/04 | No ejecutado |
| CA-07 | T-04/05/06; T-08 | Anulación y límite simultáneos; precedencia y bloqueo. | EV-01/02/03 | No ejecutado |
| CA-08 | T-03/05/06; T-08 | Replay exacto después de medianoche/reinicio/otra salida. | EV-02/03 | No ejecutado |
| CA-09 | T-02/04/06; T-08 | Formato estricto y observación normalizada con Unicode. | EV-01/03 | No ejecutado |
| CA-10 | T-05; T-08 | Misma identidad con otro contenido/ejecutor. | EV-02 | No ejecutado |
| CA-11 | T-05/07; T-08 | Reprogramación contra cierre/anulación en transacciones reales. | EV-02/04 | No ejecutado |
| CA-12 | T-06/07; T-08 | Cola visible inmediatamente y asignación por fecha/reserva. | EV-03/04 | No ejecutado |
| CA-13 | T-03/04/07; T-08 | Liberación pendiente conservada y nueva incidencia sin recepción heredada. | EV-01/04 | No ejecutado |
| CA-14 | T-04/05/07; T-08 | Rollback local y evento recuperable ante caída de Ventas. | EV-01/02/04 | No ejecutado |
| CA-15 | T-04/06; T-08 | Autorización y existencia sin revelar datos. | EV-01/03 | No ejecutado |
| CA-16 | T-04/07; T-08 | Identidad/zona/carga conservadas y simulado sin evento. | EV-01/04 | No ejecutado |
| CA-17 | T-02/06; T-08 | Modal, resultado desconocido y origen actualizado. | EV-03 | No ejecutado |
| CA-18 | T-04; T-08 | Máximo ausente/no entero/no positivo sin escrituras. | EV-01 | No ejecutado |
| CUI-01 | T-01/T-02/T-06/T-08 | Contexto y navegación. | EV-03 | No ejecutado |
| CUI-02 | T-01/T-02/T-06/T-08 | Fecha civil y reloj. | EV-03 | No ejecutado |
| CUI-03 | T-01/T-02/T-06/T-08 | Observación normalizada. | EV-03 | No ejecutado |
| CUI-04 | T-01/T-02/T-06/T-08 | Restricciones actuales. | EV-03 | No ejecutado |
| CUI-05 | T-01/T-02/T-06/T-08 | Envío y confirmación. | EV-03 | No ejecutado |
| CUI-06 | T-01/T-02/T-06/T-08 | Rechazos y resultado desconocido. | EV-03 | No ejecutado |
| CUI-07 | T-01/T-02/T-06/T-08 | Éxito y actualización. | EV-03 | No ejecutado |
| CUI-08 | T-01/T-02/T-06/T-08 | Accesibilidad y autorización. | EV-03 | No ejecutado |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Ningún criterio está aprobado por generar esta carpeta. Un fixture o doble acredita solo lo observado en ese entorno.

## 3. Registros de verificación

### EV-01. Persistencia, fecha y seguridad

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-03/04/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Aplicar migraciones en datos sintéticos; ejecutar pruebas de Gestión con reloj controlado y fallos de escritura.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: PostgreSQL/Testcontainers real; dobles de servicios externos identificados.

### EV-02. Concurrencia y recuperación durable

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-03/05/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Ejecutar solicitudes en dos transacciones y repetir tras reinicio, medianoche y cambio de incidencia; comparar filas y cuerpos originales.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: Base real; no demostrar carreras únicamente con mocks.

### EV-03. Modal, contrato y accesibilidad

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-01/02/06/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Ejecutar interacción de CUI-01 a CUI-08, comprobaciones frontend y recorrido del modal a través del Gateway.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: Separar fixtures de API real; revisión manual de foco/móvil.

### EV-04. Recorrido real de reprogramación

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-07/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Recibir, reprogramar, consultar cola, intentar asignación futura/con reserva previa, liberar y realizar otra salida; comprobar evento y simulación.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: F-02/F-03/F-06, Gestión/Operación y receptor de Ventas reales cuando se acredite entrega.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas | Instrucción conservada | Revisión humana |
|---|---|---|---|---|
| Preparación documental SDD; ninguna T-NN de implementación completada. | Codex, 16/10/2026. | Revisión funcional `c8e6e29`, plantillas SDD, contratos, modelo, diseño y bases de código citadas en el plan. | Conversación de esta entrega: completar carpetas SDD de ES-F04-04/05/06, conservar reglas y dejar pruebas pendientes. | Gerardo; revisión de esta entrega pendiente. |

Se generaron organización, plan, tareas, UI y matrices de verificación. Las comprobaciones documentales y el commit de esta entrega son trazabilidad de preparación, no evidencia de aceptación funcional. Al ejecutar tareas con IA se añadirán herramienta, instrucciones, cambios y revisión humana reales.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterios afectados | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| Comportamiento todavía por implementar/verificar. | Todos los CA/CUI. | No se acredita aceptación funcional. | Gerardo ejecuta tareas del plan y registra resultados. |
| Dependencias técnicas/servicios pendientes de disponibilidad real, DT-01 a DT-03. | Los de cada incremento dependiente. | Mocks no cierran el recorrido integrado. | Coordinación de Gerardo con responsables indicados en el plan. |
| Revisión humana y entorno reproducible de pruebas pendientes. | Cierre del alcance. | No declarar verificado. | Registrar commits, datos sintéticos, reportes y revisión al ejecutar. |

## 6. Entrega y revisión

- Commits/PR de implementación: pendientes; el commit que incorpora esta carpeta es solo documental.
- Revisor, fecha y resultado de revisión funcional/técnica de la implementación: pendientes.
- Estado del alcance implementado: Pendiente.
- Integraciones reales pendientes: las identificadas en EV-04 y en el plan.
- Verificación de criterios: No ejecutada; no hay capturas, reportes o resultados funcionales ficticios.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md) y [UI](./ui.md): comportamiento y aceptación.
- [cite: 2] [Plan](./plan.md) y [tareas](./tasks.md): fuentes, incrementos y preparación reproducible.
- [cite: 3] [Gestión §5.2.2](../../integraciones/api-contract-gestion-despachos.md#522-reprogramar-un-despacho-fallido--es-f04-04), [modelo](../../arquitectura/modelo-datos.md) y [guía SDD](../../plantillas/sdd/README.md).
