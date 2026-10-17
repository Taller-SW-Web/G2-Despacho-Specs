# ES-F06-05: Cerrar una jornada sin despachos en curso

**Funcionalidad padre:** [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md).

**Responsable funcional original:** Luis Alfonso. **Implementación asumida:** Kevin Rhamses Bohorquez, por solicitud del equipo usuario.

**Estado:** Implementado y verificado localmente; aceptación integrada pendiente.

**UI:** Aplica; interfaz administrativa de jornadas y monitoreo.

## 1. Contexto y objetivo

Cerrar una jornada sin despachos en curso en Operación de Reparto, como parte de CA-12 y CA-13 de F-06 [cite: 1].

## 2. Alcance

Cerrar y auditar atómicamente. No borrar reservas ni proyecciones. Una reserva activa aún sin proyección terminal bloquea el cierre para no interrumpir una asignación F-02 en curso. Una jornada ya cerrada devuelve el mismo resultado sin otra auditoría. F-03 debe resolver primero ASIGNADO/EN_CAMINO como NO_INTENTADO; F-06 nunca realiza esa conversión por su cuenta.

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

Cerrar y auditar atómicamente. No borrar reservas ni proyecciones. Una reserva activa aún sin proyección terminal bloquea el cierre para no interrumpir una asignación F-02 en curso. Una jornada ya cerrada devuelve el mismo resultado sin otra auditoría. F-03 debe resolver primero ASIGNADO/EN_CAMINO como NO_INTENTADO; F-06 nunca realiza esa conversión por su cuenta.

Los DTO, encabezados, scopes, rutas y errores se definen una sola vez en Operación §4.2 [cite: 2]. Los identificadores reales son UUID. Las credenciales no pertenecen a los documentos ni a las capturas.

## 6. Criterios de aceptación

### CA-01. Cierre seguro e idempotente

- **DADO** jornada sin ASIGNADO ni EN_CAMINO.
- **CUANDO** el Gestor confirma cerrar o repite el cierre.
- **ENTONCES** se conserva historia, fecha y auditoría única; el perfil queda fuera de turno y no admite nuevas reservas.

### CA-02. Pendientes de operación

- **DADO** jornada con despachos ASIGNADO o EN_CAMINO.
- **CUANDO** se solicita cierre administrativo.
- **ENTONCES** se responde 409 sin cerrar ni liberar carga.

### CA-03. Propiedad del repartidor

- **DADO** JWT de acceso con perfil vinculado.
- **CUANDO** el repartidor solicita cerrar su jornada.
- **ENTONCES** solo se cierra su jornada sin pendientes; no puede actuar sobre otro perfil.

## 7. UI, backend y requisitos no funcionales

- UI: [ui.md](./ui.md), con CR-10/11/14 y componentes administrativos compartidos.
- Backend: jornadas, reservas y proyecciones locales; consistencia con F-05 y contratos F-02/F-04.
- Rendimiento: disponibilidad objetivo menor de 200 ms, pendiente de medir con carga y entorno identificados; no se acredita por compilar.
- Seguridad: sin SQL, credenciales o datos personales en errores; autorización obligatoria también en servidor.
- Integración externa: Seguridad real pendiente de despliegue y concesión de scopes.

## 8. Verificación y completitud

| Criterio | Comprobación | Escenario |
|---|---|---|
| CA-01 | Cierre seguro e idempotente | T-03 y T-04; datos sintéticos |
| CA-02 | Pendientes de operación | T-03 y T-04; datos sintéticos |
| CA-03 | Propiedad del repartidor | T-03 y T-04; datos sintéticos |

- [ ] Todos los criterios tienen evidencia ejecutada y revisada.
- [ ] Integración con dependencias reales y revisión humana completadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), CA-12 y CA-13 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#42-jornadas-y-monitoreo) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
