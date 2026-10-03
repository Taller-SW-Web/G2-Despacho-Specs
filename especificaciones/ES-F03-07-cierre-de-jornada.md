# ES-F03-07: Cierre de jornada y resumen del día

**Funcionalidad padre:** F-03 — Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** Max Rojas  
**Estado:** Borrador  
**Actor principal:** Repartidor (proceso programado en el corte automático)

## 1. Objetivo

Garantizar que ningún despacho quede en `ASIGNADO` ni `EN_CAMINO` al terminar la jornada. Los pendientes pasan a `FALLIDO` con motivo `NO_INTENTADO` sin consumir intentos, de modo que se distingan de los intentos reales.

El cierre lo ejecuta el repartidor; si no lo hace, un corte automático a la hora configurada aplica el mismo tratamiento. Al cerrar, y en cualquier momento del día, el repartidor puede consultar el resumen de su jornada.

## 2. Actor y precondiciones

- Actor: repartidor en turno; en el corte automático, el proceso programado del módulo.
- Rol requerido: `REPARTIDOR` (cierre manual y resumen).
- El repartidor tiene una asignación diaria activa.
- Existe una hora de corte configurada.
- Existe conexión activa (cierre manual).

## 3. Flujo principal

1. El repartidor pulsa "Cerrar jornada".
2. El sistema identifica los despachos de la jornada en `ASIGNADO` o `EN_CAMINO` y advierte cuántos quedarán como no intentados.
3. El repartidor confirma el cierre.
4. El sistema recibe la solicitud con su clave de idempotencia y pasa cada despacho pendiente a `FALLIDO` con motivo `NO_INTENTADO`, sin incrementar el contador y registrando cada transición en el historial.
5. El sistema solicita a F-05 el cierre del turno; el repartidor pasa a `FUERA_DE_TURNO`.
6. El sistema lista los paquetes que el repartidor debe devolver al centro de despacho y muestra el resumen de la jornada.

**Flujo alternativo — corte automático:** a la hora de corte configurada, el proceso programado identifica a los repartidores que no cerraron su jornada y ejecuta los pasos 4 y 5 por cada uno, registrando la operación como automática.

## 4. Reglas y validaciones

- El cierre se permite con pendientes o sin ellos; sin pendientes solo se registra el cierre y no se generan fallos.
- `NO_INTENTADO` no requiere fotografía ni incrementa el contador de intentos.
- Los despachos resueltos como `NO_INTENTADO` quedan disponibles para F-04.
- El cambio de estado y el historial de cada despacho se persisten en una misma transacción.
- En el corte automático, el ejecutor registrado es el proceso automático y el origen es automático.
- Los despachos ya resueltos no se vuelven a procesar; una ejecución repetida del corte no genera transiciones adicionales.
- Si el corte falla, los despachos que quedan abiertos se tratan al día siguiente como "pendientes de regularización" (ES-F03-02, CA-04).
- Idempotencia: repetir la solicitud de cierre con la misma clave devuelve el resultado original sin duplicar transiciones.
- Sin conexión: la interfaz informa que el cierre no se registró y exige un reintento explícito.
- El resumen muestra asignados, entregados, fallidos con intento, no intentados y pendientes; las cifras deben coincidir con el historial.
- El resumen es solo del propio repartidor y se puede consultar también fuera de turno (ES-F03-01).

## 5. Entradas, salidas e integraciones

### Entradas

- JWT del repartidor y confirmación explícita del cierre.
- Clave de idempotencia.
- Hora de corte configurada (corte automático).

### Salidas

- Despachos pendientes en `FALLIDO` (`NO_INTENTADO`) con su registro en el historial.
- Repartidor en `FUERA_DE_TURNO`.
- Lista de paquetes a devolver al centro y resumen de la jornada.

### Integraciones

- F-05 Monitoreo de Flota: cierre del turno.
- F-04 Entregas Fallidas: consume los despachos `NO_INTENTADO`.
- Máquina de estados, historial común y publicación de eventos (overview, sección 6, RT-02 y RT-03).
- Ver `integraciones/api-contract.md`.

## 6. Criterios de aceptación

### CA-01. Cierre con despachos pendientes (F-03 CA-23)

- **DADO** despachos en `ASIGNADO` o `EN_CAMINO` al terminar el turno.
- **CUANDO** el repartidor confirma el cierre, advertido de la cantidad de despachos afectados.
- **ENTONCES** esos despachos pasan a `FALLIDO` con motivo `NO_INTENTADO` sin incrementar el contador, la interfaz lista los paquetes que debe devolver al centro, quedan disponibles para F-04 y F-05 pone al repartidor en `FUERA_DE_TURNO`.

### CA-02. Cierre sin pendientes (F-03 CA-25)

- **DADO** que ningún despacho de la jornada está en `ASIGNADO` ni `EN_CAMINO`.
- **CUANDO** el repartidor confirma el cierre.
- **ENTONCES** se registra el cierre, el repartidor pasa a `FUERA_DE_TURNO` y se muestra el resumen sin generar fallos.

### CA-03. Corte automático de respaldo (F-03 CA-24)

- **DADO** que el repartidor no cerró su jornada antes de la hora de corte configurada.
- **CUANDO** se ejecuta el proceso automático.
- **ENTONCES** se aplica el tratamiento de CA-01 y el historial identifica la operación como automática.

### CA-04. Consolidado correcto del resumen (F-03 CA-26)

- **DADO** un repartidor con despachos en distintos estados.
- **CUANDO** consulta el resumen.
- **ENTONCES** ve total asignado, entregados, fallidos con intento, no intentados y pendientes, coincidentes con el historial.

### CA-05. Registro en el historial (F-03 CA-31)

- **DADO** un despacho resuelto como `NO_INTENTADO` por el cierre manual o el corte automático.
- **CUANDO** se persiste la transición.
- **ENTONCES** el historial guarda despacho, ejecutor, origen manual o automático, marca temporal del servidor, estado anterior, estado nuevo y motivo `NO_INTENTADO`.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Recepción física de los paquetes devueltos en el centro (F-04).
- Gestión de jornadas y turnos más allá de solicitar el cierre (F-05).
- Definición del valor de la hora de corte.
- Regularización de despachos que el corte no logró cerrar.
- Reportes de flota o de otros repartidores, y exportación del resumen.

### Referencias

- `funcionalidades/F-03-AppMovilRepartidor.md`, RF-07, RF-08, RF-11, sección 7 y Anexo A.
- `integraciones/api-contract.md`.
- Wireframes del cierre y del resumen de jornada.
