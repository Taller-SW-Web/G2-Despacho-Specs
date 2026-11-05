# Tareas de ES-F01-06: Cotizar el envío con datos físicos de productos

**Responsable de coordinación:** Valqui.

**Estado:** Implementación y automatización local verificadas; cierre externo y revisión pendientes.

**Actualización 05/11/2026:** incremento local del consumidor en `feature/f01-integracion-g6-cotizaciones` (base `6af187c`), con CA-20 para redondeo confirmado. T-02, T-03, T-06, T-07 y T-08 tienen implementación local; la verificación reproducible y el alcance de dobles se registran en `evidence.md`. T-01 conserva calendario y revisión normativa externa; T-04 y T-05 requieren recorrido real/revisión. Esta nota no acredita despliegue ni aceptación integral.

**Plan de origen:** [plan.md](./plan.md), preparación documental del 16/10/2026, misma revisión de esta carpeta.

Actualización del 26/10/2026: se conserva la identidad de T-01 a T-05 y se agrega T-06 para el escritor exacto. La tabla creada y los datos postales son antecedentes comunicados; ninguna tarea de backend queda completada por ello.

Actualización del 03/11/2026: H-G2-01/02/03 cerrados y respuesta D publicada. Se agregan T-07/T-08 para D-G2-02 y sus regresiones; CA-15 incorpora el estado efectivo. Las nuevas tareas y comprobaciones funcionales comienzan pendientes, con DT-08 como dependencia contractual.

Actualización del 04/11/2026: D-G2-01/02 cerrados semánticamente; afectados, orden y precedencia aceptados. DT-08 conserva la publicación normativa y compatibilidad pendientes; las tareas del consumidor mantienen su estado hasta verificar sus resultados.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato, precisión, calendario y datos conciliados; H cerrados y seguimiento D enlazados | Contrato/Datos | DT-01 a DT-03, DT-06/07/08 para su incremento | CA-01 a CA-20 | En curso |
| T-02 | Motor, agrupación, validación integral y elegibilidad probados | Backend, I-01 | T-01 para las decisiones del incremento | CA-01 a CA-05, CA-10, CA-14 a CA-16 | Completada |
| T-03 | Endpoint autorizado y cliente HTTP real de Productos integrados | Backend/Integración, I-02 | T-02 y DT-05/06 | CA-01 a CA-10, CA-14 a CA-16 | En curso |
| T-06 | Escritor exacto, instantánea y rollback verificados | Backend/Persistencia, I-02 | T-02, T-03 y DT-02/07 | CA-11 a CA-13 | Completada |
| T-07 | Rechazo de SKU padre y afectados contractuales integrados en el consumidor | Backend/Integración, I-04 | T-03 y revisión exigible enlazada en DT-08; aceptación resuelta | CA-17 a CA-19 | En curso |
| T-08 | Regresiones de estado, detalle y precedencia verificadas | Calidad/Integración, I-04 | T-02, T-06, T-07 y revisión D acordada | CA-15, CA-17 a CA-19 | En curso |
| T-04 | Tasa y recorrido real con canales y G6 verificados | Gateway/Integración, I-03 | T-03, T-06, T-08 y DT-04/05/06/08 | CA-01 a CA-19 | Pendiente |
| T-05 | Evidencia y revisión final registradas | Calidad | T-01 a T-04 y T-06 a T-08 | Todos | Pendiente |
| T-09 | Redondeos confirmados y correspondencia histórica verificados | Backend/Calidad | T-02 y T-06 | CA-20 | Completada |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar causa y responsable al iniciar una tarea bloqueada. Todas las comprobaciones siguientes son previstas.

## 2. Detalle de tareas

### T-01. Cerrar las decisiones del contrato y del cálculo

- [ ] Implementada y verificada.
- Incremento: habilita I-01/I-02. Responsable: Valqui con Arquitectura, Backend y canales.
- Objetivo y entradas: revisar contrato §§5.1/5.2/11.1, modelo y DT-01 a DT-08. Utilizar H del 02/11 y cierre semántico D del 03–04/11; enlazar la revisión normativa que incorpora D antes de acreditar conformidad del incremento afectado. Concretar zona sin tarifa, escala/redondeo, calendario, fuente postal y mapeo de tarifa/instantánea.
- Dependencias: revisión de los responsables de los documentos propietarios.
- Verificación: contrastar todos los criterios, enlazar aceptación bilateral y grant G7 por separado; calcular el ejemplo con precisión completa/de salida y escalas de la tabla; comprobar calendario. Identificar repositorio/commit backend y comparar DDL real sin recrear tablas.
- Cierre: decisiones y revisiones enlazadas en contrato/modelo/plan, sin contrato paralelo.
- Evidencia prevista: [EV-01](./evidence.md#ev-01-revisión-de-contrato-y-datos) y EV-06. Bloqueo: decisiones del incremento y homologación externa; coordina Valqui.

### T-02. Implementar el motor y la resolución previa de cobertura

- [x] Implementada y verificada localmente con proveedor controlado; evidencia del 05/11/2026.
- Incremento: I-01. Responsable: Valqui con Backend.
- Objetivo y entradas: cobertura compartida con ES-F01-05/07, agrupación conservando unidades, límite de 100 SKU únicos, validación del lote y fórmula F-01 con aritmética decimal/reloj controlable. Aplicar elegibilidad en F-01 sin trasladarla automáticamente a F-02.
- Dependencias: T-01 y fuentes locales de cobertura/tarifa disponibles.
- Verificación: totales, recargo y agrupación; cobertura previa a productos; listas/cantidades inválidas, inexistencia, error de negocio físico, `200` malformado, omisiones/duplicados/inesperados y estado efectivo recibido según D-G2-01; 1/100/101 únicos y muchas líneas con pocos SKU. G6 proyecta la jerarquía; G2 no la reconstruye ni toma medidas autoritativas del cliente.
- Cierre: CA-01 a CA-05, CA-10 y CA-14 a CA-16 cubiertos en el núcleo; sin llamadas a Productos fuera de cobertura ni por exceso de SKU. El núcleo de cálculo no escribe: delega la instantánea al escritor T-06.
- Evidencia prevista: [EV-02](./evidence.md#ev-02-motor-y-validaciones). Bloqueo: fuentes o decisiones de T-01 pendientes; Valqui coordina.

### T-03. Integrar el endpoint y Productos con identidad propia

- [ ] Implementada y verificada.
- Incremento: I-02. Responsable: Valqui con Backend, Seguridad y Productos.
- Objetivo y entradas: conectar el motor y el cliente canónico de §5.2, gestionar token propio y traducción por HTTP/código. Revisar `CatalogoProductosStub`, `@Primary` y perfiles en el backend; asegurar cliente HTTP real en el perfil normal y compartir validador/transporte con F-02.
- Dependencias: T-02, DT-01 y DT-05/06; iniciar con doble del proveedor si aún falta entorno real, registrando la limitación y sin acreditar integración real.
- Verificación: contexto real de selección de adaptador y llamada saliente a la ruta exacta; casos CA-01 a CA-10/14/15/16, error físico `422`, caída `503`, respuesta inválida `502`, distrito ausente y token propio. Probar token ausente, inválido/vencido, audiencia incorrecta, scope ausente/correcto y rechazo de la credencial saliente sin atribuirlo al canal.
- Cierre: respuestas contractuales sin costo ante errores y sin pedidos/despachos; lote único, completo y con cantidades conservadas. La respuesta exacta se integra con T-06 antes de considerarse completa; los rechazos no escriben cotizaciones.
- Evidencia prevista: [EV-03](./evidence.md#ev-03-endpoint-seguridad-e-integración). Bloqueo: credenciales/entorno de DT-05; Valqui con Seguridad y Productos.

### T-04. Verificar tasa, rendimiento y consumo real

- [ ] Implementada y verificada.
- Incremento: I-03. Responsable: Valqui con DevOps, Calidad, Productos y canales.
- Objetivo y entradas: aplicar límite por `sub` e IP y recorrer la cotización por Gateway con servicios reales; medir la latencia exigida por F-01 §8.
- Dependencias: T-03, T-06, T-08 y acuerdos DT-04/05/06/08 para el alcance D.
- Verificación: superar el límite y recibir `429` sin cálculo; comprobar aislamiento entre consumidores según configuración; ejecutar escenarios de cotización con proveedor real y reportar carga, caché y latencias medidas.
- Cierre: CA-09 y recorrido real comprobados; el canal muestra el costo logístico conforme al contrato; rendimiento contrastado con el umbral, sin declarar cumplimiento si falla.
- Evidencia prevista: [EV-04](./evidence.md#ev-04-tasa-rendimiento-y-recorrido-real). Bloqueo: entorno o configuración operativa; Valqui con DevOps.

### T-05. Cerrar trazabilidad y revisión

- [ ] Implementada y verificada.
- Incremento: cierre de I-03. Responsable: Valqui con Calidad.
- Objetivo y entradas: resultados de T-01 a T-04 y T-06 a T-08, commits, revisión funcional y técnica y documentos de esta carpeta.
- Dependencias: T-01 a T-04, T-06 a T-08 y dependencias reales disponibles.
- Verificación: recorrer cada criterio hacia tarea, prueba y registro; distinguir resultados simulados/reales y registrar comando exacto del backend y artefactos.
- Cierre: todos los criterios tienen resultados reproducibles, pendientes resueltos y revisión enlazada; índice actualizado cuando cambie el estado.
- Evidencia prevista: EV-01 a EV-07 y sección de entrega de [evidence.md](./evidence.md). Bloqueo: criterios o integración sin comprobar; Valqui coordina.

### T-06. Implementar la persistencia de cotizaciones exactas

- [x] Implementada y verificada con PostgreSQL desechable; inserción, commit y rollback comprobados el 05/11/2026.
- Incremento: I-02, antes del recorrido I-03. Responsable: Valqui con Backend y Arquitectura.
- Objetivo y entradas: escritor de la tabla existente `cotizaciones` según modelo §3.1 y CA-11 a CA-13; mapear instantánea y respuesta desde el mismo cálculo. Mantener pedido/despacho/vencimiento nulos y el estado físico del DDL. El detalle conserva las entradas físicas usadas, su actualización y el desglose; no es caché ni maestro de catálogo.
- Dependencias: T-02/T-03 y cierre DT-02/07; tablas verificadas en entorno y repositorio backend identificado.
- Verificación: PostgreSQL real, correspondencia fila/respuesta/tarifa, cambio posterior de tarifa, repetición como instantánea independiente y nulos esperados. Comparar filas antes/después de cobertura, sin tarifa, seguridad, límite, errores G6 y todos los rechazos. Inyectar error en inserción y commit: rollback y error interno, sin costo exitoso.
- Cierre: escritura confirmada antes del `200 EXACTA`, llamada HTTP fuera de la transacción de escritura, ausencia de cotizaciones parciales y sin nuevas tablas de productos ni comandos de ciclo de vida.
- Evidencia prevista: [EV-05](./evidence.md#ev-05-persistencia-exacta-y-rollback). Bloqueo: backend/esquema/mapeo sin verificar; coordina Valqui.

### T-07. Incorporar el rechazo identificado de SKU padre

- [ ] Implementada y verificada.
- Incremento: I-04. Responsable: Valqui con Backend, Productos y Tarqui para el adaptador compartido.
- Entradas y alcance: contrato §5.2.4 con D-G2-02 cerrado semánticamente; deserializar el detalle, validar todos y únicamente los afectados exactos, sin duplicados y en orden de solicitud, y preservarlos en el problema público. Distinguir el caso acordado de las otras causas de `SKU_INVALIDO`; clasificar el error no conforme con el `502` contractual, sin analizar texto libre ni sustituir la lista por toda la solicitud. Traducir el error seleccionado según la precedencia aceptada, cuya evaluación corresponde al proveedor.
- Dependencias: T-03 y revisión exigible D-G2-02 publicada y enlazada en DT-08. Un doble del acuerdo cerrado permite preparación, no cierre de esta tarea.
- Verificación/cierre: CA-17/18 con padres solos, múltiples y mezclados con SKU válidos; producto simple válido; detalle ausente/vacío/malformado/duplicado/ajeno. Sin costo ni escritura parcial; conservar SKU opacos, correlación y orden acordado.
- Evidencia prevista: EV-07. Pendiente normativo: DT-08; coordina Valqui con G6.

### T-08. Verificar las regresiones D-G2-01/02

- [ ] Implementada y verificada.
- Incremento: I-04. Responsable: Valqui con Calidad y Productos.
- Alcance: CA-15 y CA-17 a CA-19; contrastar nueve combinaciones padre/variante del proveedor y estados simples, y comprobar que F-01 decide por el estado efectivo recibido. Ejecutar matrices de errores identificados y permutaciones según contrato §5.2.4: mismo código/conjunto de afectados y lista en orden de cada solicitud. Incluir lotes sin bases con perfiles incompletos, `200` con inexistentes y fallos técnicos.
- Dependencias: T-02, T-06, T-07 y publicación normativa D-G2-01/02; proveedor controlado primero, recorrido real en T-04.
- Verificación/cierre: respuestas y afectados contractuales, sin filas nuevas en cada rechazo y sin cambios de política comercial de F-02. Registrar revisión usada y distinguir proveedor simulado/real; las pruebas reportadas por G6 no acreditan la ejecución del consumidor G2.
- Evidencia prevista: EV-07 y EV-06 para el recorrido externo. Bloqueo: DT-08 o datos del proveedor; Valqui con Calidad.

## 3. Cobertura de criterios

### T-09. Redondear resultados y conservar la precisión exacta

- Alcance: CA-20; usar `BigDecimal`, costo al siguiente múltiplo de `0.50` y volumen informado hacia arriba a tres decimales.
- Dependencias: T-02 y T-06; decisión del usuario del 05/11/2026.
- Verificación: ejemplos, múltiplos exactos, valores apenas superiores a un múltiplo, acumulación previa al redondeo, costo calculado con volumen exacto y correspondencia con la fila histórica.
- Estado: Completada localmente; resultados reproducibles en la actualización de evidencia del 05/11/2026. El cierre integral conserva las dependencias externas.

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
| CA-15 | T-01, T-02, T-03 | T-03, T-04, T-05, T-08 | EV-03, EV-06, EV-07 |
| CA-16 | T-02, T-03 | T-02, T-03, T-05 | EV-02, EV-03 |
| CA-17 | T-07 | T-07, T-08, T-04, T-05 | EV-07, EV-06 |
| CA-18 | T-07 | T-07, T-08, T-05 | EV-07 |
| CA-19 | T-07 | T-08, T-04, T-05 | EV-07, EV-06 |
| CA-20 | T-02, T-06, T-09 | Pruebas de redondeo y PostgreSQL | Actualización de evidencia del 05/11/2026 |

## 4. Cierre de la especificación

- [ ] Todas las tareas están implementadas y verificadas.
- [ ] CA-01 a CA-19 tienen evidencia reproducible y límites identificados.
- [ ] Integraciones reales, tasa y rendimiento están verificados.
- [ ] Documentos, índice, commits y revisión están enlazados.

## 5. Referencias

1. [cite: 1] [Especificación](./spec.md), criterios CA-01 a CA-19.
2. [cite: 2] [Plan](./plan.md), I-01 a I-04 y DT-01 a DT-08.
3. [cite: 3] [Evidencia](./evidence.md).
