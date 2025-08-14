# FastAPI JWT Postgres REST API (Dockerized Example)

Requirement (client brief): Example FastAPI JWT Postgres REST API running in Docker with test cases. Must include: Docker image (tested on macOS Sequoia 15.6 / Linux), SQL user/password from .env or docker compose env, FastAPI, JWT user auth, Postgres database, PGAdmin, CRUD endpoints, User and Book SQLModel models, automated tests.

This project delivers a minimal, production‑leaning template including authentication, persistence, and test setup. All services orchestrated with Docker Compose.

## Features
* FastAPI application with lifespan startup creating tables.
* JWT authentication (password hashing via passlib bcrypt + jose token generation).
* User & Book models built with SQLModel (SQLAlchemy core under the hood).
* PostgreSQL database service + persistent volume.
* PGAdmin web UI for inspecting the database.
* CRUD endpoints for books (scoped to authenticated user) and user creation.
* Token endpoint (OAuth2 password flow style) returning access token.
* Async DB access using SQLAlchemy async engine (asyncpg driver in production; aiosqlite for isolated test DB).
* Test suite (pytest + httpx + pytest-asyncio) including auth + CRUD paths.
* Environment variable driven configuration (.env loaded automatically).

## Stack
| Layer | Tech |
|-------|------|
| API | FastAPI |
| Auth | OAuth2 password flow + JWT (HS256) |
| ORM / Models | SQLModel |
| DB (runtime) | PostgreSQL 15 (asyncpg) |
| Admin | PGAdmin4 |
| Tests | pytest, httpx (ASGITransport), pytest-asyncio |
| Packaging | Poetry |
| Container | Docker / docker-compose |

## Project Structure
```
app/
	api/controller.py      # Route handlers
	auth/auth_handler.py   # Password hashing + JWT helpers
	db/database.py         # Async engine + session dependency
	models/entities.py     # SQLModel User & Book
	main.py                # FastAPI app + lifespan
tests/                   # Pytest suite
docker-compose.yml       # Services: db, pgadmin, web
Dockerfile               # Web image build
pyproject.toml           # Dependencies (Poetry)
.env                     # Environment variables (create this)
```

## Environment Variables (.env)
Example `.env` (create at repo root):
```
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppassword
POSTGRES_DB=appdb
JWT_SECRET=supersecretkey
```
These are injected into the `db` (Postgres) container and the `web` service.

## Running (Development / Demo)
Build and start stack:
```zsh
docker-compose up --build
```
Services:
* API: http://localhost:8000 (Swagger UI at /docs)
* PGAdmin: http://localhost:5050 (email: admin@admin.com / password: admin)
* Postgres: localhost:5432

Hot reload: You can add `--reload` to the uvicorn command in `docker-compose.yml` during development if desired.

## API Overview
Auth:
* POST /token – obtain JWT access token (form fields: username, password)

Users:
* POST /users/ – create a user (sends hashed_password field which is re-hashed internally)
* GET /users/me – retrieve current authenticated user

Books (require Authorization: Bearer <token>):
* POST /books/ – create book owned by current user
* GET /books/ – list current user books
* GET /books/{book_id} – retrieve one
* PUT /books/{book_id} – update title/author
* DELETE /books/{book_id} – delete

## Auth Flow
1. Create user (POST /users/).
2. Login (POST /token) with form data to receive JWT.
3. Send `Authorization: Bearer <token>` header to access protected routes.

## Testing
Run all tests locally (Python 3.12 + Poetry installed):
```zsh
poetry install --with dev --no-root
poetry run pytest -q
```
The test suite spins up an isolated SQLite (aiosqlite) database per session, independent from Postgres.

Inside containers:
```zsh
docker-compose exec web pytest -q
```

## Docker Image Notes
* Uses `python:3.12-slim` base.
* Installs dependencies with Poetry (no virtualenv inside container).
* Runs `uvicorn app.main:app` on port 8000.
* Works on macOS Sequoia 15.6 (tested) and Linux (standard Docker environment).

## Extending
Ideas:
* Add refresh tokens / token revocation.
* Add Alembic migrations.
* Add rate limiting / logging middleware.
* Implement pagination for book listing.

## License
MIT (adjust as needed).

## Quick Troubleshooting
| Issue | Fix |
|-------|-----|
| 401 on /token | Ensure user created and password correct |
| PGAdmin cannot connect | Check Postgres env vars match `.env` |
| Tests fail on DB | Remove old test *.db files, re-run |
| ModuleNotFoundError aiosqlite | Run Poetry install with dependencies |

---
This repository is a concise baseline for JWT-secured FastAPI + Postgres projects with Docker and tests.
