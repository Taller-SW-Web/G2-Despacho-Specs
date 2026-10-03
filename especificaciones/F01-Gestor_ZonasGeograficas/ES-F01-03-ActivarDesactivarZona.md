# ES-F01-03: Activar y desactivar una zona de cobertura

**Funcionalidad padre:** F-01 — Gestor de zonas geográficas y cotizador de envíos  
**Responsable:** Valqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho

## 1. Objetivo

Permitir que el Gestor de Despacho active o desactive una zona de cobertura y verificar que el cambio surte efecto únicamente sobre las operaciones futuras. La activación devuelve una zona a la cobertura efectiva del módulo; la desactivación la retira de la cobertura sin alterar los despachos que ya fueron asociados a ella.

## 2. Actor y precondiciones

- El actor está autenticado con un JWT que incluye el rol `GESTOR_DESPACHO`.
- La zona existe y tiene una delimitación persistida por esta misma funcionalidad.
- Los despachos asociados a la zona conservan su identificador de zona aunque la zona se desactive.

## 3. Flujo principal

1. El Gestor selecciona la acción de activar o desactivar desde el catálogo.
2. El frontend muestra la confirmación con el efecto esperado sobre cotizaciones y solicitudes.
3. El backend valida el rol y el estado actual de la zona.
4. En una activación, el sistema verifica que la cobertura no colisione con otra zona activa.
5. El sistema cambia el estado de la zona, registra el usuario y la marca temporal, y confirma la operación.

## 4. Reglas y validaciones

- Los únicos estados de una zona son `ACTIVO` e `INACTIVO`.
- Solo se cotiza y solo se resuelve zona para destinos incluidos en zonas `ACTIVO`.
- Una zona desactivada deja de aceptar nuevas cotizaciones y nuevas solicitudes de despacho.
- Los despachos ya registrados en la zona desactivada conservan su zona y continúan su ciclo sin cambios, incluidas sus reprogramaciones.
- Una zona no puede activarse si comparte algún distrito o código postal con una zona `ACTIVO`; el conflicto produce `409 Conflict` y la zona permanece `INACTIVO`.
- Si la zona ya se encuentra en el estado solicitado, el sistema responde con el estado vigente y no genera un cambio ni una auditoría adicional.
- La operación es idempotente por zona y estado: repetirla no produce duplicados.
- El cambio de estado se valida con control de versión para que dos operaciones simultáneas no se pisen.
- El frontend nunca ejecuta la desactivación directamente desde la tabla: siempre requiere la confirmación advertida.
- Un usuario sin el rol `GESTOR_DESPACHO` obtiene `403 Forbidden` y no expone información de configuración.

## 5. Entradas, salidas e integraciones

### Entradas

- Identificador de la zona.
- Estado solicitado: activar o desactivar.
- Identidad y roles obtenidos del JWT.

### Salidas

- Estado vigente de la zona tras la operación.
- Confirmación de la operación y actualización de la fila en el catálogo.
- Error normalizado ante conflicto de solapamiento, conflicto de versión o falta de permisos.

### Integraciones

- F-02 y los canales observan el efecto del cambio a través de la resolución de zona y de la cotización, sin recibir notificaciones adicionales.
- Seguridad y Usuarios emite el JWT que habilita el acceso administrativo.
- La ruta, el cuerpo de la operación y las formas de respuesta y error se rigen exclusivamente por `integraciones/api-contract.md` [cite: 2].

## 6. Criterios de aceptación

### CA-01. Activación sin conflicto

- **DADO** una zona en `INACTIVO` cuyos distritos y códigos postales no pertenecen a otra zona activa.
- **CUANDO** el Gestor la activa.
- **ENTONCES** el sistema la cambia a `ACTIVO` y vuelve a atender cotizaciones y resoluciones de zona para su cobertura.

### CA-02. Activación con conflicto de solapamiento

- **DADO** una zona en `INACTIVO` que comparte un distrito o código postal con una zona `ACTIVO`.
- **CUANDO** el Gestor intenta activarla.
- **ENTONCES** el sistema responde `409 Conflict`, identifica la zona activa en conflicto y conserva el estado `INACTIVO`.

### CA-03. Desactivación de una zona con despachos registrados

- **DADO** una zona activa con despachos registrados que aún no han sido entregados.
- **CUANDO** el Gestor la desactiva.
- **ENTONCES** la zona deja de aceptar cotizaciones y solicitudes nuevas, y los despachos existentes conservan su zona y continúan su ciclo, incluidas sus reprogramaciones.

### CA-04. Repetición de la misma operación

- **DADO** que la zona ya se encuentra en el estado solicitado.
- **CUANDO** el Gestor repite la acción.
- **ENTONCES** el sistema responde con el estado vigente sin generar un cambio adicional ni una auditoría duplicada.

### CA-05. Cambios concurrentes

- **DADO** dos solicitudes simultáneas de cambio de estado sobre la misma zona.
- **CUANDO** ambas se procesan.
- **ENTONCES** solo una se aplica y la otra recibe `409 Conflict` con el estado vigente.

### CA-06. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO`.
- **CUANDO** intenta cambiar el estado de una zona.
- **ENTONCES** el sistema responde `403 Forbidden` y no expone información de configuración.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Registrar o editar la cobertura de la zona.
- Configurar la tarifa de la zona.
- Reasignar, reprogramar o cancelar los despachos asociados a una zona desactivada.
- Notificar a F-02, F-05 o a los canales el cambio de estado.

### Referencias

- [cite: 1] `funcionalidades/F-01-Gestor_ZonasGeograficas.md`, RF-01, CA-04, CA-13 y CA-17.
- [cite: 2] `integraciones/api-contract.md`, secciones 3.3, 9.1 y 14.
- [cite: 3] `disenio/funcionalidades/f-01.md`, Pantalla 4: Confirmación de Desactivación de Zona.
- [cite: 4] `disenio/SystemDesign/f-01-alta-fidelidad.md`, modal de desactivación.
- [cite: 5] `arquitectura/modelo-datos.md`, columna `estado` de `zonas` y relaciones con `despachos`.
- [cite: 6] `overview.md`, sección 1.2 sobre fuentes únicas y sección 3.2 sobre relaciones entre funcionalidades.