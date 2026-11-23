# Plan de ES-F03-09: Recuperación de contraseña del repartidor

**Responsable:** Max Rojas

**Estado:** Borrador; pendiente de revisión técnica y de la confirmación de Seguridad.

**UI:** Aplica; ver [ui.md](./ui.md).

## 1. Entradas y revisiones

| Documento | Referencia | Revisión o commit utilizado |
|---|---|---|
| Especificación funcional | [spec.md](./spec.md) | Borrador del 23/11/2026 |
| UI | [ui.md](./ui.md) | Borrador del 23/11/2026 |
| Contrato de API | [Contrato externo §8.6 y §8.6.1](../../integraciones/api-contract.md#861-recuperación-de-contraseña-del-repartidor-propuesta-pendiente-de-seguridad) | Propuesta del 23/11/2026, sin confirmar por G7 |
| Componentes React | `FormularioAcceso` de `@despacho/componentes-compartidos` | Rama `feature/f03-recuperar-contrasena` del frontend |
| Arquitectura y datos | [c4-contenedores.md](../../arquitectura/c4-contenedores.md) y [modelo-datos.md](../../arquitectura/modelo-datos.md): Despacho no administra contraseñas | — |

## 2. Estrategia y responsabilidades

La recuperación es responsabilidad de Seguridad. Despacho prepara en su app la entrada y la pantalla, y las deja apagadas detrás de una variable pública hasta que Seguridad confirme la operación. Al confirmarse, se ajusta el adaptador si cambia la ruta o el payload, se publica la ruta en el Gateway y se activa la variable.

| Capa o aplicación | Responsabilidad en el incremento | Archivos o componentes previstos |
|---|---|---|
| Frontend compartido | Enlace opcional, deshabilitado o habilitado | `packages/componentes-compartidos/src/formularios/FormularioAcceso.tsx` |
| Cliente de Seguridad | Operación `solicitarRecuperacion(correo)` | `packages/cliente-api/src/sesion.ts` |
| App del repartidor | Configuración, ruta y pantalla | `config.ts`, `Aplicacion.tsx`, `paginas/PaginaAcceso.tsx`, `paginas/PaginaRecuperacion.tsx`, `sesion/SesionProveedor.tsx`, `.env.example` |
| API Gateway | Publicar `/api/v1/auth/recuperacion-contrasena` si se mantiene el proxy | Configuración de rutas humanas de Seguridad; pendiente hasta la confirmación |
| `seguridad-local` | Simular la operación para Compose | Pendiente hasta la confirmación |
| Servicios de Despacho | No aplica | — |

## 3. Frontend y componentes React

- Componentes compartidos: `FormularioAcceso` recibe `recuperacion?: { habilitada, alAbrir }`. Sin la propiedad no muestra nada, así que la app administrativa no cambia.
- Componentes propios: `PaginaRecuperacion` implementa UI-02 con Mantine, sin componentes nuevos.
- Estado y datos: estado local del formulario; no se persiste el correo ni se registra en consola.
- Cliente de API: `crearAccesoSeguridad().solicitarRecuperacion` envía `POST /recuperacion-contrasena` con `{ correo }` sobre el origen de Seguridad configurado (`VITE_SEGURIDAD_URL` o Gateway). Reutiliza el manejo de errores por `code` y `Retry-After`.
- Activación: `VITE_RECUPERACION_CONTRASENA=true`. Por omisión es `false`: el enlace se muestra deshabilitado y la ruta vuelve al acceso.
- Demo: en `VITE_MODO_DEMO` la solicitud no sale de la app.

## 4. Backend, persistencia e integraciones

- Entrada, caso de uso, datos y migración: no aplican en Despacho.
- Integraciones: Seguridad ejecuta la operación; el timeout de 15 s y el manejo de errores son los del adaptador de §8.6.
- Seguridad: operación pública; la respuesta neutra la garantiza Seguridad (RN-02). La app no deduce nada de la respuesta.
- Concurrencia e idempotencia: la pantalla evita envíos simultáneos; los reenvíos los limita Seguridad.

## 5. Orden de implementación

| Incremento | Resultado verificable | Dependencias | Criterios |
|---|---|---|---|
| I-01 | Enlace deshabilitado, pantalla y adaptador listos detrás de la variable, con pruebas simuladas | Propuesta §8.6.1 | CA-01 a CA-05, CA-07 |
| I-02 | Adaptador alineado con la operación confirmada, ruta del Gateway y simulación en `seguridad-local` | Confirmación de Seguridad | CA-01, CA-04 |
| I-03 | Activación en el ambiente y recorrido real con correo | I-02 y página de restablecimiento de Seguridad | CA-06, CA-08 |

## 6. Estrategia de verificación

| Criterio | Comprobación | Nivel y entorno | Dependencia real o simulada |
|---|---|---|---|
| CA-01 | `PaginaRecuperacion.test.tsx` | JSDOM | Seguridad simulada |
| CA-02 | `FormularioAcceso.test.tsx` y `PaginaRecuperacion.test.tsx` | JSDOM | No aplica |
| CA-03 | `PaginaRecuperacion.test.tsx` | JSDOM | No aplica |
| CA-04, CA-05 | `PaginaRecuperacion.test.tsx` | JSDOM | Seguridad simulada |
| CA-06 | Solicitud con correo inexistente | Ambiente con Seguridad | Real |
| CA-07 | Prueba de redirección con sesión | JSDOM | Sesión simulada |
| CA-08 | Recorrido manual con buzón | Ambiente con Seguridad | Real |

Comandos: `npm test`, `npm run test -w @despacho/repartidor`, `npm run test:administrativo`, `npm run typecheck` y `npm run build` desde la raíz del frontend.

## 7. Decisiones y pendientes

| ID | Decisión o pregunta | Justificación y fuente | Responsable | Bloquea qué incremento |
|---|---|---|---|---|
| DT-01 | Recuperación por enlace a una página de Seguridad, no por código en la app | Decisión del responsable del 23/11/2026; Despacho no maneja contraseñas | Max Rojas | No bloquea |
| DT-02 | La opción queda visible pero deshabilitada hasta la confirmación | Decisión del responsable del 23/11/2026 | Max Rojas | No bloquea |
| DT-03 | Confirmar ruta, payload, códigos, vigencia del enlace, límite y revocación de sesiones de §8.6.1 | Operación ausente del kit G7 v1.1.0 | Seguridad y Usuarios | I-02 |
| DT-04 | Página de restablecimiento de Seguridad y su URL en el correo | Fuera del alcance de Despacho | Seguridad y Usuarios | I-03 |
| DT-05 | Evaluar si el Gestor de Despacho necesita la misma opción | No se solicitó; su acceso usa MFA | Equipo de Despacho | No bloquea |

## 8. Condiciones para iniciar y cerrar

- [x] Las entradas de I-01 están revisadas y la propuesta contractual está registrada.
- [x] Las tareas indican dependencias, criterios cubiertos y verificación.
- [ ] Seguridad confirmó la operación (DT-03) antes de iniciar I-02.
- [ ] Al cerrar, todos los criterios tienen evidencia, incluida la integración real de CA-06 y CA-08.

## 9. Referencias

1. [Especificación funcional](./spec.md), [UI](./ui.md) y [tareas](./tasks.md).
2. [Contrato externo](../../integraciones/api-contract.md), §8.4, §8.6 y §8.6.1.
3. [Evidencia](./evidence.md).
