# Evidencia de ES-F01-06: Cotizar el envío con datos físicos de productos

**Estado:** Pendiente; la preparación documental no acredita implementación.

**Responsable de verificación:** Valqui.

**Última verificación funcional:** Pendiente.

## 1. Versión y entorno verificados

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), preparación del 16/10/2026 a partir de `91db8f8`.
- Repositorios y commits de código: pendientes, Gestión de Despachos y Gateway.
- Entorno, despliegue, datos y preparación: pendientes.
- Dependencias: Productos, Seguridad y canales no utilizados en esta preparación; simulaciones y servicios reales por identificar al ejecutar.
- Alcance efectivamente verificado: ningún criterio funcional ejecutado; solo preparación documental SDD.
- UI: no aplica; API consumida por canales, sin `ui.md`.

### Antecedentes comunicados y actualización del 26/10/2026

- La persona responsable aportó el DDL de `public.cotizaciones` y `zonas_codigos_postales`, aclaró que la primera solo está creada y la segunda tiene datos, y aceptó persistir únicamente cálculos exactos exitosos al completar F-01, antes de confirmar una venta.
- Se documenta `pedido_id` y `despacho_id` nulos al cotizar, exclusión de cobertura/rechazos y uso histórico del perfil físico y la tarifa. No se habilitan aceptación, vencimiento, cancelación ni asociación automática.
- El DDL comunicado contiene `pedido_id UUID`, estados físicos en minúsculas y escalas de peso/volumen que deben contrastarse con el cálculo. Esas observaciones no son un resultado de inspección de PostgreSQL.
- Se prepararon la matriz de errores, validación integral, límite de 100 SKU únicos y respuestas H-G2-01/02/03 en el [contrato §11.1](../../integraciones/api-contract.md#111-respuesta-propuesta-y-plan-de-homologación-física-g2g6). No se publicó un comentario en GitHub ni se acreditó aceptación de G6/G7.
- Alcance de esta actualización: documentación. Este workspace no contiene las clases Java reportadas; escritor, selección del cliente HTTP, grant de Seguridad y recorrido real permanecen sin ejecutar. Una tabla creada no acredita T-06 ni los nuevos criterios [cite: 3].

### Comprobación documental local del 26/10/2026

- `git diff --check`: ejecutado desde este repositorio, sin errores de formato del diff.
- Validación local en memoria con Python 3, sin crear archivos auxiliares: 33 Markdown modificados con enlaces locales, anclas y jerarquía de encabezados válidos; sin referencias a la operación física obsoleta en esos documentos.
- Se comprobaron los 16 identificadores de criterios de ES-F01-06 y los 10 de ES-F02-01 contra sus matrices de evidencia, conservando los identificadores anteriores.
- Resultado documental: correcto. No se ejecutaron pruebas funcionales, PostgreSQL ni servicios G2/G6/G7; los resultados de comportamiento de las matrices siguientes permanecen pendientes.

## 2. Cobertura de criterios

| Criterio | Tarea | Prueba o comprobación | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-02 a T-05, T-06 | Totales, costo, moneda, plazo y fecha esperados; instantánea confirmada | EV-02, EV-03, EV-04, EV-05 | Pendiente |
| CA-02 | T-02, T-03, T-05 | Sin cobertura: sin costo ni llamada a Productos | EV-02, EV-03 | Pendiente |
| CA-03 | T-02, T-03, T-05 | Líneas/cantidades inválidas en destino cubierto | EV-02, EV-03 | Pendiente |
| CA-04 | T-03, T-05 | SKU inexistente identificado sin costo | EV-03 | Pendiente |
| CA-05 | T-03, T-05 | Datos físicos incompletos sin costo | EV-03 | Pendiente |
| CA-06 | T-03, T-05 | Indisponibilidad sin costo estimado | EV-03 | Pendiente |
| CA-07 | T-01, T-03, T-05 | Zona activa sin tarifa: cobertura sin costo ni plazo | EV-01, EV-03 | Pendiente |
| CA-08 | T-03 a T-05, T-06 | Token técnico sin sesión humana ni creación de pedido/despacho; instantánea exacta confirmada | EV-03, EV-04, EV-05 | Pendiente |
| CA-09 | T-04, T-05 | Exceso de límite rechazado sin cálculo | EV-04 | Pendiente |
| CA-10 | T-02, T-03, T-05 | Peso/volumen del cliente no cambian el cálculo | EV-02, EV-03 | Pendiente |
| CA-11 | T-06, T-04, T-05 | Instantánea y respuesta coherentes, vínculos nulos, tarifa histórica y repetición | EV-05, EV-04 | Pendiente |
| CA-12 | T-03, T-06, T-05 | Cobertura y cada rechazo sin filas nuevas | EV-03, EV-05 | Pendiente |
| CA-13 | T-06, T-05 | Fallo en inserción/commit revierte y no devuelve costo exitoso | EV-05 | Pendiente |
| CA-14 | T-02, T-03, T-04, T-05 | Lote malformado/incompleto rechazado íntegramente | EV-02, EV-03, EV-06 | Pendiente |
| CA-15 | T-01, T-02, T-03, T-04, T-05 | Elegibilidad de estado sin confundir inexistencia | EV-03, EV-06 | Pendiente |
| CA-16 | T-02, T-03, T-05 | Cantidades conservadas y 1/100/101 SKU únicos | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Un doble no acredita integración con el proveedor real.

## 3. Registros de verificación

### EV-01. Revisión de contrato y datos

- Tareas y criterios: T-01; soporte de todos, en particular CA-01 y CA-07.
- Preparación y pasos previstos: revisar contrato §§5.1/5.2/11.1, modelo, precisión del ejemplo, calendario y decisiones DT-01 a DT-07; enlazar documentos revisados y decisiones pendientes de homologación.
- Resultado esperado: respuesta sin tarifa y cálculo definidos en documentos canónicos.
- Fecha, persona, revisión/commit y entorno: pendientes.
- Resultado observado y artefacto de revisión: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: no se han utilizado; la revisión documental no verifica el backend.

### EV-02. Motor y validaciones

- Tareas y criterios: T-02/T-05; CA-01 a CA-05, CA-10 y CA-14 a CA-16.
- Preparación y pasos previstos: datos físicos y tarifa del ejemplo, reloj/calendario controlados; ejecutar pruebas de cálculo, recargo, SKU repetidos, líneas inválidas y cobertura previa a validación.
- Resultado esperado: totales/costo según precisión acordada, sin datos físicos autoritativos del cliente ni consulta al proveedor fuera de cobertura.
- Fecha, persona, commit, entorno y comando exacto de la suite: pendientes.
- Resultado observado y reporte: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: doble de Productos previsto; no acredita disponibilidad ni autorización reales.

### EV-03. Endpoint, seguridad e integración

- Tareas y criterios: T-03/T-05; CA-01 a CA-08, CA-10 y CA-14 a CA-16; T-06 confirma las respuestas exactas.
- Preparación y pasos previstos: PostgreSQL aislado, tokens y proveedor controlado; verificar selección real del adaptador HTTP, ruta saliente, respuestas, distrito ausente, seguridad, fallos/timeout y token propio. Comparar ausencia de filas en cobertura/rechazos y conectar el escritor exacto comprobado en EV-05.
- Resultado esperado: lote íntegro con SKU únicos y cantidades conservadas; traducción diferenciada de `422` de negocio, `502` de respuesta inválida y `503` técnico; respuesta exacta solo después de la escritura confirmada.
- Fecha, persona, commit, entorno y comando exacto de la suite: pendientes.
- Resultado observado y reporte: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: proveedor controlado previsto; indicar cuáles casos también se ejecutaron con Productos real.

### EV-04. Tasa, rendimiento y recorrido real

- Tareas y criterios: T-04/T-05 y escritor T-06; recorrido de CA-01 a CA-16, especialmente CA-08/09, persistencia exacta y requisito de latencia.
- Preparación y pasos previstos: Gateway y servicios reales identificados, consumidores técnicos, configuración de tasa/caché y carga acordada; superar límite y medir latencias de solicitudes admitidas.
- Resultado esperado: rechazo por tasa sin cálculo y respuestas conformes; contrastar latencia con menos de 100 ms según F-01 §8.
- Fecha, persona, commits, entorno y comandos/pasos exactos: pendientes.
- Resultado observado, métricas y artefactos: pendientes.
- Resultado de la comprobación: Pendiente.
- Dependencias simuladas y límites: por registrar; ninguna simulación sustituye este recorrido real.

### EV-05. Persistencia exacta y rollback

- Tareas y criterios: T-06/T-04/T-05; CA-11 a CA-13 y exclusión transversal de errores.
- Preparación prevista: identificar commit backend y esquema real de `cotizaciones`; ejecutar el escritor sobre PostgreSQL aislado, comparar fila/desglose/respuesta y vínculos nulos. Sustituir tarifa y repetir solicitud; comprobar instantáneas independientes. Inyectar fallo de inserción y commit y comparar ausencia de registros parciales. Consultas de cobertura y todos los rechazos deben dejar el contador de filas sin cambios.
- Resultado esperado: una instantánea completa por ejecución exacta exitosa antes de devolver el costo, con tarifa histórica conservada y error interno al fallar la escritura; sin pedidos/despachos nuevos.
- Fecha, persona, commits, entorno, comando exacto y reporte: pendientes.
- Resultado observado: no ejecutado.
- Resultado de la comprobación: Pendiente.
- Límite: el SQL comunicado no acredita migración aplicada, escritor ni transacción ejecutados desde esta sesión.

### EV-06. Homologación física, seguridad y compatibilidad

- Tareas y criterios: T-01/T-03/T-04/T-05; CA-04/05/06/14/15/16 y seguridad.
- Preparación prevista: registrar enlace a respuestas/aceptación H-G2-01/02/03, commit del OpenAPI homologado, lista de SKU afectados y representación de `BORRADOR`. Con G7 acreditar concesión y credencial de `modulo-despacho`; ejecutar token ausente, inválido/vencido, audiencia incorrecta, scope ausente/correcto y consulta real desde F-01/F-02.
- Resultado esperado: reglas aceptadas y respuestas contractuales sin aproximaciones; elegibilidad distinta en cotización y pedido pagado, sin confundir estado e inexistencia.
- Enlaces bilaterales, grant, commits, entorno, comandos y resultados: pendientes.
- Resultado observado: no ejecutado.
- Resultado de la comprobación: Pendiente.
- Límite: una respuesta propuesta, un código en enum global o un doble HTTP no acreditan homologación, autorización ni E2E.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| Migración y preparación SDD | OpenCode, 16/10/2026 | Original, F-01, contratos y modelo en `91db8f8`; plantillas SDD y modelo ES-F01-05 | Completar las carpetas ES-F01-06, ES-F01-07 y ES-F01-08 según el modelo existente | Pendiente de revisión humana |

Se trasladaron las reglas y criterios y se prepararon plan, tareas y registros pendientes. OpenCode asistió también a la actualización documental del 26/10/2026 con los antecedentes SQL y la decisión de persistencia comunicados por la persona responsable; revisión humana pendiente. Este uso no acredita ejecución de T-01 a T-06.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| DT-01: zona sin tarifa sin respuesta contractual completa | CA-07 | Bloquea adaptador de ese caso | Valqui con Backend y canales |
| DT-02: redondeo y calendario pendientes; ejemplo suma `0.02126 m³` antes de redondear | CA-01 | Bloquea aceptación del cálculo y fecha | Valqui con Arquitectura y canales |
| DT-03: modelo de cobertura/tarifa por conciliar | CA-01, CA-02, CA-07 | Lectura local sin concretar | Valqui con Arquitectura |
| DT-04: tasa, timeout, caché y medición pendientes | CA-06, CA-09 y rendimiento | Bloquea verificación operativa | Valqui con DevOps y Productos |
| DT-05: tokens y entorno real sin verificar | CA-01 a CA-10 | Integración real pendiente | Valqui con Seguridad, Productos y canales |
| DT-06: H-G2-01/02/03 sin evidencia de aceptación bilateral ni revisión fija | CA-04/05/14/15/16 | Compatibilidad definitiva pendiente | Valqui con Productos y Calidad |
| DT-07: tabla creada comunicada, pero escritor/backend/esquema sin verificar | CA-11 a CA-13 | Persistencia exacta pendiente | Valqui con Backend y Arquitectura |

No hay resultados de implementación ejecutados en esta preparación.

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor, fecha y resultado de revisión: pendientes.
- Estado del alcance: Pendiente.
- Integraciones reales pendientes: Gateway, Seguridad, Productos y canales.

## 7. Referencias

1. [cite: 1] [Especificación](./spec.md), CA-01 a CA-16.
2. [cite: 2] [Plan](./plan.md) y [tareas](./tasks.md).
3. [cite: 3] [Contrato externo](../../integraciones/api-contract.md), [modelo de datos §§1.2 y 3.1](../../arquitectura/modelo-datos.md#12-persistencia-exacta-y-estado-comunicado-del-esquema) y [flujo SDD](../../plantillas/sdd/README.md). Los antecedentes del DDL proceden de la conversación de trabajo del 26/10/2026 y no de una ejecución de base de datos.
