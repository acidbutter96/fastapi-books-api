# 🚀 FastAPI JWT Postgres REST API (Dockerized Example)

Minimal, production‑leaning template implementing JWT auth, Postgres persistence, async SQLModel ORM and test suite — all orchestrated with Docker Compose. ✅ Built & verified on macOS Sequoia 15.6 and Linux.

> Client brief: Provide an example FastAPI + JWT + Postgres REST API in Docker with tests, CRUD, PGAdmin and User/Book models.

---

### 📚 Table of Contents
1. ✨ Features
2. 🧱 Tech Stack
3. 🗂 Project Structure
4. 🔐 Environment Variables
5. 🏁 Quick Start
6. 🔌 API Reference
7. 🔄 Auth Flow
8. 🧪 Testing
9. 🐳 Docker Image Notes
10. 🚀 Roadmap / Extensions
11. 🛠 Troubleshooting
12. 📄 License

---

## ✨ Features
| ✅ | Feature |
|----|---------|
| ✔ | FastAPI app with lifespan startup auto-creating tables |
| ✔ | JWT auth (HS256) + bcrypt password hashing (no passlib dependency) |
| ✔ | User & Book SQLModel models (type-safe + Pydantic integration) |
| ✔ | CRUD endpoints for books scoped per authenticated user |
| ✔ | OAuth2 password flow token endpoint (/token) |
| ✔ | Async SQLAlchemy engine (asyncpg in prod, aiosqlite for tests) |
| ✔ | PGAdmin UI for DB inspection |
| ✔ | Isolated, deterministic pytest suite (httpx AsyncClient) |
| ✔ | Environment-based configuration via .env |
| ✔ | Docker Compose orchestration (web, db, pgadmin) |

## 🧱 Tech Stack
| Layer | Tech |
|-------|------|
| API | FastAPI |
| Auth | OAuth2 password grant + JWT (python-jose) |
| Password Hashing | bcrypt |
| Models / ORM | SQLModel (SQLAlchemy core) |
| DB (runtime) | PostgreSQL 15 (asyncpg) |
| Admin | PGAdmin4 |
| Tests | pytest, httpx (ASGITransport), pytest-asyncio |
| Packaging | Poetry |
| Container | Docker & docker-compose |

## 🗂 Project Structure
```
app/
	api/controller.py      # Routes (auth, users, books)
	auth/auth_handler.py   # JWT + bcrypt helpers
	db/database.py         # Async engine, sessions, init
	models/entities.py     # SQLModel User & Book tables
	main.py                # FastAPI app + lifespan
tests/                   # Test suite (auth + CRUD)
docker-compose.yml       # Services: db, pgadmin, web
Dockerfile               # Build instructions
pyproject.toml           # Dependencies (Poetry)
.env                     # Environment variables (user-provided)
```

## 🔐 Environment Variables (.env)
Example:
```
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppassword
POSTGRES_DB=appdb
JWT_SECRET=supersecretkey
```
Optional override: `DATABASE_URL` (e.g. for tests / CI). Defaults assembled from the above if not provided.

## 🏁 Quick Start
```zsh
# 1. Create .env (see above)
# 2. Build & start
docker compose up --build -d

# 3. Visit API docs
open http://localhost:8000/docs  # macOS (use xdg-open on Linux)

# 4. (Optional) Run tests locally
poetry install --with dev --no-root
poetry run pytest -q
```
Services:
* API: http://localhost:8000 (Swagger UI /docs)
* PGAdmin: http://localhost:5050 (admin@admin.com / admin)
* Postgres: localhost:5432

Hot reload (dev): add `--reload` to the uvicorn command inside `docker-compose.yml`.

## 🔌 API Reference (Summary)
Auth:
* POST `/token` – obtain JWT (form: username, password)

Users:
* POST `/users/` – create user (sends plaintext password -> hashed server-side)
* GET `/users/me` – current user profile

Books (Bearer token required):
* POST `/books/` – create
* GET `/books/` – list own
* GET `/books/{id}` – retrieve
* PUT `/books/{id}` – update
* DELETE `/books/{id}` – delete

## 🔄 Auth Flow
1. Create user: POST `/users/`
2. Login: POST `/token` (form data)
3. Use header: `Authorization: Bearer <token>` for protected endpoints

## 🧪 Testing
Local (Poetry):
```zsh
poetry install --with dev --no-root
poetry run pytest -q
```
The suite switches to an ephemeral SQLite file DB via `DATABASE_URL` override — fast & isolated.

Inside container:
```zsh
docker compose exec web pytest -q
```

## 🐳 Docker Image Notes
* Base: `python:3.12-slim`
* Dependency management: Poetry (system install, no nested venv)
* Entrypoint: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
* Volume: mounts `./app` for live code edits (dev convenience)

## 🚀 Roadmap / Extensions
- [ ] Refresh / revoke tokens
- [ ] Alembic migrations instead of create_all
- [ ] Pagination & filtering for `/books/`
- [ ] Structured logging + request ID middleware
- [ ] Rate limiting / throttling
- [ ] CI pipeline (GitHub Actions) + coverage
- [ ] Separate Pydantic schemas from DB models
- [ ] Error handling module with custom exceptions

## 🛠 Troubleshooting
| Issue | Fix |
|-------|-----|
| 401 on /token | Ensure user exists & correct password |
| PGAdmin fails to connect | Verify `.env` matches docker-compose env values |
| Tables not created | Confirm lifespan ran; check container logs for DB URL |
| Tests failing with missing aiosqlite | Re-run `poetry install --with dev` |
| Connection refused on startup | Postgres not ready yet; rerun or add healthcheck |

## 📄 License
MIT (adjust if required).

---
This repository is a concise baseline for JWT‑secured FastAPI + Postgres projects with Docker and tests. PRs / improvements welcome. ✌️
