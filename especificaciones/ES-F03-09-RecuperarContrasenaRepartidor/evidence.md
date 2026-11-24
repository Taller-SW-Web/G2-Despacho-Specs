# Evidencia de ES-F03-09: Recuperación de contraseña del repartidor

**Estado:** Parcial; I-01 e I-02 verificados con Seguridad simulada. No acredita la integración con G7 desplegado.

**Responsable de verificación:** Max Rojas

**Última verificación:** 24/11/2026.

## 1. Versión y entorno verificados

- Especificación y plan utilizados: [spec.md](./spec.md) y [plan.md](./plan.md), borradores del 24/11/2026.
- Contrato de Seguridad: [OpenAPI de G7](https://github.com/Taller-SW-Web/Modulo-de-Seguridad/blob/b32b2d08bbc185a8f9ad2ff3fd634b28edb8a323/specs/contrato-api/openapi.yaml#L1433) v1.2.0, commit `b32b2d0`.
- Repositorios y commits de código: frontend y backend en la rama `feature/f03correcciones`. I-01 está en el commit `ee2a863` del frontend; los cambios de I-02 están sin commit.
- Entorno: local, Windows, Node 22, Vitest 3.2 con JSDOM, Java 23 y Maven Wrapper.
- Datos y preparación: `npm install` desde la raíz del frontend con el lockfile.
- Dependencias: Seguridad simulada con dobles de `useSesion` y `fetch`, con `seguridad-local` y con un servidor HTTP de prueba en el Gateway. G7 no está desplegado.
- Alcance efectivamente verificado: enlace deshabilitado y habilitado, pantalla, validación, mensajes, ruta del adaptador, publicación en el Gateway y simulación local.

## 2. Cobertura de criterios

| Criterio | Tarea | Prueba o comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-04, T-05, T-06 | «CA-01», «ES-F03-09» del adaptador y `publicaSoloLaSolicitudDeRecuperacionDeContrasena` | EV-01, EV-02 | Aprobado con simulación |
| CA-02 | T-02, T-04 | `FormularioAcceso.test.tsx` y «CUI-03» | EV-01 | Aprobado |
| CA-03 | T-04 | «CA-03» | EV-01 | Aprobado |
| CA-04 | T-04, T-05, T-06 | «CA-04», adaptador y `seguridad-local` | EV-01, EV-02 | Aprobado con simulación |
| CA-05 | T-04 | «CA-05» | EV-01 | Aprobado con simulación |
| CA-06 | T-06, T-07 | `seguridad-local` con correo inexistente; recorrido real | EV-02 | Aprobado con simulación; real no ejecutado |
| CA-07 | T-04 | «CA-07» | EV-01 | Aprobado |
| CA-08 | T-07 | Recorrido real | Pendiente | No ejecutado |

## 3. Registros de verificación

### EV-01. Pruebas de interfaz con Seguridad simulada

- Fecha y persona que verificó: 23/11/2026, con asistencia de IA; revisión humana pendiente.
- Tareas y criterios: T-02 a T-04; CA-01 a CA-05 y CA-07, CUI-01 a CUI-04.
- Commit y entorno exactos: frontend `ee2a863`; local.
- Preparación y pasos o comando: desde la raíz del frontend, `npm test`, `npm run test -w @despacho/repartidor`, `npm run test:administrativo`, `npm run typecheck`, `npm run format:check` y `npm run build`.
- Resultado esperado: todas las suites y el build sin errores.
- Resultado observado: componentes compartidos 212/212, app del repartidor 19/19 y app administrativa 275/275 pruebas aprobadas; typecheck, formato y build sin errores.
- Resultado de la comprobación: Aprobado.
- Artefacto: salida de consola de los comandos.
- Dependencias simuladas y límites: Seguridad simulada; no se revisó en navegador ni con G7.

### EV-02. Alineación con el contrato de G7

- Fecha y persona que verificó: 24/11/2026, con asistencia de IA; revisión humana pendiente.
- Tareas y criterios: T-01, T-05 y T-06; CA-01, CA-04 y CA-06.
- Commit y entorno exactos: rama `feature/f03correcciones` de frontend y backend, cambios sin commit; local.
- Preparación y pasos o comando: en el frontend, las mismas suites de EV-01; en el backend, `./mvnw clean verify` en `api-gateway` y la compilación y ejecución de `EmisorSeguridadLocalPruebas` como en CI.
- Resultado esperado: el adaptador llama a `/api/v1/password/recuperar`; el Gateway reenvía esa ruta sin token y rechaza `restablecer` y `cambiar`; `seguridad-local` responde `202` neutro, `429` con `Retry-After` en la cuarta solicitud por correo y `400` ante datos inválidos.
- Resultado observado: frontend 212/212, 19/19 y 276/276 pruebas aprobadas, typecheck, formato y build sin errores; `api-gateway` con 37 pruebas sin fallos, incluida la nueva de `RutasSesionRenderTests`; pruebas de `seguridad-local` completadas.
- Resultado de la comprobación: Aprobado.
- Artefacto: salida de consola y reportes de Surefire del Gateway.
- Dependencias simuladas y límites: sin G7 desplegado ni envío de correos; la pantalla de restablecer no se simula.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| T-01 a T-04 | Claude Code, 23/11/2026 | Contrato externo §8.4 y §8.6, ES-F03-01, plantillas SDD | Pedido del responsable: «apartado de recuperación con el botón listo, sin ejecutar nada hasta que Seguridad responda» | Pendiente |
| T-01, T-05, T-06 | Claude Code, 24/11/2026 | OpenAPI G7 1.2.0, `/password/recuperar` | Pedido del responsable: alinear con la API documentada por Seguridad | Pendiente |

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| G7 no tiene `canalOrigen` para la app del repartidor | CA-08 | Tras restablecer, el repartidor vuelve al login web de G7 y debe abrir la app | Solicitar el canal a Seguridad; Max Rojas |
| El OpenAPI 1.2.0 es una revisión local no desplegada | CA-06, CA-08 | Sin recorrido real | Pedir a Seguridad el ambiente desplegado; Max Rojas |
| Sin revisión en navegador móvil | CUI-01 a CUI-04 | No acredita layout real | Revisar con `npm run dev:repartidor`; Max Rojas |

## 6. Entrega y revisión

- Commits y PR de implementación: frontend `ee2a863` (I-01); cambios de I-02 pendientes de commit.
- Revisor y fecha: pendiente.
- Resultado de revisión: pendiente.
- Estado del alcance: Parcial.
- Integraciones reales pendientes: G7 desplegado con envío de correos y `canalOrigen` para la app del repartidor.

## 7. Referencias

1. [Especificación funcional](./spec.md): comportamiento esperado [cite: 1].
2. [Plan](./plan.md) y [tareas](./tasks.md): alcance e incrementos [cite: 2].
3. [Contrato externo §8.6.1](../../integraciones/api-contract.md#861-recuperación-de-contraseña-del-repartidor) y [OpenAPI de G7](https://github.com/Taller-SW-Web/Modulo-de-Seguridad/blob/b32b2d08bbc185a8f9ad2ff3fd634b28edb8a323/specs/contrato-api/openapi.yaml#L1433).
