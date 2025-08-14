FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala Poetry
RUN pip install --no-cache-dir --upgrade pip \
    && pip install poetry

# Copia manifestos primeiro (cache layer)
COPY pyproject.toml poetry.lock* ./

# Instala dependências (sem criar venv separada)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copia código mantendo a estrutura de pacote (gera /app/app/...)
COPY app ./app

# Comando default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
