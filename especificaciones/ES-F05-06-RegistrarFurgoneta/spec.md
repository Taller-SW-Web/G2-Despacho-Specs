# ES-F05-06: Registrar una nueva furgoneta

**Funcionalidad padre:** [F-05 — Gestión de repartidores y vehículos](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md).

**Responsable:** Rhamses (Kevin Rhamses Bohorquez).

**Estado:** Borrador migrado a SDD; revisión funcional y aceptación pendientes.

**Actor principal:** Gestor de Despacho.

**UI:** Aplica; nueva furgoneta desde el catálogo administrativo `/furgonetas`. Se detalla en [ui.md](./ui.md).

**Servicio propietario:** Operación de Reparto y Flota.

> Migración estructural desde `ES-F05-06-RegistrarFurgoneta.md`, revisión `f3849d9`. Se conservan las reglas y los criterios originales, incluidos sus IDs. Las discrepancias detectadas se registran en §7 y en el plan; esta migración no aprueba cambios de contrato ni acredita integración desplegada.

## 1. Contexto y objetivo

Permitir que el Gestor de Despacho registre una furgoneta en el módulo, definiendo su placa identificadora y sus límites de carga (peso en kg, volumen en m³ y máximo de paquetes en ruta). La furgoneta queda disponible para ser asignada a jornadas operativas en F-06.

El alcance general y la propiedad del catálogo corresponden a la funcionalidad padre [cite: 1].

## 2. Alcance

- Incluye: Alta, validación de placa y límites de peso, volumen y cantidad.
- Resultado del comportamiento: Furgoneta disponible, identificable y auditada con las capacidades solicitadas.

### Fuera de alcance

- Editar los límites de carga después del registro.
- Cambiar el estado de la furgoneta.
- Asignar la furgoneta a una jornada operativa.

## 3. Actor, precondiciones y resultados

- El actor está autenticado con el rol `GESTOR_DESPACHO`.
- La placa de la furgoneta no existe en el módulo.
- Los campos obligatorios son: placa, límite de peso (kg), límite de volumen (m³) y máximo de paquetes en ruta.
- Los límites de carga deben ser mayores que cero.

- Autorización de referencia: [roles y tipos de token](../../integraciones/api-contract.md#33-roles-humanos-y-tokens-de-servicio).
- Disparador: Nueva furgoneta en `/furgonetas`, conforme al flujo conservado.
- Resultado exitoso: Furgoneta disponible, identificable y auditada con las capacidades solicitadas.
- Resultado ante rechazo: informar el motivo permitido por el contrato y conservar los datos ajenos a una operación confirmada.

## 4. Flujo principal y alternativas

1. El Gestor ingresa al panel de furgonetas y selecciona `Nueva furgoneta`.
2. El frontend presenta el formulario con los campos obligatorios.
3. El Gestor completa los datos y confirma el registro.
4. El backend valida el rol, la completitud, el formato y la unicidad de la placa.
5. El sistema crea la furgoneta con estado `DISPONIBLE` y los límites definidos.
6. Se registra la auditoría del alta con usuario y marca temporal en UTC.
7. El frontend muestra la furgoneta creada en el panel.

| Criterio | Escenario | Comprobación esperada |
|---|---|---|
| CA-01 | Registro exitoso | Registrar ABC-123 con 500 kg, 4 m³ y 80 paquetes y comprobar estado y auditoría. |
| CA-02 | Placa duplicada | Repetir la placa y comprobar conflicto sin otra furgoneta. |
| CA-03 | Límites inválidos | Enviar cero y negativos en las capacidades y comprobar errores de campo. |
| CA-04 | Datos incompletos | Omitir placa o capacidades y comprobar rechazo sin escritura. |
| CA-05 | Acceso sin permisos | Registrar con otro rol y comprobar rechazo. |

## 5. Reglas, datos e integraciones

- La placa debe ser única en el módulo. Si ya existe, se rechaza con `409 Conflict`.
- Los límites de peso, volumen y paquetes deben ser mayores que cero. Si alguno es inválido, se responde `400 Bad Request`.
- La furgoneta se crea siempre con estado `DISPONIBLE`.
- Un usuario sin el rol `GESTOR_DESPACHO` recibe `403 Forbidden`.

### Entradas

- Placa de la furgoneta.
- Límite de peso en kg.
- Límite de volumen en m³.
- Máximo de paquetes en ruta.
- Identidad y roles obtenidos del JWT.

### Salidas

- Furgoneta creada con identificador, placa, límites y estado `DISPONIBLE`.
- Registro de auditoría.

### Integraciones

- F-06 consume las furgonetas `DISPONIBLE` para las asignaciones diarias.
- La ruta, cuerpos y códigos se rigen por [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md) [cite: 2].

### Contrato propietario

La operación de referencia es `POST /api/v1/furgonetas`, definida en [Operación §4.1](../../integraciones/api-contract-operacion-reparto.md#41-repartidores-y-furgonetas). Las convenciones de errores pertenecen al [contrato externo §3.5](../../integraciones/api-contract.md#35-errores). Los cuerpos, encabezados y respuestas definitivos se mantienen allí; no se crea un contrato paralelo.

## 6. Criterios de aceptación

### CA-01. Registro exitoso

- **DADO** una furgoneta con placa "ABC-123", 500 kg, 4.0 m³ y máximo de 80 paquetes.
- **CUANDO** el Gestor confirma el registro.
- **ENTONCES** el sistema la guarda en estado `DISPONIBLE` con esos límites y registra la auditoría.

### CA-02. Placa duplicada

- **DADO** una furgoneta existente con placa "ABC-123".
- **CUANDO** se intenta registrar otra con la misma placa.
- **ENTONCES** el sistema responde `409 Conflict` sin persistir el duplicado.

### CA-03. Límites inválidos

- **DADO** un formulario con peso igual a cero o negativo.
- **CUANDO** el Gestor intenta confirmar el registro.
- **ENTONCES** el sistema responde `400 Bad Request` detallando los campos inválidos.

### CA-04. Datos incompletos

- **DADO** un formulario sin placa o sin alguno de los límites.
- **CUANDO** el Gestor intenta confirmar.
- **ENTONCES** el sistema responde `400 Bad Request`.

### CA-05. Acceso sin permisos

- **DADO** un usuario sin rol `GESTOR_DESPACHO`.
- **CUANDO** intenta registrar una furgoneta.
- **ENTONCES** el sistema responde `403 Forbidden`.

## 7. UI, backend y requisitos no funcionales

- UI: interacción, estados y criterios CUI en [ui.md](./ui.md); reutilización de los [componentes compartidos](../../disenio/componentes-react.md).
- Backend: Registrar una furgoneta disponible con placa única y capacidades positivas. Propiedad local de `furgonetas`; no acceder a la base de Gestión.
- Requisitos no funcionales: Confirmar consistencia de datos, permisos y auditoría; comprobar cancelación, repetición y concurrencia cuando afecten el resultado.
- Seguridad y datos: no mostrar credenciales, tokens ni errores técnicos en la interfaz; la habilitación visual no reemplaza la autorización del backend.
- Pendiente funcional P-01: Ratificar los DTO de Operación y el tratamiento de normalización/precisión en el contrato; conservar los criterios originales de alta y la propiedad de datos de Operación.
- Responsable de P-01: Rhamses coordina con Arquitectura; la revisión afecta los criterios indicados y debe resolverse antes de declarar la aceptación completa.
- Las implementaciones existentes se referencian en [evidence.md](./evidence.md). Su existencia no reemplaza la comprobación individual de los criterios conservados.

## 8. Verificación y completitud

| Criterio | Comprobación prevista | Nivel y preparación |
|---|---|---|
| CA-01 | Registrar ABC-123 con 500 kg, 4 m³ y 80 paquetes y comprobar estado y auditoría. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-02 | Repetir la placa y comprobar conflicto sin otra furgoneta. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-03 | Enviar cero y negativos en las capacidades y comprobar errores de campo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-04 | Omitir placa o capacidades y comprobar rechazo sin escritura. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |
| CA-05 | Registrar con otro rol y comprobar rechazo. | Integración backend y recorrido UI; simulación identificada si la dependencia no existe |

- [ ] Todos los criterios y CUI cuentan con resultados por caso en [evidence.md](./evidence.md).
- [ ] P-01 está resuelto en los documentos propietarios y revisado por el equipo.
- [ ] Los datos, el contrato y la implementación son consistentes.
- [ ] Las dependencias simuladas y la integración real pendiente se identifican expresamente.

## 9. Referencias

- [cite: 1] [funcionalidades/F-05-GestionRepartidoresVehiculos.md](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md), RF-02 y CA-08 a CA-09.
- [cite: 2] [integraciones/api-contract-operacion-reparto.md](../../integraciones/api-contract-operacion-reparto.md).
- [Flujo SDD](../../plantillas/sdd/README.md) y [reglas del repositorio](../../AGENTS.md#37-especificaciones-atómicas).
- [Modelo de datos, Operación §3.2](../../arquitectura/modelo-datos.md) y [Seguridad §8.4](../../integraciones/api-contract.md#84-creación-y-vinculación-de-un-usuario-repartidor).
- Archivos de trabajo: [UI](./ui.md), [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
