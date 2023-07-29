# Для запуска проекта
- создать файлы .env's в главном каталоге как в папке envs
- в терминале выполнить команду "docker-compose --env-file compose.env build"
- в терминале выполнить команду "docker-compose --env-file compose.env up"


# Для запуска тестов
- из папки {service_name}.tests/functional запустить команду "docker-compose rm && docker-compose up --build"


# Для чтения трассировки Jaeger
- из браузера перейдите по адресу http://localhost:16686/
- после выполнения любых действий с API сервиса service_auth можно посмотреть трассировку выбрав в Jaeger сервис в поле Service


# Ссылка для BlueDeep
https://github.com/tu60rk/Auth_sprint_2
