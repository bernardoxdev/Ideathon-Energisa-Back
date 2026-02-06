set -e

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Ambiente virtual não encontrado (.venv)"
    echo "👉 Crie com: python3 -m venv .venv"
    exit 1
fi

source "$VENV_DIR/bin/activate"

export PYTHONPATH="$(pwd)"

echo "🚀 Iniciando Academic Flow API..."

python -m uvicorn backend.main:app \
    --reload \
    --host 127.0.0.1 \
    --port 8080