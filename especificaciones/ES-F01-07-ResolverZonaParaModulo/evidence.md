# Evidencia de ES-F01-07: Resolver la zona de un destino para el módulo

**Estado:** Pendiente; la preparación documental no acredita implementación.

**Responsable de verificación:** Valqui.

**Última verificación funcional:** Pendiente.

## 1. Versión y entorno verificados

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), preparación del 16/10/2026 a partir de `91db8f8`.
- Repositorios y commits de código: pendientes, Gestión y Operación.
- Entorno, despliegue, datos y preparación: pendientes.
- Dependencias: integración con F-02 y consumo desde Operación no ejecutados; contrato remoto pendiente.
- Alcance efectivamente verificado: ningún criterio funcional ejecutado; solo preparación documental SDD.
- UI: no aplica; resolución interna sin interfaz nueva ni `ui.md`.
- Actualización del 26/10/2026: se incorpora la fuente postal `zonas_codigos_postales` con datos comunicados por la persona responsable. La preparación no acredita consulta al entorno, uso efectivo por el lector ni resolución de la precedencia pendiente DT-02.

## 2. Cobertura de criterios

| Criterio | Tarea | Prueba o comprobación | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02 a T-05 | San Isidro resuelve Lima Centro y F-02 asocia su zona | EV-02, EV-03, EV-04 | Pendiente |
| CA-02 | T-02, T-04, T-05 | Destino sin cobertura devuelve ausencia de zona | EV-02, EV-04 | Pendiente |
| CA-03 | T-02, T-04, T-05 | Zona inactiva no resuelve nuevos destinos | EV-02, EV-04 | Pendiente |
| CA-04 | T-02, T-04, T-05 | Ausencia de ambos identificadores rechazada | EV-02, EV-04 | Pendiente |
| CA-05 | T-03, T-05 | Despachos existentes conservan la zona desactivada | EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Un consumidor simulado no acredita integración real con Operación.

## 3. Registros de verificación

### EV-01. Revisión de consumo y datos

- Tareas y criterios: T-01; soporte de CA-01 a CA-05.
- Preparación y pasos previstos: revisar Gestión §6, consumidores F-02/F-05, destino y modelo; cerrar DT-01 a DT-04 con ejemplos y decisiones en documentos propietarios.
- Resultado esperado: mecanismo de consumo, normalización y consistencia definidos sin compartir tablas.
- Fecha, persona, revisión/commit y entorno: pendientes.
- Resultado observado y artefacto de revisión: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: no utilizadas; la revisión no prueba el backend.

### EV-02. Resolución local

- Tareas y criterios: T-02/T-05; CA-01 a CA-04.
- Preparación y pasos previstos: PostgreSQL aislado con Lima Centro, destino no cubierto y zonas inactivas; probar destino válido, inválido, postal y repetido con configuración estable.
- Resultado esperado: zona correcta o ausencia de cobertura, rechazo sin identificadores y ninguna escritura ni tarifa calculada.
- Fecha, persona, commit, entorno y comando exacto de la suite: pendientes.
- Resultado observado y reporte: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: datos locales controlados; no acredita consumo remoto.

### EV-03. Asociación y conservación en F-02

- Tareas y criterios: T-03/T-05; CA-01 y CA-05.
- Preparación y pasos previstos: crear despacho cubierto, desactivar su zona, resolver otra vez y comparar asociación previa; ejecutar concurrencia según DT-04.
- Resultado esperado: F-02 usa la zona resuelta y el despacho previo la conserva, aunque el nuevo destino quede sin cobertura.
- Fecha, persona, commit, entorno y comando/pasos exactos: pendientes.
- Resultado observado y artefacto: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: por registrar; la asociación requiere persistencia real de F-02.

### EV-04. Consumo remoto y rendimiento

- Tareas y criterios: T-04/T-05; CA-01 a CA-04 y coherencia/rendimiento.
- Preparación y pasos previstos: servicios reales e identidad técnica; consumir mecanismo acordado en Gestión, comprobar acceso no autorizado y coherencia para la misma configuración; medir carga y latencias según DT-05.
- Resultado esperado: consumo conforme al contrato, sin tablas compartidas ni reglas duplicadas; contrastar menos de 100 ms de F-01 §8.
- Fecha, persona, commits, entorno y comandos/pasos exactos: pendientes.
- Resultado observado, métricas y artefactos: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: por identificar; si se acuerda catálogo activo, documentar qué criterios verifica localmente y cuáles requieren resolución por destino en Gestión.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| Migración y preparación SDD | OpenCode, 16/10/2026 | Original, F-01, contratos, modelo y arquitectura en `91db8f8`; plantillas SDD y modelo ES-F01-05 | Completar las carpetas ES-F01-06, ES-F01-07 y ES-F01-08 según el modelo existente | Pendiente de revisión humana |

Se trasladaron reglas y criterios y se prepararon plan, tareas y registros pendientes; la normalización se identifica como decisión por revisar. No acredita ejecución de T-01 a T-05.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| DT-01: acceso de Operación sin contrato específico | Consumo de CA-01 a CA-04 | Bloquea I-03 | Valqui con F-05 y Arquitectura |
| DT-02: original admite distrito o postal, pero la lista de entradas indicaba distrito | CA-01, CA-02, CA-04 | Normalización/precedencia por revisar | Valqui con Backend y consumidores |
| DT-03: esquema real y lector de `zonas_distritos`/`zonas_codigos_postales` sin verificar | CA-01 a CA-03 | Bloquea integración local, aunque se comuniquen datos postales existentes | Valqui con Arquitectura |
| DT-04: consistencia entre resolución y creación concurrente | CA-01 y CA-05 | Bloquea aceptación con F-02 | Valqui con F-02 |
| DT-05: entorno/carga de medición sin concretar | Rendimiento | Sin evidencia de menos de 100 ms | Valqui con DevOps y Calidad |

No hay resultados de implementación ejecutados en esta preparación.

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor, fecha y resultado de revisión: pendientes.
- Estado del alcance: Pendiente.
- Integraciones reales pendientes: F-02, Operación y autenticación del consumidor remoto.

## 7. Referencias

1. [cite: 1] [Especificación](./spec.md), CA-01 a CA-05.
2. [cite: 2] [Plan](./plan.md) y [tareas](./tasks.md).
3. [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md) y [flujo SDD](../../plantillas/sdd/README.md).
