#!/bin/bash

echo "Logs del contenedor fresquito a .txt"
# Construir la imagen Docker

container_id=$1
docker logs $container_id > containerlogs.txt
