# UI de ES-F01-10: Registrar un distrito

## 1. Formulario y componentes

Ruta `/distritos/nuevo`; React Hook Form, Zod y campos Mantine, EncabezadoPagina y notificación compartida. Reutiliza [sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [componentes React](../../disenio/componentes-react.md) [cite: 1].

## 2. Interacción y estados

- CUI-01: Nombre, provincia, departamento y ubigeo textual; validar campos obligatorios y geografía antes de enviar.
- CUI-02: Errores de API por campo y mensaje general; conservar valores ante fallos. Guardando deshabilita acciones duplicadas.
- CUI-03: Éxito vuelve al catálogo actualizado; cancelar con cambios pide confirmación de descarte.
- CUI-04: Etiquetas asociadas, foco en primer error y navegación por teclado; ancho adaptado a móvil.

## 3. Verificación

Pruebas de formulario con API simulada y recorrido navegador real aislado; [evidence.md](./evidence.md). [cite: 1] [Spec](./spec.md) y fuentes de §1.
