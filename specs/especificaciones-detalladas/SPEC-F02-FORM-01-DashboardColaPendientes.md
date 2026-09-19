# Especificación SPEC-F02-FORM-01: Dashboard de Cola de Despachos Pendientes

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-02: Programación y Asignación de Despachos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho  

---

## 1. Contexto

En el flujo operativo del centro de despacho, el Gestor de Despacho necesita una vista unificada en tiempo real para supervisar todos los paquetes que han sido recibidos de canales comerciales o de pedidos simulados y que se encuentran a la espera de ser asignados a un operador de transporte. Esta pantalla es el punto de entrada administrativo para la toma de decisiones diarias de distribución.

---

## 2. Propósito

Proveer una interfaz de usuario web responsive que permita visualizar, filtrar, paginar y ordenar los despachos en estado `PENDIENTE_ASIGNACION`, presentando indicadores claros de tiempo en espera y alertas de fechas límite, facilitando el inicio del flujo de asignación o la generación de órdenes de prueba.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Renderizado de la tabla paginada de despachos en cola (`PENDIENTE_ASIGNACION`).
- Barra de filtrado por zona de cobertura y fecha programada.
- Selector de ordenamiento (por fecha límite, fecha de creación o peso).
- Controles de paginación (selector de tamaño de página: 10, 25, 50 y navegación).
- Indicadores visuales de estado: chips de tiempo transcurrido en espera, advertencia visual para despachos próximos a vencer (< 24h).
- Manejo de estados de interfaz: carga (skeleton loaders), lista vacía amigable y error de conexión con reintento.
- Botones de acción en cada fila: botón "Asignar" (abre el modal `SPEC-F02-FORM-02`) y botón "Ver Detalle".
- Botón de cabecera "Generar Pedido de Prueba" (abre el diálogo `SPEC-F02-FORM-03`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- El usuario debe contar con una sesión activa y token JWT con rol `GESTOR_DESPACHO` o `ADMIN`.
- El servicio backend de consulta de cola debe estar disponible.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/despachos/pendientes` | Endpoint backend que suministra los datos paginados y filtrados. |
| `SPEC-F02-FORM-02` | Modal de asignación invocado al presionar el botón "Asignar" en una fila. |
| `SPEC-F02-FORM-03` | Diálogo de simulación invocado desde el botón de cabecera. |

### 4.3. Resultados
- El gestor obtiene una visión clara del volumen de carga pendiente sin retardos perceptibles.
- Los filtros y la paginación sincronizan el estado en los parámetros de la URL para permitir navegación directa o recargas.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Carga y despliegue de la cola de despachos
El frontend DEBE solicitar los despachos en estado `PENDIENTE_ASIGNACION` y renderizarlos en una tabla accesible y responsive.

#### CA-01. Despliegue con datos existentes
- **DADO** que existen despachos registrados con estado `PENDIENTE_ASIGNACION`.
- **CUANDO** el usuario accede a la ruta `/despachos/pendientes`.
- **ENTONCES** se muestra la tabla con las columnas: Código de Rastreo, ID Pedido, Destino/Zona, Peso (kg), Volumen (m³), Fecha Límite, Tiempo en Espera y Acciones, con código `200 OK`.

#### CA-02. Despliegue de estado vacío
- **DADO** que no existen pedidos pendientes para los filtros aplicados.
- **CUANDO** se completa la consulta al backend.
- **ENTONCES** la tabla se sustituye por una ilustración amigable con el mensaje *"No hay despachos pendientes de asignación"* y un botón para restablecer filtros.

#### CA-03. Bloqueo de acceso por rol insuficiente
- **DADO** un usuario con rol distinto a `GESTOR_DESPACHO` (ej. `REPARTIDOR`).
- **CUANDO** intenta acceder a la vista.
- **ENTONCES** la aplicación intercepta la ruta, muestra una pantalla de acceso denegado (`403 Forbidden`) y no efectúa peticiones de datos operativos.

### RF-02. Filtrado y ordenamiento interactivo
El usuario DEBE poder filtrar por zona y ordenar la cola según la urgencia de entrega.

#### CA-04. Filtrado por zona de cobertura
- **DADO** que el gestor selecciona la zona "Lima Norte" en el desplegable.
- **CUANDO** se confirma la selección.
- **ENTONCES** la tabla se actualiza mostrando únicamente pedidos con dicha zona asociada y reinicia el paginador a la página 1.

#### CA-05. Ordenamiento por urgencia (Fecha Límite)
- **DADO** que el gestor selecciona el ordenamiento *"Fecha Límite (Más urgente primero)"*.
- **CUANDO** se actualiza la grilla.
- **ENTONCES** los registros con menor tiempo remanente antes del vencimiento encabezan la tabla.

---

## 6. Frontend

### 6.1. Componentes visuales y jerarquía
- **`PendingDispatchesPage`**: Contenedor principal con header, métricas rápidas (total pendientes, volumen acumulado) y layout responsive.
- **`DispatchFiltersBar`**: Input de búsqueda por código de rastreo/pedido, select de zona, datepicker de rango de fechas y select de ordenamiento.
- **`DispatchesTable`**: Tabla con soporte de sort en cabeceras de columnas, skeleton loaders de 5 filas durante estado `isLoading`.
- **`DispatchesPagination`**: Controles previo/siguiente, botones numéricos de página y selector de items por página.

### 6.2. Validaciones en cliente
- El campo de búsqueda filtra localmente o debounce de 300 ms hacia la API.
- Fechas de filtro no pueden tener fecha inicial posterior a la final.

### 6.3. Manejo de errores
- En caso de fallo de red (`HTTP 500` o timeout), se muestra una alerta tipo banner con botón *"Reintentar conexión"*.

---

## 7. Backend (Contrato consumido)

- **Endpoint:** `GET /api/v1/despachos/pendientes`
- **Query Params:**
  - `pagina` (int, default: 1)
  - `limite` (int, default: 10, max: 100)
  - `zona` (string, opcional)
  - `ordenarPor` (`FECHA_LIMITE_ASC`, `FECHA_LIMITE_DESC`, `FECHA_CREACION_DESC`, `PESO_DESC`)
- **Cabeceras:** `Authorization: Bearer <JWT>`
- **Respuesta Exitosa (`200 OK`):**
```json
{
  "paginaActual": 1,
  "totalPaginas": 5,
  "totalElementos": 48,
  "elementosPorPagina": 10,
  "despachos": [
    {
      "idDespacho": "DSP-100234",
      "idPedido": "PED-2026-00891",
      "codigoRastreo": "TRK-78901",
      "destinatario": {
        "nombre": "Carlos Mendoza",
        "telefono": "+51987654321"
      },
      "direccionEntrega": "Av. Javier Prado Este 2465, San Borja",
      "idZona": "ZONA-LIMA-CENTRO",
      "nombreZona": "Lima Moderna / Centro",
      "pesoKg": 12.5,
      "volumenM3": 0.08,
      "fechaEstimadaEntrega": "2026-09-20",
      "tiempoEsperaHoras": 3.5,
      "estado": "PENDIENTE_ASIGNACION"
    }
  ]
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento:** Carga inicial y cambio de página renderizados en cliente en menos de 200 ms tras recibir la respuesta HTTP.
- **Accesibilidad:** Uso de elementos semánticos HTML5 (`table`, `thead`, `tbody`, `th scope="col"`), soporte para navegación completa con teclado (`Tab`, `Enter`, `Escape`).
- **Diseño Responsive:** Adaptable a pantallas de escritorio (>= 1280px) y tablets operativas (>= 768px con scroll horizontal suave).
- **Seguridad:** Sanitización estricta de cadenas de texto renderizadas para prevención de XSS.

---

## 9. Fuera de alcance

- Asignación directa sin modal (la selección y validación de chofer se delega a `SPEC-F02-FORM-02`).
- Modificación directa de datos del destinatario desde la grilla.
- Reordenamiento visual tipo drag-and-drop de despachos.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Component / Integration | React Testing Library | Tabla renderiza 10 filas y paginador muestra total correcto. |
| CA-02 | UI State | Storybook / Jest | Visualización de ilustración y mensaje de lista vacía. |
| CA-03 | Security / Route Guard | Vitest + React Router | Redirección a `/403` al montar componente sin rol requerido. |
| CA-04 | Functional Filter | Cypress / Playwright | Cambio en select de zona dispara petición con query param `zona`. |
| CA-05 | Sorting | Vitest | Parámetro `ordenarPor=FECHA_LIMITE_ASC` enviado al hacer clic en cabecera. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El componente esté implementado en React + Tailwind cumpliendo el diseño acordado.
2. Todos los escenarios `CA-01` a `CA-05` pasen sus pruebas automatizadas en verde.
3. Se garantice la integración con el contrato REST `GET /api/v1/despachos/pendientes`.
4. El enlace al modal de asignación (`SPEC-F02-FORM-02`) transmita el identificador del despacho seleccionado.
