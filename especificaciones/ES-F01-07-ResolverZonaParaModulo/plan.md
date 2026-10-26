# Plan de ES-F01-07: Resolver la zona de un destino para el módulo

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** No aplica. El comportamiento resuelve cobertura para casos de uso internos, sin crear ni modificar pantallas; no requiere `ui.md`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-05 | Original en `91db8f8`; migración SDD del 16/10/2026 |
| Funcionalidad padre | [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-04 y §8 | `91db8f8` |
| Contratos | [Gestión §6](../../integraciones/api-contract-gestion-despachos.md#6-api-interna-provista-por-gestión), [convenciones comunes](../../integraciones/api-contract.md#3-convenciones-comunes) | `91db8f8`; comunicación de cobertura hacia Operación pendiente |
| Arquitectura y datos | [Contenedores §§3 y 5](../../arquitectura/c4-contenedores.md), [modelo §§3.1 y 3.3](../../arquitectura/modelo-datos.md) | `91db8f8` |
| Consumidores | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), [F-05](../../funcionalidades/F-05-GestionRepartidoresVehiculos.md) | `91db8f8` |

El plan no establece una nueva ruta ni credenciales no acordadas; esas decisiones pertenecen al contrato de Gestión [cite: 1, 2].

## 2. Estrategia y responsabilidades

Centralizar la resolución en un caso de uso de Gestión compartido con las consultas de cobertura y cotización. F-02 lo invoca dentro del mismo servicio; el acceso de Operación se implementará después de acordar si requiere resolución por destino o consumo del catálogo activo. Cada consumidor conserva su responsabilidad de negocio.

| Capa o aplicación | Responsabilidad | Elementos previstos |
|---|---|---|
| Gestión, cobertura | Normalizar destino y buscar una única zona activa | Caso de uso y repositorio de lectura |
| Gestión, F-02 | Asociar zona al crear despacho o rechazar destino sin cobertura | Flujo existente de recepción |
| Operación, F-05 | Consumir información de zonas para su operación | Adaptador según contrato revisado |
| Seguridad | Identidad técnica del consumidor remoto | Mecanismo acordado en Gestión §6 |

## 3. Frontend y componentes React

No aplica. No hay formulario, pantalla ni componente React asociado; la asignación de zona o jornada se presenta en las interfaces de sus funcionalidades propietarias.

## 4. Backend, persistencia e integraciones

- Entrada: destino identificable y contexto autorizado del consumidor; adaptar el acceso remoto solo tras DT-01. La llamada local de F-02 conserva la autorización de su operación de entrada.
- Caso de uso: normalizar distrito/código postal, consultar exclusivamente zonas `ACTIVO` y retornar zona y destino normalizado o ausencia de cobertura. Un destino sin ambos identificadores se rechaza.
- Datos: zonas y delimitación pertenecen a Gestión. Leer `zonas_distritos` y `zonas_codigos_postales` como fuentes de cobertura distrital/postal, sin una segunda fuente postal en la columna heredada. No consultar directamente `asignaciones_diarias` ni otra tabla de Operación; los consumidores no acceden a la base de Gestión.
- Migración: reutilizar el esquema de cobertura y sus índices una vez conciliados (DT-03); no agregar persistencia de resoluciones.
- Estabilidad: con la misma configuración, ambos consumidores reciben la misma resolución; no mantener una segunda lógica ni una caché sin invalidación acordada.
- Efectos secundarios: ninguno en la resolución. F-02 persiste la asociación bajo su propio caso de uso. Desactivar una zona no reescribe despachos existentes.
- Concurrencia: leer cobertura de forma coherente por invocación; precisar con F-02 la frontera entre resolución y creación si la configuración cambia durante esa operación (DT-04).
- Seguridad y contrato: el resultado `200`/`400` de los criterios se conserva como comportamiento esperado del adaptador; ruta, permisos, respuestas y normalización remotos se documentan únicamente en Gestión §6 antes de implementarlos.
- Tarifas: no consultar datos físicos ni calcular costos, plazos o fechas de entrega.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Resolución local estable y validación del destino | DT-02 y DT-03 | CA-01 a CA-04 |
| I-02 | Asociación por F-02 y conservación de despachos previos | I-01 y DT-04 | CA-01 y CA-05 |
| I-03 | Consumo de Operación y rendimiento verificados | I-01/02 y DT-01/05 | CA-01 a CA-05 y coherencia entre consumidores |

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | San Isidro devuelve Lima Centro; F-02 asocia su identificador | Unitaria e integración PostgreSQL/F-02 | Datos locales reales; Operación inicialmente simulada |
| CA-02 | Sin zona activa, informa ausencia de cobertura sin zona por defecto | Integración de lectura y adaptador acordado | PostgreSQL |
| CA-03 | Zonas inactivas no cubren destinos | Integración | Datos locales |
| CA-04 | Sin distrito y código postal, rechaza sin resolver | Validación y adaptador acordado | Sin dependencia externa |
| CA-05 | Desactivar zona no cambia asociación de despachos existentes | Integración de regresión con F-02 | PostgreSQL |

Agregar destino solo con código postal, destino con ambos identificadores y repetición sin cambios, una vez resuelto DT-02. Comprobar coherencia entre consumidores, autorización de acceso remoto y respuesta en menos de 100 ms bajo las condiciones de DT-05. Ejecutar la suite del backend con su Maven Wrapper disponible y registrar comando exacto, revisión, preparación y resultados en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Fuente y motivo | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | Definir consumo de Operación: catálogo activo o resolución, ruta si corresponde, identidad, permisos y respuestas | F-01 RF-04; F-05 consume catálogo; Gestión §6 no define esa operación | Valqui con F-05 y Arquitectura | I-03 |
| DT-02 | Precisar normalización, destino solo postal y precedencia/conflicto de ambos identificadores | Original admite distrito o código postal; cotización exige distrito | Valqui con Backend y consumidores | I-01 y validación del adaptador |
| DT-03 | Verificar el esquema real y las consultas sobre `zonas_distritos` y `zonas_codigos_postales`; preservar los datos postales comunicados | Modelo §§1.2 y 3.1 actualizado el 26/10/2026; ES-F01-05 | Valqui con Arquitectura | Integración local |
| DT-04 | Acordar frontera de consistencia entre resolución y alta de despacho ante cambios concurrentes | F-01 exige configuración vigente y conservación de registros previos | Valqui con F-02 | I-02 |
| DT-05 | Acordar datos, carga, entorno y medición de menos de 100 ms | F-01 §8 | Valqui con DevOps y Calidad | Verificación de I-03 |

## 8. Condiciones para iniciar y cerrar

- [ ] Las decisiones del incremento están resueltas en el contrato o modelo propietario.
- [ ] F-02 y Operación consumen una sola fuente sin compartir persistencia.
- [ ] Se verifican destinos válidos, inválidos e inactivos y conservación de despachos.
- [ ] Todos los criterios tienen evidencia; las simulaciones se identifican.
- [ ] Integración real, rendimiento y revisión del equipo están registrados.

## 9. Referencias

1. [cite: 1] [Especificación](./spec.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [cite: 2] [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md), [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) y [modelo](../../arquitectura/modelo-datos.md).
3. [Flujo SDD](../../plantillas/sdd/README.md).
