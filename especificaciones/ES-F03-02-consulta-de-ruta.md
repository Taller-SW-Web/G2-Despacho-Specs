# ES-F03-02: Consulta de la ruta de la jornada

**Funcionalidad padre:** F-03 — Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** Max Rojas  
**Estado:** Borrador  
**Actor principal:** Repartidor

## 1. Objetivo

Mostrar al repartidor, en la vista "Mi Ruta", únicamente sus despachos de la jornada en curso, ordenados según la secuencia definida por F-02, para que sepa qué paquetes debe entregar y en qué orden.

## 2. Actor y precondiciones

- Actor: repartidor autenticado (ES-F03-01), en turno o fuera de turno.
- Rol requerido: `REPARTIDOR`.
- F-02 ha asignado los despachos con jornada y secuencia.

## 3. Flujo principal

1. El repartidor abre "Mi Ruta".
2. El sistema resuelve el repartidor desde el token.
3. El sistema recupera los despachos asignados a ese repartidor para la jornada en curso.
4. El sistema excluye los despachos `CANCELADO` y los reasignados a otro repartidor.
5. El sistema ordena los despachos por la secuencia de F-02 y los presenta con su indicador visual de estado.

## 4. Reglas y validaciones

- Solo se muestran despachos del repartidor resuelto desde el token y de la jornada en curso.
- Cada elemento muestra: código operativo interno, dirección, destinatario, estado, número de intento y posición en la secuencia.
- La dirección del destinatario solo se muestra mientras el despacho está en `ASIGNADO` o `EN_CAMINO`; no se ofrece exportación ni copia masiva.
- Si la petición incluye un identificador de repartidor distinto al del token, se responde `403 Forbidden` sin exponer datos.
- Los despachos de fechas anteriores que quedaron sin cierre (por falla del corte automático) no se incorporan a la ruta vigente: se muestran en una bandeja de "pendientes de regularización" y no pueden operarse.
- La vista contempla estados de carga, vacío y error.

## 5. Entradas, salidas e integraciones

### Entradas

- JWT del repartidor.

### Salidas

- Lista ordenada de despachos de la jornada, mensaje de ruta vacía o bandeja de pendientes de regularización.

### Integraciones

- F-02 Programación y Asignación: jornada, secuencia, destinatario y dirección de cada despacho.
- F-05 Monitoreo de Flota: resolución del repartidor.
- Ver `integraciones/api-contract.md`.

## 6. Criterios de aceptación

### CA-01. Carga exitosa de la ruta del día (F-03 CA-05)

- **DADO** que el repartidor tiene despachos de la jornada actual.
- **CUANDO** abre "Mi Ruta".
- **ENTONCES** el sistema lista los despachos ordenados por secuencia con código operativo interno, dirección, destinatario, estado, número de intento y posición, y excluye los despachos `CANCELADO` o reasignados a otro repartidor.

### CA-02. Jornada sin asignaciones (F-03 CA-06)

- **DADO** que el repartidor no tiene despachos en la jornada actual.
- **CUANDO** abre "Mi Ruta".
- **ENTONCES** el sistema muestra un mensaje de ruta vacía.

### CA-03. Acceso a despachos de otro repartidor (F-03 CA-07)

- **DADO** que un repartidor manipula la petición para consultar la ruta de otro.
- **CUANDO** el backend recibe un identificador distinto al resuelto desde su token.
- **ENTONCES** responde `403 Forbidden` sin exponer datos.

### CA-04. Despachos de jornadas anteriores (F-03 CA-08)

- **DADO** despachos de fechas anteriores que quedaron sin cierre por una falla del corte automático.
- **CUANDO** el repartidor carga su ruta.
- **ENTONCES** el sistema no los incorpora a la ruta vigente, los muestra en una bandeja de "pendientes de regularización" y no permite operarlos.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Definición de la secuencia, asignación, reasignación y cancelación de despachos (F-02).
- Cálculo de rutas o navegación propia; el repartidor usa aplicaciones externas de mapas.
- Regularización de los despachos de jornadas anteriores.

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-02 y sección 8 (Protección de datos).
- `integraciones/api-contract.md`.
- Wireframe de la vista "Mi Ruta".
