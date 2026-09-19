# Especificación SPEC-F03-PROC-02: Gestión de Storage Privado y Emisión de URLs Firmadas

**Tipo:** Proceso Interno de Backend / Servicio de Almacenamiento  
**Macro-funcionalidad:** F-03: Web Responsive del Repartidor y Evidencia de Entrega  
**Responsable:** *Por definir*  
**Estado:** Especificado  
**Actor principal:** Repartidor / Gestor de Despacho  

---

## 1. Contexto

Las fotografías tomadas como evidencia de entrega o de intento fallido contienen información sensible sobre predios particulares y destinatarios. Para proteger la privacidad y cumplir con las normativas de seguridad informática, las imágenes no deben almacenarse en carpetas públicas ni exponerse mediante URLs estáticas y accesibles sin control.

---

## 2. Propósito

Implementar el servicio de backend para la carga de evidencias fotográficas en un bucket de objetos privado (Supabase Storage / AWS S3), validar la integridad y tipo del archivo, persistir únicamente la ruta/clave del objeto en base de datos y emitir bajo demanda URLs presignadas temporales (con vigencia de 5 minutos) exclusivamente para usuarios autorizados.

---

## 3. Alcance

Esta especificación cubre exclusivamente:
- Validación técnica del archivo binario recibido:
  - Tipos MIME permitidos: `image/jpeg`, `image/png`.
  - Tamaño máximo permitido: 2 MB (2,097,152 bytes).
  - Verificación de magic numbers en el encabezado del stream para prevenir spoofing de extensiones.
- Carga del archivo en el bucket privado con nomenclatura estructurada: `evidencias/{yyyy}/{MM}/{idDespacho}_{uuid}.jpg`.
- Persistencia exclusiva de la clave o ruta del objeto (`clave_evidencia`) en la tabla `despachos`.
- Exposición del endpoint `GET /api/v1/despachos/{idDespacho}/evidencia`.
- Verificación de autorización RBAC: solo el repartidor propietario que tomó la foto o un usuario con rol `GESTOR_DESPACHO` o `ADMIN` pueden solicitar el enlace.
- Generación de URL firmada temporal con expiración estricta de 300 segundos (5 minutos).

---

## 4. Precondiciones, dependencias y resultados

### 4.1. Precondiciones
- Bucket de almacenamiento configurado con políticas de acceso privado (bloqueo total de lectura pública).
- Credenciales de servicio del proveedor de almacenamiento configuradas en el backend.

### 4.2. Dependencias
| Componente / Servicio | Responsabilidad |
|---|---|
| Supabase Storage / S3 SDK | Cliente para subir objetos y firmar URLs temporales. |
| Seguridad y Usuarios | Autenticación y roles para controlar el acceso a la evidencia. |
| `SPEC-F04-FORM-01` | Vista de incidencias en F-04 que consumirá este servicio para mostrar la foto al gestor. |

### 4.3. Resultados
- Fotografía resguardada de forma segura en almacenamiento en la nube privado.
- Enlace temporal generado en tiempo de ejecución que expira automáticamente tras 5 minutos.

---

## 5. Requisitos y criterios de aceptación automatizables

### RF-01. Validación y subida de archivos
El servicio DEBE rechazar archivos maliciosos o con sobretamaño.

#### CA-01. Subida exitosa de archivo válido
- **DADO** un archivo JPEG de 800 KB con contenido binario legítimo.
- **CUANDO** se envía al servicio de almacenamiento.
- **ENTONCES** se carga en el bucket privado y se retorna la clave `evidencias/2026/09/DSP-100234_abc123.jpg`.

#### CA-02. Rechazo por tipo no permitido o sobretamaño
- **DADO** un archivo con extensión `.jpg` pero cuyo contenido real es un ejecutable (`application/x-msdownload`) o un archivo de 3 MB.
- **CUANDO** se intenta procesar.
- **ENTONCES** el sistema rechaza la solicitud con código `400 Bad Request` sin persistir nada en el bucket.

### RF-02. Emisión segura de URLs firmadas
El servicio DEBE emitir enlaces con expiración únicamente a usuarios autorizados.

#### CA-03. Emisión de URL firmada autorizada
- **DADO** un despacho con evidencia y un usuario autenticado con rol `GESTOR_DESPACHO`.
- **CUANDO** invoca `GET /api/v1/despachos/{idDespacho}/evidencia`.
- **ENTONCES** el backend responde `200 OK` con un JSON conteniendo una URL con token de firma temporal y expiración de 300 segundos.

#### CA-04. Denegación de acceso a terceros
- **DADO** un usuario autenticado con rol `REPARTIDOR` que intenta solicitar la evidencia de un despacho asignado a otro chofer.
- **CUANDO** invoca el endpoint.
- **ENTONCES** el backend responde `403 Forbidden` y no genera la URL firmada.

#### CA-05. Enlace vencido inaccesible
- **DADO** una URL firmada generada hace más de 5 minutos.
- **CUANDO** se intenta acceder a ella desde un navegador.
- **ENTONCES** el servidor de almacenamiento deniega el acceso con código `403 Access Denied`.

---

## 6. Frontend

*N/A - Proceso de backend.* Consumido por la visualización de evidencia en F-03 y F-04.

---

## 7. Backend

### 7.1. Servicio de almacenamiento (Java 21 / Spring Boot)
```java
@Service
public class AlmacenamientoEvidenciaService {

    private final StorageClient storageClient; // Supabase / S3
    private final DespachoRepository despachoRepository;

    public String guardarEvidencia(UUID idDespacho, MultipartFile archivo) {
        validarArchivo(archivo);
        String clave = String.format("evidencias/%s/%s_%s.jpg", 
            LocalDate.now().getYear(), idDespacho, UUID.randomUUID());
        storageClient.subirObjeto(clave, archivo.getBytes(), archivo.getContentType());
        return clave;
    }

    public String generarUrlFirmada(UUID idDespacho, String usuarioAutenticado, boolean esGestor) {
        Despacho despacho = despachoRepository.findById(idDespacho)
            .orElseThrow(() -> new RecursoNoEncontradoException("Despacho no encontrado"));
        
        if (!esGestor && !despacho.getIdRepartidor().equals(usuarioAutenticado)) {
            throw new AccesoDenegadoException("No tiene permisos para ver la evidencia de este despacho");
        }

        return storageClient.crearUrlFirmada(despacho.getClaveEvidencia(), Duration.ofMinutes(5));
    }
}
```

---

## 8. Requisitos no funcionales

- **Seguridad:** Los buckets de almacenamiento jamás deben tener permisos de lectura anónima (`public: false`).
- **Rendimiento:** Generación de URL firmada en menos de 20 ms (cálculo de firma HMAC local sin llamadas de red obligatorias).
- **Trazabilidad:** Toda emisión de URL firmada se registra en logs de auditoría para fines de cumplimiento.

---

## 9. Fuera de alcance

- Reconocimiento óptico de caracteres (OCR) sobre los paquetes.
- Reconocimiento facial del destinatario (prohibido por políticas de privacidad).

---

## 10. Estrategia de verificación

| Criterio | Tipo de Prueba | Herramienta | Evidencia esperada |
|---|---|---|---|
| CA-01 | Storage Test | LocalStack / Mock S3 | Archivo persistido con clave única en bucket privado. |
| CA-02 | File Validation Test | JUnit 5 | Archivo binario no imagen genera `BadFileException`. |
| CA-03 | Presigned URL Test | MockMvc | Retorno `200 OK` con URL que contiene parámetros de firma (`X-Amz-Signature` o similar). |
| CA-04 | Authorization Test | MockMvc | Chofer no propietario recibe `403 Forbidden`. |

---

## 11. Criterio de completitud

Esta especificación se considerará cumplida cuando:
1. Las fotografías se almacenen exclusivamente en almacenamiento privado.
2. Las URLs de acceso expiren en 5 minutos y estén protegidas por permisos RBAC.
3. Se verifiquen todas las pruebas de seguridad y subida de archivos.
