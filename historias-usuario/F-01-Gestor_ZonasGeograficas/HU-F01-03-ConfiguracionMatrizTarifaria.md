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
**QUIERO** parametrizar la tarifa vigente por zona (tarifa base, peso incluido, recargo por kilogramo adicional, factor volumétrico, moneda y plazo estimado en días hábiles)  
**PARA** que el cotizador calcule automáticamente el costo de envío conforme a la configuración vigente de cada sector.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisito `RF-02`, Criterios `CA-05`, `CA-06`).
- **Endpoints asociados:**
  - `GET /api/v1/zonas/{idZona}/tarifa` (consultar la tarifa vigente) y `PUT /api/v1/zonas/{idZona}/tarifa` (crear o reemplazar la tarifa), definidos en [integraciones/api-contract.md](../../integraciones/api-contract.md), sección 9.1.
- **Rol requerido:** `GESTOR_DESPACHO` (autenticación JWT).
- **Componentes de Frontend:**
  - Formulario de Tarifas: configurar tarifa base, peso incluido, recargo por kilogramo, factor volumétrico y plazo estimado por zona.
- **Cuerpo de la tarifa (sección 9.1 del contrato):**

  ```json
  {
    "tarifaBase": 10,
    "pesoIncluidoKg": 3,
    "recargoKgAdicional": 2,
    "factorVolumetrico": 1.25,
    "moneda": "PEN",
    "plazoEstimadoDiasHabiles": 2
  }
  ```

- **Reglas de negocio:**
  - La regla tarifaria se asocia a una zona existente y en estado `ACTIVO`.
  - `tarifaBase` y `recargoKgAdicional` DEBEN ser valores mayores o iguales a cero; `pesoIncluidoKg` debe ser mayor que cero y `factorVolumetrico`, si se informa, también.
  - La moneda se expresa en `PEN` y `plazoEstimadoDiasHabiles` es un número entero de días hábiles.
  - No se soportan rangos de peso por tramos ni tarifa plana por zona; quedan fuera del alcance de F-01.
  - Si la regla es inválida (tarifa negativa, peso incluido no positivo o zona inexistente o inactiva), se responde `400 Bad Request` detallando los campos inválidos y no se persiste.
  - Al guardar una nueva regla, esta queda como única tarifa vigente de la zona y la anterior se conserva como histórico.
  - La regla guardada aplica a todas las cotizaciones futuras para esa zona.
- **Entidades de datos involucradas:** `tarifas_zona`, `zonas` (ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-05: Configuración de tarifa mixta por peso y zona**
  - **DADO** que se configura para la zona "Lima Norte" una tarifa base de 10.00 PEN hasta 3 kg, más 2.00 PEN por cada kg adicional.
  - **CUANDO** se guarda la regla tarifaria.
  - **ENTONCES** el sistema asocia la regla a la zona y la aplica a todas las cotizaciones futuras para ese sector.

- [ ] **CA-06: Rechazo de regla tarifaria inválida**
  - **DADO** que se configura una regla con tarifa base negativa, peso incluido no positivo, factor volumétrico no positivo o una zona inexistente o en `INACTIVO`.
  - **CUANDO** el administrador intenta guardar la regla.
  - **ENTONCES** el sistema rechaza la operación con código `400 Bad Request`, detalla los campos inválidos y no persiste la regla.

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Entidad JPA y repositorio para `tarifas_zona` implementados en Spring Data.
- [ ] Validación de consistencia tarifaria (valores no negativos, peso incluido y factor volumétrico positivos, zona existente y activa) cubierta con pruebas unitarias (`JUnit 5 + Mockito`).
- [ ] Prueba de integración verificando asociación correcta de la regla a la zona y rechazo `400` para reglas inconsistentes.
- [ ] Comprobación automatizada de que la tarifa configurada se aplica en las cotizaciones posteriores.
- [ ] Formulario de Tarifas implementado en React + Tailwind con validación visual en tiempo real.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.
