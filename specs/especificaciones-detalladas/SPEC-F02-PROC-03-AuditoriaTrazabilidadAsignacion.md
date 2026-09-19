# Especificación SPEC-F02-PROC-03: Auditoría Inmutable y Trazabilidad de Asignaciones

**Tipo:** Proceso Interno / Servicio de Backend  
**Macro-funcionalidad:** F-02: Programación y Asignación de Despachos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho / Auditor del Sistema  

---

## 1. Contexto

Para garantizar la transparencia en las operaciones de distribución y dar cumplimiento a los requerimientos de gobernanza y trazabilidad logística, cada asignación de despacho, modificación de operador y cambio de estado debe quedar permanentemente asentada en un registro de auditoría inmutable, vinculando la identidad del usuario responsable y los saldos operativos resultantes.

---

## 2. Propósito

Implementar el servicio de auditoría transaccional encargado de capturar y persistir de forma atómica e inalterable los eventos de asignación de despachos, registrando marcas temporales en UTC, la identidad del usuario gestor extraída del contexto de seguridad, el operador receptor y el balance de carga vehicular resultante.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Definición de la entidad JPA inmutable `AuditoriaAsignacion`.
- Servicio de backend `AuditoriaAsignacionService` invocado síncronamente dentro de la transacción de asignación (`SPEC-F02-PROC-02`).
- Extracción segura del identificador de usuario (`sub` o `username`) desde el `SecurityContextHolder` de Spring Security.
- Registro de marcas temporales de alta precisión en UTC (`Instant.now()`).
- Captura de métricas de carga en el instante de la asignación: peso del paquete, volumen del paquete, capacidad remanente antes y después de la operación.
- Garantía de inmutabilidad: repositorio configurado para operaciones estrictamente de lectura e inserción (`save` inicial), bloqueando actualizaciones (`UPDATE`) y eliminaciones (`DELETE`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- La asignación del despacho debe haber sido validada satisfactoriamente en cuanto a reglas de negocio y capacidad.
- Debe existir un contexto de seguridad autenticado en el hilo de ejecución (`SecurityContextHolder`).

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| Spring Security | Suministrar el principal autenticado (`UserDetails` o token JWT decodificado). |
| `SPEC-F02-PROC-02` | Caso de uso transaccional que invoca la persistencia de auditoría. |
| PostgreSQL (Supabase) | Persistir los registros en la tabla `auditoria_asignaciones`. |

### 4.3. Resultados
- Registro persistido con UUID generado automáticamente en la tabla de auditoría.
- Si la persistencia de auditoría falla, toda la asignación efectúa rollback, impidiendo que existan asignaciones no auditadas.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Captura y persistencia de datos de auditoría
El servicio DEBE almacenar todos los metadatos relevantes de la asignación sin omisiones.

#### CA-01. Registro íntegro de auditoría tras asignación
- **DADO** que una asignación de despacho es confirmada por el usuario gestor `tarqui@tienda.com`.
- **CUANDO** se persiste la transacción en el backend.
- **ENTONCES** se inserta un registro en `auditoria_asignaciones` que contiene: `idDespacho`, `idRepartidor`, `idUsuarioGestor = "tarqui@tienda.com"`, `fechaHoraAsignacion` en UTC, peso asignado, volumen asignado y nuevo saldo remanente del vehículo.

#### CA-02. Atomicidad ante fallo de persistencia de auditoría
- **DADO** un error de base de datos durante la inserción del registro de auditoría (ej. violación de restricción o fallo de conexión).
- **CUANDO** se produce la excepción en el servicio de auditoría.
- **ENTONCES** la transacción completa revierte (rollback) y el despacho permanece en `PENDIENTE_ASIGNACION`.

### RF-02. Inmutabilidad de los registros
El sistema DEBE impedir cualquier alteración o borrado de registros históricos.

#### CA-03. Bloqueo de modificación o eliminación
- **DADO** un registro de auditoría ya persistido en el sistema.
- **CUANDO** se intenta invocar una operación de actualización o borrado a través de la capa de persistencia.
- **ENTONCES** el repositorio o trigger de base de datos rechaza la operación arrojando `UnsupportedOperationException` o violación de permisos.

---

## 6. Frontend

*N/A - Proceso exclusivamente de backend.* Los datos de auditoría pueden ser consultados en vistas de trazabilidad histórica o reportes de gestión por usuarios con rol auditor.

---

## 7. Backend

### 7.1. Modelo de Datos y Entidad JPA
```java
@Entity
@Table(name = "auditoria_asignaciones")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class AuditoriaAsignacion {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id_auditoria", updatable = false, nullable = false)
    private UUID idAuditoria;

    @Column(name = "id_despacho", updatable = false, nullable = false)
    private UUID idDespacho;

    @Column(name = "id_repartidor", updatable = false, nullable = false)
    private String idRepartidor;

    @Column(name = "usuario_gestor", updatable = false, nullable = false)
    private String usuarioGestor;

    @Column(name = "fecha_hora", updatable = false, nullable = false)
    private Instant fechaHora;

    @Column(name = "peso_kg", updatable = false, nullable = false)
    private Double pesoKg;

    @Column(name = "volumen_m3", updatable = false, nullable = false)
    private Double volumenM3;

    @Column(name = "capacidad_remanente_kg", updatable = false, nullable = false)
    private Double capacidadRemanenteKg;

    @Column(name = "capacidad_remanente_m3", updatable = false, nullable = false)
    private Double capacidadRemanenteM3;

    @Column(name = "observaciones", updatable = false)
    private String observaciones;

    public AuditoriaAsignacion(UUID idDespacho, String idRepartidor, String usuarioGestor,
                               Double pesoKg, Double volumenM3, Double remanenteKg, 
                               Double remanenteM3, String observaciones) {
        this.idDespacho = idDespacho;
        this.idRepartidor = idRepartidor;
        this.usuarioGestor = usuarioGestor;
        this.fechaHora = Instant.now();
        this.pesoKg = pesoKg;
        this.volumenM3 = volumenM3;
        this.capacidadRemanenteKg = remanenteKg;
        this.capacidadRemanenteM3 = remanenteM3;
        this.observaciones = observaciones;
    }
}
```

---

## 8. Requisitos no funcionales

- **Inmutabilidad:** Entidad con getters públicos, sin setters, columnas con `updatable = false`.
- **Rendimiento:** Inserción indexada por `id_despacho` y `fecha_hora` con tiempo de persistencia < 20 ms.
- **Trazabilidad Horaria:** Marcas temporales siempre persistidas en UTC (`Instant`), normalizadas con el huso horario estándar del módulo.

---

## 9. Fuera de alcance

- Exportación masiva de auditoría a formatos externos (PDF/Excel).
- Almacenamiento en sistemas de auditoría WORM (Write Once Read Many) externos o blockchain.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Data JPA Test | `@DataJpaTest` | Registro persistido con todos los campos obligatorios poblados. |
| CA-02 | Transaction Rollback | `@SpringBootTest` | Fallo forzado en auditoría revierte el cambio de estado del despacho. |
| CA-03 | Immutability Test | JUnit 5 | Intento de `save` con entidad modificada es ignorado o bloqueado por JPA. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. La tabla `auditoria_asignaciones` y su entidad JPA estén mapeadas en el backend.
2. El servicio capture de forma transparente el usuario gestor desde el contexto de Spring Security.
3. Se garantice la atomicidad de la transacción junto al caso de uso de asignación (`SPEC-F02-PROC-02`).
