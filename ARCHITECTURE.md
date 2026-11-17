# Arquitectura del sistema

## 1. Descripción general

Generador de Recetas con IA es una aplicación web basada en FastAPI que permite administrar ingredientes y generar recetas mediante OpenRouter.

## 2. Componentes principales

- **Frontend:** HTML, CSS y JavaScript.
- **API REST:** FastAPI.
- **Autenticación:** JWT y protección de contraseñas.
- **Persistencia:** SQLAlchemy y PostgreSQL.
- **Inteligencia artificial:** integración con OpenRouter.
- **Contenedores:** Docker y Docker Compose.

## 3. Organización del código

- `app/main.py`: punto de entrada de la aplicación.
- `app/config.py`: configuración y variables de entorno.
- `app/database.py`: conexión con la base de datos.
- `app/models/`: modelos de datos.
- `app/routers/`: endpoints de autenticación, ingredientes y recetas.
- `app/schemas/`: esquemas de validación.
- `app/services/`: lógica de seguridad e integración con IA.
- `app/static/`: recursos estáticos.
- `app/templates/`: interfaz web.
- `tests/`: pruebas automatizadas.

## 4. Flujo de generación de recetas

1. El usuario inicia sesión.
2. Registra ingredientes en su inventario.
3. Solicita generar una receta.
4. La API consulta los ingredientes disponibles.
5. El servicio de IA solicita una receta a OpenRouter.
6. La respuesta se valida y se almacena.
7. El usuario puede consultar el historial y calificar recetas.

## 5. Infraestructura

Docker Compose coordina la aplicación y PostgreSQL. Las variables sensibles se administran mediante `.env`, excluido del repositorio.
