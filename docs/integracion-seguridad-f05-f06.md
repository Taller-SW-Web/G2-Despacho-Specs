# Preparación de la integración F-05/F-06 con Seguridad

**Fecha:** 03/11/2026. **Responsable de Despacho:** Kevin Rhamses Bohorquez.
**Estado:** preparación local; cuentas, concesiones, eventos y aceptación conjunta pendientes.

## 1. Alcance y fuentes

Este documento organiza la ejecución y la evidencia; el contrato canónico sigue en [Seguridad §8](../integraciones/api-contract.md#8-integración-con-seguridad-y-usuarios) y [Operación §4](../integraciones/api-contract-operacion-reparto.md#4-api-de-f-05-y-f-06-perfiles-flota-y-jornadas). No redefine payloads de Seguridad.

Fuentes leídas de las carpetas suministradas por el usuario, sin modificarlas ni actualizarlas:

- Repositorio documental `Modulo-de-Seguridad-main`: `specs/kit-integracion.md`, SPEC-03/11/17/18, `specs/contrato-api/openapi.yaml`, `docs/integracion/acuerdos.md`, `docs/integracion/matriz-scopes.md` y `specs/catalogo-eventos.md` [cite: 1].
- Backend `Modulo-de-Seguridad-Backend-develop`: README de despliegue, controladores de usuarios/login/descubrimiento y catálogo SQL de scopes. Es código de Seguridad de solo lectura; la carpeta exportada no acredita un SHA remoto.
- Frontend de Seguridad: instrucciones de sesión en memoria. No se comparten tokens entre orígenes mediante almacenamiento del navegador.
- Bases de Despacho: Specs `03343ce` en `main`, frontend `da7efad` y backend `e4f8ee1` en `develop`. Código preparado en `feature/f05-f06-integracion-seguridad`; documentación en `docs/f05-f06-integracion-seguridad`, desde `main` porque Specs no tiene `develop`.

Si un enlace remoto no contiene aún una reorganización de las fuentes exportadas, se debe confirmar su revisión con G7; no se afirma que la copia suministrada coincida con el main publicado.

Huellas SHA-256 de las fuentes exportadas leídas (raíz documental G7, no la copia anidada):

| Fuente | SHA-256 |
|---|---|
| `docs/integracion/acuerdos.md` | `f1d421f4401cb419cb6855e1ae8ea30337d8f2ac3bae5414c00a58e1c9ab67b7` |
| `specs/kit-integracion.md` | `10e41026388d16d3594e1620e325f333ff14e496f37aee5158dd39588f3ffd31` |
| `specs/catalogo-eventos.md` | `4bbc55f7765da3d9b7fefe4af335ced4e3315d814282af34e494b71f9d872a19` |

## 2. Decisiones ya resueltas por Seguridad

| Decisión | Aplicación en F-05/F-06 |
|---|---|
| A5: el repartidor es un perfil local | Guardar el UUID de Seguridad; resolverlo mediante `sub`. No pedir rol `REPARTIDOR` ni claim `idRepartidor`. |
| A6: alta administrativa y activación por enlace | El administrador global crea la cuenta, sin contraseña elegida por el Gestor. Puede llevar `roles: []`; el titular activa y establece su contraseña. |
| No hay alta global con token de servicio | El registro de F-05 conserva `ACTIVO`/`PENDIENTE`; la vinculación solo guarda el UUID y audita. |
| Login JSON, MFA, refresh y logout | Los responsables de sesión/F-03/Gateway adaptan sus consumidores al contrato de G7. No se desarrolla otro proveedor de identidad dentro de F-05/F-06. |
| Usuario y servicio son perfiles de token distintos | Operación exige el perfil de claims de G7; un JWT de servicio no sustituye al repartidor ni al Gestor. No exigir audiencia de servicio a una persona. |
| JWT local no comprueba revocación inmediata | No prometer bloqueo global inmediato sin consumidor/reconciliación o mecanismo autorizado y probado. `usuarios:leer` no equivale a `tokens:introspeccion`. |
| Reactivación global y alta local son dimensiones distintas | Nunca rehabilitar una baja local por recibir un desbloqueo global; tampoco cerrar jornadas o liberar reservas automáticamente. |

## 3. Trabajo propio y dependencias

| ID | Resultado | Dueño | Situación |
|---|---|---|---|
| SEG-01 | Conciliar contrato y ES-F05-05/ES-F06-01 con A5/A6 y JWT | Rhamses | Verificado documentalmente; sin aceptación externa |
| SEG-02 | Explicar en vinculación y apertura qué comprueba cada operación | Rhamses | Implementado localmente; sin crear cuentas globales |
| SEG-03 | Validar UUID/roles de acceso, iat/jti y scope de servicio en Operación | Rhamses | Verificado localmente con firma RS256/JWKS; ver EV-G7 de las ES |
| SEG-04 | Entregar cliente técnico, secreto y concesiones por ambiente | Seguridad/operaciones | Pendiente de acreditación; no hay secretos reales en esta entrega |
| SEG-05 | Canal administrativo de alta/baja y entrega del UUID | Rhamses y Seguridad | Propuesta: administrador G7 crea cuenta; comunica UUID al Gestor; titular activa. Falta designar personas y canal; no es un acuerdo confirmado |
| SEG-06 | Publicar broker, permisos y revisión del catálogo de eventos | Seguridad | Pendiente de confirmación operativa |
| SEG-07 | Consumir eventos y reconciliar el estado global sin alterar la baja local | Rhamses | Pendiente de SEG-06 y aceptación de la proyección/reconciliación; no implementado por esta revisión |
| SEG-08 | Integrar acceso/MFA/refresh/logout y sesión en memoria | Responsables de sesión, F-03 y Gateway | Dependencia compartida pendiente; esta tarea no modifica sus flujos |
| SEG-09 | Ejecutar recorrido con cuentas y credenciales reales | Ambos equipos | Pendiente de SEG-04/05/08; los dobles no lo sustituyen |

Las reglas de flota existentes conservan el historial: el cambio de cuenta, la desvinculación y la reactivación local no están habilitados por el contrato actual. Una solicitud de corrección se coordina y se especifica antes de programarla.

## 4. Solicitud concreta de aprovisionamiento

Enviar por el canal que acuerden los responsables; este documento no envía mensajes ni acredita aprobación de Seguridad:

1. Aprovisionar `modulo-despacho` por ambiente y entregar su secreto por un canal seguro, con procedimiento de rotación y revocación.
2. Verificar `usuarios:leer` y `direcciones:leer` para `api-seguridad`, ya aprobados documentalmente.
3. Registrar y conceder los seis scopes internos de [§8.2](../integraciones/api-contract.md#82-obtención-de-un-token-de-servicio), con audiencia `api-despacho`. No se encontraron en el catálogo G7 suministrado. Un scope escrito por Despacho no demuestra una concesión efectiva.
4. Verificar `ventas:pedidos:estado` para `api-ventas`; coordinar `productos:fisicos:leer` para `api-productos` con el dueño de Productos. Son dependencias de otros recorridos de Despacho, no permisos de administración de identidades.
5. Verificar las concesiones de Marketplace/Chatbot/Ventas contra nuestra API según [§3.4](../integraciones/api-contract.md#34-scopes-de-servicio-de-despacho). No mezclar credenciales de esos equipos con las de Despacho.
6. Proveer cuentas de prueba de Gestor, repartidor activado sin rol global, pendiente de activación y bloqueado/inactivo. Comunicar UUID y estado por el canal acordado; no compartir contraseñas definitivas.
7. Confirmar conexión RabbitMQ, TLS, permisos, retención, disponibilidad de productores y suscripciones; especialmente `usuario.roles_cambiados`, que Despacho prevé pero no figura entre los cuatro eventos de su suscripción confirmada en la cabecera del catálogo exportado.

No solicitar `tokens:introspeccion` como si ya estuviera concedido: G7 no lo concede a Despacho en la matriz revisada. Si se necesita certeza inmediata, justificar el caso y obtener su aprobación.

## 5. Preparación del entorno

El README del backend G7 declara el origen H3 `https://g7-auth-service.onrender.com`. La comprobación pública del 03/11/2026 obtuvo HTTP 200 en salud, descubrimiento y JWKS. Esto no demuestra login, cuentas aprovisionadas, concesiones ni broker.

En Gateway, Gestión y Operación, configurar el origen sin ruta:

```dotenv
SEGURIDAD_URL=https://g7-auth-service.onrender.com
SEGURIDAD_AUDIENCIA=api-despacho
SEGURIDAD_ALGORITMO=RS256
DEMO_SIN_AUTENTICACION=false
```

Las plantillas no contienen secretos; las variables del cliente técnico se cargan en el proceso/panel del servidor. El Compose de desarrollo conserva el emisor simulado y no acredita la integración real. No cambiar un entorno desplegado ni ejecutar migraciones compartidas para verificar este documento.

## 6. Matriz de aceptación conjunta

| Caso | Resultado esperado | Evidencia actual |
|---|---|---|
| Crear perfil sin Seguridad disponible | Alta local pendiente; sin cuenta global ni contraseña | Implementación existente; regresión PostgreSQL requerida |
| Crear/activar cuenta G7 sin roles | Titular activa; token de acceso con `sub` UUID y `roles: []` | Recorrido G7 real pendiente |
| Vincular y repetir | UUID único, 204, auditoría única; no creación remota | Código existente; pruebas locales según evidence de ES-F05-05 |
| UUID ajeno/duplicado, perfil inactivo o sustitución de vínculo | Rechazo contractual sin cambiar vínculo ni auditoría | Pruebas PostgreSQL existentes; ejecución actual identificada por separado |
| JWT firmado RS256 con perfil de acceso G7 | Operación lo valida sin exigir rol global de repartidor | Prueba criptográfica local con JWKS controlado |
| JWT sin iat/jti/roles, sub no UUID, refresco o servicio de otra audiencia | Rechazo antes del negocio | Pruebas locales del validador y decoder |
| Repartidor vinculado activo frente a pendiente/inactivo/sin perfil | Acceso permitido o denegado por su perfil local | Pruebas existentes del filtro; no confundir con estado global |
| Abrir jornada y reservar con recursos aptos | Éxito; perfil pendiente/inactivo no admite apertura/carga | Suites F-06 existentes; alcance y resultados en su evidencia |
| Bloqueo global durante jornada; vencimiento de bloqueo temporal | Negar lo acordado sin perder reservas ni alterar la baja local | Pendiente de eventos/reconciliación y pruebas conjuntas |
| Eventos repetidos, desordenados, desconocidos y perdidos | Aplicar reglas del catálogo G7; reconciliar por API | Pendiente de SEG-06/07 |
| Token de servicio real con los seis scopes internos | Comunicación Gestión/Operación autorizada sin JWT humano reenviado | Pendiente de concesiones y secreto reales |
| Expiración, cambio de roles, rotación de claves y caída de JWKS | Rechazo/caché/recuperación conforme a G7, sin prometer revocación instantánea | Pruebas específicas pendientes; el decoder local no certifica una rotación desplegada |

La aceptación conjunta solo se completa con revisiones, entorno, fecha, ejecutor y resultados registrados. La preparación documental y las pruebas locales no se marcan como integración al 100%.

## 7. Referencias

1. [Kit G7](https://github.com/Taller-SW-Web/Modulo-de-Seguridad/blob/main/specs/kit-integracion.md), [acuerdos](https://github.com/Taller-SW-Web/Modulo-de-Seguridad/blob/main/docs/integracion/acuerdos.md), [catálogo de eventos](https://github.com/Taller-SW-Web/Modulo-de-Seguridad/blob/main/specs/catalogo-eventos.md) [cite: 1]. Revisiones leídas: exportaciones locales suministradas; disponibilidad de esos mismos paths en main no acreditada.
2. [ES-F05-05](../especificaciones/ES-F05-05-VincularRepartidorConSeguridad/spec.md) y [ES-F06-01](../especificaciones/ES-F06-01-AbrirJornada/spec.md) [cite: 2].
