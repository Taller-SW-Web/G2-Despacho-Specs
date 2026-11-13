# UI de ES-F01-12: Activar o desactivar un distrito

## 1. Pantalla y componentes

Acciones del listado con ModalConfirmacion, notificaciones y EstadoVista del [paquete compartido](../../disenio/componentes-react.md) [cite: 1].

## 2. Interacción y estados

- CUI-01: Confirmación de baja: «San Borja dejará de admitir nuevas cotizaciones y solicitudes de despacho. Los despachos existentes continuarán su proceso. Sus asociaciones con zonas se conservarán».
- CUI-02: Reactivación explícita, sin prometer zona activa ni tarifa; estado/filtro se refrescan tras éxito confirmado.
- CUI-03: Conflicto actualiza datos consultados y exige otra confirmación. Fallos no se presentan como éxito; bloqueo durante envío.
- CUI-04: Formulario de zona conserva inactivos asociados, los rotula «Inactivo · sin cobertura» y permite retirarlos; solo activos para nuevas selecciones. Conserva cobertura exclusivamente postal.
- CUI-05: Modal con foco atrapado/restaurado, cancelar por teclado, acciones rotuladas y sin depender del color.

## 3. Verificación

Componentes y recorrido navegador/Gateway en base desechable; [evidence.md](./evidence.md). [cite: 1] [Spec](./spec.md) y componentes de §1.
