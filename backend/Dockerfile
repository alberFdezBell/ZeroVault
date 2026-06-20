# --- FASE 1: Compilación de Dependencias ---
FROM python:3.11-alpine AS builder

WORKDIR /app

# Instalar herramientas del sistema necesarias para compilar ciertas librerías C
RUN apk add --no-cache gcc musl-dev libffi-dev

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Copiar archivos de configuración de dependencias
COPY pyproject.toml poetry.lock ./

# Configurar Poetry para no crear entornos virtuales aislados (instalar directo en el sistema del builder)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# --- FASE 2: Imagen Final de Producción ---
FROM python:3.11-alpine AS runner

WORKDIR /app

# Crear un usuario del sistema sin privilegios para ejecutar la app
RUN addgroup -S vaultgroup && adduser -S vaultuser -G vaultgroup

# Copiar las librerías pre-compiladas e instaladas desde el builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el código fuente de la aplicación
COPY ./app ./app

# Cambiar la propiedad de los archivos al usuario seguro
RUN chown -R vaultuser:vaultgroup /app

# Cambiar al usuario no-raíz
USER vaultuser

# Exponer el puerto interno de FastAPI
EXPOSE 8000

# Comando de ejecución seguro usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]