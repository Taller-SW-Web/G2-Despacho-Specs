# Especificación SPEC-F01-FORM-01: Panel y Delimitación Geoespacial de Zonas de Cobertura

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-01: Gestión de Zonas Geográficas y Cotizador de Envíos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Administrador / Gestor de Despacho  

---

## 1. Contexto

Para que el centro de despacho pueda operar, es indispensable delimitar con precisión qué distritos, códigos postales o áreas poligonales tienen cobertura de entrega a domicilio. Esta vista permite a los administradores y gestores configurar y mantener el catálogo maestro de zonas geográficas, visualizarlas en un mapa interactivo y activar o desactivar su operatividad.

---

## 2. Propósito

Proveer una interfaz gráfica web responsive con mapa interactivo (Leaflet / OpenStreetMap) para listar, crear, editar, delimitar polígonos o distritos de cobertura y alternar el estado operativo (`ACTIVO` / `INACTIVO`) de las zonas geográficas del sistema.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Panel administrativo con la lista paginada de zonas configuradas y buscador por nombre o distrito.
- Modal o formulario de alta y edición de zona con campos: nombre descriptivo, distritos comprendidos, códigos postales y delimitación geográfica.
- Componente de mapa interactivo para dibujo y ajuste de polígonos de cobertura (soporte GeoJSON).
- Validación visual preventiva para evitar solapamiento entre polígonos de zonas activas.
- Acción de activación/desactivación con diálogo de advertencia informando que una zona desactivada no aceptará nuevas cotizaciones pero conservará sus despachos históricos.
- Envío a los endpoints de CRUD de zonas (`GET /api/v1/zonas`, `POST /api/v1/zonas`, `PUT /api/v1/zonas/{id}`, `PATCH /api/v1/zonas/{id}/estado`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- El usuario debe estar autenticado con rol `ADMIN` o `GESTOR_DESPACHO`.
- Servicio de cartografía Leaflet / tiles de OpenStreetMap accesible.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/zonas` | Listar zonas existentes y sus geometrías. |
| `POST /api/v1/zonas` | Crear una nueva zona de cobertura validada. |
| `PATCH /api/v1/zonas/{id}/estado` | Cambiar estado `ACTIVO` / `INACTIVO`. |
| Leaflet / React-Leaflet | Renderizado interactivo y herramientas de dibujo de polígonos. |

### 4.3. Resultados
- Zona persistida con geometría PostGIS en base de datos.
- Actualización inmediata del catálogo visual y mapa sin recargas completas.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Listado y búsqueda de zonas
El sistema DEBE mostrar las zonas configuradas con sus indicadores de cobertura.

#### CA-01. Listado con zonas activas e inactivas
- **DADO** que existen zonas registradas en el sistema.
- **CUANDO** el administrador ingresa a `/zonas`.
- **ENTONCES** se despliega la tabla con: Nombre de Zona, Distritos cubiertos, Estado (`ACTIVO` / `INACTIVO`), Fecha de Creación y Acciones (Editar, Tarifas, Desactivar).

### RF-02. Creación y delimitación en mapa
El usuario DEBE poder definir el perímetro geográfico mediante herramientas de dibujo.

#### CA-02. Registro exitoso de nueva zona
- **DADO** que el usuario ingresa el nombre "Lima Moderna", selecciona los distritos Miraflores, San Isidro y dibuja el polígono correspondiente.
- **CUANDO** pulsa "Guardar Zona".
- **ENTONCES** el frontend valida que no existan polígonos solapados en cliente, envía la petición `POST /api/v1/zonas`, recibe `201 Created` y muestra notificación de éxito.

#### CA-03. Rechazo de solapamiento de perímetro
- **DADO** un polígono trazado que interseca significativamente con otra zona en estado `ACTIVO`.
- **CUANDO** se intenta guardar.
- **ENTONCES** el sistema resalta el área de conflicto en color rojo, muestra el mensaje *"El perímetro se solapa con la zona activa [Nombre Zona]"* y bloquea la confirmación.

### RF-03. Desactivación controlada
El sistema DEBE advertir el impacto antes de desactivar una zona operativa.

#### CA-04. Advertencia y confirmación de desactivación
- **DADO** una zona activa con despachos en curso.
- **CUANDO** el gestor pulsa "Desactivar".
- **ENTONCES** un modal modal alerta *"La zona dejará de aceptar nuevas cotizaciones y solicitudes. Los despachos existentes completarán su entrega normalmente"*. Al confirmar, el estado cambia a `INACTIVO` con código `200 OK`.

---

## 6. Frontend

### 6.1. Componentes visuales
- **`ZonesManagementPage`**: Layout general con cabecera, botón "Nueva Zona" y tabla paginada.
- **`ZoneFormModal`**: Diálogo modal con tabs o sección dividida: datos alfanuméricos a la izquierda y mapa interactivo a la derecha.
- **`CoverageMapPicker`**: Componente React con Leaflet y Leaflet Draw para creación de polígonos, edición de vértices y cálculo de área estimada.
- **`DeactivateZoneDialog`**: Diálogo de confirmación con advertencia de impacto operativo.

### 6.2. Validaciones en cliente
- Nombre de zona obligatorio (3 a 50 caracteres).
- Al menos un distrito seleccionado o un polígono con mínimo 3 coordenadas válidas.

---

## 7. Backend (Contratos consumidos)

- **Ruta creación:** `POST /api/v1/zonas`
- **Cuerpo (Request Body):**
```json
{
  "nombre": "Lima Moderna",
  "distritos": ["Miraflores", "San Isidro", "San Borja"],
  "codigosPostales": ["15074", "15036", "15037"],
  "geometria": {
    "type": "Polygon",
    "coordinates": [
      [
        [-77.035, -12.122],
        [-77.020, -12.095],
        [-77.001, -12.105],
        [-77.035, -12.122]
      ]
    ]
  }
}
```
- **Ruta cambio estado:** `PATCH /api/v1/zonas/{idZona}/estado` (`{ "estado": "INACTIVO" }`)

---

## 8. Requisitos no funcionales

- **Rendimiento:** Renderizado del mapa y capas GeoJSON en cliente en menos de 500 ms.
- **Seguridad:** Rutas protegidas por JWT con roles `ADMIN` o `GESTOR_DESPACHO`.
- **Accesibilidad:** Tabla navegable mediante teclado y botones con etiquetas `aria-label`.

---

## 9. Fuera de alcance

- Configuración de tarifas (se especifica en `SPEC-F01-FORM-02`).
- Asignación de vehículos a zonas (se gestiona en `SPEC-F05-FORM-03`).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Component Test | RTL / Vitest | Renderizado de tabla con botones de acción según rol. |
| CA-02 | Integration UI | Cypress | Trazado de polígono en canvas y submit exitoso. |
| CA-03 | Visual Validation | Vitest | Detección de intersección entre GeoJSONs bloquea submit. |
| CA-04 | Modal Confirmation | RTL | Modal de confirmación ejecuta PATCH y actualiza badge de estado. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El panel de gestión y el mapa Leaflet permitan el dibujo y edición de polígonos GeoJSON.
2. Se prevengan solapamientos de zonas activas tanto en cliente como en backend.
3. Se cumplan las pruebas automatizadas de los criterios `CA-01` a `CA-04`.
