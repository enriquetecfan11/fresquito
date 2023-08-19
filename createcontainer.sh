#!/bin/bash

echo "Create Container in docker"
# Construir la imagen Docker
docker build -t fresquito .

echo "Run container"
# Iniciar el contenedor
docker run -d --name fresquito -p 80:80 fresquito
