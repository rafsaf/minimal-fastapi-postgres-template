[![Live example](https://img.shields.io/badge/live%20example-https%3A%2F%2Fminimal--fastapi--postgres--template.rafsaf.pl-blueviolet)](https://minimal-fastapi-postgres-template.rafsaf.pl/)
[![License](https://img.shields.io/github/license/rafsaf/minimal-fastapi-postgres-template)](https://github.com/rafsaf/minimal-fastapi-postgres-template/blob/main/LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](https://docs.python.org/3/whatsnew/3.12.html)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Tests](https://github.com/rafsaf/minimal-fastapi-postgres-template/actions/workflows/tests.yml/badge.svg)](https://github.com/rafsaf/minimal-fastapi-postgres-template/actions/workflows/tests.yml)

# Minimal async FastAPI + PostgreSQL template

- [Minimal async FastAPI + PostgreSQL template](#minimal-async-fastapi--postgresql-template)
  - [Features](#features)
  - [Quickstart](#quickstart)
    - [1. Install cookiecutter globally and cookiecutter this project](#1-install-cookiecutter-globally-and-cookiecutter-this-project)
    - [2. Install dependecies with poetry or without it](#2-install-dependecies-with-poetry-or-without-it)
    - [3. Setup databases](#3-setup-databases)
    - [4. Now you can run app](#4-now-you-can-run-app)
    - [5. Activate pre-commit](#5-activate-pre-commit)
    - [6. Running tests](#6-running-tests)
  - [About](#about)
  - [Step by step example - POST and GET endpoints](#step-by-step-example---post-and-get-endpoints)
    - [1. Create SQLAlchemy model](#1-create-sqlalchemy-model)
    - [2. Create and apply alembic migration](#2-create-and-apply-alembic-migration)
    - [3. Create request and response schemas](#3-create-request-and-response-schemas)
    - [4. Create endpoints](#4-create-endpoints)
    - [5. Write tests](#5-write-tests)
  - [Deployment strategies - via Docker image](#deployment-strategies---via-docker-image)
  - [Docs URL, CORS and Allowed Hosts](#docs-url-cors-and-allowed-hosts)

## Features

- [x] SQLAlchemy 2.0, async queries, best possible autocompletion support
- [x] Postgresql database under `asyncpg`
- [x] [Alembic](https://alembic.sqlalchemy.org/en/latest/) migrations
- [x] Very minimal project structure yet ready for quick start building new apps
- [x] Refresh token endpoint (not only access like in official template)
- [x] Database in docker-compose.yml and ready to go Dockerfile with [uvicorn](https://www.uvicorn.org/) webserver
- [x] [Poetry](https://python-poetry.org/docs/) and Python 3.12 based
- [x] `pre-commit` hooks with [ruff](https://github.com/astral-sh/ruff)
- [x] **Perfect** pytest asynchronous test setup with +40 tests and full coverage

<br>

_Check out also online example: https://minimal-fastapi-postgres-template.rafsaf.pl, it's 100% code used in template (docker image) with added domain and https only._

<kbd>![template-fastapi-minimal-openapi-example](https://drive.google.com/uc?export=view&id=1rIXFJK8VyVrV7v4qgtPFryDd5FQrb4gr)</kbd>



## Quickstart

### 1. Install cookiecutter globally and cookiecutter this project

```bash
pip install cookiecutter

# And cookiecutter this project :)
cookiecutter https://github.com/rafsaf/minimal-fastapi-postgres-template

```

### 2. Install dependecies with poetry or without it

```bash
cd project_name
### Poetry install (python3.12)
poetry install

### Optionally there is also `requirements-dev.txt` file
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

Note, be sure to use `python3.12` with this template with either poetry or standard venv & pip, if you need to stick to some earlier python version, you should adapt it yourself (remove new versions specific syntax for example `str | int` for python < 3.10 or `tomllib` for python < 3.11)

### 3. Setup databases

```bash
### Setup two databases
docker-compose up -d

### Alembic migrations upgrade and initial_data.py script
bash init.sh
```

### 4. Now you can run app

```bash
### And this is it:
uvicorn app.main:app --reload

```

You should then use `git init` to initialize git repository and access OpenAPI spec at http://localhost:8000/ by default. To customize docs url, cors and allowed hosts settings, read section about it.

### 5. Activate pre-commit

[pre-commit](https://pre-commit.com/) is de facto standard now for pre push activities like isort or black.

Refer to `.pre-commit-config.yaml` file to see my opinionated choices.

```bash
# Install pre-commit
pre-commit install

# First initialization and run on all files
pre-commit run --all-files
```

### 6. Running tests

```bash
# Note, it will use second database declared in docker-compose.yml, not default one
pytest

# collected 7 items

# app/tests/test_auth.py::test_auth_access_token PASSED                                                                       [ 14%]
# app/tests/test_auth.py::test_auth_access_token_fail_no_user PASSED                                                          [ 28%]
# app/tests/test_auth.py::test_auth_refresh_token PASSED                                                                      [ 42%]
# app/tests/test_users.py::test_read_current_user PASSED                                                                      [ 57%]
# app/tests/test_users.py::test_delete_current_user PASSED                                                                    [ 71%]
# app/tests/test_users.py::test_reset_current_user_password PASSED                                                            [ 85%]
# app/tests/test_users.py::test_register_new_user PASSED                                                                      [100%]
#
# ======================================================== 7 passed in 1.75s ========================================================
```

<br>

## About

This project is heavily based on the official template https://github.com/tiangolo/full-stack-fastapi-postgresql (and on my previous work: [link1](https://github.com/rafsaf/fastapi-plan), [link2](https://github.com/rafsaf/docker-fastapi-projects)), but as it now not too much up-to-date, it is much easier to create new one than change official. I didn't like some of conventions over there also (`crud` and `db` folders for example or `schemas` with bunch of files). This template aims to be as much up-to-date as possible, using only newest python versions and libraries versions.

`2.0` style SQLAlchemy API is good enough so there is no need to write everything in `crud` and waste our time... The `core` folder was also rewritten. There is great base for writting tests in `tests`, but I didn't want to write hundreds of them, I noticed that usually after changes in the structure of the project, auto tests are useless and you have to write them from scratch anyway (delete old ones...), hence less than more. Similarly with the `User` model, it is very modest, with just `id` (uuid), `email` and `password_hash`, because it will be adapted to the project anyway.

<br>

## Step by step example - POST and GET endpoints

I always enjoy to have some kind of an example in templates (even if I don't like it much, _some_ parts may be useful and save my time...), so let's create two example endpoints:

- `POST` endpoint `/pets/create` for creating `Pets` with relation to currently logged `User`
- `GET` endpoint `/pets/me` for fetching all user's pets.

<br>

### 1. Create SQLAlchemy model

We will add Pet model to `app/models.py`. To keep things clear, below is full result of models.py file.

```python
# app/models.py

import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_model"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)


class Pet(Base):
    __tablename__ = "pet"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user_model.id", ondelete="CASCADE"),
    )
    pet_name: Mapped[str] = mapped_column(String(50), nullable=False)



```

Note, we are using super powerful SQLAlchemy feature here - Mapped and mapped_column were first introduced in SQLAlchemy 2.0 on Feb 26, if this syntax is new for you, read carefully "what's new" part of documentation https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html.

<br>

### 2. Create and apply alembic migration

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

PS. Note, alembic is configured in a way that it work with async setup and also detects specific column changes.

<br>

### 3. Create request and response schemas

I personally lately (after seeing clear benefits at work in Samsung) prefer less files than a lot of them for things like schemas.

Thats why there are only 2 files: `requests.py` and `responses.py` in `schemas` folder and I would keep it that way even for few dozen of endpoints. Not to mention this is opinionated.

```python
# app/schemas/requests.py

(...)


class PetCreateRequest(BaseRequest):
    pet_name: str

```

```python
# app/schemas/responses.py

(...)


class PetResponse(BaseResponse):
    id: int
    pet_name: str
    user_id: str

```

<br>

### 4. Create endpoints

```python
# /app/api/endpoints/pets.py

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Pet, User
from app.schemas.requests import PetCreateRequest
from app.schemas.responses import PetResponse

router = APIRouter()


@router.post("/create", response_model=PetResponse, status_code=201)
async def create_new_pet(
    new_pet: PetCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Creates new pet. Only for logged users."""

    pet = Pet(user_id=current_user.id, pet_name=new_pet.pet_name)

    session.add(pet)
    await session.commit()
    return pet


@router.get("/me", response_model=list[PetResponse], status_code=200)
async def get_all_my_pets(
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Get list of pets for currently logged user."""

    stmt = select(Pet).where(Pet.user_id == current_user.id).order_by(Pet.pet_name)
    pets = await session.execute(stmt)
    return pets.scalars().all()

```

Also, we need to add newly created endpoints to router.

```python
# /app/api/api.py

from fastapi import APIRouter

from app.api.endpoints import auth, pets, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(pets.router, prefix="/pets", tags=["pets"])

```

<br>

### 5. Write tests

```python
# /app/tests/test_pets.py

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import Pet, User


async def test_create_new_pet(
    client: AsyncClient, default_user_headers, default_user: User
):
    response = await client.post(
        app.url_path_for("create_new_pet"),
        headers=default_user_headers,
        json={"pet_name": "Tadeusz"},
    )
    assert response.status_code == 201
    result = response.json()
    assert result["user_id"] == default_user.id
    assert result["pet_name"] == "Tadeusz"


async def test_get_all_my_pets(
    client: AsyncClient, default_user_headers, default_user: User, session: AsyncSession
):
    pet1 = Pet(user_id=default_user.id, pet_name="Pet_1")
    pet2 = Pet(user_id=default_user.id, pet_name="Pet_2")
    session.add(pet1)
    session.add(pet2)
    await session.commit()

    response = await client.get(
        app.url_path_for("get_all_my_pets"),
        headers=default_user_headers,
    )
    assert response.status_code == 200

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

## Deployment strategies - via Docker image

This template has by default included `Dockerfile` with [Uvicorn](https://www.uvicorn.org/) webserver, because it's simple and just for showcase purposes, with direct relation to FastAPI and great ease of configuration. You should be able to run container(s) (over :8000 port) and then need to setup the proxy, loadbalancer, with https enbaled, so the app stays behind it.

If you prefer other webservers for FastAPI, check out [Nginx Unit](https://unit.nginx.org/), [Daphne](https://github.com/django/daphne), [Hypercorn](https://pgjones.gitlab.io/hypercorn/index.html).

## Docs URL, CORS and Allowed Hosts

There are some **opinionated** default settings in `/app/main.py` for documentation, CORS and allowed hosts.

1. Docs

   ```python
   app = FastAPI(
       title=config.settings.PROJECT_NAME,
       version=config.settings.VERSION,
       description=config.settings.DESCRIPTION,
       openapi_url="/openapi.json",
       docs_url="/",
   )
   ```

   Docs page is simpy `/` (by default in FastAPI it is `/docs`). Title, version and description are taken directly from `config` and then directly from `pyproject.toml` file. You can change it completely for the project, remove or use environment variables `PROJECT_NAME`, `VERSION`, `DESCRIPTION`.

2. CORS

   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[str(origin) for origin in config.settings.BACKEND_CORS_ORIGINS],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

   If you are not sure what are CORS for, follow https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS. React and most frontend frameworks nowadays operate on `http://localhost:3000` thats why it's included in `BACKEND_CORS_ORIGINS` in .env file, before going production be sure to include your frontend domain here, like `https://my-fontend-app.example.com`.

3. Allowed Hosts

   ```python
   app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.settings.ALLOWED_HOSTS)
   ```

   Prevents HTTP Host Headers attack, you shoud put here you server IP or (preferably) full domain under it's accessible like `example.com`. By default in .env there are two most popular records: `ALLOWED_HOSTS=["localhost", "127.0.0.1"]`
