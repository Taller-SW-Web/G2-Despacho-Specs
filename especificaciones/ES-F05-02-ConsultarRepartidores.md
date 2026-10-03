# ES-F05-02: Consultar repartidores

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho consulte el catálogo de repartidores del módulo mediante un listado paginado con filtros por estado de registro, estado de vinculación y turno habitual. El panel sirve como punto de entrada para las operaciones de edición, baja y reintento de vinculación.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- Los repartidores fueron registrados previamente mediante ES-F05-01.
- La consulta utiliza paginación y puede incluir filtros opcionales.

## 3. Flujo principal

1. El Gestor ingresa al panel de repartidores.
2. El frontend solicita la primera página con los filtros seleccionados.
3. El backend valida el rol y recupera los repartidores que coinciden con los filtros.
4. El sistema devuelve la página con datos del repartidor, estados de registro y vinculación, y turno habitual.
5. El frontend presenta el listado con acciones disponibles por fila: editar, dar de baja y reintentar vinculación cuando aplique.

## 4. Reglas y validaciones

- Cada fila muestra como mínimo: identificador, nombres, apellidos, DNI, teléfono, turno habitual, estado de registro (`ACTIVO` / `INACTIVO`) y estado de vinculación (`PENDIENTE`, `PENDIENTE_ACTIVACION`, `VINCULADO`, `ERROR`).
- Los filtros por estado de registro, estado de vinculación y turno habitual pueden combinarse.
- Si no existen repartidores que coincidan, se muestra un estado vacío.
- Un usuario sin el rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- El listado pagina a partir de 50 registros y responde en menos de 200 ms.

## 5. Entradas, salidas e integraciones

### Entradas

- Página y tamaño de página.
- Filtro opcional por estado de registro.
- Filtro opcional por estado de vinculación.
- Filtro opcional por turno habitual.
- Identidad y roles obtenidos del JWT.

### Salidas

- Página de repartidores con los campos definidos.
- Metadatos de paginación.
- Estado vacío cuando no existen resultados.
- Error normalizado si la solicitud no está autorizada.

### Integraciones

- La ruta, parámetros y forma de error se rigen por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Listado con repartidores

- **DADO** que existen repartidores registrados.
- **CUANDO** el Gestor abre el panel de repartidores.
- **ENTONCES** el sistema muestra un listado paginado con los datos y estados de cada repartidor.

### CA-02. Aplicación de filtros

- **DADO** repartidores con distintos estados y turnos.
- **CUANDO** el Gestor combina uno o más filtros.
- **ENTONCES** el sistema devuelve solo las coincidencias.

### CA-03. Listado vacío

- **DADO** que no existen repartidores que coincidan con los filtros.
- **CUANDO** el Gestor consulta el panel.
- **ENTONCES** el frontend muestra un estado vacío.

### CA-04. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar los repartidores.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Registrar, editar o dar de baja repartidores.
- Consultar la disponibilidad operativa o la ocupación del repartidor en una jornada.
- Gestionar furgonetas.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-01 y CA-07.
- [cite: 2] `integraciones/api-contract.md`.
