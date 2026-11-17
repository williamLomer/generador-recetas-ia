# Política de seguridad

## Reporte de vulnerabilidades

Si encuentras una vulnerabilidad en este proyecto académico, informa al responsable del repositorio mediante GitHub Issues, evitando publicar datos sensibles o credenciales.

## Protección de credenciales

- No publicar archivos `.env`.
- No incluir claves API ni contraseñas en el código.
- Utilizar secretos aleatorios y robustos para JWT.
- Mantener las dependencias actualizadas.
- Revocar inmediatamente cualquier credencial expuesta.

## Autenticación y datos

- Las contraseñas deben almacenarse mediante funciones de hash seguras.
- Los endpoints privados requieren autenticación JWT.
- Los datos de ingredientes y recetas deben respetar el aislamiento por usuario.

## Alcance

Este proyecto tiene fines académicos. No se considera auditado ni certificado para producción.
