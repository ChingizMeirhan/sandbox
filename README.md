Events Journal

Events Journal — учебно-прикладной backend-сервис для приёма, хранения и чтения событий (events), реализованный как полноценный микросервис.

Проект используется как архитектурная и техническая база для отработки:

FastAPI и REST API,

SQLAlchemy 2.x (ORM),

PostgreSQL + JSONB,

Alembic миграций,

Docker Compose,

middleware,

health/readiness checks,

API-тестирования.

Проект сознательно построен как production-style сервис, а не как упрощённый учебный пример.

Возможности

Приём событий через HTTP API

Валидация входных данных

Хранение событий в PostgreSQL (JSONB payload)

Чтение списка событий

Healthcheck и readiness endpoints

Request ID middleware (tracing)

Управление схемой БД через Alembic

Smoke-тесты API

Полностью воспроизводимый запуск через Docker Compose

Технологический стек

Python 3.12

FastAPI

SQLAlchemy 2.x

PostgreSQL 16

Alembic

Docker / Docker Compose

pytest + httpx

Архитектура

Проект состоит из двух сервисов:

app — FastAPI приложение

db — PostgreSQL

Вся инфраструктура поднимается одной командой через Docker Compose.

Принципиальное архитектурное решение:

Приложение не управляет схемой БД напрямую.
Единственный источник истины для схемы — Alembic миграции.

API
Healthcheck
GET /healthz


Ответ:

{"status":"ok"}


Используется для проверки доступности сервиса.

Readiness
GET /readyz


Ответ:

{"status":"ready"}


Используется для определения готовности сервиса к обработке запросов
(применяется в тестах и при запуске).

Создание события
POST /events


Body:

{
  "source": "docker",
  "type": "test",
  "payload": {
    "ok": true,
    "n": 123
  }
}


Ответ (201):

{
  "id": 1,
  "source": "docker",
  "type": "test",
  "payload": {
    "ok": true,
    "n": 123
  },
  "created_at": "2026-02-08T18:26:41.123Z"
}


Особенности:

payload хранится как JSONB;

лишние поля запрещены;

created_at заполняется на стороне БД.

Получение списка событий
GET /events?limit=20


Особенности:

сортировка по убыванию id (последние события сверху);

limit от 1 до 200 (валидация).

Middleware
RequestIdMiddleware

Читает X-Request-Id из входящего запроса (если передан)

Генерирует UUID, если заголовок отсутствует

Добавляет X-Request-Id в каждый ответ

Используется для трассировки запросов и логирования.

Структура проекта
sandbox/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── middleware.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── event.py
│   ├── schemas/
│   │   └── event.py
│   └── main.py
│
├── alembic/
│   ├── versions/
│   │   └── *_create_events_table.py
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   └── test_smoke.py
│
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── requirements.txt
├── .env              (не коммитится)
├── .env.app          (не коммитится)
├── .env.app.example
└── README.md

Назначение основных файлов
app/main.py

Точка входа FastAPI:

инициализация приложения;

подключение middleware;

подключение роутов;

настройка логирования.

Не содержит:

create_all;

логики работы с БД.

app/api/routes.py

HTTP API:

/healthz

/readyz

/events

Содержит бизнес-логику и работу с БД.

app/core/config.py

Конфигурация приложения через pydantic-settings.

Читает только .env.app, содержит:

DATABASE_URL

APP_ENV

LOG_LEVEL

app/db/session.py

Создание SQLAlchemy engine и Session.

app/models/event.py

ORM-модель таблицы events.

app/schemas/event.py

Pydantic-схемы:

EventIn

EventOut

alembic/

Система миграций БД.

Все изменения схемы выполняются только через Alembic.

tests/test_smoke.py

Smoke-тесты API:

healthz / readyz

создание и чтение событий

валидация входных данных

проверка X-Request-Id

Переменные окружения
.env (Docker / DB)
POSTGRES_DB=petdb
POSTGRES_USER=petuser
POSTGRES_PASSWORD=petpass

.env.app (Application)
APP_ENV=dev
LOG_LEVEL=INFO
DATABASE_URL=postgresql+psycopg://petuser:petpass@db:5432/petdb


Файлы .env и .env.app не коммитятся.
В репозитории хранится .env.app.example.

Запуск проекта
Запуск сервисов
docker compose up -d --build

Остановка
docker compose down

Полный сброс БД
docker compose down -v

Управление схемой БД

Создание миграции:

docker compose exec -w /app app alembic revision --autogenerate -m "message"


Применение миграций:

docker compose exec -w /app app alembic upgrade head

Тестирование
pytest -q


Тесты ожидают готовность сервиса через /readyz.

Текущее состояние проекта

Проект:

стабильно запускается;

воспроизводим одной командой;

архитектурно корректен;

готов к расширению.

Планируемое развитие

фильтрация событий (source, type, date range);

индексы в PostgreSQL;

idempotency (защита от дублей);

статусы обработки событий;

cursor-pagination;

observability (логирование, метрики).

Автор

Pet-проект для практики архитектуры backend-сервисов и инженерных подходов.
