# ES-F06-06: Reservar capacidad para una asignación

**Funcionalidad padre:** [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md).

**Responsable funcional original:** Luis Alfonso. **Implementación asumida:** Kevin Rhamses Bohorquez, por solicitud del equipo usuario.

**Estado:** Implementado y verificado localmente; aceptación integrada pendiente.

**UI:** No aplica: API interna consumida por Gestión; sus efectos visibles se cubren en ES-F06-02 y ES-F06-04.

## 1. Contexto y objetivo

Reservar capacidad para una asignación en Operación de Reparto, como parte de Soporte a CA-09, CA-11 y CA-14; F-02 de F-06 [cite: 1].

## 2. Alcance

Confirmar las tres dimensiones bajo bloqueo compatible con F-05. Una clave UUID de asignación identifica contenido y resultado durable, aun después de liberar. No crear dos reservas activas del mismo despacho ni sobrepasar límites concurrentemente.

Fuera de alcance: login, CRUD F-05, decisiones comerciales, asignación canónica F-02 y resolución de entregas F-03.

## 3. Actor, precondiciones y resultados

- Actor: Gestión con JWT de servicio, audiencia api-despacho y scope de la operación.
- Propietario de datos: Operación; zonas se consultan por HTTP, nunca mediante tablas compartidas.
- Resultado: respuesta contractual confirmada o rechazo sin efectos parciales; errores no se transforman en éxito.

## 4. Flujo principal y alternativas

1. Validar identidad y parámetros antes de consultar datos protegidos.
2. Aplicar el comportamiento de §2 y comprobar las dependencias requeridas.
3. Confirmar mutación y auditoría juntas cuando corresponda; las lecturas no mutan estados.
4. Devolver el resultado de Operación y conservar los datos anteriores ante rechazo.

## 5. Reglas, datos e integraciones

Confirmar las tres dimensiones bajo bloqueo compatible con F-05. Una clave UUID de asignación identifica contenido y resultado durable, aun después de liberar. No crear dos reservas activas del mismo despacho ni sobrepasar límites concurrentemente.

Los DTO, encabezados, scopes, rutas y errores se definen una sola vez en Operación §5.1 [cite: 2]. Los identificadores reales son UUID. Las credenciales no pertenecen a los documentos ni a las capturas.

## 6. Criterios de aceptación

### CA-01. Reserva válida

- **DADO** jornada apta y capacidad suficiente.
- **CUANDO** Gestión solicita reserva con clave UUID.
- **ENTONCES** se persiste una reserva activa y se devuelve CONFIRMADA con remanente.

### CA-02. Capacidad insuficiente

- **DADO** peso, volumen o paquetes exceden remanente.
- **CUANDO** se solicita reservar.
- **ENTONCES** se responde 422 con las dimensiones afectadas sin cambios.

### CA-03. Repetición y conflicto de clave

- **DADO** clave previamente persistida.
- **CUANDO** se repite el mismo contenido o se cambia.
- **ENTONCES** el mismo contenido devuelve resultado original; otro contenido responde 409.

### CA-04. Reserva anterior y concurrencia

- **DADO** reserva activa de ese despacho u operaciones simultáneas.
- **CUANDO** se solicita una asignación nueva.
- **ENTONCES** se rechaza la anterior activa y nunca se sobrerreserva.

### CA-05. Permiso técnico

- **DADO** JWT ajeno, humano o sin scope.
- **CUANDO** se invoca la ruta privada.
- **ENTONCES** se deniega antes de modificar datos y el Gateway no publica esa ruta.

## 7. UI, backend y requisitos no funcionales

- UI: No aplica; no hay pantalla para ejecutar comandos técnicos.
- Backend: jornadas, reservas y proyecciones locales; consistencia con F-05 y contratos F-02/F-04.
- Rendimiento: disponibilidad objetivo menor de 200 ms, pendiente de medir con carga y entorno identificados; no se acredita por compilar.
- Seguridad: sin SQL, credenciales o datos personales en errores; autorización obligatoria también en servidor.
- Integración externa: Seguridad real pendiente de despliegue y concesión de scopes.

## 8. Verificación y completitud

| Criterio | Comprobación | Escenario |
|---|---|---|
| CA-01 | Reserva válida | T-03 y T-04; datos sintéticos |
| CA-02 | Capacidad insuficiente | T-03 y T-04; datos sintéticos |
| CA-03 | Repetición y conflicto de clave | T-03 y T-04; datos sintéticos |
| CA-04 | Reserva anterior y concurrencia | T-03 y T-04; datos sintéticos |
| CA-05 | Permiso técnico | T-03 y T-04; datos sintéticos |

- [ ] Todos los criterios tienen evidencia ejecutada y revisada.
- [ ] Integración con dependencias reales y revisión humana completadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), Soporte a CA-09, CA-11 y CA-14; F-02 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#51-gestión-consulta-y-reserva-capacidad-en-operación) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
