# ES-F03-03: Consulta del detalle de un despacho

**Funcionalidad padre:** F-03 — Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** Max Rojas  
**Estado:** Borrador  
**Actor principal:** Repartidor

## 1. Objetivo

Mostrar al repartidor la información necesaria para ejecutar la entrega de un despacho concreto y contactar al destinatario, protegiendo los datos personales frente a usuarios no autorizados.

## 2. Actor y precondiciones

- Actor: repartidor autenticado (ES-F03-01).
- Rol requerido: `REPARTIDOR`.
- El despacho existe, está asignado al repartidor del token y pertenece a la jornada en curso.

## 3. Flujo principal

1. El repartidor selecciona un despacho en "Mi Ruta".
2. El sistema verifica que el despacho exista y pertenezca al repartidor del token.
3. El sistema recupera los datos de entrega del despacho.
4. El sistema muestra el detalle con la opción de llamada directa al destinatario.

## 4. Reglas y validaciones

- El detalle muestra: dirección, referencia, destinatario, teléfono con llamada directa, intento actual sobre el máximo configurado, fecha programada y estado.
- Teléfono y dirección se muestran solo al repartidor propietario y solo mientras el despacho está en `ASIGNADO` o `EN_CAMINO`.
- No se ofrece exportación ni copia masiva de datos del destinatario.
- Despacho asignado a otro repartidor: `403 Forbidden`.
- Código que no corresponde a ningún despacho: `404 Not Found`, sin datos parciales.

## 5. Entradas, salidas e integraciones

### Entradas

- JWT del repartidor.
- Código del despacho.

### Salidas

- Detalle del despacho o la respuesta de error correspondiente.

### Integraciones

- F-02 Programación y Asignación: destinatario, dirección, teléfono y fecha programada.
- Ventas y Postventa: origen del teléfono y la referencia de dirección (acuerdo pendiente, Anexo C n.º 2 de F-03).
- Ver `integraciones/api-contract.md`.

## 6. Criterios de aceptación

### CA-01. Detalle exitoso (F-03 CA-09)

- **DADO** un despacho asignado al repartidor en `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** abre su detalle.
- **ENTONCES** ve dirección, referencia, destinatario, teléfono con llamada directa, intento actual sobre el máximo configurado, fecha programada y estado.

### CA-02. Despacho de otro repartidor (F-03 CA-10)

- **DADO** un despacho asignado a otro repartidor.
- **CUANDO** se solicita su detalle.
- **ENTONCES** el backend responde `403 Forbidden`.

### CA-03. Despacho inexistente (F-03 CA-11)

- **DADO** un código que no corresponde a ningún despacho.
- **CUANDO** se solicita su detalle.
- **ENTONCES** el backend responde `404 Not Found` sin datos parciales.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Geolocalización y navegación propia.
- Edición de los datos del destinatario.
- Notificación al cliente final (canales y Ventas y Postventa).

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-03 y sección 8.
- `integraciones/api-contract.md`.
- Wireframe del detalle del despacho.
