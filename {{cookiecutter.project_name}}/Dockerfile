# See https://unit.nginx.org/installation/#docker-images

FROM nginx/unit:1.28.0-python3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y python3-pip

# Build folder for our app, only stuff that matters copied.
RUN mkdir build
WORKDIR /build

# Update, install requirements and then cleanup.
COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get remove -y python3-pip  \
    && apt-get autoremove --purge -y  \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

# Copy the rest of app
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY pyproject.toml .

# Nginx unit config and init.sh will be consumed at container startup.
COPY init.sh /docker-entrypoint.d/init.sh
COPY nginx-unit-config.json /docker-entrypoint.d/config.json
RUN chmod a+x /docker-entrypoint.d/init.sh