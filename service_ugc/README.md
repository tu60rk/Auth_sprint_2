# Для запуска ugc сервиса
- создать файл ugc.env в текущем каталоге. Пример файла в envs -> ugc.env.example
- в терминале выполнить команду "docker-compose build"
- в терминале выполнить команду "docker-compose up"


# Для запуска тестов
- из папки {service_name}.tests/functional запустить команду "docker-compose rm && docker-compose up --build"

# Kafka
- Создание топика доступно по адресу: localhost:8080

# Доступ к API сервиса
- ugc - http://localhost/api/v1/openapi


# Ссылка для BlueDeep
https://github.com/tu60rk/Auth_sprint_2
