# [HU-F01-03] Configuración de la Matriz Tarifaria por Zona

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-01: Gestor de Zonas Geográficas y Cotizador de Envíos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 3 |
| **Componentes** | Backend, Frontend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-01`, `sdd`, `tarifas`, `matriz-tarifaria` |
| **Responsable sugerido** | Valqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Administrador de Zonas  
**QUIERO** parametrizar las reglas de tarifa por zona (tarifa base, recargo por kilogramo adicional, rangos de peso y factor de cubicaje volumétrico)  
**PARA** que el cotizador calcule automáticamente el costo de envío conforme a la configuración vigente de cada sector.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../specs/funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisito `RF-02`, Criterios `CA-05`, `CA-06`).
- **Endpoints asociados:**
  - Administración de tarifas bajo `/api/v1/zonas/{idZona}/tarifas` (a consolidar en [specs/api-contract.md](../../specs/api-contract.md)).
- **Roles requeridos:** `ADMIN` o `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Formulario de Tarifas: configurar tarifa base, recargo por kilogramo, rangos de peso y factor de cubicaje por zona.
- **Reglas de negocio:**
  - La regla tarifaria se asocia a una zona existente y en estado `ACTIVO`.
  - La tarifa base y el recargo por kilo adicional DEBEN ser valores mayores o iguales a cero; los rangos de peso deben ser consistentes (límite inferior menor que el superior).
  - Se soportan esquemas de costo base, recargo por kilogramo adicional, factor de cubicaje volumétrico y tarifa plana por zona.
  - Si la regla es inválida (tarifa negativa, zona inexistente o rangos inconsistentes), se responde `400 Bad Request` detallando los campos inválidos y no se persiste.
  - La regla guardada aplica a todas las cotizaciones futuras para esa zona.
- **Entidades de datos involucradas:** `tarifas_zona`, `zonas` (ver [specs/modelo-datos.md](../../specs/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-05: Configuración de tarifa mixta por peso y zona**
  - **DADO** que se configura para la zona "Lima Norte" una tarifa base de 10.00 PEN hasta 3 kg, más 2.00 PEN por cada kg adicional.
  - **CUANDO** se guarda la regla tarifaria.
  - **ENTONCES** el sistema asocia la regla a la zona y la aplica a todas las cotizaciones futuras para ese sector.

- [ ] **CA-06: Rechazo de regla tarifaria inválida**
  - **DADO** que se configura una regla con tarifa base negativa, una zona inexistente o rangos de peso inconsistentes.
  - **CUANDO** el administrador intenta guardar la regla.
  - **ENTONCES** el sistema rechaza la operación con código `400 Bad Request`, detalla los campos inválidos y no persiste la regla.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Entidad JPA y repositorio para `tarifas_zona` implementados en Spring Data.
- [ ] Validación de consistencia tarifaria (rangos, valores no negativos, zona existente y activa) cubierta con pruebas unitarias (`JUnit 5 + Mockito`).
- [ ] Prueba de integración verificando asociación correcta de la regla a la zona y rechazo `400` para reglas inconsistentes.
- [ ] Comprobación automatizada de que la tarifa configurada se aplica en las cotizaciones posteriores.
- [ ] Formulario de Tarifas implementado en React + Tailwind con validación visual en tiempo real.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.