FROM debian:latest

# Base install:
COPY /devops/docker_fs/. /
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3 build-essential wget bash python-dev-is-python3

# Install PostgreSQL: \
RUN sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get -y update
RUN apt-get -y install libpq-dev postgresql-client-16

# Virtual Env and code setup
RUN apt-get -y install python3.11-venv
RUN python3 -m venv /venv/
COPY  requirements.txt /tmp/requirements.txt
RUN bash -c 'source /venv/bin/activate; /venv/bin/pip install -r /tmp/requirements.txt;'

ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

COPY . /app

RUN python manage.py collectstatic --no-input

# Prevent startup without a mountpoint for the database:
# Finally, ports and entrypoint:
EXPOSE 8000
WORKDIR /app
CMD ["sh", "start.sh"]
