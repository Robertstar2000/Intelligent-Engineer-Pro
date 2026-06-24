# Project Structure & Alembic Setup Reference

## Directory Layout

```
social_agent/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + routers
│   ├── config.py            # Pydantic Settings from .env
│   ├── db.py                # Async SQLAlchemy engine + SessionLocal
│   ├── models.py            # All ORM models (Base = DeclarativeBase)
│   ├── schemas.py           # Pydantic request/response models
│   ├── security.py          # Fernet encrypt/decrypt
│   ├── adapters/
│   │   ├── base.py          # PublishRequest, PublishResult, SocialAdapter
│   │   ├── linkedin.py      # LinkedIn Posts API
│   │   └── meta.py          # Facebook Page + Instagram Graph API
│   ├── services/
│   │   ├── formatter.py     # Per-platform text formatting
│   │   ├── policy.py        # Brand safety / risk scoring
│   │   └── publisher.py     # Orchestrates approval → publish flow
│   └── routes/
│       ├── accounts.py      # POST /social/accounts
│       └── posts.py         # POST /social/posts, /approve, /publish
├── tests/
│   ├── conftest.py          # pytest-asyncio mode=auto
│   ├── test_formatters.py
│   └── test_publish_flow.py
├── alembic/
│   ├── env.py               # Async Alembic config
│   ├── versions/
│   │   └── 001_initial.py   # Hand-written initial migration
├── .env                     # DATABASE_URL + TOKEN_ENCRYPTION_KEY
├── .env.example
└── pyproject.toml
```

## Alembic Async SQLAlchemy Pattern (Alembic 1.18.x)

### The `env.py` pattern

```python
import asyncio
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from app.config import settings
from app.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def _offline_requested() -> bool:
    # context.is_offline_mode() doesn't work at module level in Alembic 1.18.x
    # because the context proxy isn't fully initialized when env.py top-level code runs.
    # Check sys.argv as a reliable fallback.
    if "offline" in sys.argv:
        return True
    try:
        return context.is_offline_mode()
    except Exception:
        return False

def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        {"sqlalchemy.url": settings.database_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if _offline_requested():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Key pitfalls discovered (Alembic 1.18.x)

1. **`context.is_offline_mode()` fails at module level** — The Alembic `EnvironmentContext` proxy isn't fully initialized when `env.py` top-level code executes. Always check `sys.argv` for `"offline"` as a reliable fallback.

2. **Offline mode requires DB connection for `begin_transaction()`** — `context.configure(url=...)` alone doesn't set up a connection for offline mode. The `literal_binds=True` + `begin_transaction()` path still tries to connect. Options:
   - Write migrations manually (no autogenerate) and run `alembic upgrade head` with a live DB
   - Use `as_sql=True` with `output_buffer=StringIO()` for pure SQL generation without a connection

3. **`pip install -e ".[dev]"` with pyproject.toml** — If using a flat layout (no `src/` directory), add `[tool.setuptools.packages.find] include = ["app*"]` to `pyproject.toml` so setuptools can find your package.

### Initial migration (hand-written)

The initial migration (`001_initial.py`) was hand-written rather than auto-generated because:
- No PostgreSQL was available for autogenerate to compare against
- Hand-writing gives exact control over enum types, constraints, and indexes

The migration creates:
- 3 custom enums: `social_platform`, `post_status`, `approval_mode`
- 5 tables: `social_accounts`, `social_posts`, `social_post_targets`, `publish_attempts`, `social_audit_log`
- Indexes on foreign keys and frequently-queried columns
- Full `upgrade()` + `downgrade()` with proper CASCADE and enum cleanup

## Running migrations (when DB is available)

```bash
cd /mnt/usb_4tb/books/social_agent
source .venv/bin/activate
alembic upgrade head          # Apply all migrations
alembic downgrade -1          # Roll back one revision
alembic revision --autogenerate -m "description"  # Generate from model changes
alembic current                # Show current revision
```

## Model/migration sync rule

Always keep `app/models.py` and the migration in sync. If you add a table to the SQL schema, also add the corresponding SQLAlchemy model class. The env.py loads `Base.metadata` from models, so missing classes = missing tables in autogenerate comparisons.

## Fernet key generation

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
# Store in .env as TOKEN_ENCRYPTION_KEY
```
