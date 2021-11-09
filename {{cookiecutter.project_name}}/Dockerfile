# See https://unit.nginx.org/installation/#docker-images

FROM nginx/unit:1.25.0-python3.9

ENV PYTHONUNBUFFERED 1

# Nginx unit config and init.sh will be consumed at container startup.
COPY ./app/init.sh /docker-entrypoint.d/init.sh
COPY ./nginx-unit-config.json /docker-entrypoint.d/config.json
RUN chmod +x /docker-entrypoint.d/init.sh

# Build folder for our app, only stuff that matters copied.
RUN mkdir build
WORKDIR /build

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini .
COPY ./requirements.txt .

# Update, install requirements and then cleanup.
RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r requirements.txt                                       \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list