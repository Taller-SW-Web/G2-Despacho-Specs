# Tareas de ES-F01-05: Consultar la cobertura de un destino

**Responsable de coordinación:** Valqui.

**Estado:** Pendiente de implementación.

**Plan de origen:** [plan.md](./plan.md), misma revisión documental que esta carpeta.

Esta entrega prepara las tareas; no ejecuta cambios de contrato ni código. No hay UI ni componentes asociados; la operación es de API de servicio.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato del DTO y errores de cobertura concretado | Contrato | Revisión posterior DT-01 | CA-01 a CA-05 | Pendiente |
| T-02 | Base compartida de datos, errores y tokens de servicio preparada | Preparación backend | DT-03; coordinación con Arquitectura/DevOps/Seguridad | Soporte de CA-01 a CA-05 | Pendiente |
| T-03 | Casos de uso de evaluación de cobertura implementados y probados | Backend, I-01/I-02 | T-01 y T-02 | CA-01 a CA-03 | Pendiente |
| T-04 | Autorización por token de servicio y scope verificada | Backend/Seguridad, I-02 | T-02 y T-03 | CA-04 | Pendiente |
| T-05 | Límite de tasa por `sub` e IP aplicado y probado | Backend/Gateway, I-03 | T-03 y DT-05 | CA-05 | Pendiente |
| T-06 | Consumo de Marketplace y Chatbot verificado | Integración, I-03 | T-04 y DT-04 | CA-01 a CA-04 | Pendiente |
| T-07 | Cobertura, evidencia y revisión del alcance completadas | Calidad | T-03 a T-06 | Todos los criterios del alcance | Pendiente |

Estados permitidos: `Pendiente`, `En curso`, `Bloqueada`, `Completada`. Al iniciar una tarea cuya dependencia no esté disponible, registrar el bloqueo y su responsable.

## 2. Detalle de tareas

### T-01. Concretar el contrato del DTO y los errores

- [ ] Implementada y verificada.

- Incremento del plan: habilita I-01.
- Responsable: Valqui con Backend y Arquitectura.
- Objetivo y alcance: resolver DT-01 en `integraciones/api-contract.md`: campos de la respuesta de cobertura, códigos de error y forma del mensaje fuera de cobertura; enlazarlo desde los documentos consumidores.
- Entradas: contrato externo §5.1 y §10.1 y [spec.md](./spec.md).
- Dependencias: revisión posterior a DT-01.
- Verificación: revisión de solicitudes/respuestas representativas para CA-01 a CA-05, sin crear un segundo contrato.
- Condición de cierre: decisión y revisión enlazadas. Esta tarea no se ejecuta en la preparación documental actual.
- Evidencia: pendiente.
- Bloqueo, si existe: cierre de DT-01.

### T-02. Preparar la base compartida del backend

- [ ] Implementada y verificada.

- Incremento del plan: soporte de I-01/I-02.
- Responsable: coordinación de Valqui con Arquitectura, DevOps y Seguridad.
- Objetivo y alcance: revisar el esquema y las migraciones; disponer de la base de errores, conexión de datos, rutas del Gateway y emisión de tokens de servicio con scope.
- Entradas: DT-03 del plan y modelo de datos.
- Dependencias: ninguna.
- Verificación: compilación y arranque del servicio con la configuración acordada.
- Condición de cierre: herramientas, comandos y resultados reales registrados.
- Evidencia: pendiente; completar enlace a EV-02 en evidence.md.
- Bloqueo, si existe: disponibilidad de Seguridad y DevOps.

### T-03. Implementar y probar la evaluación de cobertura

- [ ] Implementada y verificada.

- Incremento del plan: I-01/I-02.
- Responsable: Valqui con Backend.
- Objetivo y alcance: caso de uso que normaliza el destino, busca la zona `ACTIVO` y compone la respuesta sin costo, con sus errores.
- Entradas: contrato cerrado, datos de zonas y distritos, base de errores disponible; reglas de [spec.md](./spec.md).
- Dependencias: T-01 y T-02.
- Verificación: `./mvnw.cmd test` desde Gestión; PostgreSQL aislado; destino cubierto y no cubierto; ausencia de `distrito`.
- Condición de cierre: CA-01 a CA-03 cubiertos en backend, sin modificar recursos.
- Evidencia: pendiente; completar enlace a EV-01.
- Bloqueo, si existe: contrato y base pendientes.

### T-04. Verificar la autorización por token de servicio

- [ ] Implementada y verificada.

- Incremento del plan: I-02.
- Responsable: Valqui con Seguridad.
- Objetivo y alcance: validar el token de servicio y exigir el scope `cotizaciones:calcular`; rechazar sin revelar cobertura.
- Entradas: contrato §3.4 y §8; base de tokens de T-02.
- Dependencias: T-02 y T-03.
- Verificación: pruebas con token ausente, token inválido y token sin scope.
- Condición de cierre: CA-04 cubierto; el canal no accede a configuración interna.
- Evidencia: pendiente; completar enlace a EV-01.
- Bloqueo, si existe: emisión de tokens de servicio pendiente.

### T-05. Aplicar y probar el límite de tasa

- [ ] Implementada y verificada.

- Incremento del plan: I-03.
- Responsable: Valqui con Backend/Gateway.
- Objetivo y alcance: aplicar `LIMITE_COTIZACIONES_POR_MINUTO` por `sub` e IP y devolver `DESP_ERROR_LIMITE_COTIZACION`.
- Entradas: DT-05 y parámetro del modelo de datos.
- Dependencias: T-03 y cierre de DT-05.
- Verificación: prueba que supera el límite por el mismo `sub` e IP y recibe `429`.
- Condición de cierre: CA-05 cubierto; el límite se aplica también a la consulta sin líneas.
- Evidencia: pendiente; completar enlace a EV-03.
- Bloqueo, si existe: definición del mecanismo del límite.

### T-06. Verificar el consumo de los canales

- [ ] Implementada y verificada.

- Incremento del plan: I-03.
- Responsable: Valqui con los responsables de Marketplace y Chatbot.
- Objetivo y alcance: comprobar que los canales consumen la operación sin `lineas`, no inyectan peso/volumen y no esperan costo (DT-04).
- Entradas: contrato externo §5.1 y §10.1.
- Dependencias: T-04 y cierre de DT-04.
- Verificación: recorrido de extremo a extremo por Gateway con un canal simulado.
- Condición de cierre: consumo conforme al contrato; ventas y postventa no invoca la operación.
- Evidencia: pendiente; completar enlace a EV-04.
- Bloqueo, si existe: contrato de consumo pendiente.

### T-07. Verificar y entregar la especificación

- [ ] Implementada y verificada.

- Incremento del plan: cierre.
- Responsable: Valqui con coordinación de Gerardo.
- Objetivo y alcance: ejecutar las comprobaciones de todos los criterios, completar [evidence.md](./evidence.md) y actualizar trazabilidad e índice.
- Entradas: T-01 a T-06 y el resto de la carpeta.
- Dependencias: T-03 a T-06 y dependencias reales disponibles.
- Verificación: registrar commits, entorno y dependencias; revisar ausencia de datos de configuración en la respuesta.
- Condición de cierre: revisión funcional y técnica registrada; explicar cualquier dependencia pendiente.
- Evidencia: pendiente; completar EV-01 a EV-04.
- Bloqueo, si existe: criterios sin comprobar.

## 3. Cobertura de criterios

| Criterio funcional | Tareas que lo implementan | Tarea o comprobación que lo verifica | Evidencia |
|---|---|---|---|
| CA-01 | T-03 | T-03 y T-07 | EV-01, EV-04 |
| CA-02 | T-03 | T-03 y T-07 | EV-01 |
| CA-03 | T-03 | T-03 y T-07 | EV-01 |
| CA-04 | T-04 | T-04 y T-07 | EV-01, EV-04 |
| CA-05 | T-05 | T-05 y T-07 | EV-03 |

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están implementadas y verificadas.
- [ ] Los criterios tienen evidencia reproducible y las limitaciones están documentadas.
- [ ] Las simulaciones e integraciones pendientes se identifican expresamente.
- [ ] Los documentos y el índice están actualizados y la revisión está enlazada.

## 5. Referencias

1. [Especificación funcional](./spec.md), criterios CA-01 a CA-05 [cite: 1].
2. [Plan](./plan.md), incrementos I-01 a I-03 y pendientes DT-01 a DT-05 [cite: 2].
3. [Evidencia](./evidence.md) [cite: 3].
