# Evidencia de ES-F04-02: Consultar el detalle de una incidencia

**Estado:** Pendiente de implementación y verificación funcional.

**Responsable de verificación:** Gerardo.

**Última verificación funcional:** No ejecutada.

## 1. Versión y entorno verificados

- Documentación preparada: [spec.md](./spec.md), [ui.md](./ui.md), [plan.md](./plan.md) y [tasks.md](./tasks.md), en la misma revisión que crea esta carpeta.
- Origen: archivo suelto de ES-F04-02 en `0b32afc`, con la revisión funcional y contractual realizada en esta conversación. Se conservan CA-01 a CA-11.
- Base de código consultada: frontend `d2bc27d` y backend `1e7834b`; lectura estática del código, no pruebas funcionales ni acreditación de ES-F04-02 implementada.
- Commits de implementación, despliegue/entorno funcional, datos ejecutados y dependencias utilizadas: pendientes.
- Alcance acreditable en esta entrega: organización y coherencia documental; ningún CA/CUI se aprueba por ella [cite: 1, 2].

## 2. Cobertura de criterios

| Criterio | Tareas | Comprobación prevista | Registro previsto | Resultado |
|---|---|---|---|---|
| CA-01 | T-03/04/05/06/08/10 | Detalle actual, datos completos e identificación coherente. | EV-01/03/04 | No ejecutado |
| CA-02 | T-02/03/07/08/10 | Firma temporal, renovación, ampliación y permisos. | EV-02/03/04 | No ejecutado |
| CA-03 | T-03/05/07/08/10 | `NO_INTENTADO` sin foto frente a referencia faltante. | EV-01/03/04 | No ejecutado |
| CA-04 | T-03/04/05/08/10 | Inexistencia, ausencia de incidencia y datos inconsistentes. | EV-01/04 | No ejecutado |
| CA-05 | T-02/03/05/07/08/10 | Autorización y retirada de contenido protegido. | EV-01/02/03/04 | No ejecutado |
| CA-06 | T-03/04/05/06/08/10 | Dos ciclos sin recepción/fotografía heredadas. | EV-01/04 | No ejecutado |
| CA-07 | T-03/05/08/09/10 | Restricciones combinadas y máximo configurable. | EV-01/04 | No ejecutado |
| CA-08 | T-02/03/04/05/08/10 | Historia completa, orden estable y estado resuelto. | EV-01/02/04 | No ejecutado |
| CA-09 | T-03/06/07/08/10 | Fallos de dependencias y recuperación por bloque. | EV-03/04 | No ejecutado |
| CA-10 | T-03/08/09/10 | Actualización, conflicto, formularios y URL de regreso. | EV-04/05 | No ejecutado |
| CA-11 | T-04/05/06/07/08/09/10 | Lectura y renovación sin efectos de negocio. | EV-01/03/05 | No ejecutado |
| CUI-01 | T-03/08/10 | Bloques, contador, recepción, fechas y etiquetas. | EV-04 | No ejecutado |
| CUI-02 | T-03/08/09/10 | Matriz completa de decisiones y consulta histórica. | EV-04 | No ejecutado |
| CUI-03 | T-02/03/08/10 | Estados diferenciados y retirada tras `401/403`. | EV-02/04 | No ejecutado |
| CUI-04 | T-02/03/07/08/10 | Visor, respuesta anterior, renovación y cierre. | EV-02/03/04 | No ejecutado |
| CUI-05 | T-02/03/08/10 | Operaciones sin transición y comunicaciones separadas. | EV-02/04 | No ejecutado |
| CUI-06 | T-03/08/09/10 | Temporizador, actualización fallida y restauración. | EV-04/05 | No ejecutado |
| CUI-07 | T-03/06/07/08/10 | Datos desconocidos sin valores inventados. | EV-03/04 | No ejecutado |
| CUI-08 | T-02/03/08/10 | Teclado, foco, ampliación y viewport móvil. | EV-02/04 | No ejecutado |

Resultados permitidos: `Pendiente`, `Aprobado`, `Fallido`, `No ejecutado`. Fixtures y dobles identificados comprueban solo su alcance; no demuestran permisos efectivos, objetos privados ni integración real.

## 3. Registros de verificación

### EV-01. Consulta canónica, datos y seguridad

- Tareas/criterios: T-04/05/10; CA-01/03/04/05/06/07/08/11.
- Preparación prevista: PostgreSQL aislado con dos ciclos del mismo despacho, varios estados, recepción, historial y outbox; JWT de prueba con identidades/roles distintos.
- Comando previsto: `./mvnw.cmd test` desde Gestión; Docker para Testcontainers.
- Esperado: selección consistente, contrato completo, acciones correctas, histórico consultable y errores sin datos parciales; ninguna escritura por consultar.
- Fecha, persona, commit/entorno, salida observada y reporte: pendientes. **Resultado: No ejecutado.**

### EV-02. Componentes compartidos y accesibilidad

- Tareas/criterios: T-01/02/10; CCR-08-01, CCR-18-01/02 y CCR-19-01; soporte de CUI-03/04/05/08.
- Preparación prevista: fixtures de estados, enlace expirado, cambio de recurso e historial con recepción sin transición; herramientas habilitadas en T-01.
- Esperado: estados diferenciados, renovación mediante contenedor, retirada de URL/imagen, orden estable y foco/teclado utilizables.
- Fecha, persona, commit, comando/recorrido y artefactos: pendientes. **Resultado: No ejecutado.**

### EV-03. Operación y lectura de evidencia

- Tareas/criterios: T-06/07/10; CA-01/02/03/05/09/11 y CUI-04/07.
- Preparación prevista: proveedor de lotes y credencial interna; objeto privado de prueba asociado, Gestor sin perfil de repartidor, repartidor propietario/ajeno y fallos controlados.
- Comando previsto: `./mvnw.cmd test` desde Operación y pruebas del adaptador de Gestión; registrar aparte el recorrido contra almacenamiento real.
- Esperado: degradación por dato, permisos y firma/vencimiento correctos, renovación explícita y ausencia de mutaciones de negocio.
- Fecha, persona, commits, dependencias reales/dobles, salida y reportes: pendientes. **Resultado: No ejecutado.**

### EV-04. Página, actualización y navegación

- Tareas/criterios: T-03/08/09/10; CA-01 a CA-10 y CUI-01 a CUI-08.
- Preparación prevista: primero fixtures identificados y después Gateway/servicios reales; listado y formularios disponibles para los recorridos que los requieren.
- Comandos previstos: `npm run typecheck`, `npm run build` y comando de pruebas configurado en T-01. Verificar reloj controlado, respuestas fuera de orden, teclado y móvil.
- Esperado: contenido y mensajes coherentes, actualización de 30 segundos, retirada de datos protegidos, formularios con identidad/versión y regreso a la consulta restaurada.
- Fecha, persona, commits, escenarios efectivos, salidas y capturas/reportes: pendientes. **Resultado: No ejecutado.**

### EV-05. Recorrido real y ausencia de efectos de lectura

- Tareas/criterios: T-09/10; CA-10/11 y CUI-06.
- Preparación prevista: servicios reales identificados, datos sintéticos y snapshots de contador, recepción, historial, reservas y eventos antes de leer/renovar evidencia.
- Esperado: lecturas repetidas sin mutaciones; recibir/decidir solo desde sus comandos, `409` ante una decisión desactualizada y reintento exacto sin duplicados; listado actualizado después de resolver.
- Fecha, persona, commits, pasos/comandos, resultado observado y artefactos: pendientes. **Resultado: No ejecutado.**

### EV-06. Preparación y validación documental

- Alcance: migración de una sola versión activa a carpeta SDD, enlaces, índices, criterios y trazabilidad; no acredita T-01 a T-10 ejecutadas.
- Fecha y herramienta: 15/10/2026, Codex mediante Git y PowerShell; revisión documental del mismo commit que introduce esta carpeta.
- Comprobaciones ejecutadas: `git diff --check`; enlaces/anclas locales y ejemplos JSON; existencia de cinco archivos, ausencia de la ruta anterior, IDs únicos y cobertura CA/CUI en tareas/evidencia; sin marcadores de plantilla ni casillas de implementación completadas.
- Resultado observado: formato correcto, 380 enlaces/anclas locales válidos y 24 ejemplos JSON válidos en 22 archivos nuevos/modificados; 11 CA, 8 CUI, 10 tareas y 6 registros de evidencia. `spec.md` conserva 172 líneas sin bloques de código.
- **Resultado: Aprobado exclusivamente para preparación documental.** EV-01 a EV-05 siguen sin ejecutar; T-01 a T-10 permanecen pendientes y la revisión humana queda pendiente.

Al ejecutar una comprobación, conservar commit/entorno exactos, preparación reproducible, resultado observado y artefactos. No registrar tokens, credenciales, datos personales reales ni URLs firmadas.

## 4. Uso de IA

| Trabajo | Herramienta y fecha | Entradas y revisión | Instrucción y revisión humana |
|---|---|---|---|
| Revisión funcional y preparación de carpeta SDD | Codex, 15/10/2026 | Archivo ES-F04-02 revisado en esta conversación, plantillas SDD, contratos, modelo, diseño/componentes y bases de código de §1. | Gerardo solicitó alinear la especificación, generar los cinco Markdown y guardar un commit con título breve. Documentos preparados con asistencia de IA; revisión humana de esta entrega pendiente. |

La conversación registra el proceso, no demuestra el cumplimiento de criterios funcionales.

## 5. Diferencias, fallos y pendientes

| Hallazgo | Criterios afectados | Siguiente acción y coordinación |
|---|---|---|
| DT-01: herramientas y componentes por verificar/implementar. | Todos los CUI; CA-02/05/08. | T-01/02; Gerardo con responsables de componentes. |
| DT-02: fuentes y productores históricos por implementar/verificar. | CA-01/04/06/08/11. | T-04/05; Gerardo con Arquitectura y F-02/F-03. |
| DT-03: lotes, credenciales y evidencia privada sin comprobación real. | CA-02/03/05/09/11. | T-06/07; coordinación con Operación/F-03 y DevOps. |
| DT-04: listado y formularios propietarios pendientes para recorrido completo. | CA-07/10/11; CUI-02/06. | T-09; no acreditar decisiones simuladas como reales. |
| DT-05: parámetros y zona operativa definidos documentalmente, sin verificar ejecución. | CA-02/07 y fechas. | Probar configuración y presentación conforme al plan. |

## 6. Entrega y revisión

- Entrega actual: documentos SDD y alineamiento de contratos/referencias.
- Commit documental: el que introduce esta carpeta; no es un commit de implementación.
- Commits/PR de implementación, revisor, fecha y resultado de revisión: pendientes.
- Estado del alcance funcional: Pendiente; EV-01 a EV-05 no ejecutados.
- Integraciones reales pendientes: Gestión, Operación, almacenamiento privado, identidad y recorridos con ES-F04-01/03/04/05.

## 7. Referencias

- [cite: 1] [Especificación](./spec.md) y [UI](./ui.md): criterios y comportamiento esperado.
- [cite: 2] [Plan](./plan.md), [tareas](./tasks.md) y [flujo SDD](../../plantillas/sdd/README.md): preparación, incrementos y evidencia.
- [cite: 3] [Gestión](../../integraciones/api-contract-gestion-despachos.md), §§5.2/5.3; [Operación](../../integraciones/api-contract-operacion-reparto.md), §§3.4/5.4; [componentes React](../../disenio/componentes-react.md), §4.2.
