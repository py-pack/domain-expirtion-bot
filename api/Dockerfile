FROM python:3.13-slim

ENV TZ=Europe/Kiev
ENV PYTHONPATH=/app/src
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY . .

RUN uv sync --frozen --no-dev

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]

#FROM dev AS prod
#
#COPY ./app /app
#COPY ./pyproject.toml /app
#COPY ./poetry.lock /app
#
#EXPOSE 9000
#
#RUN poetry install --no-dev --no-interaction --no-ansi
#
#CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9000"]
