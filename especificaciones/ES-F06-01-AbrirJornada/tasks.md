# Tareas de ES-F06-01: Abrir una jornada operativa

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
- Criterios: CA-01, CA-02, CA-03, CA-04, CA-05, CA-06; CUI-01 a CUI-06.
- Verificación: contrastar el resultado observable del criterio y sus efectos; guardar reporte de ejecución y commit en evidence.md.
- Cierre: resultado reproducible sin atribuir aceptación real a un doble.
- Evidencia: [EV-01](./evidence.md#ev-01-verificación-del-incremento), verificación local registrada; límites pendientes.


### T-02. Componer interfaz y componentes

- [x] Implementada y verificada localmente.
- Incremento: I-02; área: Frontend; depende de T-01.
- Entradas: spec.md, contrato canónico y plan.md.
- Criterios: CA-01, CA-02, CA-03, CA-04, CA-05, CA-06; CUI-01 a CUI-06.
- Verificación: contrastar el resultado observable del criterio y sus efectos; guardar reporte de ejecución y commit en evidence.md.
- Cierre: resultado reproducible sin atribuir aceptación real a un doble.
- Evidencia: [EV-01](./evidence.md#ev-01-verificación-del-incremento), verificación local registrada; límites pendientes.


### T-03. Implementar persistencia y autorización

- [x] Implementada y verificada localmente.
- Incremento: I-03; área: Backend; depende de T-01.
- Entradas: spec.md, contrato canónico y plan.md.
- Criterios: CA-01, CA-02, CA-03, CA-04, CA-05, CA-06; CUI-01 a CUI-06.
- Verificación: contrastar el resultado observable del criterio y sus efectos; guardar reporte de ejecución y commit en evidence.md.
- Cierre: resultado reproducible sin atribuir aceptación real a un doble.
- Evidencia: [EV-01](./evidence.md#ev-01-verificación-del-incremento), verificación local registrada; límites pendientes.


### T-04. Verificar recorrido y registrar evidencia

- [ ] Implementada y verificada.
- Incremento: I-04; área: Calidad; depende de T-02 y T-03.
- Entradas: spec.md, contrato canónico y plan.md.
- Criterios: CA-01, CA-02, CA-03, CA-04, CA-05, CA-06; CUI-01 a CUI-06.
- Verificación: contrastar el resultado observable del criterio y sus efectos; guardar reporte de ejecución y commit en evidence.md.
- Cierre: resultado reproducible sin atribuir aceptación real a un doble.
- Evidencia: [EV-01](./evidence.md#ev-01-verificación-del-incremento), verificación local registrada; límites pendientes.

## 3. Cobertura de criterios

| Criterio | Implementación | Verificación | Evidencia |
|---|---|---|---|
| CA-01 | T-01 a T-03 | T-04 | Ver evidence.md |
| CA-02 | T-01 a T-03 | T-04 | Ver evidence.md |
| CA-03 | T-01 a T-03 | T-04 | Ver evidence.md |
| CA-04 | T-01 a T-03 | T-04 | Ver evidence.md |
| CA-05 | T-01 a T-03 | T-04 | Ver evidence.md |
| CA-06 | T-01 a T-03 | T-04 | Ver evidence.md |
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

## 6. Incremento de integración G7 del 03/11/2026

| ID | Resultado | Dependencia | Estado |
|---|---|---|---|
| T-G7-01 | Conciliar contrato y precondiciones con A5/A6 | Fuentes suministradas G7 | Verificado documentalmente; sin aceptación externa |
| T-G7-02 | Ajustar perfil JWT de Operación y mensajes de vinculación/apertura | T-G7-01 | Implementado y verificado localmente; ver EV-G7 |
| T-G7-03 | Registrar comprobaciones criptográficas y regresión F-05/F-06 | T-G7-02 | Verificado localmente: 75 pruebas frontend, 34 backend, typecheck y build; ver EV-G7 |
| T-G7-04 | Acreditar cuentas, concesiones y flujo integrado | Seguridad y responsables de sesión | Pendiente externo |
| T-G7-05 | Acordar y consumir eventos/reconciliación | Broker, permisos y revisión G7 | Pendiente; no implementado |

Estas tareas no sustituyen la evidencia histórica ni completan la aceptación conjunta de los criterios.
