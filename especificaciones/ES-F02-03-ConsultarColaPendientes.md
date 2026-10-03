# ES-F02-03: Consultar la cola de despachos pendientes

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho (aplicación web)

## 1. Objetivo

Permitir que el Gestor de Despacho consulte, filtre y priorice de forma paginada los despachos que se encuentran físicamente en el centro de despacho esperando salir (estado `PENDIENTE_ASIGNACION`). La consulta proporciona una vista rápida de las variables de carga (peso, volumen y paquetes), el tiempo en espera y la fecha programada, distinguiendo los despachos listos para ser asignados hoy de aquellos reprogramados para fechas futuras (F-04) o creados para pruebas.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO` mediante token JWT.
- Existen despachos registrados en el sistema procedentes de solicitudes de Ventas (ES-F02-01), reprogramaciones de Entregas Fallidas (F-04) o simulaciones de prueba (ES-F02-02).
- La consulta utiliza paginación por defecto y admite filtros por rango de fechas, zona de cobertura y número de intento.

## 3. Flujo principal

1. El Gestor ingresa a la pestaña "Cola de pendientes" dentro del panel de Programación y Asignación.
2. El frontend envía una petición `GET /api/v1/despachos/pendientes` incluyendo los parámetros de paginación y los filtros seleccionados por el usuario.
3. El backend valida el token y comprueba que el usuario posea el rol `GESTOR_DESPACHO`.
4. El sistema recupera exclusivamente los registros cuyo estado vigente es `PENDIENTE_ASIGNACION` que cumplan con los filtros de zona, fecha o intento.
5. Los registros se ordenan de forma predeterminada por fecha programada ascendente (primeros los despachos con fecha más próxima o atrasada).
6. Para cada despacho se calculan el tiempo transcurrido en espera y los indicadores de estado especial (Simulado, Reintento, Programado para fecha futura).
7. Se calculan los totales para las tarjetas de indicadores KPI ("Pendientes para hoy", "Programados a futuro", "Reintentos").
8. El backend responde con la página de resultados y metadatos de paginación.
9. El frontend renderiza la tabla a todo el ancho y habilita el botón "Asignar" únicamente para aquellos despachos cuya fecha programada sea igual o menor a la fecha de hoy.

## 4. Reglas y validaciones

- **Exclusividad de estado:** la consulta devuelve única y estrictamente registros en estado `PENDIENTE_ASIGNACION`. Cualquier despacho en estado `ASIGNADO`, `EN_CAMINO`, `ENTREGADO`, `FALLIDO`, `DEVUELTO_A_ORIGEN` o `CANCELADO` queda automáticamente excluido.
- **Campos mínimos por fila:** código operativo y de rastreo, identificador del pedido (`idPedido`), zona de cobertura, dirección de entrega (truncada a una línea), peso en kg, volumen en m³, cantidad de paquetes (unidades físicas), fecha programada, número de intento sobre el máximo permitido, tiempo transcurrido en espera y acción "Asignar".
- **Orden de presentación:** estricto orden ascendente por `fechaProgramada` (antigüedad de compromiso).
- **Despachos con fecha futura:** los despachos cuya fecha programada sea posterior al día actual del servidor se muestran con el distintivo informativo "Programado para [fecha]" y su botón "Asignar" se renderiza deshabilitado, mostrando el texto de ayuda "Disponible desde [fecha]".
- **Tiempo de espera elevado:** si el tiempo en espera del despacho supera el umbral estándar definido para la operación, se resalta visualmente en color de advertencia acompañado del ícono `IconClockExclamation` y tooltip descriptivo.
- **Filtros combinables:**
  - `fecha`: selector de fecha exacta o rango de fechas programadas.
  - `idZona`: selector de zona de cobertura activa.
  - `intento`: selector por categorías (Todos / Primer intento [intento = 0 o 1] / Reintentos [intento > 1]).
- **Paginación y rendimiento:** páginas configurables de 10 a 100 registros (20 por omisión); el tiempo de respuesta del backend no debe exceder 250 ms.
- **Seguridad:** el acceso no autorizado o sin rol `GESTOR_DESPACHO` se rechaza con `403 Forbidden` sin exponer registros.

## 5. Entradas, salidas e integraciones

### Entradas

- Parámetros de consulta (Query Params) en `GET /api/v1/despachos/pendientes`:
  - `pagina` (entero mayor o igual a 0).
  - `limite` (entero, tamaño de página).
  - `idZona` (opcional, string).
  - `fechaDesde` y `fechaHasta` (opcionales, formato `YYYY-MM-DD`).
  - `tipoIntento` (opcional: `TODOS`, `PRIMER_INTENTO`, `REINTENTOS`).
- Encabezado `Authorization: Bearer <jwt_usuario>`.

### Salidas

- Respuesta HTTP `200 OK` con estructura JSON:
  - `contenido`: lista de despachos pendientes con datos físicos, códigos, fechas y etiquetas.
  - `paginacion`: `paginaActual`, `totalPaginas`, `totalElementos`, `elementosPorPagina`.
  - `resumenKpi`: contadores agregados para "Pendientes hoy", "Programados a futuro" y "Reintentos".
- Estado vacío cuando no existen despachos pendientes (`totalElementos = 0`).
- Error `403 Forbidden` ante falta de permisos.

### Integraciones

- **Zonas de Cobertura (F-01):** provee los identificadores y nombres de zonas activas para el filtro.
- **Entregas Fallidas (F-04):** provee los despachos que reingresaron a la cola tras una reprogramación con su nuevo intento.
- **Modal de Asignación (ES-F02-04):** recibe el despacho seleccionado mediante el botón "Asignar".
- Las rutas y parámetros se detallan en `integraciones/api-contract.md` (Sección 9.2).

## 6. Criterios de aceptación

### CA-01. Consulta exitosa de la cola de pendientes

- **DADO** que existen despachos en estado `PENDIENTE_ASIGNACION`.
- **CUANDO** el Gestor abre la pantalla de programación con credenciales válidas.
- **ENTONCES** el sistema devuelve exclusivamente los despachos en dicho estado con todas las columnas obligatorias (incluyendo peso, volumen y cantidad física de paquetes), ordenados por fecha programada ascendente y con paginación.

### CA-02. Filtro combinado por zona y tipo de intento

- **DADO** una lista de despachos pendientes con diversas zonas e intentos.
- **CUANDO** el Gestor filtra por la zona "Lima Norte" y selecciona "Reintentos".
- **ENTONCES** el sistema devuelve únicamente los despachos de esa zona cuyo contador de intentos sea mayor a 1, conservando el estado `PENDIENTE_ASIGNACION`.

### CA-03. Restricción de asignación en despachos programados a futuro

- **DADO** un despacho reprogramado por F-04 con fecha de entrega posterior al día de hoy.
- **CUANDO** el Gestor visualiza la fila en la tabla.
- **ENTONCES** el despacho muestra la etiqueta "Programado para [fecha]" y el botón "Asignar" se encuentra deshabilitado con el mensaje explicativo "Disponible desde [fecha]".

### CA-04. Cola de pendientes vacía

- **DADO** que no existen despachos en espera de asignación.
- **CUANDO** el Gestor consulta la cola.
- **ENTONCES** la tabla muestra el estado vacío "No hay despachos pendientes de asignación" junto al botón "Generar pedido de prueba", sin mostrar registros de otros estados.

### CA-05. Acceso sin permisos requeridos

- **DADO** un usuario autenticado sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar el listado de pendientes.
- **ENTONCES** el backend responde `403 Forbidden` y no expone datos operativos ni contadores.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Asignar el despacho o seleccionar repartidor (corresponde a ES-F02-04).
- Consultar despachos ya asignados o en tránsito (corresponde a ES-F02-05).
- Modificar datos del pedido original o cancelar directamente sin anulación de Ventas.

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-02).
- Contrato de API: `integraciones/api-contract.md` (Sección 9.2).
- Diseño de interfaz: `disenio/funcionalidades/f-02.md` (Pantalla 1) y `disenio/SYSTEM-DESIGN.md` (Sección 21.D).
