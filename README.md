# Generador de Recetas con IA

Aplicación web académica desarrollada con Python, FastAPI, SQLAlchemy, PostgreSQL y OpenRouter. Permite crear una cuenta, administrar un inventario personal, generar recetas estructuradas a partir de los ingredientes disponibles y gestionar el historial y sus calificaciones.

## Funcionalidades

- Registro e inicio de sesión con tokens JWT.
- Contraseñas protegidas mediante PBKDF2-HMAC-SHA256 con salt individual.
- CRUD de ingredientes con aislamiento por usuario.
- Generación de recetas mediante OpenRouter con respuesta JSON validada.
- Persistencia de recetas, ingredientes y calificaciones.
- Historial, calificación de 1 a 5 estrellas y eliminación de recetas.
- Interfaz web adaptable y favicon SVG.
- Documentación OpenAPI/Swagger en `/docs`.

## Arquitectura

El navegador consume la API REST de FastAPI. Los routers gestionan autenticación, inventario e historial; SQLAlchemy conecta con PostgreSQL. El servicio `app/services/ai_service.py` construye el prompt, llama a OpenRouter y valida la estructura JSON antes de almacenar la receta.

La arquitectura y organización del código se describen en [ARCHITECTURE.md](ARCHITECTURE.md).

## Modelo de datos

- `users`: cuentas y credenciales protegidas.
- `ingredients`: inventario asociado a un usuario.
- `recipes`: recetas generadas asociadas a un usuario.
- `ratings`: calificaciones asociadas a receta y usuario.

## Requisitos

- Python 3.11 o superior.
- Docker Engine y Docker Compose (para ejecución contenerizada).
- Una clave de API de OpenRouter para generar recetas con IA.

## Ejecución local

Crear y activar el entorno virtual, instalar dependencias y preparar la configuración:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` y define `SECRET_KEY` y `OPENROUTER_API_KEY`. Para ejecución local sin PostgreSQL puedes cambiar `DATABASE_URL` a `sqlite:///./recetas.db`.

Iniciar la API:

```powershell
uvicorn app.main:app --reload
```

Por defecto, Uvicorn estará disponible en `http://127.0.0.1:8000`. La documentación Swagger estará en `http://127.0.0.1:8000/docs`.

## Ejecución con Docker Compose

Copia `.env.example` a `.env`, configura una `POSTGRES_PASSWORD` segura, una `SECRET_KEY` aleatoria de al menos 32 caracteres y `OPENROUTER_API_KEY`.

```powershell
docker compose up --build -d
docker compose logs -f app
```

La configuración actual publica el puerto interno 8000 del contenedor en el puerto **8001** del equipo local. Por tanto, la API estará en `http://localhost:8001` y Swagger en `http://localhost:8001/docs`. PostgreSQL conserva sus datos en el volumen `postgres_data`.

## Pruebas

Las pruebas utilizan una base SQLite temporal y no requieren llamar realmente a OpenRouter. Ejecutarlas localmente:

```powershell
pytest -v
```

O dentro del contenedor:

```powershell
docker compose exec app pytest -v
```

La suite cubre estado de la API, hash de contraseñas, JWT, construcción del prompt, validación JSON, registro e inicio de sesión y operaciones del inventario. En la validación manual realizada durante el desarrollo se obtuvieron **9 pruebas aprobadas**. El flujo de integración continua también ejecuta esta suite en cada push y pull request.

## Variables de entorno

| Variable | Descripción |
|---|---|
| `APP_NAME` | Nombre de la aplicación |
| `DATABASE_URL` | Cadena de conexión a la base de datos |
| `SECRET_KEY` | Secreto para firmar JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token en minutos |
| `OPENROUTER_API_KEY` | Clave privada del proveedor LLM |
| `OPENROUTER_MODEL` | Identificador del modelo |
| `OPENROUTER_SITE_URL` | URL enviada en la cabecera HTTP-Referer |
| `OPENROUTER_APP_NAME` | Nombre enviado al proveedor |
| `POSTGRES_DB` | Nombre de la base de datos PostgreSQL |
| `POSTGRES_USER` | Usuario de PostgreSQL |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL |

## Endpoints principales

| Método | Ruta | Descripción | Autenticación |
|---|---|---|---|
| GET | `/health` | Verificar estado de la API | No |
| POST | `/auth/register` | Registrar usuario | No |
| POST | `/auth/login` | Iniciar sesión | No |
| GET | `/ingredients/` | Listar ingredientes del usuario | JWT |
| POST | `/ingredients/` | Crear ingrediente | JWT |
| GET | `/ingredients/{ingredient_id}` | Consultar ingrediente | JWT |
| PUT | `/ingredients/{ingredient_id}` | Actualizar ingrediente | JWT |
| DELETE | `/ingredients/{ingredient_id}` | Eliminar ingrediente | JWT |
| POST | `/recipes/generate` | Generar receta con IA | JWT |
| GET | `/recipes/` | Consultar historial | JWT |
| POST | `/recipes/{recipe_id}/rating` | Calificar receta | JWT |
| DELETE | `/recipes/{recipe_id}` | Eliminar receta | JWT |

Para probar la API, inicia la aplicación y visita `/docs`.

## Seguridad y publicación

- No subir `.env`, claves API, contraseñas reales ni secretos al repositorio.
- `.env.example` contiene solo nombres y valores de ejemplo.
- Revocar y regenerar cualquier clave que haya sido compartida accidentalmente.
- Revisar [SECURITY.md](SECURITY.md) para las pautas de reporte y manejo de vulnerabilidades.

## Despliegue en VPS

El despliegue público aún requiere infraestructura externa y no se declara realizado:

1. Crear un VPS Linux e instalar Docker Engine y Docker Compose.
2. Apuntar el registro DNS A del dominio a la IP del VPS.
3. Clonar el repositorio y crear un archivo `.env` con secretos fuertes.
4. Ejecutar `docker compose up --build -d`.
5. Configurar Caddy o Nginx como proxy inverso y emitir un certificado TLS válido, por ejemplo, con Let's Encrypt.
6. Verificar HTTPS, `/health`, `/docs` y los flujos principales.

El VPS, dominio y sus credenciales deben ser proporcionados por el responsable del proyecto.


## Despliegue de demostración en Render

Se incluye `render.yaml` para crear un servicio Docker en Render. Para conservar datos sin depender del disco efímero del servicio, se utiliza PostgreSQL administrado en Neon. Consulta [DEPLOY_RENDER.md](DEPLOY_RENDER.md) para la configuración paso a paso y los límites del plan gratuito. Esta alternativa no sustituye un VPS propio si la evaluación lo exige expresamente.
