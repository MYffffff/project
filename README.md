Каталог фильмов и сериалов (FastAPI)

Стек: FastAPI, PostgreSQL, SQLAlchemy (async), Alembic, Docker Compose

Запуск
1) Установите и запустите Docker Desktop.
2) Проверьте переменные в .env (по умолчанию уже настроено).
3) Старт:
   docker compose up --build
4) Swagger UI: http://localhost:8000/docs
   Health-check: http://localhost:8000/health

CRUD для фильмов
- GET /movies — список
- GET /movies/{id} — получить по id
- POST /movies — создать
- PUT /movies/{id} — полное обновление
- PATCH /movies/{id} — частичное обновление
- DELETE /movies/{id} — удалить

Данные и связи
- В базе: фильмы, сериалы, жанры, режиссёры; жанры связаны с фильмами и сериалами (many-to-many).
- Для фильмов можно ��ередавать director_id и genre_ids (идентификаторы должны существовать в БД).

Транзакционность
- Каждая операция выполняется внутри транзакции (ACID) через session.begin().

Структура
- app/ — приложение (роуты, модели, схемы, репозитории)
- alembic/ — миграции
- Dockerfile, docker-compose.yml, .env
