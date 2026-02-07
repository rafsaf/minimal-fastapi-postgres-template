FROM python:3.14-slim-trixie AS base

ENV PYTHONUNBUFFERED=1
WORKDIR /build

# Create requirements.txt file
FROM base AS uv
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /uvx /bin/
COPY uv.lock pyproject.toml ./
RUN uv export --no-dev --no-hashes -o /requirements.txt --no-install-workspace --frozen
RUN uv export --only-group dev --no-hashes -o /requirements-dev.txt --no-install-workspace --frozen

FROM base AS final
COPY --from=uv /requirements.txt .

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

# Expose port 8000 for app and optional 9090 for prometheus metrics
EXPOSE 8000
EXPOSE 9090

# Make the init script executable
RUN chmod +x ./init.sh

# Set ENTRYPOINT to always run init.sh
ENTRYPOINT ["./init.sh"]

# Set CMD to uvicorn
# /venv/bin/uvicorn is used because from entrypoint script PATH is new
CMD ["/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--loop", "uvloop"]