# UI de ES-F02-09

## 1. Composición

Reutilizar [CR-01, CR-02, CR-12 y CR-15](../../disenio/componentes-react.md) y el [sistema de diseño](../../disenio/SYSTEM-DESIGN.md). Botón «Adelantar a hoy» en filas futuras de la cola; no habilitar «Asignar» hasta confirmar y releer.

## 2. Confirmación y estados

- Modal con código, fecha original y hoy del servidor, motivo obligatorio de hasta 500 puntos de código y aviso: «No asigna un repartidor ni reserva capacidad».
- Confirmar y Cancelar; carga bloquea cierre, Escape y doble envío. Pausar refresco periódico mientras esté abierto.
- Éxito: notificación, cierre, recarga de cola e indicadores, conservar filtros y devolver foco al origen o a un control existente si desapareció.
- Conflicto: pedir cerrar y recargar, sin reenviar datos obsoletos. Sin permiso: cerrar controles protegidos.
- Resultado incierto: bloquear edición del motivo y comando nuevo; ofrecer recuperación explícita del mismo comando y consulta de cola.
- Controles táctiles de 44 px, etiquetas accesibles, foco contenido y modal adaptado a móvil.
