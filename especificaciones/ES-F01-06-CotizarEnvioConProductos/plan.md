# Plan de ES-F01-06: Cotizar el envío con datos físicos de productos

**Responsable:** Valqui.

**Estado:** Borrador; pendiente de revisión técnica e implementación.

**UI:** No aplica. Marketplace y Chatbot presentan el resultado en sus propias interfaces; esta API no modifica pantallas del módulo ni requiere `ui.md`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-10 | Original en `91db8f8`; migración SDD del 16/10/2026 |
| Funcionalidad padre | [F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-02, RF-03 y §8 | `91db8f8` |
| Contrato externo | [Cotización §5.1](../../integraciones/api-contract.md#51-solicitar-cotización), [Productos §5.2](../../integraciones/api-contract.md#52-integración-de-despacho-con-productos-y-ofertas), §§3.4, 3.5 y 8 | `91db8f8` |
| Arquitectura y datos | [Contenedores §3.1](../../arquitectura/c4-contenedores.md#31-gestión-de-despachos), [modelo](../../arquitectura/modelo-datos.md), §§3.1 y 3.5 | `91db8f8` |
| Cobertura y tarifas | [ES-F01-05](../ES-F01-05-ConsultarCoberturaDestino/plan.md), [ES-F01-04](../ES-F01-04-ConfigurarTarifaZona/plan.md) | `91db8f8` |

Las decisiones pendientes se resuelven en sus documentos propietarios antes de implementar el incremento afectado [cite: 1, 2].

## 2. Estrategia y responsabilidades

Gestión recibe la solicitud por Gateway, verifica identidad, destino y límite, resuelve cobertura y solo después valida las líneas. Agrupa SKU, obtiene sus datos físicos en lote con credencial propia, calcula totales y aplica la regla vigente. La cotización es de solo cálculo y lectura.

| Capa o aplicación | Responsabilidad | Elementos previstos |
|---|---|---|
| Gateway | Enrutamiento y control de tasa según acuerdo | Ruta existente de cotizaciones |
| Gestión | Orquestación, cobertura, tarifa, cálculo y errores | Caso de uso de cotización y adaptador de Productos |
| Productos y Ofertas | Proveer datos físicos vigentes por SKU | API externa §5.2 |
| Seguridad y Usuarios | Emitir tokens de canal y de `modulo-despacho` | Credenciales y scopes por ambiente |
| Marketplace y Chatbot | Consumir costo logístico y estimación | Interfaz propia del canal |

## 3. Frontend y componentes React

No aplica. No se requieren componentes React ni mock visual del módulo. El doble de Productos se limita a pruebas del backend y no acredita integración real.

## 4. Backend, persistencia e integraciones

- Entrada: implementar la variante con `lineas` de la operación canónica de §5.1, compartiendo la resolución de cobertura con ES-F01-05/07. No validar líneas antes de descartar falta de cobertura.
- Caso de uso: agrupar cantidades por SKU; consultar cada SKU una vez en el lote; validar peso y dimensiones; calcular las magnitudes y costo con la fórmula de F-01 RF-03. Utilizar aritmética decimal y concretar redondeo antes del adaptador final (DT-02).
- Datos locales: lectura de zonas, delimitación y tarifa vigente en Gestión; conciliar nombres de tablas y correspondencia de campos tarifarios con ES-F01-04/05 (DT-03). No persistir cotizaciones ni crear despachos.
- Migración: no se propone tabla nueva; verificar el esquema y preparar solo las migraciones acordadas para las fuentes locales.
- Integración: usar el contrato de Productos §5.2 y el token propio con audiencia y scope acordados; nunca propagar el token del canal. Ante indisponibilidad, responder el error contractual sin aproximar el costo.
- Calendario: calcular plazo y fecha con reloj controlable y calendario operativo acordado; no deducir feriados ni horas de corte no documentados (DT-02).
- Seguridad: autorización por scope antes de revelar cobertura; ignorar peso/volumen aportados por el cliente como datos autoritativos; no exponer reglas internas de tarifa.
- Concurrencia y efectos: usar una lectura coherente de cobertura y tarifa para cada cálculo; no modifica recursos, no publica eventos ni requiere `Idempotency-Key`.
- Configuración operativa: acordar tasa por `sub` e IP, timeout, caché y medición de latencia; no fijar valores nuevos en esta carpeta (DT-04).

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Motor de cálculo, agrupación y validaciones probados con datos controlados | DT-02 y DT-03 | CA-01 a CA-05, CA-10 |
| I-02 | Endpoint autorizado y adaptador de Productos con manejo de fallos | I-01, DT-01 y DT-05 | CA-01 a CA-08, CA-10 |
| I-03 | Tasa, recorrido por Gateway e integración real verificados | I-02 y DT-04 | CA-01 a CA-10 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | Totales, costo, plazo y fecha con tarifa vigente; incluir recargo sobre peso incluido | Unitaria e integración PostgreSQL | Productos simulado inicialmente; real al cierre |
| CA-02 | Sin cobertura, incluso con líneas inválidas: sin validar productos ni llamarlos | Integración con contador de llamadas | Doble de Productos |
| CA-03 | Lista vacía y cantidades cero/negativas en destino cubierto | Integración del endpoint | Datos locales |
| CA-04 | SKU desconocido identificado sin costo | Contrato e integración | Doble y proveedor real |
| CA-05 | Peso/dimensiones ausentes o no positivos sin costo | Contrato e integración | Datos controlados del proveedor |
| CA-06 | Fallo y timeout producen indisponibilidad, nunca estimación | Integración de fallos | Doble con fallos inyectados |
| CA-07 | Cobertura sin tarifa no inventa costo ni plazo | Integración | PostgreSQL; DT-01 resuelto |
| CA-08 | Token técnico válido sin sesión humana; sin creación de recursos | Seguridad e integración | Tokens de prueba y reales |
| CA-09 | Exceso de límite produce rechazo sin cálculo | Gateway e integración | Configuración real de tasa |
| CA-10 | Peso/volumen del cliente no alteran resultado | Integración | Datos de Productos controlados |

Verificar además token ausente/sin scope, distrito ausente, SKU repetidos, sustitución de tarifa y ausencia de escrituras. Para CA-01, contrastar la precisión: el ejemplo de Productos suma `0.02126 m³` antes de redondear, mientras el criterio conserva `0.021 m³`; DT-02 debe definir la precisión de salida y cálculo. Ejecutar la suite del repositorio backend con su Maven Wrapper disponible; registrar comando exacto, revisión, datos, reportes y latencias en [evidence.md](./evidence.md).

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Fuente y motivo | Responsable | Bloquea |
|---|---|---|---|---|
| DT-01 | Completar respuesta para zona activa sin tarifa, sin inventar HTTP o código | F-01 CA-23; contrato §5.1 | Valqui con Backend y consumidores | CA-07 e I-02 |
| DT-02 | Precisar redondeo, escala, calendario y cálculo de fecha | F-01 RF-03; ejemplo de Productos y CA-01 | Valqui con Arquitectura y canales | I-01 y aceptación de CA-01 |
| DT-03 | Conciliar `zona_distritos`/`zonas_distritos`, campos de peso y plazo de tarifa | Modelo §§3.1 y 6; ES-F01-04/05 | Valqui con Arquitectura | Lectura local e I-01/02 |
| DT-04 | Acordar tasa, timeout, caché y medición de menos de 100 ms con Productos | F-01 §§4.1 y 8; contrato §11 | Valqui con DevOps y Productos | I-03 y rendimiento |
| DT-05 | Disponer de tokens, permisos y entorno de Productos; verificar consumo de canales | Contrato §§5.2, 8 y 11 | Valqui con Seguridad, Productos y canales | I-02 real e I-03 |

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
