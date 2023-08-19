#!/bin/bash

echo "Run container"

# Iniciar el contenedor
docker run -d --name fresquito -p 80:80 fresquito