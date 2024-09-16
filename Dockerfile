FROM python:3.12.6-slim-bullseye as base

ENV PYTHONUNBUFFERED 1
WORKDIR /build

# Create requirements.txt file
FROM base as poetry
RUN pip install poetry==1.8.2
COPY poetry.lock pyproject.toml ./
RUN poetry export -o /requirements.txt --without-hashes

FROM base as common
COPY --from=poetry /requirements.txt .
# Create venv, add it to path and install requirements
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install -r requirements.txt

# Install uvicorn server
RUN pip install uvicorn[standard]

# Copy the rest of app
COPY app app
COPY alembic alembic
COPY alembic.ini .
COPY pyproject.toml .
COPY init.sh .

# Create new user to run app process as unprivilaged user
RUN addgroup --gid 1001 --system uvicorn && \
    adduser --gid 1001 --shell /bin/false --disabled-password --uid 1001 uvicorn

# Run init.sh script then start uvicorn
RUN chown -R uvicorn:uvicorn /build
CMD bash init.sh && \
    runuser -u uvicorn -- /venv/bin/uvicorn app.main:app --app-dir /build --host 0.0.0.0 --port 8000 --workers 2 --loop uvloop
EXPOSE 8000