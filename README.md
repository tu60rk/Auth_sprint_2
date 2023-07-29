# Для запуска проекта
- создать файл .env в главном каталоге
- заполнить по примеру .env.example
- заполнить по примеру .env.example
- создать файл .env в каталоге service_admin/config
- в терминале выполнить команду "docker-compose build"
- в терминале выполнить команду "docker-compose up"


# Для запуска тестов
- из папки {service_name}.tests/functional запустить команду "docker-compose rm && docker-compose up --build"


# Для чтения трассировки Jaeger
- из браузера перейдите по адресу http://localhost:16686/
- после выполнения любых действий с API сервиса service_auth можно посмотреть трассировку выбрав в Jaeger сервис в поле Service

# Доступ к сервисам
- auth - http://localhost/auth/api/v1/openapi
- movies - http://localhost/movies/api/v1/openapi
- admin - http://localhost/admin

# Ссылка для BlueDeep
https://github.com/tu60rk/Auth_sprint_2
