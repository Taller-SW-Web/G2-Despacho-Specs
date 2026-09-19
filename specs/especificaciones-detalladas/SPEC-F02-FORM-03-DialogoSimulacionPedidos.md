# Especificación SPEC-F02-FORM-03: Diálogo de Generación de Pedidos de Prueba (Testing Autónomo)

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-02: Programación y Asignación de Despachos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Gestor de Despacho / Desarrollador  

---

## 1. Contexto

Para permitir que el equipo de desarrollo, QA y los gestores de logística puedan validar el comportamiento del panel de asignación y los flujos posteriores sin depender de la disponibilidad o del ritmo de integración del módulo de Ventas, el sistema cuenta con una capacidad de simulación autónoma de carga de trabajo.

---

## 2. Propósito

Proveer un diálogo de configuración rápida en la interfaz de usuario que permita inyectar pedidos y despachos simulados con datos válidos y consistentes en la base de datos de manera inmediata, quedando listos en la cola `PENDIENTE_ASIGNACION`.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Botón desencadenador en la barra superior del Dashboard: *"Simular Pedido de Prueba"*.
- Diálogo modal con opciones de parametrización básica:
  - Selector de Zona de Cobertura (opcional, lista zonas activas de F-01).
  - Campo numérico de Peso en kg (opcional, entre 0.1 y 50.0 kg).
  - Selector de cantidad de pedidos a generar (opcional: 1, 3 o 5 pedidos por lote).
  - Botón de *"Generación Rápida con 1 Clic"* (omite inputs y autogenera todo con datos realistas).
- Envío de la petición a `POST /api/v1/despachos/solicitudes/simular`.
- Manejo de estados de carga (spinner / disabled) durante la creación.
- Notificación toast informando los códigos generados (`TRK-SIM-XXXXX`).
- Refresco automático de la tabla de pendientes (`SPEC-F02-FORM-01`).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Usuario autenticado con rol `GESTOR_DESPACHO` o `ADMIN`.
- Existencia de al menos una zona activa en la base de datos para referenciar el destino.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `POST /api/v1/despachos/solicitudes/simular` | Endpoint backend que genera los registros simulados (`SPEC-F02-PROC-01`). |
| `GET /api/v1/zonas` | Endpoint de F-01 para poblar el selector de zonas activas. |
| `SPEC-F02-FORM-01` | Vista padre receptora de los nuevos despachos generados. |

### 4.3. Resultados
- Uno o varios despachos con estado `PENDIENTE_ASIGNACION` y códigos `PED-SIM-XXXXX` y `TRK-SIM-XXXXX` se crean en la base de datos.
- La tabla de pendientes muestra inmediatamente las nuevas filas sin necesidad de recargar manualmente el navegador.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Simulación interactiva de órdenes
El diálogo DEBE permitir la creación de órdenes de prueba configuradas o completamente aleatorias.

#### CA-01. Generación rápida con un clic
- **DADO** que el usuario abre el diálogo de simulación.
- **CUANDO** pulsa *"Generación Rápida"*.
- **ENTONCES** el frontend envía `{}` a la API, el backend crea un despacho con dirección ficticia válida en Lima, peso entre 1.0 y 10.0 kg, estado `PENDIENTE_ASIGNACION`, y el frontend muestra el toast *"Pedido de prueba TRK-SIM-XXXXX creado exitosamente"*.

#### CA-02. Generación parametrizada por zona y peso
- **DADO** que el usuario selecciona la zona "Lima Norte" e ingresa un peso de 15.5 kg.
- **CUANDO** confirma la simulación.
- **ENTONCES** el backend crea el despacho con exactamente 15.5 kg y coordenadas geográficas dentro del polígono de Lima Norte.

#### CA-03. Validación de campos numéricos en cliente
- **DADO** que el usuario ingresa un peso de 0 o un número negativo.
- **CUANDO** intenta enviar el formulario.
- **ENTONCES** el campo se resalta en rojo con el mensaje *"El peso debe ser mayor a 0 kg"* y se bloquea la llamada HTTP.

---

## 6. Frontend

### 6.1. Componentes
- **`SimulationDialog`**: Modal compacto con título *"Simulador de Despachos (Testing)"*.
- **`ZoneSelect`**: Dropdown con zonas activas disponibles.
- **`WeightInput`**: Input de tipo número (`step="0.1"`, `min="0.1"`, `max="100"`).
- **`BatchCountRadio`**: Selector de radio buttons para cantidad (1, 3, 5).
- **`DialogButtons`**: Botón secundario *"Generación Rápida (Defaults)"* y botón principal *"Generar [N] Despacho(s)"*.

### 6.2. Comportamiento y UX
- El modal se cierra automáticamente al completar la llamada exitosa.
- Notificación tipo toast verde con icono de check y código de rastreo generado enlazable.

---

## 7. Backend (Contrato consumido)

- **Ruta:** `POST /api/v1/despachos/solicitudes/simular`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Content-Type: application/json`
- **Cuerpo (Opcional):**
```json
{
  "idZona": "ZONA-LIMA-CENTRO",
  "pesoKg": 8.5,
  "cantidad": 1
}
```
- **Respuesta Exitosa (`201 Created`):**
```json
{
  "idDespacho": "DSP-SIM-98214",
  "idPedido": "PED-SIM-45123",
  "codigoRastreo": "TRK-SIM-78192",
  "destinatario": {
    "nombre": "Destinatario Simulado QA",
    "telefono": "+51999888777",
    "email": "qa-test@example.com"
  },
  "direccionEntrega": "Calle Las Begonias 450, San Isidro, Lima",
  "idZona": "ZONA-LIMA-CENTRO",
  "pesoKg": 8.5,
  "volumenM3": 0.04,
  "estado": "PENDIENTE_ASIGNACION",
  "fechaCreacion": "2026-09-19T16:30:00Z"
}
```

---

## 8. Requisitos no funcionales

- **Tiempos de Respuesta:** El proceso de simulación debe completarse y responder en menos de 300 ms en el backend.
- **Ambiente Operativo:** Capacidad disponible en entornos de desarrollo, pruebas y staging; en producción requiere rol estricto `ADMIN`.
- **Aislamiento:** Los datos generados deben llevar prefijos claros (`SIM-`) para facilitar limpiezas de datos de prueba si fuera necesario.

---

## 9. Fuera de alcance

- Simulación de entregas en ruta (la simulación de cambios de estado en calle corresponde a la web de repartidor F-03).
- Simulación de pagos de pasarelas bancarias (corresponde a Ventas).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Component Test | Vitest + RTL | Clic en simulación rápida envía payload vacío y dispara mutación. |
| CA-02 | Functional Test | Cypress | Creación con zona y peso específico visible en la tabla inmediatamente. |
| CA-03 | Client Validation | React Testing Library | Peso negativo muestra mensaje de validación sin emitir fetch. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. El diálogo esté accesible desde el panel principal de programación.
2. Permita tanto la generación rápida como parametrizada.
3. Actualice la cola reactivamente mediante invalidación de caché en React Query.
4. Cumpla las pruebas unitarias y de integración de frontend y backend.
