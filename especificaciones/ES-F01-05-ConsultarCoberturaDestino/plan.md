# Plan de ES-F01-05: Consultar la cobertura de un destino

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** No aplica. Es una operación de API de servicio consumida por Marketplace y Chatbot; no crea ni modifica una interfaz del módulo. No se incluye `ui.md`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-05 | Contenido previo en `12d5041`; migración en esta carpeta. |
| UI | No aplica; justificado en [spec.md](./spec.md), sección 7 | — |
| Contrato | [Contrato externo](../../integraciones/api-contract.md), §§3.4, 3.5, 5.1 y 10.1 | `12d5041`; referencias adaptadas a la división de `0fbd89a`; DTO de respuesta pendiente de detalle. |
| Arquitectura y datos | [C4 contenedores](../../arquitectura/c4-contenedores.md), §3.1; [modelo de datos](../../arquitectura/modelo-datos.md), §3.1 | `12d5041`. |

Este cambio prepara documentación. La modificación del contrato, el código y las pruebas se ejecutan en tareas posteriores. No se duplican contratos ni se da por cerrada la revisión técnica [cite: 1, 2].

## 2. Estrategia y responsabilidades

La operación se expone a través del Gateway con autorización por token de servicio. Gestión valida la identidad de servicio, la presencia de `distrito` y evalúa la cobertura contra zonas `ACTIVO`, sin líneas de producto. Responde disponibilidad, zona y datos normalizados del destino. Los canales son responsables de su propia interfaz.

| Área | Responsabilidad | Ubicación o elementos previstos |
|---|---|---|
| Gateway | Enrutamiento, propagación de identidad de servicio y aplicación del límite de tasa | `api-gateway`. |
| Gestión de Despachos | Autorización por scope, caso de uso y evaluación de cobertura | Funcionalidad `zonas/` o `cotizaciones/` bajo el paquete base existente. |
| Seguridad y Usuarios | Emisión de tokens de servicio con `cotizaciones:calcular` | Contrato §3.4 y §8. |
| Marketplace y Chatbot | Consumo de la operación y su propia interfaz | Fuera del alcance de este módulo. |

No se crean módulos desplegables nuevos ni una interfaz administrativa.

## 3. Contrato e integración

- Endpoint: `POST /api/v1/cotizaciones` sin `lineas`. Sin `lineas`, la respuesta no incluye costo, plazo ni datos de productos.
- Autenticación: token de servicio con `tipo=servicio` y scope `cotizaciones:calcular`; el consumidor no puede acceder a configuración interna.
- Validación: `distrito` obligatorio; su ausencia produce `DESP_ERROR_DESTINO_REQUERIDO`.
- Salida: `coberturaDisponible`, nombre de la zona cuando aplica y datos normalizados del destino; mensaje de destino fuera de cobertura cuando no hay zona activa.
- Errores: `DESP_ERROR_DESTINO_REQUERIDO`, `DESP_ERROR_LIMITE_COTIZACION` y la autenticación/autorización del contrato.
- Sin `Idempotency-Key`; no modifica recursos ni publica eventos.
- El DTO exacto y los códigos se concretan en el contrato antes de implementar el adaptador real (DT-01).

## 4. Backend, persistencia e integraciones

- Entrada: `POST /api/v1/cotizaciones` sin `lineas`. Validar el token de servicio y su scope; el canal no sustituye esta comprobación.
- Caso de uso: normalizar el destino, buscar la zona `ACTIVO` que contiene el distrito o el código postal y componer la respuesta sin costo.
- Datos locales: `zonas`, `zonas_distritos`, `distrito` y `zonas_codigos_postales`, de solo lectura. La tabla postal con datos fue comunicada el 26/10/2026; verificar que las consultas la utilicen y no la columna postal heredada de otra relación. No vaciar ni recrear esos datos.
- Migración: revisar el esquema existente y su gestión con Arquitectura; crear migraciones Flyway solo para cambios necesarios.
- Integraciones: Seguridad y Usuarios emite el token de servicio; no se consulta a Productos y Ofertas porque no hay líneas.
- Efectos secundarios: ninguno; la variante sin líneas no crea ni modifica recursos, incluida `cotizaciones`. La persistencia exacta de ES-F01-06 no debe trasladarse a esta consulta.
- Límite de tasa: aplicar el parámetro `LIMITE_COTIZACIONES_POR_MINUTO` por `sub` e IP (DT-05); su implementación puede residir en el Gateway o en el servicio según se acuerde.
- Errores: aplicar el formato central de §3.5; el detalle del DTO y del límite se concreta en el contrato.
- Fechas: el modelo establece `America/Lima` para presentación y UTC para instantes si la respuesta incluyera marcas temporales.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | DTO, errores y contrato concretados; casos de uso aislados probados | DT-01 | CA-01 a CA-03 (pruebas aisladas) |
| I-02 | Endpoint autorizado y probado con datos locales | I-01, DT-02 y base de token/errores de DT-03 | CA-01 a CA-04 |
| I-03 | Límite de tasa y verificación del recorrido por Gateway | I-02 y DT-05 | CA-05 y confirmación de CA-01 a CA-04 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | Destino cubierto responde disponibilidad y zona sin costo | Integración PostgreSQL del backend y Gateway | Real |
| CA-02 | Destino fuera de cobertura responde `200` con `false` | Datos sin zona activa | Real |
| CA-03 | Falta de `distrito` produce `DESP_ERROR_DESTINO_REQUERIDO` | Prueba del endpoint | Real |
| CA-04 | Token ausente o sin scope rechazado sin revelar cobertura | Pruebas de seguridad del endpoint | Real |
| CA-05 | Exceso de límite produce `429` con `DESP_ERROR_LIMITE_COTIZACION` | Prueba de tasa por `sub` e IP | Real |

Comandos previstos: desde Gestión, `./mvnw.cmd test`; las pruebas con Testcontainers requieren Docker. Los resultados se anotan en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Justificación y fuente | Responsable | Bloquea qué incremento |
|---|---|---|---|---|
| DT-01 | DTO de la respuesta de cobertura, códigos de error y forma del mensaje fuera de cobertura | Contrato externo §5.1 y §10.1 | Valqui con Backend y Arquitectura | Adaptadores de I-01/02 |
| DT-02 | Verificar esquema real y lector de `zonas_distritos`/`zonas_codigos_postales`, y acordar precedencia/conflicto entre distrito y postal con ES-F01-07 | Modelo §3.1 actualizado con DDL comunicado; tabla postal con datos no acredita consultas correctas | Arquitectura con Backend | CA-01/02 e integración real |
| DT-03 | Esquema/migraciones necesarios, base compartida de errores, conexión de datos y rutas del Gateway, y emisión de tokens de servicio con scope | Inicialización actual del backend y modelo | Valqui coordina con Arquitectura, DevOps y Seguridad | Ejecución real de I-02 |
| DT-04 | Verificación del contrato de consumo de Marketplace y Chatbot (que no inyecten peso/volumen ni esperen costo) | Contrato externo §5.1 y §10.1 | Valqui con los responsables de los canales | Aceptación de I-02 |
| DT-05 | Mecanismo del límite de tasa por `sub` e IP y valor de `LIMITE_COTIZACIONES_POR_MINUTO` | Modelo de datos, parámetros globales; F-01 CA-14 | Valqui con Arquitectura y DevOps | CA-05 e I-03 |

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas del incremento están revisadas y los pendientes bloqueantes resueltos.
- [ ] Las tareas cubren todos los criterios y tienen una comprobación concreta.
- [ ] La operación respeta el contrato externo, la autorización por scope y la propiedad de datos.
- [ ] El límite de tasa se verifica de extremo a extremo.
- [ ] Todos los criterios del alcance cuentan con evidencia, distinguiendo dobles y servicios reales.

## 9. Referencias

1. [Especificación](./spec.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [Contrato externo](../../integraciones/api-contract.md#51-solicitar-cotización), [modelo de datos](../../arquitectura/modelo-datos.md) y [arquitectura de contenedores](../../arquitectura/c4-contenedores.md).
3. [Flujo SDD](../../plantillas/sdd/README.md).
