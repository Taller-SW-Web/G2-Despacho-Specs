# ES-F05-07: Consultar furgonetas

**Funcionalidad padre:** F-05 — Gestión de repartidores y vehículos  
**Responsable:** Rhamses  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho consulte el catálogo de furgonetas del módulo mediante un listado paginado con filtros por estado y placa. El panel sirve como punto de entrada para las operaciones de edición y cambio de estado de cada furgoneta.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- Las furgonetas fueron registradas previamente mediante ES-F05-06.
- La consulta utiliza paginación y puede incluir filtros opcionales.

## 3. Flujo principal

1. El Gestor ingresa al panel de furgonetas.
2. El frontend solicita la primera página con los filtros seleccionados.
3. El backend valida el rol y recupera las furgonetas que coinciden con los filtros.
4. El sistema devuelve la página con datos de la furgoneta incluyendo placa, estado y límites de carga.
5. El frontend presenta el listado con acciones disponibles por fila: editar y cambiar estado.

## 4. Reglas y validaciones

- Cada fila muestra como mínimo: identificador, placa, estado (`DISPONIBLE`, `EN_MANTENIMIENTO`, `FUERA_DE_SERVICIO`), límite de peso (kg), límite de volumen (m³) y máximo de paquetes.
- Los filtros por estado y búsqueda por placa pueden combinarse.
- Si no existen furgonetas que coincidan, se muestra un estado vacío.
- Un usuario sin el rol `GESTOR_DESPACHO` recibe `403 Forbidden`.
- El listado pagina a partir de 50 registros y responde en menos de 200 ms.

## 5. Entradas, salidas e integraciones

### Entradas

- Página y tamaño de página.
- Filtro opcional por estado de la furgoneta.
- Búsqueda opcional por placa.
- Identidad y roles obtenidos del JWT.

### Salidas

- Página de furgonetas con los campos definidos.
- Metadatos de paginación.
- Estado vacío cuando no existen resultados.
- Error normalizado si la solicitud no está autorizada.

### Integraciones

- La ruta, parámetros y forma de error se rigen por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Listado con furgonetas

- **DADO** que existen furgonetas registradas.
- **CUANDO** el Gestor abre el panel de furgonetas.
- **ENTONCES** el sistema muestra un listado paginado con placa, estado y límites de carga.

### CA-02. Filtro por estado

- **DADO** furgonetas con distintos estados.
- **CUANDO** el Gestor filtra por `DISPONIBLE`.
- **ENTONCES** el sistema devuelve solo las furgonetas en ese estado.

### CA-03. Búsqueda por placa

- **DADO** furgonetas registradas.
- **CUANDO** el Gestor busca por placa "ABC".
- **ENTONCES** el sistema devuelve las furgonetas cuya placa contiene ese texto.

### CA-04. Listado vacío

- **DADO** que no existen furgonetas que coincidan con los filtros.
- **CUANDO** el Gestor consulta el panel.
- **ENTONCES** el frontend muestra un estado vacío.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta consultar las furgonetas.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Registrar, editar o cambiar el estado de furgonetas.
- Consultar la ocupación actual de una furgoneta en jornada.
- Gestionar repartidores.

### Referencias

- [cite: 1] `funcionalidades/F-05-GestionRepartidoresVehiculos.md`, RF-02 y CA-13.
- [cite: 2] `integraciones/api-contract.md`.
