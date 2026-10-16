# Plan de ES-F03-01: Acceso y habilitación operativa del repartidor

**Responsable:** Max Rojas

**Estado:** Borrador

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas

| Documento | Referencia |
|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-04 |
| UI | [ui.md](./ui.md), UI-01, UI-02 y CUI-01 a CUI-05 |
| Contrato | [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md) |
| Funcionalidad | [F-03](../../funcionalidades/F-03-AppMovilRepartidor.md), RF-01 y sección 8 |

## 2. Estrategia y responsabilidades

El frontend obtiene el contexto del repartidor y adapta la vista; el backend valida el JWT, resuelve el repartidor en F-05 y decide la habilitación. Ninguna decisión de permiso depende del cliente.

| Área | Responsabilidad |
|---|---|
| Web del repartidor | Pantalla de acceso, consulta del contexto y modo operativo o de solo lectura |
| Backend de operación de reparto | Validación del JWT, resolución en F-05, contexto y rechazo de transiciones |
| Seguridad y Usuarios | Emisión del JWT (externo) |
| F-05 Monitoreo de Flota | Vínculo, estado operativo y asignación diaria (externo) |

## 3. Frontend

- Pantalla de acceso con mensajes por motivo de rechazo.
- Guardia de ruta: sin contexto válido no se muestra «Mi Ruta».
- El modo operativo o de solo lectura se deriva del indicador de habilitación del backend, no de cálculos locales.
- Ante `409`, cambiar a solo lectura sin recargar.
- Antes del contrato cerrado se usan fixtures por estado (en turno, fuera de turno, `401`, `403`).

## 4. Backend e integraciones

- Validar vigencia y rol `REPARTIDOR` en cada solicitud.
- Resolver el repartidor a partir del identificador de usuario del token; ignorar identificadores del cliente.
- Consultar en F-05 estado operativo y asignación diaria; calcular la habilitación según RN-04.
- Rechazar transiciones con `409` cuando el repartidor no está en turno.
- Solo lectura sobre F-05; no publica eventos.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Acceso y modos visibles con fixtures | Base frontend | CUI-01 a CUI-05 |
| I-02 | Autorización y contexto en backend probados | DT-01, DT-02, DT-03 | CA-01 a CA-04 |
| I-03 | Recorrido real integrado | I-01 e I-02 | CA-01 a CA-04 y CUI-01 a CUI-05 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Dependencia |
|---|---|---|
| CA-01 | Repartidor en turno obtiene contexto habilitado | F-05 real o doble identificado |
| CA-02 | Sin token y token vencido devuelven `401` sin datos | Real |
| CA-03 | Otro rol y usuario sin vínculo devuelven `403` | Real o doble de F-05 |
| CA-04 | `FUERA_DE_TURNO` consulta y recibe `409` al operar | F-05 real o doble identificado |

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Responsable | Bloquea |
|---|---|---|---|
| DT-01 | Mecanismo de autenticación y validación del JWT con Seguridad y Usuarios (Anexo C n.º 1 de F-03) | Max Rojas con Arquitectura | I-02, I-03 |
| DT-02 | Ruta, DTO del contexto y códigos de error para distinguir rol incorrecto y usuario no vinculado | Max Rojas con Backend | I-02, I-03 |
| DT-03 | Forma de consulta a F-05 (vínculo, estado y asignación) y comportamiento si F-05 no responde | Max Rojas con responsable de F-05 | I-02 |
| DT-04 | Componentes compartidos aplicables a la web del repartidor | Max Rojas con responsables de componentes | I-01 |
| DT-05 | Tratamiento de un repartidor en `DISPONIBLE`, `EN_RUTA` o `SATURADO` sin asignación diaria activa | Max Rojas con responsable de F-05 | CA-01, CA-04 |

## 8. Condiciones para cerrar

- [ ] Pendientes bloqueantes resueltos.
- [ ] Tareas con comprobación concreta para cada criterio.
- [ ] Evidencia registrada distinguiendo fixtures, dobles y servicios reales.

## 9. Referencias

1. [spec.md](./spec.md), [ui.md](./ui.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
2. [Contrato de operación de reparto](../../integraciones/api-contract-operacion-reparto.md).
