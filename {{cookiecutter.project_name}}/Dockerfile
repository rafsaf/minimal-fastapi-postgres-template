FROM nginx/unit:1.25.0-python3.9

# Our Debian with Python and Nginx for python apps.
# See https://hub.docker.com/r/nginx/unit/
ENV PYTHONUNBUFFERED 1

COPY ./app/initial.sh /docker-entrypoint.d/initial.sh
COPY ./config/config.json /docker-entrypoint.d/config.json

RUN mkdir build

# We create folder named build for our app.
WORKDIR /build

COPY ./app ./app
COPY ./pytest.ini .
COPY ./aerich.ini .
COPY ./requirements.txt .
COPY ./.env .

# We copy our app folder to the /build

RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r requirements.txt                                       \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list