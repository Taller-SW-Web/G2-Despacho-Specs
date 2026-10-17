# ES-F06-04: Calcular ocupación y estado operativo

**Funcionalidad padre:** [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md).

**Responsable funcional original:** Luis Alfonso. **Implementación asumida:** Kevin Rhamses Bohorquez, por solicitud del equipo usuario.

**Estado:** Implementado y verificado localmente; aceptación integrada pendiente.

**UI:** Aplica; interfaz administrativa de jornadas y monitoreo.

## 1. Contexto y objetivo

Calcular ocupación y estado operativo en Operación de Reparto, como parte de CA-11, CA-14 y CA-15 de F-06 [cite: 1].

## 2. Alcance

Sumar reservas ACTIVA sin deducir liberaciones pendientes ni sumar filas de despachos. Derivar con prioridad FUERA_DE_TURNO, SATURADO, EN_RUTA y DISPONIBLE. Un despacho FALLIDO sigue ocupando mientras su reserva esté activa. La liberación no reabre una jornada cerrada.

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

Sumar reservas ACTIVA sin deducir liberaciones pendientes ni sumar filas de despachos. Derivar con prioridad FUERA_DE_TURNO, SATURADO, EN_RUTA y DISPONIBLE. Un despacho FALLIDO sigue ocupando mientras su reserva esté activa. La liberación no reabre una jornada cerrada.

Los DTO, encabezados, scopes, rutas y errores se definen una sola vez en Operación §4.2 [cite: 2]. Los identificadores reales son UUID. Las credenciales no pertenecen a los documentos ni a las capturas.

## 6. Criterios de aceptación

### CA-01. Cambio de estado derivado

- **DADO** jornada activa con y sin un despacho EN_CAMINO.
- **CUANDO** se actualiza la proyección y se consulta.
- **ENTONCES** cambia entre EN_RUTA y DISPONIBLE mientras no esté saturado.

### CA-02. Saturación multidimensional

- **DADO** 20 de 80 paquetes y el límite de peso o volumen alcanzado.
- **CUANDO** se calcula el estado.
- **ENTONCES** se obtiene SATURADO y se excluye de disponibilidad.

### CA-03. Retorno físico y liberación

- **DADO** reserva activa de paquete fallido.
- **CUANDO** F-04 confirma la liberación original.
- **ENTONCES** baja la ocupación una sola vez; antes de la confirmación sigue contando y una jornada cerrada permanece cerrada.

## 7. UI, backend y requisitos no funcionales

- UI: [ui.md](./ui.md), con CR-10/11/14 y componentes administrativos compartidos.
- Backend: jornadas, reservas y proyecciones locales; consistencia con F-05 y contratos F-02/F-04.
- Rendimiento: disponibilidad objetivo menor de 200 ms, pendiente de medir con carga y entorno identificados; no se acredita por compilar.
- Seguridad: sin SQL, credenciales o datos personales en errores; autorización obligatoria también en servidor.
- Integración externa: Seguridad real pendiente de despliegue y concesión de scopes.

## 8. Verificación y completitud

| Criterio | Comprobación | Escenario |
|---|---|---|
| CA-01 | Cambio de estado derivado | T-03 y T-04; datos sintéticos |
| CA-02 | Saturación multidimensional | T-03 y T-04; datos sintéticos |
| CA-03 | Retorno físico y liberación | T-03 y T-04; datos sintéticos |

- [ ] Todos los criterios tienen evidencia ejecutada y revisada.
- [ ] Integración con dependencias reales y revisión humana completadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), CA-11, CA-14 y CA-15 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#42-jornadas-y-monitoreo) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
