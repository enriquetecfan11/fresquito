#!/bin/bash
# Ejecutar Fresquito en Ubuntu sin Docker.
# Requiere: Python 3.10+, pip. Opcional: venv.
# Uso: desde la raíz del repo: ./scripts/run-ubuntu.sh
#      o desde scripts/: ./run-ubuntu.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "Fresquito – ejecución en Ubuntu (desde $REPO_ROOT)"

if ! command -v python3 &>/dev/null; then
  echo "Error: python3 no encontrado. Instala Python 3.10 o superior."
  exit 1
fi

# Opcional: usar venv si existe
if [ -d "venv" ]; then
  echo "Activando venv..."
  # shellcheck source=/dev/null
  source venv/bin/activate
elif [ -d ".venv" ]; then
  echo "Activando .venv..."
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

echo "Instalando dependencias..."
pip install -e . -q

if [ ! -f "data/input/town_index.csv" ]; then
  echo "Aviso: data/input/town_index.csv no existe. Algunos endpoints pueden fallar hasta que ejecutes el pipeline."
fi

echo "Iniciando API en http://0.0.0.0:5000"
exec fresquito
