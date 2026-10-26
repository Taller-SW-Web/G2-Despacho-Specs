# Evidencia de ES-F02-01: Recepción de solicitudes de despacho

**Estado:** Backend implementado y verificado localmente con PostgreSQL real y Productos/Seguridad de prueba; integración con los proveedores reales pendiente.

**Responsable de coordinación:** Tarqui.

**Última ejecución:** 16/10/2026, America/Lima.

## 1. Versión y entorno verificados

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md), Común §§3, 5.2, 7.1, 8 y 9.
- Backend: rama `feature/f02-implementacion-specs`, base `316767f`, cambios en el árbol de trabajo; no se atribuye un commit nuevo.
- Linux, Temurin 21.0.12.1, PostgreSQL 18.6 local aislado, Flyway V1–V3 y JPA reales.
- `ProgramacionHttpTests` utiliza MockMvc, JWT RS256 firmados y descubrimiento/JWKS HTTP de prueba. Productos es un doble HTTP con ruta y payload canónicos; no un catálogo local usado como éxito real.
- Registro reproducible: [guía del backend](../../../G2-Despacho-Backend/docs/f02-implementacion-especificaciones.md), §§7–8 [cite: 1].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación ejecutada | Resultado |
|---|---|---|---|
| CA-01 | T-04 a T-08 | SKU repetidos agrupados; 2,65 kg y 0,02126 m³; paquete lógico 1; fecha hábil según Lima; códigos únicos; despacho e historial atómicos. | Backend aprobado con Productos HTTP simulado. |
| CA-02 | T-04, T-08 | Zona inactiva produce `422 DESP_ERROR_SIN_COBERTURA`, sin consultar Productos ni persistir. | Aprobado localmente. |
| CA-03 | T-01, T-08 | Obligatorios, cantidades cero/fraccionarias/cadenas, campos extra y UUID v4 inválido; `400` con errores por campo. | Aprobado localmente. |
| CA-04 | T-03, T-08 | Misma clave/contenido devuelve código/cuerpo originales; otra clave para el mismo pedido devuelve `200` con estado actual. Dos creaciones concurrentes conservan una entidad y un historial. | Aprobado localmente. |
| CA-05 | T-05, T-08 | SKU no encontrado y peso nulo producen los `422` correspondientes, sin datos parciales. | Aprobado con Productos simulado. |
| CA-06 | T-05, T-08 | `5xx` y espera superior al timeout producen `503`; no queda despacho ni clave aceptada. | Aprobado con fallos HTTP inducidos. |
| CA-07 | T-02, T-08 | Firma, emisor, expiración, audiencia y tipo inválidos: `401`; scope/sub no autorizados: `403`; sin efectos. | Aprobado con JWT y JWKS de prueba. |

## 3. Registros ejecutados

- **EV-01:** `ProgramacionHttpTests`: validación, autorización e idempotencia de recepción.
- **EV-02:** misma suite, casos de datos físicos, rechazo y timeout del proveedor HTTP.
- **EV-03:** misma suite, persistencia PostgreSQL/JPA, unicidad concurrente y fallo inducido al insertar historial: rollback de despacho y clave.
- `ProveedorTokenServicioTests`: 2 pruebas adicionales de credencial propia, scope, renovación y emisión fallida.
- La suite completa de Gestión terminó con **69 pruebas aprobadas, 0 fallos, 0 errores y 0 omitidas** mediante `mvnw verify`; incluye 23 pruebas HTTP de F-02 y regresiones F-01/F-04. Comando completo e informes en la guía del backend.

## 4. Ajustes respecto del plan y límites

Se utiliza la ruta canónica de Productos `/api/v1/productos/datos-fisicos/consulta`, no `lote-datos-fisicos`. Los dobles HTTP se implementan con el servidor HTTP del JDK, sin añadir WireMock. Al no disponer de daemon Docker, todas las suites se ejecutaron contra PostgreSQL externo de pruebas, incluida la suite JDBC histórica en un esquema aislado; no se ejecutó el modo Testcontainers.

No hay UI propia de esta especificación. La aceptación entre módulos reales y sus credenciales por ambiente permanece pendiente; las pruebas locales no acreditan disponibilidad de Productos o Seguridad del equipo.

## 5. Referencias

1. `G2-Despacho-Backend/docs/f02-implementacion-especificaciones.md`: implementación, comando reproducible, entorno, resultados y límites de los dobles HTTP.
