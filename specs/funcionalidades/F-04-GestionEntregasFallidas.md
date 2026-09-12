# Especificación F-04: Entregas Fallidas y Reprogramaciones

**Responsable:** Gerardo
**Estado:** En especificación
**Actor principal:** Gestor de Despacho

## 1. Contexto

En la logística de última milla, una entrega puede fallar por ausencia del cliente, dirección no localizada, rechazo del paquete u otra incidencia operativa. El módulo de Despacho y Entrega debe administrar estas excepciones sin perder la trazabilidad del pedido ni interrumpir el flujo normal de los demás despachos.

La arquitectura del proyecto establece que cada módulo mantiene sus propios datos y se integra con los demás mediante APIs, sin acceso directo a bases de datos ajenas. Despacho y Entrega es responsable de la entidad despacho, mientras que Ventas y Postventa es responsable de la entidad pedido.

## 2. Propósito

Permitir que el Gestor de Despacho consulte las incidencias reportadas por los repartidores y decida si corresponde programar un nuevo intento de entrega o derivar el paquete a almacén. Toda decisión debe quedar registrada y, cuando se produzca una devolución, su resultado debe comunicarse a Ventas y Postventa.

## 3. Alcance

Esta funcionalidad incluye:

- Panel de despachos en estado `FALLIDO` con motivo, fecha, número de intento e información de evidencia disponible.
- Consulta del detalle y del historial de intentos de cada despacho.
- Validación del máximo de intentos permitido mediante una política configurable, cuyo valor inicial es dos.
- Reprogramación de una nueva fecha de entrega y retorno del despacho a la cola de asignación.
- Derivación del paquete a almacén cuando no corresponda un nuevo intento.
- Comunicación obligatoria del resultado de la devolución a Ventas y Postventa.
- Registro de auditoría para cada decisión y cambio de estado.

El mecanismo de comunicación con Ventas y Postventa, incluido si será síncrono o asíncrono, se definirá en el contrato único `specs/api-contract.md`.

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones

- El usuario debe estar autenticado y autorizado con el rol de Gestor de Despacho.
- El despacho debe existir y encontrarse en estado `FALLIDO`.
- El reporte de fallo debe contener, como mínimo, motivo, fecha, repartidor y número de intento.
- La política de intentos debe estar configurada; el valor inicial es de dos intentos.
- La nueva fecha de entrega debe ser posterior a la fecha actual.

### 4.2. Dependencias

| Dependencia | Responsabilidad |
|---|---|
| Seguridad y Usuarios | Proporcionar la identidad autenticada y los permisos del Gestor de Despacho. |
| Operación del repartidor (F-03) | Registrar el fallo inicial, su motivo y la evidencia disponible. |
| Programación y Asignación (F-02) | Recibir nuevamente los despachos reprogramados en la cola de asignación. |
| Ventas y Postventa | Recibir el resultado de una devolución a almacén para continuar el tratamiento del pedido. |

### 4.3. Resultados

- Una reprogramación válida cambia el estado a `PENDIENTE_ASIGNACION`, registra la nueva fecha y conserva el historial de intentos.
- La reprogramación no incrementa el contador; un nuevo intento se registra cuando el repartidor vuelve a ejecutar la entrega.
- Una derivación a almacén cambia el estado a `DEVUELTO_A_ALMACEN` y registra el resultado de su comunicación a Ventas y Postventa.
- Toda operación registra fecha, usuario, estado anterior, estado nuevo y observaciones aplicables.

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Consultar entregas fallidas

El sistema DEBE permitir que el Gestor de Despacho consulte los despachos en estado `FALLIDO`.

#### CA-01. Listado con incidencias

- **DADO** que existen despachos en estado `FALLIDO`.
- **CUANDO** el Gestor abre la pantalla de Entregas Fallidas.
- **ENTONCES** el sistema muestra el código de rastreo, fecha del incidente, motivo, número de intento y evidencia disponible.

#### CA-02. Listado sin incidencias

- **DADO** que no existen despachos en estado `FALLIDO`.
- **CUANDO** el Gestor abre la pantalla.
- **ENTONCES** el sistema muestra un estado vacío y no presenta información de otros estados.

#### CA-03. Acceso sin permisos

- **DADO** que un usuario sin el rol requerido intenta consultar las incidencias.
- **CUANDO** realiza la solicitud con su credencial de acceso.
- **ENTONCES** el backend rechaza la operación con `403 Forbidden` y no expone información del despacho.

### RF-02. Consultar el detalle de una incidencia

El sistema DEBE mostrar la información necesaria para decidir sobre un despacho fallido.

#### CA-04. Consulta de detalle exitosa

- **DADO** que existe un despacho en estado `FALLIDO`.
- **CUANDO** el Gestor abre su detalle.
- **ENTONCES** visualiza el motivo, fecha, repartidor, intento actual, historial de estados y evidencia disponible.

#### CA-05. Despacho inexistente

- **DADO** que el código consultado no corresponde a un despacho existente.
- **CUANDO** el Gestor solicita el detalle.
- **ENTONCES** el sistema informa que el recurso no existe y no presenta datos parciales.

### RF-03. Reprogramar un despacho

El sistema DEBE permitir una nueva fecha de entrega mientras no se haya alcanzado el máximo de intentos configurado.

#### CA-06. Reprogramación válida

- **DADO** que un despacho fallido tiene un intento registrado y el máximo configurado es dos.
- **CUANDO** el Gestor selecciona una fecha futura y confirma la reprogramación.
- **ENTONCES** el sistema cambia el estado a `PENDIENTE_ASIGNACION`, guarda la nueva fecha, conserva el contador en uno y registra la auditoría.

#### CA-07. Fecha inválida

- **DADO** que un despacho puede ser reprogramado.
- **CUANDO** el Gestor selecciona la fecha actual o una fecha pasada.
- **ENTONCES** el sistema rechaza la operación, explica la validación y mantiene el despacho en `FALLIDO`.

#### CA-08. Límite de intentos alcanzado

- **DADO** que el despacho alcanzó el máximo de intentos configurado.
- **CUANDO** el Gestor consulta su detalle o intenta reprogramarlo.
- **ENTONCES** el frontend deshabilita la reprogramación, el backend rechaza cualquier intento equivalente y solo se ofrece la derivación a almacén.

#### CA-09. Estado incompatible

- **DADO** que el despacho ya no se encuentra en estado `FALLIDO`.
- **CUANDO** se intenta reprogramar usando información desactualizada.
- **ENTONCES** el sistema rechaza la operación, conserva el estado vigente e informa que el despacho fue actualizado.

### RF-04. Derivar un paquete a almacén

El sistema DEBE permitir que el Gestor derive un despacho fallido a almacén y comunique el resultado a Ventas y Postventa.

#### CA-10. Derivación exitosa

- **DADO** que un despacho se encuentra en estado `FALLIDO`.
- **CUANDO** el Gestor confirma su derivación a almacén.
- **ENTONCES** el sistema cambia el estado a `DEVUELTO_A_ALMACEN`, registra la auditoría e inicia la comunicación del resultado a Ventas y Postventa.

#### CA-11. Operación repetida

- **DADO** que el despacho ya fue derivado a almacén.
- **CUANDO** se repite la misma operación.
- **ENTONCES** el sistema no duplica el cambio de estado, la auditoría de negocio ni la comunicación externa, e informa que la decisión ya fue procesada.

#### CA-12. Falla de la integración externa

- **DADO** que el despacho fue derivado a almacén.
- **CUANDO** no es posible comunicar el resultado a Ventas y Postventa.
- **ENTONCES** el sistema conserva el estado local, registra la comunicación como pendiente o fallida y deja evidencia suficiente para su reintento o tratamiento posterior.

El comportamiento anterior no determina todavía el protocolo, transporte ni estrategia técnica de reintentos.

### RF-05. Mantener trazabilidad

El sistema DEBE conservar un historial auditable de las decisiones realizadas sobre una entrega fallida.

#### CA-13. Registro de auditoría

- **DADO** que el Gestor reprograma o deriva un despacho a almacén.
- **CUANDO** la operación es aceptada.
- **ENTONCES** se registra el usuario, la fecha, el estado anterior, el estado nuevo y la información relevante de la decisión.

## 6. Frontend

La funcionalidad tendrá una experiencia web responsive compuesta por:

| Elemento | Responsabilidad |
|---|---|
| Pantalla de Entregas Fallidas | Mostrar filtros, listado paginado y estados de carga, vacío, error y éxito. |
| Detalle de la incidencia | Presentar motivo, intento actual, historial y evidencia disponible. |
| Formulario de reprogramación | Solicitar una fecha futura, validar la entrada y confirmar la operación. |
| Confirmación de devolución | Advertir el efecto de derivar el paquete a almacén antes de confirmar. |
| Retroalimentación | Informar resultados exitosos, validaciones, conflictos y errores de comunicación. |

La interfaz debe impedir acciones conocidas como inválidas, pero las mismas reglas siempre deben volver a validarse en el backend.

## 7. Backend

El backend deberá cubrir las siguientes responsabilidades lógicas:

| Componente lógico | Responsabilidad |
|---|---|
| Consulta de incidencias | Recuperar únicamente despachos fallidos, con filtros y paginación. |
| Consulta de detalle | Obtener el despacho, historial, motivo, intentos y evidencia disponible. |
| Caso de uso de reprogramación | Validar estado, fecha y límite antes de devolver el despacho a la cola de asignación. |
| Caso de uso de devolución | Cambiar el estado y solicitar la comunicación del resultado a Ventas y Postventa. |
| Política de intentos | Leer y aplicar el máximo configurable, inicialmente establecido en dos. |
| Persistencia y auditoría | Guardar cambios de estado y trazabilidad de manera consistente. |
| Adaptador de integración | Comunicar el resultado externo y registrar su éxito, estado pendiente o falla. |

Esta sección no prescribe nombres de clases, paquetes ni archivos. Las rutas, cuerpos, respuestas y códigos específicos se definirán en `specs/api-contract.md` y se publicarán mediante Swagger UI desde el backend desplegado.

## 8. Requisitos no funcionales

- **Seguridad:** todas las operaciones requieren una identidad válida y autorización de Gestor de Despacho.
- **Aislamiento:** no se accederá directamente a bases de datos pertenecientes a otros módulos.
- **Consistencia:** el cambio de estado y su auditoría deben persistirse de manera consistente.
- **Trazabilidad:** las decisiones y los intentos de integración deben poder consultarse posteriormente.
- **Usabilidad:** la pantalla debe ser responsive y comunicar con claridad estados vacíos, validaciones y errores.
- **Escalabilidad:** los listados deben admitir paginación para evitar cargar todas las incidencias en una sola solicitud.

## 9. Fuera de alcance

- **Reembolsos, extornos y notas de crédito:** pertenecen a Ventas y Postventa.
- **Captura inicial del fallo:** corresponde a la funcionalidad de Operación del Repartidor (F-03).
- **Reasignación a repartidor o vehículo:** corresponde a Programación y Asignación (F-02); F-04 solo devuelve el despacho a la cola.
- **Enrutamiento y optimización de rutas:** no forman parte de la gestión de la incidencia.
- **Definición del transporte de integración:** la elección entre comunicación síncrona, Webhook, mensajería u otra alternativa se acordará en el contrato de integración.

## 10. Estrategia de verificación

| Criterios | Verificación automatizada | Nivel | Evidencia esperada |
|---|---|---|---|
| CA-01 y CA-02 | Consultar datos con y sin incidencias y validar la representación correspondiente. | Integración y frontend | Pruebas exitosas del listado y sus estados visuales. |
| CA-03 | Ejecutar la consulta con un usuario sin permisos. | Integración de seguridad | Respuesta `403` y ausencia de datos protegidos. |
| CA-04 y CA-05 | Consultar un detalle existente y otro inexistente. | Integración y frontend | Datos completos para el caso válido y error controlado para el inexistente. |
| CA-06 a CA-09 | Probar fechas, límite configurable, transiciones y estado desactualizado. | Unitaria, integración y frontend | Reprogramación válida y rechazo de cada condición inválida. |
| CA-10 y CA-11 | Ejecutar una devolución y repetirla. | Unitaria e integración | Un único cambio, una única comunicación y auditoría sin duplicados. |
| CA-12 | Simular indisponibilidad de la integración externa. | Integración | Estado local conservado y comunicación registrada para tratamiento posterior. |
| CA-13 | Consultar la auditoría después de cada decisión aceptada. | Integración con persistencia | Usuario, fecha y transición almacenados correctamente. |

Además, se ejecutarán dos recorridos funcionales completos:

1. `FALLIDO` → reprogramación válida → `PENDIENTE_ASIGNACION`.
2. `FALLIDO` → derivación a almacén → `DEVUELTO_A_ALMACEN`.

Las pruebas unitarias cubrirán las reglas de negocio; las pruebas de integración cubrirán seguridad, persistencia PostgreSQL, auditoría e interacción entre componentes; y las pruebas del frontend cubrirán los estados visuales y formularios.

## 11. Criterio de completitud

La funcionalidad se considera completa cuando:

- Todos los criterios `CA-01` a `CA-13` están implementados y cuentan con pruebas exitosas.
- Los dos recorridos funcionales completos han sido verificados.
- Los cambios de estado y registros de auditoría persisten correctamente.
- La comunicación con Ventas y Postventa se ajusta al mecanismo finalmente acordado y su falla no se pierde silenciosamente.
- La interfaz muestra correctamente carga, estado vacío, validaciones, conflictos y errores.
- No se han incorporado capacidades declaradas fuera de alcance.
- La evidencia de pruebas puede relacionarse con cada criterio de aceptación.
