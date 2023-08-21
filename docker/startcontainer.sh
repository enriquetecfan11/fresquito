#!/bin/bash

echo "Run container"

# Iniciar el contenedor
docker run -d -p 8081:80 --name fresquito fresquito