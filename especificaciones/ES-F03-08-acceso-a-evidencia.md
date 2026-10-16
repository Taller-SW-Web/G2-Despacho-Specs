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
3. Operación concede una URL firmada temporal mediante el mecanismo definido en su contrato, §3.4.
4. El usuario visualiza la fotografía.

## 4. Reglas y validaciones

- La evidencia nunca se expone de forma pública.
- Acceso al objeto sin firma válida o con enlace vencido: denegado. Renovar el enlace exige validar otra vez la autorización del usuario.
- Usuario que no es el repartidor propietario ni tiene rol `GESTOR_DESPACHO`: `403 Forbidden`.
- El mecanismo de lectura está definido en [Operación §3.4](../integraciones/api-contract-operacion-reparto.md#34-autorizar-la-lectura-de-evidencia): respuesta, vigencia configurable, permisos y errores. Su implementación y comprobación real permanecen pendientes; no se exige perfil de repartidor al Gestor.

## 5. Entradas, salidas e integraciones

### Entradas

- JWT del usuario.
- Identificador de evidencia obtenido del recurso autorizado; Operación valida su asociación y devuelve el identificador del despacho correspondiente.

### Salidas

- URL firmada de lectura y vencimiento, o error contractual; una URL expirada o un fallo de carga no significan ausencia de fotografía.

### Integraciones

- Operación de Reparto y Flota: evidencia asociada en almacenamiento privado y autorización temporal.
- F-04 Entregas Fallidas: consume la referencia de su incidencia y permite consulta histórica después de resolver el despacho.
- Ver `integraciones/api-contract-operacion-reparto.md`.

## 6. Criterios de aceptación

### CA-01. Consulta autorizada de evidencia (F-03 CA-27)

- **DADO** un despacho con evidencia.
- **CUANDO** el repartidor propietario o un usuario con rol `GESTOR_DESPACHO` solicita verla.
- **ENTONCES** Operación devuelve URL firmada y vencimiento conforme a §3.4; el visor permite verla y renovar explícitamente un enlace vencido, sin persistir URLs ni conservar la fotografía de otro recurso.

### CA-02. Acceso sin autorización válida (F-03 CA-28)

- **DADO** un acceso al objeto sin firma válida o con enlace vencido.
- **CUANDO** se solicita la evidencia.
- **ENTONCES** el acceso es denegado.

### CA-03. Usuario no autorizado (F-03 CA-29)

- **DADO** un usuario que no es el repartidor propietario ni tiene rol `GESTOR_DESPACHO`.
- **CUANDO** solicita el acceso a la evidencia.
- **ENTONCES** el backend responde `403 Forbidden`.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Carga, procesamiento y conservación de fotografías; esta consulta consume el almacenamiento privado y la autorización definidos en el contrato.
- Eliminación o edición de evidencias.

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-09.
- `funcionalidades/pendiente.md`, sección F-03.
- `integraciones/api-contract-operacion-reparto.md`.
