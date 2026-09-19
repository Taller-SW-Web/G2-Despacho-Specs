# Especificación SPEC-F01-FORM-02: Parametrización de Matriz Tarifaria y Reglas de Cobro

**Tipo:** Formulario / Vista  
**Macro-funcionalidad:** F-01: Gestión de Zonas Geográficas y Cotizador de Envíos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Administrador / Gestor de Despacho  

---

## 1. Contexto

Cada zona de cobertura requiere un esquema de costos y plazos de entrega que equilibre la rentabilidad del transporte con las expectativas comerciales del cliente. Esta interfaz permite definir de forma dinámica las reglas de tarificación por zona, aplicando costos base, recargos por peso excedente y penalidades volumétricas.

---

## 2. Propósito

Proveer una interfaz de usuario web responsive para consultar, configurar y actualizar la matriz de tarifas asociada a cada zona geográfica activa, incluyendo tarifa base, peso base incluido, recargo por kilogramo adicional, factor volumétrico y plazo estimado de entrega.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Vista o modal de configuración de tarifas accesible desde el listado de zonas (`SPEC-F01-FORM-01`).
- Formulario de parametrización con los campos:
  - Moneda (por defecto `PEN - Soles`).
  - Tarifa base (monto fijo mínimo de envío).
  - Peso base incluido en la tarifa (en kg).
  - Recargo por kilogramo adicional (monto por cada kg excedente).
  - Factor volumétrico de conversión (m³ a kg volumétrico equivalente).
  - Plazo estimado de entrega en días hábiles (rango mínimo y máximo, ej. 1 a 2 días).
- Simulador en tiempo real incorporado en el formulario: permite ingresar un peso y volumen de prueba para ver cómo calcularía el costo final antes de guardar.
- Guardado y validación de reglas mediante `PUT /api/v1/zonas/{idZona}/tarifas`.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- La zona geográfica debe existir previamente en estado `ACTIVO`.
- Usuario autenticado con rol `ADMIN` o `GESTOR_DESPACHO`.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| `GET /api/v1/zonas/{idZona}/tarifas` | Obtener la configuración tarifaria vigente de la zona. |
| `PUT /api/v1/zonas/{idZona}/tarifas` | Persistir las nuevas reglas tarifarias en base de datos. |
| `SPEC-F01-PROC-01` | Motor de cotización que consumirá estas reglas inmediatamente. |

### 4.3. Resultados
- Regla tarifaria actualizada y vigente para futuras cotizaciones.
- Registro de auditoría con usuario, fecha y valores anteriores/nuevos.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Parametrización y validación de tarifas
El formulario DEBE validar la coherencia numérica de los valores ingresados.

#### CA-01. Configuración válida de tarifa mixta
- **DADO** la zona "Lima Norte", tarifa base de 10.00 PEN hasta 3.0 kg, recargo de 2.50 PEN/kg adicional, factor volumétrico de 200 y plazo de 1 a 2 días.
- **CUANDO** el usuario confirma el guardado.
- **ENTONCES** el frontend valida que todos los valores sean positivos, envía `PUT /api/v1/zonas/{idZona}/tarifas` y recibe respuesta `200 OK` con notificación de éxito.

#### CA-02. Rechazo por valores negativos o inconsistentes
- **DADO** un intento de guardar con tarifa base negativa (-5.00 PEN) o plazo máximo menor al plazo mínimo.
- **CUANDO** se intenta confirmar.
- **ENTONCES** el formulario bloquea el envío, resalta los campos con error y muestra el mensaje *"Los montos deben ser mayores o iguales a cero"*.

### RF-02. Simulación interactiva de cálculo
El formulario DEBE calcular en cliente el costo proyectado mientras se editan los valores.

#### CA-03. Simulación reactiva en tiempo real
- **DADO** una tarifa base de 12.00 PEN (hasta 5 kg) y recargo de 3.00 PEN/kg.
- **CUANDO** el usuario ingresa en la caja de prueba un paquete de 7 kg.
- **ENTONCES** el widget de simulación muestra instantáneamente: *"Costo estimado: 18.00 PEN (12.00 base + 6.00 por 2 kg adicionales)"*.

---

## 6. Frontend

### 6.1. Componentes
- **`TariffFormModal`**: Contenedor modal con formulario reactivo (`react-hook-form`).
- **`TariffInputsSection`**: Inputs numéricos con formato de moneda (`PEN`) y validaciones de rango.
- **`DeliveryTimeframeInput`**: Selectores de plazo mínimo y máximo en días hábiles.
- **`TariffLivePreviewCard`**: Tarjeta lateral interactiva con inputs de prueba (`pesoKg`, `volumenM3`) y display del costo resultante.

---

## 7. Backend (Contratos consumidos)

- **Ruta:** `PUT /api/v1/zonas/{idZona}/tarifas`
- **Cabeceras:** `Authorization: Bearer <JWT>`, `Content-Type: application/json`
- **Cuerpo:**
```json
{
  "moneda": "PEN",
  "tarifaBase": 10.00,
  "pesoBaseKg": 3.0,
  "recargoPorKgAdicional": 2.50,
  "factorVolumetrico": 200.0,
  "plazoMinimoDias": 1,
  "plazoMaximoDias": 2
}
```
- **Respuesta Exitosa (`200 OK`):** Retorna el objeto tarifario actualizado y la marca temporal de vigencia.

---

## 8. Requisitos no funcionales

- **Precisión Aritmética:** Cálculos de simulación y almacenamiento manejados con 2 decimales para moneda (`BigDecimal` en backend).
- **Rendimiento:** Actualización de simulación visual inmediata (< 10 ms).
- **Auditoría:** Todo cambio de tarifas persiste usuario y timestamp UTC.

---

## 9. Fuera de alcance

- Promociones comerciales, cupones de descuento o subsidios de envío (corresponden a Ventas y Checkout).
- Cobro en pasarelas bancarias.

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Component Test | RTL / Vitest | Formulario válido envía payload estructurado y recibe `200`. |
| CA-02 | Validation Test | Vitest | Tarifas negativas muestran mensajes de validación y bloquean submit. |
| CA-03 | Interactive Test | Jest / RTL | Modificar input de prueba actualiza el cálculo del preview card. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Las tarifas por zona puedan parametrizarse y persistirse consistentemente.
2. La calculadora de prueba visual refleje la fórmula matemática exacta del motor de cotización (`SPEC-F01-PROC-01`).
3. Se superen las pruebas automatizadas de validación y componentes.
