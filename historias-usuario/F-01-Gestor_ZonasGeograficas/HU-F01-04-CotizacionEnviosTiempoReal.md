# [HU-F01-04] Cotización de Envíos en Tiempo Real para Canales de Venta

| Campo Jira | Valor |
|---|---|
| **Tipo de Issue** | Historia (Story) |
| **Épica / Feature** | F-01: Gestor de Zonas Geográficas y Cotizador de Envíos |
| **Prioridad** | Alta |
| **Estimación (Story Points)** | 5 |
| **Componentes** | Backend, Base de Datos |
| **Etiquetas (Labels)** | `despacho`, `modulo`, `f-01`, `sdd`, `cotizacion`, `api`, `checkout` |
| **Responsable sugerido** | Valqui |

---

## 1. Declaración de la Historia (User Story)

**COMO** Canal de Venta (carrito de compras, marketplace o chatbot)  
**QUIERO** invocar el endpoint de cotización con el destino, peso y dimensiones del paquete antes de confirmar una orden  
**PARA** ofrecer al cliente el costo de envío exacto y la promesa de entrega en tiempo real.

---

## 2. Descripción y Contexto Técnico

- **Especificación origen:** [F-01-Gestor_ZonasGeograficas.md](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) (Requisito `RF-03`, Criterios `CA-07`, `CA-08`, `CA-09`, `CA-10`).
- **Endpoints asociados:**
  - `POST /api/v1/zonas/cotizar` (detallado en [integraciones/api-contract.md](../../integraciones/api-contract.md)).
- **Autenticación:** Pública o mediante API Key de canal comercial; no requiere token JWT de usuario.
- **Cuerpo de la solicitud:** `distrito`, `codigoPostal`, `coordenadas` (`latitud`, `longitud`), `pesoKg`, `volumenM3`.
- **Reglas de negocio:**
  - El destino debe identificarse por distrito, código postal o coordenadas; la zona de cobertura debe existir y encontrarse en estado `ACTIVO`.
  - Si el peso es menor o igual a cero, se responde `400 Bad Request` con el mensaje "El peso del paquete debe ser mayor a cero".
  - Si el volumen es negativo, se responde `400 Bad Request` con el mensaje "El volumen del paquete debe ser mayor o igual a cero".
  - Si el destino se encuentra fuera de todas las zonas activas, se responde `200 OK` con `coberturaDisponible: false`, sin costo de envío ni plazo estimado y el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura".
  - El motor de cálculo opera sobre sus propias tablas maestras de zonas y tarifas (caché o base de datos local) sin acoplamientos externos.
  - Rendimiento: tiempo de respuesta menor a 100 ms.
- **Entidades de datos involucradas:** `zonas`, `tarifas_zona` (lectura, ver [arquitectura/modelo-datos.md](../../arquitectura/modelo-datos.md)).

---

## 3. Criterios de Aceptación (Gherkin)

- [ ] **CA-07: Cotización exitosa dentro de cobertura**
  - **DADO** un paquete de 5 kg con destino a un distrito dentro de la zona "Lima Centro".
  - **CUANDO** el carrito de compras invoca el endpoint `POST /api/v1/zonas/cotizar`.
  - **ENTONCES** el sistema calcula el flete conforme a la matriz tarifaria activa y retorna el monto total calculado junto con la promesa de entrega (ej. "Entrega estimada en 24 a 48 horas").

- [ ] **CA-08: Cotización con parámetros de peso inválidos**
  - **DADO** una solicitud de cotización con peso negativo o cero.
  - **CUANDO** se envía al endpoint de cotización.
  - **ENTONCES** el sistema rechaza la petición con código `400 Bad Request` indicando "El peso del paquete debe ser mayor a cero".

- [ ] **CA-09: Cotización con volumen inválido**
  - **DADO** una solicitud de cotización con volumen negativo.
  - **CUANDO** se envía al endpoint de cotización.
  - **ENTONCES** el sistema rechaza la petición con código `400 Bad Request` indicando "El volumen del paquete debe ser mayor o igual a cero".

- [ ] **CA-10: Cotización sin cobertura de entrega**
  - **DADO** una solicitud de cotización para un destino fuera de todas las zonas activas.
  - **CUANDO** se envía al endpoint de cotización.
  - **ENTONCES** el sistema retorna código `200 OK` con `coberturaDisponible: false`, sin costo de envío ni plazo estimado, y con el mensaje "La dirección se encuentra fuera de nuestra zona de cobertura".

---

## 4. Definición de Terminado (Definition of Done - DoD)

- [ ] Motor de cotización implementado en Spring Boot sobre tablas maestras propias (caché o base de datos local).
- [ ] Pruebas unitarias (`JUnit 5 + Mockito`) de cálculo tarifario y validación de cobertura geográfica.
- [ ] Prueba de integración del endpoint `POST /api/v1/zonas/cotizar` validando respuestas `200` y `400` según [integraciones/api-contract.md](../../integraciones/api-contract.md).
- [ ] Verificación automatizada del tiempo de respuesta menor a 100 ms.
- [ ] Documentación y trazabilidad actualizadas en el repositorio.