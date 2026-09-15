# [HU-F01-01] Administración de Zonas de Cobertura

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-01: Gestor de Zonas Geográficas y Cotizador de Envíos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Frontend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-01`, `sdd`, `zonas`, `cobertura` |
| **Responsable sugerido** | Valqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Administrador de Zonas o Gestor de Despacho  
**QUIERO** registrar y delimitar zonas geográficas de cobertura logística asociadas a distritos, sectores, códigos postales o polígonos trazados sobre un mapa  
**PARA** definir las áreas donde el módulo puede entregar pedidos y permitir que el cotizador calcule tarifas solo dentro de esas zonas.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../specs/funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisito `RF-01`, Criterios `CA-01`, `CA-03`).
- **Endpoints asociados:**
  - CRUD de zonas de cobertura bajo `/api/v1/zonas` (creación `POST /api/v1/zonas` y listado `GET /api/v1/zonas`, a consolidar en [specs/api-contract.md](../../specs/api-contract.md)).
- **Roles requeridos:** `ADMIN` o `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Formulario de Zona: registrar o editar una zona con nombre, distritos comprendidos, códigos postales y estado.
  - Mapa de Delimitación: dibujar o seleccionar polígonos de cobertura sobre un mapa (ej. Leaflet) y previsualizar el área registrada.
- **Reglas de negocio:**
  - El nombre de la zona es obligatorio y debe ser único; los distritos y/o polígonos no deben generar solapamientos conflictivos con zonas activas existentes.
  - Si la zona o su delimitación ya se encuentran cubiertos, se responde `409 Conflict` con detalle del solapamiento y no se persiste.
  - Toda zona creada se guarda con identificador único y estado `ACTIVO`.
  - La validación de solapamiento se realiza mediante cálculo geoespacial (PostGIS).
- **Entidades de datos involucradas:** `zonas` (ver [specs/modelo-datos.md](../../specs/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-01: Creación exitosa de una zona de cobertura**
  - **DADO** que un usuario administrador ingresa el nombre de la zona (ej. "Lima Centro"), distritos comprendidos (Miraflores, San Isidro, Lince) y estado "Activo".
  - **CUANDO** confirma la creación de la zona en el sistema.
  - **ENTONCES** el backend valida que no existan solapamientos conflictivos, registra la zona con identificador único y estado `ACTIVO` y responde el recurso creado.

- [ ] **CA-03: Rechazo de zona duplicada o solapada**
  - **DADO** que se intenta registrar una zona cuyo nombre, distrito o polígono ya se encuentra cubierto por una zona activa existente.
  - **CUANDO** el administrador confirma la creación.
  - **ENTONCES** el sistema rechaza la operación con código `409 Conflict`, detalla el solapamiento detectado y no persiste la zona duplicada.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Entidad JPA y repositorio para `zonas` implementados en Spring Data.
- [ ] Validación de solapamiento geoespacial con PostGIS cubierta por pruebas unitarias e integración.
- [ ] Pruebas de integración del CRUD verificando la creación exitosa de zonas válidas y el rechazo `409` para duplicadas o solapadas.
- [ ] Formulario de Zona y Mapa de Delimitación (Leaflet) implementados en React + Tailwind con previsualización del área registrada.
- [ ] Respuestas HTTP alineadas al contrato en [specs/api-contract.md](../../specs/api-contract.md).
- [ ] Documentación y trazabilidad actualizadas en el repositorio.