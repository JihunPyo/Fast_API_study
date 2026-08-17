# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A group study repository for the book *코딩 자율학습 FastAPI 파이썬 백엔드 개발 입문* (FastAPI backend dev). It is not a single application — it's a collection of independent FastAPI apps/snapshots, each runnable on its own from its own directory.

- `solution/` — the book's official reference source, downloaded as-is (see `solution/README.md`). Do not "fix" or refactor this; it's a reference to compare against.
  - `solution/todos/` — final Todo app with all chapters (3–7) applied.
  - `solution/blog/` — final Blog app (self-check project, DB/ORM stage only).
  - `solution/source/todos3` … `todos7/` — snapshots of the Todo app at the end of each chapter, so a chapter can be started mid-book without earlier chapters.
- `pyojihun/` (and similarly named per-member folders) — each participant's own work, organized as `todos_wkN/` and `blog_wkN/` per week, per `README.md`'s stated folder convention.

Each week builds on two parallel tracks (see root `README.md`): typing along with the book's Todo app chapter-by-chapter, and independently designing a parallel "Blog" app with the same features (CRUD → ORM → auth → JWT → file upload) without copying the solution.

## Running an app

Each numbered app (`todos3`..`todos7`, `todos`, `blog`) is a standalone FastAPI project with no shared code between directories — `cd` into the specific one you're working on before running anything.

```bash
cd solution/todos   # or solution/source/todos5, solution/blog, etc.
pip install -r ../requirements.txt   # from solution/, or relative path
fastapi dev main.py
```

There are no test suites, lint configs, or build tooling in this repo — it's instructional code, verify behavior by running the app and hitting endpoints (e.g. via `/docs` Swagger UI).

## Architecture pattern (chapters 4+)

From `todos4` onward, every app snapshot follows the same layered structure — recognize it rather than rediscovering it per-directory:

```
main.py              # FastAPI() app, lifespan hook calls Base.metadata.create_all, includes routers
models.py            # Pydantic-facing domain models
database/
  db_connection.py   # SQLAlchemy engine + SessionFactory + get_session() dependency
  orm.py             # SQLAlchemy ORM table classes (Base subclasses)
schema/
  request.py         # Pydantic request bodies
  response.py         # Pydantic response models
routers/              # (todos5+) APIRouter per resource, e.g. todo.py, user.py
auth/                 # (todos5+) password.py (pwdlib/argon2 hashing), jwt.py (pyjwt) or session-based auth
```

- DB is MySQL via `pymysql`, connection string hardcoded in `database/db_connection.py` (e.g. `mysql+pymysql://root:fastapi@localhost:3306/fastapi_db`) — a local MySQL instance with matching credentials/db name must exist before running any app from `todos4` onward.
- Auth evolves across chapters: `todos5` introduces password hashing, `todos6`/`todos7`/final `todos` add JWT (`jwt_create.py`, `jwt_decoding.py`, `jwt_checked.py` are standalone scratch scripts demonstrating JWT flow, not imported by `main.py`) alongside `SessionMiddleware`-based session login.
- `uploads/` holds files handled by chapter 7's file upload feature.

When editing or reviewing code, match the chapter-appropriate pattern for that directory rather than importing conventions from a later chapter's snapshot.
