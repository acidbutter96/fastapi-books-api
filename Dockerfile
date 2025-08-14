FROM python:3.12-slim
WORKDIR /app
# Instala Poetry
RUN pip install --no-cache-dir --upgrade pip \
    && pip install poetry

# Copia arquivos do projeto
COPY pyproject.toml poetry.lock* ./
COPY ./app /app

# Instala dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
