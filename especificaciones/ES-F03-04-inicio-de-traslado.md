# ES-F03-04: Inicio de traslado del despacho

**Funcionalidad padre:** F-03 — Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** Max Rojas  
**Estado:** Borrador  
**Actor principal:** Repartidor

## 1. Objetivo

Permitir que el repartidor declare que recogió el paquete y salió del centro de despacho, cambiando el despacho de `ASIGNADO` a `EN_CAMINO`.

La transición confirma que el paquete está físicamente en poder del repartidor y fuera del centro, y deja trazabilidad de quién la ejecutó y cuándo.

## 2. Actor y precondiciones

- Actor: repartidor en turno (estado operativo `DISPONIBLE`, `EN_RUTA` o `SATURADO`, con asignación diaria activa).
- Rol requerido: `REPARTIDOR`.
- El despacho está en `ASIGNADO`, asignado al repartidor del token y pertenece a la jornada en curso.
- El repartidor ya recogió el paquete sellado en el centro de despacho.
- Existe conexión activa.

## 3. Flujo principal

1. El repartidor pulsa "En camino" sobre el despacho.
2. El sistema recibe la solicitud con su clave de idempotencia y valida token, turno y propiedad del despacho.
3. El sistema solicita a la máquina de estados común la transición `ASIGNADO` → `EN_CAMINO`.
4. El sistema persiste, en una misma transacción, el nuevo estado, la marca temporal del servidor, el repartidor ejecutor y el registro en el historial común.
5. El sistema devuelve el resultado y la vista se actualiza sin recargarse por completo.

## 4. Reglas y validaciones

- Solo se permite desde `ASIGNADO`; cualquier otro estado de origen se rechaza con `409 Conflict` y el estado se conserva.
- Si F-02 reasignó o canceló el despacho mientras seguía en pantalla, se responde `409 Conflict`, la interfaz informa que el despacho fue actualizado y refresca la ruta sin aplicar cambios.
- La cancelación por F-02 solo es posible mientras el despacho permanece en `ASIGNADO` y físicamente en el centro.
- Repartidor fuera de turno: `409 Conflict` (ES-F03-01).
- No modifica el contador de intentos.
- Idempotencia: una segunda solicitud con la misma clave devuelve el resultado original sin duplicar la transición ni el historial.
- Sin conexión: la interfaz informa que el cambio no se registró, conserva el estado anterior y exige un reintento explícito.
- La transición responde en menos de 2 segundos en red 4G.

## 5. Entradas, salidas e integraciones

### Entradas

- JWT del repartidor.
- Código del despacho.
- Clave de idempotencia.

### Salidas

- Despacho en `EN_CAMINO` con marca temporal y ejecutor, y registro en el historial común.
- O la respuesta de rechazo correspondiente.

### Integraciones

- Máquina de estados y historial común del módulo (overview, sección 6).
- Publicación del evento a Ventas y Postventa según RT-03 del overview.
- F-02: estado de asignación y cancelación del despacho.
- Ver `integraciones/api-contract.md`.

## 6. Criterios de aceptación

### CA-01. Inicio de traslado exitoso (F-03 CA-12)

- **DADO** un despacho en `ASIGNADO`.
- **CUANDO** el repartidor recoge el paquete, sale del centro de despacho y pulsa "En camino".
- **ENTONCES** el estado cambia a `EN_CAMINO` con marca temporal del servidor y repartidor ejecutor, y la vista se actualiza sin recargarse por completo.

### CA-02. Transición no permitida (F-03 CA-13)

- **DADO** un despacho ya `ENTREGADO`.
- **CUANDO** el repartidor intenta marcarlo "En camino".
- **ENTONCES** el backend responde `409 Conflict` y conserva el estado.

### CA-03. Despacho reasignado o cancelado durante la jornada (F-03 CA-14)

- **DADO** que F-02 reasignó el despacho a otro repartidor o lo canceló por anulación del pedido mientras seguía en pantalla.
- **CUANDO** el repartidor intenta operarlo.
- **ENTONCES** el backend responde `409 Conflict`, la interfaz informa que el despacho fue actualizado y refresca la ruta sin aplicar cambios.

### CA-04. Registro en el historial (F-03 CA-31)

- **DADO** una transición a `EN_CAMINO` aceptada.
- **CUANDO** se persiste.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual, marca temporal del servidor, estado anterior y estado nuevo.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Asignación, reasignación y cancelación de despachos (F-02).
- Captura de GPS o seguimiento en tiempo real.
- Operación sin conexión.

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-04, RF-11 y Anexo A.
- `arquitectura/diagrama-estados-despacho.md`.
- `integraciones/api-contract.md`.
