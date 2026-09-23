# [HU-F02-01] Recepción de Solicitudes de Despacho

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-02: Programación y Asignación de Despachos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-02`, `sdd`, `recepcion`, `api` |
| **Responsable sugerido** | Tarqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Sistema Comercial (Ventas / Checkout)  
**QUIERO** enviar una solicitud de despacho formal con los datos del pedido, destinatario y dimensiones  
**PARA** que el módulo de despacho registre el paquete en cola y genere un código de rastreo único para su entrega.  

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-02-ProgramacionAsignacionDespachos.md](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md) (Requisito `RF-01`).
- **Endpoints asociados:**
  - `POST /api/v1/despachos/solicitudes` (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md)).
- **Roles requeridos:** `GESTOR_DESPACHO` o `SISTEMA_VENTAS` (autenticación JWT).
- **Reglas de negocio:**
  - El payload debe incluir obligatoriamente: `idPedido`, datos de destinatario (`nombre`, `telefono`, `email`), `direccionEntrega`, `coordenadas` (`latitud`, `longitud`), `pesoKg` > 0 y `volumenM3` > 0.
  - La fecha estimada de entrega debe ser igual o posterior a la fecha actual.
  - Si la validación es exitosa, se genera automáticamente un código de rastreo único (`TRK-XXXXX`), se asigna el estado inicial `PENDIENTE_ASIGNACION` y se retorna HTTP `201 Created`.
  - Si faltan datos obligatorios o los valores numéricos son inválidos (peso o volumen <= 0), la petición se rechaza con HTTP `400 Bad Request` sin persistencia parcial.
- **Entidades de datos involucradas:** `despachos`, `historial_estados_despacho`.

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-01: Recepción exitosa desde sistema comercial**
  - **DADO** que un sistema externo envía una solicitud con identificador de pedido, datos del destinatario, dirección, coordenadas, peso y volumen válidos.
  - **CUANDO** la petición es procesada con un token de autorización válido en `POST /api/v1/despachos/solicitudes`.
  - **ENTONCES** el sistema guarda el despacho con estado `PENDIENTE_ASIGNACION`, genera un código de rastreo único y responde con código `201 Created` y el cuerpo del despacho registrado.

- [ ] **CA-03: Rechazo de solicitud con datos incompletos o inconsistentes**
  - **DADO** que una solicitud carece de dirección de entrega o presenta un peso menor o igual a cero.
  - **CUANDO** la solicitud es evaluada por la capa de validación en `POST /api/v1/despachos/solicitudes`.
  - **ENTONCES** el sistema rechaza la operación con código `400 Bad Request`, detalla los campos inválidos en la estructura estándar de error y no persiste registros parciales en la base de datos.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Código implementado en Java 21 / Spring Boot siguiendo las convenciones de [AGENTS.md](../../AGENTS.md).
- [ ] DTOs de entrada validados con anotaciones `@NotNull`, `@NotBlank`, `@Positive` (`jakarta.validation`).
- [ ] Pruebas unitarias de validación y de servicio con `JUnit 5 + Mockito` aprobadas con cobertura >= 80%.
- [ ] Prueba de integración del endpoint `POST /api/v1/despachos/solicitudes` validada contra [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
