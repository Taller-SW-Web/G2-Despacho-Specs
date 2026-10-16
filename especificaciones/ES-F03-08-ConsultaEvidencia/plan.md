# Plan de ES-F03-08: Consulta autorizada de la evidencia

**Responsable:** Max Rojas

**Estado:** Borrador

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-03 |
| UI | [ui.md](./ui.md), UI-01 y CUI-01 a CUI-04 |
| Contrato | [Operación §3.4](../../integraciones/api-contract-operacion-reparto.md#34-autorizar-la-lectura-de-evidencia) |
| Pendientes del equipo | [pendiente.md](../../funcionalidades/pendiente.md), sección F-03 |
| Origen de la evidencia | [ES-F03-05](../ES-F03-05-EntregaExitosaEvidencia/spec.md) y [ES-F03-06](../ES-F03-06-EntregaFallida/spec.md) |

## 2. Estrategia y responsabilidades

El backend autoriza cada solicitud y concede una URL firmada de corta vigencia; el almacenamiento rechaza todo acceso sin firma válida.

| Área | Responsabilidad |
|---|---|
| Visor (web del repartidor y vistas administrativas) | Solicitud, visualización y renovación explícita |
| Backend de operación de reparto | Autorización por propiedad o rol, asociación evidencia–despacho y firma |
| Almacenamiento privado | Rechazo de accesos sin firma válida |

## 3. Frontend

- Componente de visor reutilizable en ambas aplicaciones.
- No persistir URLs; descartar la imagen al cambiar de recurso.
- Renovar solo por acción explícita del usuario.

## 4. Backend e integraciones

- Validar token y autorizar: propietario (`REPARTIDOR`) o `GESTOR_DESPACHO`.
- Validar la asociación evidencia–despacho y devolver el identificador del despacho.
- Emitir URL firmada con vigencia configurable según §3.4.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Visor con fixtures | DT-02 | CUI-01 a CUI-04 |
| I-02 | Autorización y firma en backend | DT-01, ES-F03-05 I-02 | CA-01 a CA-03 |
| I-03 | Recorrido integrado | I-01, I-02 | CA-01 a CA-03 y CUI-01 a CUI-04 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 | URL emitida y fotografía visible; renovación tras vencimiento | Almacenamiento real |
| CA-02 | Objeto inaccesible sin firma, con firma alterada o vencida | Almacenamiento real |
| CA-03 | `403` para otro repartidor y otro rol | Real |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Responsable | Bloquea |
|---|---|---|---|
| DT-01 | Mecanismo de almacenamiento y firma, y valor de la vigencia configurable (`pendiente.md`, F-03) | Max Rojas con Arquitectura | I-02 |
| DT-02 | Componentes compartidos aplicables al visor | Max Rojas con responsables de componentes | I-01 |
| DT-03 | Si el repartidor propietario puede consultar evidencias de jornadas anteriores | Max Rojas con responsable de F-03 | CA-01 |

## 8. Condiciones para cerrar

- [ ] Pendientes bloqueantes resueltos.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Operación §3.4](../../integraciones/api-contract-operacion-reparto.md#34-autorizar-la-lectura-de-evidencia).
