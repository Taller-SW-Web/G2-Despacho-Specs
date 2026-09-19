# Especificación SPEC-F03-FORM-01: Vista Mobile "Mi Ruta" y Detalle de Despacho

**Tipo:** Formulario / Vista (Mobile-First)  
**Macro-funcionalidad:** F-03: Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Repartidor  

---

## 1. Contexto

El repartidor opera en campo desde su dispositivo móvil inteligente, bajo condiciones de luz solar y desplazamientos constantes. Requiere una interfaz táctil ergonómica, ágil y clara que le presente su hoja de ruta del día en la secuencia asignada por el centro de despacho, con acceso directo a los datos de entrega y al botón de inicio de traslado.

---

## 2. Propósito

Proveer una interfaz web mobile-first optimizada para uso con una sola mano que permita al repartidor autenticado consultar su ruta de entrega diaria ordenada secuencialmente, visualizar los datos de contacto y dirección de cada destinatario, y marcar el inicio de traslado hacia el destino (`ASIGNADO` → `EN_CAMINO`).

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Vista principal *"Mi Ruta"* con cabecera de estado operativo del chofer y barra de progreso de entregas (ej. *"4 de 10 completadas"*).
- Lista de despachos de la jornada actual ordenados por `secuenciaRuta`.
- Tarjeta de despacho con: código de rastreo, nombre de destinatario, dirección formateada, número de intento sobre el máximo, chip de estado (`ASIGNADO`, `EN_CAMINO`, `ENTREGADO`, `FALLIDO`).
- Vista expandida / detalle del despacho:
  - Teléfono del destinatario con enlace directo de llamada (`tel:<numero>`).
  - Referencias de entrega o notas del gestor.
  - Botón de apertura de aplicación de mapas externa (Google Maps / Waze) con las coordenadas de destino.
- Botón de acción principal contextual:
  - En estado `ASIGNADO`: botón *"Iniciar Traslado (En camino)"* que dispara `PATCH /api/v1/despachos/{id}/iniciar-traslado`.
  - En estado `EN_CAMINO`: botones de acceso a *"Confirmar Entrega"* (`SPEC-F03-FORM-02`) y *"Reportar Incidencia"* (`SPEC-F03-FORM-03`).
- Manejo de estados de carga, jornada sin despachos y error por falta de conexión.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Repartidor autenticado con token JWT (rol `REPARTIDOR`).
- Repartidor con jornada activa asignada hoy en F-05 y estado operativo distinto a `FUERA_DE_TURNO`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/repartidor/mi-ruta` | Endpoint que entrega la lista de despachos del repartidor en turno. |
| `PATCH /api/v1/despachos/{id}/iniciar-traslado` | Endpoint que ejecuta la transición a `EN_CAMINO`. |
| `SPEC-F03-FORM-02` | Formulario de entrega exitosa. |
| `SPEC-F03-FORM-03` | Formulario de reporte de fallo. |

### 4.3. Resultados
- El estado del despacho pasa a `EN_CAMINO` con marca temporal del servidor y sin recarga completa de página.
- El repartidor ve reflejado el progreso de su jornada de forma fluida.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Carga de la ruta asignada
La vista DEBE consultar únicamente los paquetes asignados al repartidor autenticado.

#### CA-01. Despliegue de ruta ordenada por secuencia
- **DADO** un repartidor con 5 despachos asignados para hoy.
- **CUANDO** abre "Mi Ruta".
- **ENTONCES** se listan los 5 despachos estrictamente en el orden 1 al 5, mostrando código de rastreo, dirección y botón de acción correspondiente.

#### CA-02. Jornada sin entregas asignadas
- **DADO** que el repartidor no tiene despachos asignados para la fecha.
- **CUANDO** accede a la aplicación.
- **ENTONCES** se muestra el mensaje *"No tienes despachos programados para hoy"* con un icono representativo y botón para refrescar.

#### CA-03. Bloqueo por turno inactivo
- **DADO** un repartidor cuyo estado en F-05 es `FUERA_DE_TURNO`.
- **CUANDO** intenta operar en la vista.
- **ENTONCES** la aplicación muestra un aviso banner *"Tu turno no se encuentra activo. Solicita apertura de jornada al Gestor de Flota"* y deshabilita los botones de acción de traslado.

### RF-02. Transición a "En Camino"
El repartidor DEBE poder declarar el inicio del traslado de forma táctil.

#### CA-04. Inicio de traslado exitoso
- **DADO** un despacho en estado `ASIGNADO`.
- **CUANDO** el repartidor pulsa *"Iniciar Traslado"*.
- **ENTONCES** el botón muestra spinner, envía `PATCH`, recibe `200 OK`, el chip de estado cambia a `EN_CAMINO` en color azul y se habilitan los botones de "Entregar" y "Fallar".

---

## 6. Frontend

### 6.1. Componentes Mobile-First
- **`DriverRoutePage`**: Contenedor con ancho máximo móvil (`max-w-md mx-auto`), header con avatar, nombre de chofer y progreso del día.
- **`RouteTimelineList`**: Lista vertical de tarjetas de despacho con indicadores visuales de secuencia (1, 2, 3...).
- **`DispatchCard`**: Tarjeta táctil con padding amplio (mínimo 48px de área táctil según estándares WCAG).
- **`CallClientButton`**: Botón con icono de teléfono y acción nativa `tel:`.
- **`StartTransitButton`**: Botón de ancho completo en color primario con feedback táctil y prevención de doble clic.

### 6.2. Usabilidad en campo
- Contraste alto certificado para legibilidad en exteriores bajo luz solar.
- Prevención de acciones accidentales mediante micro-animaciones de confirmación.

---

## 7. Backend (Contratos consumidos)

### 7.1. Obtener Mi Ruta
- **Ruta:** `GET /api/v1/repartidor/mi-ruta`
- **Cabeceras:** `Authorization: Bearer <JWT>`
- **Respuesta (`200 OK`):**
```json
{
  "idRepartidor": "REP-0012",
  "fecha": "2026-09-19",
  "totalDespachos": 6,
  "despachosCompletados": 2,
  "despachos": [
    {
      "idDespacho": "DSP-100234",
      "secuenciaRuta": 1,
      "codigoRastreo": "TRK-78901",
      "destinatario": "Carlos Mendoza",
      "telefono": "+51987654321",
      "direccion": "Av. Javier Prado Este 2465, San Borja",
      "referencia": "Casa blanca frente al parque",
      "coordenadas": { "latitud": -12.0894, "longitud": -77.0034 },
      "estado": "ASIGNADO",
      "numeroIntento": 1,
      "maximoIntentos": 2
    }
  ]
}
```

### 7.2. Iniciar Traslado
- **Ruta:** `PATCH /api/v1/despachos/{idDespacho}/iniciar-traslado`
- **Respuesta:** `200 OK` con `{ "idDespacho": "...", "estado": "EN_CAMINO", "fechaInicioTraslado": "..." }`

---

## 8. Requisitos no funcionales

- **Rendimiento Móvil:** Bundle liviano (< 150 KB de JS inicial) y tiempos de interacción rápidos (< 100 ms).
- **Protección de Datos:** El teléfono del cliente solo se muestra mientras el despacho no esté cerrado (`ASIGNADO` o `EN_CAMINO`).
- **Seguridad:** El backend infiere el `idRepartidor` exclusivamente del token JWT decodificado, nunca de parámetros en la URL.

---

## 9. Fuera de alcance

- Navegación GPS integrada por voz (se delega a aplicaciones nativas mediante intent `geo:` o enlace universal a Google Maps).
- Reordenamiento de la secuencia por parte del chofer (la secuencia es fijada por el centro de despacho).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Mobile View Test | Cypress (Viewport iPhone 14) | Lista de 5 tarjetas en orden secuencial 1..5. |
| CA-02 | Empty State Test | Vitest / RTL | Mensaje amigable cuando la lista de ruta viene vacía. |
| CA-03 | Security Guard | RTL | Aviso de turno inactivo bloquea botones de cambio de estado. |
| CA-04 | Transit Action | Vitest | Clic en "Iniciar Traslado" emite PATCH y actualiza badge a `EN_CAMINO`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. La vista mobile responsive se adapte ergonómicamente a smartphones.
2. Permita consultar la ruta, llamar al cliente e iniciar el traslado a `EN_CAMINO`.
3. Supere las pruebas automatizadas de interfaz y contratos de red.
