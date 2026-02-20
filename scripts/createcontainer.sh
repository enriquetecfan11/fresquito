#!/bin/bash
# Construir la imagen Docker de Fresquito.
# Uso: ./scripts/createcontainer.sh (desde la raíz) o ./createcontainer.sh (desde scripts/)

set -e
# Ir siempre a la raíz del repo (donde está el Dockerfile)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

if [ ! -f "Dockerfile" ]; then
  echo "Error: no se encuentra Dockerfile en $REPO_ROOT"
  exit 1
fi

echo "Construyendo imagen Docker (fresquito) desde $REPO_ROOT"
docker build -t fresquito .
echo "Imagen fresquito creada correctamente."
