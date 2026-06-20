#!/bin/sh
set -e

echo "🚀 Inicializando ZeroVault Backend..."

# Esperar a que la BD esté lista
echo "⏳ Esperando a que PostgreSQL esté disponible..."
while ! nc -z ${DATABASE_URL#*@} 2>/dev/null; do
  sleep 1
done
echo "✅ PostgreSQL está disponible"

# Inicializar BD
echo "🗄️  Inicializando base de datos..."
python -m app.init_db

# Iniciar aplicación
echo "🔥 Iniciando servidor FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
