# ES-F03-08: Consulta autorizada de la evidencia

**Funcionalidad padre:** F-03 — Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** Max Rojas  
**Estado:** Borrador  
**Actor principal:** Repartidor propietario o Gestor de Despacho

## 1. Objetivo

Permitir visualizar la fotografía de evidencia de un despacho solo a usuarios autorizados, sin exponerla de forma pública, para que el repartidor y F-04 puedan revisarla.

## 2. Actor y precondiciones

- Actor: repartidor propietario del despacho o usuario con rol `GESTOR_DESPACHO`.
- El despacho tiene evidencia registrada.
- El usuario cuenta con autorización vigente.

## 3. Flujo principal

1. El usuario solicita ver la evidencia de un despacho.
2. El sistema valida el token y verifica que sea el repartidor propietario o tenga rol `GESTOR_DESPACHO`.
3. El sistema concede el acceso mediante el mecanismo autorizado que defina el equipo.
4. El usuario visualiza la fotografía.

## 4. Reglas y validaciones

- La evidencia nunca se expone de forma pública.
- Acceso directo, o con autorización ausente o vencida: denegado.
- Usuario que no es el repartidor propietario ni tiene rol `GESTOR_DESPACHO`: `403 Forbidden`.
- El mecanismo de acceso autorizado está pendiente de decisión del equipo (`pendiente.md`, sección F-03).

## 5. Entradas, salidas e integraciones

### Entradas

- JWT del usuario.
- Código del despacho.

### Salidas

- Acceso a la fotografía o respuesta de denegación.

### Integraciones

- Servicio de evidencia (por definir).
- F-04 Entregas Fallidas: consulta la evidencia de los despachos `FALLIDO`.
- Ver `integraciones/api-contract.md`.

## 6. Criterios de aceptación

### CA-01. Consulta autorizada de evidencia (F-03 CA-27)

- **DADO** un despacho con evidencia.
- **CUANDO** el repartidor propietario o un usuario con rol `GESTOR_DESPACHO` solicita verla.
- **ENTONCES** el sistema permite visualizar la evidencia mediante el mecanismo de acceso autorizado que defina el equipo.

### CA-02. Acceso sin autorización válida (F-03 CA-28)

- **DADO** un acceso directo o con una autorización ausente o vencida.
- **CUANDO** se solicita la evidencia.
- **ENTONCES** el acceso es denegado.

### CA-03. Usuario no autorizado (F-03 CA-29)

- **DADO** un usuario que no es el repartidor propietario ni tiene rol `GESTOR_DESPACHO`.
- **CUANDO** solicita el acceso a la evidencia.
- **ENTONCES** el backend responde `403 Forbidden`.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Decisión técnica sobre almacenamiento y mecanismo de acceso.
- Eliminación o edición de evidencias.

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-09.
- `funcionalidades/pendiente.md`, sección F-03.
- `integraciones/api-contract.md`.
