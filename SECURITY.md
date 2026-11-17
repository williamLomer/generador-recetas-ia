# Política de seguridad

## Manejo de credenciales

- No publicar archivos `.env`, tokens JWT, claves API ni contraseñas.
- Usar secretos aleatorios y exclusivos para cada entorno.
- Si una credencial se expone, revocarla y generar una nueva inmediatamente.
- Mantener las dependencias actualizadas.

## Datos y autenticación

- Los endpoints privados requieren autenticación JWT.
- Las consultas de ingredientes y recetas deben limitarse al usuario autenticado.
- Las contraseñas se almacenan como hashes con salt individual.

## Reporte

Para reportar una vulnerabilidad, contacta al mantenedor del repositorio de manera privada. Evita incluir datos personales, tokens o secretos en issues públicos.

## Alcance

Proyecto académico. No se declara auditado, certificado ni endurecido para operar en producción.
