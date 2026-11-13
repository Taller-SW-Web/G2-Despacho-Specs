# ES-F01-10: Registrar un distrito

**Funcionalidad padre:** [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).

**Responsable:** Valqui. **Estado:** Implementado y verificado localmente; revisión y aceptación pendientes.

**Actor principal:** Gestor de Despacho. **UI:** Aplica. **Servicio propietario:** Gestión de Despachos.

## 1. Contexto y objetivo

Registrar distritos dentro del ámbito administrado sin asignarles cobertura implícita [cite: 1].

## 2. Alcance

Alta activa y validaciones; asignación de zona pertenece a ES-F01-02.

## 3. Actor, precondiciones y resultados

El Gestor autenticado proporciona identidad y geografía. El resultado tiene UUID, versión, fechas y auditoría; ante rechazo no hay escritura parcial.

## 4. Flujo principal y alternativas

1. Completar el formulario.
2. Validar formato, geografía y unicidad, incluyendo inactivos.
3. Confirmar registro y auditoría juntos y actualizar catálogo.

## 5. Reglas, datos e integraciones

Aplican [Gestión §3.1.1](../../integraciones/api-contract-gestion-despachos.md#311-administración-de-distritos--13112026) y ES-F01-08 [cite: 2]. El catálogo no valida un padrón externo; ámbito y prefijos son los declarados en el contrato.

## 6. Criterios de aceptación

- **CA-01:** DADO datos válidos únicos, CUANDO se registra, ENTONCES crea activo con UUID y auditoría del ejecutor en UTC.
- **CA-02:** DADO nombre equivalente por mayúsculas/espacios extremos o ubigeo repetido, incluso inactivo, CUANDO se registra, ENTONCES `409` por campo sin altas.
- **CA-03:** DADO geografía, formato o campos no permitidos, CUANDO se envía, ENTONCES `400` por campo.
- **CA-04:** DADO un alta sin zona, CUANDO se cotiza, ENTONCES no ofrece cobertura.
- **CA-05:** DADO fallo de auditoría o usuario no autorizado, CUANDO se registra, ENTONCES no hay cambios confirmados.

## 7. UI, backend y requisitos no funcionales

UI en [ui.md](./ui.md). Restricciones también en backend/base; identidad del JWT y reloj del servidor.

## 8. Verificación y completitud

Integración de alta, duplicados concurrentes y rollback; componentes de formulario. Evidencia en [evidence.md](./evidence.md).

## 9. Referencias

- [cite: 1] [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md).
- [cite: 2] [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md).
- [Plan](./plan.md), [tareas](./tasks.md), [UI](./ui.md), [evidencia](./evidence.md).
