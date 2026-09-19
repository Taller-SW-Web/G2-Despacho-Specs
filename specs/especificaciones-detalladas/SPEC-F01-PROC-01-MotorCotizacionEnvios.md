# Especificación SPEC-F01-PROC-01: Motor de Cotización en Tiempo Real con Rate Limit

**Tipo:** Proceso Interno / API Pública Backend  
**Macro-funcionalidad:** F-01: Gestión de Zonas Geográficas y Cotizador de Envíos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Canales de Venta Externos (Marketplace, Chatbot, Carrito Web)  

---

## 1. Contexto

Durante el proceso de checkout o consulta en canales de venta, el cliente requiere conocer de forma instantánea si su dirección cuenta con cobertura de despacho a domicilio y cuál será el costo exacto y plazo de entrega. Al tratarse de un endpoint público consumido en altos volúmenes, debe ser ultra-rápido, determinista y estar protegido contra abusos de tráfico.

---

## 2. Propósito

Implementar el servicio de backend y endpoint REST público de cotización en tiempo real que evalúa la cobertura de una dirección, aplica la fórmula matemática de tarifas activas según peso y volumen, y entrega el costo y plazo estimado, incorporando control de tasa de peticiones (*Rate Limiting*).

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Exposición del endpoint público `POST /api/v1/cotizaciones` (sin exigencia de token JWT).
- Validación de DTO de entrada: peso mayor a cero, volumen mayor a cero (si se informa), y destino (distrito, código postal o coordenadas).
- Invocación síncrona de resolución de zona (`SPEC-F01-PROC-02`).
- Manejo de destinos sin cobertura: retorno exitoso `200 OK` con bandera `coberturaDisponible: false` sin costo ni plazo.
- Aplicación de fórmula de tarificación activa para destinos cubiertos:
  - `pesoVolumetrico = volumenM3 * factorVolumetrico`
  - `pesoCalculo = max(pesoKg, pesoVolumetrico)`
  - `pesoExcedente = max(0, pesoCalculo - pesoBaseKg)`
  - `costoTotal = tarifaBase + (pesoExcedente * recargoPorKgAdicional)`
- Aplicación de política de Rate Limiting por IP/origen (máximo 60 peticiones/minuto). Emisión de `429 Too Many Requests` ante excesos.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Existencia de zonas y reglas tarifarias vigentes en estado `ACTIVO`.
- Peso informado mayor a cero.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `SPEC-F01-PROC-02` | Servicio de resolución geoespacial de zona activa. |
| Redis / Bucket Token | Mecanismo en memoria para el control de tasa de peticiones (Rate Limiter). |
| `TarifaRepository` | Lectura en caché de las reglas tarifarias activas. |

### 4.3. Resultados
- Respuesta estructurada en menos de 100 ms con el desglose comercial de la cotización.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Cálculo de cotización
El motor DEBE calcular el costo exacto según la regla tarifaria de la zona correspondiente.

#### CA-01. Cotización exitosa dentro de cobertura
- **DADO** un destino en San Borja (zona "Lima Moderna", tarifa base 10.00 PEN hasta 3 kg, recargo 2.00 PEN/kg), peso de 5 kg y sin volumen.
- **CUANDO** se invoca `POST /api/v1/cotizaciones`.
- **ENTONCES** el sistema calcula: base 10.00 + (2 kg excedentes × 2.00) = 14.00 PEN, y responde `200 OK` con `coberturaDisponible: true`, `costoEnvio: 14.00`, `moneda: "PEN"`, `plazoEstimadoDias: 1`.

#### CA-02. Destino fuera de cobertura activa
- **DADO** una dirección en un distrito sin cobertura registrada o cuya zona está `INACTIVO`.
- **CUANDO** se solicita la cotización.
- **ENTONCES** el sistema responde `200 OK` con `coberturaDisponible: false`, `costoEnvio: null`, `plazoEstimadoDias: null` y mensaje *"La dirección se encuentra fuera de nuestra zona de cobertura"*.

#### CA-03. Rechazo por peso menor o igual a cero
- **DADO** una solicitud con `pesoKg = 0` o valor negativo.
- **CUANDO** llega al backend.
- **ENTONCES** el sistema responde `400 Bad Request` con el mensaje *"El peso del paquete debe ser mayor a cero"*.

### RF-02. Control de abuso (Rate Limiting)
El endpoint DEBE protegerse contra ataques de denegación de servicio o scraping.

#### CA-04. Límite de tasa excedido
- **DADO** que una dirección IP cliente realiza más de 60 peticiones en una ventana de 60 segundos.
- **CUANDO** envía la solicitud número 61.
- **ENTONCES** el sistema responde `429 Too Many Requests`, cabecera `Retry-After: [segundos]` y no ejecuta la lógica de cálculo.

---

## 6. Frontend

*N/A - Proceso exclusivamente de backend.* Expone una API pública consumida por carritos de compra de tiendas web, apps móviles de clientes o chatbots de atención.

---

## 7. Backend

### 7.1. Implementación en Spring Boot 3 / Java 21
```java
@RestController
@RequestMapping("/api/v1/cotizaciones")
public class CotizadorController {

    private final CotizadorService cotizadorService;
    private final RateLimiterService rateLimiterService;

    @PostMapping
    public ResponseEntity<CotizacionResponse> cotizarEnvio(
            @Valid @RequestBody CotizacionRequest request, 
            HttpServletRequest httpRequest) {
        
        // 1. Control de tasa de peticiones
        String clienteIp = httpRequest.getRemoteAddr();
        if (!rateLimiterService.permitirSolicitud(clienteIp)) {
            return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS).build();
        }

        // 2. Procesar cotización
        CotizacionResponse respuesta = cotizadorService.calcularCotizacion(request);
        return ResponseEntity.ok(respuesta);
    }
}
```

### 7.2. Contrato HTTP de Respuesta (`200 OK`)
```json
{
  "coberturaDisponible": true,
  "idZona": "ZONA-LIMA-CENTRO",
  "nombreZona": "Lima Moderna / Centro",
  "costoEnvio": 14.00,
  "moneda": "PEN",
  "plazoEstimadoDias": 1,
  "mensaje": "Cobertura confirmada para entrega al día siguiente"
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** Tiempo de respuesta P95 inferior a 80 ms (utilizando caché Redis para las tablas tarifarias).
- **Acceso Público:** No requiere token JWT de autenticación; se habilita en el filtro de seguridad de Spring Security (`/api/v1/cotizaciones` en `permitAll`).
- **Disponibilidad:** Alta resiliencia para no interrumpir el proceso de compra de los canales de venta.

---

## 9. Fuera de alcance

- Cobro y recaudación de dinero.
- Reserva de cupo o inventario de transporte.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Unit Test | JUnit 5 | Cálculo matemático exacto de tarifas mixtas y volumétricas. |
| CA-02 | Integration Test | MockMvc | Dirección fuera de polígono retorna `coberturaDisponible: false`. |
| CA-03 | Validation Test | MockMvc | `pesoKg <= 0` retorna HTTP `400 Bad Request`. |
| CA-04 | Rate Limit Test | Testcontainers | 61 peticiones consecutivas desde la misma IP arrojan HTTP `429`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El endpoint público de cotización responda con precisión a las reglas tarifarias de cada zona.
2. El rate limiting proteja efectivamente la infraestructura contra sobrecargas.
3. Se verifiquen todas las pruebas unitarias y de integración automáticas.
