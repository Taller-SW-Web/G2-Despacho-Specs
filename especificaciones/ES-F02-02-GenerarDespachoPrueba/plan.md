# Plan de ES-F02-02: Generación de despachos de prueba para simulación

**Responsable:** Tarqui.

**Estado:** Backend implementado y verificado localmente; frontend funcional pendiente. La ejecución y las diferencias de nombres técnicos se registran en [evidence.md](./evidence.md).

**UI:** Aplica; botón y modal en cabecera de `/programacion`.

## 1. Entradas y revisiones

| Documento | Referencia y secciones | Revisión utilizada |
|---|---|---|
| Comportamiento | [spec.md](./spec.md), CA-01 a CA-04 | Especificación atómica SDD. |
| UI | [ui.md](./ui.md), UI-01 a UI-03, CUI-01 a CUI-04 | Especificación de interfaz. |
| Funcionalidad padre | [F-02](../../funcionalidades/F-02-ProgramacionAsignacionDespachos.md), RF-09, CA-20 | Especificación funcional vigente. |
| Contrato de API | [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación) | Endpoint `POST /api/v1/despachos/simulaciones`. |
| Componentes React | [componentes-react.md](../../disenio/componentes-react.md), CR-01, CR-09, CR-12, CR-15 | Contratos de Mantine compartidos. |

## 2. Estrategia y responsabilidades

El generador de simulaciones forma parte de `servicio-gestion-despachos`. Se compone de un endpoint REST administrativo, un generador pseudoaleatorio determinista o realista de direcciones y nombres locales, y la invocación al mismo repositorio de persistencia de despachos, garantizando que los despachos generados cumplan con las mismas restricciones del modelo de datos (`peso > 0`, `volumen > 0`, `cantidadPaquetes = 1`, `esSimulacion = true`).

| Capa | Responsabilidad | Elementos previstos |
|---|---|---|
| Frontend | Botón de acción, modal opcional, mutación React Query y feedback toast. | `BotonGenerarPrueba.tsx`, `ModalSimulacion.tsx`, `useGenerarDespachoPrueba`. |
| API / Web | Validación de JWT `GESTOR_DESPACHO` y DTO de entrada. | `SimulacionController`, `SimulacionRequestDTO`, `DespachoResponseDTO`. |
| Aplicación | Orquestación: obtención de zona activa, generación de datos verosímiles y persistencia. | `GenerarDespachoPruebaUseCase`, `SimuladorDatosService`. |
| Dominio | Entidad `Despacho` con flag `esSimulacion = true`, validación de fecha hoy. | `Despacho`, `EstadoDespacho`. |
| Infraestructura | Persistencia en `despachos` y `historial_estados_despacho`. | `DespachoRepository`, `AuditoriaRepository`. |

## 3. Frontend y componentes React

- El componente `BotonGenerarPrueba` se integra en la cabecera `EncabezadoPagina` (CR-05) del panel de programación.
- Usa `useMutation` de `@tanstack/react-query` apuntando a `POST /api/v1/despachos/simulaciones`.
- Al disparar, activa estado de carga (`loading={isPending}`) para evitar duplicados (CCR-01-01).
- En `onSuccess`, invoca `notifications.show()` de Mantine con tipo éxito y revalida la query de la cola de pendientes.
- El tag "Simulado" se renderiza mediante `BadgeEstado` (CR-09) con variante `outline` neutra.

## 4. Backend, persistencia e integraciones

- **Endpoint:** `POST /api/v1/despachos/simulaciones`.
- **Seguridad:** `@PreAuthorize("hasRole('GESTOR_DESPACHO')")`.
- **Generador de datos:**
  - Si no se envía `idZona`: selecciona aleatoriamente una de las zonas con estado `ACTIVO` en base de datos.
  - Genera nombre ficticio (ej. "Juan Pérez - Prueba"), dirección realista dentro del distrito de la zona (ej. "Av. Arequipa 1234"), teléfono simulado "+51999999999".
  - Si no se envía `pesoKg`: valor aleatorio entre 1.5 y 18.0 kg con 2 decimales.
  - Si no se envía `volumenM3`: valor aleatorio entre 0.010 y 0.080 m³ con 3 decimales.
  - Fija `cantidadPaquetes = 1`.
  - Fija `fechaProgramada = LocalDate.now("America/Lima")`.
  - Genera códigos con prefijo `SIM-` mediante secuencia de base de datos y restricciones únicas; no usa un contador de milisegundos que pueda repetirse.
- **Persistencia:** transaccional con `es_simulacion = true`.
- **Auditoría:** registra `CREACION_SIMULACION` en `historial_estados_despacho` con el usuario extraído del JWT.
- **Sin efectos externos:** el dispatcher de eventos hacia Ventas descarta despachos con `esSimulacion == true`.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Generador de datos simulados y caso de uso de backend. | Repositorio JPA de zonas y despachos. | CA-01, CA-02. |
| I-02 | Endpoint REST con seguridad y manejo de errores 400/422/403. | Spring Security JWT. | CA-03, CA-04. |
| I-03 | Componente de botón y modal en React con revalidación de cola. | Endpoint de backend I-02. | CUI-01 a CUI-04. |

## 6. Estrategia de verificación

- Pruebas unitarias de `SimuladorDatosService` validando rangos de peso, volumen y fecha hoy.
- Pruebas de integración con `MockMvc` verificando códigos de respuesta 201, 400 y 403.
- Verificación de que el despacho simulado no inserta registros en la bandeja de salida outbox hacia Ventas.
- Pruebas de frontend con React Testing Library verificando deshabilitación del botón en vuelo y llamada a la mutación.
