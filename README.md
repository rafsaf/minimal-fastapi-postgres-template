# Minimal FastAPI PostgreSQL template

[![Live example](https://img.shields.io/badge/live%20example-https%3A%2F%2Fminimal--fastapi--postgres--template.rafsaf.pl-blueviolet)](https://minimal-fastapi-postgres-template.rafsaf.pl/)
[![License](https://img.shields.io/github/license/rafsaf/minimal-fastapi-postgres-template)](https://github.com/rafsaf/minimal-fastapi-postgres-template/blob/main/LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue)](https://docs.python.org/3/whatsnew/3.14.html)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Tests](https://github.com/rafsaf/minimal-fastapi-postgres-template/actions/workflows/tests.yml/badge.svg)](https://github.com/rafsaf/minimal-fastapi-postgres-template/actions/workflows/tests.yml)

_Check out online example: [https://minimal-fastapi-postgres-template.rafsaf.pl](https://minimal-fastapi-postgres-template.rafsaf.pl), it's 100% code used in template (docker image) with added my domain and https only._

- [Minimal FastAPI PostgreSQL template](#minimal-fastapi-postgresql-template)
  - [About](#about)
  - [Features](#features)
  - [Quickstart](#quickstart)
    - [1. Create repository from a template](#1-create-repository-from-a-template)
    - [2. Install dependencies with uv](#2-install-dependencies-with-uv)
    - [3. Run app](#3-run-app)
    - [4. Activate pre-commit](#4-activate-pre-commit)
    - [5. Running tests](#5-running-tests)
  - [Step by step example - POST and GET endpoints](#step-by-step-example---post-and-get-endpoints)
    - [1. Create new app](#1-create-new-app)
    - [2. Create SQLAlchemy model](#2-create-sqlalchemy-model)
    - [3. Import new models.py file in alembic env.py](#3-import-new-modelspy-file-in-alembic-envpy)
    - [4. Create and apply alembic migration](#4-create-and-apply-alembic-migration)
    - [5. Create request and response schemas](#5-create-request-and-response-schemas)
    - [6. Create endpoints](#6-create-endpoints)
    - [7. Add Pet model to tests factories](#7-add-pet-model-to-tests-factories)
    - [8. Create new test file](#8-create-new-test-file)
    - [9. Write tests](#9-write-tests)
  - [Design choices](#design-choices)
    - [Dockerfile](#dockerfile)
    - [Registration](#registration)
    - [Delete user endpoint](#delete-user-endpoint)
    - [JWT and refresh tokens](#jwt-and-refresh-tokens)
    - [Writing scripts / cron](#writing-scripts--cron)
    - [Docs URL](#docs-url)
    - [CORS](#cors)
    - [Allowed Hosts](#allowed-hosts)
  - [License](#license)

## About

If you are curious about latest changes and rationale, read 2026 update blog post: [Update of minimal-fastapi-postgres-template to version 7.0.0](https://rafsaf.pl/blog/2026/02/07/update-of-minimal-fastapi-postgres-template-to-version-7.0.0/).

Enjoy!

## Features

- [x] Template repository.
- [x] [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) 2.0, async queries, best possible autocompletion support.
- [x] PostgreSQL 18 database under [asyncpg](https://github.com/MagicStack/asyncpg) interface.
- [x] Full [Alembic](https://github.com/alembic/alembic) migrations setup (also in unit tests).
- [x] Secure and tested setup for [PyJWT](https://github.com/jpadilla/pyjwt) and [bcrypt](https://github.com/pyca/bcrypt).
- [x] Ready to go Dockerfile with [uvicorn](https://www.uvicorn.org/) webserver.
- [x] [uv](https://docs.astral.sh/uv/getting-started/installation/), [mypy](https://github.com/python/mypy), [pre-commit](https://github.com/pre-commit/pre-commit) hooks with [ruff](https://github.com/astral-sh/ruff).
- [x] Perfect pytest asynchronous test setup and full coverage.

![template-fastapi-minimal-openapi-example](https://rafsaf.pl/blog/2026/02/07/update-of-minimal-fastapi-postgres-template-to-version-7.0.0/minimal-fastapi-postgres-template-2026-02-07-version-7.0.0.png)

## Quickstart

### 1. Create repository from a template

See [docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) or just use git clone.

### 2. Install dependencies with [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
cd your_project_name

uv sync

```

Uv should automatically install Python version currently required by template (>=3.14) or use existing Python installation if you already have it.

### 3. Run app

```bash
make up

```

Refer to `Makefile` to see shortcut (`apt install build-essential` - on linux)

If you want to work without it, this should do:

```bash
docker compose up -d

alembic upgrade head

uvicorn app.main:app --reload

```

You should then use `git init` (if needed) to initialize git repository and access OpenAPI spec at [http://localhost:8000/](http://localhost:8000/) by default. See last section for customizations.

### 4. Activate pre-commit

[pre-commit](https://pre-commit.com/) is de facto standard now for pre push activities like isort or black or its nowadays replacement ruff.

Refer to `.pre-commit-config.yaml` file to see my current opinionated choices.

```bash
# Shortcut
make lint

```

Full commands

```bash
# Install pre-commit
pre-commit install --install-hooks

# Run on all files
pre-commit run --all-files

```

### 5. Running tests

Note, it will create databases for session and run tests in many processes by default (using pytest-xdist) to speed up execution, based on how many CPU are available in environment.

For more details about initial database setup, see logic `app/conftest.py` file, especially `fixture_setup_new_test_database` function. Pytest configuration is also in `[tool.pytest.ini_options]` in `pyproject.toml`.

Moreover, there is coverage pytest plugin with required code coverage level 100%.

```bash
# see all pytest configuration flags in pyproject.toml
pytest

# or 
make test

```

## Step by step example - POST and GET endpoints

I always enjoy to have some kind of an example in templates (even if I don't like it much, _some_ parts may be useful and save my time...), so let's create two example endpoints:

- `POST` endpoint `/pets/create` for creating `Pets` with relation to currently logged `User`
- `GET` endpoint `/pets/me` for fetching all user's pets.

### 1. Create new app

Add `app/pets` folder and `app/pets/__init__.py`.

### 2. Create SQLAlchemy model

We will add `Pet` model to `app/pets/models.py`.

```python
# app/pets/models.py

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class Pet(Base):
    __tablename__ = "pets_pet"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        sa.ForeignKey("auth_user.user_id", ondelete="CASCADE"),
    )
    pet_name: Mapped[str] = mapped_column(sa.String(50), nullable=False)

```

Note, we are using super powerful SQLAlchemy feature here - `Mapped` and `mapped_column` were first introduced in SQLAlchemy 2.0, if this syntax is new for you, read carefully [what's new](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html) part of documentation.

### 3. Import new models.py file in alembic env.py

Without this step, alembic won't be able to follow changes in new `models.py` file. In `alembic/env.py` import new file

```python
# alembic/env.py

(...) 
# import other models here
import app.pets.models  # noqa

(...)

```

### 4. Create and apply alembic migration

```bash
### Use below commands in root folder in virtualenv ###

# if you see FAILED: Target database is not up to date.
# first use alembic upgrade head

# Create migration with alembic revision
alembic revision --autogenerate -m "create_pet_model"


# File similar to "2022050949_create_pet_model_44b7b689ea5f.py" should appear in `/alembic/versions` folder


# Apply migration using alembic upgrade
alembic upgrade head

# (...)
# INFO  [alembic.runtime.migration] Running upgrade d1252175c146 -> 44b7b689ea5f, create_pet_model
```

PS. Note, alembic is configured in a way that it work with async setup and also detects specific column changes if using `--autogenerate` flag.

### 5. Create request and response schemas

```python
# app/pets/schemas.py

from pydantic import BaseModel, ConfigDict


class PetCreateRequest(BaseModel):
    pet_name: str


class PetResponse(BaseModel):
    id: int
    pet_name: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)

```

### 6. Create endpoints

```python
# app/pets/views.py

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core import database_session
from app.pets.models import Pet
from app.pets.schemas import PetCreateRequest, PetResponse

router = APIRouter()


@router.post(
    "/create",
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
    description="Creates new pet. Only for logged users.",
)
async def create_new_pet(
    data: PetCreateRequest,
    session: AsyncSession = Depends(database_session.new_async_session),
    current_user: User = Depends(get_current_user),
) -> Pet:
    new_pet = Pet(user_id=current_user.user_id, pet_name=data.pet_name)

    session.add(new_pet)
    await session.commit()

    return new_pet


@router.get(
    "/me",
    response_model=list[PetResponse],
    status_code=status.HTTP_200_OK,
    description="Get list of pets for currently logged user.",
)
async def get_all_my_pets(
    session: AsyncSession = Depends(database_session.new_async_session),
    current_user: User = Depends(get_current_user),
) -> list[Pet]:
    pets = await session.scalars(
        select(Pet).where(Pet.user_id == current_user.user_id).order_by(Pet.pet_name)
    )

    return list(pets.all())

```

Now we need to add newly created router to `main.py` app.

```python
# main.py

(...)

from app.pets.views import router as pets_router

(...)

app.include_router(pets_router, prefix="/pets", tags=["pets"])

```

### 7. Add Pet model to tests factories

File `app/tests/factories.py` contains `User` model factory already. Every new DB model should also have it, as it really simplify things later (when you have more models and relationships).

```python
# app/tests/factories.py
(...)

from app.pets.models import Pet

(...)

class PetFactory(SQLAlchemyFactory[Pet]):
    pet_name = Use(Faker().first_name)

```

### 8. Create new test file

Create folder `app/pet/tests` and inside files `__init__.py` and eg. `test_pets_views.py`.

### 9. Write tests

We will write two really simple tests into new file `test_pets_views.py`

```python
# app/pet/tests/test_pets_views.py

from fastapi import status
from httpx import AsyncClient

from app.auth.models import User
from app.main import app
from app.tests.factories import PetFactory


async def test_create_new_pet(
    client: AsyncClient, default_user_headers: dict[str, str], default_user: User
) -> None:
    response = await client.post(
        app.url_path_for("create_new_pet"),
        headers=default_user_headers,
        json={"pet_name": "Tadeusz"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    result = response.json()
    assert result["user_id"] == default_user.user_id
    assert result["pet_name"] == "Tadeusz"


async def test_get_all_my_pets(
    client: AsyncClient,
    default_user_headers: dict[str, str],
    default_user: User,
) -> None:
    pet1 = await PetFactory.create_async(
        user_id=default_user.user_id, pet_name="Alfred"
    )
    pet2 = await PetFactory.create_async(
        user_id=default_user.user_id, pet_name="Tadeusz"
    )

    response = await client.get(
        app.url_path_for("get_all_my_pets"),
        headers=default_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {
            "user_id": pet1.user_id,
            "pet_name": pet1.pet_name,
            "id": pet1.id,
        },
        {
            "user_id": pet2.user_id,
            "pet_name": pet2.pet_name,
            "id": pet2.id,
        },
    ]

```

## Design choices

There are couple decisions to make and changes that can/should be done after fork. I try to describe below things I consider most opinionated.

### Dockerfile

This template has by default included `Dockerfile` with [Uvicorn](https://www.uvicorn.org/) webserver, because it's simple in direct relation to FastAPI and great ease of configuration. You should be able to run container(s) (over :8000 port) and then need to setup the proxy, loadbalancer, with https enbaled, so the app stays behind it. Ye, **it's safe**(as much as anything is safe), you don't need anything except prefered LB. Other webservers to consider: [Nginx Unit](https://unit.nginx.org/), [Daphne](https://github.com/django/daphne), [Hypercorn](https://pgjones.gitlab.io/hypercorn/index.html).

### Registration

Is open. You would probably want to either remove it altogether or change.

### Delete user endpoint

Rethink `delete_current_user`, maybe you don't need it.

### JWT and refresh tokens

By using `/auth/access-token` user can exchange username + password for JWT. Refresh tokens is saved **in database table**. I've seen a lot of other, not always secure or sane setups. It's up to you if you want to change it to be also JWT (which seems to be popular), just one small note: It's `good` design if one can revoke all or preferably some refresh tokens. It's much `worse` design if one cannot. On the other hand, it's fine not to have option to revoke access tokens (as they are shortlived).

### Writing scripts / cron

Very rarely app has not some kind of background tasks. Feel free to use `new_script_async_session` if you need to have access to database outside of FastAPI. Cron can be simply: new file, async task with session (doing something), wrapped by `asyncio.run(script_func())`.

### Docs URL

Docs page is simply `/` (by default in FastAPI it is `/docs`). You can change it completely for the project, just as title, version, etc.

```python
app = FastAPI(
    title="minimal fastapi postgres template",
    version="7.0.0",
    description="https://github.com/rafsaf/minimal-fastapi-postgres-template",
    openapi_url="/openapi.json",
    docs_url="/",
)
```

### CORS

If you are not sure what are CORS for, follow [developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS). Most frontend frameworks nowadays operate on `http://localhost:3000` thats why it's included in `BACKEND_CORS_ORIGINS` in `.env` file, before going production be sure to include your frontend domain there, like `https://my-frontend-app.example.com`.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in config.settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Allowed Hosts

This middleware prevents HTTP Host Headers attack, you should put here your server IP or (preferably) full domain under which it's accessible like `example.com`. By default `"localhost", "127.0.0.1", "0.0.0.0"`

```python
app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.settings.ALLOWED_HOSTS)
```

## License

The code is under MIT License. It's here for educational purposes, created mainly to have a place where up-to-date Python and FastAPI software lives. Do whatever you want with this code.
