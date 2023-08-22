# Ejecutar esto para correr el contedor

Construir la imagen Docker
docker build -t fresquito .

Ejecutar el contenedor
docker run -d --name mi-contenedor mi-aplicacion

Para exponer el puerto 80

docker run -d --name fresquito -p 80:80 fresquito

Sin detach

docker run -p 9090:9090--name fresquito fresquito
