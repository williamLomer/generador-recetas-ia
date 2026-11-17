# Guía de contribución

## Requisitos
- Python 3.11 o superior.
- Docker y Docker Compose.
- Git.

## Flujo de trabajo
1. Crear una rama para el cambio.
2. Implementar una mejora concreta.
3. Ejecutar las pruebas con `pytest -v`.
4. Verificar que no se incluyan secretos ni archivos `.env`.
5. Describir claramente los cambios realizados.

## Convención de commits
- feat: nueva funcionalidad.
- fix: corrección de errores.
- docs: documentación.
- test: pruebas automatizadas.
- refactor: reorganización del código.

## Validación
Antes de publicar cambios, ejecutar:

`docker compose exec app pytest -v`
