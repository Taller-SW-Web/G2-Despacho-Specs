# UI de ES-F01-10: Registrar un distrito

## 1. Formulario y componentes

Panel izquierdo de `/distritos`; `/distritos/nuevo` es un acceso compatible a la misma administración en modo alta. React Hook Form, Zod, campos Mantine y notificación compartida. Formulario sin navegación propia ni segundo título principal. Reutiliza [sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [componentes React](../../disenio/componentes-react.md) [cite: 1].

## 2. Interacción y estados

- CUI-01: Nombre, provincia, departamento y ubigeo textual; validar campos obligatorios y geografía antes de enviar.
- CUI-02: Errores de API por campo y mensaje general; conservar valores ante fallos. Guardando deshabilita acciones duplicadas.
- CUI-03: **Guardar distrito** confirma éxito, limpia el formulario y renueva el listado conservando filtros, sin salir de la administración. Informar si el registro queda oculto por los filtros. El fallo del refresco no convierte un guardado confirmado en error ni permite repetirlo como recuperación.
- CUI-04: Etiquetas asociadas, foco en primer error y navegación por teclado; ancho adaptado a móvil.
- CUI-05: **Limpiar formulario**, seleccionar una edición y volver a zonas requieren confirmar el descarte si existen cambios. Cancelar conserva el borrador. Cierre/recarga con pendientes utiliza `beforeunload`.

## 3. Verificación

Pruebas de formulario con API simulada y recorrido navegador real aislado; [evidence.md](./evidence.md). [cite: 1] [Spec](./spec.md) y fuentes de §1.
