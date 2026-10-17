# ES-F06-08: Actualizar la proyección operativa del despacho

**Funcionalidad padre:** [F-06](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md).

**Responsable funcional original:** Luis Alfonso. **Implementación asumida:** Kevin Rhamses Bohorquez, por solicitud del equipo usuario.

**Estado:** En implementación; aceptación pendiente.

**UI:** No aplica: API interna consumida por Gestión; sus efectos visibles se cubren en ES-F06-02 y ES-F06-04.

## 1. Contexto y objetivo

Actualizar la proyección operativa del despacho en Operación de Reparto, como parte de Soporte a CA-11 y cierre; F-02/F-03 de F-06 [cite: 1].

## 2. Alcance

Recibir la versión canónica confirmada por Gestión; conservar destinatario, destino, jornada y reserva para los consumidores de campo. Versiones antiguas/repetidas no reemplazan datos. Validar que la reserva pertenece al despacho y jornada, sin convertir la proyección en dueño del despacho.

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

Recibir la versión canónica confirmada por Gestión; conservar destinatario, destino, jornada y reserva para los consumidores de campo. Versiones antiguas/repetidas no reemplazan datos. Validar que la reserva pertenece al despacho y jornada, sin convertir la proyección en dueño del despacho.

Los DTO, encabezados, scopes, rutas y errores se definen una sola vez en Operación §5.3 [cite: 2]. Los identificadores reales son UUID. Las credenciales no pertenecen a los documentos ni a las capturas.

## 6. Criterios de aceptación

### CA-01. Versión nueva válida

- **DADO** reserva y jornada que corresponden al despacho.
- **CUANDO** Gestión envía proyección de versión superior.
- **ENTONCES** se actualizan los datos locales y se recalcula el estado en la siguiente consulta.

### CA-02. Versión antigua o repetida

- **DADO** proyección ya persistida.
- **CUANDO** llega versión igual o menor.
- **ENTONCES** se confirma sin sobrescribir la versión vigente.

### CA-03. Referencias incompatibles

- **DADO** reserva o jornada ajena al despacho.
- **CUANDO** llega una proyección.
- **ENTONCES** se responde 409 sin reasignar referencias.

### CA-04. Autorización y datos privados

- **DADO** petición sin scope o con payload inválido.
- **CUANDO** se invoca la ruta interna.
- **ENTONCES** se rechaza sin exponer datos personales ni publicar la ruta en el Gateway.

## 7. UI, backend y requisitos no funcionales

- UI: No aplica; no hay pantalla para ejecutar comandos técnicos.
- Backend: jornadas, reservas y proyecciones locales; consistencia con F-05 y contratos F-02/F-04.
- Rendimiento: disponibilidad objetivo menor de 200 ms, pendiente de medir con carga y entorno identificados; no se acredita por compilar.
- Seguridad: sin SQL, credenciales o datos personales en errores; autorización obligatoria también en servidor.
- Integración externa: Seguridad real pendiente de despliegue y concesión de scopes.

## 8. Verificación y completitud

| Criterio | Comprobación | Escenario |
|---|---|---|
| CA-01 | Versión nueva válida | T-03 y T-04; datos sintéticos |
| CA-02 | Versión antigua o repetida | T-03 y T-04; datos sintéticos |
| CA-03 | Referencias incompatibles | T-03 y T-04; datos sintéticos |
| CA-04 | Autorización y datos privados | T-03 y T-04; datos sintéticos |

- [ ] Todos los criterios tienen evidencia ejecutada y revisada.
- [ ] Integración con dependencias reales y revisión humana completadas.

## 9. Referencias

1. [Funcionalidad padre](../../funcionalidades/F-06-DisponibilidadCapacidadDiaria.md), Soporte a CA-11 y cierre; F-02/F-03 [cite: 1].
2. [Contrato de Operación](../../integraciones/api-contract-operacion-reparto.md#53-gestión-comunica-el-estado-confirmado-a-operación) [cite: 2].
3. [Modelo de datos](../../arquitectura/modelo-datos.md) y [componentes](../../disenio/componentes-react.md) [cite: 3].
4. [Plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
