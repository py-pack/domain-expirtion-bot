
# 📁 Структура проєкту

```
.
├── api/                  # FastAPI + Poetry backend
├── front/                # Vue.js frontend
├── docker/               # Docker-файли
├── .env                  # змінні оточення (доступи до БД тощо)
└── docker-compose.yml    # основна docker-конфігурація
```



# Create Backend

```Dockerfile
FROM python:3.13-slim AS dev

ENV TZ=Europe/Kiev

RUN pip install --upgrade pip

RUN pip install poetry==2.1

WORKDIR /app
```

```yml
services:
    api:
        build:
            context: ./api
            dockerfile: Dockerfile
            target: dev
        image: "ldi/dom_exp:1.0"
        container_name: ${NAME_SERVICE:-domain_ex}_api
        restart: unless-stopped
        volumes:
            - ./api:/app
        env_file:
            - .env
        ports:
            - "10431:9000"

        command: bash
```

Initialize the project
```bash
docker-compose run --rm api bash

########
poetry init
# відповідай на запитання, або просто натискай Enter
poetry add fastapi uvicorn[standard] psycopg2-binary redis

```


Add Dockerfile
```Dockerfile

# old code ...

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi


COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]

```

Edit docker-compose.yml
```yml
command: [ "uvicorn", "main:app", "--reload", "--host", "${HOST:-0.0.0.0}", "--port", "${PORT:-9000}" ]
```

---

#  Налаштування Docker-інтерпретатора в PyCharm

## Встановлюємо інтерпретатор через Dockerfile:

1. **File → Settings → Project → Python Interpreter**
2. Натиснути ⚙️ → **Add...**
3. Обрати **Docker**
4. Поля:
   - **Dockerfile**: `api/Dockerfile`
   - **Context**: `api/`
   - Галочка: ✅ *Rebuild image automatically every time*
5. Натиснути **Next**, далі **Create**

---


# Create Frontend


```yml
services:
    front:
        image: node:22
        working_dir: /app
        volumes:
            - ./front:/app
        command: sh
```

```bash
    docker compose run --rm front bash
```

```bash
    npm create vue@latest
```

