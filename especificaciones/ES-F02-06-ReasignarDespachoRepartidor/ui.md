# UI de ES-F02-06: Reasignar despacho a otro repartidor

**Responsable:** Tarqui.

**Estado:** Modal implementado y verificado con React y navegador contra G2 real; aceptación humana pendiente.

**Recuperación:** se conservan clave, versión original y cuerpo tras timeout, `503` o `DESP_ERROR_REASIGNACION_EN_PROCESO`. No se permite cambiar destino/motivo, cerrar por Escape ni descartar; se ofrece «Recuperar reasignación». Un rechazo definitivo libera esa edición; un conflicto recarga la ruta. Las barras usan las métricas reales de F-06, sin fabricar límites. No se añaden bibliotecas de estado o UI.

**Aplicabilidad:** Modal interactivo de reasignación invocado desde la pestaña "Rutas por repartidor" (`/programacion`).

**Especificación funcional:** [spec.md](./spec.md).

## 1. Usuario, contexto y objetivo

- **Usuario:** Gestor de Despacho con rol `GESTOR_DESPACHO`.
- **Contexto:** Modal centrado que se abre desde una tarjeta de despacho `ASIGNADO` al pulsar el botón secundario "Reasignar".
- **Objetivo:** Mostrar los datos del despacho y el conductor actual, seleccionar un nuevo conductor disponible con capacidad suficiente, registrar el motivo obligatorio del cambio y confirmar la transferencia operativa.
- **Componentes React asociados:** Mantine `Modal` (CR-12), `Card` de Repartidor (CR-20), `Progress` (CR-11), `Textarea` (CR-02), `Button` (CR-01), `NotificacionOperacion` (CR-15).

## 2. Referencias visuales

- [SYSTEM-DESIGN.md](../../disenio/SYSTEM-DESIGN.md): secciones 13.4, 16.4, 17, 18 y 21.
- [Diseño F-02](../../disenio/funcionalidades/f-02.md): Pantalla 4 (Modal de Reasignación de Despacho).
- [Componentes React](../../disenio/componentes-react.md): CR-01, CR-02, CR-11, CR-12, CR-15, CR-20.

## 3. Pantallas e interacción

### UI-01. Resumen del despacho y repartidor actual

- Tarjeta superior que identifica:
  - Código de rastreo, pedido y dirección de destino.
  - Carga física: peso en kg, volumen en m³ y cantidad de paquetes.
  - Conductor actual asignado (nombre, placa de furgoneta y posición actual en su ruta).

### UI-02. Selección de nuevo repartidor y barras de capacidad

- Lista de selección o catálogo desplegable con los otros repartidores habilitados para hoy (excluye al chofer actual).
- Al elegir un candidato:
  - Muestra sus tres barras de ocupación actuales y la proyección sombreada sumando el paquete a reasignar.
  - Si el candidato no tiene cupo en peso, volumen o paquetes, la barra sobrecargada se muestra en rojo y se bloquea la confirmación.

### UI-03. Campo obligatorio de motivo

- Campo `Textarea` con etiqueta "Motivo de la reasignación" marcado con asterisco rojo de obligatoriedad (`required`).
- Placeholder: *"Indique la causa operativa del cambio (ej. avería en furgoneta, redistribución de carga)"*.
- Validación visual inmediata: si el usuario intenta enviar con el campo vacío o con solo espacios, se muestra mensaje de error *"El motivo es obligatorio para reasignar"*.

### UI-04. Botones y confirmación

- Botón "Cancelar": cierra el modal sin alterar asignaciones.
- Botón primario "Confirmar reasignación":
  - Deshabilitado mientras no se elija nuevo chofer, si el chofer elegido no tiene capacidad o si el motivo está vacío.
  - Al pulsar, entra en estado `loading` con spinner impidiendo dobles envíos.
- Tras éxito: toast informativo, cierre de modal y recarga reactiva de la ruta.

## 4. Criterios de aceptación de interfaz (CUI)

### CUI-01. Apertura con exclusión del chofer actual
- **DADO** un despacho asignado al repartidor "Carlos Chofer".
- **CUANDO** se abre el modal de reasignación.
- **ENTONCES** en la lista de candidatos para reasignación no aparece "Carlos Chofer", solo los demás repartidores en turno.

### CUI-02. Exigencia visible del motivo
- **DADO** que se seleccionó un nuevo chofer con capacidad disponible.
- **CUANDO** el campo de motivo está vacío.
- **ENTONCES** el botón "Confirmar reasignación" permanece deshabilitado.

### CUI-03. Advertencia de sobrecarga en candidato
- **DADO** un chofer candidato cuya capacidad libre de peso es menor al peso del paquete.
- **CUANDO** se evalúa su tarjeta.
- **ENTONCES** la barra de peso se torna roja con advertencia de sobrecarga y no permite su selección.

### CUI-04. Prevención de doble clic
- **DADO** que el usuario hace clic en "Confirmar reasignación".
- **CUANDO** la llamada HTTP está en tránsito.
- **ENTONCES** el botón muestra spinner y no admite clics sucesivos.

### CUI-05. Actualización reactiva tras éxito
- **DADO** que el backend responde HTTP 200.
- **CUANDO** se procesa la confirmación.
- **ENTONCES** el modal se cierra, se emite toast de confirmación y el despacho desaparece de la ruta del chofer origen.
