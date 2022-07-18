# base image
FROM python:3.10-slim-bullseye

#maintainer
LABEL DockerfileAuthor="LakesideMiners"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1


RUN apt-get update -y \
    && apt-get install libpq-dev pwgen gcc -y

RUN ls
#directory to store app source code
RUN mkdir /app

RUN touch "UWU"

RUN ls 
#switch to /app directory so that everything runs from here
WORKDIR /app
RUN touch "OwO"

RUN ls
#copy the app code to image working directory
COPY ./ /app

RUN ls /app
#let pip install required packages
RUN pip --root-user-action=ignore install -r requirements.txt

# not so long ago, in a dockerfile not so far away.
RUN echo "**** Starting Database Setup...****"

RUN python3 ./manage.py migrate

RUN echo "**** Installing SQL Files...****"

RUN python3 ./manage.py install_sql_files _all_

RUN echo "**** --> CREATING SUPERUSER / ADMINISTRATOR <--****"

RUN python3 ./manage.py createsuperuser

RUN echo "**** Initalizing Timezone Data...****"

RUN python3 ./manage.py init_timezones

RUN echo "**** Dynapages: Register Templates...****"

RUN python3 ./manage.py registertemplate

RUN echo "**** Dynapages: Register Widgets...****"

RUN python3 ./manage.py registerwidgets

RUN echo "**** Dynapages: Init Dynapages...****"

RUN python3 ./manage.py init_dynapages

RUN echo "*** Loading Disciplines and Categories (defaults): ***"

RUN python3 ./manage.py load_disciplines DOCUMENTATION/Categories/disciplines.tsv

RUN python3 ./manage.py load_categories DOCUMENTATION/Categories/categories.tsv

RUN echo "*** Creating Initial Community ***"

RUN python3 ./manage.py create_community

RUN echo "****** SETUP COMPLETE! Further parameters can be modified in 'config/settings.ini'! *****"

RUN echo "You may (now hopefully) start the Django environment using runserver! :3!"

RUN echo "Thank you for using Ply! :3 :3"

RUN python3 manage.py runserver 0.0.0.0:8000 
