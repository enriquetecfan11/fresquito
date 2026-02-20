#!/bin/bash
# Construir imagen Docker de Fresquito, arrancar el contenedor y exponer la API.
# Uso: ./scripts/build-and-run.sh [puerto]
#      Por defecto puerto 5000. Ejemplo para 80: ./scripts/build-and-run.sh 80

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

PORT="${1:-5000}"

echo "=== Fresquito: build y run ==="
echo ""

# 1. Construir imagen
if [ ! -f "Dockerfile" ]; then
  echo "Error: no se encuentra Dockerfile en $REPO_ROOT"
  exit 1
fi
echo "[1/3] Construyendo imagen..."
docker build -t fresquito .
echo ""

# 2. Parar y eliminar contenedor anterior si existe
echo "[2/3] Preparando contenedor..."
if docker ps -a -q -f name=^fresquito$ | grep -q .; then
  docker stop fresquito 2>/dev/null || true
  docker rm fresquito
fi
echo ""

# 3. Arrancar contenedor
echo "[3/3] Iniciando contenedor..."
docker run -d -p "${PORT}:5000" --name fresquito fresquito
echo ""
echo "Listo. API en http://localhost:${PORT}"
echo "  Ejemplo: curl http://localhost:${PORT}"
echo "  Logs:    ./scripts/logs.sh"
