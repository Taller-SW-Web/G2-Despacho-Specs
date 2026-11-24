# Plan de ES-F03-09: Recuperación de contraseña del repartidor

**Responsable:** Max Rojas

**Estado:** Borrador; alineado con el OpenAPI 1.2.0 de G7 y pendiente de revisión técnica.

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas y revisiones

| Documento | Referencia | Revisión o commit utilizado |
|---|---|---|
| Especificación funcional | [spec.md](./spec.md) | Borrador del 24/11/2026 |
| UI | [ui.md](./ui.md) | Borrador del 24/11/2026 |
| Contrato de API | [Contrato externo §8.6 y §8.6.1](../../integraciones/api-contract.md#861-recuperación-de-contraseña-del-repartidor) | Actualización del 24/11/2026 |
| Contrato de Seguridad | [OpenAPI de G7](https://github.com/Taller-SW-Web/Modulo-de-Seguridad/blob/b32b2d08bbc185a8f9ad2ff3fd634b28edb8a323/specs/contrato-api/openapi.yaml#L1433), `/password/recuperar` y `/password/restablecer` | v1.2.0, commit `b32b2d0` del 10/11/2026; revisión local no desplegada |
| Componentes React | `FormularioAcceso` de `@despacho/componentes-compartidos` | Rama `feature/f03correcciones` del frontend |
| Arquitectura y datos | [c4-contenedores.md](../../arquitectura/c4-contenedores.md) y [modelo-datos.md](../../arquitectura/modelo-datos.md): Despacho no administra contraseñas | — |

## 2. Estrategia y responsabilidades

La recuperación es responsabilidad de G7. Despacho ofrece en su app la entrada y la pantalla del correo, publica en el Gateway solo la solicitud del enlace y la simula en `seguridad-local`. El restablecimiento ocurre en la pantalla de G7 a la que lleva el correo. La opción se activa por ambiente con una variable pública.

| Capa o aplicación | Responsabilidad en el incremento | Archivos o componentes |
|---|---|---|
| Frontend compartido | Enlace opcional, deshabilitado o habilitado | `packages/componentes-compartidos/src/formularios/FormularioAcceso.tsx` |
| Cliente de Seguridad | `solicitarRecuperacion(correo)` contra `POST /api/v1/password/recuperar` | `packages/cliente-api/src/sesion.ts` |
| App del repartidor | Configuración, ruta y pantalla | `config.ts`, `Aplicacion.tsx`, `paginas/PaginaAcceso.tsx`, `paginas/PaginaRecuperacion.tsx`, `sesion/SesionProveedor.tsx`, `.env.example` |
| API Gateway | Publicar `POST /api/v1/password/recuperar` sin token; no publicar `restablecer` ni `cambiar` | `RutasAccesoSeguridad.java`, `ConfiguracionSeguridad.java` |
| `seguridad-local` | Simular `recuperar`: `202` neutro, `429` tras tres por correo y hora, `canalOrigen` del enum de G7 | `EmisorSeguridadLocal.java` |
| Servicios de Despacho | No aplica | — |

## 3. Frontend y componentes React

- Componentes compartidos: `FormularioAcceso` recibe `recuperacion?: { habilitada, alAbrir }`. Sin la propiedad no muestra nada, así que la app administrativa no cambia.
- Componentes propios: `PaginaRecuperacion` implementa UI-02 con Mantine, sin componentes nuevos.
- Estado y datos: estado local del formulario; no se persiste el correo ni se registra en consola.
- Cliente de API: `crearAccesoSeguridad().solicitarRecuperacion` envía `POST {origen}/api/v1/password/recuperar` con `{ correo }`, sin `canalOrigen`, sobre el origen de Seguridad configurado (`VITE_SEGURIDAD_URL` o Gateway). Reutiliza el manejo de errores por `code` y `Retry-After`.
- Activación: `VITE_RECUPERACION_CONTRASENA=true`. El código la deja apagada por omisión; `.env.example` la activa en local, donde la simula `seguridad-local`. En un ambiente desplegado se activa cuando G7 publique la operación.
- Demo: en `VITE_MODO_DEMO` la solicitud no sale de la app.

## 4. Backend, persistencia e integraciones

- Entrada, caso de uso, datos y migración: no aplican en los servicios de Despacho.
- Gateway: `recuperar` se reenvía al origen de Seguridad con la misma política CORS que el login. `restablecer` y `cambiar` responden `401` porque no están publicadas.
- Integraciones: G7 ejecuta la operación; el timeout de 15 s y el manejo de errores son los del adaptador de §8.6.
- Seguridad: operación pública; la respuesta neutra la garantiza G7 (RN-02). La app no deduce nada de la respuesta.
- Concurrencia e idempotencia: la pantalla evita envíos simultáneos; G7 limita a tres solicitudes por correo y hora.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Enlace deshabilitado, pantalla y adaptador detrás de la variable, con pruebas simuladas | §8.6.1 | CA-01 a CA-05, CA-07 |
| I-02 | Adaptador con la ruta de G7, ruta en el Gateway y simulación en `seguridad-local` | OpenAPI G7 1.2.0 | CA-01, CA-04 |
| I-03 | Activación en el ambiente desplegado y recorrido real con correo | G7 desplegado; DT-06 | CA-06, CA-08 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | `PaginaRecuperacion.test.tsx`, `gestorSesion.test.ts` y `RutasSesionRenderTests` | JSDOM; Spring Boot | Seguridad simulada |
| CA-02 | `FormularioAcceso.test.tsx` y `PaginaRecuperacion.test.tsx` | JSDOM | No aplica |
| CA-03 | `PaginaRecuperacion.test.tsx` | JSDOM | No aplica |
| CA-04 | `PaginaRecuperacion.test.tsx`, `gestorSesion.test.ts` y `EmisorSeguridadLocalPruebas` | JSDOM; Java | Seguridad simulada |
| CA-05 | `PaginaRecuperacion.test.tsx` | JSDOM | Seguridad simulada |
| CA-06 | Solicitud con correo inexistente | Ambiente con G7 | Real |
| CA-07 | Prueba de redirección con sesión | JSDOM | Sesión simulada |
| CA-08 | Recorrido manual con buzón | Ambiente con G7 | Real |

Comandos: en el frontend, `npm test`, `npm run test -w @despacho/repartidor`, `npm run test:administrativo`, `npm run typecheck` y `npm run build`. En el backend, `./mvnw clean verify` en `api-gateway` y las pruebas de `seguridad-local` del paso de CI.

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Justificación y fuente | Responsable | Bloquea qué incremento |
|---|---|---|---|---|
| DT-01 | Recuperación por enlace a una pantalla de G7, no por código en la app | Decisión del responsable del 23/11/2026; Despacho no maneja contraseñas | Max Rojas | No bloquea |
| DT-02 | La opción es visible y se deshabilita mientras el ambiente no la active | Decisión del responsable del 23/11/2026 | Max Rojas | No bloquea |
| DT-03 | Ruta, payload, códigos, vigencia del enlace, límite y revocación de sesiones | Resuelto el 24/11/2026: definidos en el OpenAPI G7 1.2.0 (SPEC-08) | Seguridad y Usuarios | Resuelto |
| DT-04 | Pantalla de restablecer y enlace del correo | Resuelto: pantalla 5b de G7 con `POST /password/restablecer` | Seguridad y Usuarios | Resuelto |
| DT-05 | Evaluar si el Gestor de Despacho necesita la misma opción | No se solicitó; su acceso usa MFA | Equipo de Despacho | No bloquea |
| DT-06 | `canalOrigen` para la app del repartidor | El enum de G7 solo admite `WEB`, `CHATBOT`, `RETAIL` y `MARKETPLACE`; sin él, el repartidor vuelve al login web de G7 | Seguridad y Usuarios | No bloquea I-02; afecta I-03 |
| DT-07 | Ambiente de G7 con la operación desplegada y envío real de correos | El OpenAPI 1.2.0 es una revisión local no desplegada | Seguridad y Usuarios | I-03 |

## 8. Condiciones para iniciar y cerrar

- [x] Las entradas de I-01 e I-02 están revisadas y el contrato de G7 está identificado.
- [x] Las tareas indican dependencias, criterios cubiertos y verificación.
- [ ] G7 desplegó la operación (DT-07) antes de iniciar I-03.
- [ ] Al cerrar, todos los criterios tienen evidencia, incluida la integración real de CA-06 y CA-08.

## 9. Referencias

1. [Especificación funcional](./spec.md), [UI](./ui.md) y [tareas](./tasks.md).
2. [Contrato externo](../../integraciones/api-contract.md), §8.4, §8.6 y §8.6.1.
3. [OpenAPI de G7](https://github.com/Taller-SW-Web/Modulo-de-Seguridad/blob/b32b2d08bbc185a8f9ad2ff3fd634b28edb8a323/specs/contrato-api/openapi.yaml#L1433) v1.2.0.
4. [Evidencia](./evidence.md).
