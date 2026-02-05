Movies & Series Catalog API

Stack: FastAPI, PostgreSQL, SQLAlchemy (async), Alembic, Docker Compose

Project structure
- app/
  - main.py
  - core/
    - config.py
  - db/
    - session.py
  - models/
    - models.py
  - schemas/
    - movie.py
  - repositories/
    - movie_repository.py
  - api/
    - deps.py
    - routers/
      - movies.py
- alembic/
  - env.py
  - versions/
    - 20240210_000001_init.py
- alembic.ini
- requirements.txt
- Dockerfile
- docker-compose.yml
- .env

Running locally with Docker Compose
1. Ensure Docker is installed and running.
2. Adjust values in .env if needed.
3. Start services:
   docker compose up --build
4. Open Swagger UI:
   http://localhost:8000/docs

Database connection is read from environment variables in .env and injected into both services by docker-compose.

Alembic migrations
- Migrations are executed automatically on container start (alembic upgrade head).

CRUD endpoints for movies
- GET /movies
- GET /movies/{id}
- POST /movies
- PUT /movies/{id}
- PATCH /movies/{id}
- DELETE /movies/{id}

Notes
- ACID: Each request handler uses a session with an explicit transaction (session.begin) to ensure atomic DB operations; constraints and FKs enforce consistency.
- You can pre-create genres and directors via future endpoints or direct SQL inserts to test relations, or pass genre_ids and director_id that exist.
