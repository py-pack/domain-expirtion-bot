FROM python:3.11-slim as dev

ENV TZ=Europe/Kiev

RUN pip install --upgrade pip

RUN pip install poetry==1.8.2

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM dev as prod

COPY ./app /app
COPY ./pyproject.toml /app
COPY ./poetry.lock /app

EXPOSE 9000

RUN poetry install --with prod

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9000"]
