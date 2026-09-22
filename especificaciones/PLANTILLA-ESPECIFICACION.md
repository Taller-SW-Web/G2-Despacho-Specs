# ES-FXX-XX: Nombre breve del caso de uso

> Copiar este archivo en la misma carpeta `especificaciones/`, reemplazar los datos de ejemplo y eliminar esta indicación. Cada archivo debe describir un solo comportamiento concreto, implementable y verificable.

**Funcionalidad padre:** F-XX — Nombre de la funcionalidad  
**Responsable:** Nombre del integrante  
**Estado:** Borrador / En revisión / Aprobada  
**Actor principal:** Rol que inicia el caso de uso

## 1. Objetivo

Describir en uno o dos párrafos el resultado concreto que debe conseguir esta especificación y el valor que aporta.

## 2. Actor y precondiciones

- Actor que ejecuta la acción.
- Permisos o rol requerido.
- Estado previo necesario.
- Datos o dependencias que deben existir.

## 3. Flujo principal

1. El actor inicia la acción.
2. El sistema recibe y valida la solicitud.
3. El sistema ejecuta la regla principal.
4. El sistema registra y devuelve el resultado.

## 4. Reglas y validaciones

- Regla de negocio principal.
- Estados desde los que se permite la operación.
- Restricciones y validaciones.
- Tratamiento de conflictos, duplicados o reintentos cuando corresponda.

## 5. Entradas, salidas e integraciones

### Entradas

- Datos necesarios para ejecutar el caso de uso.

### Salidas

- Resultado esperado y cambios producidos.

### Integraciones

- Funcionalidades o módulos que proporcionan o consumen información.
- Referenciar `integraciones/api-contract.md` cuando exista comunicación mediante API o eventos; no duplicar aquí el contrato completo.

## 6. Criterios de aceptación

### CA-01. Escenario principal

- **DADO** el contexto y las precondiciones.
- **CUANDO** el actor ejecuta la acción.
- **ENTONCES** el sistema produce el resultado esperado.

### CA-02. Validación o escenario alternativo

- **DADO** una condición inválida o alternativa.
- **CUANDO** se intenta ejecutar la acción.
- **ENTONCES** el sistema rechaza o procesa el caso de forma controlada.

## 7. Fuera de alcance y referencias

### Fuera de alcance

- Comportamientos relacionados que esta especificación no resuelve.

### Referencias

- Especificación de la funcionalidad padre en `funcionalidades/`.
- Contrato aplicable en `integraciones/api-contract.md`.
- Diseño o flujo de interfaz relacionado, cuando corresponda.
