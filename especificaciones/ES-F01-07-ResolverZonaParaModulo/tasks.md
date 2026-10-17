# Tareas de ES-F01-07: Resolver la zona de un destino para el módulo

**Responsable de coordinación:** Valqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparación documental del 16/10/2026, misma revisión de esta carpeta.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Consumo, normalización y modelo acordados | Contrato/Datos | DT-01 a DT-04 | CA-01 a CA-05 | Pendiente |
| T-02 | Resolución local única implementada y probada | Backend, I-01 | T-01: DT-02/03 | CA-01 a CA-04 | Pendiente |
| T-03 | F-02 integrado y asociaciones previas conservadas | Integración, I-02 | T-02 y DT-04 | CA-01 y CA-05 | Pendiente |
| T-04 | Consumo de Operación y rendimiento verificados | Integración, I-03 | T-01 a T-03 y DT-05 | CA-01 a CA-05 | Pendiente |
| T-05 | Evidencia y revisión final registradas | Calidad | T-01 a T-04 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar causa y responsable si una dependencia impide iniciar. Todas las comprobaciones siguientes son previstas.

## 2. Detalle de tareas

### T-01. Acordar las entradas y el consumo de cobertura

- [ ] Implementada y verificada.
- Incremento: habilita I-01 a I-03. Responsable: Valqui con Arquitectura, F-02 y F-05.
- Objetivo y entradas: resolver DT-01 a DT-04 del [plan](./plan.md) usando F-01 RF-04, contrato de Gestión §6 y modelo; definir acceso de Operación, normalización, mapeo y frontera de consistencia con F-02.
- Dependencias: revisión de los consumidores y propietarios de contrato/modelo.
- Verificación: contrastar distrito solo, código postal solo, ambos coincidentes/conflictivos y ausencia de ambos; comprobar permisos y respuestas del mecanismo acordado.
- Cierre: decisiones registradas en documentos canónicos sin inventar rutas locales ni acceso compartido a tablas.
- Evidencia prevista: [EV-01](./evidence.md#ev-01-revisión-de-consumo-y-datos). Bloqueo: acuerdos DT-01 a DT-04; coordina Valqui.

### T-02. Implementar la resolución local compartida

- [ ] Implementada y verificada.
- Incremento: I-01. Responsable: Valqui con Backend.
- Objetivo y entradas: caso de uso único de cobertura según [spec.md](./spec.md), compartido con ES-F01-05/06, usando el modelo conciliado.
- Dependencias: decisiones DT-02/03 de T-01.
- Verificación: suite unitaria e integración PostgreSQL: Lima Centro, destino no cubierto, zonas inactivas, destino inválido y repetición estable mientras no cambie la configuración.
- Cierre: CA-01 a CA-04 cubiertos en resolución local, sin escrituras ni cálculo de tarifas.
- Evidencia prevista: [EV-02](./evidence.md#ev-02-resolución-local). Bloqueo: normalización o datos sin conciliar; Valqui con Arquitectura.

### T-03. Integrar F-02 y preservar las asociaciones existentes

- [ ] Implementada y verificada.
- Incremento: I-02. Responsable: Valqui con responsable de F-02.
- Objetivo y entradas: F-02 consulta el caso de uso local y asocia la zona devuelta sin mantener reglas propias; aplica DT-04.
- Dependencias: T-02 y decisión DT-04 de T-01.
- Verificación: crear despacho en San Isidro, desactivar Lima Centro y resolver nuevamente; comprobar que el nuevo destino queda sin cobertura y el despacho previo conserva su zona. Probar cambio concurrente según acuerdo.
- Cierre: CA-01 y CA-05 comprobados de extremo a extremo con F-02.
- Evidencia prevista: [EV-03](./evidence.md#ev-03-asociación-y-conservación-en-f-02). Bloqueo: caso de uso de F-02 o acuerdo de consistencia; Valqui con F-02.

### T-04. Verificar consumo de Operación y rendimiento

- [ ] Implementada y verificada.
- Incremento: I-03. Responsable: Valqui con F-05, Seguridad y DevOps.
- Objetivo y entradas: implementar el mecanismo acordado en DT-01, comprobar identidad técnica y coherencia de cobertura, y medir latencia bajo DT-05.
- Dependencias: T-01 a T-03; DT-05 y servicios/credenciales de prueba disponibles.
- Verificación: recorrer consumo de Operación según contrato, rechazar acceso no autorizado y contrastar información con F-02 para la misma configuración; medir el umbral de F-01 §8 con carga y entorno registrados.
- Cierre: integración real sin acceso a tablas ajenas y medición reproducible; los dobles iniciales se identifican sin acreditar el recorrido real.
- Evidencia prevista: [EV-04](./evidence.md#ev-04-consumo-remoto-y-rendimiento). Bloqueo: contrato o entorno de Operación; Valqui coordina.

### T-05. Completar la trazabilidad y revisión

- [ ] Implementada y verificada.
- Incremento: cierre de I-03. Responsable: Valqui con Calidad.
- Objetivo y entradas: reunir reportes, commits, decisiones y revisión de todos los criterios.
- Dependencias: T-01 a T-04 y servicios reales disponibles.
- Verificación: recorrer CA-01 a CA-05 hacia pruebas y registros, anotar el comando exacto del Maven Wrapper del backend y comprobar que no existe lógica de cobertura duplicada.
- Cierre: evidencia reproducible y revisión funcional/técnica enlazadas; actualizar estado del índice cuando corresponda.
- Evidencia prevista: EV-01 a EV-04 y sección de entrega de [evidence.md](./evidence.md). Bloqueo: criterios o integraciones sin verificar; Valqui con Calidad.

## 3. Cobertura de criterios

| Criterio | Tareas que lo implementan | Verificación | Evidencia prevista |
|---|---|---|---|
| CA-01 | T-02, T-03 | T-02 a T-05 | EV-02, EV-03, EV-04 |
| CA-02 | T-02, T-04 | T-02, T-04, T-05 | EV-02, EV-04 |
| CA-03 | T-02, T-04 | T-02, T-04, T-05 | EV-02, EV-04 |
| CA-04 | T-02, T-04 | T-02, T-04, T-05 | EV-02, EV-04 |
| CA-05 | T-03 | T-03, T-05 | EV-03 |

## 4. Cierre de la especificación

- [ ] Todas las tareas están implementadas y verificadas.
- [ ] CA-01 a CA-05 tienen evidencia reproducible y límites identificados.
- [ ] Consumo real, estabilidad, conservación y rendimiento están comprobados.
- [ ] Documentos, índice, commits y revisión están enlazados.

## 5. Referencias

1. [cite: 1] [Especificación](./spec.md), CA-01 a CA-05.
2. [cite: 2] [Plan](./plan.md), I-01 a I-03 y DT-01 a DT-05.
3. [cite: 3] [Evidencia](./evidence.md).
