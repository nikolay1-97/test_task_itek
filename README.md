# Описание приложения.
Приложение представляет собой REST API сервис, позволяющий совершать CRUD операции с сущностью пользователь.

Приложение написано на FastAPI.

Приложение поддерживает использование реляционной СУБД PostgreSQL и нереляционной Redis.

Есть возможность запуска приложения в Docker.

Для запуска приложения локально, необходимы запущенные серверы PostgreSQL и Redis.
## Описание выбора типа СУБД и настроек репозиториев.
В приложении реализовано два репозитория для работы с данными.

Один репозиторий взаимодействует с PostgreSQL, другой с Redis.

Для выбора СУБД PostgreSQL, нужно присвоить переменной окружения "NO_SQL" значение False.

Для выбора СУБД Redis, нужно присвоить переменной окружения "NO_SQL" значение True.
Переменная окружения "NO_SQL" хранится в файлах ".env" и ".env-non-dev" в корневой директории.

Чтобы дать либо отменить разрешение на добавлене/обновление/чтение/удаление данных,
нужно установить соответствующие значения для следующих переменных окружения:
  - CREAT- разрешение на добавление записей в БД(True либо False);
  - UPDATE- разрешение на обновление данных в БД(True либо False);
  - READ- разрешение на чтение данных из БД(True либо False);
  - DELETE- разрешение на удаление данных из БД(True либо False).

Переменные окружения из файла ".env" используются для запуска приложения локально.

Переменные окружения из файла ".env-non-dev" используются для запуска приложения в Docker.
## Описание технологий, примененных в приложении.
Приложение написано на FastAPI.

Есть возможность использовать СУБД PostgreSQL и Redis.

Миграции выполняются с помощью "Alembic".

Сборщик зависимостей- Poetry.

Есть возможность запуска приложения в Docker.
## Описание структуры приложения.
Классы-репозитории находятся в "/app/data_sources/storages/user_repository.py.

Модели данных находятся в "/app/data_sources/models.py".

Модели данных Pydantic находятся в "/app/pydantic_models/pydantic_models.py".

Обработчики запросов находятся в "app/views/crud_for_users.py".

Конфигурация приложения находится в "/app/config.py".

Файл запуска приложения- "/app/main.py".

Переменные окружения, необходимые для запуска приложения локально, находятся в файле ".env" в корневой директории.

Переменные окружения, необходимые для запуска приложения в Docker, находятся в файле ".env-non-dev" в корневой директории.
# Запуск приложения в Docker.
## Подготовка к запуску приложения.
Перед запуском приложения, необходимо установить значения для переменных окружения в файле ".env-non-dev",
который находится в корневой директории.

В данном файле находятся следующие переменные окружения:

POSTGRES_DB,

POSTGRES_USER- имя пользователя базы данных,

POSTGRES_PASSWORD- пароль для базы данных,

DB_USER- имя пользователя базы данных,

PASSWORD- пароль для базы данных,

DB_HOST- хост базы данных,

DB_NAME- имя базы данных,

DB_PORT- порт базы данных,

REDIS_HOST- хост Redis,

REDIS_PORT- порт для Redis,

APP_HOST- хост для запуска приложения,

APP_PORT- порт для запуска приложения,

NO_SQL- выбор типа СУБД(True либо False)

CREAT- разрешение на добавление записей в БД(True либо False)

UPDATE- разрешение на обновление данных в БД(True либо False)

READ- разрешение на чтение данных из БД(True либо False)

DELETE- разрешение на удаление записей из БД(True либо False)
## Запуск приложения.
Для сборки контейнеров необходимо выполнить команду "docker compose build" в терминале из корневой директории.
Для запуска приложения необходимо выполнить команду "docker compose up app" в терминале из корневой директории.
После запуска приложения, взаимодействовать с ним можно, перейдя по ссылке "http://хост:порт/docs".
По данной ссылке будет доступна автодокументация приложения.
# Запуск приложения локально.
## Подготовка к запуску приложнния.
Перед запуском приложения, необходимо установить значения для переменных окружения в файле ".env",
который находится в корневой директории.

В данном файле находятся следующие переменные окружения:

DB_USER- имя пользователя базы данных,

PASSWORD- пароль для базы данных,

DB_HOST- хост базы данных,

DB_NAME- имя базы данных,

DB_PORT- порт базы данных,

REDIS_HOST- хост Redis,

REDIS_PORT- порт для Redis,

APP_HOST- хост для запуска приложения,

APP_PORT- порт для запуска приложения,

NO_SQL- выбор типа СУБД(True либо False)

CREAT- разрешение на добавление записей в БД(True либо False)

UPDATE- разрешение на обновление данных в БД(True либо False)

READ- разрешение на чтение данных из БД(True либо False)

DELETE- разрешение на удаление записей из БД(True либо False)

Для выполнения миграций, необходимо выполнить команду "alembic upgrade head" 2 раза подряд в терминале из
директории "/app".

Для запуска приложения, необходимо выполнить команду "python main.py" в терминале из директории "/app".

После запуска приложения, взаимодействовать с ним можно, перейдя по ссылке "http://хост:порт/docs".
По данной ссылке будет доступна автодокументация приложения.




