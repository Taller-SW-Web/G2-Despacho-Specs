# Especificación SPEC-F03-FORM-04: Vista de Cierre de Jornada y Resumen Diario

**Tipo:** Formulario / Vista (Mobile-First)  
**Macro-funcionalidad:** F-03: Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Repartidor  

---

## 1. Contexto

Al finalizar el turno de trabajo en calle, el repartidor debe concluir formalmente su jornada operativa. La regla de negocio del sistema exige que ningún despacho quede en estado inconcluso (`ASIGNADO` o `EN_CAMINO`). Por ello, el cierre de jornada debe advertir y liquidar de forma automática los paquetes que no pudieron ser intentados, permitiendo al operador entregar cuentas claras en el centro de despacho.

---

## 2. Propósito

Proveer una interfaz táctil que permita al repartidor solicitar el cierre de su jornada, advertir explícitamente sobre el tratamiento de paquetes no intentados, transicionar al repartidor a estado `FUERA_DE_TURNO` y presentar una pantalla con el resumen consolidado de la labor del día y el listado de paquetes que debe entregar físicamente en el centro.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Botón *"Finalizar Jornada / Cerrar Turno"* en la cabecera o menú inferior de la web del repartidor.
- Detección en cliente de paquetes inconclusos (`ASIGNADO` o `EN_CAMINO`).
- Diálogo de confirmación diferenciado:
  - Sin pendientes: confirmación directa del cierre.
  - Con pendientes: diálogo modal de advertencia indicando la cantidad exacta de paquetes que pasarán a `FALLIDO` con motivo `NO_INTENTADO` (sin penalizar intentos del cliente) y que deben retornarse al centro.
- Invocación del endpoint `POST /api/v1/repartidor/cerrar-jornada`.
- Transición del estado operativo del repartidor a `FUERA_DE_TURNO` en F-05.
- Pantalla de Resumen Diario con métricas: Total asignados, Entregados exitosos, Fallidos con intento real, No intentados y lista de paquetes a devolver en almacén.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Repartidor autenticado con sesión activa y turno vigente en la jornada.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `POST /api/v1/repartidor/cerrar-jornada` | Endpoint que liquida pendientes y solicita el cierre de turno a F-05 (`SPEC-F03-PROC-01`). |
| `GET /api/v1/repartidor/resumen-jornada` | Endpoint que consolida las estadísticas de la jornada. |
| F-05 (Flota y Capacidad) | Pasa al repartidor a `FUERA_DE_TURNO` y libera el vehículo asignado. |

### 4.3. Resultados
- Ningún despacho queda en estado `ASIGNADO` ni `EN_CAMINO`.
- El repartidor queda bloqueado para realizar nuevas transiciones en calle.
- Se presenta la hoja de liquidación visual para el control de entrega física de paquetes en almacén.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Advertencia y liquidación de pendientes
El sistema DEBE advertir claramente antes de cerrar una jornada con despachos no entregados.

#### CA-01. Cierre con despachos pendientes
- **DADO** un repartidor con 2 despachos en `ASIGNADO` al momento de querer cerrar turno.
- **CUANDO** pulsa *"Cerrar Jornada"*.
- **ENTONCES** un modal de advertencia alerta: *"Tienes 2 paquetes pendientes. Se marcarán como 'No intentado' y deberás entregarlos en el centro de despacho"*. Al pulsar *"Confirmar Cierre"*, el backend responde `200 OK` y los despachos pasan a `FALLIDO` con motivo `NO_INTENTADO` sin consumir intentos.

#### CA-02. Cierre limpio sin pendientes
- **DADO** que todos los despachos fueron entregados o reportados con fallo en calle.
- **CUANDO** el repartidor pulsa *"Cerrar Jornada"*.
- **ENTONCES** la confirmación es directa, el turno se cierra de inmediato y se despliega la pantalla de resumen.

### RF-02. Despliegue del resumen de jornada
El sistema DEBE mostrar el balance final de la jornada del repartidor.

#### CA-03. Consolidado estadístico correcto
- **DADO** un cierre exitoso de turno.
- **CUANDO** carga la vista de resumen.
- **ENTONCES** se presentan 4 tarjetas: Total Asignados (8), Entregados (5), Fallidos en visita (2), No intentados (1), más la lista con los 3 paquetes que debe retornar físicamente.

---

## 6. Frontend

### 6.1. Componentes
- **`ShiftCloseWarningModal`**: Modal de alta visibilidad con icono amarillo de alerta y lista de códigos `TRK-` afectados.
- **`DailySummaryPage`**: Vista de resumen con diseño tipo tarjeta de embarque / recibo.
- **`MetricsCardsGrid`**: 4 cuadrantes con números grandes y colores temáticos (verde, ámbar, rojo, gris).
- **`PhysicalReturnChecklist`**: Lista con casillas de verificación para que el chofer coteje los bultos físicos devueltos en la ventanilla del centro de despacho.

---

## 7. Backend (Contratos consumidos)

### 7.1. Cerrar Jornada
- **Ruta:** `POST /api/v1/repartidor/cerrar-jornada`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Idempotency-Key: <UUID>`
- **Respuesta (`200 OK`):**
```json
{
  "idRepartidor": "REP-0012",
  "estadoOperativo": "FUERA_DE_TURNO",
  "despachosNoIntentadosCerrados": 2,
  "fechaCierre": "2026-09-19T18:30:00Z"
}
```

### 7.2. Resumen Diario
- **Ruta:** `GET /api/v1/repartidor/resumen-jornada`
- **Respuesta (`200 OK`):**
```json
{
  "fecha": "2026-09-19",
  "totalAsignados": 10,
  "entregados": 7,
  "fallidosConIntento": 1,
  "noIntentados": 2,
  "paquetesRetornoFisico": [
    { "idDespacho": "DSP-100234", "codigoRastreo": "TRK-78901", "motivo": "CLIENTE_AUSENTE" },
    { "idDespacho": "DSP-100235", "codigoRastreo": "TRK-78902", "motivo": "NO_INTENTADO" },
    { "idDespacho": "DSP-100236", "codigoRastreo": "TRK-78903", "motivo": "NO_INTENTADO" }
  ]
}
```

---

## 8. Requisitos no funcionales

- **Seguridad:** Una vez cerrada la jornada, el token del repartidor queda inhabilitado para ejecutar nuevas transiciones en F-03.
- **Auditoría:** La operación de cierre registra la hora exacta del servidor en UTC y el actor ejecutor.

---

## 9. Fuera de alcance

- Registro de recepción física de los paquetes en almacén (responsabilidad del Gestor en `SPEC-F04-FORM-02`).
- Liquidación de viáticos o combustible del repartidor.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI Warning Test | RTL / Vitest | Modal lista paquetes pendientes y exige confirmación explícita. |
| CA-02 | Clean Close Test | MockMvc | Cierre sin pendientes pasa a `FUERA_DE_TURNO` sin generar fallos. |
| CA-03 | Summary Display | Cypress | Tarjetas de resumen coinciden exactamente con la respuesta de la API. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El cierre de jornada garantice que no queden despachos en `ASIGNADO` ni `EN_CAMINO`.
2. Los paquetes no intentados no incrementen el contador de intentos del despacho.
3. El repartidor visualice su hoja de liquidación y pase a estado `FUERA_DE_TURNO`.
