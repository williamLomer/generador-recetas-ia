# Despliegue gratuito en Render + Neon

Esta guía publica la aplicación como servicio web Docker en Render y utiliza Neon para PostgreSQL persistente. Es una alternativa económica para demostraciones académicas; **no equivale a contratar un VPS administrado por el estudiante**.

## Servicios y límites del plan gratuito

- Render Free: el servicio se suspende después de 15 minutos sin tráfico y puede tardar alrededor de un minuto en despertar. El sistema de archivos del servicio es efímero.
- Neon Free: PostgreSQL administrado con 1 GB de almacenamiento y 100 CU-horas mensuales por proyecto; el cómputo se suspende por inactividad.
- Render proporciona una URL `onrender.com` y TLS/HTTPS administrado. No se necesita comprar dominio para tener una URL pública HTTPS.

Consulta los límites actuales antes de usarlo más allá de una demostración.

## 1. Crear la base de datos en Neon

1. Crear una cuenta en https://neon.com/.
2. Crear un proyecto PostgreSQL.
3. Seleccionar una región cercana a la región de Render que usarás.
4. Copiar la cadena de conexión desde el panel de Neon.
5. Ajustar el esquema del driver para SQLAlchemy/psycopg: reemplazar el prefijo `postgresql://` por `postgresql+psycopg://`. Mantener los parámetros SSL suministrados por Neon (normalmente `?sslmode=require`).
6. No publicar ni enviar la cadena de conexión por chat.

## 2. Crear el servicio en Render

1. Crear una cuenta en https://render.com/.
2. Conectar la cuenta de GitHub y autorizar acceso al repositorio `williamLomer/generador-recetas-ia`.
3. En Render, seleccionar **New → Blueprint**.
4. Elegir el repositorio. Render detectará `render.yaml`.
5. Confirmar la creación del Web Service con plan **Free**.
6. Cuando solicite valores secretos, configurar:
   - `DATABASE_URL`: cadena de Neon ajustada a `postgresql+psycopg://`.
   - `OPENROUTER_API_KEY`: clave privada de OpenRouter.
   - `SECRET_KEY` se genera desde el Blueprint; no la reemplaces con una clave de desarrollo.
7. Esperar a que termine el despliegue y comprobar el endpoint `/health`.

## 3. Verificar

- Abrir la URL pública asignada por Render.
- Comprobar `/health` y `/docs`.
- Registrar un usuario de prueba.
- Crear ingredientes y generar una receta.
- Comprobar que el historial sigue allí tras reiniciar/despertar el servicio; los datos deben estar en Neon, no en el disco local.

## Notas

- El primer acceso después de 15 minutos de inactividad puede tardar aproximadamente un minuto.
- Mantener los consumos dentro de los límites gratuitos de Render y Neon.
- Render Free no ofrece un VPS con acceso SSH ni disco persistente. Si el requisito académico exige expresamente VPS propio, esta alternativa sirve para demostrar la aplicación en HTTPS, pero no sustituye ese requisito.
- No subir el archivo `.env` a GitHub.
