#!/bin/bash
# Construir la imagen Docker de Fresquito.
# Uso: desde la raíz del repo ./scripts/createcontainer.sh
#      o desde scripts/ ./createcontainer.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "Construyendo imagen Docker (fresquito) desde $REPO_ROOT"
docker build -t fresquito .
echo "Imagen fresquito creada correctamente."
