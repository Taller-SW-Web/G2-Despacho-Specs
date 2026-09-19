# Especificación SPEC-F04-FORM-01: Panel Operativo de Entregas Fallidas

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-04: Entregas Fallidas y Reprogramaciones  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho  

---

## 1. Contexto

Cuando un intento de entrega fracasa en calle o una jornada concluye con paquetes no intentados, la mercancía debe regresar al centro de despacho para su custodia y resolución. El Gestor de Despacho requiere de un panel centralizado para fiscalizar qué paquetes están volviendo con los repartidores, cuáles ya ingresaron físicamente al centro y decidir si corresponde reprogramarlos o cancelarlos.

---

## 2. Propósito

Proveer una pantalla administrativa web responsive para consultar, filtrar y monitorear todos los despachos en estado `FALLIDO`, distinguiendo los pendientes de retorno de los ya recibidos en almacén, alertando sobre retornos atrasados o pedidos anulados, y habilitando los flujos de recepción física, reprogramación o devolución a origen.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Tabla paginada de despachos con estado `FALLIDO`.
- Filtros por: motivo de fallo, rango de fechas, repartidor y estado de recepción física (*"Pendiente de retorno"* vs *"Recibido en centro"*).
- Indicadores visuales y badges destacados:
  - Badge de Recepción: verde (*"Recibido en centro"*) o ámbar (*"Pendiente de retorno"*).
  - Alerta de *"Retorno atrasado"*: resaltado en rojo para despachos de choferes que ya cerraron su turno pero cuyos paquetes no figuran como recibidos.
  - Indicador de Intentos: contador sobre el máximo (ej. *"1/2"* o *"2/2 - Límite alcanzado"*).
  - Badge de *"Pedido anulado"*: alerta si el módulo comercial canceló la orden.
  - Miniatura de evidencia fotográfica con visor modal interactivo (invocando URL firmada de `SPEC-F03-PROC-02`).
- Botones de acción contextuales en cada fila:
  - *"Confirmar Recepción"* (abre `SPEC-F04-FORM-02`).
  - *"Reprogramar"* (abre `SPEC-F04-FORM-03`, deshabilitado si no fue recibido o si alcanzó el límite de intentos).
  - *"Devolver a Origen"* (abre `SPEC-F04-FORM-04`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Usuario autenticado con rol `GESTOR_DESPACHO` o `ADMIN`.
- Existencia de despachos en estado `FALLIDO` en la base de datos.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/entregas-fallidas` | Endpoint backend que retorna los despachos fallidos con sus banderas. |
| `SPEC-F03-PROC-02` | Emisión de URL firmada para visualizar la foto de evidencia. |
| `SPEC-F04-FORM-02` | Formulario de recepción física en centro. |
| `SPEC-F04-FORM-03` | Modal de reprogramación. |
| `SPEC-F04-FORM-04` | Modal de devolución a origen. |

### 4.3. Resultados
- Supervisión completa del inventario en tránsito que no fue entregado.
- Prevención de pérdidas materiales mediante el control estricto de retornos atrasados.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Despliegue del listado de incidencias
El panel DEBE mostrar las incidencias con sus indicadores visuales correspondientes.

#### CA-01. Listado con indicadores completos
- **DADO** despachos registrados en estado `FALLIDO`.
- **CUANDO** el gestor ingresa a `/entregas-fallidas`.
- **ENTONCES** la tabla renderiza: Código de rastreo, Fecha de incidencia, Motivo tipificado, Repartidor, Contador de intentos, Estado de recepción y Acciones habilitadas según corresponda.

#### CA-02. Resaltado de retorno atrasado
- **DADO** un despacho fallido asignado a un repartidor cuyo turno ya finalizó (`FUERA_DE_TURNO`) y cuyo paquete sigue marcado como "Pendiente de retorno".
- **CUANDO** se despliega en el panel.
- **ENTONCES** la fila se resalta con borde rojo y badge *"Retorno atrasado"*, indicando el nombre del repartidor en custodia del bulto.

#### CA-03. Deshabilitación de acciones antes de recepción
- **DADO** un despacho marcado como "Pendiente de retorno".
- **CUANDO** el gestor revisa las opciones de la fila.
- **ENTONCES** los botones *"Reprogramar"* y *"Devolver a Origen"* se muestran deshabilitados con tooltip *"Primero debe confirmarse la recepción física del paquete en el centro"*.

---

## 6. Frontend

### 6.1. Componentes
- **`FailedDeliveriesPage`**: Vista general con métricas rápidas (total fallidos, pendientes de recepción, atrasados).
- **`FailedDeliveriesTable`**: Tabla responsive con sorting y badges temáticos de Tailwind.
- **`EvidenceViewerModal`**: Diálogo modal para ampliar la fotografía de evidencia y leer los comentarios del chofer.
- **`FailedFiltersBar`**: Filtros por estado de recepción, motivo, fecha y chofer.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `GET /api/v1/entregas-fallidas`
- **Query Params:** `pagina`, `limite`, `estadoRecepcion` (`PENDIENTE` / `RECIBIDO`), `motivo`, `repartidor`
- **Respuesta (`200 OK`):**
```json
{
  "totalElementos": 12,
  "paginaActual": 1,
  "despachos": [
    {
      "idDespacho": "DSP-100234",
      "codigoRastreo": "TRK-78901",
      "fechaIncidencia": "2026-09-19T17:40:00Z",
      "motivo": "CLIENTE_AUSENTE",
      "motivoTexto": "Cliente ausente",
      "comentariosRepartidor": "Timbre no funciona",
      "tieneEvidencia": true,
      "idRepartidor": "REP-0012",
      "nombreRepartidor": "Juan Pérez",
      "intentoActual": 1,
      "maximoIntentos": 2,
      "recibidoEnCentro": false,
      "retornoAtrasado": true,
      "pedidoAnulado": false
    }
  ]
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** Carga inicial de la grilla en menos de 250 ms para lotes de 50 registros.
- **Seguridad:** Acceso restringido exclusivamente a usuarios con rol `GESTOR_DESPACHO` o `ADMIN`.
- **Feedback Operativo:** Alertas visuales con colores accesibles (WCAG AAA) para retornos críticos.

---

## 9. Fuera de alcance

- Registro manual del reporte de fallo desde el centro (el reporte original ocurre en campo mediante F-03).
- Reclamaciones financieras o reembolsos al cliente (corresponden a Ventas y Postventa).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI Grid Test | RTL / Vitest | Tabla renderiza columnas, badges y paginador. |
| CA-02 | Visual Alert Test | Storybook / Jest | Paquete con retorno atrasado muestra badge rojo. |
| CA-03 | Button Disabled Test | Vitest | Botón "Reprogramar" deshabilitado si `recibidoEnCentro === false`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El panel clasifique inequívocamente paquetes pendientes de retorno de los recibidos.
2. Alerte sobre choferes con entregas atrasadas.
3. Condicione las decisiones de reprogramación o cierre a la previa confirmación de recepción.
