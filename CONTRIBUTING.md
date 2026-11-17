# Guía de contribución

## Requisitos

- Python 3.11 o superior.
- Git.
- Docker Engine y Docker Compose para probar el despliegue local.

## Flujo recomendado

1. Crear una rama para el cambio.
2. Implementar una modificación pequeña y enfocada.
3. Ejecutar `pytest -v`.
4. Revisar `git diff` y comprobar que no se incluyan secretos ni archivos locales.
5. Crear un commit con un mensaje descriptivo.
6. Abrir un pull request explicando el cambio y las pruebas ejecutadas.

## Convención de commits

- `feat:` nueva funcionalidad.
- `fix:` corrección.
- `docs:` documentación.
- `test:` pruebas.
- `refactor:` reorganización sin cambio funcional.

## Seguridad

Nunca incluir `.env`, claves API, tokens JWT ni contraseñas reales en commits o pull requests.
