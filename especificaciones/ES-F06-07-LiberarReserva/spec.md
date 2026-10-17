# ES-F06-07: Liberar una reserva confirmada

**Funcionalidad padre:** [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md).

**Responsable funcional original:** Luis Alfonso. **Implementación asumida:** Kevin Rhamses Bohorquez, por solicitud del equipo usuario.

**Estado:** Implementado y verificado localmente; aceptación integrada pendiente.

**UI:** No aplica: API interna consumida por Gestión; sus efectos visibles se cubren en ES-F06-02 y ES-F06-04.

## 1. Contexto y objetivo

Liberar una reserva confirmada en Operación de Reparto, como parte de Soporte a CA-15; F-02/F-04 de F-06 [cite: 1].

## 2. Alcance

Liberar exclusivamente la reserva y despacho indicados, conservando motivo e instante de la primera liberación. Compensación, recepción, cancelación, entrega y reasignación comparten la misma regla idempotente. No reabrir jornada ni liberar otra referencia.

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

Liberar exclusivamente la reserva y despacho indicados, conservando motivo e instante de la primera liberación. Compensación, recepción, cancelación, entrega y reasignación comparten la misma regla idempotente. No reabrir jornada ni liberar otra referencia.

Los DTO, encabezados, scopes, rutas y errores se definen una sola vez en Operación §5.2 [cite: 2]. Los identificadores reales son UUID. Las credenciales no pertenecen a los documentos ni a las capturas.

## 6. Criterios de aceptación

### CA-01. Liberación válida

- **DADO** reserva activa del despacho comunicado.
- **CUANDO** Gestión confirma liberar.
- **ENTONCES** se marca LIBERADA con motivo e instante y deja de sumar ocupación.

### CA-02. Repetición

- **DADO** reserva ya liberada.
- **CUANDO** se solicita otra liberación incluso con motivo diferente.
- **ENTONCES** se devuelve la primera liberación sin cambiar datos ni descontar dos veces.

### CA-03. Referencia incorrecta

- **DADO** reserva inexistente o de otro despacho.
- **CUANDO** se solicita liberar.
- **ENTONCES** se responde 404 o 409 sin tocar otras reservas.

### CA-04. Autorización e indisponibilidad

- **DADO** token sin permiso o caída de datos.
- **CUANDO** se solicita liberar.
- **ENTONCES** se responde 401/403/503 sin afirmar éxito.

## 7. UI, backend y requisitos no funcionales

- UI: No aplica; no hay pantalla para ejecutar comandos técnicos.
- Backend: jornadas, reservas y proyecciones locales; consistencia con F-05 y contratos F-02/F-04.
- Rendimiento: disponibilidad objetivo menor de 200 ms, pendiente de medir con carga y entorno identificados; no se acredita por compilar.
- Seguridad: sin SQL, credenciales o datos personales en errores; autorización obligatoria también en servidor.
- Integración externa: Seguridad real pendiente de despliegue y concesión de scopes.

## 8. Verificación y completitud

| Criterio | Comprobación | Escenario |
|---|---|---|
| CA-01 | Liberación válida | T-03 y T-04; datos sintéticos |
| CA-02 | Repetición | T-03 y T-04; datos sintéticos |
| CA-03 | Referencia incorrecta | T-03 y T-04; datos sintéticos |
| CA-04 | Autorización e indisponibilidad | T-03 y T-04; datos sintéticos |

- [ ] Todos los criterios tienen evidencia ejecutada y revisada.
- [ ] Integración con dependencias reales y revisión humana completadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), Soporte a CA-15; F-02/F-04 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#52-gestión-libera-una-reserva-en-operación) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
