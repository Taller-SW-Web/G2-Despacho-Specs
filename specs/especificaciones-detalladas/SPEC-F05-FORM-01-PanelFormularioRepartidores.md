# Especificación SPEC-F05-FORM-01: Panel y Formulario de Administración de Repartidores

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-05: Monitoreo de Flota, Operadores y Capacidad Diaria  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Flota / Administrador  

---

## 1. Contexto

Para que el sistema de despacho cuente con personal habilitado para transportar mercancías, se requiere un registro maestro de repartidores. Esta vista permite al Gestor de Flota dar de alta a nuevos conductores, mantener sus datos de contacto y licencias actualizados, coordinar su vinculación con el módulo de Seguridad y Usuarios para la emisión de credenciales, y gestionar su baja lógica sin romper la integridad histórica de las entregas pasadas.

---

## 2. Propósito

Proveer una interfaz de usuario web responsive para listar, filtrar, registrar, editar y dar de baja lógica a los repartidores de la empresa, supervisando el estado de vinculación de su cuenta de usuario con el módulo de Seguridad.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Tabla paginada de repartidores con filtros por estado de registro (`ACTIVO`, `INACTIVO`), turno habitual y estado de vinculación de usuario (`VINCULADO`, `PENDIENTE`).
- Modal de alta y edición de repartidor con los campos:
  - Nombres y Apellidos.
  - Documento Nacional de Identidad (DNI) con validación de 8 dígitos y unicidad.
  - Teléfono móvil y correo electrónico corporativo.
  - Número de licencia de conducir (brevete) y fecha de vencimiento.
  - Turno habitual de trabajo (Mañana, Tarde, Completo).
- Integración de disparo automático de alta de usuario hacia Seguridad (`SPEC-F05-PROC-03`).
- Botón de acción para reintentar la vinculación si el servicio de Seguridad estuvo temporalmente inaccesible.
- Acción de baja lógica (`DELETE /api/v1/repartidores/{id}`):
  - Verifica que el chofer no tenga despachos en curso (`ASIGNADO` o `EN_CAMINO`). Si tiene pendientes, bloquea la acción con HTTP `409 Conflict`.
  - Pasa el estado a `INACTIVO` preservando todo su historial.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Usuario autenticado con rol `GESTOR_FLOTA` o `ADMIN`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/repartidores` | Listar choferes con filtros y paginación. |
| `POST /api/v1/repartidores` | Crear chofer y solicitar cuenta a Seguridad. |
| `DELETE /api/v1/repartidores/{id}` | Aplicar baja lógica si no tiene cargas activas. |
| `SPEC-F05-PROC-03` | Proceso de vinculación de identidades con Seguridad y Usuarios. |

### 4.3. Resultados
- Repartidor registrado en estado `ACTIVO`, en `FUERA_DE_TURNO` y con usuario de acceso coordinado.
- Exclusión inmediata de choferes dados de baja para nuevas jornadas de transporte.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Registro y unicidad de documentos
El formulario DEBE validar que los documentos de identidad no se encuentren duplicados.

#### CA-01. Registro exitoso con vinculación inmediata
- **DADO** que el gestor ingresa DNI "45871234" no registrado, nombres "Juan Pérez", brevete "Q45871234" y correo válido.
- **CUANDO** confirma el formulario.
- **ENTONCES** el backend valida unicidad, persiste el chofer en `ACTIVO`, solicita la creación del usuario en Seguridad, responde `201 Created` y el chofer aparece como `VINCULADO`.

#### CA-02. Rechazo por DNI duplicado
- **DADO** un DNI que ya pertenece a otro repartidor activo o inactivo.
- **CUANDO** se intenta guardar.
- **ENTONCES** el sistema responde `409 Conflict` con el mensaje *"Ya existe un repartidor registrado con el DNI indicado"* y resalta el campo.

### RF-02. Baja lógica e integridad operativa
El sistema DEBE proteger las operaciones en curso antes de admitir una baja.

#### CA-03. Baja lógica exitosa sin despachos en curso
- **DADO** un repartidor sin despachos activos en la fecha.
- **CUANDO** el gestor pulsa "Dar de baja".
- **ENTONCES** el estado cambia a `INACTIVO`, se conservan sus registros históricos y el chofer ya no puede ser seleccionado para jornadas diarias.

#### CA-04. Bloqueo de baja con despachos en curso
- **DADO** un chofer que tiene 2 despachos en `ASIGNADO` o `EN_CAMINO`.
- **CUANDO** el gestor intenta darle de baja.
- **ENTONCES** el backend rechaza la petición con `409 Conflict` informando *"No se puede dar de baja a un repartidor con despachos en curso. Reasigne o culmine los paquetes previamente"*.

---

## 6. Frontend

### 6.1. Componentes
- **`DriversManagementPage`**: Layout general con barra de búsqueda, selector de estado y botón *"Nuevo Repartidor"*.
- **`DriverFormModal`**: Diálogo modal con validación reactiva de DNI (regex de 8 dígitos numéricos).
- **`LinkStatusBadge`**: Chip visual: verde (*"Vinculado"*), ámbar (*"Pendiente de vinculación"* con botón de reintento).
- **`DeactivateDriverDialog`**: Diálogo de confirmación para baja lógica.

---

## 7. Backend (Contrato consumido)

- **Ruta creación:** `POST /api/v1/repartidores`
- **Cuerpo:**
```json
{
  "nombres": "Juan",
  "apellidos": "Pérez Gómez",
  "dni": "45871234",
  "telefono": "+51987654321",
  "email": "juan.perez@empresa.com",
  "numeroBrevete": "Q45871234",
  "turnoHabitual": "MAÑANA"
}
```
- **Respuesta Exitosa (`201 Created`):** Retorna el repartidor con `idRepartidor`, estado `ACTIVO`, estado operativo `FUERA_DE_TURNO` y estado de vinculación.

---

## 8. Requisitos no funcionales

- **Integridad Referencial:** Prohibición absoluta de borrado físico (`DELETE SQL`); todas las bajas son lógicas (`is_activo = false`).
- **Seguridad:** Acceso restringido a roles `GESTOR_FLOTA` y `ADMIN`.

---

## 9. Fuera de alcance

- Gestión de nóminas, pagos o contratos laborales (fuera del ERP de despacho).
- Asignación de vehículos a repartidores (se realiza en `SPEC-F05-FORM-03`).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | UI Form Test | RTL / Vitest | Registro válido envía POST y muestra fila con badge `VINCULADO`. |
| CA-02 | Uniqueness Test | MockMvc | DNI duplicado arroja HTTP `409 Conflict`. |
| CA-03 | Soft Delete Test | `@DataJpaTest` | `delete` actualiza campo `activo = false` sin borrar fila. |
| CA-04 | Active Shipments Guard | JUnit 5 | Chofer con despachos en curso rechaza baja con código `409`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El CRUD de repartidores garantice unicidad de DNI y baja lógica estricta.
2. Se prevenga la baja de operadores con paquetes en custodia.
3. Se soporte el reintento visual de vinculación con Seguridad.
