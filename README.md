## Small FastAPI template, all boring and tedious things covered

![OpenAPIexample](./docs/OpenAPI_example.png)

- SQLAlchemy using new 2.0 API + async queries
- Postgresql database under `asyncpg`
- Alembic migrations
- Very minimal project structure yet ready for quick start building new api
- Refresh token endpoint (not only access like in official template)
- Two databases in docker-compose.yml (second for tests)
- poetry
- `pre-push.sh` script with poetry export, autoflake, black, isort and flake8
- Setup for tests, one big test for token flow and very extensible `conftest.py`

## What this repo is

This is a minimal template for FastAPI backend + postgresql db as of 2021, `async` style for database sessions, endpoints and tests. It provides basic codebase that almost every application has, but nothing more.

## What this repo is not

It is not complex, full featured solutions for all human kind problems. It doesn't include any third party that isn't necessary for most of apps (dashboards, queues) or implementation differs so much in every project that it's pointless (complex user model, emails).

## Quickstart

```bash
# You can even install it globally
pip install cookiecutter

# And cookiecutter this project :)
cookiecutter https://github.com/rafsaf/minimal-fastapi-postgres-template

cd project_name
# Poetry install (and activate environment!)
poetry install
# Databases
docker-compose up -d
# Alembic migrations upgrade and initial_data.py script
bash init.sh
# And this is it:
uvicorn app.main:app
```

tests:

```bash
pytest
# Note, it will use second database declared in docker-compose.yml, not default one like
# in official template
```

## About

This project is heavily base on official template https://github.com/tiangolo/full-stack-fastapi-postgresql (and on my previous work: [link1](https://github.com/rafsaf/fastapi-plan), [link2](https://github.com/rafsaf/docker-fastapi-projects)), but as it is now not too much up-to-date, it is much easier to create new one than change official. I didn't like some of conventions over there also (`crud` and `db` folders for example).

`2.0` style SQLAlchemy API is good enough so there is no need to write everything in `crud` and waste our time... The `core` folder was also rewritten. There is great base for writting tests in `tests`, but I didn't want to write hundreds of them, I noticed that usually after changes in the structure of the project, auto tests are useless and you have to write them from scratch anyway (delete old ones...), hence less than more. Similarly with the `User` model, it is very modest, because it will be adapted to the project anyway (and there are no tests for these endpoints, you would remove them probably).

## Learn by example

Let's imagine we need to create API for a website where users brag about their dogs... or whatever, they just can crud dogs in user panel for some reason. We will add dummy model Dog to our API, with relation to the default table User and crud auth endpoints, then test it shortly.
