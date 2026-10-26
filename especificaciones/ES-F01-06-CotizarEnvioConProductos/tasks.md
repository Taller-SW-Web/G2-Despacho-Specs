# Tareas de ES-F01-06: Cotizar el envío con datos físicos de productos

**Responsable de coordinación:** Valqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparación documental del 16/10/2026, misma revisión de esta carpeta.

Actualización del 26/10/2026: se conserva la identidad de T-01 a T-05 y se agrega T-06 para el escritor exacto. La tabla creada y los datos postales son antecedentes comunicados; ninguna tarea de backend queda completada por ello.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato, precisión, calendario y datos conciliados; homologación física enlazada | Contrato/Datos | DT-01 a DT-03, DT-06/07 | CA-01 a CA-16 | Pendiente |
| T-02 | Motor, agrupación, validación integral y elegibilidad probados | Backend, I-01 | T-01 para las decisiones del incremento | CA-01 a CA-05, CA-10, CA-14 a CA-16 | Pendiente |
| T-03 | Endpoint autorizado y cliente HTTP real de Productos integrados | Backend/Integración, I-02 | T-02 y DT-05/06 | CA-01 a CA-10, CA-14 a CA-16 | Pendiente |
| T-06 | Escritor exacto, instantánea y rollback verificados | Backend/Persistencia, I-02 | T-02, T-03 y DT-02/07 | CA-11 a CA-13 | Pendiente |
| T-04 | Tasa y recorrido real con canales y G6 verificados | Gateway/Integración, I-03 | T-03, T-06 y DT-04/05/06 | CA-01 a CA-16 | Pendiente |
| T-05 | Evidencia y revisión final registradas | Calidad | T-01 a T-04 y T-06 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar causa y responsable al iniciar una tarea bloqueada. Todas las comprobaciones siguientes son previstas.

## 2. Detalle de tareas

### T-01. Cerrar las decisiones del contrato y del cálculo

- [ ] Implementada y verificada.
- Incremento: habilita I-01/I-02. Responsable: Valqui con Arquitectura, Backend y canales.
- Objetivo y entradas: revisar contrato §§5.1/5.2/11.1, modelo y DT-01 a DT-07. Publicar las tres respuestas propuestas, fijar revisión aceptada de G6 y precisar SKU afectados/estados. Concretar zona sin tarifa, escala/redondeo, calendario, fuente postal y mapeo de tarifa/instantánea.
- Dependencias: revisión de los responsables de los documentos propietarios.
- Verificación: contrastar todos los criterios, enlazar aceptación bilateral y grant G7 por separado; calcular el ejemplo con precisión completa/de salida y escalas de la tabla; comprobar calendario. Identificar repositorio/commit backend y comparar DDL real sin recrear tablas.
- Cierre: decisiones y revisiones enlazadas en contrato/modelo/plan, sin contrato paralelo.
- Evidencia prevista: [EV-01](./evidence.md#ev-01-revisión-de-contrato-y-datos) y EV-06. Bloqueo: decisiones del incremento y homologación externa; coordina Valqui.

### T-02. Implementar el motor y la resolución previa de cobertura

- [ ] Implementada y verificada.
- Incremento: I-01. Responsable: Valqui con Backend.
- Objetivo y entradas: cobertura compartida con ES-F01-05/07, agrupación conservando unidades, límite de 100 SKU únicos, validación del lote y fórmula F-01 con aritmética decimal/reloj controlable. Aplicar elegibilidad en F-01 sin trasladarla automáticamente a F-02.
- Dependencias: T-01 y fuentes locales de cobertura/tarifa disponibles.
- Verificación: totales, recargo y agrupación; cobertura previa a productos; listas/cantidades inválidas, inexistencia, error de negocio físico, `200` malformado, omisiones/duplicados/inesperados y estados homologados; 1/100/101 únicos y muchas líneas con pocos SKU. Sin datos autoritativos del cliente.
- Cierre: CA-01 a CA-05, CA-10 y CA-14 a CA-16 cubiertos en el núcleo; sin llamadas a Productos fuera de cobertura ni por exceso de SKU. El núcleo de cálculo no escribe: delega la instantánea al escritor T-06.
- Evidencia prevista: [EV-02](./evidence.md#ev-02-motor-y-validaciones). Bloqueo: fuentes o decisiones de T-01 pendientes; Valqui coordina.

### T-03. Integrar el endpoint y Productos con identidad propia

- [ ] Implementada y verificada.
- Incremento: I-02. Responsable: Valqui con Backend, Seguridad y Productos.
- Objetivo y entradas: conectar el motor y el cliente canónico de §5.2, gestionar token propio y traducción por HTTP/código. Revisar `CatalogoProductosStub`, `@Primary` y perfiles en el backend; asegurar cliente HTTP real en el perfil normal y compartir validador/transporte con F-02.
- Dependencias: T-02, DT-01 y DT-05/06; iniciar con doble del proveedor si aún falta entorno real, registrando la limitación y sin acreditar homologación.
- Verificación: contexto real de selección de adaptador y llamada saliente a la ruta exacta; casos CA-01 a CA-10/14/15/16, error físico `422`, caída `503`, respuesta inválida `502`, distrito ausente y token propio. Probar token ausente, inválido/vencido, audiencia incorrecta, scope ausente/correcto y rechazo de la credencial saliente sin atribuirlo al canal.
- Cierre: respuestas contractuales sin costo ante errores y sin pedidos/despachos; lote único, completo y con cantidades conservadas. La respuesta exacta se integra con T-06 antes de considerarse completa; los rechazos no escriben cotizaciones.
- Evidencia prevista: [EV-03](./evidence.md#ev-03-endpoint-seguridad-e-integración). Bloqueo: credenciales/entorno de DT-05; Valqui con Seguridad y Productos.

### T-04. Verificar tasa, rendimiento y consumo real

- [ ] Implementada y verificada.
- Incremento: I-03. Responsable: Valqui con DevOps, Calidad, Productos y canales.
- Objetivo y entradas: aplicar límite por `sub` e IP y recorrer la cotización por Gateway con servicios reales; medir la latencia exigida por F-01 §8.
- Dependencias: T-03, T-06 y acuerdos DT-04/05/06.
- Verificación: superar el límite y recibir `429` sin cálculo; comprobar aislamiento entre consumidores según configuración; ejecutar escenarios de cotización con proveedor real y reportar carga, caché y latencias medidas.
- Cierre: CA-09 y recorrido real comprobados; el canal muestra el costo logístico conforme al contrato; rendimiento contrastado con el umbral, sin declarar cumplimiento si falla.
- Evidencia prevista: [EV-04](./evidence.md#ev-04-tasa-rendimiento-y-recorrido-real). Bloqueo: entorno o configuración operativa; Valqui con DevOps.

### T-05. Cerrar trazabilidad y revisión

- [ ] Implementada y verificada.
- Incremento: cierre de I-03. Responsable: Valqui con Calidad.
- Objetivo y entradas: resultados de T-01 a T-04 y T-06, commits, revisión funcional y técnica y documentos de esta carpeta.
- Dependencias: T-01 a T-04, T-06 y dependencias reales disponibles.
- Verificación: recorrer cada criterio hacia tarea, prueba y registro; distinguir resultados simulados/reales y registrar comando exacto del backend y artefactos.
- Cierre: todos los criterios tienen resultados reproducibles, pendientes resueltos y revisión enlazada; índice actualizado cuando cambie el estado.
- Evidencia prevista: EV-01 a EV-06 y sección de entrega de [evidence.md](./evidence.md). Bloqueo: criterios o integración sin comprobar; Valqui coordina.

### T-06. Implementar la persistencia de cotizaciones exactas

- [ ] Implementada y verificada.
- Incremento: I-02, antes del recorrido I-03. Responsable: Valqui con Backend y Arquitectura.
- Objetivo y entradas: escritor de la tabla existente `cotizaciones` según modelo §3.1 y CA-11 a CA-13; mapear instantánea y respuesta desde el mismo cálculo. Mantener pedido/despacho/vencimiento nulos y el estado físico del DDL. El detalle conserva las entradas físicas usadas, su actualización y el desglose; no es caché ni maestro de catálogo.
- Dependencias: T-02/T-03 y cierre DT-02/07; tablas verificadas en entorno y repositorio backend identificado.
- Verificación: PostgreSQL real, correspondencia fila/respuesta/tarifa, cambio posterior de tarifa, repetición como instantánea independiente y nulos esperados. Comparar filas antes/después de cobertura, sin tarifa, seguridad, límite, errores G6 y todos los rechazos. Inyectar error en inserción y commit: rollback y error interno, sin costo exitoso.
- Cierre: escritura confirmada antes del `200 EXACTA`, llamada HTTP fuera de la transacción de escritura, ausencia de cotizaciones parciales y sin nuevas tablas de productos ni comandos de ciclo de vida.
- Evidencia prevista: [EV-05](./evidence.md#ev-05-persistencia-exacta-y-rollback). Bloqueo: backend/esquema/mapeo sin verificar; coordina Valqui.

## 3. Cobertura de criterios

| Criterio | Tareas que lo implementan | Verificación | Evidencia prevista |
|---|---|---|---|
| CA-01 | T-02, T-03, T-06 | T-02 a T-05, T-06 | EV-02, EV-03, EV-04, EV-05 |
| CA-02 | T-02, T-03 | T-02, T-03, T-05 | EV-02, EV-03 |
| CA-03 | T-02, T-03 | T-02, T-03, T-05 | EV-02, EV-03 |
| CA-04 | T-02, T-03 | T-03, T-05 | EV-03 |
| CA-05 | T-02, T-03 | T-03, T-05 | EV-03 |
| CA-06 | T-03 | T-03, T-05 | EV-03 |
| CA-07 | T-01, T-03 | T-03, T-05 | EV-01, EV-03 |
| CA-08 | T-03, T-06 | T-03 a T-05, T-06 | EV-03, EV-04, EV-05 |
| CA-09 | T-04 | T-04, T-05 | EV-04 |
| CA-10 | T-02, T-03 | T-02, T-03, T-05 | EV-02, EV-03 |
| CA-11 | T-06 | T-06, T-04, T-05 | EV-05, EV-04 |
| CA-12 | T-03, T-06 | T-03, T-06, T-05 | EV-03, EV-05 |
| CA-13 | T-06 | T-06, T-05 | EV-05 |
| CA-14 | T-02, T-03 | T-02, T-03, T-04, T-05 | EV-02, EV-03, EV-06 |
| CA-15 | T-01, T-02, T-03 | T-03, T-04, T-05 | EV-03, EV-06 |
| CA-16 | T-02, T-03 | T-02, T-03, T-05 | EV-02, EV-03 |

## 4. Cierre de la especificación

- [ ] Todas las tareas están implementadas y verificadas.
- [ ] CA-01 a CA-16 tienen evidencia reproducible y límites identificados.
- [ ] Integraciones reales, tasa y rendimiento están verificados.
- [ ] Documentos, índice, commits y revisión están enlazados.

## 5. Referencias

1. [cite: 1] [Especificación](./spec.md), criterios CA-01 a CA-16.
2. [cite: 2] [Plan](./plan.md), I-01 a I-03 y DT-01 a DT-07.
3. [cite: 3] [Evidencia](./evidence.md).
