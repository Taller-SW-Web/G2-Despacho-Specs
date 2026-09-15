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
**QUIERO** que la configuración de zonas y tarifas quede restringida a usuarios autorizados y registre el usuario y la marca temporal de cada cambio, mientras el endpoint de cotización permanece accesible sin token de usuario  
**PARA** garantizar la trazabilidad de las decisiones de configuración y permitir que el checkout cotice sin fricciones.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../specs/funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisitos `RF-01` y `RF-03`, Criterios `CA-04`, `CA-11`).
- **Endpoints asociados:**
  - Administrativos de zonas y tarifas (requieren token JWT con rol `ADMIN` o `GESTOR_DESPACHO`).
  - `POST /api/v1/zonas/cotizar` (público o protegido por API Key de canal comercial; detallado en [specs/api-contract.md](../../specs/api-contract.md)).
- **Roles requeridos:** `ADMIN` o `GESTOR_DESPACHO` para todas las operaciones de registro o modificación de zonas y tarifas.
- **Reglas de negocio y persistencia:**
  - Un usuario sin los roles `ADMIN` ni `GESTOR_DESPACHO` que intente registrar o modificar zonas o tarifas recibe `403 Forbidden` y no accede a información de configuración.
  - El endpoint de cotización procesa las solicitudes sin exigir autenticación de usuario; la protección, cuando aplique, se realiza mediante API Key de canal comercial.
  - Cada creación, modificación o desactivación de zonas y tarifas DEBE registrar el usuario autenticado y la marca temporal correspondiente (UTC).
  - Las marcas temporales de auditoría se persisten en `TIMESTAMPTZ` y los registros son de solo inserción.
- **Entidades de datos involucradas:** `zonas`, `tarifas_zona` (ver [specs/modelo-datos.md](../../specs/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-04: Acceso sin permisos requeridos**
  - **DADO** que un usuario sin el rol `ADMIN` ni `GESTOR_DESPACHO` intenta registrar o modificar zonas o tarifas.
  - **CUANDO** realiza la petición al backend.
  - **ENTONCES** el sistema rechaza la solicitud con código `403 Forbidden` y no expone información de configuración.

- [ ] **CA-11: Cotización sin token de usuario**
  - **DADO** que el endpoint de cotización es de acceso público o protegido por API Key de canal comercial.
  - **CUANDO** un canal de venta envía una solicitud sin token JWT de usuario.
  - **ENTONCES** el sistema procesa la cotización normalmente y no exige autenticación de usuario.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Spring Security configurado: endpoints administrativos protegidos con rol `ADMIN` o `GESTOR_DESPACHO`; cotización pública o vía API Key de aplicación.
- [ ] Pruebas de seguridad (`Spring Security Test`) verificando `403 Forbidden` para roles incorrectos o usuarios anónimos y respuesta exitosa para la cotización sin token.
- [ ] Auditoría de cambios de zonas y tarifas con usuario autenticado y marca temporal en UTC.
- [ ] Prueba de integración (`DataJpaTest`) confirmando la persistencia correcta de los registros de auditoría.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.