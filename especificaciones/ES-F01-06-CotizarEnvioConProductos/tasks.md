# Tareas de ES-F01-06: Cotizar el envío con datos físicos de productos

**Responsable de coordinación:** Valqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparación documental del 16/10/2026, misma revisión de esta carpeta.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato, precisión, calendario y datos conciliados | Contrato/Datos | DT-01 a DT-03 | CA-01 a CA-10 | Pendiente |
| T-02 | Motor de cálculo y agrupación probado | Backend, I-01 | T-01 | CA-01 a CA-05, CA-10 | Pendiente |
| T-03 | Endpoint autorizado y cliente de Productos integrados | Backend/Integración, I-02 | T-02 y DT-05 | CA-01 a CA-08, CA-10 | Pendiente |
| T-04 | Tasa y recorrido real con canales verificados | Gateway/Integración, I-03 | T-03 y DT-04/05 | CA-01 a CA-10 | Pendiente |
| T-05 | Evidencia y revisión final registradas | Calidad | T-01 a T-04 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar causa y responsable al iniciar una tarea bloqueada. Todas las comprobaciones siguientes son previstas.

## 2. Detalle de tareas

### T-01. Cerrar las decisiones del contrato y del cálculo

- [ ] Implementada y verificada.
- Incremento: habilita I-01/I-02. Responsable: Valqui con Arquitectura, Backend y canales.
- Objetivo y entradas: revisar [spec.md](./spec.md), contrato externo §§5.1/5.2, modelo y pendientes DT-01 a DT-03; concretar zona sin tarifa, escala/redondeo, calendario y mapeo de datos.
- Dependencias: revisión de los responsables de los documentos propietarios.
- Verificación: contrastar solicitudes/respuestas de todos los criterios; calcular el ejemplo con precisión completa y de salida; comprobar calendario con fin de semana y día no laborable acordado.
- Cierre: decisiones y revisiones enlazadas en contrato/modelo/plan, sin contrato paralelo.
- Evidencia prevista: [EV-01](./evidence.md#ev-01-revisión-de-contrato-y-datos). Bloqueo: DT-01 a DT-03; coordina Valqui.

### T-02. Implementar el motor y la resolución previa de cobertura

- [ ] Implementada y verificada.
- Incremento: I-01. Responsable: Valqui con Backend.
- Objetivo y entradas: cobertura compartida con ES-F01-05/07, agrupación de SKU, validaciones y fórmula de F-01 con aritmética decimal y reloj/calendario controlables.
- Dependencias: T-01 y fuentes locales de cobertura/tarifa disponibles.
- Verificación: pruebas unitarias de totales, recargo y agrupación; sin cobertura incluso con líneas inválidas; con cobertura, lista vacía, cantidad inválida, SKU desconocido y datos físicos incompletos; datos del cliente ignorados.
- Cierre: CA-01 a CA-05 y CA-10 cubiertos en el núcleo, sin llamadas a Productos fuera de cobertura ni escrituras de negocio.
- Evidencia prevista: [EV-02](./evidence.md#ev-02-motor-y-validaciones). Bloqueo: fuentes o decisiones de T-01 pendientes; Valqui coordina.

### T-03. Integrar el endpoint y Productos con identidad propia

- [ ] Implementada y verificada.
- Incremento: I-02. Responsable: Valqui con Backend, Seguridad y Productos.
- Objetivo y entradas: conectar el motor a la operación del contrato §5.1 y el cliente en lote de §5.2; gestionar token de `modulo-despacho`, errores y zona sin tarifa.
- Dependencias: T-02, DT-01 y DT-05; iniciar con doble del proveedor si aún falta entorno real, registrando la limitación.
- Verificación: suite de integración del backend con PostgreSQL y proveedor controlado; casos CA-01 a CA-08/10, timeout/indisponibilidad, distrito ausente, token ausente/sin scope y token saliente distinto del recibido.
- Cierre: respuestas contractuales sin costo ante errores; no crea pedido/despacho ni persiste cotización; el lote contiene SKU únicos.
- Evidencia prevista: [EV-03](./evidence.md#ev-03-endpoint-seguridad-e-integración). Bloqueo: credenciales/entorno de DT-05; Valqui con Seguridad y Productos.

### T-04. Verificar tasa, rendimiento y consumo real

- [ ] Implementada y verificada.
- Incremento: I-03. Responsable: Valqui con DevOps, Calidad, Productos y canales.
- Objetivo y entradas: aplicar límite por `sub` e IP y recorrer la cotización por Gateway con servicios reales; medir la latencia exigida por F-01 §8.
- Dependencias: T-03 y acuerdos DT-04/05.
- Verificación: superar el límite y recibir `429` sin cálculo; comprobar aislamiento entre consumidores según configuración; ejecutar escenarios de cotización con proveedor real y reportar carga, caché y latencias medidas.
- Cierre: CA-09 y recorrido real comprobados; el canal muestra el costo logístico conforme al contrato; rendimiento contrastado con el umbral, sin declarar cumplimiento si falla.
- Evidencia prevista: [EV-04](./evidence.md#ev-04-tasa-rendimiento-y-recorrido-real). Bloqueo: entorno o configuración operativa; Valqui con DevOps.

### T-05. Cerrar trazabilidad y revisión

- [ ] Implementada y verificada.
- Incremento: cierre de I-03. Responsable: Valqui con Calidad.
- Objetivo y entradas: resultados de T-01 a T-04, commits, revisión funcional y técnica y documentos de esta carpeta.
- Dependencias: T-01 a T-04 y dependencias reales disponibles.
- Verificación: recorrer cada criterio hacia tarea, prueba y registro; distinguir resultados simulados/reales y registrar comando exacto del backend y artefactos.
- Cierre: todos los criterios tienen resultados reproducibles, pendientes resueltos y revisión enlazada; índice actualizado cuando cambie el estado.
- Evidencia prevista: EV-01 a EV-04 y sección de entrega de [evidence.md](./evidence.md). Bloqueo: criterios o integración sin comprobar; Valqui coordina.

## 3. Cobertura de criterios

| Criterio | Tareas que lo implementan | Verificación | Evidencia prevista |
|---|---|---|---|
| CA-01 | T-02, T-03 | T-02 a T-05 | EV-02, EV-03, EV-04 |
| CA-02 | T-02, T-03 | T-02, T-03, T-05 | EV-02, EV-03 |
| CA-03 | T-02, T-03 | T-02, T-03, T-05 | EV-02, EV-03 |
| CA-04 | T-02, T-03 | T-03, T-05 | EV-03 |
| CA-05 | T-02, T-03 | T-03, T-05 | EV-03 |
| CA-06 | T-03 | T-03, T-05 | EV-03 |
| CA-07 | T-01, T-03 | T-03, T-05 | EV-01, EV-03 |
| CA-08 | T-03 | T-03 a T-05 | EV-03, EV-04 |
| CA-09 | T-04 | T-04, T-05 | EV-04 |
| CA-10 | T-02, T-03 | T-02, T-03, T-05 | EV-02, EV-03 |

## 4. Cierre de la especificación

- [ ] Todas las tareas están implementadas y verificadas.
- [ ] CA-01 a CA-10 tienen evidencia reproducible y límites identificados.
- [ ] Integraciones reales, tasa y rendimiento están verificados.
- [ ] Documentos, índice, commits y revisión están enlazados.

## 5. Referencias

1. [cite: 1] [Especificación](./spec.md), criterios CA-01 a CA-10.
2. [cite: 2] [Plan](./plan.md), I-01 a I-03 y DT-01 a DT-05.
3. [cite: 3] [Evidencia](./evidence.md).
