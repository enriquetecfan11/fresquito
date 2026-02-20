#!/bin/bash

echo "Run container"

# Flask escucha en 5000 dentro del contenedor; mapeamos al host (ej. 8081:5000 o 80:5000)
# Uso: ./startcontainer.sh [puerto_host]
# Por defecto: puerto 5000 en host. Para exponer en 80: ./startcontainer.sh 80
PORT="${1:-5000}"
docker run -d -p "${PORT}:5000" --name fresquito fresquito
echo "Contenedor fresquito iniciado. API en http://localhost:${PORT}"
