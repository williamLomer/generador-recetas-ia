# Arquitectura del sistema

## Visión general

La aplicación organiza la lógica en una API FastAPI, una capa de persistencia SQLAlchemy y un servicio de generación conectado a OpenRouter. La interfaz web se entrega mediante plantillas y archivos estáticos.

## Componentes

- **Interfaz:** HTML, CSS y JavaScript en `app/templates/` y `app/static/`.
- **API:** routers FastAPI para autenticación, ingredientes y recetas.
- **Validación:** esquemas Pydantic en `app/schemas/`.
- **Persistencia:** modelos SQLAlchemy y PostgreSQL; SQLite se utiliza en las pruebas.
- **Seguridad:** tokens JWT y hash de contraseñas con PBKDF2-HMAC-SHA256.
- **Servicio IA:** `app/services/ai_service.py` construye la solicitud, invoca OpenRouter y valida el JSON recibido.
- **Despliegue local:** Docker Compose coordina la API y PostgreSQL.

## Organización del código

- `app/main.py`: crea la aplicación, registra routers y recursos web.
- `app/config.py`: carga configuración desde variables de entorno y `.env`.
- `app/database.py`: motor, sesiones y base declarativa.
- `app/models/`: entidades persistentes.
- `app/routers/`: endpoints HTTP.
- `app/schemas/`: validación de entrada y salida.
- `app/services/`: seguridad e integración con IA.
- `tests/`: suite de pruebas automatizadas.

## Flujo de generación

1. El usuario se autentica y recibe un token JWT.
2. Registra ingredientes en su inventario.
3. Solicita `POST /recipes/generate`.
4. La API consulta únicamente los ingredientes asociados al usuario autenticado.
5. El servicio construye un prompt y envía la petición a OpenRouter.
6. La respuesta JSON se valida antes de persistir los datos.
7. El usuario consulta el historial y puede calificar o eliminar sus recetas.

## Configuración y secretos

Las credenciales se cargan desde variables de entorno. El archivo local `.env` no debe versionarse; `.env.example` sirve como plantilla sin secretos reales.
