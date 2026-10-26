# ES-F01-07: Resolver la zona de un destino para el módulo

**Funcionalidad padre:** [F-01 — Gestor de zonas geográficas y cotizador de envíos](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md)

**Responsable:** Valqui

**Estado:** Borrador

**Actor principal:** Programación y asignación (F-02)

**UI:** No aplica. Es una resolución interna consumida por casos de uso; no crea ni modifica pantallas.

**Servicio propietario:** Gestión de Despachos.

**Origen:** Especificación de la revisión `91db8f8`, migrada al flujo SDD el 16/10/2026; conserva los criterios CA-01 a CA-05.

## 1. Contexto y objetivo

Determinar qué zona de cobertura activa contiene un destino y entregar esa resolución a las funcionalidades que la necesitan. F-02 la utiliza al crear un despacho para asociarle su zona o para rechazar el destino, y F-05 la utiliza para asignar la zona de trabajo de un repartidor en su jornada. Al ser F-01 la fuente única de cobertura del módulo, ninguna otra funcionalidad mantiene reglas propias de cobertura.

## 2. Alcance

- Incluye: resolver el destino contra la cobertura activa vigente y entregar zona o ausencia de cobertura; mantener una fuente única para los consumidores.
- Fuera de alcance: calcular costo, plazo o fecha estimada; administrar zonas y tarifas; registrar o reasignar despachos; abrir o cerrar jornadas. La definición de la comunicación entre microservicios corresponde al contrato de Gestión, no a esta carpeta.

## 3. Actor, precondiciones y resultados

- El consumidor es una funcionalidad interna del módulo que actúa con identidad de servicio.
- El destino se identifica con `distrito`, `codigoPostal` o ambos.
- Las zonas y su delimitación se encuentran persistidas por esta misma funcionalidad.
- El destino puede o no estar cubierto; ambos resultados son respuestas válidas.
- Disparador: F-02 necesita asociar la zona a una solicitud o F-05 necesita información de cobertura para su operación.
- Resultado exitoso: zona identificada y destino normalizado, o ausencia de cobertura, sin mutaciones.
- Resultado ante rechazo: destino no identificable rechazado sin asignar una zona por defecto.

## 4. Flujo principal y alternativas

1. F-02 recibe una solicitud de despacho o F-05 prepara la asignación de una jornada y obtiene el destino.
2. El consumidor solicita la resolución de zona con los datos del destino.
3. El backend busca la zona en estado `ACTIVO` que contiene el distrito o el código postal.
4. El sistema devuelve el identificador y el nombre de la zona, junto con los datos normalizados del destino.
5. El consumidor asocia la zona a su operación o declara que el destino no tiene cobertura.

| Alternativa | Condición | Comportamiento esperado | Criterio |
|---|---|---|---|
| Sin cobertura | Ninguna zona activa contiene el destino | Respuesta sin zona y con indicación de ausencia de cobertura | CA-02 |
| Solo zonas inactivas | La zona fue desactivada | No resuelve nuevas operaciones | CA-03 |
| Destino no identificable | Faltan distrito y código postal | Rechaza sin zona por defecto | CA-04 |
| Despachos previos | Ya tienen una zona asociada | Conservan su asociación aunque cambie la cobertura | CA-05 |

## 5. Reglas, datos e integraciones

### Reglas y validaciones

- Solo las zonas en estado `ACTIVO` resuelven cobertura; una zona `INACTIVO` se trata como si no existiera.
- Un destino no cubierto se responde `200 OK` con `coberturaDisponible: false`, sin zona y con el mensaje de destino fuera de cobertura.
- La resolución no crea, edita ni cambia el estado de ninguna zona ni de ningún despacho.
- La zona devuelta es la vigente en el momento de la resolución; un cambio posterior de estado no modifica los registros ya asociados.
- La resolución no aplica tarifas ni calcula costos: esos datos corresponden al motor de cotización de [ES-F01-06](../ES-F01-06-CotizarEnvioConProductos/spec.md).
- El consumidor no puede forzar una zona distinta de la que resulta de la cobertura, ni declarar cobertura cuando el sistema la niega.
- La resolución debe ser estable para el mismo destino mientras la configuración no cambie, de modo que F-02 y F-05 observen la misma zona.
- Un destino sin `distrito` ni `codigoPostal` identificables no puede resolverse y se rechaza con `400 Bad Request`.

### Entradas

- Datos del destino: `distrito` o `codigoPostal` identificable; `direccion` opcional. La obligatoriedad por consumidor y la combinación de ambos se revisarán en el contrato antes de implementar el adaptador.
- Identidad de servicio del consumidor interno.

### Salidas

- Identificador y nombre de la zona que cubre el destino, o la declaración de que no existe cobertura.
- Datos normalizados del destino utilizados en la resolución.
- Error normalizado cuando el destino no es identificable.

### Integraciones

- F-02 consume la resolución al crear un despacho y rechaza los destinos sin cobertura.
- F-05 consume el catálogo de zonas activas para asignar la zona de trabajo del repartidor.
- El mecanismo concreto por el que F-05, que pertenece al microservicio de Operación de Reparto y Flota, acceda a esta resolución no está definido en la [API interna de Gestión, sección 6](../../integraciones/api-contract-gestion-despachos.md#6-api-interna-provista-por-gestión) y permanece como acuerdo pendiente de documentar en ese contrato [cite: 2].
- La zona es propiedad de Gestión de Despachos; ningún consumidor accede a su base de datos.
- La resolución local usa `zonas_distritos` para distrito y `zonas_codigos_postales` como fuente postal canónica, conforme al modelo. La existencia de datos postales fue comunicada el 26/10/2026; el uso efectivo por el lector y la precedencia ante ambos identificadores siguen pendientes de verificar [cite: 3].
- Esta resolución no inserta en `cotizaciones`; el histórico de cálculos exactos se escribe exclusivamente desde ES-F01-06 y no determina la zona de una recepción nueva.

## 6. Criterios de aceptación

### CA-01. Resolución de un destino cubierto

- **DADO** una solicitud de despacho con destino en San Isidro, que pertenece a "Lima Centro".
- **CUANDO** F-02 solicita la resolución de zona.
- **ENTONCES** el sistema devuelve el identificador y el nombre de "Lima Centro" y F-02 los asocia al despacho.

### CA-02. Resolución de un destino sin cobertura

- **DADO** un destino cuyo distrito o código postal no pertenece a ninguna zona activa.
- **CUANDO** el consumidor solicita la resolución.
- **ENTONCES** el sistema responde `200 OK` con `coberturaDisponible: false`, sin zona y con el mensaje de destino fuera de cobertura.

### CA-03. Destino cubierto por una zona desactivada

- **DADO** un destino que solo pertenece a zonas en estado `INACTIVO`.
- **CUANDO** el consumidor solicita la resolución.
- **ENTONCES** el sistema lo declara sin cobertura, porque la desactivación retira la zona de la cobertura efectiva.

### CA-04. Destino no identificable

- **DADO** una solicitud que no informa `distrito` ni `codigoPostal`.
- **CUANDO** el consumidor solicita la resolución.
- **ENTONCES** el sistema responde `400 Bad Request` y no devuelve una zona por defecto.

### CA-05. Zona desactivada con despachos existentes

- **DADO** una zona desactivada con despachos ya registrados.
- **CUANDO** se consulta la resolución de uno de esos destinos.
- **ENTONCES** los despachos existentes conservan la zona con la que fueron creados, aunque la zona ya no resuelva cobertura para destinos nuevos.

## 7. UI, backend y requisitos no funcionales

- UI: no aplica; es un servicio de resolución sin interacción visual nueva. No se incluye `ui.md`.
- Backend: Gestión es propietario de cobertura; F-02 reutiliza el caso de uso local y Operación consume únicamente la comunicación que se acuerde, sin compartir tablas.
- Requisitos no funcionales: resolución estable mientras no cambie la configuración; aislamiento de datos e identidad de servicio para comunicación remota. F-01 §8 exige respuesta en menos de 100 ms; condiciones de medición pendientes [cite: 1].
- Pendientes: contrato de consumo desde Operación, normalización y precedencia de distrito/código postal, conciliación del modelo y medición; detalle en [plan.md §7](./plan.md#7-decisiones-y-pendientes).

## 8. Verificación y completitud

| Criterio | Tipo de comprobación | Datos o escenario necesarios |
|---|---|---|
| CA-01 | Integración con F-02 | San Isidro en Lima Centro; despacho asociado a la zona resuelta |
| CA-02 | Integración | Destino fuera de toda zona activa |
| CA-03 | Integración | Destino cubierto únicamente por zonas inactivas |
| CA-04 | Validación | Ausencia de distrito y código postal |
| CA-05 | Integración de regresión | Despacho previo asociado y zona posteriormente desactivada |

- [ ] CA-01 a CA-05 cuentan con evidencia reproducible en [evidence.md](./evidence.md).
- [ ] Los consumidores comparten la misma resolución sin acceso cruzado a tablas.
- [ ] Los acuerdos que afectan integración y medición están revisados y documentados.
- [ ] Commits y revisión funcional y técnica están enlazados.

Las tareas están en [tasks.md](./tasks.md); la migración documental no acredita implementación.

## 9. Referencias

- [cite: 1] [Funcionalidad F-01](../../funcionalidades/F-01-Gestor_ZonasGeograficas.md), RF-04, CA-02, CA-12 y CA-13; §8.
- [cite: 2] [Contrato de Gestión](../../integraciones/api-contract-gestion-despachos.md), §§3.1 y 6; [convenciones compartidas](../../integraciones/api-contract.md#3-convenciones-comunes), §§3.2 y 3.4.
- [cite: 3] [Modelo de datos](../../arquitectura/modelo-datos.md), tablas de cobertura `zonas`, `zonas_distritos`, `distrito` y `zonas_codigos_postales`.
- [cite: 4] [Visión general](../../overview.md), §§3.1 y 3.2 sobre relaciones entre F-01, F-02 y F-05.
- [cite: 5] [Macroproceso](../../arquitectura/macroproceso-despacho.md), solicitud de despacho y resolución de zona.
- Documentos SDD: [plan](./plan.md), [tareas](./tasks.md) y [evidencia](./evidence.md).
