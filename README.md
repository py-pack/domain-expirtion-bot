# Domain Expiration 3

Данный проект собирает данные о доменах


1. Копируем `.env.example` в `.env`
    
        cp .env.example .env

1. Заполняем секретный ключ в 32 символа `X_TOKEN`

1. Запускаем через докер

        docker compose up --build

1. Можем выполнить запрос

        curl --location 'http://localhost:9001/api/domain/expiration?domain_name=google.com' \
             --header 'Token-X: your_32_char_static_token_here'