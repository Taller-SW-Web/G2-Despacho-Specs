# Plan de ES-F01-06: Cotizar el envío con datos físicos de productos

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**Actualización:** 04/11/2026. Se conserva la preparación de persistencia del 26/10 y se registra H cerrado, D-G2-01 cerrado el 03/11 y D-G2-02 cerrado semánticamente el 04/11. La sincronización normativa G6 y la verificación del consumidor tienen seguimiento propio. Implementación y pruebas funcionales se realizarán en el backend identificado al iniciar las tareas.

**UI:** No aplica. Marketplace y Chatbot presentan el resultado en sus propias interfaces; esta API no modifica pantallas del módulo ni requiere `ui.md`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-10 | Original en `91db8f8`; migración SDD del 16/10/2026 |
| Funcionalidad padre | [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-02, RF-03 y §8 | `91db8f8` |
| Contrato externo | [Cotización §5.1](../../integraciones/api-contract.md#51-solicitar-cotización), [Productos §5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas), §§3.4, 3.5 y 8 | `91db8f8` |
| Arquitectura y datos | [Contenedores §3.1](../../arquitectura/c4-contenedores.md#31-gestión-de-despachos), [modelo](../../arquitectura/modelo-datos.md), §§3.1 y 3.5 | `91db8f8` |
| Cobertura y tarifas | [ES-F01-05](../ES-F01-05-ConsultarCoberturaDestino/plan.md), [ES-F01-04](../ES-F01-04-ConfigurarTarifaZona/plan.md) | `91db8f8` |
| Seguimiento físico | [Contrato §§5.2.3, 5.2.4 y 11.1](../../integraciones/api-contract.md#111-homologación-física-g2g6-y-precisiones-de-seguimiento), CA-15 y CA-17 a CA-19 de [spec.md](./spec.md) | Fuentes del 02–04/11/2026; semántica H/D cerrada, merge proveedor `eeaf39a`; OpenAPI inspeccionado `6fcd81f`, aún rc.3 sin sincronización D (DT-08) |

Las decisiones pendientes se resuelven en sus documentos propietarios antes de implementar el incremento afectado [cite: 1, 2]. Las referencias de revisión de la tabla conservan la línea base original; para esta actualización rigen además el contrato §§5.1/5.2/11.1 y el modelo §§1.2/3.1 de la revisión que contenga estos cambios. El SQL y el estado de tablas fueron comunicados por la persona responsable, sin inspección de PostgreSQL en esta sesión.

## 2. Estrategia y responsabilidades

Gestión recibe la solicitud por Gateway, verifica identidad, destino y límite, resuelve cobertura y solo después valida las líneas. Agrupa cantidades por SKU, obtiene y valida el lote físico con credencial propia, aplica la elegibilidad homologada y calcula con la tarifa capturada. Antes de responder con costo confirma una instantánea en `cotizaciones`. La consulta de solo cobertura y los rechazos no escriben cotizaciones.

| Capa o aplicación | Responsabilidad | Elementos previstos |
|---|---|---|
| Gateway | Enrutamiento y control de tasa según acuerdo | Ruta existente de cotizaciones |
| Gestión | Orquestación, cobertura, tarifa, cálculo, persistencia exacta y errores | Caso de uso, adaptador de Productos y escritor de cotizaciones |
| Productos y Ofertas | Proveer datos físicos vigentes por SKU | API externa §5.2 |
| Seguridad y Usuarios | Emitir tokens de canal y de `modulo-despacho` | Credenciales y scopes por ambiente |
| Marketplace y Chatbot | Consumir costo logístico y estimación | Interfaz propia del canal |

## 3. Frontend y componentes React

No aplica. No se requieren componentes React ni mock visual del módulo. El doble de Productos se limita a pruebas del backend y no acredita integración real.

## 4. Backend, persistencia e integraciones

- Entrada: implementar la variante con `lineas` de la operación canónica de §5.1, compartiendo la resolución de cobertura con ES-F01-05/07. No validar líneas antes de descartar falta de cobertura.
- Caso de uso: agrupar cantidades sin cambiar la identidad del SKU, rechazar más de 100 únicos y validar la clasificación íntegra y exclusiva del lote antes de calcular. Aplicar elegibilidad por caso de uso; no compartir automáticamente la política comercial de F-01 con F-02. Usar aritmética decimal y la fórmula de F-01 RF-03 (DT-02).
- Datos locales: lectura de `zonas`, `zonas_distritos`, `zonas_codigos_postales`, `distrito` y tarifa vigente en Gestión, compartiendo resolución con ES-F01-05/07 (DT-03). La tabla postal con datos es un antecedente comunicado, no evidencia del lector.
- Persistencia: implementar el escritor de `cotizaciones` conforme al modelo §3.1; reutilizar la tabla creada, sin duplicar tablas de productos. Copiar destino, carga, términos tarifarios, totales y `detalle` con líneas, perfil usado, `actualizadoEn`, desglose y fecha estimada. `pedido_id`, `despacho_id` y `vence_en` quedan nulos, `es_simulado=false` y se conserva el estado físico inicial del DDL. No inferir UUID desde el `sub` técnico.
- Transacción: consultar G6 y obtener el cálculo/tarifa antes de abrir la escritura. Construir respuesta y fila desde el mismo resultado, insertar y confirmar antes de devolver `200 EXACTA`; fallos de inserción/commit revierten la fila y aplican el error interno del contrato, sin costo exitoso. No exigir idempotencia: repetir puede producir otra instantánea. No crear pedidos ni despachos.
- Migración: contrastar el DDL comunicado y los adaptadores contra el entorno; no recrear tablas ni reescribir migraciones aplicadas. Conciliar escalas, términos derivados y campos obligatorios del escritor en DT-02/07. El UUID opcional de pedido permanece nulo; una vinculación futura con `idPedido` textual requiere decisión y migración propias.
- Integración: utilizar la operación canónica del contrato §5.2 y token propio, sin propagar el del canal. Revisar `CatalogoProductosStub`, `@Primary`, perfiles y la selección de adaptadores en el backend; el perfil normal debe emitir HTTP real. Validar en contexto de aplicación esa selección; compartir transporte/validador con `productosProgramacion` sin duplicar reglas comerciales.
- Errores: distinguir por HTTP/código y esquema contractual el error físico, la inexistencia, la no elegibilidad y el fallo técnico. H-G2-01/02/03 están cerrados; contrastar el consumidor con `0.6.0-rc.3` (DT-06). Deserializar y conservar los SKU afectados sin extraerlos del texto libre ni usar todo el lote como sustituto.
- Precisiones D: consumir el estado efectivo calculado por G6 y aplicar la elegibilidad comercial únicamente en F-01. Incorporar el rechazo identificado del SKU padre y su traducción pública ya acordados en contrato §5.2.4, fijando la revisión exigible mediante DT-08. Validar lista obligatoria, tipos, pertenencia, identidad, unicidad y orden de solicitud; un error no conforme produce el `502` contractual. No convertir cualquier `SKU_INVALIDO` en SKU padre. Compartir el transporte y validador con F-02, no su política de estado. Un SKU de producto simple conserva el recorrido normal.
- Precedencia del proveedor: aplicar la regla aceptada del contrato §5.2.4, sin recalcularla desde G2 ni combinar afectados de distintas clases. En las permutaciones se conserva el código y el conjunto de afectados; su lista sigue el orden de cada solicitud. Un `200` íntegro con `noEncontrados` conserva el rechazo de inexistencia de §5.2.2.
- Calendario: calcular plazo y fecha con reloj controlable y calendario operativo acordado; no deducir feriados ni horas de corte no documentados (DT-02).
- Seguridad: autorización por scope antes de revelar cobertura; ignorar peso/volumen aportados por el cliente como datos autoritativos; no exponer reglas internas de tarifa.
- Concurrencia y efectos: capturar cobertura/tarifa de forma coherente; una sustitución posterior no reescribe instantáneas. La escritura exacta es el único efecto nuevo; sin eventos, cobros, reservas ni `Idempotency-Key`. Los estados de ciclo de vida del DDL no habilitan nuevos comandos.
- Configuración operativa: acordar tasa por `sub` e IP, timeout, caché y medición de latencia; no fijar valores nuevos en esta carpeta (DT-04).

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Motor, agrupación, integridad de lote y elegibilidad probados con datos controlados | DT-02/03 y reglas de DT-06 fijadas para el incremento | CA-01 a CA-05, CA-10, CA-14 a CA-16 |
| I-02 | Endpoint autorizado, cliente HTTP real y escritor exacto con errores diferenciados | I-01, DT-01, DT-05/06/07 | CA-01 a CA-08, CA-10 a CA-16 |
| I-04 | Precisiones de estado efectivo y error identificado, con regresiones de consumidor | I-02 y revisión normativa D-G2-01/02 enlazada en DT-08; aceptación semántica resuelta | CA-15, CA-17 a CA-19 |
| I-03 | Tasa, recorrido por Gateway e integración real G2 → G6 verificados | I-02, I-04 y DT-04 | CA-01 a CA-19 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | Totales, costo, plazo y fecha con tarifa vigente; incluir recargo sobre peso incluido | Unitaria e integración PostgreSQL | Productos simulado inicialmente; real al cierre |
| CA-02 | Sin cobertura, incluso con líneas inválidas: sin validar productos ni llamarlos | Integración con contador de llamadas | Doble de Productos |
| CA-03 | Lista vacía y cantidades cero/negativas en destino cubierto | Integración del endpoint | Datos locales |
| CA-04 | SKU desconocido identificado sin costo | Contrato e integración | Doble y proveedor real |
| CA-05 | Error de negocio G6 con SKU afectados, sin costo ni fila | Contrato e integración | Doble y datos controlados del proveedor; diferenciar `200` inválido de CA-14 |
| CA-06 | Fallo y timeout producen indisponibilidad, nunca estimación | Integración de fallos | Doble con fallos inyectados |
| CA-07 | Cobertura sin tarifa no inventa costo ni plazo | Integración | PostgreSQL; DT-01 resuelto |
| CA-08 | Token técnico válido sin sesión humana ni creación de pedido/despacho; instantánea exacta confirmada | Seguridad e integración | Tokens de prueba/reales y escritor de T-06 |
| CA-09 | Exceso de límite produce rechazo sin cálculo | Gateway e integración | Configuración real de tasa |
| CA-10 | Peso/volumen del cliente no alteran resultado | Integración | Datos de Productos controlados |
| CA-11 | Fila coherente con respuesta/tarifa; vínculos nulos, cambio posterior de tarifa y repetición | Integración PostgreSQL | Escritor y transacción reales |
| CA-12 | Cobertura y cada rechazo sin filas nuevas | Integración PostgreSQL | Comparación de estado antes/después |
| CA-13 | Fallos de inserción/commit, error interno y rollback | Integración de fallos | PostgreSQL real y fallos controlados |
| CA-14 | Omisiones, duplicados, inesperados, JSON ilegible, estado desconocido y campos inválidos | Contrato e integración | Respuestas controladas de G6 |
| CA-15 | Estados efectivos; variante activa con padre activo/inactivo/borrador, variantes no activas y productos simples | Contrato e integración | Nueve combinaciones de proveedor y lectura del estado recibido por G2 |
| CA-16 | 1/100/101 SKU únicos y cantidades acumuladas | Unitaria e integración | Contador de llamadas y valores decimales controlados |
| CA-17 | SKU padre solos/múltiples/mixtos, identidad opaca y producto simple válido | Contrato e integración PostgreSQL | Doble bajo revisión acordada; G6 real al cierre DT-08 |
| CA-18 | Detalle ausente, vacío, tipos incorrectos, duplicados y SKU no solicitados | Contrato e integración | Problemas controlados; `502`, sin costo ni fila |
| CA-19 | Permutar lote: mismo código/conjunto de afectados y lista en orden de cada solicitud | Contrato proveedor-consumidor | Precedencia y orden aceptados; revisión exigible fijada en DT-08 |

Verificar además selección del cliente HTTP con perfil normal, token ausente/inválido/vencido, audiencia incorrecta, scope ausente/correcto, token saliente propio y distrito ausente. Comparar ausencia de escrituras solo en cobertura/rechazos; los cálculos exactos deben persistirse. Para CA-01, el ejemplo suma `0.02126 m³` antes de redondear y el criterio conserva `0.021 m³`: DT-02 debe conciliar cálculo, salida y escalas del DDL sin redondeo intermedio. Ejecutar los tests afectados con el Maven Wrapper del backend y registrar comando exacto, revisión, reportes y latencias. La prueba con proveedor simulado no acredita E2E.

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Fuente y motivo | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | Completar respuesta para zona activa sin tarifa, sin inventar HTTP o código | F-01 CA-23; contrato §5.1 | Valqui con Backend y consumidores | CA-07 e I-02 |
| DT-02 | Precisar redondeo, escalas del DDL, calendario y correspondencia de peso volumétrico/cobrable con la fórmula existente | F-01 RF-03; modelo de `cotizaciones`; ejemplo y CA-01 | Valqui con Arquitectura y canales | I-01 y aceptación de cálculo/instantánea |
| DT-03 | Verificar lector distrital/postal y campos de tarifa contra esquema real; acordar precedencia con ES-F01-07 | Modelo §§1.2/3.1 y ES-F01-04/05/07 | Valqui con Arquitectura | Lectura local e I-01/02 |
| DT-04 | Acordar tasa, timeout, caché y medición de menos de 100 ms con Productos | F-01 §§4.1 y 8; contrato §11 | Valqui con DevOps y Productos | I-03 y rendimiento |
| DT-05 | Disponer de tokens, permisos y entorno de Productos; verificar consumo de canales | Contrato §§5.2, 8 y 11 | Valqui con Seguridad, Productos y canales | I-02 real e I-03 |
| DT-06 | Contrastar consumidor y matriz de errores contra H-G2-01/02/03 ya cerrados y la revisión fija `0.6.0-rc.3` | Contrato §11.1: aceptación del 02/11 y PR #108 enlazados; implementación G2 por verificar | Valqui con Productos y Calidad | Compatibilidad de I-02 e I-03; cierre contractual H ya acreditado |
| DT-07 | Verificar tabla creada, repositorio backend y mapeo del escritor; no habilitar vínculos o ciclo de vida no acordados | DDL comunicado y decisión de persistir solo exactas; modelo §§1.2 y 3.1 | Valqui con Backend y Arquitectura | Escritor real y CA-11 a CA-13 |
| DT-08 | Aceptación semántica resuelta; enlazar publicación normativa D-G2-01/02 y contrastar compatibilidad del consumidor | Aceptación G6 del 03/11 y final G2 del 04/11, contrato §11.1; merge `eeaf39a`. OpenAPI `6fcd81f` aún sin sincronización D | Valqui con Productos y Calidad; coordinar F-02 con Tarqui | Cierre de I-04 y regresiones D; preparar dobles del acuerdo cerrado y fijar revisión exigible antes de acreditar conformidad integral |

## 8. Condiciones para iniciar y cerrar

- [ ] Las entradas y decisiones bloqueantes del incremento están revisadas.
- [ ] Cobertura, tarifa, calendario y datos físicos tienen fuentes acordadas.
- [ ] Todos los criterios tienen tareas y resultados reproducibles.
- [ ] Las pruebas distinguen dobles de integración real y verifican seguridad, tasa y rendimiento.
- [ ] Revisión y commits de implementación están enlazados.

## 9. Referencias

1. [cite: 1] [Especificación](./spec.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
2. [cite: 2] [Contrato externo](../../integraciones/api-contract.md), [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md) y [modelo de datos](../../arquitectura/modelo-datos.md).
3. [Flujo SDD](../../plantillas/sdd/README.md).
