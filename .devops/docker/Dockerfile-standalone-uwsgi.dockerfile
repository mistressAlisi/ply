FROM debian:bookworm
RUN  apt-get update;



RUN  apt install -y postgresql-common;
RUN  /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y;

RUN apt-get install --no-install-recommends -y \
    openssl \
    build-essential \
    curl \
    xz-utils \
    ca-certificates \
    fontconfig \
    python3.11 \
    python3.11-venv \
    python-is-python3 \
    libpq-dev \
    python3.11-dev \
    uwsgi-plugin-python3 \
    uwsgi-emperor \
    uwsgi-plugin-alarm-xmpp \
    uwsgi-plugin-emperor-pg \
    uwsgi-plugin-geoip \
    uwsgi \
    nginx \
    rabbitmq-server \
    postgresql-client-16;




WORKDIR /app
ADD ../requirements.txt /app/requirements.txt
COPY .devops/docker_fs/etc/banner /etc/banner/
COPY .devops/docker_fs/usr/bin/* /usr/bin/
COPY .devops/docker_fs/usr/sbin/* /usr/sbin/
RUN set -ex \
    && apt-get -y install libgmp-dev \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt;

RUN apt-get clean




ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 80
EXPOSE 443
ADD .. /app
RUN python3 /app/manage.py collectstatic
RUN ln -s /etc/uwsgi/apps-available/ply.ini /etc/uwsgi/apps-enabled
CMD ["bash", "/usr/bin/docker_run_uwsgi-standalone.sh"]