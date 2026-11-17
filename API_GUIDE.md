# Guía de uso de la API

La documentación interactiva está disponible en `/docs` cuando la aplicación se encuentra en ejecución.

## 1. Registrar una cuenta

`POST /auth/register`

Ejemplo de cuerpo:

```json
{
  "email": "usuario@ejemplo.com",
  "full_name": "Usuario de prueba",
  "password": "UnaClaveSegura123"
}
```

La respuesta contiene un token de acceso. Guarda el token de forma privada.

## 2. Iniciar sesión

`POST /auth/login`

```json
{
  "email": "usuario@ejemplo.com",
  "password": "UnaClaveSegura123"
}
```

En Swagger, pulsa **Authorize** e introduce el token como esquema Bearer cuando la interfaz lo solicite.

## 3. Añadir un ingrediente

`POST /ingredients/` (requiere JWT)

```json
{
  "name": "Tomate",
  "quantity": 3,
  "unit": "unidades"
}
```

Los campos corresponden al nombre, cantidad positiva y unidad del ingrediente.

## 4. Consultar inventario

`GET /ingredients/` (requiere JWT)

Devuelve los ingredientes asociados al usuario autenticado.

## 5. Generar una receta

`POST /recipes/generate` (requiere JWT)

No requiere cuerpo JSON. La API utiliza el inventario del usuario autenticado y solicita a OpenRouter una receta estructurada. Se necesita configurar `OPENROUTER_API_KEY` en el entorno de ejecución.

## 6. Consultar historial

`GET /recipes/` (requiere JWT)

Devuelve las recetas guardadas para el usuario autenticado.

## 7. Calificar una receta

`POST /recipes/{recipe_id}/rating` (requiere JWT)

```json
{
  "score": 5
}
```

El valor de `score` debe ser un entero entre 1 y 5.

## 8. Eliminar una receta

`DELETE /recipes/{recipe_id}` (requiere JWT)

El identificador debe corresponder a una receta del usuario autenticado.

## Códigos HTTP frecuentes

- `200`: operación correcta.
- `201`: recurso creado.
- `204`: recurso eliminado sin cuerpo de respuesta.
- `401`: falta autenticación o el token no es válido.
- `404`: recurso no encontrado para el usuario autenticado.
- `503`: servicio de generación no disponible, por ejemplo, por falta de configuración de OpenRouter.

Nunca compartas tokens JWT, contraseñas ni claves API en capturas o reportes.
