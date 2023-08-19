#!/bin/bash

# Construir la imagen Docker
docker build -t fresquito .

# Iniciar el contenedor
docker run -d --name fresquito -p 80:80 fresquito
