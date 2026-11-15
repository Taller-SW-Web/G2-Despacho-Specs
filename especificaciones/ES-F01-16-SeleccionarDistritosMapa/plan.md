# Plan de ES-F01-16

## 1. Solución

Reutilizar FormularioZona/React Hook Form como única fuente de selección. Componente cartográfico diferido recibe distritos/selección y callback; preservar entradas existentes con códigos/indicador postal. Capas con asociaciones permiten indicar conflictos, pero el backend sigue siendo autoridad al guardar. Leer [spec](./spec.md) y [UI](./ui.md).

## 2. Verificación

Componentes con API simulada para sincronización, conservación y recuperación; backend conserva regresiones de zonas. Navegador con Gateway/Gestión aislados para selección real, formulario y móvil. Suites frontend, typecheck/build y recorrido registrado en [evidencia](./evidence.md).
