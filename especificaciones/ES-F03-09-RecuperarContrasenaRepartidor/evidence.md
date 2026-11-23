# Evidencia de ES-F03-09: Recuperación de contraseña del repartidor

**Estado:** Parcial; I-01 verificado con Seguridad simulada. No acredita la integración con Seguridad.

**Responsable de verificación:** Max Rojas

**Última verificación:** 23/11/2026.

## 1. Versión y entorno verificados

- Especificación y plan utilizados: [spec.md](./spec.md) y [plan.md](./plan.md), borradores del 23/11/2026.
- Repositorios y commits de código: frontend, rama `feature/f03-recuperar-contrasena` creada desde `origin/develop`; commit pendiente.
- Entorno: local, Windows, Node 22, Vitest 3.2 con JSDOM.
- Datos y preparación: `npm install` desde la raíz con el lockfile.
- Dependencias: Seguridad simulada con un doble de `useSesion`; la operación real no existe todavía.
- Alcance efectivamente verificado: enlace deshabilitado y habilitado, pantalla, validación, mensajes de error y mensaje neutro.

## 2. Cobertura de criterios

| Criterio | Tarea | Prueba o comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-04 | `PaginaRecuperacion.test.tsx` «CA-01» | EV-01 | Aprobado con simulación |
| CA-02 | T-02, T-04 | `FormularioAcceso.test.tsx` y «CUI-03» | EV-01 | Aprobado |
| CA-03 | T-04 | «CA-03» | EV-01 | Aprobado |
| CA-04 | T-04 | «CA-04» | EV-01 | Aprobado con simulación |
| CA-05 | T-04 | «CA-05» | EV-01 | Aprobado con simulación |
| CA-06 | T-07 | Recorrido real | Pendiente | No ejecutado |
| CA-07 | T-04 | «CA-07» | EV-01 | Aprobado |
| CA-08 | T-07 | Recorrido real | Pendiente | No ejecutado |

## 3. Registros de verificación

### EV-01. Pruebas de interfaz con Seguridad simulada

- Fecha y persona que verificó: 23/11/2026, con asistencia de IA; revisión humana pendiente.
- Tareas y criterios: T-01 a T-04; CA-01 a CA-05 y CA-07, CUI-01 a CUI-04.
- Commit y entorno exactos: rama `feature/f03-recuperar-contrasena`, cambios sin commit; local.
- Preparación y pasos o comando: desde la raíz del frontend, `npm test`, `npm run test -w @despacho/repartidor`, `npm run test:administrativo`, `npm run typecheck`, `npm run format:check` y `npm run build`.
- Resultado esperado: todas las suites y el build sin errores.
- Resultado observado: componentes compartidos 212/212, app del repartidor 19/19 y app administrativa 275/275 pruebas aprobadas; typecheck, formato y build sin errores.
- Resultado de la comprobación: Aprobado.
- Artefacto: salida de consola de los comandos.
- Dependencias simuladas y límites: Seguridad simulada; no se revisó en navegador ni con la operación real.

## 4. Uso de IA, si aplica

| Tarea | Herramienta y fecha | Documentos y revisiones de entrada | Instrucción o sesión | Resultado revisado por |
|---|---|---|---|---|
| T-01 a T-04 | Claude Code, 23/11/2026 | Contrato externo §8.4 y §8.6, ES-F03-01, plantillas SDD | Pedido del responsable: «apartado de recuperación con el botón listo, sin ejecutar nada hasta que Seguridad responda» | Pendiente |

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterio afectado | Impacto | Siguiente acción y responsable |
|---|---|---|---|
| La operación de §8.6.1 no está confirmada por Seguridad | CA-01, CA-04, CA-06, CA-08 | La opción permanece deshabilitada | Enviar la propuesta a Seguridad; Max Rojas |
| Sin revisión en navegador móvil | CUI-01 a CUI-04 | No acredita layout real | Revisar con `npm run dev:repartidor`; Max Rojas |

## 6. Entrega y revisión

- Commits y PR de implementación: pendientes.
- Revisor y fecha: pendiente.
- Resultado de revisión: pendiente.
- Estado del alcance: Parcial.
- Integraciones reales pendientes: operación y página de restablecimiento de Seguridad, ruta del Gateway y simulación en `seguridad-local`.

## 7. Referencias

1. [Especificación funcional](./spec.md): comportamiento esperado [cite: 1].
2. [Plan](./plan.md) y [tareas](./tasks.md): alcance e incrementos [cite: 2].
3. [Contrato externo §8.6.1](../../integraciones/api-contract.md#861-recuperación-de-contraseña-del-repartidor-propuesta-pendiente-de-seguridad).
