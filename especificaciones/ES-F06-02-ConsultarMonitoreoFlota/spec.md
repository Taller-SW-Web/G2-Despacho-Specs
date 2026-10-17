# ES-F06-02: Consultar el monitoreo de flota

**Funcionalidad padre:** [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md).

**Responsable funcional original:** Luis Alfonso. **Implementación asumida:** Kevin Rhamses Bohorquez, por solicitud del equipo usuario.

**Estado:** En implementación; aceptación pendiente.

**UI:** Aplica; interfaz administrativa de jornadas y monitoreo.

## 1. Contexto y objetivo

Consultar el monitoreo de flota en Operación de Reparto, como parte de CA-07 y CA-08 de F-06 [cite: 1].

## 2. Alcance

Mostrar repartidores activos, jornada, zona y tres métricas con actualización cada 30 segundos mientras la página sea visible. Resumen global antes de paginar y filtrar por estado; filtros y página en URL. Conservar datos autorizados con aviso ante fallo de refresco y bloquear mutaciones hasta recuperar.

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

Mostrar repartidores activos, jornada, zona y tres métricas con actualización cada 30 segundos mientras la página sea visible. Resumen global antes de paginar y filtrar por estado; filtros y página en URL. Conservar datos autorizados con aviso ante fallo de refresco y bloquear mutaciones hasta recuperar.

Los DTO, encabezados, scopes, rutas y errores se definen una sola vez en Operación §4.2 [cite: 2]. Los identificadores reales son UUID. Las credenciales no pertenecen a los documentos ni a las capturas.

## 6. Criterios de aceptación

### CA-01. Saturación visible

- **DADO** una jornada al 100 por ciento de cualquiera de sus límites.
- **CUANDO** se consulta el tablero.
- **ENTONCES** se presenta SATURADO y valores reales; verde por debajo de 70, ámbar desde 70 y rojo desde 100 sin clasificar después de redondear.

### CA-02. Resumen global y paginación

- **DADO** más de 50 perfiles con estados distintos.
- **CUANDO** se consulta otra página o se filtra.
- **ENTONCES** los totales corresponden al conjunto completo y los filtros no fabrican datos.

### CA-03. Recuperación y permisos

- **DADO** datos previos confirmados y un fallo de refresco o una pérdida de autorización.
- **CUANDO** se actualiza el tablero.
- **ENTONCES** un fallo conserva datos marcados desactualizados; 401/403 retira datos y formularios.

## 7. UI, backend y requisitos no funcionales

- UI: [ui.md](./ui.md), con CR-10/11/14 y componentes administrativos compartidos.
- Backend: jornadas, reservas y proyecciones locales; consistencia con F-05 y contratos F-02/F-04.
- Rendimiento: disponibilidad objetivo menor de 200 ms, pendiente de medir con carga y entorno identificados; no se acredita por compilar.
- Seguridad: sin SQL, credenciales o datos personales en errores; autorización obligatoria también en servidor.
- Integración externa: Seguridad real pendiente de despliegue y concesión de scopes.

## 8. Verificación y completitud

| Criterio | Comprobación | Escenario |
|---|---|---|
| CA-01 | Saturación visible | T-03 y T-04; datos sintéticos |
| CA-02 | Resumen global y paginación | T-03 y T-04; datos sintéticos |
| CA-03 | Recuperación y permisos | T-03 y T-04; datos sintéticos |

- [ ] Todos los criterios tienen evidencia ejecutada y revisada.
- [ ] Integración con dependencias reales y revisión humana completadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), CA-07 y CA-08 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#42-jornadas-y-monitoreo) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
