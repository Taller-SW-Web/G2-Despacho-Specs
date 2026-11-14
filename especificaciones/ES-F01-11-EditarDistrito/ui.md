# UI de ES-F01-11: Editar un distrito

## 1. Formulario y componentes

Ruta `/distritos/:id/editar`; misma pantalla unificada, con el distrito seleccionado en el formulario izquierdo y el listado visible. Comparte formulario de alta y los [componentes existentes](../../disenio/componentes-react.md) [cite: 1].

## 2. Interacción y estados

- CUI-01: Precargar detalle y versión; nombre/ubigeo de solo lectura si identidad protegida, explicando catálogo base o asociaciones.
- CUI-02: Errores por campo y valores conservados. Un conflicto de versión exige revisar datos actuales; nunca reenviar automáticamente sobre otra versión.
- CUI-03: Carga, inexistente, error y acceso denegado diferenciados; estado se consulta, no se edita aquí.
- CUI-04: Guardado/descarte explícitos, foco/teclado accesibles y adaptación móvil según el sistema de diseño.
- CUI-05: **Editar** consulta el detalle vigente y su versión, identifica la fila y desplaza/lleva el foco al formulario. **Guardar cambios** y **Cancelar edición** vuelven al modo alta; cambiar de selección o cancelar un borrador modificado exige descarte explícito.
- CUI-06: Un conflicto conserva lo escrito; **Revisar datos actuales** exige descartar expresamente antes de consultar otra versión. Actualizar el listado no reemplaza el detalle. Respuestas de selecciones anteriores se ignoran y no se reenvían decisiones automáticamente.

## 3. Verificación

Pruebas de protección y conflicto con API simulada, luego navegador/Gateway aislado; [evidence.md](./evidence.md). [cite: 1] [Spec](./spec.md) y componentes de §1.
