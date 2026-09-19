# Especificación SPEC-F02-PROC-01: Recepción y Validación de Solicitudes de Despacho

**Tipo:** Proceso Interno / API Backend  
**Macro-funcionalidad:** F-02: Programación y Asignación de Despachos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Sistema Comercial Externo (Ventas) / Gestor de Despacho  

---

## 1. Contexto

El flujo de entrega a domicilio inicia cuando un pedido comercial es pagado y preparado en almacén. El módulo de Despacho debe recibir esta solicitud mediante una interfaz REST desacoplada, validar los datos geográficos y físicos del paquete, verificar la cobertura en el catálogo de zonas y registrar formalmente el despacho en base de datos con un código de rastreo único.

---

## 2. Propósito

Implementar el servicio de backend responsable de recibir, validar sintáctica y semánticamente las solicitudes de despacho (reales y simuladas), resolver su pertenencia a una zona de cobertura activa y persistir la entidad `Despacho` en estado `PENDIENTE_ASIGNACION`.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Exposición del endpoint formal `POST /api/v1/despachos/solicitudes`.
- Exposición del endpoint de pruebas `POST /api/v1/despachos/solicitudes/simular`.
- Validación estricta con Jakarta Validation (`@Valid`): destinatario, dirección, coordenadas geográficas, peso > 0 y volumen > 0.
- Consulta síncrona o resolución de zona contra el servicio de F-01 (`SPEC-F01-PROC-02`).
- Generación de código de rastreo alfanumérico único (`TRK-XXXXX` o `TRK-SIM-XXXXX`).
- Asignación del estado inicial `PENDIENTE_ASIGNACION` y contador de intentos en cero.
- Persistencia atómica en la tabla `despachos` de PostgreSQL (Supabase).
- Emisión de respuesta HTTP `201 Created` o estructura estándar de error (`400 Bad Request`, `422 Unprocessable Entity`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- La petición debe incluir un token JWT válido con rol `SISTEMA_VENTAS`, `GESTOR_DESPACHO` o `ADMIN`.
- La dirección de entrega debe encontrarse dentro de una zona geográfica activa en el sistema.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Autenticación y verificación del token JWT. |
| F-01 (Resolución de Zona) | Confirmar que el destino tiene cobertura y retornar el `idZona`. |
| PostgreSQL / Supabase | Almacenar las entidades `Despacho` y `HistorialEstadoDespacho`. |

### 4.3. Resultados
- Registro persistido en la tabla `despachos` con clave primaria UUID, código de rastreo único y estado `PENDIENTE_ASIGNACION`.
- Se genera el registro inicial en el historial de transiciones de estado con fecha y hora UTC.
- Retorno de código `201 Created` con el recurso creado.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Recepción y validación de solicitudes formales
El backend DEBE validar la estructura completa del payload antes de persistir.

#### CA-01. Solicitud válida con cobertura confirmada
- **DADO** un payload con `idPedido` válido, datos de contacto de destinatario, coordenadas geográficas en distrito con cobertura, `pesoKg = 5.2` y `volumenM3 = 0.04`.
- **CUANDO** se envía la petición a `POST /api/v1/despachos/solicitudes`.
- **ENTONCES** el sistema responde `201 Created`, retorna el `idDespacho` generado, `codigoRastreo` formato `TRK-[A-Z0-9]{5}`, estado `PENDIENTE_ASIGNACION` y fecha de creación en UTC.

#### CA-02. Rechazo por datos de carga inválidos (peso o volumen <= 0)
- **DADO** un payload donde `pesoKg = 0` o `volumenM3 = -0.01`.
- **CUANDO** se procesa la solicitud.
- **ENTONCES** el sistema rechaza la operación con código `400 Bad Request`, especificando en el array de errores el campo violado y la regla de validación, sin persistir registros en base de datos.

#### CA-03. Rechazo por destino sin cobertura geográfica
- **DADO** un pedido cuyas coordenadas o distrito no pertenecen a ninguna zona activa de F-01.
- **CUANDO** se invoca el proceso de recepción.
- **ENTONCES** el backend responde `422 Unprocessable Entity` con el mensaje *"La dirección de entrega no cuenta con cobertura activa en el módulo de despacho"*.

### RF-02. Generación autónoma de pedidos simulados
El backend DEBE proveer un generador de despachos de prueba para desacoplar el desarrollo de Ventas.

#### CA-04. Simulación exitosa con defaults
- **DADO** una llamada a `POST /api/v1/despachos/solicitudes/simular` con cuerpo `{}`.
- **CUANDO** se procesa la solicitud.
- **ENTONCES** se autogenera un pedido (`PED-SIM-XXXXX`), destinatario simulado, coordenadas dentro de una zona activa aleatoria, peso aleatorio entre 1 y 10 kg, y se retorna `201 Created` en estado `PENDIENTE_ASIGNACION`.

---

## 6. Frontend

*N/A - Proceso exclusivamente de backend.* Las interfaces que consumen este proceso son el formulario de simulación (`SPEC-F02-FORM-03`) y los sistemas externos de e-commerce o pasarelas comerciales.

---

## 7. Backend

### 7.1. Arquitectura de clases y servicios (Java 21 / Spring Boot)
- **`DespachoController`**: Controlador REST anotado con `@RestController` y `@RequestMapping("/api/v1/despachos/solicitudes")`.
- **`RecepcionDespachoService`**: Servicio transaccional `@Service` que orquesta la validación, llamada a resolución de zona y persistencia.
- **`SimuladorDespachoService`**: Servicio auxiliar para generación determinista de datos de prueba con librerías faker o diccionarios controlados.
- **`DespachoRepository`**: Repositorio Spring Data JPA extendiendo `JpaRepository<Despacho, UUID>`.
- **`CodigoRastreoGenerator`**: Generador seguro de códigos de rastreo con sufijo aleatorio y verificación de colisión.

### 7.2. Contrato de Entrada (DTOs)
```java
public record SolicitudDespachoRequest(
    @NotBlank(message = "El idPedido es obligatorio")
    String idPedido,
    
    @NotNull(message = "Los datos del destinatario son obligatorios")
    @Valid
    DestinatarioDto destinatario,
    
    @NotBlank(message = "La dirección de entrega es obligatoria")
    String direccionEntrega,
    
    @NotNull(message = "Las coordenadas geográficas son obligatorias")
    @Valid
    CoordenadasDto coordenadas,
    
    @Positive(message = "El peso en kg debe ser mayor a cero")
    Double pesoKg,
    
    @Positive(message = "El volumen en m3 debe ser mayor a cero")
    Double volumenM3,
    
    LocalDate fechaEstimadaEntrega
) {}
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** Latencia promedio inferior a 150 ms para el procesamiento completo y persistencia.
- **Integridad y Transaccionalidad:** Uso de `@Transactional` para asegurar que el despacho y su registro inicial en el historial se guarden atómicamente.
- **Seguridad:** Autorización basada en roles mediante `@PreAuthorize("hasAnyRole('SISTEMA_VENTAS', 'GESTOR_DESPACHO', 'ADMIN')")`.
- **Idempotencia:** Si un sistema externo reenvía el mismo `idPedido` en un intervalo menor a 1 hora, el sistema detecta duplicidad y retorna el registro existente sin crear un segundo despacho.

---

## 9. Fuera de alcance

- Procesamiento de pagos, pasarelas bancarias o facturación fiscal.
- Asignación de repartidor (se ejecuta en `SPEC-F02-PROC-02`).
- Georreferenciación de direcciones en texto plano a coordenadas (se asume que el sistema comercial o frontend envía latitud y longitud).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Integration Test | `@SpringBootTest` + `MockMvc` | Retorno `201 Created` y verificación de registro en Supabase/H2. |
| CA-02 | Unit Validation | `Validator` / JUnit 5 | `400 Bad Request` con violations en `pesoKg` y `volumenM3`. |
| CA-03 | Mocked Integration | Mockito | Simulación de zona sin cobertura retorna `422 Unprocessable Entity`. |
| CA-04 | Service Test | JUnit 5 | Servicio de simulación genera registro consistente con prefijo `SIM-`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Los endpoints de recepción y simulación estén operativos y documentados en Swagger UI.
2. Todas las validaciones de datos y reglas de cobertura operen con cobertura de pruebas unitarias >= 85%.
3. El código cumpla estrictamente con las convenciones Java de [AGENTS.md](../../AGENTS.md) (nombres en español, camelCase, inmutabilidad de records).
