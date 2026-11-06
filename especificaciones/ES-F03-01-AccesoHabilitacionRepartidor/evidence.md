# Evidencia de ES-F03-01: Acceso y habilitación operativa del repartidor

**Estado:** Pendiente; no acredita implementación.

**Responsable de verificación:** Max Rojas

**Última verificación:** Pendiente

## 1. Versión y entorno

- Documentos: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión.
- Commits de frontend y backend: pendientes.
- Entorno: pendiente.
- Datos: sintéticos; sin datos personales reales ni tokens.

## 2. Cobertura de criterios

| Criterio | Tarea | Comprobación | Registro | Resultado |
|---|---|---|---|---|
| CA-01 | T-03, T-04 | Acceso en turno con transiciones habilitadas | EV-01, EV-03 | Pendiente |
| CA-02 | T-03, T-04 | `401` sin token o vencido, sin datos | EV-01, EV-03 | Pendiente |
| CA-03 | T-03, T-04 | `403` por rol o falta de vínculo | EV-01, EV-03 | Pendiente |
| CA-04 | T-03, T-04 | Solo lectura y `409` fuera de turno | EV-01, EV-03 | Pendiente |
| CUI-01 a CUI-05 | T-01, T-04 | Modos, mensajes, accesibilidad y móvil | EV-02, EV-03 | Pendiente |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Una comprobación con fixtures o dobles no acredita integración real.

## 3. Registros

### EV-01. Seguridad y contexto en backend

- Criterios: CA-01 a CA-04.
- Resultado esperado: `401`, `403` y `409` correctos; contexto resuelto solo desde el token.
- Dependencias simuladas: F-05 (identificar si es doble).
- Resultado observado: pendiente.

### EV-02. UI con fixtures

- Criterios: CUI-01 a CUI-05.
- Resultado esperado: modos y mensajes correctos en móvil. No valida la autorización real.
- Dependencias simuladas: API.
- Resultado observado: pendiente.

### EV-03. Recorrido con servicios reales

- Criterios: CA-01 a CA-04 y CUI-01 a CUI-05.
- Resultado esperado: comportamiento completo con Seguridad y Usuarios y F-05 reales.
- Dependencias simuladas: ninguna.
- Resultado observado: pendiente.

Cada registro ejecutado indica fecha, persona, commit, entorno, pasos, resultado observado y artefacto.

### EV-04. Preparación de sesión y doble local · 05/11/2026

- Alcance: acceso humano de ambas apps, MFA del gestor, renovación rotativa, perfil y cierre; referencia única de formatos en [contrato externo §8.6](../../integraciones/api-contract.md#86-acceso-humano-de-ambas-aplicaciones).
- Código: ramas `feature/sesion-mfa-local` de Frontend/Backend, sobre frontend `16feb89` y backend `614f685`. Documentación: `docs/sesion-mfa-local` de Specs. Incremento sin commit ni publicación en esta fase.
- Fuente externa: copia de `Modulo-de-Seguridad-main` facilitada por el usuario; kit §7, SPEC-05/06/09 y OpenAPI v1.1.0, que declara `revision-local-no-publicada`.
- Implementación preparada: transporte humano compartido, sesión en memoria independiente por app, renovación única ante concurrencia, protección de navegación, código OTP aleatorio visible solo en buzón Vite local, y proxy de acceso humano en Gateway base/render. El emisor requiere habilitación explícita; no crea cuentas en G7 ni perfiles F-05.
- Regresiones escritas: acceso sin sesión, desafío sin tokens, validación de rol, renovación concurrente y resultado tardío tras logout, limpieza local ante fallo remoto; emisor con OTP/rotación/reutilización/independencia de familias, y rutas de Gateway. No se afirma que estos casos hayan aprobado.
- Resultado observado: revisión de código y documentación exclusivamente. Por instrucción explícita del usuario no se ejecutaron pruebas, comprobación de tipos, builds, Maven, Compose, peticiones a G7 ni validación de navegador. CA/CUI, integración y aceptación permanecen abiertos.
- Límites: falta verificar disponibilidad y revisión desplegada, CORS, gestor activado con MFA/entrega real del OTP y dos repartidores activados con sus UUID. Las credenciales entre microservicios siguen siendo una dependencia distinta. Los JWT ya emitidos pueden seguir válidos hasta vencer; no se implementó revocación distribuida.

### EV-05. Verificación local autorizada · 05/11/2026

- Entorno: Compose ya iniciado por el usuario, Gateway local y frontends Vite en `localhost:5173` y `localhost:5174`. Seguridad temporal de G2; no se realizaron llamadas a G7 ni escrituras de negocio.
- Navegador: credenciales incorrectas rechazadas; gestor entra únicamente después de verificar OTP; un repartidor no obtiene acceso administrativo. Gerardo entra sin MFA y su ruta informa fuera de turno; Kevin consulta su ruta existente. Ambos pueden cerrar sesión y vuelven al ingreso. Recargar la app del repartidor elimina la sesión en memoria. La sesión de Kevin siguió permitiendo actualizar su ruta tras el intervalo de vigencia inicial.
- MFA: tres errores agotan los intentos; reenviar genera otro código, invalida el anterior y conserva el vencimiento original del desafío. La cuarta solicitud devuelve la limitación y deshabilita reenvío; el código vigente todavía permite terminar el acceso.
- Correcciones realizadas al verificar: etiquetas accesibles explícitas; aviso de desarrollo como nota; cierre del repartidor con icono visible sobre la cabecera oscura; cuenta atrás calculada con la hora actual al abrir un desafío. La ruta humana del Gateway se configura en Java para que el perfil demo sin `SEGURIDAD_URL` no intente registrar un destino vacío. Las pruebas de rutas de flota preparan ahora su sesión explícitamente.
- Comprobaciones aprobadas: `npm run typecheck`, `npm run build` de ambas apps, 13 pruebas del repartidor, 208 pruebas compartidas más la nueva regresión del contador, comprobaciones HTTP/criptografía del emisor y `clean verify` del Gateway con 30 pruebas sin fallos ni omisiones. Los casos de sesión incluyen renovación automática con reloj controlado, vencimiento del desafío, renovación concurrente y cierre con respuesta tardía.
- Suite administrativa: 218 de 219 pruebas aprobaron en la repetición con un único proceso, incluidos los diez casos de sesión. Un caso de `CierreRecorrido.test.tsx` agotó la espera del listado vacío; había aprobado en la primera ejecución y sus dos casos aprobaron al repetir ese archivo aislado (35,67 s en total). La ejecución paralela con compilaciones había agotado otras siete esperas, que aprobaron al repetir por separado. No se aumentaron límites ni se debilitaron aserciones. Todos los casos tuvieron una ejecución satisfactoria; la suite general no se registra como completamente verde en una sola ejecución.
- Artefactos locales fuera de Git: `G2-Despacho-Frontend/test-results/sesion-local/gestor-autenticado.jpg`, `repartidor-autenticado.jpg` y `administrativo.log`; informe Maven en `G2-Despacho-Backend/api-gateway/target/surefire-reports/`.
- Límite: valida acceso/sesiones con el doble local y navegación sobre los datos existentes. No acredita entrega de OTP real, integración G7, almacenamiento de evidencia, aceptación completa de F-03 ni recorrido funcional completo en nube.

### EV-06. Publicación para revisión · 05/11/2026

- [Frontend PR #21 hacia `develop`](https://github.com/Taller-SW-Web/G2-Despacho-Frontend/pull/21), commit `2f6bc0a`: acceso de ambas apps, formulario compartido, MFA, sesión en memoria, renovación y cierre.
- [Backend PR #29 hacia `develop`](https://github.com/Taller-SW-Web/G2-Despacho-Backend/pull/29), commit `c5d887b`: emisor local de sesiones y ruta humana común a los perfiles del Gateway.
- Ambas ramas están sincronizadas con sus bases remotas. Las descripciones conservan los resultados de EV-05, el fallo intermitente de la ejecución administrativa completa y los pendientes de G7. CI remoto, revisión y aceptación quedan sujetos al estado de los PR; esta publicación no cierra los criterios de integración real.

## 4. Uso de IA

| Tarea | Herramienta y fecha | Entrada | Revisado por |
|---|---|---|---|
| Segmentación documental en formato SDD | Claude, 16/10/2026 | Especificación ES-F03-01 previa y estructura de ES-F01-01 | Pendiente |

## 5. Pendientes

| Hallazgo | Criterio | Impacto | Acción |
|---|---|---|---|
| DT-01: autenticación con Seguridad y Usuarios | CA-01 a CA-03 | Bloquea integración real | Max Rojas con Arquitectura |
| DT-02: DTO y códigos de error | CA-03, CA-04 | Bloquea mensajes definitivos | Max Rojas con Backend |
| DT-03: consulta a F-05 | CA-01, CA-04 | Bloquea backend real | Max Rojas con F-05 |
| DT-05: estado en turno sin asignación diaria | CA-01, CA-04 | Regla incompleta | Max Rojas con F-05 |

## 6. Entrega y revisión

- PR de implementación: pendiente.
- Revisor y fecha: pendientes.
- Estado del alcance: Pendiente.
