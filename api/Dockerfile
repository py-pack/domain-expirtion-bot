FROM python:3.13-slim

ENV TZ=Europe/Kiev

RUN pip install --upgrade pip

RUN pip install poetry==2.1

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]

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
