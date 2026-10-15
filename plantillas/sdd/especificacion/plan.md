# Plan de ES-FXX-NN: [Nombre del comportamiento]

**Responsable:** [por completar].

**Estado:** Borrador; pendiente de revisión técnica.

**UI:** [Aplica / No aplica, con motivo].

## 1. Entradas y revisiones

| Documento | Referencia | Revisión o commit utilizado |
|---|---|---|
| Especificación funcional | [spec.md](./spec.md) | [por completar] |
| UI, si aplica | [Completar enlace a ui.md o indicar No aplica] | [por completar] |
| Contrato de API | [Enlace y secciones exactas] | [por completar] |
| Componentes React, si aplica | [Enlace e identificadores] | [por completar] |
| Arquitectura y datos | [Enlaces y secciones aplicables] | [por completar] |

El plan concreta la implementación de esas fuentes. Si descubre una regla o un cambio contractual pendiente, resolverlo en el documento propietario antes de implementar el incremento afectado [cite: 1, 2].

## 2. Estrategia y responsabilidades

[Explicar la solución y su recorrido desde la entrada hasta el resultado. Justificar las decisiones necesarias, con el alcance mínimo de esta especificación.]

| Capa o aplicación | Responsabilidad en el incremento | Archivos o componentes previstos |
|---|---|---|
| Frontend, si aplica | [por completar / No aplica] | [por completar] |
| API Gateway, si requiere cambio | [por completar / No aplica] | [por completar] |
| Servicio propietario | [por completar] | [por completar] |
| Otro servicio o módulo | [Interacción mediante contrato, sin compartir persistencia] | [Cliente o adaptador] |

## 3. Frontend y componentes React

[Si no aplica, indicar el motivo y omitir el resto de esta sección.]

- Componentes compartidos: [reutilizados y nuevos, enlazados a su especificación].
- Componentes propios: [responsabilidad y relación con UI-XX].
- Estado y datos: [estado local, consultas, mutaciones y actualización posterior].
- Cliente de API: [operaciones del contrato y adaptación al estado de la interfaz].
- Mock: [operaciones y escenarios cubiertos, limitaciones y paso para sustituirlo por integración real].

Implementar y verificar los componentes compartidos necesarios antes de las pantallas que los consumen.

## 4. Backend, persistencia e integraciones

- Entrada: [controlador o proceso y validación basada en el contrato].
- Caso de uso: [reglas y límites transaccionales].
- Datos: [entidades afectadas, propietario y restricciones necesarias].
- Migración: [No aplica / cambio propuesto, compatibilidad y tratamiento de datos existentes].
- Integraciones: [cliente, timeout y tratamiento de fallos según lo acordado].
- Efectos secundarios: [auditoría, eventos o almacenamiento, si aplica].
- Seguridad: [validación de identidad, autorización y acceso al recurso].
- Concurrencia e idempotencia: [reglas aplicables y estrategia; no imponer encabezados no acordados].

Referenciar el modelo y el contrato sin copiar esquemas completos. Si se necesita una migración, su implementación y verificación deben figurar en las tareas.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | [por completar] | [Contrato / componente / otro incremento] | [CA-NN / CUI-NN] |
| I-02 | [por completar] | I-01 | [por completar] |

Los incrementos pueden separar trabajo frontend con mocks y backend real; la integración final debe comprobar que ambos respetan el mismo contrato.

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | [por completar] | [por completar] | [por completar] |
| CA-02 | [por completar] | [por completar] | [por completar] |

Describir datos de prueba, permisos, fallos y efectos que deben verificarse. Registrar comandos previstos o pasos manuales reproducibles. Las pruebas y sus resultados reales se enlazarán en `evidence.md`.

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Justificación y fuente | Responsable | Bloquea qué incremento |
|---|---|---|---|---|
| DT-01 | [por completar] | [por completar] | [por completar] | [I-NN / No bloquea] |

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas del incremento están revisadas y los contratos necesarios están definidos.
- [ ] Las tareas indican dependencias, criterios cubiertos y verificación.
- [ ] No hay decisiones pendientes que bloqueen el incremento que se va a implementar.
- [ ] Al cerrar, todos los criterios del alcance tienen evidencia y la integración real pendiente está identificada o completada según el alcance acordado.

## 9. Referencias

1. [Especificación funcional](./spec.md) y [tareas](./tasks.md).
2. [Completar referencias al contrato, arquitectura, modelo de datos y componentes compartidos].
3. [Evidencia](./evidence.md).
