# Evidencia de ES-F04-05: Cerrar un despacho como devuelto a origen

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Gerardo.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), migración SDD del 16/10/2026.
- Origen funcional: base documental `c8e6e29`; se conservan CA-01 a CA-15 y se añaden los CUI de presentación en `ui.md`.
- Bases de código inspeccionadas: frontend `d2bc27d` y backend `1e7834b`; lectura estática, sin compilaciones ni pruebas funcionales ejecutadas.
- Commits de implementación, despliegue funcional, datos ejecutados y servicios realmente comprobados: pendientes.
- Esta entrega prepara documentos y referencias. La validación documental no acredita los comandos, el modal, las migraciones ni sus integraciones [cite: 1, 2].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-03/04/06/07; T-08 | Cierre local, versión, historial/resultado y evento real atómicos. | EV-01/03/04 | No ejecutado |
| CA-02 | T-03/05/06; T-08 | Replay exacto después de reinicio o cambios técnicos. | EV-02/03 | No ejecutado |
| CA-03 | T-04/07; T-08 | Caída de Ventas conserva cierre y agota reintentos RT-03. | EV-01/04 | No ejecutado |
| CA-04 | T-02/04/06; T-08 | Recepción de esta incidencia pendiente, incluso con una histórica recibida. | EV-01/03 | No ejecutado |
| CA-05 | T-02/04/06/07; T-08 | Anulación permite cierre; no genera otra cancelación. | EV-01/03/04 | No ejecutado |
| CA-06 | T-02/04/06; T-08 | Motivo/formato y normalización Unicode de ambos textos. | EV-01/03 | No ejecutado |
| CA-07 | T-04/06; T-08 | 401/403/404 y retirada de datos protegidos. | EV-01/03 | No ejecutado |
| CA-08 | T-02/04/07; T-08 | Límite, intentos disponibles y NO_INTENTADO sin cierre automático. | EV-01/03/04 | No ejecutado |
| CA-09 | T-05/06; T-08 | Estado/versión/incidencia obsoletos sin editar decisiones. | EV-02/03 | No ejecutado |
| CA-10 | T-03/05/07; T-08 | Dos cierres, cierre/reprogramación/anulación y contenido incompatible. | EV-02/04 | No ejecutado |
| CA-11 | T-04/07; T-08 | Solicitud original continúa al cerrar con liberación pendiente. | EV-01/04 | No ejecutado |
| CA-12 | T-03/04/05; T-08 | Inconsistencia local y rollback de cada escritura. | EV-01/02 | No ejecutado |
| CA-13 | T-03/04/07; T-08 | Datos conservados y simulado sin evento externo. | EV-01/04 | No ejecutado |
| CA-14 | T-02/06; T-08 | Envío, resultado desconocido y recuperación del origen. | EV-03 | No ejecutado |
| CA-15 | T-04/06/07; T-08 | Fuera de fallidos/cola, detalle final autorizado y sin metadatos. | EV-01/03/04 | No ejecutado |
| CUI-01 | T-01/T-02/T-06/T-08 | Resumen y contexto. | EV-03 | No ejecutado |
| CUI-02 | T-01/T-02/T-06/T-08 | Motivo y observación. | EV-03 | No ejecutado |
| CUI-03 | T-01/T-02/T-06/T-08 | Condiciones de cierre. | EV-03 | No ejecutado |
| CUI-04 | T-01/T-02/T-06/T-08 | Confirmación única. | EV-03 | No ejecutado |
| CUI-05 | T-01/T-02/T-06/T-08 | Conflicto y estado nuevo. | EV-03 | No ejecutado |
| CUI-06 | T-01/T-02/T-06/T-08 | Resultado desconocido. | EV-03 | No ejecutado |
| CUI-07 | T-01/T-02/T-06/T-08 | Éxito y comunicación. | EV-03 | No ejecutado |
| CUI-08 | T-01/T-02/T-06/T-08 | Accesibilidad y permisos. | EV-03 | No ejecutado |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Ningún criterio está aprobado por generar esta carpeta. Un fixture o doble acredita solo lo observado en ese entorno.

## 3. Registros de verificación

### EV-01. Cierre, datos y seguridad

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-03/04/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Migrar base sintética; probar el comando y fallos de escritura en PostgreSQL; observar conservación de datos y ausencia de eventos simulados.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: Persistencia real; receptor de eventos doble controlado solo para pruebas aisladas.

### EV-02. Concurrencia y resultado original

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-03/05/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Procesar dos decisiones a la vez y repetir tras reinicio/24 horas/cambio técnico; comparar código/cuerpo y filas.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: Transacciones reales; no inferir aceptación de un simple estado final.

### EV-03. Modal, recuperación y accesibilidad

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-01/02/06/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Ejecutar CUI-01 a CUI-08 y comprobaciones frontend; fallar envío/refresco y recuperar desde el Gateway.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: Fixtures y APIs reales se registran por separado; revisión manual de teclado/móvil.

### EV-04. Cierre logístico e integraciones reales

- Fecha/persona, commit de implementación y entorno exacto: pendientes de ejecución.
- Tareas: T-07/08; criterios asociados en la matriz anterior.
- Preparación y pasos previstos: Cerrar con liberación pendiente, después liberarla; consultar fallidos/cola/detalle y contrastar evento real y simulado.
- Resultado esperado: cumplir los criterios vinculados y conservar sus invariantes.
- Resultado observado: pendiente; no se ejecutó esta comprobación.
- Resultado de la comprobación: No ejecutado.
- Artefactos de prueba, salida, captura o reporte: pendientes; se enlazarán al ejecutar.
- Dependencias y límites: Gestión/Operación/F-02 y RT-03 reales; entrega a Ventas solo si se ejecuta contra su receptor.

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
- [cite: 3] [Gestión §5.2.3](../../integraciones/api-contract-gestion-despachos.md#523-cerrar-como-devuelto-a-origen--es-f04-05), [modelo](../../arquitectura/modelo-datos.md) y [guía SDD](../../plantillas/sdd/README.md).
