# ES-F06-01: Abrir una jornada operativa

**Funcionalidad padre:** [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md).

**Responsable funcional original:** Luis Alfonso. **Implementación asumida:** Kevin Rhamses Bohorquez, por solicitud del equipo usuario.

**Estado:** En implementación; aceptación pendiente.

**UI:** Aplica; interfaz administrativa de jornadas y monitoreo.

## 1. Contexto y objetivo

Abrir una jornada operativa en Operación de Reparto, como parte de CA-01 a CA-06 de F-06 [cite: 1].

## 2. Alcance

Crear la jornada de hoy en America/Bogota con repartidor activo/vinculado, furgoneta disponible y zona activa comprobada en Gestión. Guardar las capacidades como instantánea; impedir dos jornadas activas del mismo recurso, incluso de fechas distintas. Rechazar carga histórica aún reservada antes de reutilizar recursos.

Fuera de alcance: login, CRUD F-05, decisiones comerciales, asignación canónica F-02 y resolución de entregas F-03.

## 3. Actor, precondiciones y resultados

- Actor: Gestor con JWT de acceso y GESTOR_DESPACHO; cierre propio conforme al contrato.
- Propietario de datos: Operación; zonas se consultan por HTTP, nunca mediante tablas compartidas.
- Resultado: respuesta contractual confirmada o rechazo sin efectos parciales; errores no se transforman en éxito.

## 4. Flujo principal y alternativas

1. Validar identidad y parámetros antes de consultar datos protegidos.
2. Aplicar el comportamiento de §2 y comprobar las dependencias requeridas.
3. Confirmar mutación y auditoría juntas cuando corresponda; las lecturas no mutan estados.
4. Devolver el resultado de Operación y conservar los datos anteriores ante rechazo.

## 5. Reglas, datos e integraciones

Crear la jornada de hoy en America/Bogota con repartidor activo/vinculado, furgoneta disponible y zona activa comprobada en Gestión. Guardar las capacidades como instantánea; impedir dos jornadas activas del mismo recurso, incluso de fechas distintas. Rechazar carga histórica aún reservada antes de reutilizar recursos.

Los DTO, encabezados, scopes, rutas y errores se definen una sola vez en Operación §4.2 [cite: 2]. Los identificadores reales son UUID. Las credenciales no pertenecen a los documentos ni a las capturas.

## 6. Criterios de aceptación

### CA-01. Apertura válida

- **DADO** recursos aptos y zona activa.
- **CUANDO** el Gestor confirma la apertura.
- **ENTONCES** se crea una jornada activa con sus capacidades y auditoría; aparece disponible.

### CA-02. Repartidor ocupado

- **DADO** una jornada activa del repartidor.
- **CUANDO** se intenta otra apertura.
- **ENTONCES** se responde 409 sin cambios.

### CA-03. Perfil no habilitado

- **DADO** un perfil inactivo o pendiente.
- **CUANDO** se solicita abrir jornada.
- **ENTONCES** se responde 422 sin crear jornada.

### CA-04. Furgoneta no disponible

- **DADO** vehículo en mantenimiento, retirado, ocupado o con carga histórica pendiente.
- **CUANDO** se solicita abrir jornada.
- **ENTONCES** se responde 409 sin cambios.

### CA-05. Zona o fecha no aptas

- **DADO** zona inexistente/inactiva o fecha distinta de hoy.
- **CUANDO** se solicita abrir jornada.
- **ENTONCES** se responde 422; una caída de Gestión responde 503, sin asumir zona activa.

### CA-06. Acceso no autorizado

- **DADO** identidad sin permiso administrativo.
- **CUANDO** se solicita abrir jornada.
- **ENTONCES** se responde 401/403 sin efectos.

## 7. UI, backend y requisitos no funcionales

- UI: [ui.md](./ui.md), con CR-10/11/14 y componentes administrativos compartidos.
- Backend: jornadas, reservas y proyecciones locales; consistencia con F-05 y contratos F-02/F-04.
- Rendimiento: disponibilidad objetivo menor de 200 ms, pendiente de medir con carga y entorno identificados; no se acredita por compilar.
- Seguridad: sin SQL, credenciales o datos personales en errores; autorización obligatoria también en servidor.
- Integración externa: Seguridad real pendiente de despliegue y concesión de scopes.

## 8. Verificación y completitud

| Criterio | Comprobación | Escenario |
|---|---|---|
| CA-01 | Apertura válida | T-03 y T-04; datos sintéticos |
| CA-02 | Repartidor ocupado | T-03 y T-04; datos sintéticos |
| CA-03 | Perfil no habilitado | T-03 y T-04; datos sintéticos |
| CA-04 | Furgoneta no disponible | T-03 y T-04; datos sintéticos |
| CA-05 | Zona o fecha no aptas | T-03 y T-04; datos sintéticos |
| CA-06 | Acceso no autorizado | T-03 y T-04; datos sintéticos |

- [ ] Todos los criterios tienen evidencia ejecutada y revisada.
- [ ] Integración con dependencias reales y revisión humana completadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), CA-01 a CA-06 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#42-jornadas-y-monitoreo) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
