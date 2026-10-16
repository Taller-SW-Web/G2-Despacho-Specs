# UI de ES-F03-08: Consulta autorizada de la evidencia

**Responsable:** Max Rojas

**Estado:** Borrador

**Aplicabilidad:** Visor de evidencia en la web del repartidor y en las vistas administrativas que lo consuman (F-04).

**Especificación funcional:** [spec.md](./spec.md)

## 1. Usuario, contexto y objetivo

- Usuarios: repartidor propietario (celular) y Gestor de Despacho (escritorio).
- Objetivo visible: ver la fotografía de evidencia de un despacho.
- Entrada: detalle del despacho (ES-F03-03) o incidencia en F-04.

## 2. Referencias visuales

| Fuente | Aplicación |
|---|---|
| [Sistema de diseño](../../disenio/SYSTEM-DESIGN.md) | Visor, estados y mensajes |
| [Componentes React](../../disenio/componentes-react.md) | Componentes compartidos aplicables (DT-02 del plan) |

## 3. Pantallas e interacción

### UI-01. Visor de evidencia

| Elemento | Contenido y comportamiento |
|---|---|
| Imagen | Fotografía cargada desde la URL firmada; texto alternativo con el código del despacho |
| Vencimiento | Al vencer, se sustituye la imagen por el aviso y la acción «Renovar enlace» |
| Persistencia | No guarda la URL; al cambiar de recurso descarta la imagen anterior |

| Paso | Acción | Respuesta de la interfaz | Criterio |
|---|---|---|---|
| 1 | Pulsar «Ver evidencia» | Carga y fotografía | CA-01 |
| 2 | Enlace vencido | «El enlace venció» y «Renovar enlace» | CA-01, CA-02 |
| 3 | Pulsar «Renovar enlace» | Nueva solicitud autorizada y fotografía | CA-01 |
| 4 | Respuesta `403` | Acceso denegado sin imagen | CA-03 |
| 5 | Fallo de carga | «No se pudo cargar la fotografía» y «Reintentar»; sin indicar que no existe | RN-06 |

## 4. Estados de la interfaz

| Estado | Qué se muestra | Acciones | Criterio |
|---|---|---|---|
| Cargando | Indicador en el área de imagen | Esperar | CA-01 |
| Visible | Fotografía | Cerrar | CA-01 |
| Enlace vencido | Aviso | «Renovar enlace» | CA-01 |
| Acceso denegado | Mensaje sin imagen | Cerrar | CA-03 |
| Fallo de carga | Mensaje sin afirmar ausencia | «Reintentar» | RN-06 |

## 5. Accesibilidad

- Imagen con texto alternativo; visor cerrable con teclado.
- Mensajes anunciados a lectores de pantalla.
- Adaptación a móvil y escritorio.

## 6. Verificación de UI

| ID | Condición y acción | Resultado observable | Criterio |
|---|---|---|---|
| CUI-01 | Abrir como propietario y como Gestor | Fotografía visible | CA-01 |
| CUI-02 | Dejar vencer el enlace y renovar | Aviso y nueva carga autorizada | CA-01 |
| CUI-03 | Cambiar de despacho en el visor | No se muestra la imagen anterior | CA-01 |
| CUI-04 | Recibir `403` o fallo de carga | Mensajes correctos sin imagen | CA-03 |

## 7. Referencias

1. [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md) y [evidence.md](./evidence.md).
