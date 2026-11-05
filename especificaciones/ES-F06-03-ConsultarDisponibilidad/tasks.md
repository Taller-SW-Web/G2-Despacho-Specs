# Tareas de ES-F06-03: Consultar repartidores disponibles

**Responsable:** Kevin Rhamses Bohorquez. **Estado:** Implementación local verificada; integración desplegada y aceptación pendientes.

**Plan de origen:** [plan.md](./plan.md), preparado en esta revisión.

## 1. Orden y dependencias

| ID | Resultado | Incremento | Área | Depende de | Estado |
|---|---|---|---|---|---|
| T-01 | Definir contrato y trazabilidad | I-01 | Documentación | Ninguna | Completada localmente |
| T-02 | Componer interfaz y componentes | I-02 | Frontend | T-01 | Completada localmente |
| T-03 | Implementar persistencia y autorización | I-03 | Backend | T-01 | Completada localmente |
| T-04 | Verificar recorrido y registrar evidencia | I-04 | Calidad | T-02 y T-03 | Parcial: automatización aprobada; aceptación pendiente |

## 2. Detalle de tareas

### T-01. Definir contrato y trazabilidad

- [x] Implementada y verificada localmente.
- Incremento: I-01; área: Documentación; depende de Ninguna.
- Entradas: spec.md, contrato canónico y plan.md.
- Criterios: CA-01, CA-02, CA-03; CUI-01 a CUI-06.
- Verificación: contrastar el resultado observable del criterio y sus efectos; guardar reporte de ejecución y commit en evidence.md.
- Cierre: resultado reproducible sin atribuir aceptación real a un doble.
- Evidencia: [EV-01](./evidence.md#ev-01-verificación-del-incremento), verificación local registrada; límites pendientes.


### T-02. Componer interfaz y componentes

- [x] Implementada y verificada localmente.
- Incremento: I-02; área: Frontend; depende de T-01.
- Entradas: spec.md, contrato canónico y plan.md.
- Criterios: CA-01, CA-02, CA-03; CUI-01 a CUI-06.
- Verificación: contrastar el resultado observable del criterio y sus efectos; guardar reporte de ejecución y commit en evidence.md.
- Cierre: resultado reproducible sin atribuir aceptación real a un doble.
- Evidencia: [EV-01](./evidence.md#ev-01-verificación-del-incremento), verificación local registrada; límites pendientes.


### T-03. Implementar persistencia y autorización

- [x] Implementada y verificada localmente.
- Incremento: I-03; área: Backend; depende de T-01.
- Entradas: spec.md, contrato canónico y plan.md.
- Criterios: CA-01, CA-02, CA-03; CUI-01 a CUI-06.
- Verificación: contrastar el resultado observable del criterio y sus efectos; guardar reporte de ejecución y commit en evidence.md.
- Cierre: resultado reproducible sin atribuir aceptación real a un doble.
- Evidencia: [EV-01](./evidence.md#ev-01-verificación-del-incremento), verificación local registrada; límites pendientes.


### T-04. Verificar recorrido y registrar evidencia

- [ ] Implementada y verificada.
- Incremento: I-04; área: Calidad; depende de T-02 y T-03.
- Entradas: spec.md, contrato canónico y plan.md.
- Criterios: CA-01, CA-02, CA-03; CUI-01 a CUI-06.
- Verificación: contrastar el resultado observable del criterio y sus efectos; guardar reporte de ejecución y commit en evidence.md.
- Cierre: resultado reproducible sin atribuir aceptación real a un doble.
- Evidencia: [EV-01](./evidence.md#ev-01-verificación-del-incremento), verificación local registrada; límites pendientes.

## 3. Cobertura de criterios

| Criterio | Implementación | Verificación | Evidencia |
|---|---|---|---|
| CA-01 | T-01 a T-03 | T-04 | Ver evidence.md |
| CA-02 | T-01 a T-03 | T-04 | Ver evidence.md |
| CA-03 | T-01 a T-03 | T-04 | Ver evidence.md |
| CUI-01 | T-01 a T-03 | T-04 | Ver evidence.md |
| CUI-02 | T-01 a T-03 | T-04 | Ver evidence.md |
| CUI-03 | T-01 a T-03 | T-04 | Ver evidence.md |
| CUI-04 | T-01 a T-03 | T-04 | Ver evidence.md |
| CUI-05 | T-01 a T-03 | T-04 | Ver evidence.md |
| CUI-06 | T-01 a T-03 | T-04 | Ver evidence.md |

## 4. Cierre de la especificación

- [ ] Tareas y criterios verificados.
- [x] Integraciones, limitaciones y revisión humana pendiente registradas.

## 5. Referencias

1. [Especificación](./spec.md) [cite: 1].
2. [Plan](./plan.md) [cite: 2].
3. [Evidencia](./evidence.md) [cite: 3].


## Revisión automatizada del 26/10/2026

Ver [EV-02](./evidence.md#ev-02-revision-f05-f06) y el [reporte común](../ES-F06-01-AbrirJornada/evidencia/validacion.md#revision-f05-f06-2026-10-26). Las suites de código y navegador aprobaron en CI; esto no completa la revisión humana ni la integración con Seguridad real. No se aplicaron migraciones sobre bases compartidas.
