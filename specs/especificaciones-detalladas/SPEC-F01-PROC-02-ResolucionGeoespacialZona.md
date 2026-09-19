# Especificación SPEC-F01-PROC-02: Servicio PostGIS de Resolución de Cobertura y Zona

**Tipo:** Proceso Interno de Backend / Servicio Geoespacial  
**Macro-funcionalidad:** F-01: Gestión de Zonas Geográficas y Cotizador de Envíos  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Servicios Internos del Módulo (F-01, F-02, F-05)  

---

## 1. Contexto

Para que el módulo opere de forma consistente, debe existir una única fuente de verdad sobre qué zona geográfica corresponde a una dirección de entrega. Tanto el motor de cotización (F-01) al cotizar un paquete, como la recepción de pedidos (F-02) al asignar la zona a un despacho, y la gestión de flota (F-05) al definir la zona de un chofer, dependen de este servicio geoespacial interno.

---

## 2. Propósito

Implementar el servicio interno de backend que resuelve de forma determinista y en milisegundos la zona geográfica activa que cubre un destino, utilizando consultas espaciales en PostgreSQL con PostGIS (`ST_Contains`) sobre coordenadas de latitud/longitud o resolución por catálogo de distritos.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Servicio Java/Spring `ResolucionZonaService` accesible por inyección de dependencias interna o cliente REST de baja latencia.
- Resolución primaria por coordenadas geográficas (`latitud`, `longitud` en formato WGS 84 / SRID 4326) ejecutando funciones espaciales PostGIS sobre polígonos indexados (R-Tree / GiST).
- Resolución secundaria (fallback) por normalización de texto de distrito o código postal.
- Filtrado estricto por zonas en estado `ACTIVO`. Si una zona está `INACTIVO`, el servicio la ignora y retorna ausencia de cobertura para nuevas operaciones.
- Retorno de DTO inmutable con `idZona`, `nombreZona`, `tarifaVigente` o `Optional.empty()` si no existe cobertura.

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Extensión PostGIS habilitada en PostgreSQL (Supabase).
- Geometrías de zonas almacenadas con SRID 4326 y con índice GiST en la columna de geometría.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| PostgreSQL + PostGIS | Motor de base de datos con capacidades espaciales y operadores topológicos. |
| `ZonaRepository` | Repositorio Spring Data con consultas espaciales nativas. |

### 4.3. Resultados
- Identificador de zona resuelto con certeza matemática y geográfica.
- F-02 asocia la zona al despacho sin mantener una lógica de cobertura duplicada.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Resolución por coordenadas espaciales
El servicio DEBE verificar si un punto geográfico cae dentro de algún polígono activo.

#### CA-01. Punto ubicado dentro de una zona activa
- **DADO** unas coordenadas (-12.1215, -77.0298) ubicadas dentro del polígono de "Lima Moderna".
- **CUANDO** se solicita la resolución de zona.
- **ENTONCES** el servicio ejecuta `ST_Contains` y retorna la zona "Lima Moderna" con su identificador y estado `ACTIVO`.

#### CA-02. Punto ubicado fuera de toda zona o en zona inactiva
- **DADO** unas coordenadas en un área rural sin cobertura o en una zona desactivada.
- **CUANDO** se solicita la resolución.
- **ENTONCES** el servicio retorna `Optional.empty()`.

### RF-02. Resolución alternativa por distrito
El servicio DEBE resolver por texto de distrito cuando no se cuente con coordenadas exactas.

#### CA-03. Resolución exitosa por distrito
- **DADO** una solicitud con distrito "San Isidro" sin coordenadas.
- **CUANDO** se procesa la resolución.
- **ENTONCES** el sistema busca en la lista de distritos mapeados de zonas activas y retorna la zona correspondiente.

---

## 6. Frontend

*N/A - Componente interno de backend.*

---

## 7. Backend

### 7.1. Consulta nativa PostGIS en Spring Data JPA
```java
@Repository
public interface ZonaRepository extends JpaRepository<Zona, String> {

    @Query(value = """
        SELECT z.* FROM zonas z 
        WHERE z.estado = 'ACTIVO' 
          AND ST_Contains(z.geometria, ST_SetSRID(ST_Point(:longitud, :latitud), 4326))
        LIMIT 1
    """, nativeQuery = true)
    Optional<Zona> buscarZonaActivaPorCoordenadas(
        @Param("latitud") double latitud, 
        @Param("longitud") double longitud
    );

    @Query("""
        SELECT z FROM Zona z 
        JOIN z.distritos d 
        WHERE z.estado = 'ACTIVO' AND LOWER(d.nombre) = LOWER(:distrito)
    """)
    Optional<Zona> buscarZonaActivaPorDistrito(@Param("distrito") String distrito);
}
```

---

## 8. Requisitos no funcionales

- **Rendimiento Ultrarrápido:** Tiempo de ejecución de consulta espacial inferior a 25 ms gracias al índice GiST.
- **Concurrencia:** Consulta puramente de lectura (`readOnly = true`), altamente escalable ante ráfagas de consultas simultáneas.
- **Consistencia:** Fuente única de resolución de zona para todo el ecosistema del módulo.

---

## 9. Fuera de alcance

- Geocodificación inversa (convertir texto de dirección a coordenadas mediante Google Maps o Nominatim).
- Cálculo de distancias kilométricas por carretera (rutas en grafos viales).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Data Spatial Test | Testcontainers (PostGIS) | Punto dentro del polígono retorna la entidad `Zona`. |
| CA-02 | Boundary Test | JUnit 5 | Punto en el exterior retorna `Optional.empty()`. |
| CA-03 | Text Lookup Test | JUnit 5 | Distrito "San Isidro" mapea a la zona correcta. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Las consultas PostGIS operen con índice espacial GiST en Supabase/PostgreSQL.
2. Los servicios de F-01 y F-02 consuman este servicio como única autoridad de resolución.
3. Se superen las pruebas automatizadas con base de datos espacial.
