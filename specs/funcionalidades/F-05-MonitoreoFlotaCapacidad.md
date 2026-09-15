# Especificación F-05: Monitoreo de Flota, Operadores y Capacidad Diaria

**Responsable:** Rhamses
**Estado:** En especificación
**Actor principal:** Gestor de Flota

## 1. Contexto

El módulo de Despacho y Entrega opera con un equipo de repartidores y una flota de vehículos heterogénea (motos, autos, furgonetas). Sin un registro centralizado de quién está en turno, qué vehículo le corresponde y cuánta carga puede asumir durante el día, el Panel de Programación (F-02) no tiene información confiable para asignar pedidos: puede saturar a un operador, asignar un paquete pesado a una moto, o intentar enviar a alguien que no está trabajando ese día.

Este subsistema actúa como el proveedor oficial de disponibilidad operativa dentro del módulo. Administra las tablas maestras de repartidores y vehículos, y expone un servicio de consulta que F-02 consume en tiempo real antes de asignar cada despacho. La información de flota también determina qué repartidores pueden iniciar sesión en la App Móvil (F-03).

## 2. Propósito

Proveer al Gestor de Flota de un panel administrativo para gestionar el personal de reparto y los vehículos, configurar sus límites operativos diarios y supervisar en tiempo real el estado de ocupación de la flota, de modo que la asignación de despachos siempre ocurra sobre información actualizada y sin riesgo de sobrecarga.

## 3. Alcance

Esta funcionalidad incluye:

- CRUD completo de repartidores: registro, edición de datos personales, cambio de estado operativo y asignación de turno de trabajo.
- CRUD completo de vehículos: registro de unidades con su tipo, placa, estado mecánico y límites de carga (peso en kg, volumen en m³ y máximo de paquetes por jornada).
- Asignación operativa diaria: emparejamiento de un repartidor con un vehículo para la jornada en curso.
- Panel gráfico de monitoreo con indicadores por repartidor (estado, paquetes asignados, porcentaje de ocupación) y resumen global de la flota.
- Endpoint `GET /api/v1/repartidores/disponibles` para proveer a F-02 el catálogo de operadores habilitados para recibir nuevos despachos.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario debe estar autenticado con el rol `GESTOR_FLOTA` o `ADMIN_DESPACHO` para cualquier operación de configuración.
- Para registrar un repartidor, su documento de identidad no debe existir previamente en el sistema.
- Para asociar un vehículo a un repartidor, ambos deben existir y encontrarse en estado activo.
- Solo puede existir una asignación operativa activa por repartidor por jornada.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Proporcionar la identidad autenticada mediante token JWT y los permisos del Gestor de Flota. |
| Programación y Asignación (F-02) | Consumir el endpoint `GET /api/v1/repartidores/disponibles` para filtrar a quién asignar pedidos. |
| Operación del Repartidor (F-03) | Verificar que el repartidor está registrado y activo antes de permitirle iniciar sesión en la App Móvil. |

### 4.3. Resultados

- Un repartidor registrado queda en estado `INACTIVO` hasta que inicie turno y se le asocie un vehículo.
- La asignación operativa diaria activa al repartidor y le transfiere los límites de carga del vehículo asignado.
- El cambio de estado de un repartidor a `FUERA_DE_TURNO` lo excluye inmediatamente de las respuestas del endpoint de disponibilidad.
- El panel gráfico refleja en todo momento la suma de paquetes asignados (estado `ASIGNADO` o `EN_CAMINO`) frente al límite diario configurado.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Gestión de repartidores

El sistema DEBE permitir registrar, editar, cambiar el estado y consultar los operadores de reparto del módulo.

#### CA-01. Registro exitoso de un nuevo repartidor

- **DADO** que el Gestor de Flota ingresa los datos de un nuevo operador: nombres, apellidos, DNI, teléfono, número de brevete y turno habitual.
- **CUANDO** confirma el registro.
- **ENTONCES** el sistema valida que el DNI no exista previamente, crea el repartidor con estado `INACTIVO` y devuelve su identificador único.

#### CA-02. Rechazo por documento de identidad duplicado

- **DADO** que ya existe un repartidor registrado con un DNI determinado.
- **CUANDO** se intenta registrar otro operador con el mismo número de documento.
- **ENTONCES** el sistema rechaza la operación con código `409 Conflict` e indica que el documento ya está registrado, sin persistir el duplicado.

#### CA-03. Desactivación de un repartidor con despachos históricos

- **DADO** que un repartidor tiene despachos finalizados asociados en el historial.
- **CUANDO** el Gestor cambia su estado a `INACTIVO`.
- **ENTONCES** el sistema aplica baja lógica (no elimina el registro), lo excluye de nuevas asignaciones y preserva su historial de entregas intacto.

#### CA-04. Acceso sin permisos requeridos

- **DADO** que un usuario sin el rol `GESTOR_FLOTA` ni `ADMIN_DESPACHO` intenta registrar o modificar repartidores.
- **CUANDO** realiza la petición al backend.
- **ENTONCES** el sistema rechaza la solicitud con código `403 Forbidden` y no expone información del personal.

### RF-02. Gestión de vehículos y capacidad

El sistema DEBE permitir administrar el catálogo de vehículos con sus límites de carga y su estado de servicio.

#### CA-05. Registro de vehículo con parámetros de capacidad

- **DADO** que el Gestor registra una furgoneta con placa "ABC-123", capacidad de 500 kg, 4.0 m³ y tope de 80 paquetes diarios.
- **CUANDO** confirma el registro.
- **ENTONCES** el sistema guarda la unidad con estado `DISPONIBLE` y sus límites de carga configurados.

#### CA-06. Rechazo de vehículo con placa duplicada

- **DADO** que ya existe un vehículo registrado con la placa "ABC-123".
- **CUANDO** se intenta registrar otro con la misma placa.
- **ENTONCES** el sistema rechaza la operación con código `409 Conflict` y no persiste el duplicado.

#### CA-07. Desactivación de vehículo por mantenimiento

- **DADO** que un vehículo debe entrar a mantenimiento.
- **CUANDO** el Gestor cambia su estado a `EN_MANTENIMIENTO`.
- **ENTONCES** el sistema lo excluye de las asignaciones operativas disponibles y, si tenía un repartidor asociado en el turno activo, lo marca como sin vehículo asignado.

### RF-03. Asignación operativa diaria (repartidor – vehículo)

El sistema DEBE permitir vincular a cada repartidor un vehículo para la jornada en curso, heredándole sus límites de capacidad.

#### CA-08. Asignación diaria exitosa

- **DADO** que el Gestor inicia el turno de la mañana y selecciona al repartidor "Juan Pérez" y la furgoneta "ABC-123".
- **CUANDO** confirma la asignación operativa del día.
- **ENTONCES** el sistema activa al repartidor con estado `DISPONIBLE`, le asigna los límites de la furgoneta (500 kg, 4.0 m³, 80 paquetes) y lo incluye en las respuestas del endpoint de disponibilidad.

#### CA-09. Rechazo por asignación duplicada en la misma jornada

- **DADO** que el repartidor "Juan Pérez" ya tiene una asignación operativa activa en la jornada actual.
- **CUANDO** se intenta crear otra asignación para el mismo operador en el mismo día.
- **ENTONCES** el sistema rechaza la operación con código `409 Conflict` e indica que el repartidor ya fue asignado en esta jornada.

### RF-04. Panel gráfico de monitoreo de flota

El sistema DEBE presentar al Gestor de Flota un tablero visual actualizado con el estado de ocupación de cada repartidor en tiempo real.

#### CA-10. Visualización de repartidor saturado

- **DADO** que un repartidor tiene un tope de 50 paquetes y se le han asignado 48 despachos en estado `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el Gestor de Flota consulta el panel de monitoreo.
- **ENTONCES** el sistema muestra al operador con una barra de progreso en color rojo, etiqueta de estado `SATURADO` y la relación numérica `48/50 paquetes (96%)`.

#### CA-11. Resumen global de disponibilidad de flota

- **DADO** que existen 8 repartidores en turno con distintos estados de carga.
- **CUANDO** el Gestor accede al panel de monitoreo.
- **ENTONCES** el sistema muestra tarjetas de resumen con el total de repartidores `DISPONIBLES`, `EN_RUTA`, `SATURADOS` e `INACTIVOS`, actualizadas sin necesidad de recargar la página.

### RF-05. API de consulta de disponibilidad para programación

El sistema DEBE exponer un endpoint que devuelva únicamente los operadores habilitados para recibir nuevos despachos, con su balance de capacidad actualizado.

#### CA-12. Respuesta con operadores disponibles y su balance de carga

- **DADO** que existen 5 repartidores en turno, de los cuales 3 tienen capacidad remanente (estados `DISPONIBLE` o `EN_RUTA`) y 2 están `SATURADOS` o `FUERA_DE_TURNO`.
- **CUANDO** el servicio de F-02 invoca `GET /api/v1/repartidores/disponibles`.
- **ENTONCES** el sistema retorna la lista de los 3 operadores habilitados, incluyendo por cada uno: identificador, nombre, tipo de vehículo, capacidad máxima, paquetes asignados, porcentaje de ocupación y estado.

#### CA-13. Respuesta vacía cuando no hay repartidores disponibles

- **DADO** que todos los repartidores en turno están `SATURADOS` o `FUERA_DE_TURNO`.
- **CUANDO** F-02 invoca el endpoint de disponibilidad.
- **ENTONCES** el sistema retorna código `200 OK` con una lista vacía, sin generar error.

## 6. Frontend

La funcionalidad tendrá una experiencia web responsive compuesta por:

| Elemento | Responsabilidad |
|---|---|
| Panel de Repartidores | Mostrar el listado paginado con filtros por estado y turno, y acciones para registrar, editar o cambiar el estado de un operador. |
| Formulario de Repartidor | Registrar o editar datos personales, brevete y turno habitual del operador. |
| Panel de Vehículos | Mostrar el catálogo con filtros por tipo, estado mecánico y placa, con acciones de alta, edición y cambio de estado. |
| Formulario de Vehículo | Registrar o editar tipo, placa, estado y límites de capacidad (kg, m³, paquetes). |
| Asignación Diaria | Interfaz de emparejamiento repartidor–vehículo con validación de disponibilidad antes de confirmar. |
| Dashboard de Monitoreo | Tarjetas de resumen global de flota y tabla por repartidor con barra de progreso coloreada por nivel de ocupación. |
| Retroalimentación | Informar resultados exitosos, conflictos de duplicidad, validaciones de capacidad y errores de red. |

La interfaz debe impedir acciones conocidas como inválidas, pero las mismas reglas deben validarse siempre en el backend.

## 7. Backend

El backend deberá cubrir las siguientes responsabilidades lógicas:

| Componente lógico | Responsabilidad |
|---|---|
| Controlador de Repartidores | Exponer el CRUD de operadores (`/api/v1/repartidores`) con validación de unicidad de documento y autorización. |
| Controlador de Vehículos | Exponer el CRUD de vehículos (`/api/v1/vehiculos`) con validación de unicidad de placa y estado mecánico. |
| Servicio de Asignación Diaria | Crear y validar la asignación operativa repartidor–vehículo para la jornada activa sin duplicar. |
| Motor de Ocupación | Calcular en tiempo real el porcentaje de ocupación de cada repartidor sumando sus despachos activos. |
| Endpoint de Disponibilidad | Resolver `GET /api/v1/repartidores/disponibles` filtrando por estado y capacidad remanente con latencia menor a 200 ms. |
| Persistencia y Auditoría | Registrar en PostgreSQL todos los cambios de estado de repartidores y vehículos con usuario y marca temporal. |

Las rutas, cuerpos, respuestas y códigos específicos se centralizan en `specs/api-contract.md` y se publicarán mediante Swagger UI desde el backend desplegado.

## 8. Requisitos no funcionales

- **Rendimiento:** El endpoint `GET /api/v1/repartidores/disponibles` debe responder en menos de 200 ms para no agregar latencia al flujo de asignación de F-02.
- **Seguridad:** Todas las operaciones de configuración y consulta del panel requieren autenticación con token JWT y rol `GESTOR_FLOTA` o `ADMIN_DESPACHO`. El endpoint de disponibilidad es de uso interno entre servicios del módulo.
- **Aislamiento:** El módulo administra sus propios datos sin acceder directamente a bases de datos de otros módulos.
- **Integridad referencial:** Los repartidores y vehículos con historial de despachos solo pueden desactivarse lógicamente; no se permite su eliminación física.
- **Trazabilidad:** Cada cambio de estado o asignación operativa debe registrar el usuario gestor y la marca temporal exacta en UTC.
- **Escalabilidad:** El panel de monitoreo debe soportar paginación para equipos con más de 50 operadores activos simultáneos.

## 9. Fuera de alcance

- **Mantenimiento mecánico y costos:** El registro de reparaciones, gastos de combustible o compra de repuestos corresponde al ERP de la empresa.
- **Rastreo GPS en tiempo real del vehículo:** El seguimiento punto a punto con telemetría o sensores IoT no está comprendido en esta fase.
- **Asignación de despachos a repartidores:** Vincular un pedido a un operador es responsabilidad exclusiva del Panel de Programación (F-02); F-05 solo provee el catálogo de disponibilidad.
- **Autenticación de repartidores:** La validación del token JWT del repartidor en la App Móvil es responsabilidad del módulo de Seguridad y Usuarios.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 y CA-02 | Registrar operadores válidos y con DNI duplicado. | Integración y unitaria | Registro exitoso con identificador único y rechazo `409` para duplicados. |
| CA-03 | Desactivar un repartidor con historial y verificar que el registro persiste. | Integración | Baja lógica aplicada, historial intacto y operador excluido del endpoint de disponibilidad. |
| CA-04 | Invocar endpoints de repartidores sin credenciales o con rol incorrecto. | Integración de seguridad | Código `403 Forbidden` y bloqueo total de información. |
| CA-05 a CA-07 | Registrar vehículos válidos, con placa duplicada y aplicar cambio de estado por mantenimiento. | Integración y unitaria | Registro exitoso, rechazo `409` para placa duplicada y exclusión del catálogo de asignación. |
| CA-08 y CA-09 | Crear asignación operativa válida y repetir la operación en la misma jornada. | Unitaria e integración | Activación correcta del repartidor con límites del vehículo y rechazo `409` para duplicado. |
| CA-10 y CA-11 | Consultar el panel con repartidores en distintos niveles de carga. | Integración y frontend | Barras de progreso correctas, colores y resumen global coherente con los datos de la base de datos. |
| CA-12 y CA-13 | Invocar el endpoint de disponibilidad con operadores disponibles y sin ninguno disponible. | Integración | Lista filtrada correctamente y respuesta `200 OK` con lista vacía cuando no hay disponibles. |

Además, se ejecutarán dos recorridos funcionales completos:

1. `Alta de repartidor` → asignación de vehículo para la jornada → aparición en el endpoint de disponibilidad → confirmación de asignación desde F-02 → actualización de porcentaje de ocupación.
2. `Saturación de operador` → cambio automático a estado `SATURADO` → exclusión del endpoint de disponibilidad → cambio visual en el panel de monitoreo.

Las pruebas unitarias cubrirán el motor de cálculo de ocupación y las reglas de unicidad; las pruebas de integración cubrirán seguridad, persistencia PostgreSQL y el endpoint de disponibilidad; las pruebas de frontend validarán el panel de monitoreo, formularios y la asignación diaria.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Todos los criterios `CA-01` a `CA-13` están implementados y cuentan con pruebas automatizadas exitosas.
- Los dos recorridos funcionales completos han sido verificados de extremo a extremo.
- F-02 consume correctamente el endpoint `/api/v1/repartidores/disponibles` y la asignación de despachos respeta los límites provistos por F-05.
- El panel de monitoreo refleja en tiempo real el estado de ocupación de cada repartidor con los colores y etiquetas correctos.
- La baja lógica de repartidores y vehículos preserva el historial de entregas asociado.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede trazarse hacia cada criterio de aceptación.
