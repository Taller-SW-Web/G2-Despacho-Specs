# Modelo de Datos: Módulo de Despacho (PostgreSQL / Supabase)

> [!NOTE]
> Este documento representa la plantilla y estructura base del modelo de datos relacional para el microservicio de Despacho. Los esquemas detallados de tablas, tipos de datos, restricciones de integridad, índices y extensiones se definirán y acordarán conjuntamente con el equipo de desarrollo.

---

## 1. Convenciones Generales de Persistencia

- **Motor de Base de Datos:** PostgreSQL (v15/v16) alojado en **Supabase**.
- **Nomenclatura:** Formato `snake_case` en minúsculas para nombres de tablas y columnas (ej. `id_despacho`, `fecha_creacion`, `peso_kg`).
- **Marcas Temporales:** Atributos de auditoría en UTC utilizando `TIMESTAMPTZ` (`creado_en`, `actualizado_en`).
- **Estados:** Restricciones de verificación (*CHECK constraints*) o tipos `ENUM` alineados con las especificaciones funcionales y consolidados posteriormente en [specs/overview.md](overview.md) (`PENDIENTE_ASIGNACION`, `ASIGNADO`, `EN_CAMINO`, `ENTREGADO`, `FALLIDO`, `DEVUELTO_A_ALMACEN`).

---

## 2. Diagrama Entidad-Relación (ERD)

*(Pendiente de modelado y consolidación con los 5 integrantes del equipo).*

---

## 3. Catálogo de Tablas Identificadas

### 3.1 Zonas y Tarifas (F-01: Valqui)
- **`zonas`**: *(En definición)*
- **`tarifas_zona`**: *(En definición)*

### 3.2 Despachos y Trazabilidad (F-02: Tarqui / capacidad transversal de seguimiento)
- **`despachos`**: *(En definición)*
- **`historial_estados_despacho`**: *(En definición)*

### 3.3 Evidencias e Incidencias en Ruta (F-03: Max / F-04: Gerardo)
- **`evidencias_entrega`**: *(En definición)*
- **`incidencias_entrega_fallida`**: *(En definición)*

### 3.4 Flota, Operadores y Vehículos (F-05: Rhamses)
- **`repartidores`**: *(En definición)*
- **`vehiculos`**: *(En definición)*
- **`turnos_operador`**: *(En definición)*

---

## 4. Puntos Clave a Definir en la Sesión de Equipo

1. **Estrategia de Claves Primarias:** Elección entre UUID v4 (`gen_random_uuid()`) o enteros de 64 bits autoincrementales (`BIGSERIAL`).
2. **Soporte Geoespacial:** Adopción de la extensión `PostGIS` (`GEOMETRY(Point, 4326)`) para coordenadas frente a columnas numéricas (`latitud NUMERIC`, `longitud NUMERIC`).
3. **Estrategia de Borrado:** Implementación de borrado lógico (*soft delete*) mediante columnas `activo BOOLEAN` o `eliminado_en TIMESTAMPTZ`.
4. **Almacenamiento de Evidencias:** Guardar URLs públicas/firmadas provenientes de Supabase Storage en lugar de contenido binario directo.
