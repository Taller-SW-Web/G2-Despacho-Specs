# UI de ES-F01-11: Editar un distrito

## 1. Formulario y componentes

Ruta `/distritos/:id/editar`; comparte formulario de alta y los [componentes existentes](../../disenio/componentes-react.md) [cite: 1].

## 2. Interacción y estados

- CUI-01: Precargar detalle y versión; nombre/ubigeo de solo lectura si identidad protegida, explicando catálogo base o asociaciones.
- CUI-02: Errores por campo y valores conservados. Un conflicto de versión exige revisar datos actuales; nunca reenviar automáticamente sobre otra versión.
- CUI-03: Carga, inexistente, error y acceso denegado diferenciados; estado se consulta, no se edita aquí.
- CUI-04: Guardado/descarte explícitos, foco/teclado accesibles y adaptación móvil según el sistema de diseño.

## 3. Verificación

Pruebas de protección y conflicto con API simulada, luego navegador/Gateway aislado; [evidence.md](./evidence.md). [cite: 1] [Spec](./spec.md) y componentes de §1.
