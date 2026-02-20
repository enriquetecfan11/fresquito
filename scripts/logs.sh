#!/bin/bash

echo "Logs del contenedor fresquito a .txt"
# Uso: ./logs.sh [nombre_contenedor]
# Por defecto usa el contenedor 'fresquito'
CONTAINER="${1:-fresquito}"
docker logs "$CONTAINER" > containerlogs.txt
echo "Logs guardados en containerlogs.txt"
