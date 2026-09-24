# Macroproceso de Despacho y Entrega

## 1. Alcance del macroproceso

La cotización ocurre antes de la creación del despacho y sirve como antecedente comercial. El macroproceso operativo comienza cuando Ventas y Postventa envía un pedido pagado, preparado y listo para entrega. Termina en uno de tres resultados finales:

- `ENTREGADO` al destinatario.
- `CANCELADO` antes de comenzar el traslado.
- `DEVUELTO_A_ORIGEN` en el centro de despacho.

## 2. Vista general

```mermaid
flowchart TB
    classDef externo fill:#F8FAFC,color:#0F172A,stroke:#64748B,stroke-width:2px
    classDef proceso fill:#DBEAFE,color:#172554,stroke:#2563EB,stroke-width:2px
    classDef decision fill:#FEF3C7,color:#713F12,stroke:#D97706,stroke-width:2px
    classDef final fill:#DCFCE7,color:#14532D,stroke:#16A34A,stroke-width:2px
    classDef rechazo fill:#FEE2E2,color:#7F1D1D,stroke:#DC2626,stroke-width:2px
    classDef antecedente fill:#F3E8FF,color:#581C87,stroke:#9333EA,stroke-width:2px,stroke-dasharray:6 4

    subgraph PREVIO["Antecedente comercial opcional"]
        CANALES["Marketplace o Chatbot<br/>solicitan cotización"]:::externo
        COT["Despacho informa cobertura y<br/>cotización base o calculada"]:::antecedente
        VENPRECIO["Ventas decide promociones y<br/>precio cobrado al cliente"]:::externo
        CANALES --> COT --> VENPRECIO
    end

    VEN["Ventas y Postventa<br/>Pedido pagado y preparado"]:::externo
    REC["1. Recibir y validar<br/>solicitud de despacho"]:::proceso
    PROD["Productos y Ofertas<br/>Peso y dimensiones por SKU"]:::externo
    VAL{"Cobertura y datos<br/>físicos válidos?"}:::decision
    RECH["Rechazar solicitud<br/>sin crear despacho"]:::rechazo
    CREAR["2. Crear despacho<br/>PENDIENTE_ASIGNACION"]:::proceso
    ASIG["3. Programar y asignar<br/>repartidor, jornada y capacidad"]:::proceso
    CANCELA{"Ventas anula antes<br/>del traslado?"}:::decision
    CANC["CANCELADO"]:::final
    RUTA["4. Ejecutar reparto<br/>ASIGNADO → EN_CAMINO"]:::proceso
    RESULTADO{"Entrega concretada?"}:::decision
    ENTREGA["ENTREGADO<br/>con evidencia"]:::final
    FALLO["5. Registrar FALLIDO<br/>y retornar al centro"]:::proceso
    RECEP["6. Confirmar recepción<br/>y liberar capacidad"]:::proceso
    REINTENTO{"Reprogramación<br/>permitida?"}:::decision
    REPROG["Fijar nueva fecha y volver a<br/>PENDIENTE_ASIGNACION"]:::proceso
    DEV["DEVUELTO_A_ORIGEN"]:::final
    EVENTOS["7. Comunicar estados a Ventas<br/>mediante webhook"]:::proceso

    VEN --> REC
    REC --> PROD
    PROD --> VAL
    VAL -->|No| RECH
    VAL -->|Sí| CREAR
    CREAR --> ASIG
    ASIG --> CANCELA
    CANCELA -->|Sí| CANC
    CANCELA -->|No| RUTA
    RUTA --> RESULTADO
    RESULTADO -->|Sí| ENTREGA
    RESULTADO -->|No o no intentado| FALLO
    FALLO --> RECEP
    RECEP --> REINTENTO
    REINTENTO -->|Sí| REPROG
    REPROG --> ASIG
    REINTENTO -->|No: máximo, anulación o cierre| DEV

    CANC --> EVENTOS
    ENTREGA --> EVENTOS
    DEV --> EVENTOS
```

Para mantener la vista legible, el diagrama conecta el bloque de comunicación con los resultados finales. Sin embargo, el historial y el seguimiento se actualizan en cada transición, y cada cambio de estado confirmado genera también su notificación hacia Ventas y Postventa.

## 3. Procesos que componen el macroproceso

| Proceso | Responsable principal | Entrada | Resultado |
|---|---|---|---|
| 1. Recibir y validar | F-02 con apoyo de F-01 y Productos | Pedido, destinatario, destino y líneas | Solicitud rechazada o datos válidos para crear el despacho. |
| 2. Crear despacho | F-02 | Solicitud válida | Despacho `PENDIENTE_ASIGNACION`, zona, peso, volumen y fecha programada. |
| 3. Programar y asignar | F-02 con capacidad de F-05 | Despacho pendiente y jornada vigente | Despacho `ASIGNADO`, reserva y secuencia de ruta. |
| 4. Ejecutar reparto | F-03 | Ruta del repartidor | Despacho `EN_CAMINO` y luego resultado de la visita. |
| 5. Gestionar resultado | F-03 | Entrega o incidencia | `ENTREGADO` o `FALLIDO` con evidencia y motivo cuando corresponda. |
| 6. Resolver fallido | F-04 con liberación en F-05 | Paquete retornado al centro | Reprogramación o `DEVUELTO_A_ORIGEN`. |
| 7. Comunicar estados | Componente transversal de Gestión | Transición confirmada | Webhook idempotente hacia Ventas y seguimiento actualizado. |

## 4. Reglas de lectura para otros equipos

- Marketplace y Chatbot pueden solicitar una cotización base sin productos o una cotización calculada con productos. Ninguna de las dos crea el despacho.
- Despacho comunica un costo logístico; Ventas decide cuánto se cobra finalmente al cliente.
- Ventas no necesita volver a cotizar para crear el despacho. Envía las líneas y Despacho consulta nuevamente los datos físicos vigentes.
- Una cancelación solo termina en `CANCELADO` mientras el despacho está `PENDIENTE_ASIGNACION` o `ASIGNADO`.
- Si Ventas solicita cancelar cuando el despacho está `EN_CAMINO`, Despacho responde `409 Conflict`; el flujo continúa hasta entrega o fallo.
- Todo `FALLIDO` debe regresar al centro antes de reprogramarse o cerrarse.
- Un reintento regresa a asignación y recorre nuevamente el proceso de reparto.
- Los estados finales se notifican a Ventas, que continúa cualquier tratamiento comercial, reembolso o comunicación con el cliente.

## 5. Referencias

- [Glosario de dominio](./glosario-dominio.md).
- [Diagrama de estados del despacho](./diagrama-estados-despacho.md).
- [Contrato de comunicación](../integraciones/api-contract.md).
- [Visión general](../overview.md).
