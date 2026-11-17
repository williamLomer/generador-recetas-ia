# Generador de Recetas con IA

Aplicación web académica desarrollada con Python, FastAPI, SQLAlchemy, PostgreSQL y OpenRouter. Permite crear una cuenta, administrar un inventario personal, generar recetas estructuradas a partir de los ingredientes disponibles y gestionar el historial y sus calificaciones.

## Funcionalidades
- Registro e inicio de sesión con tokens JWT.
- Contraseñas almacenadas mediante PBKDF2-HMAC-SHA256 con salt individual.
- CRUD de ingredientes con aislamiento por usuario.
- Generación de recetas por OpenRouter con respuesta JSON validada.
- Persistencia de recetas, ingredientes y calificaciones.
- Historial, calificación de 1 a 5 estrellas y eliminación de recetas.
- Interfaz web adaptable y favicon SVG.
- Documentación OpenAPI/Swagger en `/docs`.

## Arquitectura
El navegador consume la API REST de FastAPI. Los routers delegan autenticación, persistencia y generación de recetas a servicios internos. SQLAlchemy conecta con PostgreSQL. `ai_service.py` construye el prompt, llama a OpenRouter y valida la estructura JSON antes de almacenar la receta.

## Modelo de datos
- `users`: cuentas y credenciales protegidas.
- `ingredients`: inventario asociado a un usuario.
- `recipes`: recetas generadas asociadas a un usuario.
- `ratings`: calificaciones asociadas a receta y usuario; una calificación por usuario/receta.

## Ejecución local
Requiere Python 3.11+.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edita `.env` y define `SECRET_KEY`, `OPENROUTER_API_KEY` y, si lo deseas, `OPENROUTER_MODEL`. Para ejecución local sin PostgreSQL puedes cambiar `DATABASE_URL=sqlite:///./recetas.db`.

```powershell
uvicorn app.main:app --reload
```
Abre `http://127.0.0.1:8001` o la documentación `http://127.0.0.1:8001/docs`.

## Ejecución con Docker Compose
Copia `.env.example` a `.env`, añade `POSTGRES_PASSWORD` y una clave `SECRET_KEY` aleatoria de al menos 32 caracteres. Configura `OPENROUTER_API_KEY`.

```bash
docker compose up --build -d
docker compose logs -f app
```
La API estará en el puerto 8000. Los datos de PostgreSQL se conservan en el volumen `postgres_data`.

## Pruebas
```bash
pytest
```
La suite contiene pruebas de salud, seguridad de contraseñas, JWT, construcción del prompt, parseo de JSON, autenticación y operaciones del inventario. La generación real de OpenRouter requiere una clave y no se invoca en las pruebas unitarias.

## Variables de entorno
| Variable | Descripción |
|---|---|
| `APP_NAME` | Nombre de la aplicación |
| `DATABASE_URL` | Cadena de conexión a base de datos |
| `SECRET_KEY` | Secreto para firmar JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token |
| `OPENROUTER_API_KEY` | Clave privada del proveedor LLM |
| `OPENROUTER_MODEL` | Identificador del modelo |
| `OPENROUTER_SITE_URL` | URL para cabecera HTTP-Referer |
| `OPENROUTER_APP_NAME` | Nombre enviado al proveedor |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Credenciales del contenedor PostgreSQL |

## Despliegue en VPS (pendiente de infraestructura)
1. Crear un VPS Linux e instalar Docker Engine y Docker Compose.
2. Apuntar el registro DNS A del dominio a la IP del VPS.
3. Clonar el repositorio, crear `.env` en el servidor y configurar secretos fuertes.
4. Ejecutar `docker compose up --build -d`.
5. Configurar Caddy o Nginx como proxy inverso y emitir certificado TLS válido (por ejemplo, Let's Encrypt con Caddy).
6. Verificar HTTPS, `/health`, `/docs` y los flujos de usuario.

El despliegue requiere dominio, VPS y credenciales que pertenecen al estudiante. No se declara desplegado hasta realizar y comprobar estos pasos.

## Seguridad y publicación
No subir `.env`, claves API, contraseñas reales ni secretos al repositorio. `.env.example` contiene únicamente nombres y valores de ejemplo. Revocar y regenerar cualquier clave que haya sido compartida accidentalmente.


## Endpoints principales

| Método | Ruta | Descripción | Autenticación |
|---|---|---|---|
| GET | `/health` | Verificar estado de la API | No |
| POST | `/auth/register` | Registrar usuario | No |
| POST | `/auth/login` | Iniciar sesión | No |
| GET | `/ingredients/` | Listar ingredientes | JWT |
| POST | `/ingredients/` | Crear ingrediente | JWT |
| GET | `/ingredients/{ingredient_id}` | Consultar ingrediente | JWT |
| PUT | `/ingredients/{ingredient_id}` | Actualizar ingrediente | JWT |
| DELETE | `/ingredients/{ingredient_id}` | Eliminar ingrediente | JWT |
| POST | `/recipes/generate` | Generar receta con IA | JWT |
| GET | `/recipes/` | Consultar historial | JWT |
| POST | `/recipes/{recipe_id}/rating` | Calificar receta | JWT |
| DELETE | `/recipes/{recipe_id}` | Eliminar receta | JWT |

Para probar los endpoints, iniciar la aplicación y visitar `/docs`.