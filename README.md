# Full featured FastAPI template, all boring and tedious things are covered

- SQLAlchemy using new 2.0 API + async queries
- Postgresql database under `asyncpg`
- Alembic migrations
- Very minimal project structure yet ready for quick start building new api
- Refresh token endpoint (not only access like in official template)
- Two databases in docker-compose.yml (second for tests)
- poetry
- `pre-push.sh` script with poetry export, autoflake, black, isort and flake8
- Setup for tests, one big test for token flow and very extensible `conftest.py`

# Quickstart

```bash
# You can install it globally
pip install cookiecutter

# And cookiecutter this project :)
cookiecutter https://github.com/rafsaf/minimal-fastapi-postgres-template

cd project_name
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

# About

This project is heavily base on official template https://github.com/tiangolo/full-stack-fastapi-postgresql (and on my previous work: [link1](https://github.com/rafsaf/fastapi-plan), [link2](https://github.com/rafsaf/docker-fastapi-projects)), but as it is now not too much up-to-date, it is much easier to create new one than change official. I didn't like some of conventions over there also (`crud` and `db` folders for example).

`2.0` style SQLAlchemy API is good enough so there is no need to write everything in `crud` and waste our time... The `core` folder was also rewritten. There is great base for writting tests in `tests`, but I didn't want to write hundreds of them, I noticed that usually after changes in the structure of the project, auto tests are useless and you have to write them from scratch, hence less than more. Similarly with the `User` model, it is very modest, because it will be adapted to the project anyway (and there are no tests for these endpoints)
