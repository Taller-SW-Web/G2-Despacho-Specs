# Especificación SPEC-F05-PROC-03: Integración y Sincronización con Módulo de Seguridad

**Tipo:** Proceso Interno de Backend / Integración Externa  
**Macro-funcionalidad:** F-05: Monitoreo de Flota, Operadores y Capacidad Diaria  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Servicio Integrador de Seguridad y Usuarios  

---

## 1. Contexto

En la arquitectura modular del sistema, el módulo de Seguridad y Usuarios es el único dueño de las identidades, credenciales, hashes de contraseña y emisión de tokens JWT. El módulo de Despacho no almacena contraseñas ni autentica directamente; sin embargo, para que un repartidor pueda ingresar a la web responsive de campo (F-03), debe contar con una cuenta de usuario con rol `REPARTIDOR` vinculada a su ficha de chofer en F-05.

---

## 2. Propósito

Implementar el cliente de integración y la lógica de sincronización de backend entre F-05 y el módulo de Seguridad y Usuarios para solicitar la creación del usuario de acceso del repartidor, asociar su identificador de cuenta (`idUsuario`) al chofer en base de datos y gestionar reintentos automáticos y manuales en caso de indisponibilidad del servicio de seguridad.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Invocación síncrona o por webhook hacia la API de Seguridad y Usuarios al registrar un nuevo chofer (`POST /api/v1/usuarios`).
- Payload de solicitud: nombres, apellidos, correo corporativo, DNI y rol asignado (`REPARTIDOR`).
- Mapeo y almacenamiento del `idUsuario` retornado por Seguridad en la tabla `repartidores`.
- Resolución de identidad para F-03: servicio interno que recibe el `idUsuario` extraído del token JWT del repartidor y devuelve su `idRepartidor` operativo correspondiente.
- Manejo de tolerancia a fallos:
  - Si Seguridad no responde o devuelve error 5xx, el repartidor se persiste con bandera `vinculado = false` y estado de vinculación `PENDIENTE_VINCULACION`.
  - El repartidor con vinculación pendiente no puede ser asignado a jornadas diarias hasta regularizarse.
  - Exposición del endpoint `POST /api/v1/repartidores/{id}/reintentar-vinculacion` para reintento manual.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Conectividad de red con el servicio de Seguridad y Usuarios.
- Token de servicio o credenciales API configuradas para comunicación inter-módulos.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| Módulo de Seguridad y Usuarios | Crear la cuenta, asignar el rol `REPARTIDOR` y generar credenciales iniciales. |
| `SPEC-F03-FORM-01` | Consultará la resolución chofer-usuario al momento del login móvil. |

### 4.3. Resultados
- Chofer vinculado de forma unívoca con su identidad de autenticación.
- F-03 puede identificar al chofer a partir de los claims estándar del token JWT.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Solicitud de alta y enlace de cuentas
El proceso DEBE asociar el identificador de usuario devuelto por Seguridad.

#### CA-01. Vinculación exitosa en el alta
- **DADO** el registro de un nuevo chofer "Juan Pérez" con correo `juan.perez@empresa.com`.
- **CUANDO** F-05 solicita la creación de la cuenta a Seguridad y recibe HTTP `201` con `idUsuario = "usr-8891-uuid"`.
- **ENTONCES** se persiste `idUsuario = "usr-8891-uuid"` en el repartidor y el campo `vinculado` se marca como `true`.

#### CA-02. Resiliencia ante caída de Seguridad
- **DADO** que el servicio de Seguridad se encuentra temporalmente caído durante el alta del chofer.
- **CUANDO** se intenta la creación de usuario.
- **ENTONCES** la transacción no aborta el registro del chofer en F-05; el repartidor se guarda en estado `PENDIENTE_VINCULACION` y se emite un log de advertencia.

### RF-02. Reintento y resolución de chofer
El sistema DEBE permitir regularizar la vinculación y resolver la identidad desde el token.

#### CA-03. Reintento exitoso de vinculación
- **DADO** un chofer en estado `PENDIENTE_VINCULACION`.
- **CUANDO** el gestor pulsa *"Reintentar Vinculación"* una vez restablecido el servicio de Seguridad.
- **ENTONCES** se reenvía la solicitud, se obtiene el `idUsuario`, se actualiza a `vinculado = true` y el chofer queda habilitado para asignaciones diarias.

#### CA-04. Resolución inversa de chofer para F-03
- **DADO** una petición que llega a F-03 con un JWT cuyo claim `sub` es `"usr-8891-uuid"`.
- **CUANDO** F-03 solicita la identidad operativa a este servicio.
- **ENTONCES** se retorna el identificador operativo `"REP-0012"` y sus datos de flota.

---

## 6. Frontend

*N/A - Proceso de backend.* Consumido internamente por F-03 y por el botón de reintento en `SPEC-F05-FORM-01`.

---

## 7. Backend

### 7.1. Cliente REST de Integración (Java 21 / Spring Boot)
```java
@Service
@RequiredArgsConstructor
@Slf4j
public class SeguridadClientService {

    private final RestClient seguridadRestClient;
    private final RepartidorRepository repartidorRepository;

    public void sincronizarUsuarioRepartidor(Repartidor repartidor) {
        try {
            UsuarioSeguridadResponse response = seguridadRestClient.post()
                .uri("/api/v1/usuarios/repartidores")
                .body(new CrearUsuarioRequest(
                    repartidor.getEmail(), 
                    repartidor.getNombres(), 
                    repartidor.getApellidos(), 
                    repartidor.getDni()
                ))
                .retrieve()
                .body(UsuarioSeguridadResponse.class);

            repartidor.setIdUsuarioSeguridad(response.idUsuario());
            repartidor.setEstadoVinculacion(EstadoVinculacion.VINCULADO);
        } catch (Exception ex) {
            log.warn("Fallo en sincronización con Seguridad para chofer {}: {}", repartidor.getIdRepartidor(), ex.getMessage());
            repartidor.setEstadoVinculacion(EstadoVinculacion.PENDIENTE_VINCULACION);
        }
        repartidorRepository.save(repartidor);
    }

    public Optional<Repartidor> resolverPorUsuarioSeguridad(String idUsuarioSeguridad) {
        return repartidorRepository.findByIdUsuarioSeguridad(idUsuarioSeguridad);
    }
}
```

---

## 8. Requisitos no funcionales

- **Desacoplamiento:** F-05 nunca almacena contraseñas ni secrets de usuarios; la gestión de credenciales reside 100% en Seguridad.
- **Tolerancia a Fallos:** Circuit Breaker (Resilience4j) configurado para no bloquear el registro de choferes ante indisponibilidad externa.

---

## 9. Fuera de alcance

- Recuperación de contraseñas olvidadas por el chofer.
- Autenticación multifactor (MFA).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Mock Client Test | WireMock | Creación en Seguridad retorna UUID y persiste `VINCULADO`. |
| CA-02 | Fault Tolerance Test | JUnit 5 | Error 500 de Seguridad marca `PENDIENTE_VINCULACION`. |
| CA-03 | Retry Test | WireMock | Reintento exitoso cambia estado a `VINCULADO`. |
| CA-04 | Lookup Test | `@DataJpaTest` | Búsqueda por `idUsuarioSeguridad` retorna el repartidor. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El alta de choferes solicite la creación de la cuenta en Seguridad.
2. Se gestione adecuadamente el estado pendiente en caso de indisponibilidad.
3. F-03 resuelva al chofer a partir del token JWT sin ambigüedades.
