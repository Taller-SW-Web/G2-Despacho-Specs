# Tareas de ES-F03-09: Recuperación de contraseña del repartidor

**Responsable:** Max Rojas

**Estado:** En curso; I-01 e I-02 implementados localmente, I-03 bloqueado por el despliegue de G7.

**Plan de origen:** [plan.md](./plan.md), borrador del 24/11/2026.

## 1. Orden y dependencias

| ID | Resultado de la tarea | Área | Depende de | Criterios | Estado |
|---|---|---|---|---|---|
| T-01 | Documentar la operación de G7 en el contrato externo (§8.6.1) y registrar los pendientes en §11 | Integración | Ninguna | Todos | Completada |
| T-02 | Enlace opcional «¿Olvidaste tu contraseña?» en `FormularioAcceso` | Frontend | Ninguna | CA-02 | Completada |
| T-03 | Operación `solicitarRecuperacion` en el cliente de Seguridad | Frontend | T-01 | CA-01, CA-04, CA-05 | Completada |
| T-04 | Pantalla, ruta y variable de activación en la app del repartidor | Frontend | T-02, T-03 | CA-01 a CA-05, CA-07 | Completada |
| T-05 | Alinear el adaptador con `POST /api/v1/password/recuperar` de G7 | Frontend | OpenAPI G7 1.2.0 | CA-01, CA-04 | Completada |
| T-06 | Publicar la ruta en el Gateway y simularla en `seguridad-local` | Integración | T-05 | CA-01, CA-04 | Completada |
| T-07 | Activar la opción en el ambiente y ejecutar el recorrido real | Calidad | T-05, T-06, DT-07 | CA-06, CA-08 | Bloqueada |

## 2. Detalle de tareas

### T-01. Contrato

- [x] Implementada y verificada.

- Incremento del plan: I-01 e I-02.
- Objetivo y alcance: describir en §8.6.1 la operación de G7, sus reglas y el uso por Despacho; registrar en §11 el `canalOrigen` y el despliegue pendientes.
- Verificación: enlaces y anclas del contrato revisados.
- Evidencia: [EV-02](./evidence.md#ev-02-alineación-con-el-contrato-de-g7).

### T-02. Enlace en el formulario de acceso

- [x] Implementada y verificada.

- Incremento del plan: I-01.
- Objetivo y alcance: propiedad opcional `recuperacion` en `FormularioAcceso`; deshabilitado con aviso accesible o habilitado.
- Verificación: `npm test` (tres pruebas en `FormularioAcceso.test.tsx`).
- Evidencia: [EV-01](./evidence.md#ev-01-pruebas-de-interfaz-con-seguridad-simulada).

### T-03. Cliente de Seguridad

- [x] Implementada y verificada.

- Incremento del plan: I-01.
- Objetivo y alcance: `solicitarRecuperacion(correo)` en `packages/cliente-api/src/sesion.ts`.
- Verificación: `npm run typecheck`.
- Evidencia: [EV-01](./evidence.md#ev-01-pruebas-de-interfaz-con-seguridad-simulada).

### T-04. Pantalla y activación

- [x] Implementada y verificada.

- Incremento del plan: I-01.
- Objetivo y alcance: `PaginaRecuperacion`, ruta `/repartidor/recuperar-contrasena`, `RECUPERACION_CONTRASENA_HABILITADA` y `VITE_RECUPERACION_CONTRASENA` en `.env.example`.
- Verificación: `npm run test -w @despacho/repartidor` (seis pruebas), `npm run build`.
- Evidencia: [EV-01](./evidence.md#ev-01-pruebas-de-interfaz-con-seguridad-simulada).

### T-05. Adaptador con la ruta de G7

- [x] Implementada y verificada.

- Incremento del plan: I-02.
- Objetivo y alcance: el adaptador llama a `POST {origen}/api/v1/password/recuperar` con `{ correo }` y sin `canalOrigen`; el mensaje de `429` informa el límite de tres por hora.
- Verificación: `npm run test:administrativo` (prueba «ES-F03-09» en `gestorSesion.test.ts`).
- Evidencia: [EV-02](./evidence.md#ev-02-alineación-con-el-contrato-de-g7).

### T-06. Gateway y simulación local

- [x] Implementada y verificada.

- Incremento del plan: I-02.
- Objetivo y alcance: el Gateway publica `POST /api/v1/password/recuperar` sin token y no publica `restablecer` ni `cambiar`; `seguridad-local` responde `202` neutro, `429` con `Retry-After` tras tres por correo y hora, y `400` ante un correo o `canalOrigen` inválidos.
- Verificación: `./mvnw clean verify` en `api-gateway` (`RutasSesionRenderTests`) y pruebas de `seguridad-local`.
- Evidencia: [EV-02](./evidence.md#ev-02-alineación-con-el-contrato-de-g7).

### T-07. Recorrido real

- [ ] Implementada y verificada.

- Incremento del plan: I-03.
- Objetivo y alcance: activar la variable en el ambiente, solicitar el enlace con una cuenta de prueba, restablecer en la pantalla de G7 y volver a ingresar.
- Bloqueo: DT-07 (despliegue de G7); DT-06 afecta el regreso a la app.

## 3. Cobertura de criterios

| Criterio funcional o de UI | Tareas que lo implementan | Tarea o comprobación que lo verifica | Evidencia |
|---|---|---|---|
| CA-01 | T-03, T-04, T-05, T-06 | `PaginaRecuperacion.test.tsx`, `gestorSesion.test.ts`, `RutasSesionRenderTests`; T-07 | EV-01, EV-02 simuladas; real pendiente |
| CA-02 / CUI-01 / CUI-03 | T-02, T-04 | `FormularioAcceso.test.tsx`, `PaginaRecuperacion.test.tsx` | EV-01 |
| CA-03 | T-04 | `PaginaRecuperacion.test.tsx` | EV-01 |
| CA-04 | T-04, T-05, T-06 | `PaginaRecuperacion.test.tsx`, `gestorSesion.test.ts`, `EmisorSeguridadLocalPruebas`; T-07 | EV-01, EV-02 simuladas; real pendiente |
| CA-05 | T-04 | `PaginaRecuperacion.test.tsx` | EV-01 |
| CA-06 | T-06 | `EmisorSeguridadLocalPruebas` (correo inexistente); T-07 | EV-02 simulada; real pendiente |
| CA-07 | T-04 | `PaginaRecuperacion.test.tsx` | EV-01 |
| CA-08 | T-07 | T-07 | Pendiente |
| CUI-02 | T-02, T-04 | `FormularioAcceso.test.tsx` | EV-01 |
| CUI-04 | T-04 | `PaginaRecuperacion.test.tsx` | EV-01 |

## 4. Cierre de la especificación

- [ ] Todas las tareas del alcance están completadas y verificadas.
- [ ] Los criterios tienen evidencia; los fallos y limitaciones están documentados.
- [x] Las simulaciones e integraciones pendientes se identifican expresamente.
- [x] Los documentos y el índice están actualizados cuando corresponde.
- [ ] La revisión del equipo y los commits o PR de implementación están enlazados.

## 5. Referencias

1. [Especificación funcional](./spec.md): criterios de aceptación [cite: 1].
2. [Plan](./plan.md): incrementos y dependencias [cite: 2].
3. [Evidencia](./evidence.md): resultados y artefactos de verificación [cite: 3].
