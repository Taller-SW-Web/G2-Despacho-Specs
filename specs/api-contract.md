# Contrato Único de Comunicación API (Frontend - Backend)

Este documento representa el **único contrato oficial de comunicación** entre las aplicaciones cliente (paneles web administrativos, web responsive del repartidor, consultas de seguimiento e integraciones externas) y los servicios backend del módulo de Despacho. Toda interacción HTTP debe ajustarse a las especificaciones aquí descritas.

> **Estado:** En consolidación. La numeración y los responsables ya están alineados con el índice vigente; los detalles de cada endpoint se revisarán conforme se completen las especificaciones funcionales.

---

## 1. Convenciones Generales y Transversales

### 1.1 Formato y Codificación
- Todas las peticiones y respuestas utilizan formato `application/json` con codificación UTF-8.
- Las fechas y marcas de tiempo siguen el estándar ISO 8601 en UTC (`YYYY-MM-DDTHH:mm:ssZ`).
- Las claves de objetos JSON utilizan formato `camelCase`.
- Los valores de estados, códigos de error o enumeraciones utilizan formato `UPPER_SNAKE_CASE`.

### 1.2 Seguridad, Autenticación y Autorización
Todas las llamadas protegidas requieren el encabezado estándar:
```http
Authorization: Bearer <token_jwt>
```
El token JWT emitido por el servicio central de Seguridad contiene los datos del usuario y su rol:
- `ADMIN`: Control total de catálogos y zonas.
- `GESTOR_DESPACHO`: Operación de programación, asignación e incidencias (F-02, F-04).
- `GESTOR_FLOTA`: Administración de flota vehicular y conductores (F-05).
- `REPARTIDOR`: Acceso exclusivo a su hoja de ruta y registro de evidencias (F-03).
- **Acceso Público:** Los endpoints de cotización para clientes (F-01) y las consultas públicas de seguimiento no exigen token JWT de usuario. El seguimiento es una capacidad transversal y no constituye una funcionalidad numerada.

### 1.3 Estructura Estándar de Errores
Cuando una operación no resulta exitosa (`4xx` o `5xx`), el cuerpo de respuesta adopta la siguiente estructura:
```json
{
  "codigo": "DESP_ERROR_CAPACIDAD_EXCEDIDA",
  "mensaje": "La capacidad remanente del repartidor es insuficiente para este paquete",
  "detalles": [
    "Peso requerido: 30.0 kg, Peso remanente: 20.0 kg"
  ],
  "timestamp": "2026-09-11T20:50:00Z"
}
```

### 1.4 Integración Asíncrona Común (Webhooks hacia Ventas y Devoluciones)
El backend cuenta con una función común que dispara eventos asíncronos cuando se alcanzan estados terminales:
- **Evento `DESPACHO_ENTREGADO`:** Emitido cuando el repartidor marca `ENTREGADO` con foto y firma (notifica a Ventas/Postventa).
- **Evento `DESPACHO_DEVUELTO_ALMACEN`:** Emitido cuando el Gestor de Incidencias marca `DEVUELTO_A_ALMACEN` (notifica a Devoluciones y Ventas).

---

## 2. Endpoints: F-01 - Gestor de Zonas Geográficas y Cotizador de Envíos (Valqui)

### 2.1 Cotizar Costo y Tiempo de Envío
Calcula la tarifa de flete y plazo estimado a partir de la dirección o zona de destino, peso y volumen.

- **Método:** `POST`
- **Ruta:** `/api/v1/zonas/cotizar`
- **Autenticación:** Pública (o API Key de canal comercial)
- **Cuerpo de la Solicitud (Request Body):**
```json
{
  "distrito": "Miraflores",
  "codigoPostal": "15074",
  "coordenadas": {
    "latitud": -12.1215,
    "longitud": -77.0298
  },
  "pesoKg": 4.5,
  "volumenM3": 0.02
}
```
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "coberturaDisponible": true,
  "idZona": "ZONA-LIMA-CENTRO",
  "nombreZona": "Lima Moderna / Centro",
  "costoEnvio": 12.50,
  "moneda": "PEN",
  "plazoEstimadoDias": 1,
  "mensaje": "Cobertura confirmada para entrega al día siguiente"
}
```

### 2.2 Listar Zonas de Cobertura
- **Método:** `GET`
- **Ruta:** `/api/v1/zonas`
- **Rol requerido:** `ADMIN`, `GESTOR_DESPACHO`

---

## 3. Endpoints: F-02 - Panel de Programación y Asignación de Despachos (Tarqui)

### 3.1 Recepción de Solicitud de Despacho
Registra una solicitud formal de despacho proveniente de Ventas o integraciones autorizadas.

- **Método:** `POST`
- **Ruta:** `/api/v1/despachos/solicitudes`
- **Rol requerido:** `GESTOR_DESPACHO` o `SISTEMA_VENTAS`
- **Cuerpo de la Solicitud (Request Body):**
```json
{
  "idPedido": "PED-2026-00891",
  "destinatario": {
    "nombre": "Carlos Mendoza",
    "telefono": "+51987654321",
    "email": "carlos.mendoza@example.com"
  },
  "direccionEntrega": "Av. Javier Prado Este 2465, San Borja, Lima",
  "coordenadas": {
    "latitud": -12.08945,
    "longitud": -77.00342
  },
  "pesoKg": 12.5,
  "volumenM3": 0.08,
  "fechaEstimadaEntrega": "2026-09-15"
}
```
- **Respuesta Exitosa (`201 Created`):**
```json
{
  "idDespacho": "DSP-100234",
  "idPedido": "PED-2026-00891",
  "codigoRastreo": "TRK-78901",
  "estado": "PENDIENTE_ASIGNACION",
  "fechaCreacion": "2026-09-11T20:50:00Z"
}
```

### 3.2 Generación de Despacho de Prueba (Modo Autónomo / Testing)
Genera órdenes y despachos simulados con datos válidos para que el equipo pueda probar la cola sin depender del avance de otros módulos.

- **Método:** `POST`
- **Ruta:** `/api/v1/despachos/solicitudes/simular`
- **Rol requerido:** `GESTOR_DESPACHO`
- **Cuerpo de la Solicitud (Request Body):** *(Opcional, puede enviarse `{}` para autogenerar todo)*
```json
{
  "zona": "ZONA-LIMA-CENTRO",
  "pesoKg": 5.0
}
```
- **Respuesta Exitosa (`201 Created`):**
```json
{
  "idDespacho": "DSP-SIM-54321",
  "idPedido": "PED-SIM-98765",
  "codigoRastreo": "TRK-SIM-12345",
  "estado": "PENDIENTE_ASIGNACION",
  "direccionEntrega": "Calle de Prueba 123, Miraflores, Lima",
  "pesoKg": 5.0,
  "volumenM3": 0.03,
  "fechaEstimadaEntrega": "2026-09-12"
}
```

### 3.3 Listar Cola de Despachos Pendientes
- **Método:** `GET`
- **Ruta:** `/api/v1/despachos/pendientes`
- **Rol requerido:** `GESTOR_DESPACHO`
- **Parámetros de Consulta:** `pagina` (int), `limite` (int), `zona` (string), `ordenarPor` (enum).
- **Respuesta Exitosa (`200 OK`):** Retorna lista paginada de despachos con estado `PENDIENTE_ASIGNACION`.

### 3.4 Asignar Despacho a Repartidor
- **Método:** `POST`
- **Ruta:** `/api/v1/despachos/{idDespacho}/asignar`
- **Rol requerido:** `GESTOR_DESPACHO`
- **Cuerpo de la Solicitud:**
```json
{
  "idRepartidor": "REP-0012",
  "observaciones": "Entrega prioritaria de mañana"
}
```
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idDespacho": "DSP-100234",
  "idRepartidor": "REP-0012",
  "estado": "ASIGNADO",
  "fechaAsignacion": "2026-09-11T20:51:00Z"
}
```
- **Respuestas de Error:** `409 Conflict` (repartidor fuera de turno o despacho ya asignado), `422 Unprocessable Entity` (sobrecarga de peso o volumen).

---

## 4. Endpoints: F-03 - Web Responsive del Repartidor y Evidencia de Entrega (Max)

### 4.1 Obtener Mi Ruta del Día
Retorna los despachos asignados al repartidor autenticado.

- **Método:** `GET`
- **Ruta:** `/api/v1/repartidor/mi-ruta`
- **Rol requerido:** `REPARTIDOR`
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idRepartidor": "REP-0012",
  "fecha": "2026-09-11",
  "totalDespachos": 8,
  "despachos": [
    {
      "idDespacho": "DSP-100234",
      "secuenciaRuta": 1,
      "destinatario": "Carlos Mendoza",
      "telefono": "+51987654321",
      "direccion": "Av. Javier Prado Este 2465, San Borja",
      "coordenadas": { "latitud": -12.08945, "longitud": -77.00342 },
      "estado": "ASIGNADO",
      "itemsResumen": "1x Laptop, 1x Mouse"
    }
  ]
}
```

### 4.2 Iniciar Traslado hacia el Destino
- **Método:** `PATCH`
- **Ruta:** `/api/v1/despachos/{idDespacho}/iniciar-traslado`
- **Rol requerido:** `REPARTIDOR`
- **Respuesta Exitosa (`200 OK`):** Transiciona a estado `EN_CAMINO`.

### 4.3 Registrar Entrega Exitosa (Evidencia Fotográfica y Firma)
- **Método:** `POST`
- **Ruta:** `/api/v1/despachos/{idDespacho}/evidencia-entrega`
- **Rol requerido:** `REPARTIDOR`
- **Cuerpo de la Solicitud (Request Body):**
```json
{
  "receptor": {
    "nombre": "Carlos Mendoza",
    "documentoIdentidad": "45678912",
    "parentesco": "TITULAR"
  },
  "fotoPaqueteBase64": "data:image/jpeg;base64,...",
  "firmaDigitalBase64": "data:image/png;base64,...",
  "coordenadasEntrega": {
    "latitud": -12.08945,
    "longitud": -77.00342
  }
}
```
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idDespacho": "DSP-100234",
  "estado": "ENTREGADO",
  "fechaEntrega": "2026-09-11T20:52:00Z",
  "mensaje": "Entrega confirmada y evidencia guardada exitosamente"
}
```

### 4.4 Registrar Entrega Fallida
- **Método:** `POST`
- **Ruta:** `/api/v1/despachos/{idDespacho}/registrar-fallo`
- **Rol requerido:** `REPARTIDOR`
- **Cuerpo de la Solicitud:**
```json
{
  "motivo": "CLIENTE_AUSENTE",
  "comentario": "Se timbró 3 veces y se llamó al teléfono sin respuesta",
  "fotoFachadaBase64": "data:image/jpeg;base64,..."
}
```
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "idDespacho": "DSP-100234",
  "estado": "FALLIDO",
  "numeroIntento": 1,
  "mensaje": "Fallo registrado y derivado al centro de excepciones"
}
```

### 4.5 Catálogo Oficial de Motivos de Fallo
- **Método:** `GET`
- **Ruta:** `/api/v1/catalogos/motivos-fallo`
- **Autenticación:** Requerida (`REPARTIDOR`, `GESTOR_DESPACHO`)
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "motivos": [
    { "codigo": "CLIENTE_AUSENTE", "descripcion": "Cliente no se encuentra en el domicilio" },
    { "codigo": "DIRECCION_NO_UBICADA", "descripcion": "Dirección inubicable o inexistente" },
    { "codigo": "PAQUETE_RECHAZADO", "descripcion": "Receptor rechaza la recepción del paquete" },
    { "codigo": "ZONA_INACCESIBLE", "descripcion": "Cierre de vías, huelga o restricción de acceso" }
  ]
}
```

---

## 5. Endpoints: Seguimiento de Pedidos (Capacidad Transversal)

### 5.1 Consulta Pública de Rastreo
Permite a cualquier cliente consultar el estado, línea de tiempo y ubicación de su paquete.

- **Método:** `GET`
- **Ruta:** `/api/v1/tracking/{codigoRastreo}`
- **Autenticación:** Pública (sin token)
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "codigoRastreo": "TRK-78901",
  "estadoActual": "EN_CAMINO",
  "estadoEtiqueta": "En camino hacia tu domicilio",
  "fechaEstimadaEntrega": "2026-09-11",
  "destinatarioAnonimizado": "C***** M******",
  "direccionAnonimizada": "Av. Javier Prado Este 24**, San Borja",
  "coordenadasZona": {
    "latitud": -12.08945,
    "longitud": -77.00342
  },
  "hitos": [
    {
      "estado": "PENDIENTE_ASIGNACION",
      "titulo": "Pedido recibido en centro logístico",
      "fecha": "2026-09-11T10:00:00Z",
      "completado": true
    },
    {
      "estado": "ASIGNADO",
      "titulo": "Preparado y asignado a repartidor",
      "fecha": "2026-09-11T14:30:00Z",
      "completado": true
    },
    {
      "estado": "EN_CAMINO",
      "titulo": "Repartidor en ruta hacia tu dirección",
      "fecha": "2026-09-11T16:00:00Z",
      "completado": true
    },
    {
      "estado": "ENTREGADO",
      "titulo": "Entregado en domicilio",
      "fecha": null,
      "completado": false
    }
  ]
}
```
- **Respuestas de Error:** `404 Not Found` (código de rastreo no encontrado).

---

## 6. Endpoints: F-04 - Centro de Entregas Fallidas y Reprogramaciones (Gerardo)

### 6.1 Listar Despachos Fallidos
- **Método:** `GET`
- **Ruta:** `/api/v1/despachos/fallidos`
- **Rol requerido:** `GESTOR_DESPACHO`
- **Respuesta Exitosa (`200 OK`):** Retorna la lista de despachos con estado `FALLIDO`, motivo reportado y evidencias asociadas.

### 6.2 Reprogramar Despacho
- **Método:** `POST`
- **Ruta:** `/api/v1/despachos/{idDespacho}/reprogramar`
- **Rol requerido:** `GESTOR_DESPACHO`
- **Cuerpo de la Solicitud:**
```json
{
  "nuevaFechaEntrega": "2026-09-13",
  "motivoReprogramacion": "Coordinación telefónica con cliente"
}
```
- **Respuesta Exitosa (`200 OK`):** Despacho devuelto a la cola con estado `PENDIENTE_ASIGNACION`.
- **Respuestas de Error:** `422 Unprocessable Entity` (se superó el límite de reintentos).

### 6.3 Devolución Definitiva a Almacén
- **Método:** `POST`
- **Ruta:** `/api/v1/despachos/{idDespacho}/devolver-almacen`
- **Rol requerido:** `GESTOR_DESPACHO`
- **Cuerpo de la Solicitud:**
```json
{
  "motivoDevolucion": "Cliente no habido tras reintentos máximos agotados"
}
```
- **Respuesta Exitosa (`200 OK`):** Transiciona a `DEVUELTO_A_ALMACEN` y emite webhook a Devoluciones y Ventas.

---

## 7. Endpoints: F-05 - Panel de Monitoreo de Flota, Operadores y Capacidad Diaria (Rhamses)

### 7.1 Consultar Repartidores Disponibles con Balance de Capacidad
Endpoint fundamental consumido por el Panel de Asignación (F-02) para decidir a qué repartidor programar despachos.

- **Método:** `GET`
- **Ruta:** `/api/v1/repartidores/disponibles`
- **Rol requerido:** `GESTOR_DESPACHO`, `GESTOR_FLOTA`
- **Parámetros de Consulta:**
  - `zona` (opcional, string): Filtrar por zona asignada.
  - `pesoRequeridoKg` (opcional, float): Filtrar operadores con al menos este peso remanente.
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "repartidores": [
    {
      "idRepartidor": "REP-0012",
      "nombre": "Luis Morales",
      "estadoDisponibilidad": "DISPONIBLE",
      "vehiculo": {
        "idVehiculo": "VEH-101",
        "tipo": "MOTO",
        "placa": "MTO-456"
      },
      "capacidadMaximaKg": 50.0,
      "capacidadOcupadaKg": 15.0,
      "capacidadRemanenteKg": 35.0,
      "capacidadMaximaM3": 0.6,
      "capacidadOcupadaM3": 0.2,
      "capacidadRemanenteM3": 0.4,
      "despachosAsignadosCount": 2,
      "porcentajeOcupacion": 30.0
    }
  ]
}
```

### 7.2 Panel Resumen de Ocupación de Flota
- **Método:** `GET`
- **Ruta:** `/api/v1/flota/resumen-capacidad`
- **Rol requerido:** `GESTOR_FLOTA`, `GESTOR_DESPACHO`
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "totalRepartidoresTurno": 10,
  "repartidoresDisponibles": 6,
  "repartidoresEnRuta": 3,
  "repartidoresSaturados": 1,
  "capacidadTotalFlotaKg": 1500.0,
  "capacidadOcupadaFlotaKg": 820.0,
  "porcentajeOcupacionGlobal": 54.67
}
```

### 7.3 CRUD de Repartidores y Vehículos
- `GET /api/v1/repartidores`: Lista de todos los repartidores y sus turnos.
- `POST /api/v1/repartidores`: Alta de nuevo repartidor.
- `PUT /api/v1/repartidores/{idRepartidor}`: Modificación de operador y estado.
- `GET /api/v1/vehiculos`: Catálogo de flota vehicular.
- `POST /api/v1/vehiculos`: Registro de nuevo vehículo con límites de peso/volumen.

### 7.4 Asignación Operativa Diaria (Repartidor – Vehículo)
Vincula a un repartidor con un vehículo para la jornada en curso, activándolo con los límites de carga de esa unidad.

- **Método:** `POST`
- **Ruta:** `/api/v1/repartidores/{idRepartidor}/asignacion-diaria`
- **Rol requerido:** `GESTOR_FLOTA`, `ADMIN_DESPACHO`
- **Cuerpo de la Solicitud (Request Body):**
```json
{
  "idVehiculo": "VEH-101",
  "fechaJornada": "2026-09-15"
}
```
- **Respuesta Exitosa (`201 Created`):**
```json
{
  "idAsignacion": "ASIG-0023",
  "idRepartidor": "REP-0012",
  "nombreRepartidor": "Juan Pérez",
  "idVehiculo": "VEH-101",
  "tipoVehiculo": "FURGONETA",
  "placa": "ABC-123",
  "fechaJornada": "2026-09-15",
  "estadoRepartidor": "DISPONIBLE",
  "capacidadMaximaKg": 500.0,
  "capacidadMaximaM3": 4.0,
  "maximoPaquetesDiarios": 80
}
```
- **Respuestas de Error:**
  - `409 Conflict`: el repartidor ya tiene una asignación activa en la misma jornada.
  - `404 Not Found`: repartidor o vehículo no encontrado.
  - `422 Unprocessable Entity`: repartidor no está en estado `INACTIVO` o vehículo no está `DISPONIBLE`.
