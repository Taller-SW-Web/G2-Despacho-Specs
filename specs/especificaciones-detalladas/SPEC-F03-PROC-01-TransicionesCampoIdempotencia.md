# Especificación SPEC-F03-PROC-01: Transiciones de Estado de Campo e Idempotencia

**Tipo:** Proceso Interno / Caso de Uso Backend  
**Macro-funcionalidad:** F-03: Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Repartidor (API Móvil)  

---

## 1. Contexto

En el trabajo de campo, los repartidores se enfrentan a conexiones intermitentes o pérdidas temporales de señal 4G. En esos escenarios, un repartidor puede reintentar enviar una entrega o un reporte de fallo varias veces creyendo que la primera falló. El backend debe garantizar que las transiciones de estado sean estrictamente válidas y que los reintentos de red no provoquen duplicación de registros ni incrementos indebidos en el contador de intentos del cliente.

---

## 2. Propósito

Implementar el motor transaccional de backend que gestiona las transiciones del ciclo de entrega en campo (`ASIGNADO` → `EN_CAMINO` → `ENTREGADO` / `FALLIDO`), validando la habilitación del operador, controlando el incremento del contador de intentos y asegurando idempotencia estricta mediante la cabecera `Idempotency-Key`.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Validación de identidad del chofer: el usuario autenticado en el token JWT debe corresponder exactamente al repartidor asignado al despacho.
- Verificación de la máquina de estados local (Anexo A de F-03 y `SPEC-TRANS-PROC-01`).
- Gestión del contador de intentos:
  - `ENTREGADO`: No altera el contador.
  - `FALLIDO` con motivo tipificado (`CLIENTE_AUSENTE`, etc.): Incrementa en exactamente +1.
  - `FALLIDO` con motivo `NO_INTENTADO`: No altera el contador.
- Mecanismo de Idempotencia:
  - Verificación de cabecera HTTP obligatoria `Idempotency-Key` (formato UUID).
  - Almacenamiento y consulta de transacciones en la tabla `registro_idempotencia` con TTL de 24 horas.
  - Ante reintentos con la misma clave, retorno inmediato de la respuesta original en caché con HTTP `200 OK`, sin duplicar transiciones ni llamadas a la base de datos.
- Registro transaccional en el historial del despacho (`SPEC-TRANS-PROC-02`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Token JWT válido con rol `REPARTIDOR`.
- Repartidor con jornada activa en F-05.
- Envío obligatorio de la cabecera `Idempotency-Key`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `SPEC-TRANS-PROC-01` | Validador transversal de transiciones de estado. |
| `SPEC-TRANS-PROC-02` | Persistencia atómica en el historial del despacho. |
| Redis / PostgreSQL | Almacenamiento de claves de idempotencia y respuestas serializadas. |

### 4.3. Resultados
- Transición de estado aplicada exactamente una vez.
- Contador de intentos inalterado ante múltiples reintentos de conexión.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Validación de transiciones y propiedad del despacho
El backend DEBE asegurar que solo el chofer asignado pueda cambiar el estado en la secuencia permitida.

#### CA-01. Transición legal de campo
- **DADO** un despacho en `ASIGNADO` asignado a "REP-0012".
- **CUANDO** el repartidor "REP-0012" invoca `iniciar-traslado`.
- **ENTONCES** el estado cambia a `EN_CAMINO`, se guarda la marca temporal UTC del servidor y responde `200 OK`.

#### CA-02. Rechazo por despacho ajeno
- **DADO** un despacho asignado al repartidor "REP-0012".
- **CUANDO** un usuario con token del repartidor "REP-9999" intenta cambiar su estado.
- **ENTONCES** el backend rechaza la operación con código `403 Forbidden` sin alterar el despacho.

### RF-02. Control estricto de Idempotencia
El backend DEBE neutralizar reintentos duplicados provenientes de pérdidas de señal.

#### CA-03. Reintento con clave de idempotencia idéntica
- **DADO** una solicitud previa de entrega exitosa procesada con `Idempotency-Key: a1b2c3d4-...`.
- **CUANDO** el cliente móvil reenvía la misma petición 5 segundos después con la misma clave de idempotencia.
- **ENTONCES** el backend detecta la clave registrada, no ejecuta una segunda inserción en el historial, no altera contadores y devuelve la respuesta HTTP original `200 OK`.

#### CA-04. Incremento singular del contador de intentos
- **DADO** un despacho en intento 1 que se marca como `FALLIDO` con `Idempotency-Key: f9e8d7c6-...`.
- **CUANDO** la petición se reintenta 3 veces consecutivas debido a timeout de red en el cliente.
- **ENTONCES** el contador final de intentos en la base de datos es exactamente 2 (se incrementó únicamente una vez).

---

## 6. Frontend

*N/A - Proceso exclusivamente de backend.* Consumido por las vistas móviles `SPEC-F03-FORM-01`, `SPEC-F03-FORM-02`, `SPEC-F03-FORM-03`.

---

## 7. Backend

### 7.1. Lógica del Interceptor / Filtro de Idempotencia
```java
@Component
public class IdempotenciaFilter extends OncePerRequestFilter {

    private final IdempotenciaRepository idempotenciaRepository;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) 
            throws ServletException, IOException {
        
        String claveIdempotencia = request.getHeader("Idempotency-Key");
        if (claveIdempotencia != null && request.getMethod().matches("POST|PATCH")) {
            Optional<RegistroIdempotencia> previo = idempotenciaRepository.findByClave(claveIdempotencia);
            if (previo.isPresent()) {
                // Retornar respuesta previa almacenada
                response.setStatus(previo.get().getStatusHttp());
                response.setContentType("application/json");
                response.getWriter().write(previo.get().getCuerpoRespuesta());
                return;
            }
        }
        filterChain.doFilter(request, response);
    }
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** Resolución de clave de idempotencia en memoria en menos de 5 ms.
- **Tolerancia a Concurrencia:** Bloqueo distribuido o restricción de unicidad en base de datos (`UNIQUE(clave_idempotencia)`) para impedir que dos peticiones simultáneas procesen la misma clave en paralelo.
- **Seguridad:** Requerimiento obligatorio de JWT firmado.

---

## 9. Fuera de alcance

- Almacenamiento offline en SQLite/IndexedDB en el cliente móvil (la arquitectura asume conexión activa; si se cae la red, se falla explícitamente y se reintenta).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | State Transition Test | `@SpringBootTest` | `ASIGNADO` pasa a `EN_CAMINO` exitosamente. |
| CA-02 | Security Driver Check | MockMvc | Chofer no propietario recibe HTTP `403 Forbidden`. |
| CA-03 | Idempotency Replay | Testcontainers | Dos peticiones idénticas producen exactamente un solo registro en base de datos. |
| CA-04 | Counter Increment Test | JUnit 5 | Múltiples reintentos de fallo mantienen `numeroIntento` en +1 del original. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Se rechacen todas las transiciones que violen la máquina de estados o la propiedad del despacho.
2. El filtro de idempotencia proteja todas las rutas `POST` y `PATCH` de campo.
3. Las pruebas automatizadas garanticen que los reintentos no alteren los saldos de intentos del cliente.
