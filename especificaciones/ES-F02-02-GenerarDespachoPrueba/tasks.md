# Tareas de ES-F02-02: Generación de despachos de prueba para simulación

**Responsable de coordinación:** Tarqui.

**Estado:** Backend implementado y verificado localmente; frontend funcional pendiente. Ver [evidence.md](./evidence.md).

**Plan de origen:** [plan.md](./plan.md), preparado el 16/10/2026.

## 1. Orden y dependencias

| ID | Resultado | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Contrato de endpoint `POST /api/v1/despachos/simulaciones` documentado y alineado a Gestión §3.2. | Contrato | api-contract-gestion-despachos.md | CA-01 | Completada |
| T-02 | Caso de uso `GenerarDespachoPrueba` con generador coherente de datos dentro de zonas activas. | Backend / Dominio | Catálogo Zonas (F-01) | CA-01, CA-02 | Verificada localmente |
| T-03 | Caso de uso y controlador REST protegidos mediante Spring Security y rol `GESTOR_DESPACHO`. | Backend / API | T-02 | CA-01 a CA-04 | Verificada localmente |
| T-04 | Pruebas de integración de backend con MockMvc y PostgreSQL real. | Calidad / Backend | T-03 | CA-01 a CA-04 | Aprobada con PostgreSQL externo; ver evidencia |
| T-05 | Componente React `BotonGenerarPrueba` con estado loading y feedback toast Mantine. | Frontend / UI | T-01, CR-01, CR-15 | CUI-01, CUI-02 | Pendiente |
| T-06 | Integración reactiva del botón con la tabla de pendientes e indicador "Simulado". | Integración UI | T-03, T-05, ES-F02-03 | CUI-03, CUI-04 | Pendiente |

## 2. Detalle de tareas

### T-01. Validar contrato de API
- Alcance: confirmar payload de entrada `{ idZona?, pesoKg?, volumenM3?, observaciones? }` y respuesta 201 en [api-contract-gestion-despachos.md §3.2](../../integraciones/api-contract-gestion-despachos.md#32-programación-y-asignación).
- Comprobación: esquemas validados.

### T-02. Implementar servicio simulador de datos
- Alcance: selección de zona activa, generación de datos ficticios, pesos, volúmenes, fecha de hoy y códigos con prefijo `SIM-`. No se fabrican coordenadas opcionales sin una fuente geográfica.
- Comprobación: tests unitarios que verifiquen coherencia de datos autogenerados.

### T-03. Controlador y caso de uso
- Alcance: `SimulacionController` y `GenerarDespachoPruebaUseCase`. Inserción en base de datos con `es_simulacion = true` y registro en historial.
- Comprobación: invocación vía curl o MockMvc devuelve 201 con objeto JSON completo.

### T-04. Suite de pruebas de backend
- Alcance: tests con MockMvc cubriendo generación por omisión, personalizada, validación de errores y 403.
- Comprobación: todos los tests en verde.

### T-05. Implementar botón en frontend
- Alcance: botón Mantine tipo outline en el header con icono de probeta/paquete, hook de mutación con TanStack Query y prevención de doble clic.
- Comprobación: prueba con Vitest y React Testing Library verificando estado de carga y llamada a la API.

### T-06. Conexión con tabla y feedback
- Alcance: al recibir 201, invalidar query de la cola y disparar notificación tipo toast. Renderizar badge neutral punteado "Simulado" en la fila.
- Comprobación: verificación manual o E2E en Playwright.
