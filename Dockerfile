FROM python:3.11-slim

ENV POETRY_VERSION=1.5.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /bot

COPY pyproject.toml poetry.lock /bot/

RUN poetry install --no-root --no-interaction --no-ansi

COPY . /bot/

CMD ["python", "bot.py"]
