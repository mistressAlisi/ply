FROM python:3.9.12-buster

ADD ../requirements.txt /app/requirements.txt

ADD .. /app
WORKDIR /app

ENV SECRET_KEY "supdocker"

RUN echo "deb http://http.debian.net/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://http.debian.net/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/ buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    openssl \
    build-essential \
    curl \
    xz-utils \
    ca-certificates \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-base \
    fonts-roboto \
    fonts-inconsolata \
    ttf-mscorefonts-installer \
    fontconfig \
    xorg

RUN set -ex \
    && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt install -fy xfonts-75dpi xfonts-base ./wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt-get -y install libgmp-dev \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && /env/bin/python manage.py collectstatic --noinput

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE $PORT

CMD ["bash", "start.sh"]