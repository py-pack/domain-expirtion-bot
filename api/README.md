# Domain Expiration Slim

Данный проект собирает данные о доменах


1. Копируем `.env.example` в `.env`
    
        cp .env.example .env

2. Заполняем секретный ключ в 32 символа `X_TOKEN`

3. Запускаем через докер

        docker compose up --build

4. Можем выполнить запрос

        curl --location 'http://localhost:9001/api/domain/expiration?domain_name=google.com' \
             --header 'Token-X: your_32_char_static_token_here'



---

## Commands

### Add user

```bash
docker compose exec api python -m command.add_user
```
