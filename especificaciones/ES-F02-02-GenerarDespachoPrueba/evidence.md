# Evidencia de ES-F02-02: Generación de despachos de prueba para simulación

**Estado:** Backend implementado y verificado localmente; pantalla funcional e integración de frontend pendientes.

**Responsable de coordinación:** Tarqui.

**Última ejecución:** 16/10/2026, America/Lima.

## 1. Versión y entorno verificados

- Entradas: [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y Gestión §3.2.
- Backend: rama `feature/f02-implementacion-specs`, base `316767f`, cambios en el árbol de trabajo.
- Linux, Java 21.0.12.1 y PostgreSQL 18.6 aislado. Migraciones, entidad JPA y controlador reales; JWT RS256 y JWKS de prueba.
- Implementación: `GenerarDespachoPrueba`, `CoberturaProgramacionLocal`, `ProgramacionPersistencia` y `ControladorProgramacion`.
- [Registro compartido de ejecución](../../../G2-Despacho-Backend/docs/f02-implementacion-especificaciones.md), §§7–8 [cite: 1].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación ejecutada | Resultado |
|---|---|---|---|
| CA-01 | T-02 a T-04 | `{}` genera despacho pendiente, códigos `SIM`, paquete 1 y fecha civil de Lima; persiste historial y aparece en cola. | Backend aprobado. |
| CA-02 | T-02 a T-04 | Respeta zona, 12,5 kg y 0,045 m³ personalizados. También conserva decimales pequeños y admite cobertura solo postal. | Backend aprobado. |
| CA-03 | T-03, T-04 | Rechaza carga no positiva o con tipo incorrecto con `400`; zona inactiva con `422`; sin escrituras. | Backend aprobado. |
| CA-04 | T-03, T-04 | Acceso humano sin rol o token de servicio: `403`; petición sin token: `401` según Común §3.5. | Backend aprobado aplicando el contrato canónico. |
| CUI-01 a CUI-04 | T-05, T-06 | Botón, carga, toast, actualización de pantalla y badge integrado. | No ejecutado; frontend funcional pendiente. |

## 3. Registros ejecutados

- **EV-01:** `ProgramacionHttpTests`, casos de simulación, validación, acceso, cobertura y carga decimal. Verificación adicional de que crear/asignar simulados no genera comunicaciones a Ventas.
- **EV-02 y EV-03:** no ejecutados; corresponden a la interfaz funcional y su integración.
- Suite completa de Gestión: **69 pruebas aprobadas, sin fallos, errores u omisiones**, mediante `mvnw verify`; empaquetado correcto. Informes y comando reproducible en la guía del backend.

## 4. Límites

La generación no consulta Productos ni inventa repartidores o zonas. Los códigos se generan mediante secuencia de base de datos, evitando el correlativo basado en milisegundos sugerido por el plan. Las coordenadas son opcionales y no se fabrican sin una fuente geográfica. No se ejecutaron pruebas de navegador de esta funcionalidad ni integración con los servicios reales del equipo.

## 5. Referencias

1. `G2-Despacho-Backend/docs/f02-implementacion-especificaciones.md`: entorno, fuentes, implementación y resultados reproducibles.
