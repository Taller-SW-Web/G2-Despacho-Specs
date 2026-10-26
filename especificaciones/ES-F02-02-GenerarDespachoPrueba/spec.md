# ES-F02-02: Generación de despachos de prueba para simulación

**Funcionalidad padre:** [F-02 — Programación y asignación de despachos](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-09 y CA-20.

**Responsable:** Tarqui.

**Estado:** Backend implementado y verificado localmente; interfaz funcional pendiente. Ver [evidence.md](./evidence.md).

**Actor principal:** Gestor de Despacho (aplicación web) / Equipo técnico.

**Servicio propietario:** Gestión de Despachos.

**UI:** Aplica; botón secundario "Generar pedido de prueba" en cabecera del Panel de Programación y modal de configuración opcional, documentados en [ui.md](./ui.md).

Documentos SDD: [plan](./plan.md), [tareas](./tasks.md), [evidencia](./evidence.md) y [UI](./ui.md). Preparación del 16/10/2026; conservar los criterios no acredita su implementación.

## 1. Contexto y objetivo

El equipo técnico y los gestores de despacho requieren contar con carga de trabajo inmediata en la cola de asignación para realizar pruebas funcionales, verificar límites de carga de furgonetas y comprobar el flujo operativo sin depender de pedidos reales emitidos por Ventas y Postventa.

El objetivo es permitir que el Gestor de Despacho genere de forma autónoma despachos simulados con datos realistas y consistentes directamente en estado `PENDIENTE_ASIGNACION`. Estos despachos reciben la marca booleana `esSimulacion=true` para mostrar la etiqueta "Simulado" en la interfaz, tienen fecha programada igual a hoy para permitir su asignación inmediata y siguen exactamente las mismas reglas de negocio operativas que un despacho real [cite: 1].

## 2. Alcance

- Incluye: generación de pedidos simulados con valores por omisión coherentes en zonas activas de F-01; soporte de parámetros opcionales (`idZona`, `pesoKg`, `volumenM3`, `observaciones`); generación de códigos únicos (`DSP-SIM-XXXXX`, `TRK-SIM-XXXXX`); estado inicial `PENDIENTE_ASIGNACION`; `cantidadPaquetes = 1`; inclusión inmediata en la cola de pendientes; registro de auditoría con el usuario gestor autenticado.
- Fuera de alcance: emisión de eventos externos hacia Ventas y Postventa (los despachos simulados no notifican al módulo comercial); cobros o facturación; creación de zonas o repartidores ficticios.

## 3. Actor, precondiciones y resultados

### 3.1. Precondiciones

- El usuario está autenticado con JWT y posee el rol `GESTOR_DESPACHO`.
- Existen zonas de cobertura en estado `ACTIVO` en F-01.
- El panel administrativo de programación o el cliente de API está disponible.

### 3.2. Dependencias

- **Zonas y Cotizador (F-01):** provee las zonas activas para ubicar geográficamente el despacho generado.
- **Cola de pendientes (ES-F02-03):** recibe de inmediato el despacho simulado para su visualización.
- **Trazabilidad (ES-F02-08 / RT-02):** registra la creación en el historial con el usuario ejecutor.
- **Contrato de API:** [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).

### 3.3. Resultados

- Despacho creado en `PENDIENTE_ASIGNACION` con `esSimulacion = true`, fecha programada de hoy, datos físicos consistentes y códigos `DSP-SIM-XXXXX` y `TRK-SIM-XXXXX`.
- Respuesta HTTP `201 Created` con el cuerpo del despacho.
- Notificación tipo toast en el frontend y actualización reactiva de la tabla de la cola de pendientes con badge "Simulado".

## 4. Flujo principal y alternativas

1. El Gestor pulsa el botón secundario "Generar pedido de prueba" en la cabecera del panel o invoca `POST /api/v1/despachos/simulaciones`.
2. Opcionalmente puede enviar parámetros personalizados (`idZona`, `pesoKg`, `volumenM3`). De omitirse, el payload es `{}`.
3. El backend valida el JWT, el rol `GESTOR_DESPACHO` y los parámetros opcionales.
4. El sistema selecciona una zona activa de F-01 (o la indicada) y genera datos verosímiles: destinatario, dirección, peso (entre 1.0 y 25.0 kg), volumen (entre 0.005 y 0.15 m³), `cantidadPaquetes = 1` y fecha de entrega igual al día actual.
5. Genera `idPedido = "PED-SIM-" + correlativo`, `codigoRastreo = "TRK-SIM-" + correlativo` y código operativo `DSP-SIM-` correlativo.
6. Persiste la entidad con `esSimulacion=true` y registra la auditoría.
7. Devuelve `201 Created` con el detalle del despacho.
8. El frontend muestra toast de éxito y añade la fila a la tabla destacándola temporalmente.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Parámetros personalizados | Se especifica zona activa y peso/volumen positivos | Crea el despacho respetando los parámetros indicados y autogenerando el resto | CA-02 |
| Zona inexistente o inactiva | Se envía `idZona` de una zona inactiva o inexistente | Responde `422 Unprocessable Entity` con detalle de error | CA-03 |
| Peso o volumen inválidos | Se envía `pesoKg <= 0` o `volumenM3 <= 0` | Responde `400 Bad Request` indicando el campo fuera de rango | CA-03 |
| Sin autorización | Token aceptado sin rol `GESTOR_DESPACHO` o petición sin token aceptado | Responde `403 Forbidden` o `401 Unauthorized`, respectivamente, según Común §3.5 | CA-04 |

## 5. Reglas, datos e integraciones

| Regla | Descripción comprobable | Origen |
|---|---|---|
| RN-01 | Los despachos simulados tienen plena operatividad en cola: se filtran, asignan, reordenan y reasignan exactamente igual que uno real. | F-02 RF-09 |
| RN-02 | `esSimulacion` debe ser estrictamente `true` para los despachos creados por este endpoint. | F-02 RF-09, CA-20 |
| RN-03 | La fecha programada por defecto es la fecha actual del servidor (`LocalDate.now("America/Lima")`). | F-02 CA-20 |
| RN-04 | Los despachos simulados no emiten eventos webhooks externos hacia Ventas y Postventa (RT-03). | api-contract-gestion-despachos.md §3.2 |
| RN-05 | `cantidadPaquetes` se registra internamente siempre en `1` (paquete lógico del alcance inicial). | F-02 RF-09 |

| Operación o dependencia | Uso en este comportamiento | Contrato o fuente |
|---|---|---|
| `POST /api/v1/despachos/simulaciones` | Endpoint canónico de generación de prueba. | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) |
| Catálogo de Zonas (F-01) | Obtención de zonas activas para asignación aleatoria. | [api-contract-gestion-despachos.md §3.1](../../integraciones/api-contract-gestion-despachos.md#31-zonas-y-tarifas) |
| Auditoría (RT-02) | Registro de creación en `historial_estados_despacho`. | [ES-F02-08](../ES-F02-08-RegistrarTrazabilidadOperaciones/spec.md) |

## 6. Criterios de aceptación

### CA-01. Generación autónoma exitosa con valores por omisión

- **DADO** un usuario autenticado con rol `GESTOR_DESPACHO`.
- **CUANDO** envía una petición a `POST /api/v1/despachos/simulaciones` con payload vacío `{}`.
- **ENTONCES** el sistema crea un despacho en `PENDIENTE_ASIGNACION` con datos consistentes en una zona activa de F-01, fecha de entrega igual al día de hoy, `cantidadPaquetes = 1`, `esSimulacion = true`, responde `201 Created` y lo incorpora de inmediato a la cola de pendientes.

### CA-02. Generación exitosa con parámetros personalizados

- **DADO** una solicitud de simulación que especifica una zona activa válida (`"idZona": "ZONA-LIMA-CENTRO"`) y valores de carga (`"pesoKg": 12.5`, `"volumenM3": 0.045`).
- **CUANDO** el Gestor envía la petición con JWT válido.
- **ENTONCES** el sistema crea el despacho simulado respetando exactamente la zona, el peso y el volumen indicados, autogenera el resto de los campos consistentes y responde `201 Created`.

### CA-03. Rechazo por parámetros inválidos

- **DADO** una solicitud de simulación con un peso menor o igual a cero (`"pesoKg": -1.0`) o con un identificador de zona inexistente o inactivo en F-01.
- **CUANDO** la petición es procesada en el backend.
- **ENTONCES** el sistema responde `400 Bad Request` o `422 Unprocessable Entity` detallando el error y no persiste ningún despacho.

### CA-04. Acceso sin permisos requeridos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO` o sin token de autenticación.
- **CUANDO** intenta invocar el endpoint de simulaciones.
- **ENTONCES** el backend responde `403 Forbidden` si el token aceptado no autoriza el rol, o `401 Unauthorized` si no hay token aceptado, según Común §3.5; no genera despachos ni expone información interna.

## 7. Referencias

1. [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md): requisito RF-09 y criterio CA-20.
2. [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación): endpoint `POST /api/v1/despachos/simulaciones`.
3. [ui.md](./ui.md): especificación visual y de interacción en el panel.
