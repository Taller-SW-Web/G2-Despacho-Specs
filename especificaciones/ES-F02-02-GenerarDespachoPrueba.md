# ES-F02-02: Generación de despachos de prueba para simulación

**Funcionalidad padre:** F-02 — Programación y asignación de despachos  
**Responsable:** Tarqui  
**Estado:** Borrador  
**Actor principal:** Gestor de Despacho (aplicación web)

## 1. Objetivo

Permitir que el Gestor de Despacho o el equipo técnico autogenere de forma autónoma despachos simulados con datos válidos directamente en estado `PENDIENTE_ASIGNACION`. Esta funcionalidad provee carga de trabajo inmediata en la cola de programación para realizar pruebas de asignación, evaluar capacidades de furgonetas y verificar flujos operativos sin depender de órdenes reales ni de la disponibilidad del módulo de Ventas y Postventa.

## 2. Actor y precondiciones

- El actor está autenticado con el rol `GESTOR_DESPACHO` mediante token JWT.
- Existen zonas de cobertura en estado `ACTIVO` en F-01.
- El panel de programación o el cliente de API se encuentra disponible.

## 3. Flujo principal

1. El Gestor pulsa el botón secundario "Generar pedido de prueba" en la cabecera del panel de programación o invoca directamente el endpoint `POST /api/v1/despachos/simulaciones`.
2. Opcionalmente, la petición puede enviar parámetros de configuración específicos (ej. zona deseada, peso o volumen); de omitirse, el sistema utiliza valores generados automáticamente.
3. El backend valida el rol del usuario y los parámetros opcionales recibidos.
4. El sistema selecciona una zona de cobertura activa de F-01 y genera datos realistas y consistentes: identificador simulado de pedido (`PED-SIM-XXXXX`), nombre ficticio de destinatario, dirección de entrega válida dentro de la zona, peso (kg), volumen (m³), cantidad de paquetes (normalmente 1) y fecha programada igual al día actual.
5. El sistema genera el código operativo interno (`DSP-SIM-XXXXX`) y el código de rastreo (`TRK-SIM-XXXXX`).
6. Se crea el despacho en estado inicial `PENDIENTE_ASIGNACION` con la marca interna de despacho simulado y contador de intentos en cero.
7. Se registra el evento correspondiente en el historial de trazabilidad indicando el usuario ejecutor.
8. El backend responde `201 Created` retornando la información completa del despacho simulado.
9. En la interfaz web, el nuevo despacho se incorpora de inmediato a la cola de pendientes, muestra la etiqueta "Simulado", se resalta brevemente con la etiqueta temporal "Nuevo" y se despliega una notificación de confirmación.

## 4. Reglas y validaciones

- **Comportamiento operativo idéntico:** los despachos de prueba participan en todos los procesos regulares de la cola; pueden filtrarse, asignarse a repartidores, reordenarse en ruta, reasignarse y cancelarse bajo las mismas reglas de negocio que un despacho real.
- **Autogeneración por omisión:** si el payload de la petición está vacío (`{}`), el sistema asigna valores coherentes de forma aleatoria garantizando que la zona pertenezca a una zona activa de F-01 y que los valores físicos sean positivos y razonables.
- **Validación de parámetros personalizados:** si la petición define una zona o valores de carga específicos, se valida que la zona exista y esté activa, y que el peso, volumen y cantidad de paquetes sean mayores a cero; de lo contrario, se rechaza la solicitud.
- **Distintivo visual y metadatos:** todo despacho originado por simulación debe incluir el indicador booleano `esSimulacion=true` para que la interfaz lo identifique con el badge neutral punteado "Simulado".
- **Fecha programada inmediata:** la fecha programada se establece de forma predeterminada como la fecha de hoy para habilitar su asignación operativa inmediata sin restricciones temporales.
- **Seguridad:** el endpoint requiere estrictamente el rol `GESTOR_DESPACHO`; las invocaciones anónimas o con otros roles son rechazadas con `403 Forbidden`.

## 5. Entradas, salidas e integraciones

### Entradas

- Invocación `POST /api/v1/despachos/simulaciones`.
- Payload JSON opcional:
  - `idZona` (opcional, string).
  - `pesoKg` (opcional, decimal mayor a 0).
  - `volumenM3` (opcional, decimal mayor a 0).
  - `cantidadPaquetes` (opcional, entero mayor a 0).
  - `observaciones` (opcional, string).
- Encabezado `Authorization: Bearer <jwt_usuario>`.

### Salidas

- Respuesta HTTP `201 Created` con el detalle del despacho simulado:
  - `idDespacho`: identificador único interno (ej. `DSP-SIM-000245`).
  - `codigoRastreo`: código de seguimiento (ej. `TRK-SIM-000245`).
  - `idPedido`: referencia simulada (ej. `PED-SIM-000245`).
  - `estado`: `PENDIENTE_ASIGNACION`.
  - `idZona`, `direccionDestino`, `pesoKg`, `volumenM3`, `cantidadPaquetes`.
  - `fechaProgramada`: fecha de hoy.
  - `esSimulacion`: `true`.
- Notificación toast en frontend y actualización reactiva de la cola de pendientes.
- Error `400 Bad Request` si los parámetros personalizados contienen valores inconsistentes.
- Error `403 Forbidden` si el usuario no tiene permisos de gestor.

### Integraciones

- **Zonas y Cotizador (F-01):** consulta las zonas activas disponibles para ubicar geográficamente el despacho generado.
- **Cola de Pendientes (ES-F02-03):** recibe de inmediato el despacho creado para su visualización y filtrado.
- **Trazabilidad (ES-F02-08):** registra la creación del despacho de prueba en el historial.
- Las especificaciones técnicas de la ruta siguen `integraciones/api-contract.md` (Sección 9.2).

## 6. Criterios de aceptación

### CA-01. Generación autónoma exitosa con valores por omisión

- **DADO** un usuario autenticado con rol `GESTOR_DESPACHO`.
- **CUANDO** solicita la generación de un pedido de prueba sin especificar parámetros (payload vacío).
- **ENTONCES** el sistema crea un despacho en `PENDIENTE_ASIGNACION` con datos válidos en una zona activa de F-01, fecha de hoy, `esSimulacion=true`, responde `201 Created` y lo incorpora a la cola de pendientes.

### CA-02. Generación exitosa con parámetros personalizados

- **DADO** una solicitud de simulación que especifica una zona activa válida y un peso de 12.5 kg.
- **CUANDO** el Gestor confirma la petición.
- **ENTONCES** el sistema crea el despacho simulado respetando la zona y el peso indicados, autogenera el resto de los campos consistentes y responde `201 Created`.

### CA-03. Rechazo por parámetros inválidos

- **DADO** una solicitud de simulación con un peso menor o igual a cero o con un identificador de zona inexistente o inactiva en F-01.
- **CUANDO** la petición es procesada.
- **ENTONCES** el sistema responde `400 Bad Request` o `422 Unprocessable Entity` detallando el error y no genera ningún registro.

### CA-04. Acceso sin permisos

- **DADO** un usuario sin el rol `GESTOR_DESPACHO` o sin token de autenticación.
- **CUANDO** intenta invocar el endpoint de simulaciones.
- **ENTONCES** el backend responde `403 Forbidden` y no expone datos operativos.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Conexión o sincronización con el módulo de Ventas y Postventa (la simulación es puramente interna al módulo de Despacho).
- Asignación automática o inmediata a furgonetas (el despacho debe asignarse mediante el flujo regular de ES-F02-04).

### Referencias

- Funcionalidad padre: `funcionalidades/F-02-ProgramacionAsignacionDespachos.md` (RF-09, CA-20).
- Historia de usuario: `historias-usuario/F-02-ProgramacionAsignacionDespachos/HU-F02-02-GeneracionPedidosPrueba.md`.
- Contrato de API: `integraciones/api-contract.md` (Sección 9.2).
- Diseño de interfaz: `disenio/funcionalidades/f-02.md` (Pantalla 1).
