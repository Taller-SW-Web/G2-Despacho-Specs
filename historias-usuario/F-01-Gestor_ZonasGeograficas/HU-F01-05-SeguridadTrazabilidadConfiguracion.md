# [HU-F01-05] Seguridad y Trazabilidad de la Configuración de Zonas y Tarifas

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-01: Gestor de Zonas Geográficas y Cotizador de Envíos |
| **Prioridad** | Media |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-01`, `sdd`, `seguridad`, `auditoria`, `trazabilidad` |
| **Responsable sugerido** | Valqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Auditor de Operaciones y Canal de Venta  
**QUIERO** que la configuración de zonas y tarifas quede restringida a usuarios autorizados y registre el usuario y la marca temporal de cada cambio, mientras el endpoint de cotización se autentica con token de servicio y no exige token de usuario  
**PARA** garantizar la trazabilidad de las decisiones de configuración y permitir que el checkout cotice sin fricciones.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisitos `RF-01` y `RF-03`, Criterios `CA-04`, `CA-11`).
- **Endpoints asociados:**
  - Administrativos de zonas y tarifas (requieren token JWT con rol `GESTOR_DESPACHO`).
  - `POST /api/v1/cotizaciones` (token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`, detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md), sección 5.1).
- **Rol requerido:** `GESTOR_DESPACHO` para todas las operaciones de registro o modificación de zonas y tarifas.
- **Reglas de negocio y persistencia:**
  - Un usuario sin `GESTOR_DESPACHO` que intente registrar o modificar zonas o tarifas recibe `403 Forbidden` y no accede a información de configuración.
  - El endpoint de cotización no exige un JWT de usuario humano: se protege con un token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`. Sin token, con un token vencido o sin el scope, la respuesta es `401 Unauthorized` o `403 Forbidden` conforme a la sección 3.5 del contrato.
  - Cada creación, modificación o desactivación de zonas y tarifas DEBE registrar el usuario autenticado y la marca temporal correspondiente (UTC).
  - Las marcas temporales de auditoría se persisten en `TIMESTAMPTZ` y los registros son de solo inserción.
- **Entidades de datos involucradas:** `zonas`, `tarifas_zona` (ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-04: Acceso sin permisos requeridos**
  - **DADO** que un usuario sin el rol `GESTOR_DESPACHO` intenta registrar o modificar zonas o tarifas.
  - **CUANDO** realiza la petición al backend.
  - **ENTONCES** el sistema rechaza la solicitud con código `403 Forbidden` y no expone información de configuración.

- [ ] **CA-11: Cotización con token de servicio y sin sesión de usuario**
  - **DADO** que el canal obtuvo un token técnico con `cotizaciones:calcular`.
  - **CUANDO** un canal de venta envía la solicitud con `Authorization: Bearer <token de servicio>` y sin JWT de usuario.
  - **ENTONCES** el sistema procesa la cotización normalmente, sin requerir una sesión de usuario humano; y responde `401 Unauthorized` si el token de servicio falta o no es válido, o `403 Forbidden` si no tiene el scope.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Spring Security configurado: endpoints administrativos protegidos con `GESTOR_DESPACHO`; cotización protegida con token de servicio y scope.
- [ ] Pruebas de seguridad (`Spring Security Test`) verificando `403 Forbidden` para roles incorrectos o usuarios anónimos en la configuración, y `401`/`403` según [integraciones/api-contract.md](../../integraciones/api-contract.md) para la cotización sin token de servicio o sin el scope.
- [ ] Auditoría de cambios de zonas y tarifas con usuario autenticado y marca temporal en UTC.
- [ ] Prueba de integración (`DataJpaTest`) confirmando la persistencia correcta de los registros de auditoría.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
