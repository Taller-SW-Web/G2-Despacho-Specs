# Especificación SPEC-F02-FORM-02: Modal de Asignación de Repartidor y Validación de Ocupación

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-02: Programación y Asignación de Despachos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho  

---

## 1. Contexto

Una vez que un despacho pendiente es seleccionado en el panel de programación, el Gestor de Despacho debe asignarlo a un repartidor calificado y disponible. Esta decisión involucra evaluar en tiempo real la capacidad de carga del vehículo del repartidor para evitar sobrecargas físicas o infracciones de tránsito, garantizando la seguridad en el reparto y el cumplimiento de los tiempos de entrega.

---

## 2. Propósito

Proveer un diálogo modal interactivo que presente el catálogo de repartidores habilitados para la jornada y zona del despacho, proyecte visualmente el impacto del peso y volumen del paquete en la ocupación vehicular y permita confirmar la asignación o bloquee la acción en caso de sobrecarga.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Apertura del modal contextualizado con el despacho seleccionado (mostrando código de rastreo, peso kg, volumen m³ y zona requerida).
- Consulta y renderizado de la lista de operadores disponibles mediante `GET /api/v1/repartidores/disponibles`.
- Renderizado de tarjetas de repartidor mostrando: nombre, tipo de vehículo, placa, turno y barras de ocupación actuales (peso, volumen, paquetes).
- Simulación visual de ocupación proyectada: cálculo en cliente de `(pesoActual + pesoPaquete)` y `(volumenActual + volumenPaquete)`.
- Bloqueo preventivo en cliente: cambio de color de barras a rojo y deshabilitación del botón "Confirmar Asignación" si el paquete sobrepasa cualquiera de los límites.
- Campo de texto opcional para observaciones o instrucciones especiales de ruta.
- Envío de la asignación a `POST /api/v1/despachos/{idDespacho}/asignar`.
- Manejo de respuestas y cierre: notificación toast de éxito, refresco de la cola de pendientes y gestión de errores de concurrencia (`409 Conflict`) o sobrecarga (`422 Unprocessable Entity`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- El despacho debe existir y estar en estado `PENDIENTE_ASIGNACION`.
- El usuario autenticado debe poseer el rol `GESTOR_DESPACHO`.
- Deben existir repartidores activos con jornada abierta en la fecha actual (F-05).

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/repartidores/disponibles` | Endpoint de F-05 que entrega la disponibilidad y capacidad remanente. |
| `POST /api/v1/despachos/{idDespacho}/asignar` | Endpoint backend de F-02 que ejecuta la asignación transaccional (`SPEC-F02-PROC-02`). |
| `SPEC-F02-FORM-01` | Pantalla padre que invoca el modal y refresca su tabla tras el cierre. |

### 4.3. Resultados
- Si la asignación se aprueba, el modal se cierra, se emite una notificación toast de éxito y el despacho desaparece de la cola de pendientes.
- Si ocurre un conflicto de concurrencia o saturación en el servidor, se notifica claramente al usuario sin perder los datos del formulario.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Despliegue de repartidores y cálculo proyectado
El modal DEBE contrastar las dimensiones del despacho contra la capacidad remanente de los repartidores.

#### CA-01. Apertura con cálculo proyectado dentro del límite
- **DADO** un despacho con 10 kg y 0.05 m³ y un repartidor con remanente de 50 kg y 0.5 m³.
- **CUANDO** el gestor selecciona la tarjeta de dicho repartidor.
- **ENTONCES** la interfaz proyecta la nueva ocupación en barra verde/ámbar, habilita el botón "Confirmar Asignación" y muestra el saldo restante en kg y m³.

#### CA-02. Bloqueo visual por sobrecarga de peso o volumen
- **DADO** un despacho de 25 kg y un repartidor cuya capacidad remanente de peso es de solo 15 kg.
- **CUANDO** el gestor selecciona a dicho operador en el modal.
- **ENTONCES** la barra de peso se colorea en rojo con la leyenda *"Capacidad excedida (+10 kg)"*, se muestra un banner de advertencia y el botón de confirmación queda deshabilitado.

#### CA-03. Sin repartidores disponibles para la zona
- **DADO** que todos los repartidores de la zona están `SATURADO` o `FUERA_DE_TURNO`.
- **CUANDO** se abre el modal.
- **ENTONCES** se muestra un estado vacío con el mensaje *"No hay repartidores disponibles con capacidad para esta zona en la jornada actual"*.

### RF-02. Confirmación y manejo de respuestas
El modal DEBE comunicar la asignación al backend y reaccionar a las respuestas HTTP del servicio transaccional.

#### CA-04. Asignación exitosa
- **DADO** un repartidor seleccionado con capacidad suficiente.
- **CUANDO** el gestor pulsa "Confirmar Asignación".
- **ENTONCES** el frontend envía la petición `POST /api/v1/despachos/{idDespacho}/asignar`, recibe `200 OK`, cierra el modal y muestra el toast *"Despacho asignado correctamente a [Nombre Chofer]"*.

#### CA-05. Conflicto por despacho ya asignado concurrentemente
- **DADO** que otro gestor asignó el mismo despacho hace instantes.
- **CUANDO** se pulsa confirmar.
- **ENTONCES** el backend responde `409 Conflict`, el modal muestra una alerta roja indicando *"Este despacho ya fue asignado o procesado previamente"* y ofrece un botón para cerrar y refrescar la grilla.

---

## 6. Frontend

### 6.1. Componentes del modal
- **`AssignmentModal`**: Contenedor modal con backdrop oscurecido, botón de cierre (`X` o tecla `Esc`).
- **`PackageSummaryHeader`**: Resumen compacto del paquete: `# Código`, Peso: `X kg`, Volumen: `Y m³`, Zona: `[Nombre Zona]`.
- **`DriverSelectionList`**: Lista scrollable de repartidores disponibles con radio buttons o tarjetas clicables con foco accesible.
- **`CapacityProgressBar`**: Componente visual de barra porcentual con transiciones fluidas y cambio de color:
  - Verde: `<= 70%` de ocupación.
  - Ámbar: `71% - 99%` de ocupación.
  - Rojo: `>= 100%` (sobrecarga).
- **`AssignmentNotesInput`**: Textarea con contador de caracteres (máx. 250) para notas de despacho.
- **`ModalActionButtons`**: Botón "Cancelar" y botón principal "Confirmar Asignación" con spinner de carga durante el submit.

### 6.2. Validaciones en cliente
- Selección obligatoria de un repartidor de la lista.
- Deshabilitación reactiva del botón de envío si `pesoProyectado > capacidadMaxPeso` o `volumenProyectado > capacidadMaxVolumen`.

---

## 7. Backend (Contratos consumidos)

### 7.1. Consulta de Operadores Habilitados
- **Ruta:** `GET /api/v1/repartidores/disponibles?zona={idZona}`
- **Respuesta (`200 OK`):**
```json
[
  {
    "idRepartidor": "REP-0012",
    "nombre": "Juan Pérez",
    "tipoVehiculo": "FURGONETA",
    "placaVehiculo": "ABC-123",
    "capacidadMaxKg": 500.0,
    "capacidadRemanenteKg": 180.5,
    "capacidadMaxM3": 4.0,
    "capacidadRemanenteM3": 1.45,
    "maxPaquetesRuta": 80,
    "paquetesActuales": 35,
    "porcentajeOcupacion": 63.9
  }
]
```

### 7.2. Confirmación de Asignación
- **Ruta:** `POST /api/v1/despachos/{idDespacho}/asignar`
- **Cuerpo (Request Body):**
```json
{
  "idRepartidor": "REP-0012",
  "observaciones": "Entrega en primer piso, timbre 102"
}
```
- **Respuestas posibles:**
  - `200 OK`: Asignación completada (`{ "idDespacho": "...", "estado": "ASIGNADO", ... }`).
  - `409 Conflict`: Repartidor fuera de turno, saturado o despacho no disponible.
  - `422 Unprocessable Entity`: Capacidad de peso o volumen excedida en servidor.

---

## 8. Requisitos no funcionales

- **Interactividad y Feedback:** La simulación de barras de carga debe actualizarse de forma instantánea (< 16 ms) al cambiar la selección de operador.
- **Prevención de doble clic:** Deshabilitación inmediata del botón tras el primer clic para impedir envíos dobles en conexiones lentas.
- **Accesibilidad:** Foco atrapado dentro del modal mientras esté abierto (`focus-trap`), salida con tecla `Escape`.

---

## 9. Fuera de alcance

- Creación o edición de repartidores o vehículos desde el modal (responsabilidad de F-05).
- Reasignación de paquetes ya asignados (flujo de reprogramación o modificación avanzada).
- Cálculo o trazado cartográfico de rutas GPS óptimas.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Component Test | RTL / Vitest | Repartidor con capacidad suficiente habilita botón de confirmación. |
| CA-02 | Visual Logic | Jest / RTL | Repartidor con sobrecarga deshabilita botón y muestra barra roja. |
| CA-03 | UI Empty State | Storybook | Renderizado de estado sin choferes disponibles. |
| CA-04 | End-to-End | Cypress | Selección, confirmación, llamada POST y toast visible. |
| CA-05 | Error Handling | MSW (Mock Service Worker) | Simulación de error `409` muestra alerta de conflicto en el modal. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El modal esté integrado visualmente en el panel de despachos.
2. Se validen tanto en cliente como mediante respuestas de servidor los límites de peso y volumen.
3. Se cubran con pruebas automatizadas los escenarios `CA-01` a `CA-05`.
4. El envío persista correctamente las observaciones en la base de datos a través de la API.
