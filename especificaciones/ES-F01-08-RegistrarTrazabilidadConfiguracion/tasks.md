# Tareas de ES-F01-08: Registrar la trazabilidad de la configuración

**Responsable de coordinación:** Valqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), preparación documental del 16/10/2026, misma revisión de esta carpeta.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Representación, identidad de operación y consulta acordadas | Contrato/Datos | DT-01 a DT-04 | CA-01 a CA-06 | Pendiente |
| T-02 | Persistencia de auditoría íntegra preparada | Backend/Datos, I-01 | T-01: DT-01/02 | CA-01, CA-03, CA-06 | Pendiente |
| T-03 | Operaciones de configuración auditadas atómicamente | Backend, I-02 | T-02 y ES-F01-02/03/04 | CA-01 a CA-04 | Pendiente |
| T-04 | Repetición segura y consulta autorizada verificadas | Backend/Integración, I-03 | T-03 y DT-03/04 | CA-03, CA-05, CA-06 | Pendiente |
| T-05 | Regresión, evidencia y revisión registradas | Calidad | T-01 a T-04 | Todos | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Registrar motivo y responsable al iniciar con dependencia bloqueada. Todas las comprobaciones siguientes son previstas.

## 2. Detalle de tareas

### T-01. Concretar modelo y contratos de trazabilidad

- [ ] Implementada y verificada.
- Incremento: habilita I-01 a I-03. Responsable: Valqui con Arquitectura, Backend y Seguridad.
- Objetivo y entradas: resolver DT-01 a DT-04 del [plan](./plan.md): sustitución tarifaria en un registro, marcas e identidad, repetición y consulta autorizada del histórico.
- Dependencias: revisión con responsables de ES-F01-02/03/04 y vistas consumidoras.
- Verificación: representar creación, edición, estado, sustitución tarifaria, rechazo y repetición; comprobar que actor e instante de las dos reglas pueden reconstruirse sin duplicar la operación.
- Cierre: decisiones revisadas en modelo y contrato de Gestión; no crear un endpoint de auditoría en esta carpeta.
- Evidencia prevista: [EV-01](./evidence.md#ev-01-revisión-de-modelo-e-identidad). Bloqueo: DT-01 a DT-04; Valqui coordina.

### T-02. Preparar persistencia de inserción y lectura

- [ ] Implementada y verificada.
- Incremento: I-01. Responsable: Valqui con Backend y Arquitectura.
- Objetivo y entradas: mapear `auditoria_configuracion`, valores anteriores/nuevos, ejecutor y UTC; revisar restricciones y aplicar migración solo si T-01 la define.
- Dependencias: decisiones DT-01/02 de T-01 y base PostgreSQL del servicio.
- Verificación: pruebas de persistencia con datos de zona/tarifa; validar restricciones, lectura y preservación de registros existentes tras migración si aplica.
- Cierre: repositorio sin operaciones de edición/eliminación de histórico desde la funcionalidad; identidad y fecha conservadas.
- Evidencia prevista: [EV-02](./evidence.md#ev-02-persistencia-e-integridad). Bloqueo: modelo o permisos pendientes; Valqui con Arquitectura.

### T-03. Integrar la auditoría en la transacción de configuración

- [ ] Implementada y verificada.
- Incremento: I-02. Responsable: Valqui con responsables de ES-F01-02/03/04.
- Objetivo y entradas: invocar registro desde creación, edición, activación/desactivación y alta/sustitución tarifaria; obtener identidad del JWT y hora del servidor.
- Dependencias: T-02 y casos de uso de configuración disponibles.
- Verificación: creación/edición y estados con antes/después; sustitución con nueva regla vigente y anterior inactiva; operación inválida sin auditoría de éxito; fallo de auditoría revierte el cambio y fallo del negocio no deja registro.
- Cierre: CA-01 a CA-04 y edición de zona cubiertos, sin escrituras parciales ni uso de identidad/hora libres del cliente.
- Evidencia prevista: [EV-03](./evidence.md#ev-03-captura-transaccional). Bloqueo: operaciones de origen pendientes; Valqui coordina.

### T-04. Verificar no duplicación y consulta del histórico

- [ ] Implementada y verificada.
- Incremento: I-03. Responsable: Valqui con Backend y responsables de vistas.
- Objetivo y entradas: aplicar identidad de operación y concurrencia acordadas en DT-03; exponer lectura autorizada solo según DT-04, conservando el histórico inmutable.
- Dependencias: T-03 y cierre de DT-03/04.
- Verificación: reenviar operación aceptada, duplicado concurrente y estado sin cambio sin otro registro; consultar reglas vigentes/inactivas y orden del servidor; rechazar acceso sin rol; comprobar que no hay mutación del histórico.
- Cierre: CA-05/06 comprobados y trazabilidad de CA-03 consultable; nuevas decisiones legítimas no se descartan como reintentos por mera igualdad de cuerpo.
- Evidencia prevista: [EV-04](./evidence.md#ev-04-repetición-y-consulta-autorizada). Bloqueo: identidad o contrato de consulta pendientes; Valqui coordina.

### T-05. Ejecutar regresión y completar revisión

- [ ] Implementada y verificada.
- Incremento: cierre de I-03. Responsable: Valqui con Calidad.
- Objetivo y entradas: recorrer todas las operaciones de configuración con los resultados de T-01 a T-04 y completar la trazabilidad.
- Dependencias: T-01 a T-04, base real y autenticación disponibles.
- Verificación: suite del backend con su Maven Wrapper disponible, registrando comando exacto, commits y reportes; contrastar número de operaciones aceptadas y registros, valores e integridad.
- Cierre: CA-01 a CA-06 con resultados reproducibles y revisión técnica/funcional; actualizar índice al cambiar el estado.
- Evidencia prevista: EV-01 a EV-04 y sección de entrega de [evidence.md](./evidence.md). Bloqueo: criterios sin comprobar; Valqui con Calidad.

## 3. Cobertura de criterios

| Criterio | Tareas que lo implementan | Verificación | Evidencia prevista |
|---|---|---|---|
| CA-01 | T-02, T-03 | T-03, T-05 | EV-02, EV-03 |
| CA-02 | T-03 | T-03, T-05 | EV-03 |
| CA-03 | T-01 a T-04 | T-03 a T-05 | EV-01, EV-03, EV-04 |
| CA-04 | T-03 | T-03, T-05 | EV-03 |
| CA-05 | T-04 | T-04, T-05 | EV-04 |
| CA-06 | T-02, T-04 | T-02, T-04, T-05 | EV-02, EV-04 |

## 4. Cierre de la especificación

- [ ] Todas las tareas están implementadas y verificadas.
- [ ] CA-01 a CA-06 tienen evidencia reproducible.
- [ ] Atomicidad, inmutabilidad, no duplicación y consulta autorizada están comprobadas.
- [ ] Documentos, índice, commits y revisión están enlazados.

## 5. Referencias

1. [cite: 1] [Especificación](./spec.md), CA-01 a CA-06.
2. [cite: 2] [Plan](./plan.md), I-01 a I-03 y DT-01 a DT-04.
3. [cite: 3] [Evidencia](./evidence.md).
