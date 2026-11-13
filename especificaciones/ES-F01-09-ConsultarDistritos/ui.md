# UI de ES-F01-09: Consultar distritos

## 1. Pantalla y componentes

Ruta `/distritos`, accesible desde ShellAdministrativo. Reutiliza EncabezadoPagina, campos Mantine, EstadoVista, badges y acciones existentes. Diseño conforme a [sistema de diseño](../../disenio/SYSTEM-DESIGN.md) y [componentes React](../../disenio/componentes-react.md) [cite: 1].

## 2. Interacción y estados

- CUI-01: Buscar por nombre y filtrar Activos/Inactivos/Todos; listado con nombre, provincia, departamento, ubigeo y estado.
- CUI-02: Mostrar carga, vacío, error con reintento y acceso denegado sin datos. Peticiones obsoletas no reemplazan resultados recientes.
- CUI-03: Crear, editar y cambiar estado desde acciones rotuladas; acciones adaptadas al estado vigente.
- CUI-04: Tabla desplazable en móvil, controles con etiquetas, teclado y foco visibles; estados expresados con texto.

## 3. Verificación

Componentes con API simulada y recorrido navegador con Gateway real; resultados en [evidence.md](./evidence.md). [cite: 1] [Spec](./spec.md) y fuentes de §1.
