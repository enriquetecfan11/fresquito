**cronfile** : Este archivo contiene las configuraciones para el cron. Aquí se programará la ejecución periódica de `main.py`.

0 * * * * root python3 /app/main.py

Ejecutar esto para correr el contedor

Construir la imagen Docker
docker build -t mi-fresquito .

Ejecutar el contenedor
docker run -d --name mi-contenedor mi-aplicacion

Para exponer el puerto 80

docker run -d --name fresquito -p 80:80 fresquito

Sin detach

docker run -p 8080:80 --name fresquito fresquito
